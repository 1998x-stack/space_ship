# Space Ship Reconstruction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the pygame space-shooter into a clean fixed-timestep engine with scenes/systems/entities, and expand gameplay (3 enemy types, boss, weapons, power-ups, waves, combo scoring). Approved spec: `docs/superpowers/specs/2026-08-14-space-ship-reconstruction-design.md`.

**Architecture:** A small engine (`game.py` + `scene.py`) owns the fixed-timestep loop and scene stack. Gameplay logic lives in `systems/` (waves, combat, scoring). `entities/` holds pure sprites. `scenes/` orchestrate systems. `assets.py` hides file I/O; `settings.py` validates everything. Logic is unit-tested headlessly with `pytest`; the game is smoke-tested with `SDL_VIDEODRIVER=dummy`.

**Tech Stack:** Python 3.9+, pygame, pytest.

## Global Constraints

- Python >= 3.9 (no 3.10-only syntax such as `match` or `X | None`).
- pygame 2.x. Core game logic must not require a display (tested headless).
- All tuning values live in `settings.py`; no magic numbers in logic/scenes.
- No wildcard imports (`from x import *`).
- File I/O and asset access never crash the game on missing files (defaults/fallbacks).
- Every task ends with a passing test and a commit.

---

## Task 1: Scaffolding + settings with validation

**Files:**
- Create: `.gitignore`, `requirements.txt`, `LICENSE`, `settings.py`
- Test: `tests/test_settings.py`

**Interfaces — Produces:**
- `settings.GameSettings` dataclass with `validate() -> list[str]` and `default() -> GameSettings`, `derive(**kwargs) -> GameSettings`.
- Fields: `width=800`, `height=600`, `fps=60`, `player_speed=260.0`, `player_lives=3`, `invuln_time=1.5`, `laser_cooldown=0.25`, `player_bullet_speed=520.0`, `enemy_base_speed=90.0`, `enemies_per_wave=15`, `waves_per_boss=5`, `boss_hp=5`, `powerup_drop_chance=0.20`, `high_score_path="high_score.txt"`.

- [ ] **Step 1: Write the failing test** — `tests/test_settings.py`:

```python
import pytest
from settings import GameSettings


def test_default_valid():
    assert GameSettings.default().validate() == []


@pytest.mark.parametrize("bad", [
    {"width": 0}, {"height": -1}, {"fps": 0}, {"player_speed": -1.0},
    {"player_lives": 0}, {"laser_cooldown": -0.1}, {"enemies_per_wave": 0},
    {"waves_per_boss": 0}, {"boss_hp": 0}, {"powerup_drop_chance": 1.5},
])
def test_invalid_values_rejected(bad):
    s = GameSettings.default().derive(**bad)
    assert s.validate() != []
```

- [ ] **Step 2: Move asset/log files we no longer want tracked** (old `space_ship.log`): delete it and stop generating it. Run `rm -f space_ship.log`.

- [ ] **Step 3: Run test to verify it fails** — Run: `pytest tests/test_settings.py -v` → Expected: FAIL (`ModuleNotFoundError: settings`).

- [ ] **Step 4: Write implementation**

`requirements.txt`:
```
pygame>=2.1
pytest>=7.0
```

`.gitignore`:
```
__pycache__/
*.pyc
space_ship.log
high_score.txt
```

`LICENSE`:
```
MIT License

Copyright (c) 2026 1998x-stack

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

`settings.py`:
```python
from dataclasses import dataclass, replace


@dataclass
class GameSettings:
    width: int = 800
    height: int = 600
    fps: int = 60

    player_speed: float = 260.0
    player_lives: int = 3
    invuln_time: float = 1.5

    laser_cooldown: float = 0.25
    player_bullet_speed: float = 520.0

    enemy_base_speed: float = 90.0
    enemies_per_wave: int = 15
    waves_per_boss: int = 5
    boss_hp: int = 5

    powerup_drop_chance: float = 0.20
    high_score_path: str = "high_score.txt"

    def validate(self):
        errors = []
        if self.width < 1:
            errors.append("width must be > 0")
        if self.height < 1:
            errors.append("height must be > 0")
        if self.fps < 1:
            errors.append("fps must be > 0")
        if self.player_speed <= 0:
            errors.append("player_speed must be > 0")
        if self.player_lives < 1:
            errors.append("player_lives must be >= 1")
        if self.laser_cooldown < 0:
            errors.append("laser_cooldown cannot be negative")
        if self.enemies_per_wave < 1:
            errors.append("enemies_per_wave must be >= 1")
        if self.waves_per_boss < 1:
            errors.append("waves_per_boss must be >= 1")
        if self.boss_hp < 1:
            errors.append("boss_hp must be >= 1")
        if not (0.0 <= self.powerup_drop_chance <= 1.0):
            errors.append("powerup_drop_chance must be in [0, 1]")
        return errors

    @classmethod
    def default(cls):
        return cls()

    def derive(self, **kwargs):
        return replace(self, **kwargs)
