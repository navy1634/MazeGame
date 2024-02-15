# -*- coding: utf-8 -*-

from Frame.Window import MainWindow
from config.SetLog import logger_conf


def main():
    logger = logger_conf()
    logger.debug('START', extra={'addinfo': '処理開始'})

    root = MainWindow()
    root.mainloop()

    logger.debug('END', extra={'addinfo': '処理終了'})


if __name__ == '__main__':
    main()

