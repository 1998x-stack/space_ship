import random
import pygame
from scene import Scene
from entities.ship import Ship
from entities.monsters import make_monster
from entities.boss import Boss
from entities.bullets import EnemyBullet
from entities.powerups import PowerUp
from entities.explosion import Explosion
from systems.combat import resolve_bullets, resolve_enemy_bullets
from systems.scoring import Scoring
from systems.waves import WaveController
from scenes.pause import PauseScene
from scenes.gameover import GameOverScene
from hud import Hud


class GameplayScene(Scene):
    def __init__(self, manager, settings, assets):
        self.manager = manager
        self.settings = settings
        self.assets = assets
        self.ship = Ship(assets.image("ship.png", (50, 50)), settings)
        self.scorer = Scoring(settings.high_score_path)
        self.waves = WaveController(settings)
        self.hud = Hud(settings)
        self.enemies = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.elapsed = 0.0
        self.wave_events = []
        self.bullet_image = assets.image("laser.png", (10, 30))
        self.enemy_bullet_image = assets.image("bullet.png", (8, 24))
        self.powerup_image = assets.image("powerup.png", (24, 24))
        self.explosion_frames = [assets.image(f"explosion{i}.png", (36, 36))
                                 for i in range(1, 4)]

    def start_wave(self):
        self.waves.wave_number += 1
        self.wave_events = self.waves.build_wave_events(self.waves.wave_number)
        self.elapsed = 0.0

    def draw(self, surface):
        surface.fill((10, 10, 20))
        self.enemies.draw(surface)
        self.bosses.draw(surface)
        self.enemy_bullets.draw(surface)
        self.ship.lasers.draw(surface)
        surface.blit(self.ship.image, self.ship.rect)
        self.powerups.draw(surface)
        self.explosions.draw(surface)
        self.hud.draw(surface, self.scorer, self.ship)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.ship.update(dt, keys)
        if keys[pygame.K_SPACE]:
            self.ship.fire(self.bullet_image)
        self.ship.lasers.update(dt)
        self.enemy_bullets.update(dt)
        self.enemies.update(dt)
        self.bosses.update(dt)
        self.powerups.update(dt)
        self.explosions.update(dt)

        if not self.wave_events:
            self.start_wave()
        self.elapsed += dt
        due, self.wave_events = self.waves.spawn_due(self.elapsed, self.wave_events)
        for _, kind in due:
            if kind == "boss":
                self.bosses.add(Boss(self.assets.image("monster1.png", (90, 90)),
                                     self.settings.boss_hp))
            else:
                self.enemies.add(make_monster(
                    kind, self.assets.image("monster.png", (40, 40)),
                    self.settings, self.ship))

        # spawn enemy bullets for shooters that have a pending_shot flag
        for e in list(self.enemies) + list(self.bosses):
            if getattr(e, "pending_shot", False):
                self.enemy_bullets.add(EnemyBullet(
                    self.enemy_bullet_image, e.rect.midbottom, (0.0, 140.0)))
                e.pending_shot = False

        # player bullets vs monsters/bosses
        killed = resolve_bullets(self.enemies, self.ship.lasers)
        killed += resolve_bullets(self.bosses, self.ship.lasers)
        for e in killed:
            self.scorer.add_kill(e.score)
            self.explosions.add(Explosion(self.explosion_frames, e.rect.center))
            if random.random() < self.settings.powerup_drop_chance:
                kind = random.choice(["weapon", "shield", "life"])
                self.powerups.add(PowerUp(kind, self.powerup_image, e.rect.center))

        # damage the ship from enemy bullets and body collisions
        lost_life = False
        if resolve_enemy_bullets(self.enemy_bullets, self.ship):
            self.scorer.player_hit()
            lost_life = self.ship.take_hit()
        for e in list(self.enemies) + list(self.bosses):
            if self.ship.rect.colliderect(e.rect):
                e.kill()
                self.scorer.player_hit()
                lost_life = lost_life or self.ship.take_hit()
        if lost_life:
            self.explosions.add(Explosion(self.explosion_frames, self.ship.rect.center))

        if self.ship.lives <= 0:
            self.scorer.save_high_score()
            self.manager.replace(GameOverScene(
                self.manager, self.settings, self.assets,
                self.scorer.score, self.scorer.load_high_score()))
            return

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.manager.push(PauseScene(self.manager))