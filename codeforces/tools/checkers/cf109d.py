#!/usr/bin/env python3
"""109D Lucky Sorting 的 checker（构造题，答案不唯一）。

用法: python3 checker.py <input> <output> <answer>
校验：
  1. 若输出 -1：原数组必须不含幸运数且本身未排序；
  2. 否则：0 <= k <= 2n；每行一对下标 (1..n, 不同)；
  3. 按顺序模拟交换，要求每次交换的两张牌中至少有一张是幸运数；
  4. 最终数组必须非降序。
"""
import sys


def is_lucky(x):
    if x <= 0:
        return False
    while x:
        d = x % 10
        if d != 4 and d != 7:
            return False
        x //= 10
    return True


def main():
    inp = open(sys.argv[1]).read().split()
    n = int(inp[0])
    a = [int(v) for v in inp[1:1 + n]]
    lines = [l.strip() for l in open(sys.argv[2]).read().splitlines() if l.strip()]
    if not lines:
        sys.exit(1)
    if lines[0] == "-1":
        ok = (not any(is_lucky(v) for v in a)) and any(a[i] > a[i + 1] for i in range(n - 1))
        sys.exit(0 if ok else 1)
    k = int(lines[0])
    if k < 0 or k > 2 * n:
        sys.exit(1)
    if len(lines) < k + 1:
        sys.exit(1)
    arr = a[:]
    for t in range(k):
        parts = lines[1 + t].split()
        if len(parts) != 2:
            sys.exit(1)
        i, j = int(parts[0]), int(parts[1])
        if not (1 <= i <= n and 1 <= j <= n) or i == j:
            sys.exit(1)
        x, y = arr[i - 1], arr[j - 1]
        if not (is_lucky(x) or is_lucky(y)):
            sys.exit(1)
        arr[i - 1], arr[j - 1] = y, x
    if all(arr[i] <= arr[i + 1] for i in range(n - 1)):
        sys.exit(0)
    sys.exit(1)


main()
