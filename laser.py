# laser.py

import pygame  # 导入pygame库
from config import *  # 从config文件导入所有变量

class Laser(pygame.sprite.Sprite):
    """
    激光类，继承自pygame.sprite.Sprite
    用于表示玩家发射的激光
    """
    def __init__(self, image, pos):
        """
        初始化激光对象
        :param image: 激光的图像
        :param pos: 激光的初始位置
        """
        super().__init__()  # 调用父类的初始化方法
        self.image = image  # 设置激光的图像
        self.rect = self.image.get_rect(midbottom=pos)  # 获取图像的矩形区域，并设置初始位置
        self.speed = LASER_SPEED  # 设置激光的速度

    def update(self):
        """
        更新激光的位置
        如果激光移出屏幕顶部，则将其销毁
        """
        self.rect.y -= self.speed  # 更新激光的垂直位置
        if self.rect.bottom < 0:  # 如果激光的底部超出屏幕顶部
            self.kill()  # 销毁激光对象