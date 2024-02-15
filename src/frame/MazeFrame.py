# -*- coding: utf-8 -*-

import random
from tkinter import Frame
from Maze.Maze2D import Maze2D
from Maze.Maze3D import Maze3D
from logging import getLogger


class MazeFrame(Frame):
    logger = getLogger("maze_root").getChild("Maze")
    def __init__(self, parent, conf):
        super().__init__(parent)
        self.parent = parent
        self.conf = conf
        self.px, self.py = 1, 1
        self.seed = None
        self.maze_2d = Maze2D(self, conf=self.conf)
        self.maze_3d = Maze3D(self, conf=self.conf)
        self.bind_id_L = self.parent.parent.bind("<KeyPress-Left>", self.maze_2d._arrow_key_press)
        self.bind_id_U = self.parent.parent.bind("<KeyPress-Up>", self.maze_2d._arrow_key_press, "+")
        self.bind_id_R = self.parent.parent.bind("<KeyPress-Right>", self.maze_2d._arrow_key_press, "+")
        self.bind_id_D = self.parent.parent.bind("<KeyPress-Down>", self.maze_2d._arrow_key_press, "+")

    def set_maze(self, dim, seed=None, flag=False):
        if dim == 0:
            self.maze = self.maze_2d
        elif dim == 1:
            self.maze = self.maze_3d
        else:
            self.logger.error("invalid Value")

        self.maze.px = self.px
        self.maze.py = self.py

        self.maze.load_maze(seed=seed) # 迷路の読み込み
        self.maze.create_maze(flag=flag) # 迷路描画
        self.parent.parent.unbind("<KeyPress-Left>", self.bind_id_L)
        self.parent.parent.unbind("<KeyPress-Up>", self.bind_id_U)
        self.parent.parent.unbind("<KeyPress-Right>", self.bind_id_R)
        self.parent.parent.unbind("<KeyPress-Down>", self.bind_id_D)
        self.bind_id_L = self.parent.parent.bind("<KeyPress-Left>", self.maze._arrow_key_press)
        self.bind_id_U = self.parent.parent.bind("<KeyPress-Up>", self.maze._arrow_key_press, "+")
        self.bind_id_R = self.parent.parent.bind("<KeyPress-Right>", self.maze._arrow_key_press, "+")
        self.bind_id_D = self.parent.parent.bind("<KeyPress-Down>", self.maze._arrow_key_press, "+")


    def changePage(self, dim, flag_seed=False):
        '''
        画面遷移用の関数
        '''
        self.seed_org = self.seed
        if flag_seed: # 2D, 3D で位置を共有
            self.px = self.maze.px
            self.py = self.maze.py
            self.seed = self.seed_org # 乱数を共有
        else:
            self.px, self.py = 1, 1
            self.seed = random.randint(0, 256) # 乱数生成

        self.destroy()
        super().__init__(self.parent)
        self.set_maze(dim, seed=self.seed, flag=flag_seed)
        self.grid(row=1, column=0, rowspan=2)

        # ログ処理
        self.parent.Log_Frame.writeToLog(f'迷路開始')
        self.parent.Log_Frame.getLoc(self.px, self.py)
        self.logger.debug("GENERATE", extra={"addinfo": f"迷路生成 ({dim+2}D)"})


