#!/usr/bin/env python3
"""118E Bertown roads 的 checker（定向方案，任意合法即可）。

用法: python3 checker.py <input> <output> <answer>
校验：
  1. 输出 0：图中必须存在桥（即不存在强连通定向）；
  2. 否则：恰好 m 行，每行 (p,q) 且 {p,q} 与输入某条边一致（多重集相同），
     且定向后的有向图强连通（Kosaraju 独立验证）。
"""
import sys
from collections import deque


def main():
    inp = open(sys.argv[1]).read().split()
    n = int(inp[0]); m = int(inp[1])
    edges = []
    p = 2
    for _ in range(m):
        edges.append((int(inp[p]), int(inp[p+1]))); p += 2
    lines = [l.split() for l in open(sys.argv[2]).read().splitlines() if l.strip()]
    if not lines:
        sys.exit(1)
    if len(lines) == 1 and lines[0][0] == "0":
        # 判断是否存在桥：对每条边尝试删掉后 BFS
        adj = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(edges):
            adj[a].append((b, i)); adj[b].append((a, i))
        def connected(skip):
            seen = [False] * (n + 1); seen[1] = True
            q = deque([1]); cnt = 1
            while q:
                v = q.popleft()
                for u, i in adj[v]:
                    if i == skip or seen[u]:
                        continue
                    seen[u] = True; cnt += 1; q.append(u)
            return cnt == n
        has_bridge = any(not connected(i) for i in range(m))
        sys.exit(0 if has_bridge else 1)
    if len(lines) != m:
        sys.exit(1)
    # 校验边的多重集
    from collections import Counter
    want = Counter((min(a, b), max(a, b)) for a, b in edges)
    got = Counter()
    out_edges = []
    for pr in lines:
        if len(pr) != 2:
            sys.exit(1)
        a, b = int(pr[0]), int(pr[1])
        if not (1 <= a <= n and 1 <= b <= n) or a == b:
            sys.exit(1)
        got[(min(a, b), max(a, b))] += 1
        out_edges.append((a, b))
    if got != want:
        sys.exit(1)
    # 强连通：正向/反向 BFS
    g = [[] for _ in range(n + 1)]
    gr = [[] for _ in range(n + 1)]
    for a, b in out_edges:
        g[a].append(b); gr[b].append(a)
    def reach(adj):
        seen = [False] * (n + 1); seen[1] = True
        q = deque([1]); cnt = 1
        while q:
            v = q.popleft()
            for u in adj[v]:
                if not seen[u]:
                    seen[u] = True; cnt += 1; q.append(u)
        return cnt == n
    sys.exit(0 if (reach(g) and reach(gr)) else 1)


main()
