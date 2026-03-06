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
                self.path = []
            else:
                self.speed = 1.2 # m/s (Simüle)
                move_dist = 0.2 # Tick başına hareket
                self.pos["x"] += (dx / dist) * move_dist
                self.pos["y"] += (dy / dist) * move_dist
                # Breadcrumb path calculation
                self.path = [
                    {"x": round(self.pos["x"] + (dx/dist)*i*2, 1), "y": round(self.pos["y"] + (dy/dist)*i*2, 1)}
                    for i in range(1, 4)
                ]
        else:
            self.path = []
        
        # Batarya tüketimi simülasyonu
        consumption = 0.001 if self.status == "IDLE" else 0.01
        self.battery = max(0, self.battery - consumption)
        self.voltage = 22.0 + (self.battery / 100 * 4.0)
        self.current = 0.5 + (1.5 if self.status == "NAVIGATING" else 0)

        # Anomaly detection simulation
        if random.random() < 0.001: # 0.1% chance of anomaly per tick
            self.anomaly_detected = True
            logger.warning(f"ANOMALY DETECTED [{self.cihaz_id}]")
        elif self.anomaly_detected and random.random() < 0.1: # 10% chance to clear anomaly if present
            self.anomaly_detected = False


    def get_state(self) -> Dict:
        return {
            "id": self.cihaz_id,
            "battery": round(self.battery, 1),
            "voltage": round(self.voltage, 2),
            "current": round(self.current, 2),
            "speed": round(self.speed, 2),
            "pos": {"x": round(self.pos["x"], 2), "y": round(self.pos["y"], 2)},
            "path": self.path,
            "emergency": self.emergency,
            "status": self.status,
            "anomaly": self.anomaly_detected
        }

class FabrikaSimulasyonu:
    def __init__(self):
        self.robots = {
            "SKYGUARD-01": DijitalIkiz("SKYGUARD-01"),
            "SKYGUARD-02": DijitalIkiz("SKYGUARD-02")
        }
        # SKYGUARD-02 starting position offset
        self.robots["SKYGUARD-02"].pos = {"x": 17.0, "y": 14.0}
        
        self.stations = {
            'A1': {'x': 2, 'y': 2}, 'A2': {'x': 6, 'y': 2}, 'A3': {'x': 10, 'y': 2}, 'A4': {'x': 14, 'y': 2},
            'B1': {'x': 2, 'y': 12}, 'B2': {'x': 6, 'y': 12}, 'B3': {'x': 10, 'y': 12}, 'B4': {'x': 14, 'y': 12},
            'START': {'x': 0, 'y': 0}, 'CHRG': {'x': 17, 'y': 7}
        }

    async def veri_uret(self) -> Dict:
        """Robot verilerini üretir, günceller ve veritabanına kaydeder."""
        fleet_state = {}
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        for rid, robot in self.robots.items():
            robot.update()
            state = robot.get_state()
            fleet_state[rid] = state
            
            # Simulate logging to a database for some events
            if random.random() < 0.05: # 5% chance to log state for each robot
                self.log_to_db(timestamp, state)

        return {
            "zaman": timestamp,
            "fleet": fleet_state
        }

    def log_to_db(self, timestamp: str, state: Dict):
        """Simulates logging robot state to a database."""
        logger.debug(f"DB LOG [{state['id']}] @ {timestamp}: {state['status']}")

    def komut_isle(self, komut: Dict):
        action = komut.get("action")
        target_id = komut.get("robot_id", "SKYGUARD-01")
        robot = self.robots.get(target_id)
        
        if not robot: 
            logger.warning(f"Robot bulunamadı: {target_id}")
            return

        if action == "GOTO":
            station_id = komut.get("station")
            if station_id in self.stations:
                robot.target = self.stations[station_id]
                logger.info(f"Yönlendirme [{target_id}]: {station_id}")
        elif action == "EMERGENCY_STOP":
            robot.emergency = True
            logger.warning(f"ACİL DURDURMA TETİKLENDİ [{target_id}]")
        elif action == "RESET":
            robot.emergency = False
            logger.info(f"Sistem Resetlendi [{target_id}]")

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
