#!/usr/bin/env python3
"""CF269C Flawed Flow 的 checker（多解 / 特殊评测）。

用法：python3 cf269c.py <input> <output> <answer>
返回 0 表示通过。

校验条件（与题面一致）：
  1. 输出恰好 m 个 token，每个是 0 或 1；
  2. 对每个内部点 1<v<n：流入权和 == 流出权和；
  3. 1 号点没有入边；
  4. 定向后的图无环（Kahn 拓扑排序能删掉所有点）。
"""
import sys


def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = list(map(int, open(inp).read().split()))
    n, m = data[0], data[1]
    edges = []
    p = 2
    for _ in range(m):
        a, b, c = data[p], data[p + 1], data[p + 2]
        p += 3
        edges.append((a, b, c))
    toks = open(out).read().split()
    if len(toks) != m:
        print(f'CHECKER FAIL: 需要 {m} 个方向，实际 {len(toks)}')
        return 1
    if any(t not in ('0', '1') for t in toks):
        print('CHECKER FAIL: 方向只能是 0/1')
        return 1
    d = [int(t) for t in toks]
    insum = [0] * (n + 1)
    outsum = [0] * (n + 1)
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for (a, b, c), x in zip(edges, d):
        u, v = (a, b) if x == 0 else (b, a)
        outsum[u] += c
        insum[v] += c
        g[u].append(v)
        indeg[v] += 1
    if insum[1] != 0:
        print(f'CHECKER FAIL: 1 号点有入边 {insum[1]}')
        return 1
    for v in range(2, n):
        if insum[v] != outsum[v]:
            print(f'CHECKER FAIL: {v} 号点不守恒 in={insum[v]} out={outsum[v]}')
            return 1
    # 无环
    from collections import deque
    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    seen = 0
    while q:
        v = q.popleft()
        seen += 1
        for u in g[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                q.append(u)
    if seen != n:
        print('CHECKER FAIL: 定向后的图有环')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
