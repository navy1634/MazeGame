from __future__ import annotations

from tkinter import Frame, Tk
from typing import TYPE_CHECKING

from app.view.MazeCanvas import MazeCanvas

if TYPE_CHECKING:
    from app.controller.GameController import GameController


class MazeView(Frame):
    def __init__(self, parent: Tk | Frame, controller: GameController, canvas: MazeCanvas) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.px, self.py = 1, 1
        self.seed = 0
        self.canvas = canvas
