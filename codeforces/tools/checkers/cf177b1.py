#!/usr/bin/env python3
"""CF177B1 Rectangular Game 的 checker。

用法：python3 cf177b1.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数；
  2. 该整数等于「在 n 的所有约数上做 DP」独立重算的最大和（n 较大时改用贪心分解，
     避免 n ≤ 10^9 时枚举 1..n）；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def brute_divisor_dp(n: int) -> int:
    divs = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            divs.append(d)
            if d != n // d:
                divs.append(n // d)
        d += 1
    divs.sort()
    f = {}
    for x in divs:
        sub = 0
        for e in divs:
            if e >= x:
                break
            if x % e == 0 and f[e] > sub:
                sub = f[e]
        f[x] = x + sub
    return f[n]


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
    expected = brute_divisor_dp(n) if n <= 10 ** 7 else greedy(n)

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
