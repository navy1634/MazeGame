from __future__ import annotations

from tkinter import Button, Frame, IntVar, Label, LabelFrame, Radiobutton, Spinbox, Tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.controller.GameController import GameController


class StartView(Frame):
    def __init__(self, parent: Tk | Frame, controller: GameController) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.widget_width = 30
        self.widget_height = 3

        name_label = Label(self, text="迷路ゲーム", font=("HGS行書体", 50), width=30, height=3)
        button_frame = self.create_button()
        setting_frame = self.setting_frame()
        radio_frame = self.radio_frame()

        name_label.pack()
        setting_frame.pack()
        radio_frame.pack()
        button_frame.pack()

    def create_button(self) -> Frame:
        """ボタンの作成

        Returns:
            Frame: ボタンを配置するフレーム
        """
        frame = Frame(self, height=15, width=30)

        start_button = Button(
            frame,
            text="START",
            width=self.widget_width,
            height=self.widget_height,
            command=lambda: [self.controller.set_maze_frame(), self.controller.raise_frame(self.controller.maze_view)],
            font=("HGS行書体", 15),
        )
        setting_button = Button(
            frame, text="操作方法", width=self.widget_width, height=self.widget_height, command=lambda: self.controller.raise_frame(self.controller.operation_view), font=("HGS行書体", 15)
        )

        start_button.pack()
        setting_button.pack()
        return frame

    def setting_frame(self) -> LabelFrame:
        """迷路サイズ設定用のフレーム

        Returns:
            LabelFrame: 迷路サイズ設定
        """
        frame = LabelFrame(self, text="迷路サイズ", height=15, width=30)

        self.size_h = IntVar()
        self.size_w = IntVar()
        self.size_h.set(10)
        self.size_w.set(10)

        Label(frame, text="Height", width=15, height=self.widget_height).grid(row=0, column=0)
        Label(frame, text="Width", width=15, height=self.widget_height).grid(row=1, column=0)
        Spinbox(frame, from_=3, to=30, width=8, textvariable=self.size_h).grid(row=0, column=1)
        Spinbox(frame, from_=3, to=30, width=8, textvariable=self.size_w).grid(row=1, column=1)
        Label(frame, text="×2+1 マス", width=15, height=self.widget_height).grid(row=0, column=2)
        Label(frame, text="×2+1 マス", width=15, height=self.widget_height).grid(row=1, column=2)

        return frame

    def radio_frame(self) -> LabelFrame:
        """モード設定用のボタン

        Returns:
            LabelFrame: モード設定ボタン
        """
        frame = LabelFrame(self, text="モード設定", width=40, height=20)
        self.radio_value = IntVar()
        radio_2D = Radiobutton(frame, text="2D", command=lambda: self.controller.change_dimension(0), variable=self.radio_value, value=0, width=self.widget_width, height=2)
        radio_3D = Radiobutton(frame, text="3D", command=lambda: self.controller.change_dimension(1), variable=self.radio_value, value=1, height=2)
        self.radio_value.set(0)

        radio_2D.pack()
        radio_3D.pack()
        return frame

    def set_radio_value(self, value: int) -> None:
        """ラジオボタンの値を設定する

        Args:
            value (int): 値
        """
        self.radio_value.set(value)

    def get_radio_value(self) -> int:
        """ラジオボタンの値を取得する

        Returns:
            int: ラジオボタンの値 (0 or 1)
        """
        return self.radio_value.get()

    def get_size(self) -> tuple[int, int]:
        """迷路のサイズを取得する

        Returns:
            tuple[int, int]: 迷路のサイズ (height, width)
        """
        return self.size_h.get(), self.size_w.get()
