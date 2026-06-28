from tkinter import Frame, Label, Tk

from app.controller.game_controller import GameController
from app.view.log_view import LogView
from app.view.maze_canvas import MazeCanvas
from app.view.option_view import OptionView


class MazeView(Frame):
    def __init__(self, parent: Tk | Frame, controller: GameController) -> None:
        super().__init__(parent)

        # 迷路画面の生成
        maze_index = Label(self, text="↑ → ↓ ← キーで操作、Ctrl+Cで操作方法の表示、ゴールに辿り着くとクリア")
        self.option_view = OptionView(self, controller)
        self.log_view = LogView(self, controller)
        self.maze_view = Frame(self)
        self.canvas = MazeCanvas(self.maze_view, controller)

        # 迷路画面の配置設定
        maze_index.grid(row=0, column=0)
        self.maze_view.grid(row=1, column=0, rowspan=2, sticky="nsew")
        self.option_view.grid(row=1, column=1, sticky="nsew")
        self.log_view.grid(row=2, column=1)

        self.canvas.pack()
