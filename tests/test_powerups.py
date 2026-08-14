import pygame
from entities.powerups import PowerUp
from entities.explosion import Explosion

pygame.init()
IMG = pygame.Surface((20, 20))


def test_powerup_moves_down():
    p = PowerUp("weapon", IMG, (10, 10), speed=100.0)
    y0 = p.rect.y
    p.update(0.1)
    assert p.rect.y > y0


def test_explosion_removes_after_frames():
    g = pygame.sprite.Group()
    imgs = [pygame.Surface((5, 5)) for _ in range(3)]
    e = Explosion(imgs, (10, 10), frame_rate=0.05)
    g.add(e)
    for _ in range(4):
        e.update(0.05)
    assert not g