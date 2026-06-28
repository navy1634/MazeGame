import os
from glob import glob
from operator import itemgetter


def logfile_remove() -> None:
    """
    ログファイルを管理する関数
    最新5件までを残す
    """
    file_lists: list[tuple[str, float]] = [(file, os.path.getctime(file)) for file in glob(os.getcwd() + "/maze_my/logs/*.log")]
    file_lists.sort(key=itemgetter(1), reverse=True)
    MAX_CNT = 5
    for i, file_info in enumerate(file_lists):
        if i > MAX_CNT - 1:
            os.remove(file_info[0])


if __name__ == "__main__":
    logfile_remove()
