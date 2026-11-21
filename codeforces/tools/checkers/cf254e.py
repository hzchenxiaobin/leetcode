#!/usr/bin/env python3
"""CF254E Dormitory 的 checker（多解）。

校验条件：
  1. 第一行的评级等于最优值（用"逐日枚举全部在场朋友子集"的独立暴力算出）；
  2. 接下来 n 行：每行先给个数 cnt，再给 cnt 个朋友下标（互不相同、当天在场）；
  3. 整个方案在食物上可行：每天可用食物 = 昨天的剩余（≤ 昨天的 a）+ 今天的 a，
     必须 ≥ v + 当天喂出去的总量；剩余只能是最新一天食物的一部分。

用法: python3 cf254e.py <input> <output> <answer>
"""
import sys
from functools import lru_cache


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    pos = 0
    n, v = int(data[pos]), int(data[pos + 1]); pos += 2
    a = [0] + [int(x) for x in data[pos:pos + n]]; pos += n
    m = int(data[pos]); pos += 1
    L, R, F = [], [], []
    for _ in range(m):
        L.append(int(data[pos])); R.append(int(data[pos + 1])); F.append(int(data[pos + 2])); pos += 3
    present = [[] for _ in range(n + 1)]
    for j in range(m):
        for i in range(L[j], R[j] + 1):
            present[i].append(j)

    # 独立暴力：逐日枚举全部在场朋友子集（不是"取最便宜的前缀"）
    from functools import lru_cache
    sys.setrecursionlimit(10000)

    @lru_cache(maxsize=None)
    def best(i, carry):
        if i > n:
            return 0
        avail = carry + a[i]
        if avail < v:
            return -10 ** 9
        budget = avail - v
        res = -10 ** 9
        ps = present[i]
        for mask in range(1 << len(ps)):
            spend = sum(F[ps[k]] for k in range(len(ps)) if mask >> k & 1)
            if spend > budget:
                continue
            nc = min(a[i], budget - spend)
            res = max(res, bin(mask).count('1') + best(i + 1, nc))
        return res

    opt = best(1, 0)
    out = open(sys.argv[2], encoding='utf-8').read().split('\n')
    out = [l for l in out]
    while out and not out[-1].strip():
        out.pop()
    if len(out) != n + 1:
        print('WA: 输出应为 1 + n 行，实际 %d 行' % len(out))
        return 1
    got = int(out[0].split()[0])
    if got != opt:
        print('WA: 评级 %d，最优 %d' % (got, opt))
        return 1
    carry = 0
    total = 0
    for i in range(1, n + 1):
        nums = [int(x) for x in out[i].split()]
        if not nums:
            print('WA: 第 %d 天缺少计数' % i)
            return 1
        cnt = nums[0]
        ids = nums[1:]
        if cnt != len(ids):
            print('WA: 第 %d 天计数与实际不符' % i)
            return 1
        if len(set(ids)) != len(ids):
            print('WA: 第 %d 天重复喂同一个朋友' % i)
            return 1
        spend = 0
        for j in ids:
            if not (1 <= j <= m):
                print('WA: 朋友下标越界')
                return 1
            j -= 1
            if not (L[j] <= i <= R[j]):
                print('WA: 第 %d 天喂了不在场的朋友 %d' % (i, j + 1))
                return 1
            spend += F[j]
        avail = carry + a[i]
        if avail - spend < v:
            print('WA: 第 %d 天食物不够（可用 %d，喂出 %d，需自己吃 %d）' % (i, avail, spend, v))
            return 1
        carry = min(a[i], avail - spend - v)
        total += cnt
    if total != got:
        print('WA: 评级与日程总数不符')
        return 1
    return 0


sys.exit(main())
