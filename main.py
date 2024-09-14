# main.py

import pygame  # 导入pygame库
import random  # 导入random库，用于生成随机数
from config import *  # 从config文件导入所有变量
from ship import Ship  # 从ship模块导入Ship类
from monster import Monster  # 从monster模块导入Monster类
from score import Score  # 从score模块导入Score类
from explosion import Explosion  # 从explosion模块导入Explosion类
from logger import setup_logger, log_event # 导入日志记录器

setup_logger()  # 初始化日志记录器

def show_start_screen(screen):
    """显示游戏开始界面"""
    font = pygame.font.SysFont(FONT_NAME, 48)  # 创建字体对象
    title_surf = font.render('Spaceship Monster Shooter', True, WHITE)  # 渲染标题文本
    log_event('Start game')  # 记录日志
    screen.fill(BLACK)  # 填充屏幕为黑色
    screen.blit(title_surf, (SCREEN_WIDTH / 2 - title_surf.get_width() / 2, SCREEN_HEIGHT / 2 - title_surf.get_height() / 2))  # 绘制标题
    pygame.display.flip()  # 更新屏幕显示
    wait_for_key()  # 等待玩家按键

def show_game_over_screen(screen, final_score):
    """显示游戏结束界面和最终得分"""
    screen.fill(BLACK)  # 填充屏幕为黑色
    font = pygame.font.SysFont(FONT_NAME, 48)  # 创建字体对象
    game_over_surf = font.render('Game Over', True, WHITE)  # 渲染游戏结束文本
    log_event('Game over')  # 记录日志
    score_surf = font.render(f'Score: {final_score}', True, WHITE)  # 渲染得分文本
    screen.blit(game_over_surf, (SCREEN_WIDTH / 2 - game_over_surf.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_surf.get_height()))  # 绘制游戏结束文本
    screen.blit(score_surf, (SCREEN_WIDTH / 2 - score_surf.get_width() / 2, SCREEN_HEIGHT / 2 + 50))  # 绘制得分文本
    pygame.display.flip()  # 更新屏幕显示
    wait_for_key()  # 等待玩家按键

def wait_for_key():
    """等待玩家按键开始或结束游戏"""
    waiting = True
    clock = pygame.time.Clock()  # 创建时钟对象
    log_event('Pause game')  # 记录日志
    while waiting:
        clock.tick(FPS)  # 控制循环频率
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果是退出事件
                log_event('Quit game')  # 记录日志
                pygame.quit()  # 退出pygame
                exit()  # 退出程序
            if event.type == pygame.KEYUP:  # 如果是按键释放事件
                log_event('Resume game')  # 记录日志
                waiting = False  # 结束等待

def pause(screen):
    """游戏暂停功能"""
    paused = True
    font = pygame.font.SysFont(FONT_NAME, 48)  # 创建字体对象
    pause_surf = font.render('Game Paused', True, WHITE)  # 渲染暂停文本
    log_event('Pause game')  # 记录日志
    screen.blit(pause_surf, (SCREEN_WIDTH / 2 - pause_surf.get_width() / 2, SCREEN_HEIGHT / 2))  # 绘制暂停文本
    pygame.display.flip()  # 更新屏幕显示
    while paused:
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果是退出事件
                log_event('Quit game')  # 记录日志
                pygame.quit()  # 退出pygame
                exit()  # 退出程序
            if event.type == pygame.KEYUP and event.key == pygame.K_p:  # 如果是P键释放事件
                log_event('Resume game')  # 记录日志
                paused = False  # 结束暂停

