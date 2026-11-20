#!/usr/bin/env python3
"""CF144E Competition 的 checker（多解/构造题）。

校验条件：
1. 第一行是选出的人数 k，要求 0 <= k <= m；
2. k > 0 时第二行恰好给出 k 个互不相同的 1..m 编号（k = 0 时可以不写第二行）；
3. 这 k 个人确实能同时参赛：第 i 个人能停靠的对角格是区间 [b_i, a_i]，其中
   a_i = r_i、b_i = n + 1 - c_i；同一 d = a_i - b_i 组内必须"a 递增对应 p 递增"。
   按 a 全局递增、每次取不小于 b 的最小空闲对角格，若人人都能分到 p <= a，
   则该集合可行，否则不可行（这是区间匹配的经典贪心，见题解引理）。

用法：python3 cf144e.py <input> <output> [answer]
"""

import sys


def main() -> int:
    if len(sys.argv) < 3:
        return 2
    data = open(sys.argv[1]).read().split()
    if len(data) < 2:
        return 1
    n, m = int(data[0]), int(data[1])
    if len(data) < 2 + 2 * m:
        return 1
    a = [0] * m
    b = [0] * m
    for i in range(m):
        r = int(data[2 + 2 * i])
        c = int(data[3 + 2 * i])
        if not (1 <= r <= n and 1 <= c <= n and r + c > n):
            return 1
        a[i] = r
        b[i] = n + 1 - c

    try:
        toks = open(sys.argv[2]).read().split()
    except OSError:
        return 1
    if not toks:
        return 1
    try:
        k = int(toks[0])
    except ValueError:
        return 1
    if k < 0 or k > m:
        return 1
    if len(toks) - 1 != k:
        return 1
    try:
        idx = [int(x) for x in toks[1:]]
    except ValueError:
        return 1
    if len(set(idx)) != k:
        return 1
    for i in idx:
        if i < 1 or i > m:
            return 1

    sub = sorted((i - 1 for i in idx), key=lambda i: (a[i], b[i]))

    # 并查集跳跃指针：nxt[p] = 不小于 p 的最小空闲对角格
    nxt = list(range(n + 2))

    def find(x: int) -> int:
        root = x
        while nxt[root] != root:
            root = nxt[root]
        while nxt[x] != root:
            nxt[x], x = root, nxt[x]
        return root

    for i in sub:
        p = find(b[i])
        if p > a[i]:
            return 1
        nxt[p] = find(p + 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
