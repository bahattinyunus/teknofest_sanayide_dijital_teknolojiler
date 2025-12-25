import pytest
import datetime
from src.main import DijitalIkiz, FabrikaSimulasyonu

def test_dijital_ikiz_logic():
    """Dijital İkizin sıcaklık değişimine tepkisini test eder"""
    ikiz = DijitalIkiz("TEST-UNIT")
    
    # Başlangıç durumu
    assert ikiz.verimlilik == 100.0
    
    # Yüksek sıcaklık (Anomali) gönder
    anomali_verisi = {
        "tip": "SICAKLIK",
        "metrikler": {"deger": 60.0} # Nominal 45, Fark 15 > 10
    }
    ikiz.durumu_guncelle(anomali_verisi)
    
    # Verimlilik düşmeli
    assert ikiz.verimlilik < 100.0
    assert ikiz.saglik_puani < 100.0

@pytest.mark.asyncio
async def test_simulasyon_veri_yapisi():
    """Simülasyonun ürettiği veri paketinin yapısını doğrular"""
    sim = FabrikaSimulasyonu()
    paket = await sim.veri_uret()
    
    assert "zaman" in paket
    assert "sensorler" in paket
    assert "analitik" in paket
    assert len(paket["sensorler"]) == 3
    assert len(paket["analitik"]) == 3
    
    # Sensör veri tipleri kontrolü
    sensor = paket["sensorler"][0]
    assert isinstance(sensor["sicaklik"], float)
    assert isinstance(sensor["basinc"], float)
