#!/usr/bin/env python3
"""CF111A Petya and Inequiations 的构造校验器（答案不唯一）。

用法: python3 cf111a.py <input> <output> [expected]
  input：n x y
  output：要么是单独一个 -1，要么是 n 个正整数（每行一个）

校验条件：
  1. 输出 -1 时，必须确实无解。无解的充要条件：把 y 全堆到一个数上取得
     平方和上界 (y-n+1)^2 + (n-1)（y < n 时连"每个数至少 1"都做不到）；
  2. 否则必须恰好 n 个数，全部 >= 1，且 sum(a_i^2) >= x、sum(a_i) <= y。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, x, y = int(data[0]), int(data[1]), int(data[2])
    feasible = (y >= n) and ((y - n + 1) ** 2 + (n - 1) >= x)

    toks = open(sys.argv[2]).read().split()
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
        vals = [int(t) for t in toks]
    except ValueError:
        print("存在非整数输出", file=sys.stderr)
        return 1
    if any(v < 1 for v in vals):
        print("必须全是正整数", file=sys.stderr)
        return 1
    if sum(v * v for v in vals) < x:
        print(f"平方和 {sum(v*v for v in vals)} < {x}", file=sys.stderr)
        return 1
    if sum(vals) > y:
        print(f"总和 {sum(vals)} > {y}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
