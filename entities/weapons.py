import pygame
from entities.bullets import PlayerBullet


class Weapon:
    MAX_LEVEL = 3

    def __init__(self, laser_cooldown, bullet_speed):
        self.level = 1
        self.timer = 0.0
        self.cooldown = laser_cooldown
        self.bullet_speed = bullet_speed

    def upgrade(self):
        self.level = min(self.MAX_LEVEL, self.level + 1)

    def can_fire(self):
        return self.timer <= 0.0

    def arms(self, dt):
        self.timer = max(0.0, self.timer - dt)

    def fire(self, group, x, y, bullet_image):
        if not self.can_fire():
            return []
        self.timer = self.cooldown
        if self.level == 1:
            pts = [(0, -24)]
        elif self.level == 2:
            pts = [(-16, -24), (0, -30), (16, -24)]
        else:
            pts = [(-16, -24), (0, -30), (16, -24)]
        out = []
        for px, py in pts:
            bullet = PlayerBullet(bullet_image, (x + px, y + py), self.bullet_speed)
            out.append(bullet)
        group.add(*out)
        return out