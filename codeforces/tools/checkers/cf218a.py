#!/usr/bin/env python3
"""CF 218A Mountain Scenery 的构造合法性 checker。

题意：Bolek 把恰好 k 个山峰（偶数 x 坐标）的 y 值各抬高 1，其余顶点不变，
得到给定的折线 r。输出任意一个合法的初始折线 y。

校验条件：
  1. 输出恰好 2n+1 个整数，且都在 [0, 100] 内；
  2. 每个顶点要么与 r 相同，要么是"山峰被抬高 1"（偶数下标的 y 恰为 r-1），
     且与 r 不同的顶点恰好 k 个；
  3. y 是合法的山峰折线：对每个峰 p，y[2p] > y[2p-1] 且 y[2p] > y[2p+1]（1-based）。

约定：python3 cf218a.py <input> <output> <answer>，返回 0 表示通过。
"""
import sys


def main():
    inp, out = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    n, k = int(data[0]), int(data[1])
    r = [int(x) for x in data[2:2 + 2 * n + 1]]
    m = 2 * n + 1
    got = open(out).read().split()
    if len(got) != m:
        print(f'CHECKER FAIL: 需要 {m} 个数，实际 {len(got)} 个')
        return 1
    try:
        y = [int(x) for x in got]
    except ValueError:
        print('CHECKER FAIL: 输出含非整数 token')
        return 1
    if any(v < 0 or v > 100 for v in y):
        print('CHECKER FAIL: y 超出 [0, 100]')
        return 1
    changed = [i for i in range(m) if y[i] != r[i]]
    if len(changed) != k:
        print(f'CHECKER FAIL: 被改动的顶点数 {len(changed)} != k={k}')
        return 1
    for i in changed:
        # 0-based 下标 i 是 1-based 的 i+1；山峰是 1-based 偶数 → 0-based 奇数
        if i % 2 != 1:
            print(f'CHECKER FAIL: 顶点 {i + 1} 不是山峰却被改动')
            return 1
        if y[i] != r[i] - 1:
            print(f'CHECKER FAIL: 山峰 {i + 1} 应恰好降低 1')
            return 1
    for p in range(1, n + 1):
        i = 2 * p - 1
        if not (y[i] > y[i - 1] and y[i] > y[i + 1]):
            print(f'CHECKER FAIL: 第 {p} 个山峰不是严格峰（y={y[i]}）')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
