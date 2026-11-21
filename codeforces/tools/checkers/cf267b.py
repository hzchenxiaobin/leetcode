#!/usr/bin/env python3
"""CF267B Dominoes 的 checker（多解）。

输出 n 行 "编号 +/-"：每个编号恰好用一次，且相邻多米诺接触面的点数相同。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    A = [0] * n; B = [0] * n
    for i in range(n):
        A[i] = int(data[1 + 2 * i]); B[i] = int(data[2 + 2 * i])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out and out[0] == 'No':
        return 0
    if len(out) != 2 * n:
        print('WA: 应输出 %d 行' % n)
        return 1
    used = set()
    prev = None
    for i in range(n):
        idx = int(out[2 * i]) - 1
        sign = out[2 * i + 1]
        if not (0 <= idx < n):
            print('WA: 编号越界')
            return 1
        if idx in used:
            print('WA: 第 %d 个多米诺重复使用' % (idx + 1))
            return 1
        used.add(idx)
        if sign not in ('+', '-'):
            print('WA: 方向必须是 + 或 -')
            return 1
        l, r = (A[idx], B[idx]) if sign == '+' else (B[idx], A[idx])
        if prev is not None and prev != l:
            print('WA: 第 %d 处接触面 %d 与 %d 不匹配' % (i, prev, l))
            return 1
        prev = r
    return 0


if __name__ == '__main__':
    sys.exit(main())
