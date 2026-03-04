import pytest
from src.main import DijitalIkiz, FabrikaSimulasyonu

def test_dijital_ikiz_initial_state():
    """Dijital İkizin başlangıç durumunu doğrular"""
    ikiz = DijitalIkiz("TEST-ROBOT")
    state = ikiz.get_state()
    
    assert state["id"] == "TEST-ROBOT"
    assert state["battery"] == 100.0
    assert state["status"] == "IDLE"
    assert state["pos"] == {"x": 0.0, "y": 0.0}

def test_dijital_ikiz_movement():
    """Robotun hareket mantığını test eder"""
    ikiz = DijitalIkiz("TEST-ROBOT")
    ikiz.target = {"x": 1.0, "y": 0.0}
    
    # 1 tick güncelle
    ikiz.update()
    
    state = ikiz.get_state()
    assert state["status"] == "NAVIGATING"
    assert state["pos"]["x"] > 0
    assert state["speed"] > 0
    assert state["battery"] < 100.0

def test_emergency_stop():
    """Acil durdurma mantığını test eder"""
    ikiz = DijitalIkiz("TEST-ROBOT")
    ikiz.target = {"x": 5.0, "y": 5.0}
    ikiz.emergency = True
    
    ikiz.update()
    
    state = ikiz.get_state()
    assert state["status"] == "EMERGENCY_STOP"
    assert state["speed"] == 0
    assert state["pos"] == {"x": 0.0, "y": 0.0}

@pytest.mark.asyncio
async def test_simulasyon_output():
    """Simülasyonun ürettiği veri paketini doğrular"""
    sim = FabrikaSimulasyonu()
    paket = await sim.veri_uret()
    
    assert "zaman" in paket
    assert "robot" in paket
    assert paket["robot"]["id"] == "SKYGUARD-01"
