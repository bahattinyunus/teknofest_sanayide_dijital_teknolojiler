import pytest
import asyncio
from src.main import SensorDugumu

@pytest.mark.asyncio
async def test_sensor_veri_olusturma():
    """Sensörün geçerli veri formatı üretip üretmediğini test eder."""
    sensor = SensorDugumu("TEST-01", "SICAKLIK")
    veri = await sensor.veri_olustur()
    
    assert veri["cihaz_id"] == "TEST-01"
    assert veri["tip"] == "SICAKLIK"
    assert "metrikler" in veri
    assert "deger" in veri["metrikler"]
    assert veri["metrikler"]["birim"] == "Celsius"

@pytest.mark.asyncio
async def test_sensor_araliklari():
    """Sensör verilerinin mantıklı aralıklarda olduğunu doğrular."""
    sensor = SensorDugumu("TEST-02", "BASINC")
    veri = await sensor.veri_olustur()
    deger = veri["metrikler"]["deger"]
    
    # Basınç 1.0 ile 10.0 bar arasında olmalı (main.py'deki mantığa göre)
    assert 1.0 <= deger <= 10.0
