#!/usr/bin/env python3
"""CF177B2 Rectangular Game 的 checker。

用法：python3 cf177b2.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数；
  2. 该整数等于按定义（每步取 n 的最大真约数）独立模拟出的最大和；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def greedy(n: int) -> int:
    ans = n
    while n > 1:
        p = n
        d = 2
        while d * d <= n:
            if n % d == 0:
                p = d
                break
            d += 1
        n //= p
        ans += n
    return ans


def main() -> int:
    n = int(open(sys.argv[1], encoding='utf-8').read().split()[0])
    expected = greedy(n)

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1:
        print(f'输出应为 1 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = int(toks[0])
    except ValueError:
        print(f'输出不是整数: {toks[0]!r}')
        return 1
    if got != expected:
        print(f'答案错误：期望 {expected}，实际 {got}')
        return 1
    ref = sys.stdin.read().split()
    if ref and int(ref[0]) != got:
        print(f'与题面答案不一致：答案 {ref[0]}，输出 {got}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
