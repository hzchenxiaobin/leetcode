#!/usr/bin/env python3
"""CF268C Beautiful Sets of Points 的 checker（多解）。

输出 k 与 k 个点：0<=x<=n, 0<=y<=m, x+y>0；任意两点距离不是整数。
（距离是整数 ⇔ dx^2+dy^2 是完全平方数。）
"""
import sys
import math


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, m = int(data[0]), int(data[1])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if not out:
        print('WA: 空输出')
        return 1
    k = int(out[0])
    if len(out) != 1 + 2 * k:
        print('WA: 点数与声明不符')
        return 1
    pts = []
    for i in range(k):
        x = int(out[1 + 2 * i]); y = int(out[2 + 2 * i])
        if not (0 <= x <= n and 0 <= y <= m):
            print('WA: 点越界 (%d,%d)' % (x, y))
            return 1
        if x + y <= 0:
            print('WA: 不允许 (0,0)')
            return 1
        pts.append((x, y))
    if len(set(pts)) != k:
        print('WA: 有重复点')
        return 1
    for i in range(k):
        for j in range(i + 1, k):
            d2 = (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
            if math.isqrt(d2) ** 2 == d2:
                print('WA: (%d,%d) 与 (%d,%d) 距离是整数' % (pts[i] + pts[j]))
                return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
