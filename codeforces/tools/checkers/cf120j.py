#!/usr/bin/env python3
"""CF120J Minimum Sum 的校验器（答案不唯一）。

用法: python3 cf120j.py <input> <output> [expected]
  input：n + n 行向量
  output：i k1 j k2

校验条件：
  1. i、j 在 [1,n] 且 i != j；k1、k2 在 [1,4]；
  2. 输出组合的 |v_i^{k1}+v_j^{k2}|^2 必须等于最优值（校验器用 O(n^2*16) 暴力；n 很大时用最近点对化简）。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    vs = []
    p = 1
    for _ in range(n):
        vs.append((int(data[p]), int(data[p + 1])))
        p += 2
    toks = open(sys.argv[2]).read().split()
    if len(toks) < 4:
        print("应输出四个整数", file=sys.stderr)
        return 1
    try:
        i, k1, j, k2 = (int(t) for t in toks[:4])
    except ValueError:
        print("输出不是整数", file=sys.stderr)
        return 1
    if not (1 <= i <= n and 1 <= j <= n) or i == j:
        print("i/j 非法", file=sys.stderr)
        return 1
    if not (1 <= k1 <= 4 and 1 <= k2 <= 4):
        print("k 非法", file=sys.stderr)
        return 1

    def var(v, k):
        x, y = v
        return (x * (-1 if k in (2, 4) else 1), y * (-1 if k in (3, 4) else 1))

    a = var(vs[i - 1], k1)
    b = var(vs[j - 1], k2)
    got = (a[0] + b[0]) ** 2 + (a[1] + b[1]) ** 2

    # 最优值：每个向量取 (|x|,|y|) 后求最近点对（O(n^2) 剪枝版）
    pts = sorted((abs(x), abs(y)) for (x, y) in vs)
    best = None
    for t in range(len(pts)):
        for u in range(t + 1, len(pts)):
            dx = pts[t][0] - pts[u][0]
            dy = pts[t][1] - pts[u][1]
            d = dx * dx + dy * dy
            if best is None or d < best:
                best = d
    if got != best:
        print(f"组合模长^2={got}，最优={best}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
