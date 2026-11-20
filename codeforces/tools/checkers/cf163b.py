#!/usr/bin/env python3
"""CF163B Lemmings 的答案校验器（跳法不唯一）。

用法: python3 cf163b.py <input> <output> <expected>

校验：输出 k 个互不相同的编号；按台号升高，重量非降；每个跳跃者都来得及
（时间 ≤ t），且 t 等于最优值（用二分 + 贪心独立求得）。
"""
import sys


def optimal_t(n, k, h, m, v):
    order = sorted(range(n), key=lambda i: (m[i], v[i]))

    def feasible(t):
        need = 0
        for i in order:
            if need >= k:
                break
            if v[i] + 1e-12 >= (need + 1) * h / t:
                need += 1
        return need >= k

    lo, hi = 0.0, max(k * h / v[i] for i in range(n))
    for _ in range(100):
        mid = (lo + hi) / 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid
    return hi


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, k, h = int(data[0]), int(data[1]), int(data[2])
    m = [int(x) for x in data[3:3 + n]]
    v = [int(x) for x in data[3 + n:3 + 2 * n]]
    ids = [int(x) - 1 for x in open(sys.argv[2]).read().split()]
    if len(ids) != k:
        print(f"应输出 {k} 个数，实际 {len(ids)} 个", file=sys.stderr)
        return 1
    if len(set(ids)) != k or any(not (0 <= i < n) for i in ids):
        print("编号非法或重复", file=sys.stderr)
        return 1
    for a, b in zip(ids, ids[1:]):
        if m[a] > m[b]:
            print("重量未随台高非降", file=sys.stderr)
            return 1
    t = 0.0
    for j, i in enumerate(ids):
        t = max(t, (j + 1) * h / v[i])
    opt = optimal_t(n, k, h, m, v)
    if abs(t - opt) > 1e-9 * max(1.0, opt):
        print(f"最大用时 {t} 不是最优 {opt}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
