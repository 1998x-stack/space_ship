# Space Ship

A 2D space shooter rebuilt as a clean, fixed-timestep pygame engine. You pilot a ship,
upgrade your weapon, and survive escalating enemy waves and bosses while chasing the
highest score.


## Features

- **Fixed-timestep engine** — deterministic game logic independent of render FPS
- **Scene system** — start / play / pause / game-over flow via a scene stack
- **3 enemy types** — Drones, Strafers (fire bullets), and Kamikaze chasers
- **Boss** every 5 waves with a large HP bar
- **Weapon upgrades** — single → spread fire, upgraded via pickups
- **Power-ups** — weapon upgrade, shield, and extra life drops
- **Combo scoring** — chain kills for a score multiplier
- 8-direction ship movement with invulnerability window after being hit
- Persistent high score

## Requirements

- Python 3.9+
- pygame 2.x

## Installation

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## Controls

| Action            | Key     |
|-------------------|---------|
| Move              | Arrow keys (4- or 8-direction) |
| Fire              | Space    |
| Pause / Unpause   | P        |

## How to Play

- Destroy enemies to score points; consecutive kills raise your multiplier (up to x4).
- Killed enemies occasionally drop power-ups: **Weapon** (upgrade fire pattern),
  **Shield** (extra life), **Life**.
- Avoid enemy body contact and their bullets — you have only 3 lives, with a short
  invincibility window after each hit.
- Every wave of ~15 enemies escalates difficulty; a **boss** appears every 5 waves.
- The game ends when you run out of lives. Your best score is saved to `high_score.txt`.

## Project Structure

```
main.py            entry point
game.py            fixed-timestep engine + game loop
scene.py           Scene base + SceneManager (stack)
settings.py        validated GameSettings dataclass
assets.py          AssetManager (cached images/sounds with fallbacks)
hud.py             HUD rendering
entities/          sprites (ship, weapons, bullets, monsters, boss, power-ups, explosions)
systems/           logic (waves, combat, scoring)
scenes/            start, gameplay, pause, game-over
tests/             headless pytest suite
```

## Configuration

Tune gameplay in `settings.py` (speeds, lives, wave size, boss cadence, power-up drop
chance, etc.).

## Tests

```bash
python -m pytest -q
```

## License

MIT — see `LICENSE`.