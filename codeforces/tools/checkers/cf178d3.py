#!/usr/bin/env python3
"""CF178D3 Magic Squares 的 checker（答案不唯一，只要合法即通过）。

用法：python3 cf178d3.py <input> <output> <answer>

校验条件：
  1. 第一行是一个整数 s，其后恰有 n 行、每行 n 个整数；
  2. 输出的 n^2 个数与输入的 n^2 个数**作为多重集完全相等**；
  3. 每行、每列、两条主对角线之和都等于 s；
  4. s 等于输入总和除以 n（由 2、3 自动成立，仍显式检查）。

注意：本题答案不唯一，checker **不比对** stdin 里的期望输出（样例给的是其中一种）。
"""
import sys
from collections import Counter


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    src = [int(x) for x in data[1:1 + n * n]]

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1 + n * n:
        print(f'输出应有 1 + {n*n} 个整数，实际 {len(toks)} 个')
        return 1
    try:
        s = int(toks[0])
        grid = [[int(toks[1 + i * n + j]) for j in range(n)] for i in range(n)]
    except ValueError:
        print('输出含非整数')
        return 1

    flat = [x for row in grid for x in row]
    if Counter(flat) != Counter(src):
        print('多重集与输入不一致')
        return 1
    if sum(src) != s * n:
        print(f's 错误：应为 {sum(src)/n}，实际 {s}')
        return 1
    for i in range(n):
        if sum(grid[i]) != s:
            print(f'第 {i+1} 行和为 {sum(grid[i])}，应为 {s}')
            return 1
        if sum(grid[j][i] for j in range(n)) != s:
            print(f'第 {i+1} 列和不为 {s}')
            return 1
    d1 = sum(grid[i][i] for i in range(n))
    d2 = sum(grid[i][n - 1 - i] for i in range(n))
    if d1 != s or d2 != s:
        print(f'对角线和不等于 {s}（{d1}, {d2}）')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
