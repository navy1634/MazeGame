from __future__ import annotations

import json
from datetime import datetime, timezone
from logging import getLogger
from tkinter import Frame, Tk
from typing import TYPE_CHECKING

from app.config import config
from app.controller.Maze2DController import Maze2DController
from app.controller.Maze3DController import Maze3DController
from app.model.MazeMap import MazeMap
from app.view.LogView import LogView
from app.view.MazeView import MazeView
from app.view.OperationView import OperationView
from app.view.StartView import StartView

if TYPE_CHECKING:
    from app.controller.MazeController import MazeController
    from app.main import App

logger = getLogger("maze_root").getChild(__name__)


class GameController:
    """
    ゲーム全体のコントローラ
    """

    def __init__(self, app: App, model: MazeMap) -> None:
        logger.debug("START", extra={"addinfo": "ウィンドウ生成"})
        self.app = app
        self.model = model
        self.conf = self.get_setting()

    def set_maze_controller(self) -> None:
        """コントローラの作成"""
        self.maze_2d_controller = Maze2DController(self.app, self.model)
        self.maze_3d_controller = Maze3DController(self.app, self.model)
        self.set_key_bind(self.app, self.maze_2d_controller)
        self._set_controller(0)

    def set_view(self, start_view: StartView, maze_view: MazeView, operation_view: OperationView) -> None:
        """それぞれのviewをセットする関数

        Args:
            start_view (StartView): スタート画面
            maze_view (MazeView): 迷路画面
            main_view (Frame): ？
            operation_view (OperationView): 操作説明画面
            log_view (LogView): ログ
        """
        self.start_view = start_view
        self.maze_view = maze_view
        self.main_view = maze_view.maze_view
        self.operation_view = operation_view
        self.log_view = maze_view.log_view
        self.maze_2d_controller.set_maze_view(self.maze_view)
        self.maze_3d_controller.set_maze_view(self.maze_view)

    def set_maze_frame(self) -> None:
        """
        迷路生成し、画面を表示
        """
        self.maze_controller.changePage()
        self.raise_frame(self.main_view)

    # 2D, 3D の切替
    def change_dimension(self, dim: int) -> None:
        """2D, 3D の切替を行う関数

        Args:
            dim (int): 設定するディメンション
        """
        logger.debug("SET", extra={"addinfo": f"{dim + 2}D"})
        # 各ラジオボタンと変数を共有
        self.start_view.set_radio_value(dim)
        self.maze_controller.set_dimension(dim)
        # 切替
        self.maze_controller.changePage()
        # コントローラーの切替
        self._set_controller(dim)
        # キーバインドの解除
        self.unset_key_bind(self.app)
        # キーバインドの登録
        self.set_key_bind(self.app, self.maze_controller)

    def _set_controller(self, dim: int) -> None:
        """2D, 3D のコントローラーの切替を行う関数

        Args:
            dim (int): 設定するディメンション
        """
        if dim == 0:
            self.maze_controller = self.maze_2d_controller
        else:
            self.maze_controller = self.maze_3d_controller
        self.maze_controller.set_dimension(dim)

    # key バインド
    def set_key_bind(self, target: Tk, maze: MazeController) -> None:
        """迷路操作のためのキーイベントをバインドする関数

        Args:
            target (Tk): キーバインドを設定するウィンドウ
            maze (MazeController): 設定するハンドラー
        """
        target.bind("<KeyPress-Left>", maze.key_event_handler)
        target.bind("<KeyPress-Up>", maze.key_event_handler, "+")
        target.bind("<KeyPress-Right>", maze.key_event_handler, "+")
        target.bind("<KeyPress-Down>", maze.key_event_handler, "+")

    def unset_key_bind(self, target: Tk) -> None:
        """迷路操作のためのキーイベントをバインド解除する関数
        Args:
            target (Tk): キーバインドを解除するウィンドウ
        """
        target.unbind("<KeyPress-Left>")
        target.unbind("<KeyPress-Up>")
        target.unbind("<KeyPress-Right>")
        target.unbind("<KeyPress-Down>")

    # 設定ファイル
    def get_setting(self) -> dict:
        """
        設定ファイルの読み込み
        """
        with open(config.SRC_DIR + "/config/setting.json", "r", encoding="utf-8") as f:
            conf = json.load(f)
            f.close()
        return conf

    def save_setting(self) -> None:
        """
        設定ファイルの保存
        """
        self.conf["dim"] = self.start_view.get_radio_value()
        with open(config.SRC_DIR + "/config/setting.json", "w", encoding="utf-8") as f:
            json.dump(self.conf, f)
            f.close()

    # 画面遷移
    def raise_frame(self, frame: Frame) -> None:
        """画面遷移用の関数

        Args:
            frame (Frame): 遷移先のフレーム
        """
        logger.debug("FRAME", extra={"addinfo": f"{type(frame)}に遷移"})
        frame.tkraise()

    def writeToLog(self, msg: str) -> None:
        """ログ管理の関数

        Args:
            msg (str): メッセージ
        """
        message = f"{datetime.strftime(datetime.now(timezone.utc), '%H:%M:%S')}  {msg}"
        self.log_view.log_widget["state"] = "normal"
        if self.log_view.log_widget.index("end-1c") != "1.0":
            self.log_view.log_widget.insert("end", "\n")
        self.log_view.log_widget.insert("end", message)
        self.log_view.log_widget.see("end")
        self.log_view.log_widget["state"] = "disabled"
