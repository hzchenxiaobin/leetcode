#!/usr/bin/env python3
"""CF263E Rhombus 的 checker（多解）。

输出 a b，要求 k <= a <= n-k+1、k <= b <= m-k+1，且
f(a,b) = Σ_{|i-a|+|j-b| <= k-1} a[i][j] 取到所有合法 (x,y) 上的最大值。
（只在中小数据上使用：内部用 O(n*m*k^2) 的暴力枚举。）
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    g = []
    pos = 3
    for i in range(n):
        g.append([int(v) for v in data[pos:pos + m]])
        pos += m
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if len(out) != 2:
        print('WA: 应输出两个整数')
        return 1
    a, b = int(out[0]), int(out[1])
    if not (k <= a <= n - k + 1 and k <= b <= m - k + 1):
        print('WA: 中心点越界')
        return 1

    def f(x, y):
        tot = 0
        for i in range(max(1, x - k + 1), min(n, x + k - 1) + 1):
            rem = k - 1 - abs(i - x)
            lo = max(1, y - rem); hi = min(m, y + rem)
            for j in range(lo, hi + 1):
                tot += g[i - 1][j - 1]
        return tot

    best = -1
    for x in range(k, n - k + 2):
        for y in range(k, m - k + 2):
            v = f(x, y)
            if v > best:
                best = v
    if f(a, b) != best:
        print('WA: f(%d,%d)=%d 不是最大值 %d' % (a, b, f(a, b), best))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
