#!/usr/bin/env python3
"""CF254D Rats 的 checker（多解）。

校验条件：
  1. 输出要么是 -1，要么是四个整数 r1 c1 r2 c2；
  2. 两个格子都在表内、都不是墙、且不是同一个格子；
  3. 两枚手雷的爆炸波（沿非墙格子四连通、距离 ≤ d）覆盖了所有 'R' 格。

用法: python3 cf254d.py <input> <output> <answer>
"""
import sys
from collections import deque


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, m, d = int(data[0]), int(data[1]), int(data[2])
    g = data[3:3 + n]
    out = open(sys.argv[2], encoding='utf-8').read().split()
    rats = [(i, j) for i in range(n) for j in range(m) if g[i][j] == 'R']
    if out == ['-1']:
        return 0                     # 只验格式；可行性由对拍程序保证
    if len(out) != 4:
        print('WA: 输出应为四个整数或 -1')
        return 1
    r1, c1, r2, c2 = (int(v) for v in out)
    cells = [(r1 - 1, c1 - 1), (r2 - 1, c2 - 1)]
    for (r, c) in cells:
        if not (0 <= r < n and 0 <= c < m):
            print('WA: 坐标越界')
            return 1
        if g[r][c] == 'X':
            print('WA: 手雷放在了墙上')
            return 1
    if cells[0] == cells[1]:
        print('WA: 两枚手雷在同一个格子')
        return 1
    covered = set()
    for (sr, sc) in cells:
        dist = {(sr, sc): 0}
        q = deque([(sr, sc)])
        while q:
            i, j = q.popleft()
            covered.add((i, j))
            if dist[(i, j)] == d:
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and g[ni][nj] != 'X' and (ni, nj) not in dist:
                    dist[(ni, nj)] = dist[(i, j)] + 1
                    q.append((ni, nj))
    for (i, j) in rats:
        if (i, j) not in covered:
            print('WA: 老鼠 (%d,%d) 没有被覆盖' % (i + 1, j + 1))
            return 1
    return 0


sys.exit(main())
