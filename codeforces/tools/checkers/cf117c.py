#!/usr/bin/env python3
"""117C Cycle 的 checker（输出任意三元环）。

用法: python3 checker.py <input> <output> <answer>
校验：输出若为 -1，则竞赛图必须无三元环（用"传递竞赛图 ⟺ 出度为 0..n-1"
的判据独立验证）；否则输出三个互不相同的顶点，且两两按顺序成环。
"""
import sys


def main():
    inp = open(sys.argv[1]).read().split()
    n = int(inp[0])
    A = inp[1:1 + n]
    out = open(sys.argv[2]).read().split()
    if not out:
        sys.exit(1)
    if out[0] == "-1":
        deg = sorted(sum(1 for ch in A[i] if ch == '1') for i in range(n))
        ok = all(deg[i] == i for i in range(n))     # 传递竞赛图出度为 0..n-1
        sys.exit(0 if ok else 1)
    if len(out) < 3:
        sys.exit(1)
    try:
        a, b, c = int(out[0]), int(out[1]), int(out[2])
    except ValueError:
        sys.exit(1)
    if len({a, b, c}) != 3 or not all(1 <= x <= n for x in (a, b, c)):
        sys.exit(1)
    ok = A[a-1][b-1] == '1' and A[b-1][c-1] == '1' and A[c-1][a-1] == '1'
    sys.exit(0 if ok else 1)


main()
