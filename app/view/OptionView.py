from __future__ import annotations

from logging import getLogger
from tkinter import Button, Frame, Tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.controller.GameController import GameController


class OptionView(Frame):
    logger = getLogger("maze_root").getChild(__name__)

    def __init__(self, parent: Tk | Frame, controller: GameController, conf: dict) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.widget_width = conf["widget"]["Width"]
        self.widget_height = conf["widget"]["Height"]

        Button(self, text="reset", command=self.controller.maze_controller.reset, width=self.widget_width, height=self.widget_height).pack(anchor="center")
        Button(self, text="restart", command=self.controller.maze_controller.restart, width=self.widget_width, height=self.widget_height).pack(anchor="center")
        Button(self, text="solve", command=self.controller.maze_controller.solve, width=self.widget_width, height=self.widget_height).pack(anchor="center")
        Button(self, text="close", command=self.controller.app.win_close, width=self.widget_width, height=self.widget_height).pack(anchor="center")
