
# Space Ship Game

A 2D space shooter game built with Python's `pygame` library, where you control a spaceship to shoot and destroy enemies. The game features increasing difficulty as enemy spawn rates increase over time.

## Features

- Control a spaceship to shoot lasers and destroy incoming enemies.
- The difficulty increases as the game progresses, with faster and more frequent enemy spawns.
- Explosive effects when enemies are destroyed.
- Score tracking and high score saving.
- Smooth gameplay with background music and sound effects.
- Pause functionality and game-over screen.

## Table of Contents

- [Installation](#installation)
- [How to Play](#how-to-play)
- [Controls](#controls)
- [Configuration](#configuration)
- [Game Assets](#game-assets)
- [Contribution](#contribution)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/1998x-stack/space_ship.git
   ```

2. Navigate to the project directory:
   ```bash
   cd space_ship
   ```

3. Install the dependencies:
   ```bash
   pip install pygame
   ```

4. Run the game:
   ```bash
   python main.py
   ```

## How to Play

The goal is to control the spaceship to shoot and destroy as many enemies as possible while avoiding collision. As time passes, the enemies will spawn more frequently and move faster. Survive for as long as you can to achieve the highest score.

When your spaceship runs out of lives, the game ends, and you will see your final score along with the highest score you’ve achieved.

## Controls

| Action          | Key          |
|-----------------|--------------|
| Move Left       | `←`          |
| Move Right      | `→`          |
| Shoot Laser     | `Space`      |
| Pause/Unpause   | `P`          |

## Configuration

The game settings such as screen size, spaceship speed, laser speed, enemy spawn rates, etc., are configurable via the `config.py` file. You can modify these parameters to adjust the difficulty or change the gameplay experience.

Example of `config.py` settings:
```python
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Ship settings
SHIP_SPEED = 5
SHIP_LIVES = 3

# Laser settings
LASER_SPEED = 7
LASER_COOLDOWN = 500  # milliseconds

# Enemy settings
INITIAL_MONSTER_SPAWN_RATE = 0.01
MAX_MONSTER_SPAWN_RATE = 0.2
SPAWN_RATE_INCREMENT = 0.0001
MONSTER_SPEED = 2
```

## Game Assets

The assets (images and sounds) used in the game are located in the `assets/` folder:

```
- assets/
    - images/
        - ship.png         # Spaceship image
        - monster.png      # Enemy image
        - laser.png        # Laser image
        - background.png   # Background image
        - explosion1.png to explosion9.png  # Explosion animation frames
    - sounds/
        - shoot.wav        # Shooting sound effect
        - explosion.wav    # Explosion sound effect
        - background.mp3   # Background music
```

You can replace these assets with your own to customize the game visuals and sounds.

## Contribution

Contributions are welcome! Feel free to submit a pull request or open an issue if you have ideas for improvements or encounter any problems.

### How to Contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-or-bug-fix
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-or-bug-fix
   ```
5. Open a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


### **无人飞船打怪游戏操作指南**

#### **1. 游戏目的**
控制你的飞船，击败从上方出现的怪物，同时避免与怪物碰撞。尽可能获得更高的分数。

---

#### **2. 操作方式**

- **移动飞船：**
  - **向左移动**：按 `左方向键 (←)`
  - **向右移动**：按 `右方向键 (→)`

- **发射激光：**
  - 按 `空格键 (Space)` 发射激光攻击怪物。

- **暂停游戏：**
  - 按 `P` 键暂停游戏，再按一次 `P` 键继续游戏。

---

#### **3. 游戏界面**

- **飞船生命值**：
  - 游戏右上角显示当前剩余的飞船生命值，生命值为 0 时游戏结束。
  
- **分数**：
  - 屏幕左上角显示当前的游戏分数，击败怪物可以获得分数。

- **帧率显示**：
  - 右上角显示当前游戏帧率（FPS），用于游戏调试或优化。

---

#### **4. 游戏进程**

- **怪物生成**：
  - 怪物从屏幕顶部随机位置生成，随着时间推移，怪物的生成速度逐渐加快。
  
- **击败怪物**：
  - 发射激光击中怪物可以消灭怪物并获得积分，消灭怪物时会播放爆炸效果和声音。

- **飞船碰撞**：
  - 如果飞船与怪物碰撞，飞船会失去一条生命，游戏中的爆炸效果会被触发。

- **游戏结束**：
  - 当飞船的生命值为 0 时，游戏结束，显示最终得分以及最高分。

---

#### **5. 游戏开始与结束**

- **开始界面**：
  - 游戏启动时，显示“开始界面”，按任意键开始游戏。

- **结束界面**：
  - 游戏结束时，显示“游戏结束”界面，显示最终得分和最高得分。按任意键可以重新开始游戏。

---

#### **6. 提示**
- 随着时间增加，怪物生成的速度和难度会逐渐提升，请尽快消灭怪物，避免飞船被击中。
- 你可以通过击败怪物获得更高的分数，挑战你的最高分！

---
