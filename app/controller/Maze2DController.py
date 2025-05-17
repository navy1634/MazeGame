from __future__ import annotations

from logging import getLogger
from tkinter import Canvas, Event
from typing import TYPE_CHECKING

from app.config import config
from app.controller.MazeController import MazeController
from app.model.MazeMap import MazeMap

if TYPE_CHECKING:
    from app.main import App

logger = getLogger("maze_root").getChild(__name__)


class Maze2DController(MazeController):
    def __init__(self, app: App, model: MazeMap, conf: dict) -> None:
        super().__init__(app, model, conf)
        self.controller = app.controller
        self.frame_width = conf["3D"]["FrameWidth"]
        self.frame_height = conf["3D"]["FrameHeight"]

    # 迷路生成
    def draw_maze(self) -> Canvas:
        # マップとプレイヤーを描画する
        self.view.canvas.draw_maze()
        self.view.canvas.draw_player(self.maze_view.player_image)
        return self.view.canvas

    # キーイベント
    def key_event_handler(self, e: Event) -> None:
        # 移動前に前回の値を覚えておく
        px_tmp, py_tmp = self.model.get_player_position()
        # プレイヤーが上下左右のどちらに動くか判定
        px_current, py_current = self._move_player(px=px_tmp, py=py_tmp, direction=e.keysym)
        # 入力通りに移動できるかを確認
        check = self.model.check_move(px=px_current, py=py_current)
        # 移動できる場合
        if check == 0:
            self.model.move_player(px=px_current, py=py_current)
            self.view.canvas.delete(self.view.canvas.player)
            self.maze_view.canvas.draw_player(self.maze_view.player_image)
            self.controller.maze_controller.getLoc(px=px_current, py=py_current)
            logger.debug("MOVE", extra={"addinfo": "player={0},{1}".format(px_current, py_current)})

        # 移動できない場合
        elif check == 1:
            logger.debug("STAY", extra={"addinfo": "壁に激突"})

        # ゴールした場合
        elif check == 2:
            self.controller.raise_frame(self.app.goal_frame)
            self.controller.writeToLog("ゴール!")
            logger.debug("GOAL", extra={"addinfo": "ゴール"})
