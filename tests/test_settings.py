import pytest
from settings import GameSettings


def test_default_valid():
    assert GameSettings.default().validate() == []


@pytest.mark.parametrize("bad", [
    {"width": 0}, {"height": -1}, {"fps": 0}, {"player_speed": -1.0},
    {"player_lives": 0}, {"laser_cooldown": -0.1}, {"enemies_per_wave": 0},
    {"waves_per_boss": 0}, {"boss_hp": 0}, {"powerup_drop_chance": 1.5},
])
def test_invalid_values_rejected(bad):
    s = GameSettings.default().derive(**bad)
    assert s.validate() != []