def main():
    """主游戏程序"""
    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建游戏窗口
    pygame.display.set_caption('Spaceship Monster Shooter')  # 设置窗口标题
    clock = pygame.time.Clock()  # 创建时钟对象

    # 加载资源
    ship_image = pygame.image.load(IMAGE_PATH + 'ship.png').convert_alpha()  # 加载飞船图片
    ship_image = pygame.transform.scale(ship_image, (50, 50))  # 缩放飞船图片到50x50像素

    laser_image = pygame.image.load(IMAGE_PATH + 'laser.png').convert_alpha()  # 加载激光图片
    laser_image = pygame.transform.scale(laser_image, (10, 30))  # 缩放激光图片到10x30像素

    monster_image = pygame.image.load(IMAGE_PATH + 'monster.png').convert_alpha()  # 加载怪物图片
    monster_image = pygame.transform.scale(monster_image, (60, 60))  # 缩放怪物图片到60x60像素

    background_image = pygame.image.load(IMAGE_PATH + 'background.png').convert()  # 加载背景图片
    background_image = background_image.subsurface((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))  # 截取背景图片

    # 加载声音
    shoot_sound = pygame.mixer.Sound(SOUND_PATH + 'shoot.wav')  # 加载射击音效
    explosion_sound = pygame.mixer.Sound(SOUND_PATH + 'explosion.wav')  # 加载爆炸音效
    pygame.mixer.music.load(SOUND_PATH + 'background.mp3')  # 加载背景音乐
    pygame.mixer.music.play(-1)  # 循环播放背景音乐

    # 加载爆炸动画并缩放
    explosion_images = []
    for i in range(1, 10):
        img = pygame.image.load(IMAGE_PATH + f'explosion{i}.png').convert_alpha()  # 加载爆炸动画帧
        img = pygame.transform.scale(img, (60, 60))  # 缩放爆炸动画到60x60像素
        explosion_images.append(img)

    # 显示开始界面
    show_start_screen(screen)

    # 创建精灵组
    ship = Ship(ship_image)  # 创建飞船对象
    ship_group = pygame.sprite.GroupSingle(ship)  # 创建飞船精灵组
    laser_group = pygame.sprite.Group()  # 创建激光精灵组
    monster_group = pygame.sprite.Group()  # 创建怪物精灵组
    explosion_group = pygame.sprite.Group()  # 创建爆炸精灵组

    # 初始化变量
    running = True
    monster_spawn_rate = INITIAL_MONSTER_SPAWN_RATE  # 初始怪物生成率
    log_event(f"Initial monster spawn rate: {INITIAL_MONSTER_SPAWN_RATE}")
    score = Score()  # 创建得分对象

    while running:
        clock.tick(FPS)  # 控制游戏帧率
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果是退出事件
                running = False  # 结束游戏循环

        keys = pygame.key.get_pressed()  # 获取按键状态
        ship_group.update(keys)  # 更新飞船状态
        laser_group.update()  # 更新激光状态
        monster_group.update()  # 更新怪物状态
        explosion_group.update()  # 更新爆炸状态
        log_event('Update game')  # 记录日志

        # 发射激光
        if keys[pygame.K_SPACE]:  # 如果按下空格键
            log_event('Shoot laser')  # 记录日志
            ship.shoot(laser_image, laser_group, shoot_sound)  # 飞船发射激光

        # 暂停功能
        if keys[pygame.K_p]:  # 如果按下P键
            pause(screen)  # 暂停游戏

        # 怪物生成逻辑
        if random.random() < monster_spawn_rate:  # 随机生成怪物
            speed = random.uniform(MONSTER_SPEED, MONSTER_SPEED + 2)  # 随机生成怪物速度
            monster = Monster(monster_image, speed)  # 创建怪物对象
            monster_group.add(monster)  # 将怪物添加到精灵组
            log_event("Spawn monster")

        # 增加怪物生成概率
        if monster_spawn_rate < MAX_MONSTER_SPAWN_RATE:  # 如果生成率未达到最大值
            monster_spawn_rate += SPAWN_RATE_INCREMENT  # 增加生成率
            log_event(f"Increase monster spawn rate: {monster_spawn_rate}")

        # 碰撞检测：激光击中怪物
        laser_hits = pygame.sprite.groupcollide(laser_group, monster_group, True, True)  # 检测激光和怪物的碰撞
        for hit in laser_hits:
            explosion_sound.play()  # 播放爆炸音效
            score.increase(10)  # 增加得分
            explosion = Explosion(hit.rect.center, explosion_images)  # 创建爆炸对象
            explosion_group.add(explosion)  # 将爆炸添加到精灵组
            log_event("Monster hit")

        # 碰撞检测：怪物碰到飞船
        monster_hits = pygame.sprite.spritecollide(ship, monster_group, True)  # 检测飞船和怪物的碰撞
        for hit in monster_hits:
            explosion_sound.play()  # 播放爆炸音效
            ship.lose_life()  # 飞船失去一条生命
            explosion = Explosion(hit.rect.center, explosion_images)  # 创建爆炸对象
            explosion_group.add(explosion)  # 将爆炸添加到精灵组
            log_event("Ship hit")
            if ship.lives <= 0:  # 如果生命值为0
                running = False  # 游戏结束

        # 绘制元素
        screen.blit(background_image, (0, 0))  # 绘制背景
        ship_group.draw(screen)  # 绘制飞船
        laser_group.draw(screen)  # 绘制激光
        monster_group.draw(screen)  # 绘制怪物
        explosion_group.draw(screen)  # 绘制爆炸
        score.draw(screen)  # 绘制得分

        # 显示生命值
        font = pygame.font.SysFont(FONT_NAME, int(FONT_SIZE * 1.5))
        lives_surf = font.render(f'Lives: {ship.lives}; FULL Lives: {SHIP_LIVES}', True, RED if ship.lives == 1 else WHITE)
        lives_rect = lives_surf.get_rect()
        lives_rect.midtop = (SCREEN_WIDTH // 2, 10)  # 将文本居中，距离顶部10像素
        screen.blit(lives_surf, lives_rect)

        # 显示帧率
        fps = int(clock.get_fps())  # 获取当前帧率
        fps_surf = font.render(f'FPS: {fps}', True, WHITE)  # 渲染帧率文本
        screen.blit(fps_surf, (SCREEN_WIDTH - 100, 30))  # 绘制帧率

        pygame.display.flip()  # 更新屏幕显示

    # 显示游戏结束界面
    score.save_high_score()  # 保存最高分
    show_game_over_screen(screen, score.score)  # 显示游戏结束界面

    pygame.quit()  # 退出pygame

if __name__ == '__main__':
    main()  # 运行主游戏程序