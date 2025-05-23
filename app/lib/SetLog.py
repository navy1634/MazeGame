# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta, timezone
from logging import DEBUG, FileHandler, Formatter, Logger, StreamHandler, getLogger

from app.config.config import LOG_DIR


def logger_conf() -> Logger:
    """
    ログ取得に関する関数
    """
    time = datetime.strftime(datetime.now(timezone.utc) + timedelta(hours=9), "%Y%m%d%H%M%S%f")
    # ロガーの生成
    logger = getLogger("maze_root")
    # 出力レベルの設定
    logger.setLevel(DEBUG)

    # ハンドラの生成
    sh = StreamHandler(sys.stdout)
    fh = FileHandler(filename=LOG_DIR + "/{time}.log".format(time=time), encoding="utf-8")
    # 出力レベルの設定
    sh.setLevel(DEBUG)
    fh.setLevel(DEBUG)
    # sh.setLevel(WARNING)

    # フォーマッタの生成（第一引数はメッセージのフォーマット文字列、第二引数は日付時刻のフォーマット文字列）
    # 2022-12-15 14:17:47 【  Move  】 player=4,1, direction=1
    fmt_terminal = Formatter("%(asctime)s %(levelname)s :【 %(name)s 】%(message)s : %(addinfo)s", "%Y-%m-%d %H:%M:%S")
    # fmt_file = Formatter("%(asctime)s 【 %(message)s 】%(addinfo)s\n", "%Y-%m-%d %H:%M:%S")

    # フォーマッタの登録
    sh.setFormatter(fmt_terminal)
    # fh.setFormatter(fmt_file)

    # ハンドラの登録
    logger.addHandler(sh)
    # logger.addHandler(fh)

    logger.debug("START", extra={"addinfo": "ログ取得開始"})
    return logger
