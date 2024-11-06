# -*- coding: utf-8 -*-

from logging import getLogger
from tkinter import Canvas, Frame, Tk

from config.conf import BASE_DIR, IMAGE_DIR
from maze.MazeMap import MazeCreate
from PIL import Image, ImageTk


class Maze2D(Frame):
    logger = getLogger("maze_root").getChild(__name__)

    def __init__(self, parent, conf) -> None:
        super().__init__(parent)
        self.parent = parent
        self.Frame_Width = conf["3D"]["Frame_Width"]
        self.Frame_Height = conf["3D"]["Frame_Height"]
        self.maze = MazeCreate()


    # 迷路生成
    def create_maze(self, flag=False) -> Canvas:
        self.canvas = Canvas(
            self.parent,
            width=self.Frame_Width,
            height=self.Frame_Height,
            background='#ffffff'
        )
        self.canvas.pack()

        # マップとプレイヤーを描画する
        if not flag:
            self.return_default()
        self.draw_maze()
        self.player_image = self.load_player(IMAGE_DIR+"/player.png")
        self._draw_player(self.player_image)
        return self.canvas


    def load_maze(self, seed):
        self._maze_config()
        self.load_map(Height=self.Maze_Height, Width=self.Maze_Width, seed=seed)


    # 初期設定
    def return_default(self):
        self.px = 1
        self.py = 1


    # マップ生成
    def load_map(self, Height, Width, seed=None):
        self.map_data = self.maze.create_maze(Height, Width, seed=seed)


    # 迷路解答
    def get_ans(self):
        self.map_data = self.maze.solve_maze()


    # 迷路解読
    def draw_maze(self):
        # 左上から右下へと描画
        # 迷路の行数
        self._maze_config()

        rows = len(self.map_data)
        # 迷路の列数
        cols = len(self.map_data[0])
        for y in range(rows):
            y1 = y * self.tile_size_y
            y2 = y1 + self.tile_size_y
            for x in range(cols):
                x1 = x * self.tile_size_x
                x2 = x1 + self.tile_size_x
                # 該当場所の値を得る
                p = self.map_data[y][x]
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
                    outline=color, width=2) # 枠線


    # プレイヤー生成
    def load_player(self, image_filename):
        """
        プレイヤーの画像を読み込む
        """
        img = Image.open(image_filename)
        img = img.resize((int(self.tile_size_x), int(self.tile_size_y)))
        return ImageTk.PhotoImage(img)


    # 迷路表示
    def draw_map(self):
        # マップとプレイヤーを描画する
        self.canvas.delete(self.player)
        self._draw_player(player_image=self.player_image)


    def draw_map_event(self):
        # マップとプレイヤーを描画する
        self.canvas.delete("all")
        self.draw_maze()
        self._draw_player(player_image=self.player_image)


    # プレイヤー描画
    def _draw_player(self, player_image):
        x = self.px * self.tile_size_x
        y = self.py * self.tile_size_y
        self.player = self.canvas.create_image(x, y, image=player_image, anchor="nw")


    # 迷路のサイズ
    def _maze_config(self):
        self.Maze_Width = self.parent.parent.parent.start_frame.size_w.get()
        self.Maze_Height = self.parent.parent.parent.start_frame.size_h.get()
        self.tile_size_x = self.Frame_Width / (self.Maze_Width*2+1)
        self.tile_size_y = self.Frame_Height / (self.Maze_Height*2+1)


    # キーイベント
    def _event_key(self, e):
        if e.keysym == "Up":
            self.py -= 1
        elif e.keysym == "Left":
            self.px -= 1
        elif e.keysym == "Right":
            self.px += 1
        elif e.keysym == "Down":
            self.py += 1


    # キーイベント
    def _arrow_key_press(self, e):
        # 移動前に前回の値を覚えておく
        px_tmp = self.px
        py_tmp = self.py
        # プレイヤーが上下左右のどちらに動くか判定
        self.direction = self._event_key(e)

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
        self.logger.debug('MOVE', extra={'addinfo': "player={0},{1}".format(self.px, self.py)})

        # ゴールにたどり着いたか？
        if mv == 3:
            self.parent.parent.parent.raise_frame(self.parent.parent.parent.goal_frame)
            self.parent.parent.Log_Frame.writeToLog('ゴール!')
            self.logger.debug('GOAL', extra={'addinfo': "ゴール"})
        return


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
        # マップとプレイヤーを描画する
        self.return_default()
        self._maze_config()
        self.draw_maze()
        self.player_image = self.load_player(BASE_DIR+"/resource/player.png")
        self._draw_player(self.player_image)

        # キープレスイベントを追加。
        win.bind("<KeyPress>", self._arrow_key_press)

        win.mainloop()
