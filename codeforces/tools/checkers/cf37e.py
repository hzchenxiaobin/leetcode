# 37E 穷举：对所有目标图案，BFS 求最少操作数（每次把任意连通块涂成一色）
import sys
from collections import deque
from itertools import product

def solve(N, M):
    n = N * M
    neigh = [[] for _ in range(n)]
    for r in range(N):
        for c in range(M):
            i = r*M+c
            if r+1 < N: neigh[i].append((r+1)*M+c); neigh[(r+1)*M+c].append(i)
            if c+1 < M: neigh[i].append(r*M+c+1); neigh[r*M+c+1].append(i)
    # 枚举所有连通子集
    subsets = []
    for mask in range(1, 1 << n):
        # 连通性检查
        start = (mask & -mask).bit_length() - 1
        seen = 1 << start
        st = [start]
        while st:
            v = st.pop()
            for u in neigh[v]:
                if (mask >> u & 1) and not (seen >> u & 1):
                    seen |= 1 << u; st.append(u)
        if seen == mask: subsets.append(mask)
    # BFS：状态 = 当前黑白 (bit=1 表示黑)；初始全白 = 0
    INF = 10**9
    dist = [INF] * (1 << n)
    dist[0] = 0
    q = deque([0])
    while q:
        s = q.popleft()
        for sub in subsets:
            # 涂黑
            t = s | sub
            if dist[t] > dist[s] + 1:
                dist[t] = dist[s] + 1; q.append(t)
            # 涂白
            t = s & ~sub
            if dist[t] > dist[s] + 1:
                dist[t] = dist[s] + 1; q.append(t)
    return dist, neigh

def formula(N, M, pat, neigh):
    n = N*M
    best = 10**9
    from collections import deque as dq
    for s0 in range(n):
        d = [10**9]*n; d[s0] = 0
        q = dq([s0])
        while q:
            v = q.popleft()
            for u in neigh[v]:
                w = 0 if ((pat >> v) & 1) == ((pat >> u) & 1) else 1
                if d[u] > d[v] + w:
                    d[u] = d[v] + w
                    if w == 0: q.appendleft(u)
                    else: q.append(u)
        mx = max(d)
        best = min(best, mx + (0 if (pat >> s0) & 1 else 1))   # dist_grid[s]=1 表示黑
    return best

for (N, M) in [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]:
    dist, neigh = solve(N, M)
    n = N*M
    bad = 0; tot = 0
    for mask in range(1 << n):
        if dist[mask] >= 10**9: continue
        f = formula(N, M, mask, neigh)
        tot += 1
        if f != dist[mask]:
            bad += 1
            if bad <= 3:
                grid = [''.join('B' if mask >> (r*M+c) & 1 else 'W' for c in range(M)) for r in range(N)]
                print('MISMATCH', N, M, grid, 'bfs', dist[mask], 'formula', f)
    print(f'{N}x{M}: checked {tot} patterns, mismatch {bad}')
