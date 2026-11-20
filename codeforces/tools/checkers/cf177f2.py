#!/usr/bin/env python3
"""CF177F2 Script Generation（满分档）的 checker。

用法：python3 cf177f2.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数；
  2. 独立重算：
     - k <= 16 时枚举全部 2^k 个边子集，逐条检查男女冲突后排序；
     - 否则用"优先队列 best-first"（与正文的分桶法不同的数据结构与顺序）逐个弹出，
       数到第 t 个为止；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import heapq
import sys


def recompute(n, k, t, edges):
    if k <= 16:
        values = []
        for mask in range(1 << k):
            men = women = total = 0
            ok = True
            m2 = mask
            j = 0
            while m2:
                if m2 & 1:
                    h, w, r = edges[j]
                    if (men >> h) & 1 or (women >> w) & 1:
                        ok = False
                        break
                    men |= 1 << h
                    women |= 1 << w
                    total += r
                m2 >>= 1
                j += 1
            if ok:
                values.append(total)
        values.sort()
        return values[t - 1] if 1 <= t <= len(values) else None

    by = [[] for _ in range(n + 1)]
    for h, w, r in edges:
        by[h + 1].append((w, r))
    heap = [(0, 0, 0)]
    cnt = 0
    while heap:
        weight, mask, last = heapq.heappop(heap)
        cnt += 1
        if cnt == t:
            return weight
        for man in range(last + 1, n + 1):
            for woman, r in by[man]:
                if not (mask >> woman) & 1:
                    heapq.heappush(heap, (weight + r, mask | (1 << woman), man))
    return None


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    p = 0
    n = int(data[p]); p += 1
    k = int(data[p]); p += 1
    t = int(data[p]); p += 1
    edges = []
    for _ in range(k):
        h = int(data[p]) - 1; w = int(data[p + 1]) - 1; r = int(data[p + 2])
        p += 3
        edges.append((h, w, r))

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1:
        print(f'输出应为 1 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = int(toks[0])
    except ValueError:
        print(f'输出不是整数: {toks[0]!r}')
        return 1

    expected = recompute(n, k, t, edges)
    if expected is None:
        print('checker 未能完成独立重算（t 越界或方案数不足）')
        return 1
    if got != expected:
        print(f'答案错误：独立重算 {expected}，实际 {got}')
        return 1

    try:
        ref = sys.stdin.read().split()
    except Exception:
        ref = []
    if ref and ref[0] != str(expected):
        print(f'与期望输出不一致：期望 {ref[0]}，独立重算 {expected}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
