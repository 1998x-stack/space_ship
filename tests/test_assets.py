import pygame
from assets import AssetManager
from settings import GameSettings

pygame.init()


def test_loads_ship_and_fallback():
    am = AssetManager(GameSettings.default())
    assert am.image("does_not_exist.png", (20, 20)).get_size() == (20, 20)
    assert am.sound("missing.wav") is None


def test_caches_images():
    am = AssetManager(GameSettings.default())
    a = am.image("x.png", (10, 20))
    b = am.image("x.png", (10, 20))
    assert a is b