# score.py
# 分数模块

import pygame  # 导入pygame库
from config import *  # 从config文件导入所有变量

class Score:
    """
    分数类：用于管理游戏分数和最高分
    """
    def __init__(self):
        """
        初始化分数对象
        """
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)  # 创建字体对象
        self.score = 0  # 初始化当前分数
        self.high_score = self.load_high_score()  # 加载最高分

    def increase(self, amount):
        """
        增加分数
        :param amount: 增加的分数量
        """
        self.score += amount  # 增加当前分数
        if self.score > self.high_score:
            self.high_score = self.score  # 更新最高分（如果需要）

    def draw(self, surface):
        """
        在屏幕上绘制分数
        :param surface: 绘制的表面
        """
        score_surf = self.font.render(f'Score: {self.score}', True, WHITE)  # 渲染当前分数文本
        high_score_surf = self.font.render(f'High Score: {self.high_score}', True, RED)  # 渲染最高分文本
        surface.blit(score_surf, (10, 10))  # 绘制当前分数
        surface.blit(high_score_surf, (10, 30))  # 绘制最高分

    def load_high_score(self):
        """
        从文件加载最高分
        :return: 最高分
        """
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())  # 读取并返回最高分
        except:
            return 0  # 如果出错，返回0

    def save_high_score(self):
        """
        保存最高分到文件
        """
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))  # 将最高分写入文件