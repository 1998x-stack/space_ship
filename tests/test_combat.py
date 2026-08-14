import pygame
from entities.monsters import make_monster
from entities.bullets import PlayerBullet
from systems import combat
from settings import GameSettings

pygame.init()
IMG = pygame.Surface((30, 30))


def test_bullets_kill_monster():
    m = make_monster("drone", IMG, settings=GameSettings.default())
    m.rect = pygame.Rect(0, 0, 30, 30)
    group = pygame.sprite.Group(m)
    b = PlayerBullet(IMG, (15, 15), 100.0)
    killed = combat.resolve_bullets(group, pygame.sprite.Group(b))
    assert m in killed
    assert not group


def test_player_overlap_removes_enemy():
    m = make_monster("drone", IMG, settings=GameSettings.default())
    m.rect = pygame.Rect(0, 0, 30, 30)
    group = pygame.sprite.Group(m)
    player = pygame.sprite.Sprite()
    player.rect = pygame.Rect(10, 10, 30, 30)
    hits = combat.resolve_player(group, player)
    assert m in hits
    assert not group


def test_enemy_bullet_hits_player():
    from entities.bullets import EnemyBullet
    b = EnemyBullet(IMG, (15, 15), (0, 100.0))
    player = pygame.sprite.Sprite()
    player.rect = pygame.Rect(0, 0, 40, 40)
    assert combat.resolve_enemy_bullets(pygame.sprite.Group([b]), player) is True