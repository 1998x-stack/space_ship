# monster.py

import pygame
from config import *
import random

class Monster(pygame.sprite.Sprite):
    def __init__(self, image, speed=None):
        """怪物初始化函数"""
        super().__init__()
        self.image = image
        x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.rect = self.image.get_rect(midtop=(x, 0))
        self.speed = speed if speed is not None else MONSTER_SPEED  # 接受自定义速度，否则使用默认速度

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()