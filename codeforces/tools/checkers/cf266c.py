#!/usr/bin/env python3
"""CF266C Below the Diagonal 的 checker（多解）。

输出 m 个操作 (t,i,j)：t=1 交换行，t=2 交换列。要求 m <= 1e5、
所有 1 最终都位于主对角线下方（行号 > 列号）。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    ones = []
    p = 1
    for _ in range(n - 1):
        ones.append((int(data[p]), int(data[p + 1])))
        p += 2
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if not out:
        print('WA: 空输出')
        return 1
    m = int(out[0])
    if m < 0 or m > 100000 or len(out) != 1 + 3 * m:
        print('WA: 操作数不合法')
        return 1
    cells = set(ones)
    for k in range(m):
        t, i, j = int(out[1 + 3 * k]), int(out[2 + 3 * k]), int(out[3 + 3 * k])
        if t not in (1, 2) or not (1 <= i <= n and 1 <= j <= n) or i == j:
            print('WA: 第 %d 个操作不合法' % (k + 1))
            return 1
        if t == 1:
            cells = {(j if x == i else (i if x == j else x), y) for (x, y) in cells}
        else:
            cells = {(x, j if y == i else (i if y == j else y)) for (x, y) in cells}
    for (x, y) in cells:
        if not (x > y):
            print('WA: 仍有 1 不在对角线下方: (%d,%d)' % (x, y))
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
