# Space Ship — Reconstruction & Improvement Design

Date: 2026-08-14
Status: Approved by user
Goal: Rebuild the existing pygame space-shooter into a clean-architecture game **and** expand gameplay meaningfully.

## Context

The current `space_ship` project is a small, working pygame 2D shooter (ship, lasers,
monsters, explosions, score, lives, high-score file). Early fixes already applied:
Applied early fixes: removed per-frame disk logging, removed float drift in the spawn-rate
curve, moved magic numbers into `config.py`, and replaced `from config import *` with
`import config`. The remaining `score.py` broad-`except` cleanup is carried into the new
`systems/scoring.py` module.

This reconstruction replaces the flat file structure with a decoupled engine/scene/system/
entity layout, adds a fixed-timestep loop, and expands the gameplay.

## Non-Goals (YAGNI for v1)

- Settings/menu configuration UI
- Persistent meta-unlocks / progression outside high score
- Networking / multiplayer
- Custom content / level editor

## Architecture

A small fixed-timestep engine wrapping pygame with tight, single-purpose modules:

```
space_ship/
├── main.py            # entry point: build settings + Game, run engine
├── settings.py        # dataclass-based config with validation
├── assets.py          # AssetManager: load/cache images, sounds, fonts
├── game.py            # Game engine: window, fixed-timestep loop, scene stack
├── scene.py           # Scene base class + SceneManager (stack-based)
├── hud.py             # HUD rendering (score, lives, combo, wave)
├── entities/
│   ├── ship.py        # player (lives, shield, invulnerability timer)
│   ├── weapons.py     # fire patterns + weapon levels
│   ├── bullets.py     # player + enemy bullets
│   ├── monsters.py    # Drone / Strafe / Kamikaze (data-driven behaviors)
│   ├── boss.py
│   ├── powerups.py    # weapon, shield, extra-life pickups
│   └── explosion.py
├── systems/
│   ├── waves.py       # wave builder + boss scheduling + difficulty curve
│   ├── combat.py      # collision resolution (decoupled from sprites)
│   └── scoring.py     # points, combo/multiplier, high score persistence
├── scenes/
│   ├── start.py
│   ├── gameplay.py    # orchestrates systems during Play
│   ├── pause.py
│   └── game_over.py
└── tests/             # headless logic tests (no display needed)
```

**Responsibility rules:**
- `game.py` owns the window and loop; never touches gameplay.
- `scenes` own state/transitions.
- `systems` hold game logic.
- `entities` are pure sprites with no game-loop responsibility.
- `assets.py` hides all file I/O.

## Fixed-Timestep Loop

- Updates at `1/60s` regardless of render FPS (accumulator + clamping) for deterministic,
  frame-rate-independent physics and spawns.
- Render and input are decoupled from the simulation.
- Display current FPS and real dt for debugging.

## Entities & Combat

- Waves consist of ~15 enemies each; a boss spawns **every 5 waves**.
- Monsters share a base class with **data-driven traits** (speed, hp, fire behavior, score)
  sourced from a monster template table:
  - **Drone** — slow, straight down (10 pts)
  - **Strafer/Shooter** — descends, strafes, fires aimed bullets (25 pts)
  - **Kamikaze** — fast, chases player (15 pts)
  - **Boss** — large HP, multi-pattern bullets, big score
- Collision resolution lives in `systems/combat.py` (hit → score / power-up drop / kill),
  kept separate from sprite classes.

## Player & Progression

- 8-direction movement; 3 lives; **1.5s invulnerability window** after any hit (blinking feedback).
- **Weapon levels** 1–3 (single → spread → rapid), upgraded via power-ups.
- **Power-ups** drop from killed monsters: weapon-up, shield, extra life.
- **Waves** (of ~15 enemies) escalate spawn rate/aggression; **boss** spawns every 5 waves.
- **Combo multiplier** from consecutive kills; resets on player hit.

## Scenes & Flow

- `Start → Play → (Pause ⇄ Play) → GameOver → Start`, via a stack-based `SceneManager`.
- High score persisted to `high_score.txt`, shown on Start and Game Over screens.

## Error Handling & Assets

- `AssetManager` fails with clear messages; provides cheap default fallbacks (filled rect +
  text) so the game still runs if an asset is missing.
- All file/resource access is wrapped; never crashes on a missing file.

## Delivery

- `requirements.txt` (pygame), `.gitignore` (log, `__pycache__`, `high_score.txt`),
  `LICENSE` (MIT), updated `README`.

## Testing

- Unit-test **logic only** (no display): settings validation, fixed-timestep accumulator,
  scoring/combo math, high-score parse, wave difficulty curve, monster-template field
  integrity, collision resolution.
- Use `pytest`; game itself smoke-tested with `SDL_VIDEODRIVER=dummy`.