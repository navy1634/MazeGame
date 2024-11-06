# -*- coding: utf-8 -*-

from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.ShortestPaths import ShortestPaths
from numpy import vectorize


class MazeCreate(Maze):
    def __init__(self, seed=None) -> None:
        super().__init__(seed)


    def create_maze(self, N, M, seed=None):
        self.mz = Maze(seed=seed)
        # 迷路生成
        self.mz.generator = Prims(N, M)
        self.mz.generate()

        # スタートとゴールのマークを設置
        self.mz.start = (1, 1)
        self.mz.end = (N*2-1, M*2-1)

        return self.maze_tolist()


    def solve_maze(self):
        """
        迷路の解答生成アルゴリズム
        """
        # 幅優先探索
        self.mz.solver = ShortestPaths()
        self.mz.solve()
        return self.maze_tolist()


    def maze_tolist(self):
        """
        迷路の成形を行う
        """
        mz_str = str(self.mz).replace('#', "0").replace(' ', '1').replace('S', '2').replace('E', '3').replace("+", "4").split('\n')
        mz_str_list = [list(x) for x in mz_str]
        return vectorize(int)(mz_str_list)



if __name__ == '__main__':
    maze = MazeCreate()
    N = 20 # 縦の通路の数
    M = 20 # 横の通路の数
    map_data = maze.create_maze(N, M)
    # for mp in map_data:
    #     print(mp)

    map_ans = maze.solve_maze()
    for mp in map_ans:
        print(mp)