```

- [ ] **Step 5: Run test to verify it passes** Run: `pytest tests/test_settings.py -v` → PASS (3 passed).

- [ ] **Step 6: Commit** Run: `git add requirements.txt LICENSE settings.py tests/ .gitignore && git commit -m "chore: scaffold project with validated settings"`

---

## Task 2: Fixed-timestep engine + scene manager

**Files:**
- Create: `game.py`, `scene.py`
- Test: `tests/test_game.py`

**Interfaces — Produces:**
- `game.FIXED_DT = 1/60`, `game.MAX_FRAME_TIME = 0.25`
- `game.advance_accumulator(acc, frame_dt, fixed_dt, max_frame) -> float`
- `game.Game(settings)` with `.run(initial_scene)`, `.quit()`, attributes `.settings`, `.screen`, `.manager`.
- `scene.Scene` base: `on_enter()`, `on_exit()`, `handle_event(event)`, `update(dt)`, `draw(surface)`.
- `scene.SceneManager`: `push(s)`, `pop()`, `replace(s)`, `handle_event(event)`, `update(dt)`, `draw(surface)`, `.quit()`, `.should_quit`, `.active`.

- [ ] **Step 1: Write the failing test** — `tests/test_game.py`:

```python
from game import advance_accumulator, FIXED_DT


def test_accumulator_runs_one_step():
    leftover = advance_accumulator(0.0, FIXED_DT, FIXED_DT, 0.25)
    assert leftover < FIXED_DT


def test_accumulator_accumulates_without_stepping():
    assert advance_accumulator(0.0, FIXED_DT / 2, FIXED_DT, 0.25) == 0.0


def test_accumulator_clamps_long_frames():
    assert advance_accumulator(0.0, 0.5, FIXED_DT, 0.25) <= 0.25
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_game.py -v` → FAIL (`ModuleNotFoundError: game`).

- [ ] **Step 3: Write implementation**

`scene.py`:
```python
class Scene:
    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


class SceneManager:
    def __init__(self):
        self._stack = []
        self.should_quit = False

    @property
    def active(self):
        return len(self._stack) > 0

    def push(self, scene):
        if self._stack:
            self._stack[-1].on_exit()
        scene.on_enter()
        self._stack.append(scene)

    def pop(self):
        if self._stack:
            self._stack.pop().on_exit()
            if self._stack:
                self._stack[-1].on_enter()

    def replace(self, scene):
        if self._stack:
            self._stack.pop().on_exit()
        scene.on_enter()
        self._stack.append(scene)

    def quit(self):
        self.should_quit = True

    def handle_event(self, event):
        if self._stack:
            self._stack[-1].handle_event(event)

    def update(self, dt):
        if self._stack:
            self._stack[-1].update(dt)

    def draw(self, surface):
        if self._stack:
            self._stack[-1].draw(surface)
```

`game.py`:
```python
import pygame
from settings import GameSettings
from scene import SceneManager

FIXED_DT = 1.0 / 60.0
MAX_FRAME_TIME = 0.25


def advance_accumulator(acc, frame_dt, fixed_dt=FIXED_DT, max_frame=MAX_FRAME_TIME):
    acc += min(frame_dt, max_frame)
    steps = int(acc / fixed_dt)
    return acc - steps * fixed_dt


