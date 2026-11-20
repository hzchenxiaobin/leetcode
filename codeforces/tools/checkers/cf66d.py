#!/usr/bin/env python3
"""66D 构造题 checker：python3 checker.py <input> <output> <answer>
校验：n=2 必须输出 -1；n>=3 必须给出 n 个互不相同、<=100 位、无前导零的正整数，
两两 gcd>1，且整体 gcd=1。"""
import sys
from math import gcd

inp = open(sys.argv[1]).read().split()
out = open(sys.argv[2]).read().split()
n = int(inp[0])

if out == ["-1"]:
    sys.exit(0 if n == 2 else 1)      # n=2 无解；n>=3 一定可构造

if n == 2:
    sys.exit(1)                       # n=2 不可能有合法答案
if len(out) != n:
    sys.exit(1)
vals = []
for tok in out:
    if not tok.isdigit():
        sys.exit(1)
    if len(tok) > 100 or (len(tok) > 1 and tok[0] == "0"):
        sys.exit(1)
    vals.append(int(tok))
if len(set(vals)) != n:
    sys.exit(1)
g = 0
for v in vals:
    g = gcd(g, v)
if g != 1:
    sys.exit(1)
for i in range(n):
    for j in range(i + 1, n):
        if gcd(vals[i], vals[j]) == 1:
            sys.exit(1)
sys.exit(0)
