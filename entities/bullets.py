import pygame


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, image, center, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.speed = speed

    def update(self, dt):
        self.rect.y -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, image, center, velocity):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.velocity = velocity

    def update(self, dt):
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        if (self.rect.top > 800 or self.rect.bottom < 0
                or self.rect.left > 840 or self.rect.right < -40):
            self.kill()