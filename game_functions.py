import sys 

import pygame 

from bullet import Bullet
from alien import Alien
from time import sleep
from explode import Explode

def check_keydown_event(event,ai_settings, screen, ship, bullets):
    """响应按下按键"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 子弹发射音效
        music = pygame.mixer.Sound('musics/music02.mp3')
        music.play()
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:# 若发现不可以运行请检查是否是中文输入法
        sys.exit()

def check_keyup_event(event, ship):
    """响应松开按键"""
    if event.key == pygame.K_RIGHT:
        # 向右停止移动飞船
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                 bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:# 按下
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:# 松开
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                              bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                      bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:# 与非
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats() # 重置飞船的生命 重置分数为0
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #播放音乐
        start_background_music()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
                  play_button, explode, background):
    """更新屏幕上的图像,并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    #绘制背景
    background.blitme()

    # 更新爆炸动效
    update_explode(explode)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():# 方法bullets.sprites()返回一个列表
        bullet.draw_bullet()

    if ship.n < len(ship.images):
        ship.load_image = pygame.image.load(ship.images[ship.n])
        ship.n += 1
    else:
        ship.n = 0
    ship.blitme()

    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见 刷新屏幕
    pygame.display.flip()

def update_explode(explode):
    """更新爆炸的图案"""
    # 若存在子弹打到外星人，并且没有完成爆炸动效时
    if explode.n < len(explode.images) and explode.list:
        # 根据explode.n的累加速度切换图片以显示爆炸动效
        explode.image = pygame.image.load(explode.images[int(explode.n)])
        explode.n += 0.01 # 调节切换爆炸动效的速度
    # 若完成爆炸动效则
    else:
        # 若子弹打到外星人的列表存在
        if explode.list:
            explode.list.pop(0) # 删除最先打到的外星人所爆炸的元素
        explode.n = 0 # 重置n，表示已经完成爆炸动效
    explode.blitme()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explode):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹位置
    # bullet.py中有update函数，bullets.update()会轮流调用bullet.update()
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
                                  aliens, bullets, explode)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
                                  aliens, bullets, explode):
    """响应子弹和外星人的碰撞"""

    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的编组中的子弹和外星人
    # sprite.groupcollide将每颗子弹和每个外星人的rect比较并返回一个字典
    # 其中包含碰撞的子弹和外星人，在这个字典中每个键都是子弹，每个值都是外星人
    #参数True告诉Pygame删除相应的参数--子弹或外星人
    collision = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collision:
        # 爆炸声
        music = pygame.mixer.Sound('musics/music03.mp3')
        music.play()
        for values in collision.values():
            stats.score += ai_settings.alien_points * len(values)
            sb.prep_score()
            for value in values:# 爆炸的外星人的精灵的rect送入爆炸列表
                explode.list_explode(value.rect)
            aliens.remove(values) #将爆炸的外星人删除
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 清除了一群外星人，则
        # 提升外星人等级
        # 删除现有的子弹，同时加快游戏节奏，并新建一群外星人
        bullets.empty()# 使用empty()删除bullets编组的现有所有子弹
        ai_settings.increase_speed()# 提高飞船、子弹、外星人速度，和得分点数

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_setting, screen, ship, bullets):
    """如果还没到达极限，就再发一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    # 如果未消失的子弹大于7颗不允许发射--禁止创建过多子弹
    if len(bullets) < ai_setting.bullets_allowed:
        

        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)
        # 发射子弹的声音
        
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - 
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows - 2


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
                                  alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)
            
def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 1:
        # 将ship_left减一
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕中间底端
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    检查是否有外星人位置屏幕边缘
    并更新外星人群中所有外星人的位置
    """
    # alien.py中有update函数，aliens.update()会轮流调用alien.update()
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    # spritecollideany接受一个精灵和一个编组 检查是否有编组成员和精灵碰撞
    # 若找到则停止遍历编组，并返回第一个与之碰撞的外星人
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open('height_score.txt', 'w') as f_obj:
            f_obj.write(str(stats.high_score))

def start_background_music():
    music_track = pygame.mixer_music.load("musics/music01.mp3")
    pygame.mixer_music.play(-1)
    
    
        
     