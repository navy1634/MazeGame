from __future__ import annotations

from tkinter import Button, Frame, Label, Tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.controller.GameController import GameController


class GoalView(Frame):
    def __init__(self, parent: Tk | Frame, controller: GameController) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.widget_width = 30
        self.widget_height = 3

        Label(self, text="GAME CLEAR !!!", font=("HGS行書体", 100), width=self.widget_width, height=self.widget_height).pack()
        frame = Frame(self)
        Button(frame, text="新しく開始", width=self.widget_width, height=self.widget_height, command=self.raise_maze_restart, font=("HGS行書体", 15)).grid(row=0, column=0)
        Button(frame, text="やり直す", width=self.widget_width, height=self.widget_height, command=self.raise_maze_reset, font=("HGS行書体", 15)).grid(row=0, column=1)
        Button(frame, text="スタート画面へ", width=self.widget_width, height=self.widget_height, command=self.raise_start_frame, font=("HGS行書体", 15)).grid(row=1, column=0)
        Button(frame, text="終了", width=self.widget_width, height=self.widget_height, command=self.controller.app.win_close, font=("HGS行書体", 15)).grid(row=1, column=1)
        frame.pack()

    def raise_start_frame(self) -> None:
        """スタート画面に戻る"""
        self.controller.raise_frame(self.controller.start_view)

    def raise_maze_reset(self) -> None:
        """迷路をリセットして迷路画面を表示する"""
        self.controller.maze_controller.reset()
        self.controller.raise_frame(self.controller.maze_view)

    def raise_maze_restart(self) -> None:
        """迷路を新しく開始して迷路画面を表示する"""
        self.controller.maze_controller.restart()
        self.controller.raise_frame(self.controller.maze_view)
