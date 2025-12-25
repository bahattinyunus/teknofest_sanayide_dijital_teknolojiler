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
logger = logging.getLogger("EndustriyelSistem")

app = FastAPI(title="Teknofest Sanayide Dijital Teknolojiler")

# Statik dosyalar ve şablonlar
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

class DijitalIkiz:
    """
    Fiziksel bir varlığın dijital kopyası.
    Verimlilik ve Sağlık durumunu analiz eder.
    """
    def __init__(self, cihaz_id: str):
        self.cihaz_id = cihaz_id
        self.nominal_sicaklik = 45.0
        self.saglik_puani = 100.0
        self.verimlilik = 100.0

    def durumu_guncelle(self, sensor_verisi: Dict):
        """Sensör verisine göre dijital ikizi günceller"""
        deger = sensor_verisi["metrikler"]["deger"]
        tip = sensor_verisi["tip"]

        if tip == "SICAKLIK":
            # Sıcaklık farkına göre verimlilik düşüşü simülasyonu
            sapma = abs(deger - self.nominal_sicaklik)
            if sapma > 10:
                self.verimlilik = max(0, 100 - (sapma * 1.5))
                self.saglik_puani -= 0.1
            else:
                self.verimlilik = min(100, self.verimlilik + 0.5)

    def get_durum(self) -> Dict:
        return {
            "cihaz_id": self.cihaz_id,
            "saglik": round(self.saglik_puani, 2),
            "verimlilik": round(self.verimlilik, 2),
            "durum": "KRİTİK" if self.saglik_puani < 50 else "NORMAL"
        }

class FabrikaSimulasyonu:
    def __init__(self):
        self.cihazlar = ["TR-M01", "TR-M02", "TR-K01"]
        self.ikizler = {c: DijitalIkiz(c) for c in self.cihazlar}

    async def veri_uret(self) -> Dict:
        """Fabrika verilerini üretir ve dijital ikizleri günceller."""
        paket = {
            "zaman": datetime.now().strftime("%H:%M:%S"),
            "sensorler": [],
            "analitik": []
        }

        for cihaz_id in self.cihazlar:
            # Sensör Verisi Simülasyonu
            sicaklik = round(random.normalvariate(45, 5), 1)
            basinc = round(random.normalvariate(5, 0.5), 1)
            
            # Dijital İkiz Güncelleme
            ikiz = self.ikizler[cihaz_id]
            ikiz.durumu_guncelle({"tip": "SICAKLIK", "metrikler": {"deger": sicaklik}})
            
            paket["sensorler"].append({
                "id": cihaz_id,
                "sicaklik": sicaklik,
                "basinc": basinc
            })
            paket["analitik"].append(ikiz.get_durum())
            
        return paket

simulasyon = FabrikaSimulasyonu()

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
