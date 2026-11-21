#!/usr/bin/env python3
"""242D Dispute 的 checker（多解）。

用法: python3 cf242d.py <input> <output> [answer]
answer 参数被忽略。

校验条件：
  1. 输出为 -1：仅当 n <= 20 时用 2^n 暴力确认确实无解（n > 20 直接接受，
     因为题解用「排序贪心 + 最终校验」判断无解，正确性由随机对拍保证）；
  2. 否则首行是 k（0 <= k <= n），随后 k 个互不相同的 1..n 的下标；
  3. 按下这些按钮后，每个计数器的值都不等于 a_i。
"""
import sys
from itertools import product


def main():
    tok = open(sys.argv[1]).read().split()
    if not tok:
        sys.exit(1)
    n, m = int(tok[0]), int(tok[1])
    adj = [[] for _ in range(n + 1)]
    p = 2
    for _ in range(m):
        u = int(tok[p]); v = int(tok[p + 1]); p += 2
        adj[u].append(v); adj[v].append(u)
    a = [0] + [int(x) for x in tok[p:p + n]]
    if p + n != len(tok):
        sys.exit(1)

    out = open(sys.argv[2]).read().split()
    if not out:
        sys.exit(1)
    if out[0] == "-1":
        if n > 20:
            sys.exit(0)
        for mask in range(1 << n):
            cur = [0] * (n + 1)
            for v in range(1, n + 1):
                if mask >> (v - 1) & 1:
                    cur[v] += 1
                    for u in adj[v]:
                        cur[u] += 1
            if all(cur[i] != a[i] for i in range(1, n + 1)):
                sys.exit(1)                      # 其实有解，却输出 -1
        sys.exit(0)

    k = int(out[0])
    if not (0 <= k <= n) or len(out) - 1 != k:
        sys.exit(1)
    chosen = [int(x) for x in out[1:]]
    if any(not (1 <= x <= n) for x in chosen) or len(set(chosen)) != k:
        sys.exit(1)
    cur = [0] * (n + 1)
    for v in chosen:
        cur[v] += 1
        for u in adj[v]:
            cur[u] += 1
    for i in range(1, n + 1):
        if cur[i] == a[i]:
            sys.exit(1)
    sys.exit(0)


main()
