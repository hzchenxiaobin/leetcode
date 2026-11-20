#!/usr/bin/env python3
"""34A 的 checker：输出两个下标，必须是环上相邻的一对，且身高差等于全局最小值。

用法: python3 checker.py <input> <output> <answer>
"""
import sys


def main() -> int:
    inp = open(sys.argv[1]).read().split()
    out = open(sys.argv[2]).read().split()
    n = int(inp[0])
    a = [int(x) for x in inp[1:1 + n]]

    best = min(abs(a[i] - a[(i + 1) % n]) for i in range(n))

    if len(out) != 2:
        print("应输出两个整数")
        return 1
    try:
        x, y = int(out[0]) - 1, int(out[1]) - 1
    except ValueError:
        return 1
    if not (0 <= x < n and 0 <= y < n):
        print("下标越界")
        return 1
    if (x + 1) % n != y and (y + 1) % n != x:
        print("两人不相邻")
        return 1
    if abs(a[x] - a[y]) != best:
        print(f"身高差 {abs(a[x]-a[y])} 不是最小值 {best}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
