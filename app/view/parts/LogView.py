from __future__ import annotations

from logging import getLogger
from tkinter import Frame, Text, Tk, ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.controller.GameController import GameController


logger = getLogger("maze_root").getChild("Goal")


class LogView(Frame):
    logger = getLogger("maze_root").getChild("Log")

    def __init__(self, parent: Tk | Frame, controller: GameController) -> None:
        super().__init__(parent)
        self.controller = controller

        # なにかに使っている
        self.loc_widget = Text(self, state="disabled", width=28, height=1)
        self.loc_widget.grid(row=0, column=0, columnspan=2)

        # ログフレームの生成
        self.logger.debug("SET", extra={"addinfo": "ログフレーム生成"})
        self.log_widget = Text(self, state="disabled", borderwidth=5, width=21, height=15, wrap="none", padx=10, pady=10)
        ys = ttk.Scrollbar(self, orient="vertical", command=self.log_widget.yview)
        self.log_widget["yscrollcommand"] = ys.set
        self.log_widget.grid(row=1, column=0)
        ys.grid(row=1, column=1, sticky="ns")
