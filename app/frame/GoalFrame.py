# -*- coding: utf-8 -*-

from tkinter import Label, Frame, Button
from logging import getLogger


class GoalFrame(Frame):
    logger = getLogger("maze_root").getChild("Goal")

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.Widget_Width = 30
        self.Widget_Height = 3
        self.set_frame()

    def set_frame(self) -> None:
        Label(self, text='GAME CLEAR !!!', font=('HGS行書体', 100), width=self.Widget_Width, height=self.Widget_Height).pack()
        frame = self.set_button()
        frame.pack()

    def set_button(self):
        frame = Frame(self)
        Button(frame, text='新しく開始', width=self.Widget_Width, height=self.Widget_Height, command=self.new_game, font=("HGS行書体", 15)).grid(row=0, column=0)
        Button(frame, text='やり直す', width=self.Widget_Width, height=self.Widget_Height, command=self.restart, font=("HGS行書体", 15)).grid(row=0, column=1)
        Button(frame, text='スタート画面へ', width=self.Widget_Width, height=self.Widget_Height, command=self.start_frame, font=("HGS行書体", 15)).grid(row=1, column=0)
        Button(frame, text='終了', width=self.Widget_Width, height=self.Widget_Height, command=self.close, font=("HGS行書体", 15)).grid(row=1, column=1)
        return frame

    def restart(self) -> None:
        self.logger.debug('RESET', extra={'addinfo': '位置リセット'})
        self.parent.maze_frame.Maze_Frame.maze.return_default()
        self.parent.maze_frame.Maze_Frame.maze.draw_map_event()
        self.parent.maze_frame.Log_Frame.getLoc(1, 1)
        self.parent.maze_frame.Log_Frame.writeToLog('再開')
        self.parent.raise_frame(self.parent.maze_frame)

    def new_game(self) -> None:
        self.logger.debug('RESTART', extra={'addinfo': '迷路再生成'})
        self.parent.maze_frame.Maze_Frame.maze.load_map(self.parent.start_frame.size_h.get(), self.parent.start_frame.size_w.get())
        self.parent.maze_frame.Maze_Frame.maze.return_default()
        self.parent.maze_frame.Maze_Frame.maze.draw_map_event()
        self.parent.maze_frame.Log_Frame.getLoc(1, 1)
        self.parent.maze_frame.Log_Frame.writeToLog('リスタート')
        self.parent.raise_frame(self.parent.maze_frame)

    def start_frame(self) -> None:
        self.parent.raise_frame(self.parent.start_frame)

    def close(self) -> None:
        self.parent.win_close()
