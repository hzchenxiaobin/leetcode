#!/usr/bin/env python3
"""CF254A Cards with Numbers 的 checker（多解）。

校验条件：
  1. 若存在某个值出现奇数次，输出必须是 -1；
  2. 否则恰好 n 行，每行两个 1..2n 的下标，互不相同、覆盖全部 2n 张牌，
     且每对的两张牌数值相同。

用法: python3 cf254a.py <input> <output> <answer>
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + 2 * n]]
    out = open(sys.argv[2], encoding='utf-8').read().split()
    cnt = {}
    for v in a:
        cnt[v] = cnt.get(v, 0) + 1
    possible = all(c % 2 == 0 for c in cnt.values())
    if out == ['-1']:
        if possible:
            print('WA: 可以配对，却输出了 -1')
            return 1
        return 0
    if not possible:
        print('WA: 无解却给出了配对')
        return 1
    if len(out) != 2 * n:
        print('WA: 输出应有 2n 个整数，实际 %d 个' % len(out))
        return 1
    seen = [False] * (2 * n + 1)
    for k in range(n):
        u, v = int(out[2 * k]), int(out[2 * k + 1])
        if not (1 <= u <= 2 * n and 1 <= v <= 2 * n) or u == v:
            print('WA: 下标非法（%d,%d）' % (u, v))
            return 1
        if seen[u] or seen[v]:
            print('WA: 下标重复使用')
            return 1
        seen[u] = seen[v] = True
        if a[u - 1] != a[v - 1]:
            print('WA: 第 %d 对的数值不相同' % (k + 1))
            return 1
    if not all(seen[1:]):
        print('WA: 没有覆盖全部 2n 张牌')
        return 1
    return 0


sys.exit(main())
