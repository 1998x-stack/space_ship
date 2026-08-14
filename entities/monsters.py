import math
import random
import pygame
from settings import GameSettings

MONSTER_TEMPLATES = {
    "drone": {"hp": 1, "score": 10, "speed": 90.0},
    "strafer": {"hp": 2, "score": 25, "speed": 70.0, "fires": True, "laser_cooldown": 1.6},
    "kamikaze": {"hp": 1, "score": 15, "speed": 170.0},
}


def make_monster(kind, image, settings, player=None):
    template = MONSTER_TEMPLATES[kind]
    return Monster(kind, template, image, settings, player)


class Monster(pygame.sprite.Sprite):
    def __init__(self, kind, template, image, settings, player):
        super().__init__()
        self.kind = kind
        self.image = image
        self.rect = self.image.get_rect(
            midtop=(random.randint(0, settings.width - image.get_width()), 0))
        self.speed = template["speed"]
        self.hp = template["hp"]
        self.score = template["score"]
        self.fires = template.get("fires", False)
        self.fire_cd = template.get("laser_cooldown", float("inf"))
        self.fire_timer = random.uniform(0.3, 1.0)
        self.player = player
        self.dir = 1
        self.width = settings.width
        self.height = settings.height
        self.t = 0.0
        self.dead = False

    def update(self, dt):
        self.t += dt
        if self.kind == "drone":
            self.rect.y += self.speed * dt
        elif self.kind == "strafer":
            self.rect.y += self.speed * 0.4 * dt
            self.rect.x += self.dir * self.speed * 0.6 * dt
            if self.rect.left < 0 or self.rect.right > self.width:
                self.dir *= -1
        elif self.kind == "kamikaze" and self.player:
            tx = self.player.rect.centerx - self.rect.centerx
            ty = self.player.rect.centery - self.rect.centery
            n = math.hypot(tx, ty) or 1
            self.rect.x += tx / n * self.speed * dt
            self.rect.y += ty / n * self.speed * dt
        else:
            self.rect.y += self.speed * dt

        self.pending_shot = False  # scene reads this to spawn an enemy bullet
        self.fire_timer -= dt
        if self.fires and self.fire_timer <= 0 and self.rect.top > 20 and self.player:
            self.fire_timer = self.fire_cd
            self.pending_shot = True
        if self.rect.top > self.height + 40:
            self.kill()

    def take_damage(self, amount=1):
        self.hp -= amount
        if self.hp <= 0:
            self.dead = True
        return self.hp <= 0