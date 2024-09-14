# ship.py

import pygame  # 导入pygame库
from config import *  # 从config文件导入所有变量
from laser import Laser  # 从laser模块导入Laser类

class Ship(pygame.sprite.Sprite):
    """飞船类，继承自pygame.sprite.Sprite"""
    
    def __init__(self, image):
        """初始化飞船对象
        
        Args:
            image: 飞船的图像
        """
        super().__init__()  # 调用父类的初始化方法
        self.image = image  # 设置飞船图像
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10))  # 设置飞船位置
        self.speed = SHIP_SPEED  # 设置飞船速度
        self.lives = SHIP_LIVES  # 设置飞船生命值
        self.last_shot = pygame.time.get_ticks()  # 记录上次射击时间

    def update(self, keys):
        """更新飞船位置
        
        Args:
            keys: 按键状态
        """
        if keys[pygame.K_LEFT]:  # 如果按下左键
            self.rect.x -= self.speed  # 向左移动
        if keys[pygame.K_RIGHT]:  # 如果按下右键
            self.rect.x += self.speed  # 向右移动

        # 边界检查
        if self.rect.left < 0:  # 如果超出左边界
            self.rect.left = 0  # 限制在左边界
        if self.rect.right > SCREEN_WIDTH:  # 如果超出右边界
            self.rect.right = SCREEN_WIDTH  # 限制在右边界

    def shoot(self, laser_image, laser_group, shoot_sound):
        """发射激光
        
        Args:
            laser_image: 激光图像
            laser_group: 激光精灵组
            shoot_sound: 射击音效
        """
        current_time = pygame.time.get_ticks()  # 获取当前时间
        if current_time - self.last_shot > LASER_COOLDOWN:  # 如果冷却时间已过
            laser = Laser(laser_image, self.rect.midtop)  # 创建新的激光对象
            laser_group.add(laser)  # 将激光添加到精灵组
            self.last_shot = current_time  # 更新上次射击时间
            shoot_sound.play()  # 播放射击音效

    def lose_life(self):
        """失去一条生命"""
        self.lives -= 1  # 生命值减1
        if self.lives <= 0:  # 如果生命值小于等于0
            self.kill()  # 销毁飞船精灵