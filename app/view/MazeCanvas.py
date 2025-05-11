from __future__ import annotations

from tkinter import Canvas, Frame, Tk
from typing import TYPE_CHECKING

from PIL import Image, ImageTk

from app.config.type import Maze3DColor
from app.model.MazeMap import MazeMap

if TYPE_CHECKING:
    from app.controller.GameController import GameController


class MazeCanvas(Canvas):
    def __init__(self, parent: Tk | Frame, controller: GameController, model: MazeMap) -> None:
        super().__init__(parent)
        self.controller = controller
        self.model = model
        self.cell_size = 20

    def calc_canvas_width(self):
        self.width = len(self.model.map_data[0]) * self.cell_size
        self.height = len(self.model.map_data) * self.cell_size

    # プレイヤー描画
    def draw_player(self, player_image: ImageTk.PhotoImage) -> None:
        self.create_image(800 - self.tile_size_x * 2 + 10, 600 - self.tile_size_y * 2 + 10, image=player_image, anchor="nw")

    def maze_config(self):
        self.maze_width, self.maze_height = self.model.get_maze_size()
        self.tile_size_x = self.width / (self.maze_width * 2 + 1)
        self.tile_size_y = self.height / (self.maze_height * 2 + 1)

    # プレイヤー生成
    def load_player(self, image_file_name: str) -> ImageTk.PhotoImage:
        """
        プレイヤーの画像を読み込む
        """
        img = Image.open(image_file_name)
        img_tk = ImageTk.PhotoImage(img)
        return img_tk

    # 迷路表示
    def draw_map(self) -> None:
        # マップとプレイヤーを描画する
        self.delete("all")
        self.draw_maze(0)

    def draw_map_event(self) -> None:
        # マップとプレイヤーを描画する
        self.delete("all")
        self.direction = self.model.set_direction(self.model._default_direction())
        self.draw_maze(0)

    # 迷路解読
    def draw_maze(self, dim):
        if dim == 0:
            self.draw_maze_2d()
        else:
            self.draw_maze_3d()
            self.draw_maze_3dto2d()

    # 2D
    def draw_maze_2d(self) -> None:
        # 左上から右下へと描画
        # 迷路の行数
        self.maze_config()

        rows = len(self.model.map_data)
        # 迷路の列数
        cols = len(self.model.map_data[0])
        for y in range(rows):
            y1 = y * self.tile_size_y
            y2 = y1 + self.tile_size_y
            for x in range(cols):
                x1 = x * self.tile_size_x
                x2 = x1 + self.tile_size_x
                # 該当場所の値を得る
                p = self.model.map_data[y][x]
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
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, width=2)

    # 3D用2D
    def draw_maze_3dto2d(self) -> None:
        # 左上から右下へと描画
        # 迷路の行数
        #  |0|1|2|
        #  |3|4|5|
        #  |6|7|8|
        #  |9|A|B|
        map_viz = self.model.get_map_viz()

        for y in range(4):
            y1 = y * self.tile_size_y + (600 - self.tile_size_y * 5)
            y2 = y1 + self.tile_size_y
            for x in range(3):
                x1 = x * self.tile_size_x + 800 - self.tile_size_x * 3
                x2 = x1 + self.tile_size_x
                # 該当場所の値を得る
                p = map_viz[y * 3 + x]
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
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)

    # 3D
    def draw_maze_3d(self) -> None:
        map_viz = self.model.get_map_viz()
        self._wall_row_first(map_viz)

        self.create_line(100, 470, 700, 470, fill=Maze3DColor.LAYER1)

        if map_viz[7] == 0:
            self.create_line(100, 130, 700, 130, fill=Maze3DColor.LAYER1)
        else:
            self._wall_row_second(map_viz)
            if map_viz[7] == 4:
                self.create_line(100, 470, 700, 470, fill=Maze3DColor.LAYER4)
            self.create_line(200, 420, 600, 420, fill=Maze3DColor.LAYER2)

            if map_viz[4] == 0:
                self.create_line(200, 180, 600, 180, fill=Maze3DColor.LAYER2)
            else:
                self._wall_row_third(map_viz)
                if map_viz[4] == 4:
                    self.create_line(200, 420, 600, 420, fill=Maze3DColor.LAYER4)
                self.create_line(280, 380, 520, 380, fill=Maze3DColor.LAYER3)

                if map_viz[1] == 0:
                    self.create_line(280, 220, 520, 220, fill=Maze3DColor.LAYER3)
                else:
                    self._wall_row_fourth(map_viz)
                    if map_viz[1] == 4:
                        self.create_line(280, 380, 520, 380, fill=Maze3DColor.LAYER4)
                    self.create_line(320, 360, 480, 360, fill=Maze3DColor.LAYER3)

    def _wall_row_first(self, map_viz: list[int]) -> None:
        if map_viz[9] == 0:
            self.create_line(0, 80, 100, 130, 100, 470, 0, 520, fill=Maze3DColor.LAYER0)
        else:
            self.create_line(0, 130, 100, 130, 100, 470, 0, 470, fill=Maze3DColor.LAYER0)
            if map_viz[9] == 4:
                self.create_line(100, 470, 0, 520, fill=Maze3DColor.LAYER4)
        if map_viz[11] == 0:
            self.create_line(800, 80, 700, 130, 700, 470, 800, 520, fill=Maze3DColor.LAYER0)
        else:
            self.create_line(800, 130, 700, 130, 700, 470, 800, 470, fill=Maze3DColor.LAYER0)
            if map_viz[11] == 4:
                self.create_line(800, 470, 800, 520, fill=Maze3DColor.LAYER4)

    def _wall_row_second(self, map_viz: list[int]) -> None:
        if map_viz[6] == 0:
            self.create_line(100, 130, 200, 180, 200, 420, 100, 470, fill=Maze3DColor.LAYER1)
        else:
            self.create_line(100, 180, 200, 180, 200, 420, 100, 420, fill=Maze3DColor.LAYER1)
            if map_viz[6] == 4:
                self.create_line(200, 420, 100, 470, fill=Maze3DColor.LAYER4)
        if map_viz[8] == 0:
            self.create_line(700, 130, 600, 180, 600, 420, 700, 470, fill=Maze3DColor.LAYER1)
        else:
            self.create_line(700, 180, 600, 180, 600, 420, 700, 420, fill=Maze3DColor.LAYER1)
            if map_viz[8] == 4:
                self.create_line(600, 420, 700, 470, fill=Maze3DColor.LAYER4)

    def _wall_row_third(self, map_viz: list[int]) -> None:
        if map_viz[3] == 0:
            self.create_line(200, 180, 280, 220, 280, 380, 200, 420, fill=Maze3DColor.LAYER2)
        else:
            self.create_line(200, 220, 280, 220, 280, 380, 200, 380, fill=Maze3DColor.LAYER2)
            if map_viz[3] == 4:
                self.create_line(280, 380, 200, 420, fill=Maze3DColor.LAYER4)
        if map_viz[5] == 0:
            self.create_line(600, 180, 520, 220, 520, 380, 600, 420, fill=Maze3DColor.LAYER2)
        else:
            self.create_line(600, 220, 520, 220, 520, 380, 600, 380, fill=Maze3DColor.LAYER2)
            if map_viz[5] == 4:
                self.create_line(520, 380, 600, 420, fill=Maze3DColor.LAYER4)

    def _wall_row_fourth(self, map_viz: list[int]) -> None:
        if map_viz[0] == 0:
            self.create_line(280, 220, 320, 240, 320, 360, 280, 380, fill=Maze3DColor.LAYER3)
        else:
            self.create_line(280, 240, 320, 240, 320, 360, 280, 360, fill=Maze3DColor.LAYER3)
            if map_viz[0] == 4:
                self.create_line(320, 360, 280, 380, fill=Maze3DColor.LAYER4)
        if map_viz[2] == 0:
            self.create_line(520, 220, 480, 240, 480, 360, 520, 380, fill=Maze3DColor.LAYER3)
        else:
            self.create_line(520, 240, 480, 240, 480, 360, 520, 360, fill=Maze3DColor.LAYER3)
            if map_viz[2] == 4:
                self.create_line(480, 360, 520, 380, fill=Maze3DColor.LAYER4)
