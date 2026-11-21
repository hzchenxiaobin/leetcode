#!/usr/bin/env python3
"""CF311A 的 checker（多解）：模拟伪代码统计 tot，要求 tot > k；或验证 no solution 确实无解。"""
import sys

def simulate(points):
    pts = sorted(points)
    n = len(pts)
    INF = float('inf')
    d = INF
    tot = 0
    for i in range(n):
        for j in range(i + 1, n):
            tot += 1
            if pts[j][0] - pts[i][0] >= d:
                break
            dx = pts[j][0] - pts[i][0]
            dy = pts[j][1] - pts[i][1]
            d = min(d, (dx * dx + dy * dy) ** 0.5)
    return tot

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    n, k = map(int, open(inp).read().split()[:2])
    toks = open(out).read().split()
    if toks[:2] == ['no', 'solution']:
        if k >= n * (n - 1) // 2:
            return 0
        print('CHECKER FAIL: 有解却输出 no solution')
        return 1
    if len(toks) != 2 * n:
        print('CHECKER FAIL: 需要 %d 个坐标数，实际 %d' % (2 * n, len(toks)))
        return 1
    vals = list(map(int, toks))
    pts = [(vals[2 * i], vals[2 * i + 1]) for i in range(n)]
    for (x, y) in pts:
        if abs(x) > 10**9 or abs(y) > 10**9:
            print('CHECKER FAIL: 坐标越界')
            return 1
    if len(set(pts)) != n:
        print('CHECKER FAIL: 存在重复点')
        return 1
    tot = simulate(pts)
    if tot <= k:
        print('CHECKER FAIL: tot=%d 未超过 k=%d' % (tot, k))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
