import pygame

KINDS = {"weapon", "shield", "life"}


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind, image, center, speed=100.0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.kind = kind
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed * dt
        if self.rect.top > 700:
            self.kill()