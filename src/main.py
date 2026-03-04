import asyncio
import random
import logging
import json
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SKYGUARD-OS")

app = FastAPI(title="Teknofest Sanayide Dijital Teknolojiler")

# Statik dosyalar ve şablonlar
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

class DijitalIkiz:
    """
    Fiziksel bir AMR'nin dijital kopyası.
    Batarya, Posizyon ve Hareket durumunu simüle eder.
    """
    def __init__(self, cihaz_id: str):
        self.cihaz_id = cihaz_id
        self.battery = 100.0
        self.voltage = 24.0
        self.current = 0.5
        self.speed = 0.0
        self.pos = {"x": 0.0, "y": 0.0}
        self.target = None
        self.emergency = False
        self.status = "IDLE"

    def update(self):
        """Her tick'te robot durumunu günceller"""
        if self.emergency:
            self.speed = 0
            self.status = "EMERGENCY_STOP"
            return

        if self.target:
            self.status = "NAVIGATING"
            dx = self.target["x"] - self.pos["x"]
            dy = self.target["y"] - self.pos["y"]
            dist = (dx**2 + dy**2)**0.5
            
            if dist < 0.1:
                self.pos = self.target.copy()
                self.target = None
                self.speed = 0
                self.status = "IDLE"
            else:
                self.speed = 1.2 # m/s (Simüle)
                move_dist = 0.2 # Tick başına hareket
                self.pos["x"] += (dx / dist) * move_dist
                self.pos["y"] += (dy / dist) * move_dist
        
        # Batarya tüketimi simülasyonu
        consumption = 0.001 if self.status == "IDLE" else 0.01
        self.battery = max(0, self.battery - consumption)
        self.voltage = 22.0 + (self.battery / 100 * 4.0)
        self.current = 0.5 + (1.5 if self.status == "NAVIGATING" else 0)

    def get_state(self) -> Dict:
        return {
            "id": self.cihaz_id,
            "battery": round(self.battery, 1),
            "voltage": round(self.voltage, 2),
            "current": round(self.current, 2),
            "speed": round(self.speed, 2),
            "pos": {"x": round(self.pos["x"], 2), "y": round(self.pos["y"], 2)},
            "emergency": self.emergency,
            "status": self.status
        }

class FabrikaSimulasyonu:
    def __init__(self):
        self.robot = DijitalIkiz("SKYGUARD-01")
        self.stations = {
            'A1': {'x': 2, 'y': 2}, 'A2': {'x': 6, 'y': 2}, 'A3': {'x': 10, 'y': 2}, 'A4': {'x': 14, 'y': 2},
            'B1': {'x': 2, 'y': 12}, 'B2': {'x': 6, 'y': 12}, 'B3': {'x': 10, 'y': 12}, 'B4': {'x': 14, 'y': 12},
            'START': {'x': 0, 'y': 0}, 'CHRG': {'x': 17, 'y': 7}
        }

    async def veri_uret(self) -> Dict:
        """Robot verilerini üretir ve dijital ikizi günceller."""
        self.robot.update()
        return {
            "zaman": datetime.now().strftime("%H:%M:%S"),
            "robot": self.robot.get_state()
        }

    def komut_isle(self, komut: Dict):
        action = komut.get("action")
        if action == "GOTO":
            station_id = komut.get("station")
            if station_id in self.stations:
                self.robot.target = self.stations[station_id]
                logger.info(f"Yönlendirme: {station_id}")
        elif action == "EMERGENCY_STOP":
            self.robot.emergency = True
            logger.warning("ACİL DURDURMA TETİKLENDİ")
        elif action == "RESET":
            self.robot.emergency = False
            logger.info("Sistem Resetlendi")

simulasyon = FabrikaSimulasyonu()

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/command")
async def handle_command(request: Request):
    komut = await request.json()
    simulasyon.komut_isle(komut)
    return {"status": "success"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Gerçek zamanlı veri akışı (100ms gecikme ile hızlı simülasyon)
            veri = await simulasyon.veri_uret()
            await websocket.send_json(veri)
            await asyncio.sleep(1) # Saniyede 1 güncelleme
    except Exception as e:
        logger.error(f"WebSocket hatası: {e}")
    finally:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
