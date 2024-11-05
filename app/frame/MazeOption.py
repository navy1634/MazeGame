# -*- coding: utf-8 -*-

from tkinter import Frame, Button
from logging import getLogger


class MazeOption(Frame):
    logger = getLogger("maze_root").getChild(__name__)

    def __init__(self, parent, conf) -> None:
        super().__init__(parent)
        self.parent = parent
        self.Widget_Width = conf["widget"]["Width"]
        self.Widget_Height = conf["widget"]["Height"]

        Button(self, text='reset', command=self.maze_reset, width=self.Widget_Width, height=self.Widget_Height).pack(anchor='center')
        Button(self, text='restart', command=self.maze_restart, width=self.Widget_Width, height=self.Widget_Height).pack(anchor='center')
        Button(self, text='solve', command=self.maze_solve, width=self.Widget_Width, height=self.Widget_Height).pack(anchor='center')
        Button(self, text='close', command=self.maze_close, width=self.Widget_Width, height=self.Widget_Height).pack(anchor='center')

    def maze_reset(self) -> None:
        self.logger.debug('RESET', extra={'addinfo': '位置リセット'})
        self.parent.Maze_Frame.maze.return_default()
        self.parent.Maze_Frame.maze.draw_map_event()
        self.parent.Log_Frame.getLoc(1, 1)
        self.parent.Log_Frame.writeToLog('リセット')

    def maze_restart(self) -> None:
        self.logger.debug('RESTART', extra={'addinfo': '迷路再生成'})
        self.parent.Maze_Frame.maze.load_map(self.parent.parent.start_frame.size_h.get(), self.parent.parent.start_frame.size_w.get())
        self.parent.Maze_Frame.maze.return_default()
        self.parent.Maze_Frame.maze.draw_map_event()
        self.parent.Log_Frame.getLoc(1, 1)
        self.parent.Log_Frame.writeToLog('リスタート')

    def maze_solve(self) -> None:
        self.logger.debug('SOLVE', extra={'addinfo': '迷路解答表示'})
        self.parent.Maze_Frame.maze.get_ans()
        self.parent.Maze_Frame.maze.draw_map_event()
        self.parent.Log_Frame.writeToLog('解答表示')

    def maze_close(self) -> None:
        self.parent.parent.win_close()

