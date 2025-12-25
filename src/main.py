import asyncio
import random
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Loglama yapılandırması - Endüstriyel standart
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SİSTEM] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("EndustriyelKontrol")

class SensorDugumu:
    """
    Endüstriyel bir IoT sensörünü simüle eder.
    Sıcaklık, Basınç ve Titreşim verileri üretir.
    """
    def __init__(self, cihaz_id: str, tip: str):
        self.cihaz_id = cihaz_id
        self.tip = tip
        self.durum = "AKTİF"

    async def veri_olustur(self) -> Dict[str, Any]:
        """Sensörden asenkron veri okuma simülasyonu"""
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        veri = {
            "zaman_damgasi": datetime.now().isoformat(),
            "cihaz_id": self.cihaz_id,
            "tip": self.tip,
            "metrikler": {}
        }

        if self.tip == "SICAKLIK":
            veri["metrikler"]["deger"] = round(random.uniform(20.0, 85.0), 2)
            veri["metrikler"]["birim"] = "Celsius"
        elif self.tip == "BASINC":
            veri["metrikler"]["deger"] = round(random.uniform(1.0, 10.0), 2)
            veri["metrikler"]["birim"] = "Bar"
        elif self.tip == "TITRESIM":
            veri["metrikler"]["deger"] = round(random.uniform(0.0, 5.0), 3)
            veri["metrikler"]["birim"] = "mm/s"
            
        return veri

class VeriToplayici:
    """
    Farklı sensörlerden gelen verileri toplar ve analiz eder.
    """
    def __init__(self):
        self.veritabani_baglantisi = False
        
    async def baslat(self):
        logger.info("Veri Toplayıcı başlatılıyor...")
        self.veritabani_baglantisi = True
        logger.info("Bulut veritabanı bağlantısı kuruldu: [GÜVENLİ SSL/TLS]")

    async def veriyi_isle(self, veri: Dict[str, Any]):
        """Gelen veriyi işler ve anomali tespiti yapar"""
        deger = veri["metrikler"]["deger"]
        cihaz = veri["cihaz_id"]
        
        log_mesaji = f"Veri alındı: {cihaz} -> {deger} {veri['metrikler']['birim']}"
        
        # Basit Anomali Tespiti Simülasyonu
        if (veri["tip"] == "SICAKLIK" and deger > 80.0) or \
           (veri["tip"] == "BASINC" and deger > 9.0):
            logger.warning(f"KRİTİK UYARI: {cihaz} üzerinde eşik değer aşıldı! Değer: {deger}")
        else:
            logger.info(log_mesaji)

async def ana_dongu():
    logger.info("TEKNOFEST Endüstriyel Kontrol Sistemi v1.0 başlatılıyor...")
    
    toplayici = VeriToplayici()
    await toplayici.baslat()
    
    sensorler = [
        SensorDugumu("TR-41-M01", "SICAKLIK"),
        SensorDugumu("TR-41-M02", "BASINC"),
        SensorDugumu("TR-41-M03", "TITRESIM"),
        SensorDugumu("TR-61-K01", "SICAKLIK")
    ]
    
    try:
        while True:
            gorevler = [sensor.veri_olustur() for sensor in sensorler]
            sonuclar = await asyncio.gather(*gorevler)
            
            for sonuc in sonuclar:
                await toplayici.veriyi_isle(sonuc)
                
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Sistem kapatılıyor...")

if __name__ == "__main__":
    asyncio.run(ana_dongu())
