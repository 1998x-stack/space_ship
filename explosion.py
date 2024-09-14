# explosion.py

import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, images):
        super().__init__()
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = 50  # 毫秒
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index == len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]
                center = self.rect.center
                self.rect = self.image.get_rect(center=center)