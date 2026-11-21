#!/usr/bin/env python3
"""237B Young Table 的构造 checker。

用法: python3 cf237b.py <input> <output> [answer]
answer 参数被忽略（本题多解），只校验输出本身是否合法。

校验条件：
  1. 输出第一行只有一个整数 m，0 <= m <= s（s 为总格数）；
  2. 随后恰好 m 行、每行 4 个整数 x y p q，且 1 <= x,p <= n、1 <= y <= c[x]、1 <= q <= c[p]；
  3. 每次操作交换的是两个**不同**的格子；
  4. 依次执行后，表内仍是 1..s 的一个排列（交换保持多重集，这里防御性地再查一次）；
  5. 最终对每个 i>1 有 a[i][j] > a[i-1][j]，对每个 j>1 有 a[i][j] > a[i][j-1]。
通过返回 0，否则返回 1。
"""
import sys


def main():
    tok = open(sys.argv[1]).read().split()
    if not tok:
        sys.exit(1)
    p = 0
    n = int(tok[p]); p += 1
    c = [0] * (n + 1)
    s = 0
    for i in range(1, n + 1):
        c[i] = int(tok[p]); p += 1
        s += c[i]
    a = [None] * (n + 1)
    for i in range(1, n + 1):
        a[i] = [0] * (c[i] + 1)
        for j in range(1, c[i] + 1):
            a[i][j] = int(tok[p]); p += 1
    if p != len(tok):
        sys.exit(1)

    out = open(sys.argv[2]).read().split()
    if not out:
        sys.exit(1)
    q = 0
    m = int(out[q]); q += 1
    if not (0 <= m <= s):
        sys.exit(1)
    if len(out) - q != 4 * m:
        sys.exit(1)
    for _ in range(m):
        x = int(out[q]); y = int(out[q + 1]); u = int(out[q + 2]); v = int(out[q + 3])
        q += 4
        if not (1 <= x <= n and 1 <= u <= n):
            sys.exit(1)
        if not (1 <= y <= c[x] and 1 <= v <= c[u]):
            sys.exit(1)
        if x == u and y == v:
            sys.exit(1)
        a[x][y], a[u][v] = a[u][v], a[x][y]

    seen = set()
    for i in range(1, n + 1):
        for j in range(1, c[i] + 1):
            if not (1 <= a[i][j] <= s) or a[i][j] in seen:
                sys.exit(1)
            seen.add(a[i][j])
    if len(seen) != s:
        sys.exit(1)

    for i in range(1, n + 1):
        for j in range(1, c[i] + 1):
            if i > 1 and not a[i][j] > a[i - 1][j]:
                sys.exit(1)
            if j > 1 and not a[i][j] > a[i][j - 1]:
                sys.exit(1)
    sys.exit(0)


main()
