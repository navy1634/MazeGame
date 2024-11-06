# -*- coding: utf-8 -*-

from tkinter import Frame, Label
from frame.MazeFrame import MazeFrame
from frame.MazeOption import MazeOption
from frame.LogFrame import LogFrame
from logging import getLogger


class MainFrame(Frame):
    logger = getLogger("maze_root").getChild(__name__)

    def __init__(self, parent, conf) -> None:
        super().__init__(parent)
        self.parent = parent

        # 各widgetの生成
        Maze_Index = Label(self, text='↑ → ↓ ← キーで操作、Ctrl+Cで操作方法の表示、ゴールに辿り着くとクリア')
        self.Maze_Frame = MazeFrame(self, conf=conf)
        Option_Button = MazeOption(self, conf=conf)
        self.Log_Frame = LogFrame(self)

        # widgetの配置設定
        Maze_Index.grid(row=0, column=0)
        self.Maze_Frame.grid(row=1, column=0, rowspan=2, sticky="nsew")
        Option_Button.grid(row=1, column=1, sticky="nsew")
        self.Log_Frame.grid(row=2, column=1)
