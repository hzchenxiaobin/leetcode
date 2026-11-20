#!/usr/bin/env python3
"""CF177A1 Good Matrix Elements 的 checker。

用法（与 verify_solution.py 约定一致）：
    python3 cf177a1.py <input> <output> <answer>
`answer` 通过 /dev/stdin 传入（verify_solution.py 把期望输出喂到 stdin）。

校验条件：
  1. 输出恰好一个整数；
  2. 该整数等于按题面定义（四条线取并集、每格只算一次）独立重算的好元素之和；
  3. 若 stdin 给了期望答案，还要求与之一致。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    a = [[int(data[1 + i * n + j]) for j in range(n)] for i in range(n)]
    mid = n // 2
    good = set()
    for i in range(n):
        good.add((i, i))
        good.add((i, n - 1 - i))
        good.add((mid, i))
        good.add((i, mid))
    expected_sum = sum(a[i][j] for i, j in good)

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1:
        print(f'输出应为 1 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = int(toks[0])
    except ValueError:
        print(f'输出不是整数: {toks[0]!r}')
        return 1
    if got != expected_sum:
        print(f'答案错误：期望 {expected_sum}，实际 {got}')
        return 1
    ref = sys.stdin.read().split()
    if ref and int(ref[0]) != got:
        print(f'与题面答案不一致：答案 {ref[0]}，输出 {got}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
