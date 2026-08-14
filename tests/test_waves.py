from systems.waves import WaveController
from settings import GameSettings


def test_wave_grows_with_number():
    st = GameSettings.default().derive(enemies_per_wave=15, waves_per_boss=5)
    w = WaveController(st)
    assert len(w.build_wave_events(5)) > len(w.build_wave_events(2))


def test_boss_every_nwaves():
    st = GameSettings.default().derive(enemies_per_wave=5, waves_per_boss=5)
    w = WaveController(st)
    assert "boss" in [k for _, k in w.build_wave_events(5)]
    assert "boss" not in [k for _, k in w.build_wave_events(4)]