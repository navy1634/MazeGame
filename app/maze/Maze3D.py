# -*- coding: utf-8 -*-

from logging import getLogger
from tkinter import BOTH, Canvas, Frame, Tk

from maze.Maze3Dsub import Maze3Dto2D
from maze.MazeMap import MazeCreate


class Maze3D(Frame):
    logger = getLogger("maze_root").getChild(__name__)
    # 方向定義
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    COLOR0 = "#a5bcf9"
    COLOR1 = "#626e97"
    COLOR2 = "#535c7f"
    COLOR3 = "#404864"
    COLOR4 = "#37d86e"

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


    def __init__(self, parent, conf) -> None:
        super().__init__(parent)
        self.parent = parent
        self.conf = conf
        self.Frame_Width = conf["3D"]["Frame_Width"]
        self.Frame_Height = conf["3D"]["Frame_Height"]
        self.maze = MazeCreate()


    # 迷路生成
    def create_maze(self, flag=False) -> Canvas:
        self.canvas = Canvas(
            self.parent,
            width=self.Frame_Width,
            height=self.Frame_Height,
            background='#020202'
        )
        self.canvas.pack(fill=BOTH, expand=True)
        # マップとプレイヤーを描画する
        if not flag:
            self.return_default()
        self.direction = self._default_direction()
        self.draw_maze()
        self.subcanvas.create_maze()
        return self.canvas


    def load_maze(self, seed):
        self._maze_config()
        self.load_map(Height=self.Maze_Height, Width=self.Maze_Width, seed=seed)
        self.subcanvas =  Maze3Dto2D(self)


    # マップ生成
    def load_map(self, Height, Width, seed=None):
        self.map_data = self.maze.create_maze(Height, Width, seed=seed)



    # 迷路解答
    def get_ans(self):
        self.map_data = self.maze.solve_maze()


    # 初期設定
    def return_default(self):
        self.px = 1
        self.py = 1


    # 迷路解読
    def get_map_viz(self) -> list:
        map_viz = []
        for i in range(len(self.POS_X[0])):
            map_x = self.px + self.POS_X[self.direction][i]
            map_y = self.py + self.POS_Y[self.direction][i]

            if 0 < map_x < len(self.map_data[0]) and 0 < map_y < len(self.map_data):
                data = self.map_data[map_y][map_x]
            else:
                data = 0
            map_viz.append(data)
        return map_viz

    # Canvas に描画
    def draw_maze(self):
        map_viz = self.get_map_viz()
        self._wall_row_first(map_viz)

        self.canvas.create_line(100, 470, 700, 470, fill=self.COLOR1)

        if map_viz[7] == 0:
            self.canvas.create_line(100, 130, 700, 130, fill=self.COLOR1)
        else:
            self._wall_row_second(map_viz)
            if map_viz[7] == 4:
                self.canvas.create_line(100, 470, 700, 470, fill=self.COLOR4)
            self.canvas.create_line(200, 420, 600, 420, fill=self.COLOR2)

            if map_viz[4] == 0:
                self.canvas.create_line(200, 180, 600, 180, fill=self.COLOR2)
            else:
                self._wall_row_third(map_viz)
                if map_viz[4] == 4:
                    self.canvas.create_line(200, 420, 600, 420, fill=self.COLOR4)
                self.canvas.create_line(280, 380, 520, 380, fill=self.COLOR3)

                if map_viz[1] == 0:
                    self.canvas.create_line(280, 220, 520, 220, fill=self.COLOR3)
                else:
                    self._wall_row_fourth(map_viz)
                    if map_viz[1] == 4:
                        self.canvas.create_line(280, 380, 520, 380, fill=self.COLOR4)
                    self.canvas.create_line(320, 360, 480, 360, fill=self.COLOR3)


    # 迷路表示
    def draw_map(self):
        # マップとプレイヤーを描画する
        self.canvas.delete("all")
        self.draw_maze()
        self.subcanvas.draw_map()

    def draw_map_event(self):
        # マップとプレイヤーを描画する
        self.canvas.delete("all")
        self.direction = self._default_direction()
        self.draw_maze()
        self.subcanvas.draw_map()


    # スタート時に壁に向いていないようにする
    def _default_direction(self):
        if self.map_data[self.py][self.px+1] == 1:
            return self.EAST
        elif self.map_data[self.py+1][self.px] == 1:
            return self.SOUTH
        elif self.map_data[self.py][self.px-1] == 1:
            return self.WEST
        return self.NORTH


    # 迷路のサイズ
    def _maze_config(self):
        self.Maze_Width = self.parent.parent.parent.start_frame.size_w.get()
        self.Maze_Height = self.parent.parent.parent.start_frame.size_h.get()
        self.tile_size_x = self.Frame_Width / (self.Maze_Width*2+1)
        self.tile_size_y = self.Frame_Height / (self.Maze_Height*2+1)


    # キーイベント
    def _event_key(self, e, direction: int):
        if direction == self.NORTH:
            if e.keysym == "Up":
                self.py -= 1
            elif e.keysym == "Down":
                direction = self.SOUTH
            elif e.keysym == "Left":
                direction = self.WEST
            elif e.keysym == "Right":
                direction = self.EAST

        elif direction == self.SOUTH:
            if e.keysym == "Up":
                self.py += 1
            elif e.keysym == "Down":
                direction = self.NORTH
            elif e.keysym == "Left":
                direction = self.EAST
            elif e.keysym == "Right":
                direction = self.WEST

        elif direction == self.EAST:
            if e.keysym == "Up":
                self.px += 1
            elif e.keysym == "Down":
                direction = self.WEST
            elif e.keysym == "Left":
                direction = self.NORTH
            elif e.keysym == "Right":
                direction = self.SOUTH

        elif direction == self.WEST:
            if e.keysym == "Up":
                self.px -= 1
            elif e.keysym == "Down":
                direction = self.EAST
            elif e.keysym == "Left":
                direction = self.SOUTH
            elif e.keysym == "Right":
                direction = self.NORTH
        return direction


    # キーバインド
    def _arrow_key_press(self, e):
        # 移動前に前回の値を覚えておく
        px_tmp = self.px
        py_tmp = self.py
        # プレイヤーが上下左右のどちらに動くか判定
        self.direction = self._event_key(e, self.direction)

        # 移動先がマップデータ外なら戻す
        if self.px < 0 or self.px >= len(self.map_data[0]):
            self.px = px_tmp
        if self.py < 0 or self.py >= len(self.map_data):
            self.py = py_tmp

        # 移動先が壁なら元の位置に戻す
        mv = self.map_data[self.py][self.px]
        if mv == 0:
            self.px = px_tmp
            self.py = py_tmp
            self.logger.debug('STAY', extra={'addinfo': "壁に激突"})
            return

        self.draw_map()
        self.parent.parent.Log_Frame.getLoc(self.px, self.py)
        self.logger.debug('MOVE', extra={'addinfo': "player={0},{1}, direction={2}".format(self.px, self.py, self.direction)})

        # ゴールにたどり着いたか？
        if mv == 3:
            self.parent.parent.parent.raise_frame(self.parent.parent.parent.goal_frame)
            self.parent.parent.Log_Frame.writeToLog('ゴール!')
            self.logger.debug('GOAL', extra={'addinfo': "ゴール"})


    # 迷路描画
    def _wall_row_first(self, map_viz):
        if map_viz[9] == 0:
            self.canvas.create_line(0,    80, 100, 130, 100, 470,   0, 520, fill=self.COLOR0)
        else:
            self.canvas.create_line(0,   130, 100, 130, 100, 470,   0, 470, fill=self.COLOR0)
            if map_viz[9] == 4:
                self.canvas.create_line(100, 470,   0, 520, fill=self.COLOR4)
        if map_viz[11] == 0:
            self.canvas.create_line(800,  80, 700, 130, 700, 470, 800, 520, fill=self.COLOR0)
        else:
            self.canvas.create_line(800, 130, 700, 130, 700, 470, 800, 470, fill=self.COLOR0)
            if map_viz[11] == 4:
                self.canvas.create_line(800, 470, 800, 520, fill=self.COLOR4)

    def _wall_row_second(self, map_viz):
        if map_viz[6] == 0:
            self.canvas.create_line(100, 130, 200, 180, 200, 420, 100, 470, fill=self.COLOR1)
        else:
            self.canvas.create_line(100, 180, 200, 180, 200, 420, 100, 420, fill=self.COLOR1)
            if map_viz[6] == 4:
                self.canvas.create_line(200, 420, 100, 470, fill=self.COLOR4)
        if map_viz[8] == 0:
            self.canvas.create_line(700, 130, 600, 180, 600, 420, 700, 470, fill=self.COLOR1)
        else:
            self.canvas.create_line(700, 180, 600, 180, 600, 420, 700, 420, fill=self.COLOR1)
            if map_viz[8] == 4:
                self.canvas.create_line(600, 420, 700, 470, fill=self.COLOR4)

    def _wall_row_third(self, map_viz):
        if map_viz[3] == 0:
            self.canvas.create_line(200, 180, 280, 220, 280, 380, 200, 420, fill=self.COLOR2)
        else:
            self.canvas.create_line(200, 220, 280, 220, 280, 380, 200, 380, fill=self.COLOR2)
            if map_viz[3] == 4:
                self.canvas.create_line(280, 380, 200, 420, fill=self.COLOR4)
        if map_viz[5] == 0:
            self.canvas.create_line(600, 180, 520, 220, 520, 380, 600, 420, fill=self.COLOR2)
        else:
            self.canvas.create_line(600, 220, 520, 220, 520, 380, 600, 380, fill=self.COLOR2)
            if map_viz[5] == 4:
                self.canvas.create_line(520, 380, 600, 420, fill=self.COLOR4)

    def _wall_row_fourth(self, map_viz):
        if map_viz[0] == 0:
            self.canvas.create_line(280, 220, 320, 240, 320, 360, 280, 380, fill=self.COLOR3)
        else:
            self.canvas.create_line(280, 240, 320, 240, 320, 360, 280, 360, fill=self.COLOR3)
            if map_viz[0] == 4:
                self.canvas.create_line(320, 360, 280, 380, fill=self.COLOR4)
        if map_viz[2] == 0:
            self.canvas.create_line(520, 220, 480, 240, 480, 360, 520, 380, fill=self.COLOR3)
        else:
            self.canvas.create_line(520, 240, 480, 240, 480, 360, 520, 360, fill=self.COLOR3)
            if map_viz[2] == 4:
                self.canvas.create_line(480, 360, 520, 380, fill=self.COLOR4)


    # debag
    def _create_window(self):
        win = Tk()
        win.title("Debug")

        self.canvas = Canvas(
            win,
            width=800,
            height=600,
            background='#020202'
        )
        self.canvas.pack()
        self.subcanvas.create_maze()

        # マップを描画する
        self.draw_maze()

        # キープレスイベントを追加。
        win.bind("<KeyPress>", self._arrow_key_press)

        win.mainloop()
