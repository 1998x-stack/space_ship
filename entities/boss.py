import pygame


class Boss(pygame.sprite.Sprite):
    def __init__(self, image, hp, score=500):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midtop=(400, -100))
        self.hp = hp
        self.score = score
        self.t = 0.0
        self.dead = False

    def update(self, dt):
        self.t += dt
        if self.rect.top < 50:
            self.rect.y += 30 * dt

    def take_damage(self, amount=1):
        self.hp -= amount
        if self.hp <= 0:
            self.dead = True
        return self.hp <= 0