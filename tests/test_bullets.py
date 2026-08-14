import pygame
from entities.weapons import Weapon

pygame.init()
IMG = pygame.Surface((8, 8))


def test_weapon_fires_patterns():
    g = pygame.sprite.Group()
    w = Weapon(laser_cooldown=0.0, bullet_speed=500.0)
    assert len(w.fire(g, 100, 100, IMG)) == 1
    w.upgrade()
    assert len(w.fire(g, 100, 100, IMG)) == 3


def test_weapon_level_caps():
    w = Weapon(0.2, 500.0)
    for _ in range(10):
        w.upgrade()
    assert w.level == 3


def test_cooldown_blocks_rapid_fire():
    g = pygame.sprite.Group()
    w = Weapon(laser_cooldown=0.2, bullet_speed=500.0)
    w.fire(g, 100, 100, IMG)
    assert w.fire(g, 100, 100, IMG) == []
    w.arms(0.3)
    assert len(w.fire(g, 100, 100, IMG)) == 1