#!/usr/bin/env python3
"""31A 的 checker：输出必须是 -1（且确实无解），或三个不同的合法下标 i j k 且 a_i = a_j + a_k。

用法: python3 checker.py <input> <output> <answer>
"""
import sys


def main() -> int:
    inp = open(sys.argv[1]).read().split()
    out = open(sys.argv[2]).read().split()
    n = int(inp[0])
    a = [int(x) for x in inp[1:1 + n]]

    exists = any(
        len({i, j, k}) == 3 and a[i] == a[j] + a[k]
        for i in range(n) for j in range(n) for k in range(n)
    )

    if len(out) == 1 and out[0] == "-1":
        return 0 if not exists else 1
    if len(out) != 3:
        print("输出既不是 -1 也不是三个整数")
        return 1
    try:
        i, j, k = (int(x) - 1 for x in out)
    except ValueError:
        return 1
    if not all(0 <= x < n for x in (i, j, k)):
        print("下标越界")
        return 1
    if len({i, j, k}) != 3:
        print("下标不是三个不同的数")
        return 1
    if a[i] != a[j] + a[k]:
        print(f"不满足 a[{i}] = a[{j}] + a[{k}]")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
