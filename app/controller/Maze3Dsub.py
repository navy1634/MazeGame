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

    def __init__(self, controller: GameController, model: MazeMap, view: MazeView, conf: dict) -> None:
        self.controller = controller
        self.view = view
        self.model = model
        self.dim = 1
        self.px, self.py = 1, 1
        self.frame_width = conf["3D"]["frame_width"]
        self.frame_height = conf["3D"]["frame_height"]

    # 迷路生成
    def draw_maze(self) -> Canvas:
        # マップとプレイヤーを描画する
        self.view.canvas.draw_maze(self.dim)
        self.player_image = self.view.canvas.load_player(config.IMAGE_DIR + "/player.png")
        self.view.canvas.draw_player(self.player_image)
        return self.view.canvas

    def get_map_viz(self) -> list:
        map_viz = []
        for i in range(12):
            map_x = self.model.px + config.POS_X[self.model.direction][i]
            map_y = self.model.py + config.POS_Y[self.model.direction][i]

            if 0 < map_x < len(self.model.map_data[0]) and 0 < map_y < len(self.model.map_data):
                data = self.model.map_data[map_y][map_x]
            else:
                data = 0
            map_viz.append(data)
        return map_viz
