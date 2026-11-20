#!/usr/bin/env python3
"""CF140F New Year Snowflake 的校验器（中心可多个 / 顺序任意 / 可能为 -1）。

用法: python3 cf140f.py <input> <output> [expected]

校验条件：
  1. 独立求出「所有合法中心」的精确集合：候选中心取所有点对（含自身）的中点，
     对每个候选统计「镜像缺失」的点数，<= k 即合法；n <= k 时答案必须是 -1；
  2. 输出的中心个数与集合必须与之一致，误差 <= 1e-6，且不重复。
"""
import sys


def solve(n, k, pts):
    if n <= k:
        return None                       # 无穷多
    have = set(pts)
    cand = set()
    for i in range(n):
        for j in range(i, n):
            cand.add((pts[i][0] + pts[j][0], pts[i][1] + pts[j][1]))
    good = set()
    for sx, sy in cand:
        bad = 0
        for x, y in pts:
            if (sx - x, sy - y) not in have:
                bad += 1
                if bad > k:
                    break
        if bad <= k:
            good.add((sx, sy))
    return good


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, k = int(data[0]), int(data[1])
    pts = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(n)]
    truth = solve(n, k, pts)
    out = [ln.strip() for ln in open(sys.argv[2], encoding='utf-8') if ln.strip()]
    if truth is None:
        if out and out[0] == '-1':
            return 0
        print('FAIL: 应为 -1（有无穷多中心）')
        return 1
    if out and out[0] == '-1':
        print('FAIL: 不应为 -1')
        return 1
    c = int(out[0])
    if c != len(truth):
        print('FAIL: 中心个数 %d != %d' % (c, len(truth)))
        return 1
    got = set()
    for ln in out[1:1 + c]:
        x, y = (float(v) for v in ln.split())
        got.add((round(2 * x), round(2 * y)))
    if len(got) != c:
        print('FAIL: 中心重复')
        return 1
    for (sx, sy) in got:
        if (sx, sy) not in truth:
            print('FAIL: 非法中心 (%g, %g)' % (sx / 2, sy / 2))
            return 1
    return 0


sys.exit(main())
