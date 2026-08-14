import pygame
from entities.weapons import Weapon


class Ship(pygame.sprite.Sprite):
    def __init__(self, image, settings):
        super().__init__()
        self.image = image
        self.width = settings.width
        self.height = settings.height
        self.rect = self.image.get_rect(midbottom=(settings.width / 2, settings.height - 20))
        self.speed = settings.player_speed
        self.max_lives = settings.player_lives
        self.lives = settings.player_lives
        self.invuln_time = settings.invuln_time
        self.invuln_timer = 0.0
        self.weapon = Weapon(settings.laser_cooldown, settings.player_bullet_speed)
        self.lasers = pygame.sprite.Group()

    def update(self, dt, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        if dx or dy:
            norm = (dx * dx + dy * dy) ** 0.5
            self.rect.x += dx / norm * self.speed * dt
            self.rect.y += dy / norm * self.speed * dt
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.rect.right, self.width)
        if self.rect.top < 0:
            self.rect.top = 0
        self.weapon.arms(dt)
        self.invuln_timer = max(0.0, self.invuln_timer - dt)

    def fire(self, bullet_image):
        if self.weapon.can_fire():
            self.weapon.fire(self.lasers, self.rect.centerx, self.rect.top, bullet_image)

    def take_hit(self):
        if self.invuln_timer > 0:
            return False
        self.lives -= 1
        if self.lives > 0:
            self.invuln_timer = self.invuln_time
        return True

    def add_life(self):
        self.lives = min(self.max_lives, self.lives + 1)