class Game:
    def __init__(self, settings: GameSettings):
        pygame.init()
        self.settings = settings
        self.screen = pygame.display.set_mode((settings.width, settings.height))
        pygame.display.set_caption("Space Ship")
        self.clock = pygame.time.Clock()
        self.manager = SceneManager()
        self._running = False

    def run(self, initial_scene):
        self.manager.replace(initial_scene)
        self._running = True
        acc = 0.0
        while self._running and self.manager.active and not self.manager.should_quit:
            frame_dt = self.clock.tick(self.settings.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                self.manager.handle_event(event)
            acc = advance_accumulator(acc, frame_dt)
            steps = int(acc / FIXED_DT)
            while steps:
                self.manager.update(FIXED_DT)
                acc -= FIXED_DT
                steps -= 1
            self.manager.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def quit(self):
        self._running = False
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_game.py -v` → PASS (3 passed).

- [ ] **Step 5: Commit** Run: `git add game.py scene.py tests/test_game.py && git commit -m "feat: fixed-timestep engine + scene manager"`
---

## Task 3: AssetManager with fallbacks

**Files:**
- Create: `assets.py`
- Test: `tests/test_assets.py`

**Interfaces — Produces:**
- `assets.AssetManager(settings, images_dir="assets/images/", sounds_dir="assets/sounds/")` with `image(name, size=(32,32)) -> Surface` (cached, fallback if missing) and `sound(name) -> Sound|None` (cached, `None` if missing).

- [ ] **Step 1: Write the failing test** — `tests/test_assets.py`:

```python
import pygame
from assets import AssetManager
from settings import GameSettings

pygame.init()


def test_loads_ship_and_fallback():
    am = AssetManager(GameSettings.default())
    assert am.image("does_not_exist.png", (20, 20)).get_size() == (20, 20)
    assert am.sound("missing.wav") is None


def test_caches_images():
    am = AssetManager(GameSettings.default())
    a = am.image("x.png", (10, 20))
    b = am.image("x.png", (10, 20))
    assert a is b
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_assets.py -v` → FAIL.

- [ ] **Step 3: Write implementation**

`assets.py`:
```python
import os
import pygame
from settings import GameSettings


class AssetManager:
    def __init__(self, settings, images_dir="assets/images/", sounds_dir="assets/sounds/"):
        self.settings = settings
        self.images_dir = images_dir
        self.sounds_dir = sounds_dir
        self._images = {}
        self._sounds = {}

    def image(self, name, size=(32, 32)):
        key = (name, tuple(int(s) for s in size))
        if key in self._images:
            return self._images[key]
        path = os.path.join(self.images_dir, name)
        if os.path.exists(path):
            surf = pygame.image.load(path).convert_alpha()
            if size:
                surf = pygame.transform.scale(surf, size)
        else:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((40, 40, 40))
        self._images[key] = surf
        return surf

    def sound(self, name):
        if name in self._sounds:
            return self._sounds[name]
        path = os.path.join(self.sounds_dir, name)
        if os.path.exists(path):
            self._sounds[name] = pygame.mixer.Sound(path)
        else:
            self._sounds[name] = None
        return self._sounds[name]
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_assets.py -v` → PASS (2 passed).

- [ ] **Step 5: Commit** Run: `git add assets.py tests/test_assets.py && git commit -m "feat: asset manager with cached images and fallback"`

---

## Task 4: Entities — bullets and weapon

**Files:**
- Create: `entities/__init__.py`, `entities/bullets.py`, `entities/weapons.py`
- Test: `tests/test_bullets.py`

**Interfaces — Produces:**
- `entities/bullets.PlayerBullet(image, center, speed)`: `.rect`, `update(dt)`.
- `entities/weapons.Weapon(laser_cooldown, bullet_speed)`: `.level`, `upgrade()` (caps at 3), `can_fire()`, `arms(dt)`, `fire(group, x, y, bullet_image) -> list[PlayerBullet]` (1 at lvl1, 3 at lvl2+).

- [ ] **Step 1: Write the failing test** — `tests/test_bullets.py`:

```python
import pygame
from entities.weapons import Weapon

pygame.init()
IMG = pygame.Surface((8, 8))


def test_weapon_fires_patterns():
    g = pygame.sprite.Group()
    w = Weapon(laser_cooldown=0.2, bullet_speed=500.0)
    assert len(w.fire(g, 100, 100, IMG)) == 1
    w.upgrade()
    assert len(w.fire(g, 100, 100, IMG)) == 3


def test_weapon_level_caps():
    w = Weapon(0.2, 500.0)
    for _ in range(10):
        w.upgrade()
    assert w.level == 3


def test_cooldown_blocks_rapid_fire():
    g = pygame.sprite.Group()
    w = Weapon(laser_cooldown=0.2, bullet_speed=500.0)
    w.fire(g, 100, 100, IMG)
    assert w.fire(g, 100, 100, IMG) == []
    w.arms(0.3)
    assert len(w.fire(g, 100, 100, IMG)) == 1
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_bullets.py` → FAIL.

- [ ] **Step 3: Write implementation**

`entities/__init__.py`:
```python
```

`entities/bullets.py`:
```python
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
```

`entities/weapons.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_bullets.py -v` → PASS (3 passed).

- [ ] **Step 5: Commit** Run: `git add entities/ tests/test_bullets.py && git commit -m "feat: bullets + weapon fire patterns"`

---

## Task 5: Player ship

**Files:**
- Create: `entities/ship.py`
- Test: `tests/test_ship.py`

**Interfaces — Produces:**
- `entities/ship.Ship(image, settings)`: `.rect`, `.lives`, `.weapon`, `.lasers` (Group), `update(dt, keys)`, `fire(bullet_image)`, `take_hit() -> bool`, `add_life()`, `.max_lives`.

- [ ] **Step 1: Write the failing test** — `tests/test_ship.py`:

```python
import pygame
from entities.ship import Ship
from settings import GameSettings

pygame.init()
IMG = pygame.Surface((40, 40))


def keys(pressed):
    base = {getattr(pygame, n): False for n in
            ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_SPACE"]}
    base.update(pressed)
    return base


def test_moves_right():
    s = Ship(IMG, GameSettings.default().derive(player_speed=100.0))
    x0 = s.rect.centerx
    s.update(1.0, keys({pygame.K_RIGHT: True}))
    assert s.rect.centerx > x0


def test_hits_decrease_lives():
    s = Ship(IMG, GameSettings.default().derive(player_lives=3))
    assert s.take_hit() is True
    assert s.lives == 2


def test_invulnerability_blocks_damage():
    st = GameSettings.default().derive(player_lives=3, invuln_time=1.0)
    s = Ship(IMG, st)
    s.take_hit()
    assert s.take_hit() is False
    s.update(1.5, keys({}))
    assert s.take_hit() is True


def test_add_life_caps_at_starting():
    s = Ship(IMG, GameSettings.default().derive(player_lives=3))
    s.add_life()
    assert s.lives == 3
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_ship.py` → FAIL.

- [ ] **Step 3: Write implementation**

`entities/ship.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_ship.py -v` → PASS (4 passed).

- [ ] **Step 5: Commit** Run: `git add entities/ship.py tests/test_ship.py && git commit -m "feat: player ship with lives, invulnerability, weapon"`

---

## Task 6: Monsters (data-driven) and Boss

**Files:**
- Create: `entities/monsters.py`, `entities/boss.py`
- Test: `tests/test_monsters.py`

**Interfaces — Produces:**
- `entities/monsters.MONSTER_TEMPLATES` dict with kinds `"drone"`, `"strafer"`, `"kamikaze"`, each with keys `hp`, `score`, `speed`.
- `entities/monsters.make_monster(kind, image, settings, player=None) -> Monster`
- `Monster`: `.rect`, `.hp`, `.score`, `.kind`, `update(dt)`, `take_damage(amount=1) -> bool` (False if dead).
- `entities/boss.Boss(image, hp, score=500)`: `.hp`, `.score`, `update(dt)`, `take_damage(amount=1) -> bool`.

- [ ] **Step 1: Write the failing test** — `tests/test_monsters.py`:

```python
import pygame
from entities.monsters import MONSTER_TEMPLATES, make_monster
from entities.boss import Boss
from settings import GameSettings

pygame.init()
IMG = pygame.Surface((30, 30))


def test_templates_have_required_fields():
    for t in MONSTER_TEMPLATES.values():
        assert {"hp", "score", "speed"} <= set(t)


def test_make_monster_takes_damage():
    m = make_monster("drone", IMG, settings=GameSettings.default())
    assert m.hp == 1
    assert m.take_damage() is False  # dies on first hit


def test_boss_hp():
    b = Boss(IMG, hp=5)
    for _ in range(4):
        b.take_damage()
    assert b.hp == 1
    assert b.take_damage() is False
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_monsters.py` → FAIL.

- [ ] **Step 3: Write implementation**

`entities/monsters.py`:
```python
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
```

`entities/boss.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_monsters.py -v` → PASS (3 passed).

- [ ] **Step 5: Commit** Run: `git add entities/monsters.py entities/boss.py tests/test_monsters.py && git commit -m "feat: data-driven monsters + boss"`

---

## Task 7: Power-ups and Explosion

**Files:**
- Create: `entities/powerups.py`, `entities/explosion.py`
- Test: `tests/test_powerups.py`

**Interfaces — Produces:**
- `entities/powerups.PowerUp(kind, image, center, speed=100.0)`: `.kind` in `{"weapon","shield","life"}`, `update(dt)`.
- `entities/explosion.Explosion(images, center, frame_rate=0.05)`: `update(dt)` (auto-kills after final frame).

- [ ] **Step 1: Write the failing test** — `tests/test_powerups.py`:

```python
import pygame
from entities.powerups import PowerUp
from entities.explosion import Explosion

pygame.init()
IMG = pygame.Surface((20, 20))


def test_powerup_moves_down():
    p = PowerUp("weapon", IMG, (10, 10), speed=100.0)
    y0 = p.rect.y
    p.update(0.1)
    assert p.rect.y > y0


def test_explosion_removes_after_frames():
    g = pygame.sprite.Group()
    imgs = [pygame.Surface((5, 5)) for _ in range(3)]
    e = Explosion(imgs, (10, 10), frame_rate=0.05)
    g.add(e)
    for _ in range(4):
        e.update(0.05)
    assert not g
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_powerups.py` → FAIL.

- [ ] **Step 3: Write implementation**

`entities/powerups.py`:
```python
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
```

`entities/explosion.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_powerups.py -v` → PASS (2 passed).

- [ ] **Step 5: Commit** Run: `git add entities/powerups.py entities/explosion.py tests/test_powerups.py && git commit -m "feat: power-up pickups and explosion animation"`

---

## Task 8: Scoring system with combo + high-score persistence

**Files:**
- Create: `systems/__init__.py`, `systems/scoring.py`
- Test: `tests/test_scoring.py`

**Interfaces — Produces:**
- `systems/scoring.Scoring(high_score_path)`: `.score`, `.combo`, `.multiplier` (property), `add_kill(base)`, `player_hit()`, `load_high_score() -> int`, `save_high_score()`.
- Multiplier: `min(4, 1 + combo // 10)`; `player_hit()` resets `combo` to 0.

- [ ] **Step 1: Write the failing test** — `tests/test_scoring.py`:

```python
from systems.scoring import Scoring


def test_combo_multiplier(tmp_path):
    s = Scoring(str(tmp_path / "h.txt"))
    for _ in range(20):
        s.add_kill(10)
    assert s.multiplier == 3
    assert s.score == (sum(1 + i // 10 for i in range(1, 21)) * 10)
    s.player_hit()
    assert s.combo == 0
    assert s.multiplier == 1


def test_high_score_persist(tmp_path):
    p = str(tmp_path / "h.txt")
    s = Scoring(p)
    s.score = 500
    s.save_high_score()
    assert Scoring(p).load_high_score() == 500


def test_load_high_score_missing_or_bad(tmp_path):
    good = Scoring(str(tmp_path / "a.txt"))
    good.save_high_score()
    bad = Scoring(str(tmp_path / "b.txt"))
    bad.score = 7
    bad.save_high_score()
    import pathlib
    pathlib.Path(str(tmp_path / "bad.txt")).write_text("not a number")
    assert good.load_high_score() == 0
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_scoring.py` → FAIL.

- [ ] **Step 3: Write implementation**

`systems/scoring.py`:
```python
import os


class Scoring:
    MAX_MULTIPLIER = 4
    KILLS_PER_LEVEL = 10

    def __init__(self, high_score_path):
        self.path = high_score_path
        self.score = 0
        self.combo = 0

    @property
    def multiplier(self):
        return min(self.MAX_MULTIPLIER, 1 + self.combo // self.KILLS_PER_LEVEL)

    def add_kill(self, base):
        self.combo += 1
        self.score += base * self.multiplier

    def player_hit(self):
        self.combo = 0

    def load_high_score(self):
        try:
            with open(self.path, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0

    def save_high_score(self):
        with open(self.path, "w") as f:
            f.write(str(self.score))
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_scoring.py -v` → PASS (3 passed).

- [ ] **Step 5: Commit** Run: `git add systems/ tests/test_scoring.py && git commit -m "feat: scoring with combo multiplier + high score persistence"`

---

## Task 9: Wave controller with difficulty curve

**Files:**
- Create: `systems/waves.py`
- Test: `tests/test_waves.py`

**Interfaces — Produces:**
- `systems/waves.WaveController(settings)`: `.wave_number`, `build_wave_events(wave_number) -> list[(delay, kind)]` (kind in `{"drone","strafer","kamikaze","boss"}`), `spawn_due(elapsed, events) -> (due_events, remaining_events)`.
- Boss appears when `wave_number % waves_per_boss == 0`. Enemy count grows with wave number; spawn interval shrinks.

- [ ] **Step 1: Write the failing test** — `tests/test_waves.py`:

```python
from systems.waves import WaveController
from settings import GameSettings


def test_wave_grows_with_number():
    st = GameSettings.default().derive(enemies_per_wave=15, waves_per_boss=5)
    w = WaveController(st)
    assert len(w.build_wave_events(5)) > len(w.build_wave_events(2))


def test_boss_every_nwaves():
    st = GameSettings.default().derive(enemies_per_wave=5, waves_per_boss=5)
    w = WaveController(st)
    assert "boss" in [k for _, k in w.build_wave_events(5)]
    assert "boss" not in [k for _, k in w.build_wave_events(4)]
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_waves.py` → FAIL.

- [ ] **Step 3: Write implementation**

`systems/waves.py`:
```python
from settings import GameSettings


class WaveController:
    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.wave_number = 0

    def build_wave_events(self, wave_number):
        settings = self.settings
        n = settings.enemies_per_wave + wave_number // 2
        base_interval = max(0.3, 1.4 - wave_number * 0.08)
        events = []
        for i in range(n):
            kind = "drone"
            if wave_number >= 2 and i % 3 == 1:
                kind = "strafer"
            if wave_number >= 4 and i % 5 == 2:
                kind = "kamikaze"
            events.append((i * base_interval, kind))
        if wave_number % settings.waves_per_boss == 0:
            events.append((max(d for d, _ in events) + 0.5, "boss"))
        return events

    def spawn_due(self, elapsed, events):
        due = []
        remaining = []
        for delay, kind in events:
            (due if delay <= elapsed else remaining).append((delay, kind))
        return due, remaining
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_waves.py -v` → PASS (2 passed).

- [ ] **Step 5: Commit** Run: `git add systems/waves.py tests/test_waves.py && git commit -m "feat: wave controller with difficulty curve + boss cadence"`

---

## Task 10: Combat resolution

**Files:**
- Create: `systems/combat.py`
- Test: `tests/test_combat.py`

**Interfaces — Produces:**
- `systems.combat.resolve_bullets(enemies, bullets) -> list` (damages and kills hit monsters, kills bullets; returns killed monsters)
- `systems.combat.resolve_player(enemies, player) -> list` (returns collided enemies, removes them)
- Consumes sprites with `.rect`, `.hp`, `.take_damage(amount)`.

- [ ] **Step 1: Write the failing test** — `tests/test_combat.py`:

```python
import pygame
from entities.monsters import make_monster
from entities.bullets import PlayerBullet
from systems import combat
from settings import GameSettings

pygame.init()
IMG = pygame.Surface((30, 30))


def test_bullets_kill_monster():
    m = make_monster("drone", IMG, settings=GameSettings.default())
    m.rect = pygame.Rect(0, 0, 30, 30)
    group = pygame.sprite.Group(m)
    b = PlayerBullet(IMG, (15, 15), 100.0)
    killed = combat.resolve_bullets(group, pygame.sprite.Group(b))
    assert m in killed
    assert not group


def test_player_overlap_removes_enemy():
    m = make_monster("drone", IMG, settings=GameSettings.default())
    m.rect = pygame.Rect(0, 0, 30, 30)
    group = pygame.sprite.Group(m)
    player = pygame.sprite.Sprite()
    player.rect = pygame.Rect(10, 10, 30, 30)
    hits = combat.resolve_player(group, player)
    assert m in hits
    assert not group
```

- [ ] **Step 2: Run test to verify it fails** Run: `pytest tests/test_combat.py` → FAIL.

- [ ] **Step 3: Write implementation**

`systems/combat.py`:
```python
import pygame


def resolve_bullets(enemies, bullets):
    killed = []
    for bullet in bullets:
        hit = pygame.sprite.spritecollideany(bullet, enemies, False)
        if hit is not None and not getattr(hit, "dead", False):
            if hit.take_damage():
                killed.append(hit)
            bullet.kill()
    return killed


def resolve_player(enemies, player):
    return list(pygame.sprite.spritecollide(player, enemies, True))


def resolve_enemy_bullets(bullets, player):
    """Return True if any enemy bullet hit the player (removes the bullets)."""
    return len(pygame.sprite.spritecollide(player, bullets, True)) > 0
```

- [ ] **Step 4: Run test to verify it passes** Run: `pytest tests/test_combat.py -v` → PASS (2 passed).

- [ ] **Step 5: Commit** Run: `git add systems/combat.py tests/test_combat.py && git commit -m "feat: combat collision resolution"`

---

## Task 11: Scenes — Start, Pause, Game Over + HUD

**Files:**
- Create: `hud.py`, `scenes/__init__.py`, `scenes/start.py`, `scenes/pause.py`, `scenes/gameover.py`

**Interfaces — Consumes:** `Scene`, `SceneManager`, `GameSettings`, `AssetManager`.
**Interfaces — Produces:**
- `hud.Hud(settings)` with `draw(surface, scorer, ship)`.
- `scenes.start.StartScene(manager, settings, assets, high_score)` → on key: `manager.replace(GameplayScene(manager, settings, assets))`.
- `scenes.pause.PauseScene(manager)` → on `P`: `manager.pop()`.
- `scenes.gameover.GameOverScene(manager, settings, assets, final_score, high_score)` → on key: `manager.replace(StartScene(...))`.
- Note: `GameplayScene` and full scene wiring are defined in Task 12; scenes here reference them by import guarded for correctness.

- [ ] **Step 1: Write the HUD** — `hud.py`:

```python
import pygame


class Hud:
    def __init__(self, settings):
        self.font = pygame.font.Font(None, 36)
        self.small = pygame.font.Font(None, 28)

    def draw(self, surface, scorer, ship):
        surface.blit(self.font.render(f"Score: {scorer.score}", True, (255, 255, 255)), (10, 10))
        surface.blit(self.small.render(f"x{scorer.multiplier}", True, (255, 200, 0)), (10, 44))
        surface.blit(self.font.render(f"Lives: {ship.lives}", True, (255, 255, 255)), (10, 76))
```

- [ ] **Step 2: Write the scenes** — `scenes/start.py`:

```python
import pygame
from scene import Scene


class StartScene(Scene):
    def __init__(self, manager, settings, assets, high_score):
        self.manager = manager
        self.settings = settings
        self.assets = assets
        self.high_score = high_score

    def draw(self, surface):
        surface.fill((0, 0, 0))
        title = pygame.font.Font(None, 48)
        mid = self.settings.width / 2
        t = title.render("Space Ship", True, (255, 255, 255))
        surface.blit(t, (mid - t.get_width() / 2, 200))
        hs = title.render(f"High Score: {self.high_score}", True, (255, 200, 0))
        surface.blit(hs, (mid - hs.get_width() / 2, 300))
        prompt = pygame.font.Font(None, 32).render("Press any key", True, (200, 200, 200))
        surface.blit(prompt, (mid - prompt.get_width() / 2, 380))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            from scenes.gameplay import GameplayScene
            self.manager.replace(GameplayScene(self.manager, self.settings, self.assets))
```

- [ ] **Step 3: Write the remaining scenes** — `scenes/pause.py`:

```python
import pygame
from scene import Scene


class PauseScene(Scene):
    def __init__(self, manager):
        self.manager = manager

    def draw(self, surface):
        surface.fill((0, 0, 0))
        f = pygame.font.Font(None, 48).render("Paused (P)", True, (255, 255, 255))
        surface.blit(f, (300, 280))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.manager.pop()
``````

`scenes/gameover.py`:
```python
import pygame
from scene import Scene
from scenes.start import StartScene


class GameOverScene(Scene):
    def __init__(self, manager, settings, assets, final_score, high_score):
        self.manager = manager
        self.settings = settings
        self.assets = assets
        self.final_score = final_score
        self.high_score = high_score

    def draw(self, surface):
        surface.fill((0, 0, 0))
        f = pygame.font.Font(None, 48)
        mid = self.settings.width / 2
        for text, y, color in [
            ("Game Over", 200, (255, 255, 255)),
            (f"Score: {self.final_score}", 280, (255, 255, 255)),
            (f"High Score: {self.high_score}", 340, (255, 200, 0)),
            ("Press any key to restart", 420, (200, 200, 200)),
        ]:
            surf = f.render(text, True, color)
            surface.blit(surf, (mid - surf.get_width() // 2, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.manager.replace(StartScene(self.manager, self.settings, self.assets, self.high_score))
```

- [ ] **Step 4: Commit (after task 12 completes the GameplayScene import wiring)** Run: `git add hud.py scenes/ && git commit -m "feat: start/pause/game-over scenes + HUD"`

---

## Task 12: Gameplay scene (systems orchestration) + main entry point

**Files:**
- Create: `scenes/gameplay.py`, `main.py`
- Test: `tests/test_main_smoke.py` (uses dummy video driver)

**Interfaces — Consumes:** everything above.
**Produces:** `scenes.gameplay.GameplayScene(manager, settings, assets)` and `main.py` entry that runs the app.

- [ ] **Step 1: Write the smoke test** — `tests/test_main_smoke.py`:

```python
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from game import Game
from scenes.start import StartScene
from settings import GameSettings
from assets import AssetManager


def test_boot_and_teardown():
    pygame.init()
    settings = GameSettings.default()
    game = Game(settings)
    game.manager.replace(StartScene(game.manager, settings, AssetManager(settings), 0))
    game.manager.quit()
    pygame.quit()
```

- [ ] **Step 2: Run smoke test** Run: `pytest tests/test_main_smoke.py -v` → PASS (boots headless, no crash).

- [ ] **Step 3: Write `scenes/gameplay.py`** — orchestrate all systems:

```python
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
        self.ship.draw(surface)
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
```

- [ ] **Step 4: Write `main.py`**:

```python
from settings import GameSettings
from game import Game
from assets import AssetManager
from scenes.start import StartScene


def main():
    settings = GameSettings.default()
    game = Game(settings)
    assets = AssetManager(settings)
    game.run(StartScene(game.manager, settings, assets, 0))


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run all tests** Run: `pytest -q` → all pass (settings, game, assets, bullets, ship, monsters, powerups, scoring, waves, combat, smoke). Also boot a few headless update ticks:

- [ ] **Step 6: Commit** Run: `git add scenes/gameplay.py main.py tests/test_main_smoke.py && git commit -m "feat: gameplay scene + main entry point"`

---

## Task 13: README, package init, cleanup, full verification

**Files:**
- Modify: `README.md` (rewrite for new structure/controls), delete `scenes/__init__.py` contents if unused, remove old `config.py`, `logger.py`, `score.py`, `explosion_old`, and the git-tracked `space_ship.log`.

**Interfaces:** None.

- [ ] **Step 1: Remove obsolete modules** Run:
```bash
git rm -f config.py logger.py monster.py laser.py score.py explosion.py ship.py main.py 2>/dev/null || true
rm -f space_ship.log high_score.txt
```
(Old top-level modules were superseded by `entities/`/`systems/`; `main.py` is recreated in the new structure.)

- [ ] **Step 2: Rewrite README.md** documenting: install (`pip install -r requirements.txt`), run (`python main.py`), controls (arrows=move, space=fire, P=pause), architecture overview, testing (`pytest`).

- [ ] **Step 3: Ensure all modules commit** Run:
```bash
find . -name "*.py" | grep -v __pycache__ | sort
```
Verify `main.py`, `game.py`, `scene.py`, `assets.py`, `settings.py`, `hud.py`, `entities/`, `systems/`, `scenes/`, `tests/` all present.

- [ ] **Step 4: Run the full suite** Run: `pytest -q` → all green.

- [ ] **Step 5: Headless playable smoke** Run:
```bash
SDL_VIDEODRIVER=dummy python -c "import main"
```
Expected: no exceptions at import time.

- [ ] **Step 6: Commit** Run:
```bash
git add -A && git commit -m "chore: rewrite README, remove obsolete modules, final polish"
```
