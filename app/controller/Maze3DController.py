from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from app.config.type import DIRECTION
from app.controller.MazeController import MazeController
from app.model.MazeMap import MazeMap

if TYPE_CHECKING:
    from app.main import App


logger = getLogger("maze_root").getChild(__name__)


class Maze3DController(MazeController):
    def __init__(self, app: App, model: MazeMap) -> None:
        super().__init__(app, model)
        self.controller = app.controller

    def get_maze_mini_map(self) -> list[int]:
        """迷路のミニマップを取得する

        Returns:
            list[list[int]]: 迷路のミニマップ
        """
        return self.model.get_map_viz()

    # キーイベント
    def _move_player(self, px: int, py: int, direction: DIRECTION) -> tuple[int, int]:
        """指定された方向にプレイヤーを移動させる

        Args:
            px (int): x座標
            py (int): y座標
            direction (str): 向いている方角

        Returns:
            tuple[int, int]: 移動後のプレイヤーの座標
        """

        if direction == DIRECTION.NORTH:
            py -= 1
        elif direction == DIRECTION.SOUTH:
            py += 1
        elif direction == DIRECTION.EAST:
            px += 1
        elif direction == DIRECTION.WEST:
            px -= 1

        return px, py

    def _get_new_direction(self, current_direction: DIRECTION, keysym: str) -> DIRECTION:
        """キー入力に基づいて新しい方向を向く

        Args:
            current_direction (str): 今の向き
            keysym (str): 押されたキー

        Returns:
            int: 新しい方向
        """
        turn_logic = {
            DIRECTION.NORTH: {"Down": DIRECTION.SOUTH, "Left": DIRECTION.WEST, "Right": DIRECTION.EAST},
            DIRECTION.SOUTH: {"Down": DIRECTION.NORTH, "Left": DIRECTION.EAST, "Right": DIRECTION.WEST},
            DIRECTION.EAST: {"Down": DIRECTION.WEST, "Left": DIRECTION.NORTH, "Right": DIRECTION.SOUTH},
            DIRECTION.WEST: {"Down": DIRECTION.EAST, "Left": DIRECTION.SOUTH, "Right": DIRECTION.NORTH},
        }

        # 現在の方向に対応する転換ロジックを取得
        direction_turns = turn_logic.get(current_direction, {})
        # 押されたキーに対応する新しい方向を返す (対応がなければ現在の方向を維持)
        return direction_turns.get(keysym, current_direction)

    def key_event_handler(self, e) -> None:
        """
        キーイベント (e) と現在の方向 (current_direction) を受け取り、
        プレイヤーの移動または方向転換を行い、新しい方向を返す。
        """
        key_direction = e.keysym
        current_direction = self.model.get_direction()

        # 進行方向に移動する
        if key_direction == "Up":
            # 現在地を取得
            px_tmp, py_tmp = self.model.get_player_position()
            px_current, py_current = self._move_player(px_tmp, py_tmp, current_direction)

            # プレイヤーの移動を判定
            check = self.model.check_move(px_current, py_current)
            # 移動できる場合
            if check == 0:
                self.model.move_player(px_current, py_current)
                self.view.canvas.delete("all")
                self.view.canvas.draw_maze_3d()
                self.view.canvas.draw_maze_3dto2d()
                self.maze_view.canvas.draw_player_3d2d()
                self.controller.maze_controller.getLoc(px_current, py_current)
                logger.debug("MOVE", extra={"addinfo": f"player={px_current},{py_current}"})

            # 移動できない場合
            elif check == 1:
                logger.debug("STAY", extra={"addinfo": "壁に激突"})

            # ゴールした場合
            elif check == 2:
                self.controller.raise_frame(self.app.goal_frame)
                self.controller.writeToLog("ゴール!")
                logger.debug("GOAL", extra={"addinfo": "ゴール"})

        # 方向転換のみを行う
        elif key_direction in ["Down", "Left", "Right"]:
            new_direction = self._get_new_direction(current_direction, key_direction)
            self.model.set_direction(new_direction)
            self.view.canvas.delete("all")
            self.view.canvas.draw_maze_3d()
            self.view.canvas.draw_maze_3dto2d()
            self.maze_view.canvas.draw_player_3d2d()
