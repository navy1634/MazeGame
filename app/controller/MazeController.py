# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import abstractmethod
from datetime import datetime, timezone
from logging import getLogger
from tkinter import Frame
from typing import TYPE_CHECKING

from app.config import config
from app.model.MazeMap import MazeMap

if TYPE_CHECKING:
    from app.main import App
    from app.view.LogView import LogView
    from app.view.MazeCanvas import MazeCanvas
    from app.view.MazeView import MazeView
    from app.view.OperationView import OperationView
    from app.view.StartView import StartView

logger = getLogger("maze_root").getChild(__name__)


class MazeController:
    def __init__(self, app: App, model: MazeMap, conf) -> None:
        self.app = app
        self.model = model
        self.player_image = self.app.maze_view.canvas.load_player(config.IMAGE_DIR + "/player.png")

    # OK
    def set_model(self, model: MazeMap) -> None:
        """2D <-> 3D 切替時にマップを共有する

        Args:
            model (MazeMap): 迷路データ
        """
        self.model = model

    def set_maze_view(self, view: MazeView) -> None:
        self.view = view
        self.maze_view = view

    def getLoc(self, px: int, py: int) -> None:
        """移動時のログを吐く関数

        Args:
            px (int): 現在地のx座標
            py (int): 現在地のy座標
        """
        message = f"現在地 x座標: {px}, y座標: {py}"
        self.app.log_view.loc_widget["state"] = "normal"
        self.app.log_view.loc_widget.delete("1.0", "end")
        self.app.log_view.loc_widget.insert("end", message)
        self.app.log_view.loc_widget["state"] = "disabled"

    def _move_player(self, px: int, py: int, direction: str) -> tuple[int, int]:
        if direction == "Up":
            py -= 1
        elif direction == "Left":
            px -= 1
        elif direction == "Right":
            px += 1
        elif direction == "Down":
            py += 1
        return px, py

    @abstractmethod
    def key_event_handler(self, e) -> None:
        """矢印キーイベント"""
        raise NotImplementedError("key_event_handler is not implemented")
        # # プレイヤーが上下左右のどちらに動くか判定
        # px_tmp, py_tmp = self.model.get_player_position()
        # px_current, py_current = self._move_player(e.keysym, px_tmp, py_tmp)

        # # プレイヤーの移動を判定
        # check = self.model.check_move(px_current, py_current)

        # # 移動できる場合
        # if check == 0:
        #     self.model.move_player(px_current, py_current)
        #     self.maze_view.canvas.draw_player(self.player_image)
        #     # self.parent.parent.Log_Frame.getLoc(px_current, px_current)
        #     logger.debug("MOVE", extra={"addinfo": "player={0},{1}".format(px_current, py_current)})

        # # 移動できない場合
        # elif check == 1:
        #     logger.debug("STAY", extra={"addinfo": "壁に激突"})

        # # ゴールした場合
        # elif check == 2:
        #     # se3f.parent.parent.parent.app.controller.raise_frame(self.parent.parent.parent.goal_frame)
        #     # self.parent.parent.Log_Frame.app.controller.writeToLog("ゴール!")
        #     logger.debug("GOAL", extra={"addinfo": "ゴール"})

    # 吟味
    def set_maze(self) -> None:
        self.load_maze(seed=self.model.seed)  # 迷路の読み込み
        self.view.canvas.calc_canvas_width()
        self.view.canvas.maze_config()
        self.create_maze()  # 迷路描画
        # self.app.controller.unset_key_bind(self.app)
        # self.bind_id_dict = self.app.controller.set_key_bind(self.app, self)

    def load_maze(self, seed: int | None = None) -> None:
        height, width = self.app.start_view.get_size()
        self.map_data = self.model.create_maze(height, width, seed=seed)

    def changePage(self, dim: int) -> None:
        """
        画面遷移用の関数
        """
        # 迷路作成
        self.set_maze()
        self.maze_view.canvas.grid(row=1, column=0, rowspan=2)

        # ログ処理
        self.app.controller.writeToLog("迷路開始")
        self.getLoc(self.model.px, self.model.py)
        logger.debug("GENERATE", extra={"addinfo": f"迷路生成 ({dim + 2}D)"})

    # ボタン用の関数
    def reset(self) -> None:
        """迷路のリセットを行うボタン用の関数"""
        self.maze_reset()
        self.app.controller.writeToLog("リセット")

    def maze_reset(self):
        """迷路のリセットを行う関数"""
        logger.debug("RESET", extra={"addinfo": "位置リセット"})
        self.model.set_default_position()
        self.maze_view.canvas.draw_maze(0)
        self.getLoc(1, 1)

    def restart(self) -> None:
        """迷路のリスタートを行うボタン用の関数"""
        logger.debug("RESTART", extra={"addinfo": "迷路再生成"})
        h, w = self.app.start_view.get_size()
        self.model.create_maze(h, w)
        self.model.set_default_position()
        self.maze_view.canvas.draw_maze(0)
        self.getLoc(1, 1)
        self.app.controller.writeToLog("リスタート")
        self.app.controller.raise_frame(self.maze_view)

    def solve(self) -> None:
        """解答生成を行う関数"""
        logger.debug("SOLVE", extra={"addinfo": "迷路解答表示"})
        self.map_data = self.model.solve_maze()
        self.maze_view.canvas.draw_maze(0)
        self.app.controller.writeToLog("解答表示")

    # 迷路生成
    def create_maze(self):
        # マップとプレイヤーを描画する
        self.maze_view.canvas.draw_maze(0)
        self.maze_view.canvas.draw_player(self.player_image)
        return self.maze_view.canvas

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

    # 迷路表示
    def draw_map(self) -> None:
        # マップとプレイヤーを描画する
        self.maze_view.canvas.draw_maze(0)
        self.maze_view.canvas.draw_player(player_image=self.player_image)
