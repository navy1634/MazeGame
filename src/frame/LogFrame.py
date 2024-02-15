# -*- coding: utf-8 -*-

from tkinter import Frame, ttk, Text
from datetime import datetime
from logging import getLogger


class LogFrame(Frame):
    logger = getLogger("maze_root").getChild("Log")
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.set_current_location()
        self.set_log()

    def set_current_location(self) -> None:
        self.loc_widget = Text(self, state='disabled', width=28, height=1)
        self.loc_widget.grid(row=0, column=0, columnspan=2)

    def getLoc(self, px, py) -> None:
        message = "現在地 x座標: {px}, y座標: {py}".format(px=px, py=py)
        self.loc_widget['state'] = 'normal'
        self.loc_widget.delete('1.0', 'end')
        self.loc_widget.insert('end', message)
        self.loc_widget['state'] = 'disabled'

    def set_log(self) -> None:
        self.logger.debug("SET", extra={"addinfo": f"ログフレーム生成"})
        self.log_widget = Text(self, state='disabled', borderwidth=5, width=21, height=15, wrap='none', padx=10, pady=10)
        ys = ttk.Scrollbar(self, orient = 'vertical', command = self.log_widget.yview)
        self.log_widget['yscrollcommand'] = ys.set
        self.log_widget.grid(row=1, column=0)
        ys.grid(row=1, column=1, sticky='ns')

    def writeToLog(self, msg) -> None:
        message = "{time}  {message}".format(time=datetime.strftime(datetime.now(), '%H:%M:%S'), message=msg)
        self.log_widget['state'] = 'normal'
        if self.log_widget.index('end-1c')!='1.0':
            self.log_widget.insert('end', '\n')

        self.log_widget.insert('end', message)
        self.log_widget.see('end')
        self.log_widget['state'] = 'disabled'

