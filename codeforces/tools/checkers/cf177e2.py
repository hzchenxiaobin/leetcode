#!/usr/bin/env python3
"""CF177E2 Space Voyage（满分档）的 checker。

用法：python3 cf177e2.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数；
  2. 该整数等于"不截断、纯大整数"的独立重算：先判全部 a_i=0 的无穷分支，
     再用两次二分求 {x : D(x)=c} 的左端点与右端点，返回区间长度；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def recompute(data):
    p = 0
    n = int(data[p]); p += 1
    c = int(data[p]); p += 1
    a, b = [], []
    for _ in range(n):
        a.append(int(data[p])); b.append(int(data[p + 1])); p += 2

    if all(v == 0 for v in a):
        return -1 if c == n else 0

    def days(x):
        return n + sum(a[i] * x // b[i] for i in range(n))

    def first_at_least(target):
        hi = 1
        while days(hi) < target:
            hi *= 2
        lo = 1
        while lo < hi:
            mid = (lo + hi) // 2
            if days(mid) >= target:
                hi = mid
            else:
                lo = mid + 1
        return lo

    left = first_at_least(c)
    if days(left) != c:
        return 0
    return first_at_least(c + 1) - left


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1:
        print(f'输出应为 1 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = int(toks[0])
    except ValueError:
        print(f'输出不是整数: {toks[0]!r}')
        return 1

    expected = recompute(data)
    if got != expected:
        print(f'答案错误：独立重算 {expected}，实际 {got}')
        return 1

    try:
        ref = sys.stdin.read().split()
    except Exception:
        ref = []
    if ref and ref[0] != str(expected):
        print(f'与期望输出不一致：期望 {ref[0]}，独立重算 {expected}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
