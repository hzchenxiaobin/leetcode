#!/usr/bin/env python3
"""237D T-decomposition 的构造 checker。

用法: python3 cf237d.py <input> <output> [answer]
answer 参数被忽略（本题多解），只校验输出本身。

校验条件：
  1. 输出可解析：m；然后 m 组「k_i + k_i 个互不相同的点」；然后 m-1 对 t 的边；
  2. 每个集合非空、元素互异且都在 [1, n]，全部集合的并集等于 V；
  3. t 是以这 m 个集合为结点的一棵树：m-1 条边、无自环、无重边、连通；
  4. s 的每条边 (a,b) 都有某个集合同时包含 a、b；
  5. 对每个点 a，所有包含 a 的集合在 t 中诱导的子图连通；
  6. 最优性：最大集合大小 w == 2（n >= 2 时 w >= 2），且 m == n-1
     （w = 2 时每个集合至多覆盖一条 s 的边，故 m >= n-1）。
通过返回 0，否则返回 1。
"""
import sys


def main():
    tok = open(sys.argv[1]).read().split()
    if not tok:
        sys.exit(1)
    p = 0
    n = int(tok[p]); p += 1
    edges = []
    for _ in range(n - 1):
        u = int(tok[p]); v = int(tok[p + 1]); p += 2
        edges.append((u, v))
    if p != len(tok):
        sys.exit(1)

    out = open(sys.argv[2]).read().split()
    if not out:
        sys.exit(1)
    q = 0
    m = int(out[q]); q += 1
    if m < 1:
        sys.exit(1)
    sets = []
    for _ in range(m):
        if q >= len(out):
            sys.exit(1)
        k = int(out[q]); q += 1
        if k < 1 or q + k > len(out):
            sys.exit(1)
        cur = [int(x) for x in out[q:q + k]]
        q += k
        if any(not (1 <= x <= n) for x in cur):
            sys.exit(1)
        if len(set(cur)) != k:
            sys.exit(1)
        sets.append(cur)
    if len(out) - q != 2 * (m - 1):
        sys.exit(1)
    tadj = [[] for _ in range(m)]
    seen_pairs = set()
    for _ in range(m - 1):
        a = int(out[q]) - 1; b = int(out[q + 1]) - 1; q += 2
        if not (0 <= a < m and 0 <= b < m) or a == b:
            sys.exit(1)
        key = (min(a, b), max(a, b))
        if key in seen_pairs:
            sys.exit(1)
        seen_pairs.add(key)
        tadj[a].append(b)
        tadj[b].append(a)

    # 2. 覆盖
    union = set()
    for s in sets:
        union.update(s)
    if union != set(range(1, n + 1)):
        sys.exit(1)

    # 3. 树
    if m > 1:
        vis = [False] * m
        stack = [0]
        vis[0] = True
        cnt = 0
        while stack:
            u = stack.pop()
            cnt += 1
            for w in tadj[u]:
                if not vis[w]:
                    vis[w] = True
                    stack.append(w)
        if cnt != m:
            sys.exit(1)

    # 4. 覆盖所有原树边
    contain = [set() for _ in range(n + 1)]
    for idx, s in enumerate(sets):
        for x in s:
            contain[x].add(idx)
    for a, b in edges:
        if not (contain[a] & contain[b]):
            sys.exit(1)

    # 5. 每个点对应的集合在 t 中连通
    for a in range(1, n + 1):
        nodes = contain[a]
        start = next(iter(nodes))
        visn = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for w in tadj[u]:
                if w in nodes and w not in visn:
                    visn.add(w)
                    stack.append(w)
        if len(visn) != len(nodes):
            sys.exit(1)

    # 6. 最优性
    w = max(len(s) for s in sets)
    if w != 2 or m != n - 1:
        sys.exit(1)
    sys.exit(0)


main()
