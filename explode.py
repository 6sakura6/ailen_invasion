import pygame


class Explode():
    """创建一个爆炸类"""
    def __init__(self, screen):
        self.screen = screen
        self.n = 0 # 标记绘制到哪幅爆炸图
        self.nn = self.n # 记录n的该爆炸图的正确定位
        self.image = pygame.image.load('images/explode10.png')
        self.images = ['images/explode10.png', 'images/explode25.png', 
                       'images/explode40.png', 'images/explode60.png']

        # 一颗子弹导致的爆炸效果列表
        self.list = []

    def blitme(self):
        """在飞船爆炸的地方绘制爆炸效果"""
        #for ep_rect in self.list:
        if self.list:
            self.screen.blit(self.image, self.list[0])

    def list_explode(self, location_rect):
        self.list.append(location_rect)

