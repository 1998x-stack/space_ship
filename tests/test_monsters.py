import pygame
from entities.monsters import MONSTER_TEMPLATES, make_monster
from entities.boss import Boss
from settings import GameSettings

pygame.init()
IMG = pygame.Surface((30, 30))


def test_templates_have_required_fields():
    for t in MONSTER_TEMPLATES.values():
        assert {"hp", "score", "speed"} <= set(t)


def test_make_monster_takes_damage():
    m = make_monster("drone", IMG, settings=GameSettings.default())
    assert m.hp == 1
    assert m.take_damage() is True  # True means it died on this hit


def test_tough_monster_survives_first_hit():
    m = make_monster("strafer", IMG, settings=GameSettings.default())
    assert m.hp == 2
    assert m.take_damage() is False  # survives, hp now 1
    assert m.take_damage() is True  # second hit kills it


def test_boss_hp():
    b = Boss(IMG, hp=5)
    for _ in range(4):
        b.take_damage()
    assert b.hp == 1
    assert b.take_damage() is True