import sys
from os import environ, getcwd, makedirs, path


def resource_path(relative: str) -> str:
    """バンドル時は _MEIPASS、ソース実行時は getcwd を基点にリソースを解決する"""
    base = getattr(sys, "_MEIPASS", getcwd())
    return path.join(base, relative)


def user_data_dir() -> str:
    """書き込み可能なユーザーデータ領域 (%APPDATA%/MazeGame) を返す。無ければ作成する"""
    base = environ.get("APPDATA") or path.expanduser("~")
    directory = path.join(base, "MazeGame")
    makedirs(directory, exist_ok=True)
    return directory


# 画像など読み取り専用リソース(バンドルに同梱)
IMAGE_DIR = resource_path("images")
# ログの出力先(書き込み可能領域)
LOG_DIR = path.join(user_data_dir(), "logs")
# 設定ファイルの保存先(書き込み可能領域)
SETTING_FILE = path.join(user_data_dir(), "setting.json")
# 同梱する設定ファイルの初期値
DEFAULT_SETTING_FILE = resource_path("app/config/setting.json")

# 3Dマップの参照先
POS_X = [
    [-1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0, 1],
    [3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
    [1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0, -1],
    [-3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0],
]
POS_Y = [
    [-3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0],
    [-1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0, 1],
    [3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
    [1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0, -1],
]

# 要素のサイズ
WIDGET_WIDTH = 15
WIDGET_HEIGHT = 1

# フレームのサイズ
FRAME_WIDTH = 800
FRAME_HEIGHT = 600
SUB_FRAME_WIDTH = 60
SUB_FRAME_HEIGHT = 100

# サブフレームのサイズ
SUB_FRAME_MAZE_WIDTH = 3
SUB_FRAME_MAZE_HEIGHT = 4
