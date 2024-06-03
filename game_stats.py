import os

class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 让游戏刚启动时处处于非活动状态
        self.game_active = False

        # 在任何情况下都不应该重置最高分
        self.high_score = int(self.get_high_score())

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        """读取本地文件的最高分"""
        # 先检查是否存在该文件
        if os.path.exists('height_score.txt'):
            with open('height_score.txt') as f_obj:
                high_score = f_obj.read()
            return high_score
        else:
            return 0