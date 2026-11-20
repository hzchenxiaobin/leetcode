#!/usr/bin/env python3
"""29D checker：校验路线合法（长度、相邻、每条边恰好两次、叶子访问顺序），并核对 -1 是否真的无解。"""
import sys


def read_case(path):
    data = list(map(int, open(path).read().split()))
    n = data[0]
    edges = []
    p = 1
    for _ in range(n - 1):
        edges.append((data[p], data[p + 1]))
        p += 2
    order = data[p:]
    return n, edges, order


def feasible(n, edges, order):
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    leaves = [v for v in range(2, n + 1) if len(adj[v]) == 1]
    if len(order) != len(leaves) or sorted(order) != sorted(leaves):
        return False
    rank = {v: i for i, v in enumerate(order)}
    parent = [0] * (n + 1)
    parent[1] = -1
    bfs = [1]
    for v in bfs:
        for u in adj[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            bfs.append(u)
    INF = 10 ** 9
    mn = [INF] * (n + 1)
    mx = [-1] * (n + 1)
    cnt = [0] * (n + 1)
    for v in reversed(bfs):
        if v != 1 and len(adj[v]) == 1:
            mn[v] = mx[v] = rank[v]
            cnt[v] = 1
        for u in adj[v]:
            if parent[u] != v:
                continue
            mn[v] = min(mn[v], mn[u])
            mx[v] = max(mx[v], mx[u])
            cnt[v] += cnt[u]
        if cnt[v] > 0 and mx[v] - mn[v] + 1 != cnt[v]:
            return False
    return True


def main():
    if len(sys.argv) < 3:
        print("usage: chk.py input output")
        return 2
    n, edges, order = read_case(sys.argv[1])
    tokens = open(sys.argv[2]).read().split()
    if not tokens:
        print("FAIL: empty output")
        return 1
    if tokens[0] == "-1":
        if len(tokens) != 1:
            print("FAIL: -1 with extra tokens")
            return 1
        if feasible(n, edges, order):
            print("FAIL: -1 but a route exists")
            return 1
        return 0

    try:
        route = list(map(int, tokens))
    except ValueError:
        print("FAIL: non-integer in route")
        return 1

    if len(route) != 2 * n - 1:
        print(f"FAIL: route length {len(route)} != {2*n-1}")
        return 1
    if route[0] != 1 or route[-1] != 1:
        print("FAIL: route must start and end at root 1")
        return 1

    eset = set()
    for a, b in edges:
        eset.add((a, b))
        eset.add((b, a))
    used = {}
    for i in range(len(route) - 1):
        a, b = route[i], route[i + 1]
        if (a, b) not in eset:
            print(f"FAIL: step {i}: {a}->{b} is not an edge")
            return 1
        used[(a, b)] = used.get((a, b), 0) + 1
    for a, b in edges:
        if used.get((a, b), 0) + used.get((b, a), 0) != 2:
            print(f"FAIL: edge {a}-{b} used {used.get((a,b),0)+used.get((b,a),0)} times, need 2")
            return 1

    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    leaves = {v for v in range(2, n + 1) if len(adj[v]) == 1}
    seen = [v for v in route if v in leaves]
    if seen != order:
        print(f"FAIL: leaf visit order {seen} != {order}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
