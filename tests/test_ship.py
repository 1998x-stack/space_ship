import pygame
from entities.ship import Ship
from settings import GameSettings

pygame.init()
IMG = pygame.Surface((40, 40))


def keys(pressed):
    base = {getattr(pygame, n): False for n in
            ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_SPACE"]}
    base.update(pressed)
    return base


def test_moves_right():
    s = Ship(IMG, GameSettings.default().derive(player_speed=100.0))
    x0 = s.rect.centerx
    s.update(1.0, keys({pygame.K_RIGHT: True}))
    assert s.rect.centerx > x0


def test_hits_decrease_lives():
    s = Ship(IMG, GameSettings.default().derive(player_lives=3))
    assert s.take_hit() is True
    assert s.lives == 2


def test_invulnerability_blocks_damage():
    st = GameSettings.default().derive(player_lives=3, invuln_time=1.0)
    s = Ship(IMG, st)
    s.take_hit()
    assert s.take_hit() is False
    s.update(1.5, keys({}))
    assert s.take_hit() is True


def test_add_life_caps_at_starting():
    s = Ship(IMG, GameSettings.default().derive(player_lives=3))
    s.add_life()
    assert s.lives == 3