#!/usr/bin/env python3
"""CF177E1 Space Voyage（30 分档）的 checker。

用法（与 verify_solution.py 约定一致）：
    python3 cf177e1.py <input> <output> <answer>
`answer` 通过 /dev/stdin 传入（verify_solution.py 把期望输出喂到 stdin）。

校验条件：
  1. 输出恰好一个整数；
  2. 该整数等于"逐天模拟发礼物"的独立暴力结果（不使用 floor(a_i*x/b_i) 公式，
     而是真的循环减 b_i 数天数），枚举范围用 x <= b_max*(c+1)+2 的严格上界；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def recompute(n, c, a, b):
    if all(v == 0 for v in a):
        return -1 if c == n else 0
    bmax = max(b)
    limit = bmax * (c + 1) + 2
    if limit > 5000000:
        # 兜底（正常不该走到）：E1 的 30 分档里 limit <= 10102，
        # 若被误用于满分档数据，改用公式 + 二分，避免 checker 自身跑不完。
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

    ans = 0
    x = 1
    while x <= limit:
        total = 0
        for i in range(n):
            presents = a[i] * x
            days = 1
            while presents >= b[i]:
                presents -= b[i]
                days += 1
            total += days
            if total > c:
                break
        if total == c:
            ans += 1
        if total > c:
            break
        x += 1
    return ans


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    p = 0
    n = int(data[p]); p += 1
    c = int(data[p]); p += 1
    a, b = [], []
    for _ in range(n):
        a.append(int(data[p])); b.append(int(data[p + 1])); p += 2

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1:
        print(f'输出应为 1 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = int(toks[0])
    except ValueError:
        print(f'输出不是整数: {toks[0]!r}')
        return 1

    expected = recompute(n, c, a, b)
    if got != expected:
        print(f'答案错误：独立暴力给出 {expected}，实际 {got}')
        return 1

    try:
        ref = sys.stdin.read().split()
    except Exception:
        ref = []
    if ref and ref[0] != str(expected):
        print(f'与期望输出不一致：期望 {ref[0]}，独立暴力 {expected}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
