#!/usr/bin/env python3
"""CF141D Take-off Ramps 的校验器（最优方案可能不唯一）。

用法: python3 cf141d.py <input> <output> [expected]

校验条件：
  1. 用独立的 Dijkstra（坐标压缩 + 相邻走路边 + 跳板边）算出最小时间 T*；
  2. 输出的 T 必须等于 T*，k 必须等于给出的跳板个数，编号互不相同且在 1..n；
  3. 按输出顺序真实模拟：从 0 出发走到 x-p（距离取绝对值），再花 p+t 飞到 x+d，最后走到 L，
     得到的总时间必须等于 T，且全程不出现在负半轴、不使用 x-p<0 的跳板。
"""
import heapq
import sys


def optimum(n, L, ramps):
    coord = {0, L}
    for x, d, t, p in ramps:
        if x - p >= 0:
            coord.add(x - p)
        coord.add(x)
        coord.add(x + d)
    coord = sorted(coord)
    idx = {c: i for i, c in enumerate(coord)}
    V = len(coord)
    adj = [[] for _ in range(V)]
    for i in range(V - 1):
        w = coord[i + 1] - coord[i]
        adj[i].append((i + 1, w))
        adj[i + 1].append((i, w))
    for x, d, t, p in ramps:
        if x - p >= 0:
            adj[idx[x - p]].append((idx[x + d], p + t))
    dist = [float('inf')] * V
    dist[0] = 0
    pq = [(0, 0)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        for v, w in adj[u]:
            if du + w < dist[v]:
                dist[v] = du + w
                heapq.heappush(pq, (du + w, v))
    return dist[idx[L]]


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, L = int(data[0]), int(data[1])
    ramps = []
    pos = 2
    for _ in range(n):
        ramps.append(tuple(int(v) for v in data[pos:pos + 4]))
        pos += 4
    best = optimum(n, L, ramps)
    out = open(sys.argv[2], encoding='utf-8').read().split('\n')
    out = [ln.strip() for ln in out if ln.strip()]
    if not out:
        print('FAIL: 空输出')
        return 1
    T = int(out[0])
    if T != best:
        print('FAIL: 时间不是最优 %d != %d' % (T, best))
        return 1
    k = int(out[1]) if len(out) > 1 else 0
    seq = []
    for ln in out[2:]:
        seq.extend(int(v) for v in ln.split())
    if k != len(seq):
        print('FAIL: k 与给出的编号个数不符')
        return 1
    if len(set(seq)) != len(seq):
        print('FAIL: 同一跳板被用了多次')
        return 1
    if any(not (1 <= v <= n) for v in seq):
        print('FAIL: 编号越界')
        return 1
    cur, total = 0, 0
    for v in seq:
        x, d, t, p = ramps[v - 1]
        start = x - p
        if start < 0:
            print('FAIL: 跳板 %d 的助跑起点在负半轴' % v)
            return 1
        total += abs(start - cur)          # 走到助跑起点（可向任意方向）
        total += p + t                     # 助跑 p 米 + 飞行 t 秒
        cur = x + d
    total += L - cur                       # 落地后走到终点
    if total != T:
        print('FAIL: 方案实际耗时 %d != 声称 %d' % (total, T))
        return 1
    return 0


sys.exit(main())
