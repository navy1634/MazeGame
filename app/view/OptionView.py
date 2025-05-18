from __future__ import annotations

from logging import getLogger
from tkinter import Button, Frame, Tk
from typing import TYPE_CHECKING

from app.config import config

if TYPE_CHECKING:
    from app.controller.GameController import GameController


class OptionView(Frame):
    logger = getLogger("maze_root").getChild(__name__)

    def __init__(self, parent: Tk | Frame, controller: GameController) -> None:
        super().__init__(parent)

        Button(self, text="reset", command=controller.maze_controller.reset, width=config.WIDGET_WIDTH, height=config.WIDGET_HEIGHT).pack(anchor="center")
        Button(self, text="restart", command=controller.maze_controller.restart, width=config.WIDGET_WIDTH, height=config.WIDGET_HEIGHT).pack(anchor="center")
        Button(self, text="solve", command=controller.maze_controller.solve, width=config.WIDGET_WIDTH, height=config.WIDGET_HEIGHT).pack(anchor="center")
        Button(self, text="close", command=controller.app.win_close, width=config.WIDGET_WIDTH, height=config.WIDGET_HEIGHT).pack(anchor="center")
