#!/usr/bin/env python3
"""CF81D Polycarp's Picture Gallery 的构造校验器（答案不唯一）。

用法: python3 cf81d.py <input> <output> [expected]
  input：n m / a_1 ... a_m
  output：要么是单独一个 -1（表示无解），要么是 n 个 1..m 的整数（每个表示该位置照片所属相册）

校验条件：
  1. 若输出 -1：必须确实无解。无解的充要条件是
     sum_i min(a_i, floor(n/2)) < n —— 因为环上同色照片最多 n/2 张，
     且每张照片的相册容量是 a_i。
  2. 否则：恰好 n 个数、都在 [1,m] 内；第 i 个相册出现的次数 <= a_i；
     环上任意相邻两张（含最后一张与第一张）不能来自同一相册。
"""
import sys


def main() -> int:
    inp_path, out_path = sys.argv[1], sys.argv[2]
    data = open(inp_path).read().split()
    n, m = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + m]]
    half = n // 2
    feasible = sum(min(ai, half) for ai in a) >= n

    toks = open(out_path).read().split()
    if not toks:
        print("输出为空", file=sys.stderr)
        return 1
    if toks[0] == "-1":
        if len(toks) != 1:
            print("-1 之后不应再有内容", file=sys.stderr)
            return 1
        if feasible:
            print("该实例有解，不应输出 -1", file=sys.stderr)
            return 1
        return 0
    if len(toks) != n:
        print(f"应输出 {n} 个数，实际 {len(toks)} 个", file=sys.stderr)
        return 1
    try:
        seq = [int(x) for x in toks]
    except ValueError:
        print("存在非整数输出", file=sys.stderr)
        return 1
    cnt = [0] * (m + 1)
    for v in seq:
        if not (1 <= v <= m):
            print(f"相册编号 {v} 越界", file=sys.stderr)
            return 1
        cnt[v] += 1
    for i in range(1, m + 1):
        if cnt[i] > a[i - 1]:
            print(f"相册 {i} 用了 {cnt[i]} 张，超过 {a[i - 1]}", file=sys.stderr)
            return 1
    for i in range(n):
        if seq[i] == seq[(i + 1) % n]:
            print(f"位置 {i + 1} 与 {i % n + 1} 相邻且同相册", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
