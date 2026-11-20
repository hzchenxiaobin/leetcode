#!/usr/bin/env python3
"""CF44D 独立暴力：显式模拟飞船的世界线并求最早相撞时刻。

模型：
  * 每一艘飞船是一条时空线段 (u, v, dep, arr)：dep 时刻离开 u，arr 时刻到达 v，
    期间沿直线匀速运动（速度 1）。
  * 用优先队列按 dep 递增生成飞船：初始为 1 -> v (v != 1)，dep = 0；
    某个 (u, v) 飞船到达 v 后，立刻派生出 v -> w (w != u, v)，dep = arr。
  * 两艘飞船若在时刻 t 位于同一点则相撞。程序对已生成的所有时空线段两两求解
    “同点同时”，只接受严格位于两条线段内部的交点（端点处的“到达/出发”重合
    不属于相撞，题意样例也印证了这一点）。
  * 剪枝：任何相撞时刻 t 都 >= 两艘飞船的 dep，故 dep >= best 的飞船不必生成。

这个暴力完全不使用“最小半周长”公式，可独立验证参考程序。
用法：python3 brute.py < input，输出最早相撞时刻（10 位小数）。
"""
import sys
import numpy as np
from heapq import heappush, heappop

EPS = 1e-9


def earliest_collision(pts):
    n = len(pts)
    P = np.array(pts, dtype=float)
    diff = P[:, None, :] - P[None, :, :]
    D = np.sqrt((diff * diff).sum(-1))

    dep_arr = []   # 已生成飞船的 dep
    arr_arr = []   # 已生成飞船的 arr
    A_arr = []     # 起点
    U_arr = []     # 速度向量
    best = float("inf")

    heap = [(0.0, 0, v) for v in range(1, n)]
    heap.sort()
    seen = set()

    while heap:
        dep, u, v = heappop(heap)
        if dep >= best - EPS:
            break
        key = (u, v, round(dep, 9))
        if key in seen:
            continue
        seen.add(key)

        arr = dep + D[u, v]
        if arr - dep <= EPS:
            continue
        A = P[u]
        U = (P[v] - P[u]) / (arr - dep)

        if dep_arr:
            dep_a = np.array(dep_arr)
            arr_a = np.array(arr_arr)
            Aa = np.array(A_arr)
            Ua = np.array(U_arr)
            vv = U[None, :] - Ua                          # (T,3)
            rhs = Aa - A[None, :] + U[None, :] * dep - Ua * dep_a[:, None]
            nv = (vv * vv).sum(1)
            with np.errstate(divide="ignore", invalid="ignore"):
                s = (vv * rhs).sum(1) / nv
            resid = np.sqrt(((vv * s[:, None] - rhs) ** 2).sum(1))
            lo = np.maximum(dep_a, dep)
            hi = np.minimum(arr_a, arr)
            ok = (nv > 1e-18) & (resid < 1e-7) & (s > lo + EPS) & (s < hi - EPS)
            if ok.any():
                best = min(best, float(s[ok].min()))
                if dep >= best - EPS:
                    continue

        dep_arr.append(dep)
        arr_arr.append(arr)
        A_arr.append(A)
        U_arr.append(U)

        if arr < best - EPS:
            for w in range(n):
                if w != u and w != v:
                    heappush(heap, (arr, v, w))

    return best


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    pts = []
    p = 1
    for _ in range(n):
        pts.append((int(data[p]), int(data[p + 1]), int(data[p + 2])))
        p += 3
    print("%.10f" % earliest_collision(pts))


if __name__ == "__main__":
    main()
