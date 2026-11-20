#!/usr/bin/env python3
"""CF177F1 Script Generation（30 分档）的 checker。

用法：python3 cf177f1.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数；
  2. 该整数等于"枚举边子集并逐条检查男女冲突"的独立结果（k <= 20 时）
     或"按男人 DFS 枚举全部匹配"的结果（k 更大时），排序后取第 t 个；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def recompute(n, k, t, edges):
    values = []
    if k <= 20:
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
    else:
        by = [[] for _ in range(n)]
        for h, w, r in edges:
            by[h].append((w, r))

        def dfs(i, used, total):
            if i == n:
                values.append(total)
                return
            dfs(i + 1, used, total)
            for w, r in by[i]:
                if not (used >> w) & 1:
                    dfs(i + 1, used | (1 << w), total + r)

        dfs(0, 0, 0)
    values.sort()
    if t < 1 or t > len(values):
        return None
    return values[t - 1]


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
        print('checker 侧发现 t 超出可接受方案总数（题面保证不会发生）')
        return 1
    if got != expected:
        print(f'答案错误：独立枚举给出 {expected}，实际 {got}')
        return 1

    try:
        ref = sys.stdin.read().split()
    except Exception:
        ref = []
    if ref and ref[0] != str(expected):
        print(f'与期望输出不一致：期望 {ref[0]}，独立枚举 {expected}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
