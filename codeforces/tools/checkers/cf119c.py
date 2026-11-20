#!/usr/bin/env python3
"""CF119C Education Reform 的校验器（答案不唯一）。

用法: python3 cf119c.py <input> <output> [expected]
  input：n m k / m 行 "a_i b_i c_i"
  output：NO 或 YES + n 行 "课程编号 作业量"

校验条件：
  1. 无解时必须输出 NO（无解判据由独立 DP 计算）；
  2. 有解时必须 YES + 恰好 n 行，课程编号合法且互不相同、难度严格递增；
     作业量在对应区间内；相邻两天满足 x_t = k + x_{t-1} 或 x_t = k * x_{t-1}；
  3. 总作业量必须等于独立 DP 算出的最优值。
"""
import sys


def best_total(n, m, k, subs):
    # subs: [(a,b,c)]，独立实现的 DP：逐天推进
    order = sorted(range(m), key=lambda i: (subs[i][2], i))
    # dp[j] = {count: best total}
    dp = [dict() for _ in range(m)]
    for j in order:
        a, b, c = subs[j]
        for x in range(a, b + 1):
            dp[j][x] = x
    for day in range(2, n + 1):
        ndp = [dict() for _ in range(m)]
        for j in order:
            aj, bj, cj = subs[j]
            for i in order:
                if subs[i][2] >= cj:
                    continue
                prev = dp[i]
                if not prev:
                    continue
                ai, bi, ci = subs[i]
                for y in range(aj, bj + 1):
                    best = None
                    if ai <= y - k <= bi and (y - k) in prev:
                        best = prev[y - k] + y
                    if k and y % k == 0 and ai <= y // k <= bi and (y // k) in prev:
                        cand = prev[y // k] + y
                        if best is None or cand > best:
                            best = cand
                    if best is not None:
                        cur = ndp[j].get(y)
                        if cur is None or best > cur:
                            ndp[j][y] = best
        dp = ndp
    vals = [v for j in order for v in dp[j].values()]
    return max(vals) if vals else None


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    subs = []
    p = 3
    for _ in range(m):
        subs.append((int(data[p]), int(data[p + 1]), int(data[p + 2])))
        p += 3
    opt = best_total(n, m, k, subs)
    toks = open(sys.argv[2]).read().split()
    if not toks:
        print("输出为空", file=sys.stderr)
        return 1
    if toks[0] == "NO":
        if opt is not None:
            print(f"有解（最优 {opt}），不应输出 NO", file=sys.stderr)
            return 1
        return 0
    if toks[0] != "YES":
        print("第一行必须是 YES 或 NO", file=sys.stderr)
        return 1
    if opt is None:
        print("无解，却输出了 YES", file=sys.stderr)
        return 1
    nums = toks[1:]
    if len(nums) != 2 * n:
        print(f"应输出 {n} 行，实际数字个数 {len(nums)}", file=sys.stderr)
        return 1
    used = set()
    prev_x = None
    prev_c = None
    total = 0
    for t in range(n):
        idx = int(nums[2 * t]); x = int(nums[2 * t + 1])
        if not (1 <= idx <= m):
            print("课程编号越界", file=sys.stderr)
            return 1
        if idx in used:
            print(f"课程 {idx} 被重复使用", file=sys.stderr)
            return 1
        used.add(idx)
        a, b, c = subs[idx - 1]
        if not (a <= x <= b):
            print(f"第 {t+1} 天作业量 {x} 不在 [{a},{b}]", file=sys.stderr)
            return 1
        if prev_c is not None:
            if not (c > prev_c):
                print("难度没有严格递增", file=sys.stderr)
                return 1
            if not (x == k + prev_x or (k and x == k * prev_x)):
                print(f"第 {t+1} 天不满足 x=k+x_prev 或 k*x_prev", file=sys.stderr)
                return 1
        prev_c, prev_x = c, x
        total += x
    if total != opt:
        print(f"总作业量 {total} 不是最优 {opt}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
