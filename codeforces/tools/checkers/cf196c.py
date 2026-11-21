#!/usr/bin/env python3
"""CF196C Paint Tree 的 checker（答案不唯一：任意合法嵌入均可）。

约定：python3 cf196c.py <input> <output> <answer>，返回 0 表示通过。
校验：
  1. 输出是 1..n 的排列（把第 i 个点分配给哪个树顶点）；
  2. 任意两条不相邻的边对应的线段不相交（无三点共线，用严格叉积判定）；
  3. 相邻的边只在公共顶点处相接（由无三点共线自动成立）。
"""
import sys


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def proper_intersect(p1, p2, p3, p4):
    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def main():
    inp, out, _ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    n = int(data[0])
    edges = []
    p = 1
    for _ in range(n - 1):
        u = int(data[p]) - 1
        v = int(data[p + 1]) - 1
        p += 2
        edges.append((u, v))
    pts = []
    for i in range(n):
        pts.append((int(data[p]), int(data[p + 1])))
        p += 2

    toks = open(out).read().split()
    if len(toks) != n:
        print(f'CHECKER FAIL: 输出应有 {n} 个数，实际 {len(toks)} 个')
        return 1
    try:
        assign = [int(x) - 1 for x in toks]
    except ValueError:
        print('CHECKER FAIL: 输出含非整数')
        return 1
    if sorted(assign) != list(range(n)):
        print('CHECKER FAIL: 输出不是 1..n 的排列')
        return 1

    # 顶点 v 放在 pts[where[v]]
    where = [0] * n
    for i, v in enumerate(assign):
        where[v] = i

    m = len(edges)
    for i in range(m):
        a, b = edges[i]
        pa, pb = pts[where[a]], pts[where[b]]
        for j in range(i + 1, m):
            c, d = edges[j]
            if len({a, b, c, d}) < 4:
                continue                      # 相邻边，公共顶点处相接
            pc, pd = pts[where[c]], pts[where[d]]
            if proper_intersect(pa, pb, pc, pd):
                print(f'CHECKER FAIL: 边 {i+1} 与 {j+1} 的线段相交')
                return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
