import pygame

class Background():
    """背景类"""
    def __init__(self, screen, ai_settings):
        self.screen = screen
        self.ai_settings = ai_settings
        self.bk_1 = pygame.image.load("images/bk01.bmp")
        self.bk_2 = pygame.image.load('images/bk02.bmp')

        # 获取背景和屏幕的矩形框
        self.bk_1_rect = self.bk_1.get_rect()
        self.bk_2_rect = self.bk_2.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.bk_2_rect.y = -self.bk_2_rect.height + 2

        self.y1 = float(self.bk_1_rect.y)
        self.y2 = float(self.bk_2_rect.y)

    def update_background(self):
        """移动背景"""
        self.y1 += self.ai_settings.background_speed_factor
        self.y2 += self.ai_settings.background_speed_factor
        self.bk_1_rect.y = self.y1
        self.bk_2_rect.y = self.y2

        if self.y1 > self.screen_rect.height:
            self.y1 = -self.screen_rect.height
        if self.y2 > self.screen_rect.height:
            self.y2 = -self.screen_rect.height

    def blitme(self):
        self.screen.blit(self.bk_1, self.bk_1_rect)
        self.screen.blit(self.bk_2, self.bk_2_rect)