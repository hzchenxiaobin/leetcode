#!/usr/bin/env python3
"""CF263D Cycle in Graph 的 checker（多解）。

输出 r 与 r 个点，要求 r >= k+1、点互不相同、相邻（含首尾）都是图中的边。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    es = set()
    pos = 3
    for _ in range(m):
        u, v = int(data[pos]), int(data[pos + 1]); pos += 2
        es.add((min(u, v), max(u, v)))
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        print('WA: 题目保证有解，不应输出 -1')
        return 1
    r = int(out[0])
    cyc = [int(v) for v in out[1:1 + r]]
    if r < k + 1:
        print('WA: 环长 %d 小于 k+1=%d' % (r, k + 1))
        return 1
    if len(cyc) != r or len(set(cyc)) != r:
        print('WA: 点数不对或点重复')
        return 1
    if any(not (1 <= v <= n) for v in cyc):
        print('WA: 点下标越界')
        return 1
    for i in range(r):
        u, v = cyc[i], cyc[(i + 1) % r]
        if (min(u, v), max(u, v)) not in es:
            print('WA: (%d,%d) 不是图中的边' % (u, v))
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
