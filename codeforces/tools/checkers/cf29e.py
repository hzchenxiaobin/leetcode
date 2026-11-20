#!/usr/bin/env python3
"""29E checker：校验两条路线合法，并用独立 BFS 核对最短路长度 k。"""
import sys
from collections import deque


def read_case(path):
    data = list(map(int, open(path).read().split()))
    n, m = data[0], data[1]
    adj = [[] for _ in range(n)]
    p = 2
    for _ in range(m):
        a, b = data[p] - 1, data[p + 1] - 1
        p += 2
        adj[a].append(b)
        adj[b].append(a)
    return n, m, adj


def min_len(n, adj):
    start = (0, n - 1)
    goal = (n - 1, 0)
    dist = {start: 0}
    q = deque([start])
    while q:
        u, v = q.popleft()
        if (u, v) == goal:
            return dist[(u, v)]
        d = dist[(u, v)] + 1
        for nu in adj[u]:
            for nv in adj[v]:
                if nu == nv:
                    continue
                st = (nu, nv)
                if st not in dist:
                    dist[st] = d
                    q.append(st)
    return -1


def main():
    if len(sys.argv) < 3:
        print("usage: chk.py input output")
        return 2
    n, m, adj = read_case(sys.argv[1])
    data = list(map(int, open(sys.argv[2]).read().split()))
    if not data:
        print("FAIL: empty output")
        return 1
    if data[0] == -1:
        if len(data) != 1:
            print("FAIL: -1 with extra tokens")
            return 1
        if min_len(n, adj) != -1:
            print("FAIL: -1 but a route pair exists")
            return 1
        return 0

    k = data[0]
    if k <= 0:
        print("FAIL: k must be positive")
        return 1
    if len(data) != 1 + 2 * (k + 1):
        print(f"FAIL: token count {len(data)} != {1+2*(k+1)}")
        return 1
    bob = [x - 1 for x in data[1:2 + k]]
    alex = [x - 1 for x in data[2 + k:]]
    if len(bob) != k + 1 or len(alex) != k + 1:
        print("FAIL: route lengths")
        return 1
    if bob[0] != 0 or bob[-1] != n - 1:
        print("FAIL: Bob must go from 1 to n")
        return 1
    if alex[0] != n - 1 or alex[-1] != 0:
        print("FAIL: Alex must go from n to 1")
        return 1

    eset = set()
    for u in range(n):
        for v in adj[u]:
            eset.add((u, v))
    for name, r in (("Bob", bob), ("Alex", alex)):
        for i in range(k):
            if (r[i], r[i + 1]) not in eset:
                print(f"FAIL: {name} step {i}: {r[i]}->{r[i+1]} is not a road")
                return 1
    for t in range(k + 1):
        if bob[t] == alex[t]:
            print(f"FAIL: they meet at crossroad {bob[t]+1} at time {t}")
            return 1

    best = min_len(n, adj)
    if k != best:
        print(f"FAIL: k={k} but minimum is {best}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
