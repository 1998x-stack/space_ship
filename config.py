# config.py

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # 帧率

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 飞船设置
SHIP_SPEED = 5
SHIP_LIVES = 3  # 新增，飞船生命值

# 激光设置
LASER_SPEED = 7
LASER_COOLDOWN = 500  # 新增，激光冷却时间（毫秒）

# 怪物设置
INITIAL_MONSTER_SPAWN_RATE = 0.01
MAX_MONSTER_SPAWN_RATE = 0.06
SPAWN_RATE_INCREMENT = 0.00001
MONSTER_SPEED = 2

# 资源路径
IMAGE_PATH = 'assets/images/'
SOUND_PATH = 'assets/sounds/'

# 字体设置
FONT_NAME = 'arial'
FONT_SIZE = 20