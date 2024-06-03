import pygame
from pygame.sprite import Sprite

# 让Ship继承Sprite以便可以对其进行编组
class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载飞船图像、调整大小并获取其调整后的外界矩形
        # 加载静态的飞船--显示剩余生命
        self.image = pygame.image.load('images/ship02.bmp')
        self.load_image = pygame.image.load('images/ship02.bmp')

        self.images = ['images/ship02.bmp', 'images/shop02_left_five_point.bmp',
               'images/ship02.bmp', 'images/shop02_right_five_point.bmp',
               'images/ship02.bmp', 'images/shop02_down_three_point.bmp']
        self.n = 0 # 标记当前要画哪幅图像

        #调整图像大小 使用pygame.transform.scale(self.image, (50, 50))
        self.scaled_image = pygame.transform.scale(self.image, (100, 100))
        # 剩余的飞船图标大小
        self.left_scaled_image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.scaled_image.get_rect()# 飞船的矩形框
        self.screen_rect = self.screen.get_rect()# 屏幕的矩形框

        #将每艘飞船放在屏幕底部中央
        #将屏幕的指定坐标值赋予self.rect 飞船中心x坐标和下边缘的y坐标
        self.rect.centerx = self.screen_rect.centerx 
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值 以便更加细致调整飞船移动速度
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center的值，而不是rect  飞船右边缘小于屏幕右边缘
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        # 使用if而不用elif的原因是处理同时按下左右两个键时让飞船保持不动
        # 飞船左边缘 > 0
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.load_image, self.rect)

    def blitme_left(self):
        """绘制剩下飞船的数量"""
        self.screen.blit(self.left_scaled_image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx

