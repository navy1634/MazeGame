# -*- coding: utf-8 -*-

from logging import getLogger
from tkinter import Frame

from config.conf import IMAGE_DIR
from PIL import Image, ImageTk


class Maze3Dto2D(Frame):
    logger = getLogger("maze_root").getChild(__name__)
    # 3Dマップの参照先
    POS_X = [
        [-1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0, 1],
        [3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
        [1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0, -1],
        [-3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0],
    ]
    POS_Y = [
        [-3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0],
        [-1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0, 1],
        [3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
        [1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0, -1],
    ]

    canvas_width = 60
    canvas_height = 100
    bg_color = '#020202'
    tile_size = 40

    def __init__(self, parent) -> None:
        self.parent = parent


    # 迷路生成
    def create_maze(self):
        self.canvas = self.parent.canvas
        # マップとプレイヤーを描画する
        self.player_image = self._load_player(IMAGE_DIR+"/player.png")
        self.draw_maze()
        self.draw_player(self.player_image)
        return self.canvas


    def get_map_viz(self) -> list:
        map_viz = []
        for i in range(12):
            map_x = self.parent.px + self.POS_X[self.parent.direction][i]
            map_y = self.parent.py + self.POS_Y[self.parent.direction][i]

            if 0 < map_x < len(self.parent.map_data[0]) and 0 < map_y < len(self.parent.map_data):
                data = self.parent.map_data[map_y][map_x]
            else:
                data = 0
            map_viz.append(data)
        return map_viz


    # 迷路解読
    def draw_maze(self):
        # 左上から右下へと描画
        # 迷路の行数
        #  |0|1|2|
        #  |3|4|5|
        #  |6|7|8|
        #  |9|A|B|
        map_viz = self.get_map_viz()

        for y in range(4):
            y1 = y * self.tile_size + (600-self.tile_size*5)
            y2 = y1 + self.tile_size
            for x in range(3):
                x1 = x * self.tile_size + 800-self.tile_size*3
                x2 = x1 + self.tile_size
                # 該当場所の値を得る
                p = map_viz[y*3+x]
                # 値に応じた色を決定する
                if p == 0:
                    color = "#404040"
                if p == 1:
                    color = "white"
                if p == 2:
                    color = "red"
                if p == 3:
                    color = "blue"
                if p == 4:
                    color = "green"
                # 正方形を描画
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, # 座標
                    fill=color, # 塗色
                    outline="black", width=2) # 枠線


    # プレイヤー生成
    def _load_player(self, image_filename):
        """
        プレイヤーの画像を読み込む
        """
        img = Image.open(image_filename)
        img_tk = ImageTk.PhotoImage(img)
        return img_tk


    # プレイヤー描画
    def draw_player(self, player_image):
        self.canvas.create_image(800-self.tile_size*2+10, 600-self.tile_size*2+10, image=player_image, anchor="nw")


    # 迷路表示
    def draw_map(self):
        # マップとプレイヤーを描画する
        self.draw_maze()
        self.draw_player(player_image=self.player_image)

