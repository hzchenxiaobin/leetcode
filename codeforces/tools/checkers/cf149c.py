#!/usr/bin/env python3
"""CF149C Division into Teams 的答案校验器（分队方案不唯一）。

用法: python3 cf149c.py <input> <output> <expected>

校验：两队人数之和 = n、人数差 <= 1、每个人都恰好出现一次、技能总和之差 <= 最大值。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    out = open(sys.argv[2]).read().split()
    if not out:
        print("输出为空", file=sys.stderr)
        return 1
    try:
        x = int(out[0])
    except ValueError:
        print("第一行不是整数", file=sys.stderr)
        return 1
    if x < 0 or x > len(out) - 1:
        print("人数不合法", file=sys.stderr)
        return 1
    t1 = out[1:1 + x]
    rest = out[1 + x:]
    if not rest:
        print("缺少第二队人数", file=sys.stderr)
        return 1
    try:
        y = int(rest[0])
    except ValueError:
        print("第二队人数不是整数", file=sys.stderr)
        return 1
    t2 = rest[1:]
    if len(t2) != y:
        print(f"声明 y={y}，实际 {len(t2)} 个编号", file=sys.stderr)
        return 1
    if x + y != n:
        print(f"x+y={x + y} != n={n}", file=sys.stderr)
        return 1
    if abs(x - y) > 1:
        print(f"人数差 {abs(x - y)} > 1", file=sys.stderr)
        return 1
    ids = []
    for s in t1 + t2:
        try:
            ids.append(int(s))
        except ValueError:
            print("编号含非整数", file=sys.stderr)
            return 1
    if sorted(ids) != list(range(1, n + 1)):
        print("编号不是 1..n 的一个排列", file=sys.stderr)
        return 1
    s1 = sum(a[i - 1] for i in ids[:x])
    s2 = sum(a[i - 1] for i in ids[x:])
    if abs(s1 - s2) > max(a):
        print(f"技能差 {abs(s1 - s2)} > 最大值 {max(a)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
