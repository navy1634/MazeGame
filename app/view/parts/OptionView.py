from __future__ import annotations

from logging import getLogger
from tkinter import Button, Frame, Tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.controller.GameController import GameController


class OptionView(Frame):
    logger = getLogger("maze_root").getChild(__name__)

    def __init__(self, parent: Tk | Frame, controller: GameController, conf) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.Widget_Width = conf["widget"]["Width"]
        self.Widget_Height = conf["widget"]["Height"]

        Button(self, text="reset", command=self.controller.maze_reset, width=self.Widget_Width, height=self.Widget_Height).pack(anchor="center")
        Button(self, text="restart", command=self.controller.maze_restart, width=self.Widget_Width, height=self.Widget_Height).pack(anchor="center")
        Button(self, text="solve", command=self.controller.maze_solve, width=self.Widget_Width, height=self.Widget_Height).pack(anchor="center")
        Button(self, text="close", command=self.controller.app.win_close, width=self.Widget_Width, height=self.Widget_Height).pack(anchor="center")
