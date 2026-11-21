#!/usr/bin/env python3
"""CF263C Circle of Numbers 的 checker（多解）。

输出一个 1..n 的排列（或 -1）。要求从这个环推出的 2n 条弧
（相邻 = 环上距离 1 或 2 的点对）与输入的 2n 条边完全一致。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    given = set()
    pos = 1
    for _ in range(2 * n):
        u, v = int(data[pos]), int(data[pos + 1]); pos += 2
        given.add((min(u, v), max(u, v)))
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        return 0
    if len(out) != n:
        print('WA: 应输出 %d 个数' % n)
        return 1
    cyc = [int(v) for v in out]
    if sorted(cyc) != list(range(1, n + 1)):
        print('WA: 不是 1..n 的排列')
        return 1
    expect = set()
    for i in range(n):
        u = cyc[i]
        for d in (1, 2):
            v = cyc[(i + d) % n]
            expect.add((min(u, v), max(u, v)))
    if expect != given:
        print('WA: 由这个环推出的弧集与输入不一致（差 %d 条）' % len(expect ^ given))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
