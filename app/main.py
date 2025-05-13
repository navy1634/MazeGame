from logging import getLogger
from tkinter import Menu, Tk

from app.controller.GameController import GameController
from app.lib.SetLog import logger_conf
from app.model.MazeMap import MazeMap
from app.view.GoalView import GoalView
from app.view.MazeView import MazeView
from app.view.OperationView import OperationView
from app.view.StartView import StartView

logger = getLogger("maze_root").getChild(__name__)


class App(Tk):
    """アプリのメイン部分"""

    def __init__(self) -> None:
        super().__init__(None)
        logger.debug("START", extra={"addinfo": "ウィンドウ生成"})
        # Modelのインスタンス化
        self.model = MazeMap()
        # Controllerのインスタンス化
        self.controller = GameController(self, self.model)
        self.controller.set_maze_controller()
        self._set_frame()
        self.controller.set_view(
            start_view=self.start_view,
            maze_view=self.maze_view,
            main_view=self.maze_view.maze_view,
            operation_view=self.operation_view,
            log_view=self.maze_view.log_view,
        )
        self.controller.maze_2d_controller.set_maze_view(self.maze_view)
        self.controller.maze_3d_controller.set_maze_view(self.maze_view)
        # メニューバーの生成
        self.config(menu=self.set_menu())
        # ウィンドウの詳細設定
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
        # フレームのサイズ変更を不可能に
        self.resizable(width=False, height=False)
        # 閉じるボタン
        self.protocol("WM_DELETE_WINDOW", self.win_close)
        self.bind("<Control-Key-q>", lambda _: self.win_close())
        # ホーム画面に戻る
        self.bind("<Control-Key-h>", lambda _: self.controller.raise_frame(self.controller.start_view))
        self.bind("<Control-Key-d>", lambda _: self.controller.raise_frame(self.controller.maze_view))
        self.bind("<Control-Key-c>", lambda _: self.controller.raise_frame(self.controller.operation_view))

    def _set_frame(self) -> None:
        """フレームの設置"""
        # 各画面の生成
        # スタート画面
        self.start_view = StartView(self, self.controller)
        self.start_view.grid(row=0, column=0, sticky="nsew")
        # 迷路画面
        self.maze_view = MazeView(self, self.controller)
        self.maze_view.grid(row=0, column=0, sticky="nsew")
        # 操作方法確認画面
        self.operation_view = OperationView(self)
        self.operation_view.grid(row=0, column=0, sticky="nsew")
        # ゴール画面
        self.goal_frame = GoalView(self, self.controller)
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
        menubar.add_cascade(label="Dimension", command=lambda: self.change_dim_for_menu())
        menubar.add_cascade(label="Config", command=lambda: self.controller.raise_frame(self.controller.operation_view), accelerator="Ctrl+C")

        # 親ウィンドウのメニューに、作成したメニューバーを設定
        return menubar

    def change_dim_for_menu(self) -> None:
        """メニューバー用の関数
        2D, 3Dを切り替える
        """
        dim = self.start_view.radio_value.get()
        if dim == 0:
            dim = 1
        else:
            dim = 0
        self.controller.change_dimension(dim)

    def win_close(self) -> None:
        """画面を閉じた時の挙動"""
        logger.debug("SAVE", extra={"addinfo": "設定保存"})
        self.controller.save_setting()  # 設定の保存
        logger.debug("END", extra={"addinfo": "ウィンドウ停止"})
        self.quit()  # アプリの終了
        logger.debug("END", extra={"addinfo": "ログ取得終了"})

    def run(self) -> None:
        """アプリの実行"""
        self.mainloop()


def main():
    logger = logger_conf()
    app = App()
    app.run()


if __name__ == "__main__":
    main()
