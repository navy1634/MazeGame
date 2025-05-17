# -*- coding: utf-8 -*-
from __future__ import annotations

from logging import getLogger
from tkinter import Canvas
from typing import TYPE_CHECKING

from app.config import config
from app.controller.MazeController import MazeController
from app.model.MazeMap import MazeMap

if TYPE_CHECKING:
    from app.controller.GameController import GameController
    from app.view.MazeView import MazeView


logger = getLogger("maze_root").getChild(__name__)


class Maze3Dto2DController(MazeController):
    canvas_width = 60
    canvas_height = 100
    bg_color = "#020202"
    tile_size = 40

    def __init__(self, controller: GameController, model: MazeMap, view: MazeView) -> None:
        self.controller = controller
        self.view = view
        self.model = model
        self.dim = 1
        self.px, self.py = 1, 1

    # 迷路生成
    def draw_maze(self) -> Canvas:
        # マップとプレイヤーを描画する
        self.view.canvas.draw_maze()
        self.view.canvas.draw_player(self.maze_view.player_image)
        return self.view.canvas

    def get_map_viz(self) -> list:
        map_viz = []
        for i in range(12):
            map_x = self.model.loc.px + config.POS_X[self.model.direction][i]
            map_y = self.model.loc.py + config.POS_Y[self.model.direction][i]

            if 0 < map_x < len(self.map_data[0]) and 0 < map_y < len(self.map_data):
                data = self.map_data[map_y][map_x]
            else:
                data = 0
            map_viz.append(data)
        return map_viz
