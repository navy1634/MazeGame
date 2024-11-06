# -*- coding: utf-8 -*-

from tkinter import Frame, Button, Label, IntVar, Radiobutton, Spinbox, LabelFrame
from logging import getLogger


class StartFrame(Frame):
    logger = getLogger("maze_root").getChild("START")

    def __init__(self, parent, conf) -> None:
        super().__init__(parent)
        self.parent = parent
        self.conf = conf
        self.Widget_Width = 30
        self.Widget_Height = 3
        self.set_frame()

    def set_frame(self):
        name_label = Label(self, text="迷路ゲーム", font=("HGS行書体", 50), width=30, height=3)
        button_frame = self.set_button()
        setting_frame = self.setting_frame()
        radio_frame = self.radio_frame()

        name_label.pack()
        setting_frame.pack()
        radio_frame.pack()
        button_frame.pack()

    def set_button(self) -> Frame:
        frame = Frame(self, height=15, width=30)

        start_button = Button(frame, text="START", width=self.Widget_Width, height=self.Widget_Height, command=lambda: [self.parent.set_maze_frame(), self.parent.raise_frame(self.parent.maze_frame)], font=("HGS行書体", 15))
        setting_button = Button(frame, text="操作方法", width=self.Widget_Width, height=self.Widget_Height, command=lambda : self.parent.raise_frame(self.parent.conf_frame), font=("HGS行書体", 15))

        start_button.pack()
        setting_button.pack()
        return frame

    def setting_frame(self) -> LabelFrame:
        frame = LabelFrame(self, text="迷路サイズ", height=15, width=30)

        self.size_h = IntVar()
        self.size_w = IntVar()
        self.size_h.set(10)
        self.size_w.set(10)

        Label(frame, text="Height", width=15, height=self.Widget_Height).grid(row=0, column=0)
        Label(frame, text="Width", width=15, height=self.Widget_Height).grid(row=1, column=0)
        Spinbox(frame, from_=3, to=30, width=8, textvariable=self.size_h).grid(row=0, column=1)
        Spinbox(frame, from_=3, to=30, width=8, textvariable=self.size_w).grid(row=1, column=1)
        Label(frame, text="×2+1 マス", width=15, height=self.Widget_Height).grid(row=0, column=2)
        Label(frame, text="×2+1 マス", width=15, height=self.Widget_Height).grid(row=1, column=2)

        return frame

    def radio_frame(self):
        frame = LabelFrame(self, text="モード設定", width=40, height=20)
        self.radio_value = IntVar()
        radio_2D = Radiobutton(frame, text="2D", command=lambda: self.parent.change_dimension(0), variable=self.radio_value, value=0, width=self.Widget_Width, height=2)
        radio_3D = Radiobutton(frame, text="3D", command=lambda: self.parent.change_dimension(1), variable=self.radio_value, value=1, height=2)
        self.radio_value.set(self.conf["dim"])

        radio_2D.pack()
        radio_3D.pack()
        return frame
