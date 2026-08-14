import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, images, center, frame_rate=0.05):
        super().__init__()
        self.images = images
        self.index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = frame_rate
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        if self.timer < self.frame_rate:
            return
        center = self.rect.center
        self.index += 1
        if self.index >= len(self.images):
            self.kill()
            return
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=center)
        self.timer = 0.0