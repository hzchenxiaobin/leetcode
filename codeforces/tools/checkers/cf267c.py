#!/usr/bin/env python3
"""CF267C Berland Traffic 的 checker（多解 / 自然对数势能 + 实数输出）。

用法：python3 cf267c.py <input> <output> <answer>
返回 0 表示通过。

校验条件：
  1. 输出恰好 m+1 个实数（第一行总量，随后每条路一条）；
  2. 总量与标准答案的差 <= 1e-4 * max(1, |ans|)（题目要求 5 位小数）；
  3. 每条路 |traffic| <= c_i + 1e-4（容量）；
  4. 内部点 1<v<n 流入和 == 流出和（容差 1e-4）；
  5. 路径无关：BFS 由 traffic 求出势，再逐边核对 traffic == phi(a)-phi(b)（容差 1e-4）；
  6. 第一行总量 == 1 号点的净流出（容差 1e-4）。
"""
import sys
from collections import deque

TOL = 1e-4


def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    p = 0
    n = int(data[p]); p += 1
    m = int(data[p]); p += 1
    E = []
    for _ in range(m):
        a = int(data[p]); b = int(data[p + 1]); c = float(data[p + 2]); p += 3
        E.append((a, b, c))
    toks = open(out).read().split()
    if len(toks) != m + 1:
        print(f'CHECKER FAIL: 需要 {m+1} 个数，实际 {len(toks)}')
        return 1
    try:
        vals = [float(x) for x in toks]
    except ValueError:
        print('CHECKER FAIL: 存在非实数 token')
        return 1
    F = vals[0]
    tr = vals[1:]
    want = float(open(ans).read().split()[0])
    if abs(F - want) > 1e-4 * max(1.0, abs(want)):
        print(f'CHECKER FAIL: 总量 {F} 与标准答案 {want} 不符')
        return 1
    for i, (a, b, c) in enumerate(E):
        if abs(tr[i]) > c + TOL:
            print(f'CHECKER FAIL: 第 {i+1} 条路超容量 {abs(tr[i])} > {c}')
            return 1
    insum = [0.0] * (n + 1)
    outsum = [0.0] * (n + 1)
    for i, (a, b, c) in enumerate(E):
        outsum[a] += tr[i]
        insum[b] += tr[i]
    for v in range(2, n):
        if abs(insum[v] - outsum[v]) > TOL:
            print(f'CHECKER FAIL: {v} 号点不守恒 in={insum[v]} out={outsum[v]}')
            return 1
    # 路径无关
    adj = [[] for _ in range(n + 1)]
    for i, (a, b, c) in enumerate(E):
        adj[a].append((b, tr[i]))
        adj[b].append((a, -tr[i]))
    pot = {1: 0.0}
    q = deque([1])
    while q:
        v = q.popleft()
        for u, w in adj[v]:
            if u not in pot:
                pot[u] = pot[v] - w
                q.append(u)
    for i, (a, b, c) in enumerate(E):
        if a in pot and b in pot:
            if abs((pot[a] - pot[b]) - tr[i]) > TOL:
                print(f'CHECKER FAIL: 第 {i+1} 条路破坏路径无关')
                return 1
    net = 0.0
    for i, (a, b, c) in enumerate(E):
        if a == 1:
            net += tr[i]
        elif b == 1:
            net -= tr[i]
    if abs(net - F) > TOL * max(1.0, abs(F)):
        print(f'CHECKER FAIL: 总量 {F} 与 1 号点净流出 {net} 不符')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
