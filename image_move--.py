import sys
import pygame

pygame.init() # 初始化pygame类
screen = pygame.display.set_mode((200, 200)) # 设置窗口大小
pygame.display.set_caption('飞船') # 设置窗口标题
image = pygame.image.load('images/big_ship_image02.bmp') #加载图片
frameNumber = 6 # 设置帧率 所打开的图片帧数为6
frameRect = image.get_rect() # 获取全图的框体数据，以此计算单帧框体
frameRect.width //= frameNumber # 获取每一帧的边框数据 此时将框体锁定第一帧
fps = 10 # 设置刷新率
fcclock = pygame.time.Clock()
n = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if n < frameNumber:
        frameRect.x = frameRect.width * n # 获取第n+1帧的位置信息 即锁定第n+1帧
        n += 1
    else:
        n = 0

    screen.fill((255, 255, 255)) # 设置背景颜色为白色
    screen.blit(image, (50, 50), frameRect)
    fcclock.tick(fps)
    pygame.display.flip() # 刷新窗口