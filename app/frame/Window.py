# -*- coding: utf-8 -*-

import json
from tkinter import Tk, Menu
from frame.MainFrame import MainFrame
from frame.StartFrame import StartFrame
from frame.OperationFrame import OperationFrame
from frame.GoalFrame import GoalFrame
from logging import getLogger
from config.conf import SRC_DIR


class MainWindow(Tk):
    """
    メインウィンドウ
    """
    logger = getLogger("maze_root").getChild(__name__)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.logger.debug("START", extra={"addinfo": "ウィンドウ生成"})
        # Window の詳細設定
        self.set_config()
        # メニューバーの生成
        self.config(menu=self.set_menu())
        # フレームの設置
        self.set_frame()

    def set_frame(self) -> None:
        # フレームの設置
        self.start_frame = StartFrame(self, conf=self.conf_data) # スタート画面
        self.maze_frame = MainFrame(self, conf=self.conf_data) # 迷路画面
        self.conf_frame = OperationFrame(self) # 操作方法確認画面
        self.goal_frame = GoalFrame(self) # ゴール画面
        self.start_frame.grid(row=0, column=0, sticky="nsew")
        self.maze_frame.grid(row=0, column=0, sticky="nsew")
        self.conf_frame.grid(row=0, column=0, sticky="nsew")
        self.goal_frame.grid(row=0, column=0, sticky="nsew")
        self.raise_frame(self.start_frame)

    def set_maze_frame(self) -> None:
        """
        迷路生成し、画面を表示
        """
        self.maze_frame.Maze_Frame.changePage(self.start_frame.radio_value.get())
        self.raise_frame(self.maze_frame)

    def set_config(self) -> None:
        """
        ウィンドウの詳細設定を行う関数
        """
        # タイトルバー
        self.title("ソフトウェア開発論")
        # ウィンドウのサイズ
        self.geometry("1000x630")
        # frame.tkraise() 用の設定
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # 設定情報の取得
        self.conf_data = self.get_setting()
        # フレームのサイズ変更を不可能に
        self.resizable(width=False, height=False)
        # 閉じるボタン
        self.protocol("WM_DELETE_WINDOW", self.win_close)
        self.bind("<Control-Key-q>", lambda e: self.win_close())
        # ホーム画面に戻る
        self.bind("<Control-Key-h>", lambda e: self.raise_frame(self.start_frame))
        self.bind("<Control-Key-d>", lambda e: self.raise_frame(self.maze_frame))
        self.bind("<Control-Key-c>", lambda e: self.raise_frame(self.conf_frame))

    def change_dimension(self, dim, val=False) -> None:
        """
        2D, 3D の切替を行う関数
        """
        self.logger.debug("SET", extra={"addinfo": f"{dim+2}D"})
        # 各ラジオボタンと変数を共有
        self.start_frame.radio_value.set(dim)
        self.maze_frame.Maze_Frame.changePage(dim, flag_seed=val) # 切替

    def change_dim_for_menu(self):
        dim = self.start_frame.radio_value.get()
        if dim == 0:
            dim = 1
        else:
            dim = 0

        self.change_dimension(dim, val=True)

    def set_menu(self) -> Menu:
        """
        メニューバーの生成を行う関数
        """
        menubar = Menu(self)

        menu_file = Menu(menubar, tearoff = False)
        menu_file.add_command(label="スタート画面", command=lambda: self.raise_frame(self.start_frame), accelerator="Ctrl+H")
        menu_file.add_command(label="迷路画面", command=lambda: self.raise_frame(self.maze_frame), accelerator="Ctrl+D")
        menu_file.add_separator() # 仕切り線
        menu_file.add_command(label="終了", command=self.win_close, accelerator="Ctrl+Q")

        # メニューバーに各メニューを追加
        menubar.add_cascade(label="Frame", menu=menu_file)
        menubar.add_cascade(label="Dimension", command=lambda: self.change_dim_for_menu())
        menubar.add_cascade(label="Config", command=lambda:self.raise_frame(self.conf_frame), accelerator="Ctrl+C")

        # 親ウィンドウのメニューに、作成したメニューバーを設定
        return menubar

    def get_setting(self) -> dict:
        """
        設定ファイルの読み込み
        """
        with open(SRC_DIR + "/config/setting.json", "r", encoding="utf-8") as f:
            conf_data = json.load(f)
            f.close()
        return conf_data

    def save_setting(self) -> None:
        """
        設定ファイルの保存
        """
        self.conf_data['dim'] = self.start_frame.radio_value.get()
        with open(SRC_DIR + "/setting.json", "w", encoding="utf-8") as f:
            json.dump(self.conf_data, f)
            f.close()

    def win_close(self) -> None:
        self.logger.debug("SAVE", extra={"addinfo": "設定保存"})
        self.save_setting() # 設定の保存
        self.logger.debug("END", extra={"addinfo": "ウィンドウ停止"})
        self.quit() # アプリの終了
        self.logger.debug("END", extra={"addinfo": "ログ取得終了"})

    def raise_frame(self, frame):
        """
        画面遷移用の関数
        """
        self.logger.debug("FRAME", extra={"addinfo": f"{type(frame)}に遷移"})
        frame.tkraise()
