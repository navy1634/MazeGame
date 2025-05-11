# -*- coding: utf-8 -*-

import random

import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.ShortestPaths import ShortestPaths

from app.config import config
from app.config.type import DIRECTION


class MazeMap(Maze):
    def __init__(self) -> None:
        self.px, self.py = 1, 1  # プレイヤーの初期位置
        self.seed: int | None = None
        self.direction = DIRECTION.NORTH  # プレイヤーの初期方向

    def create_maze(self, N: int, M: int, seed: int | None = None):
        # 迷路生成
        super().__init__(seed)
        self.generator = Prims(N, M)
        self.generate()

        # スタートとゴールのマークを設置
        self.start = (1, 1)
        self.end = (N * 2 - 1, M * 2 - 1)

        return self.maze_tolist()

    def solve_maze(self):
        """
        迷路の解答生成アルゴリズム
        """
        # 幅優先探索
        self.solver = ShortestPaths()
        self.solve()
        return self.maze_tolist()

    def maze_tolist(self):
        """
        迷路の成形を行う
        """
        mz_str = str(self).replace("#", "0").replace(" ", "1").replace("S", "2").replace("E", "3").replace("+", "4").split("\n")
        mz_str_list = [list(x) for x in mz_str]
        self.map_data = np.vectorize(int)(mz_str_list)
        return self.map_data

    def get_maze_size(self):
        """
        迷路のサイズを取得する
        """
        return self.generator.H, self.generator.W

    # 初期設定
    def set_default_position(self) -> None:
        self.px = 1
        self.py = 1

    def set_seed(self, seed: int | None = None) -> None:
        """乱数のシードをセットする関数

        Args:
            seed (int): 乱数のシード
        """
        if seed is None:
            self.seed = random.randint(0, 256)
        else:
            self.seed = seed

    def get_player_position(self) -> tuple[int, int]:
        """
        プレイヤーの位置を取得する
        """
        return self.px, self.py

    def move_player(self, px: int, py: int) -> None:
        """
        プレイヤーの位置情報の更新
        """
        self.px = px
        self.py = py

    def check_move(self, px: int, py: int) -> int:
        """移動判定

        Args:
            px (int): x座標
            py (int): y座標

        Returns:
            int: 0: 移動成功, 1: 移動しない, 2: ゴール
        """

        # 移動先がマップデータ外なら戻す
        if px < 0 or px >= len(self.map_data[0]):
            return 1
        if py < 0 or py >= len(self.map_data):
            return 1

        mv = self.map_data[px][py]
        # 移動先が壁なら1を返す
        if mv == 0:
            return 1
        # 移動先がゴールなら2を返す
        elif mv == 3:
            return 2
        return 0

    def _default_direction(self) -> DIRECTION:
        """スタート時に壁に向いていないようにする

        Returns:
            DIRECTION: 初期方向
        """
        px_tmp, py_tmp = self.get_player_position()

        if self.map_data[py_tmp][px_tmp + 1] == 1:
            return DIRECTION.EAST
        elif self.map_data[py_tmp + 1][px_tmp] == 1:
            return DIRECTION.SOUTH
        elif self.map_data[py_tmp][px_tmp - 1] == 1:
            return DIRECTION.WEST
        return DIRECTION.NORTH

    def set_direction(self, direction: DIRECTION) -> None:
        """方向を設定する

        Args:
            direction (int): 方向
        """
        self.direction = direction

    def get_direction(self) -> DIRECTION:
        """方向を取得する

        Returns:
            int: 方向
        """
        return self.direction

    def get_map_viz(self) -> list:
        """3D時のミニマップ取得用

        Returns:
            list: 現在地から 3 * 4 のマップデータ
            # 迷路の行数
            #  |0|1|2|
            #  |3|4|5|
            #  |6|7|8|
            #  |9|A|B|
        """
        map_viz = []
        for i in range(len(config.POS_X[0])):
            map_x = self.px + config.POS_X[self.direction][i]
            map_y = self.py + config.POS_Y[self.direction][i]

            if 0 < map_x < len(self.map_data[0]) and 0 < map_y < len(self.map_data):
                data = self.map_data[map_y][map_x]
            else:
                data = 0
            map_viz.append(data)
        return map_viz
