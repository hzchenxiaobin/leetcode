#!/usr/bin/env python3
"""CF123A Prime Permutation 的答案校验器（答案不唯一）。

用法: python3 cf123a.py <input> <output> [expected]

输入：一行小写字母串 s（|s| = n）。
输出：要么单独一行 NO，要么第一行 YES + 第二行重排后的串 t。

校验条件：
  1. 判 NO 时，必须确实无解。无解的充要条件：设 C 为"必须相等的那些位置"
     （某个素数 p <= n/2 的倍数），当且仅当某个字符出现次数 >= |C| 时有解，
     所以 NO 要求 maxfreq < |C|；
  2. 判 YES 时，t 必须是 s 的重排（多重集合相同），且满足题面全部约束：
     对每个素数 p <= n 与每个 i in [1, n//p]，都有 t[p] == t[p*i]（1-indexed）。
"""
import sys


def primes_upto(n):
    isp = [True] * (n + 1)
    if n >= 0:
        isp[0] = False
    if n >= 1:
        isp[1] = False
    i = 2
    while i * i <= n:
        if isp[i]:
            for j in range(i * i, n + 1, i):
                isp[j] = False
        i += 1
    return [i for i in range(2, n + 1) if isp[i]]


def main() -> int:
    s = open(sys.argv[1]).read().split()[0]
    n = len(s)
    ps = primes_upto(n)
    need = [False] * (n + 1)
    for p in ps:
        if n // p >= 2:
            for x in range(p, n + 1, p):
                need[x] = True
    C = sum(need)
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    maxfreq = max(freq.values())

    out = open(sys.argv[2]).read().split()
    if not out:
        print("输出为空", file=sys.stderr)
        return 1
    if out[0] == "NO":
        if len(out) != 1:
            print("NO 之后不应有内容", file=sys.stderr)
            return 1
        if maxfreq >= C:
            print(f"有解（maxfreq={maxfreq} >= |C|={C}），不应输出 NO", file=sys.stderr)
            return 1
        return 0
    if out[0] != "YES":
        print(f"第一行应为 YES/NO，实际 {out[0]!r}", file=sys.stderr)
        return 1
    if len(out) != 2:
        print("YES 之后应恰好有一行串", file=sys.stderr)
        return 1
    t = out[1]
    if len(t) != n:
        print(f"长度 {len(t)} != {n}", file=sys.stderr)
        return 1
    if sorted(t) != sorted(s):
        print("t 不是 s 的重排", file=sys.stderr)
        return 1
    for p in ps:
        for i in range(1, n // p + 1):
            if t[p - 1] != t[p * i - 1]:
                print(f"约束失败：p={p}, i={i}, t[{p}]={t[p-1]} != t[{p*i}]={t[p*i-1]}",
                      file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
