from __future__ import annotations

import random
from logging import getLogger
from tkinter import Frame, Tk
from typing import TYPE_CHECKING

from app.controller.Maze2DController import Maze2DController
from app.controller.Maze3DController import Maze3DController
from app.view.parts.MazeCanvas import MazeCanvas

if TYPE_CHECKING:
    from app.controller.GameController import GameController

logger = getLogger("maze_root").getChild("Maze")


class MazeView(Frame):
    def __init__(self, parent: Tk | Frame, controller: GameController, canvas: MazeCanvas) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.px, self.py = 1, 1
        self.seed = 0
        self.canvas = canvas
