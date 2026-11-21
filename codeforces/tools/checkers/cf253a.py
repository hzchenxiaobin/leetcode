#!/usr/bin/env python3
"""CF253A Boys and Girls 的 checker（多解）。

校验条件：
  1. 输出恰好一行，只含 'B' 与 'G'；
  2. 'B' 的个数等于 n，'G' 的个数等于 m；
  3. 相邻不同的对数达到理论上界 min(n+m-1, 2*min(n,m))（交替排法可达）。

用法: python3 cf253a.py <input> <output> <answer>
"""
import sys


def main():
    inp = open(sys.argv[1], encoding='utf-8').read().split()
    n, m = int(inp[0]), int(inp[1])
    out = open(sys.argv[2], encoding='utf-8').read().strip()
    if '\n' in out:
        print('WA: 输出不止一行')
        return 1
    if len(out) != n + m:
        print('WA: 输出长度 %d，应为 %d' % (len(out), n + m))
        return 1
    if out.count('B') != n or out.count('G') != m:
        print('WA: B/G 个数不对（%d/%d，应为 %d/%d）' % (out.count('B'), out.count('G'), n, m))
        return 1
    if set(out) - {'B', 'G'}:
        print('WA: 出现非法字符')
        return 1
    got = sum(1 for i in range(len(out) - 1) if out[i] != out[i + 1])
    best = min(n + m - 1, 2 * min(n, m))
    if got != best:
        print('WA: 相邻不同对数 %d，最优为 %d' % (got, best))
        return 1
    return 0


sys.exit(main())
