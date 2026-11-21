#!/usr/bin/env python3
"""CF263B Squares 的 checker（多解）。

输出两个整数 x y (0 <= x,y <= 1e9)，要求恰有 k 个正方形包含它：
正方形 i 是 [0,a_i] x [0,a_i]，点 (x,y) 属于它 ⇔ max(x,y) <= a_i。
-1 表示无解，仅校验格式。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(v) for v in data[2:2 + n]]
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        return 0
    if len(out) != 2:
        print('WA: 应输出两个整数或 -1')
        return 1
    x, y = int(out[0]), int(out[1])
    if not (-10**9 <= x <= 10**9 and -10**9 <= y <= 10**9):
        print('WA: 坐标超范围')
        return 1
    if not (0 <= x <= 10**9 and 0 <= y <= 10**9):
        print('WA: 坐标必须非负')
        return 1
    t = max(x, y)
    cnt = sum(1 for v in a if t <= v)
    if cnt != k:
        print('WA: 点 (%d,%d) 被 %d 个正方形包含，应为 %d' % (x, y, cnt, k))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
