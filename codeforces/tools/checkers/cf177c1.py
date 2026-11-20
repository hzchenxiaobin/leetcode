#!/usr/bin/env python3
"""CF177C1 Party 的 checker。

用法：python3 cf177c1.py <input> <output> <answer>

校验条件：
  1. 输出恰好一个整数，且 0 <= ans <= n；
  2. 该整数等于「并查集求朋友连通块 + 标记内部含讨厌边的块」独立重算的最大块大小；
  3. 若 stdin 给了期望答案，也要求一致。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    k = int(data[pos]); pos += 1
    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for _ in range(k):
        u = int(data[pos]) - 1
        v = int(data[pos + 1]) - 1
        pos += 2
        ru, rv = find(u), find(v)
        if ru != rv:
            if size[ru] < size[rv]:
                ru, rv = rv, ru
            parent[rv] = ru
            size[ru] += size[rv]
    m = int(data[pos]); pos += 1
    dislike = []
    for _ in range(m):
        u = int(data[pos]) - 1
        v = int(data[pos + 1]) - 1
        pos += 2
        dislike.append((u, v))
    bad = [False] * n
    for u, v in dislike:
        ru = find(u)
        if ru == find(v):
            bad[ru] = True
    expected = 0
    for i in range(n):
        r = find(i)
        if not bad[r]:
            expected = max(expected, size[r])

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
