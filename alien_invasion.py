import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from explode import Explode
from background import Background

def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建背景
    background = Background(screen, ai_settings)

    # 创建一个Play按钮
    play_button = Button(ai_settings, screen, 'Play')

    # 创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个外星人编组
    aliens = Group()
    # 创建一个爆炸效果
    explode = Explode(screen)

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    pygame.mixer.init() # 初始化音频模块

    # 开始游戏的主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                        bullets)

        if stats.game_active:
            # 更新背景信息
            background.update_background()

            # 更新飞船的坐标位置
            ship.update()
            
            # 更新子弹的位置，并删除已消失的子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, 
                               aliens, bullets, explode)

            # 更新外星人的位置
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        # 更新屏幕上的图像,并切换到新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
                         bullets, play_button, explode, background)

run_game()
