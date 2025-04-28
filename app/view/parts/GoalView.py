from __future__ import annotations

from logging import getLogger
from tkinter import Button, Frame, Label, Tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.controller.GameController import GameController

logger = getLogger("maze_root").getChild("Goal")


class GoalView(Frame):
    def __init__(self, parent: Tk | Frame, controller: GameController, conf) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.widget_width = 30
        self.widget_height = 3

        Label(self, text="GAME CLEAR !!!", font=("HGS行書体", 100), width=self.widget_width, height=self.widget_height).pack()
        frame = self.set_button()
        frame.pack()

    def set_button(self) -> Frame:
        frame = Frame(self)
        Button(frame, text="新しく開始", width=self.widget_width, height=self.widget_height, command=self.controller.new_game, font=("HGS行書体", 15)).grid(row=0, column=0)
        Button(frame, text="やり直す", width=self.widget_width, height=self.widget_height, command=self.controller.restart, font=("HGS行書体", 15)).grid(row=0, column=1)
        Button(frame, text="スタート画面へ", width=self.widget_width, height=self.widget_height, command=self.start_frame, font=("HGS行書体", 15)).grid(row=1, column=0)
        Button(frame, text="終了", width=self.widget_width, height=self.widget_height, command=self.controller.app.win_close, font=("HGS行書体", 15)).grid(row=1, column=1)
        return frame

    def start_frame(self) -> None:
        self.controller.raise_frame(self.controller.start_view)
