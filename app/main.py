from logging import getLogger
from tkinter import Frame, Label, Menu, Tk

from app.controller.GameController import GameController
from app.lib.SetLog import logger_conf
from app.model.MazeMap import MazeMap
from app.view.parts.GoalView import GoalView
from app.view.parts.LogView import LogView
from app.view.parts.MazeCanvas import MazeCanvas
from app.view.parts.MazeView import MazeView
from app.view.parts.OperationView import OperationView
from app.view.parts.OptionView import OptionView
from app.view.parts.StartView import StartView

logger = getLogger("maze_root").getChild(__name__)


class App(Tk):
    def __init__(self, parent: None = None) -> None:
        super().__init__(parent)
        self.parent = parent
        logger.debug("START", extra={"addinfo": "ウィンドウ生成"})
        self.conf = "config"
        # Modelのインスタンス化
        self.model = MazeMap()
        # Controllerのインスタンス化
        self.controller = GameController(self, self.model, self.conf)
        self._set_frame()
        self.controller.set_view(
            start_view=self.start_view,
            maze_view=self.maze_view,
            main_view=self.main_view,
            operation_view=self.operation_view,
            log_view=self.log_view,
        )
        self.config(menu=self.set_menu())
        self.set_config()

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
        self.conf_data = self.controller.get_setting()
        # フレームのサイズ変更を不可能に
        self.resizable(width=False, height=False)
        # 閉じるボタン
        self.protocol("WM_DELETE_WINDOW", self.win_close)
        self.bind("<Control-Key-q>", lambda e: self.win_close())
        # ホーム画面に戻る
        self.bind("<Control-Key-h>", lambda e: self.controller.raise_frame(self.controller.start_view))
        self.bind("<Control-Key-d>", lambda e: self.controller.raise_frame(self.controller.maze_view))
        self.bind("<Control-Key-c>", lambda e: self.controller.raise_frame(self.controller.operation_view))

    def _set_frame(self) -> None:
        """フレームの設置"""
        # 迷路画面の生成
        self.canvas = MazeCanvas(self, self.controller, conf=self.conf)
        self.main_view = Frame(self)
        maze_index = Label(self.main_view, text="↑ → ↓ ← キーで操作、Ctrl+Cで操作方法の表示、ゴールに辿り着くとクリア")
        self.maze_view = MazeView(self.main_view, self.controller, canvas=self.canvas, conf=self.conf)
        self.option_view = OptionView(self.main_view, self.controller, conf=self.conf)
        self.log_view = LogView(self.main_view, self.controller, conf=self.conf)

        # 迷路画面の配置設定
        maze_index.grid(row=0, column=0)
        self.maze_view.grid(row=1, column=0, rowspan=2, sticky="nsew")
        self.option_view.grid(row=1, column=1, sticky="nsew")
        self.log_view.grid(row=2, column=1)

        # 各画面の生成
        # スタート画面
        self.start_view = StartView(self, self.controller, conf=self.conf)
        self.start_view.grid(row=0, column=0, sticky="nsew")
        # 迷路画面
        self.main_view.grid(row=0, column=0, sticky="nsew")
        # 操作方法確認画面
        self.operation_view = OperationView(self, self.controller, conf=self.conf)
        self.operation_view.grid(row=0, column=0, sticky="nsew")
        # ゴール画面
        self.goal_frame = GoalView(self, self.controller, conf=self.conf)
        self.goal_frame.grid(row=0, column=0, sticky="nsew")

        self.controller.raise_frame(self.start_view)

    def set_menu(self) -> Menu:
        """
        メニューバーの生成を行う関数
        """
        menubar = Menu(self)

        menu_file = Menu(menubar, tearoff=False)
        menu_file.add_command(label="スタート画面", command=lambda: self.controller.raise_frame(self.controller.start_view), accelerator="Ctrl+H")
        menu_file.add_command(label="迷路画面", command=lambda: self.controller.raise_frame(self.controller.maze_view), accelerator="Ctrl+D")
        menu_file.add_separator()  # 仕切り線
        menu_file.add_command(label="終了", command=self.win_close, accelerator="Ctrl+Q")

        # メニューバーに各メニューを追加
        menubar.add_cascade(label="Frame", menu=menu_file)
        menubar.add_cascade(label="Dimension", command=lambda: self.controller.change_dim_for_menu())
        menubar.add_cascade(label="Config", command=lambda: self.controller.raise_frame(self.controller.operation_view), accelerator="Ctrl+C")

        # 親ウィンドウのメニューに、作成したメニューバーを設定
        return menubar

    def win_close(self) -> None:
        """画面を閉じた時の挙動"""
        logger.debug("SAVE", extra={"addinfo": "設定保存"})
        self.controller.save_setting()  # 設定の保存
        logger.debug("END", extra={"addinfo": "ウィンドウ停止"})
        self.quit()  # アプリの終了
        logger.debug("END", extra={"addinfo": "ログ取得終了"})

    def run(self) -> None:
        self.mainloop()


def main():
    logger = logger_conf()
    logger.debug("START", extra={"addinfo": "処理開始"})

    app = App()
    app.run()

    logger.debug("END", extra={"addinfo": "処理終了"})


if __name__ == "__main__":
    main()
