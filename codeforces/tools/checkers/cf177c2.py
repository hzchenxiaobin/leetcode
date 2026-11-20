#!/usr/bin/env python3
"""CF177C2 Party 的 checker。

用法：python3 cf177c2.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数，且 0 <= ans <= n；
  2. 该整数等于用「BFS 求连通块 + 逐条讨厌边标记」独立重算的最大块大小；
     n <= 18 时改用 2^n 全枚举（按题面三个条件逐条检查）交叉确认；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def bfs_answer(n, friends, dislikes):
    adj = [[] for _ in range(n)]
    for u, v in friends:
        adj[u].append(v)
        adj[v].append(u)
    comp = [-1] * n
    sizes = []
    for s in range(n):
        if comp[s] != -1:
            continue
        cid = len(sizes)
        cnt = 0
        stack = [s]
        comp[s] = cid
        while stack:
            u = stack.pop()
            cnt += 1
            for v in adj[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        sizes.append(cnt)
    bad = [False] * len(sizes)
    for u, v in dislikes:
        if comp[u] == comp[v]:
            bad[comp[u]] = True
    return max([sz for sz, b in zip(sizes, bad) if not b], default=0)


def subset_answer(n, friends, dislikes):
    adj = [[] for _ in range(n)]
    for u, v in friends:
        adj[u].append(v)
        adj[v].append(u)
    best = 0
    for mask in range(1, 1 << n):
        ok = True
        for u, v in friends:
            if ((mask >> u) & 1) != ((mask >> v) & 1):
                ok = False
                break
        if not ok:
            continue
        for u, v in dislikes:
            if ((mask >> u) & 1) and ((mask >> v) & 1):
                ok = False
                break
        if not ok:
            continue
        s = (mask & -mask).bit_length() - 1
        seen, stack = 1 << s, [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if ((mask >> v) & 1) and not ((seen >> v) & 1):
                    seen |= 1 << v
                    stack.append(v)
        if seen == mask:
            best = max(best, bin(mask).count('1'))
    return best


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    k = int(data[pos]); pos += 1
    friends = []
    for _ in range(k):
        friends.append((int(data[pos]) - 1, int(data[pos + 1]) - 1))
        pos += 2
    m = int(data[pos]); pos += 1
    dislikes = []
    for _ in range(m):
        dislikes.append((int(data[pos]) - 1, int(data[pos + 1]) - 1))
        pos += 2
    expected = bfs_answer(n, friends, dislikes)
    if n <= 18:
        alt = subset_answer(n, friends, dislikes)
        if alt != expected:
            print(f'checker 内部不一致: BFS={expected}, 枚举={alt}')
            return 1

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != 1:
        print(f'输出应为 1 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = int(toks[0])
    except ValueError:
        print(f'输出不是整数: {toks[0]!r}')
        return 1
    if not 0 <= got <= n:
        print(f'答案越界: {got} 不在 [0, {n}]')
        return 1
    if got != expected:
        print(f'答案错误：期望 {expected}，实际 {got}')
        return 1
    ref = sys.stdin.read().split()
    if ref and int(ref[0]) != got:
        print(f'与题面答案不一致：答案 {ref[0]}，输出 {got}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
