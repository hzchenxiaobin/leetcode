#!/usr/bin/env python3
"""CF245D Restoring Table 校验器（多解）。

约定：python3 cf245d.py <input> <output> <answer>，返回 0 表示通过。
校验条件：恰好 n 个整数，每个 0 <= a_i <= 1e9；且对任意 i != j 有
a_i AND a_j == b_ij（输入的矩阵）。
"""
import sys


def main():
    if len(sys.argv) < 3:
        print('CHECKER FAIL: 用法 cf245d.py <input> <output> <answer>')
        sys.exit(1)
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    b = [[0] * n for _ in range(n)]
    p = 1
    for i in range(n):
        for j in range(n):
            b[i][j] = int(data[p])
            p += 1
    out = open(sys.argv[2]).read().split()

    def bad(msg):
        print('CHECKER FAIL:', msg)
        sys.exit(1)

    if len(out) != n:
        bad('需要 %d 个整数，实际 %d 个' % (n, len(out)))
    a = []
    for t in out:
        try:
            v = int(t)
        except ValueError:
            bad('非整数: %r' % t)
        if not (0 <= v <= 10 ** 9):
            bad('a_i 超出 [0,1e9]: %d' % v)
        a.append(v)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if (a[i] & a[j]) != b[i][j]:
                bad('a[%d] & a[%d] = %d != b = %d' % (i, j, a[i] & a[j], b[i][j]))


if __name__ == '__main__':
    main()
