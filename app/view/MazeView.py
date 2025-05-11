from __future__ import annotations

from tkinter import Frame, Label, Tk
from typing import TYPE_CHECKING

from app.view.LogView import LogView
from app.view.MazeCanvas import MazeCanvas
from app.view.OptionView import OptionView

if TYPE_CHECKING:
    from app.controller.GameController import GameController
    from app.model.MazeMap import MazeMap


class MazeView(Frame):
    def __init__(self, parent: Tk | Frame, controller: GameController, model: MazeMap) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.model = model
        self.px, self.py = 1, 1
        self.seed = 0

        # 迷路画面の生成
        maze_index = Label(self, text="↑ → ↓ ← キーで操作、Ctrl+Cで操作方法の表示、ゴールに辿り着くとクリア")
        self.option_view = OptionView(self, self.controller, self.controller.conf)
        self.log_view = LogView(self, self.controller)
        self.maze_view = Frame(self)
        self.canvas = MazeCanvas(self.maze_view, self.controller, self.model)

        # 迷路画面の配置設定
        maze_index.grid(row=0, column=0)
        self.maze_view.grid(row=1, column=0, rowspan=2, sticky="nsew")
        self.option_view.grid(row=1, column=1, sticky="nsew")
        self.log_view.grid(row=2, column=1)

        self.canvas.pack()
