#!/usr/bin/env python3
"""CF177A2 Good Matrix Elements 的 checker。

用法：python3 cf177a2.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数；
  2. 与「逐格判定 i==j / i+j==n-1 / i==mid / j==mid」独立重算的和一致；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    a = [[int(data[1 + i * n + j]) for j in range(n)] for i in range(n)]
    mid = n // 2
    total = 0
    for i in range(n):
        for j in range(n):
            if i == j or i + j == n - 1 or i == mid or j == mid:
                total += a[i][j]

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1:
        print(f'输出应为 1 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = int(toks[0])
    except ValueError:
        print(f'输出不是整数: {toks[0]!r}')
        return 1
    if got != total:
        print(f'答案错误：期望 {total}，实际 {got}')
        return 1
    ref = sys.stdin.read().split()
    if ref and int(ref[0]) != got:
        print(f'与题面答案不一致：答案 {ref[0]}，输出 {got}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
