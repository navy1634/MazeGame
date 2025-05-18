from os import getcwd

# プロジェクトファイルまでの絶対パス
BASE_DIR = getcwd()
IMAGE_DIR = BASE_DIR + "/images"
LOG_DIR = BASE_DIR + "/logs"
SRC_DIR = BASE_DIR + "/app"

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
