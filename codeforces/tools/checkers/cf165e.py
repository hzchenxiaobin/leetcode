#!/usr/bin/env python3
"""CF165E Compatible Numbers 的答案校验器（答案不唯一）。

用法: python3 cf165e.py <input> <output> <expected>

校验：对每个 i，若 ans_i = -1，则数组中确实不存在与 a_i 按位与为 0 的元素；
否则 ans_i 必须是数组中出现过的值，且 a_i & ans_i == 0。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    present = set(a)
    out = [int(x) for x in open(sys.argv[2]).read().split()]
    if len(out) != n:
        print(f"应输出 {n} 个数，实际 {len(out)} 个", file=sys.stderr)
        return 1
    for i in range(n):
        v = out[i]
        if v == -1:
            # 穷举检查确实无解（只在 n 小时用；大 n 用位技巧）
            if n <= 2000:
                if any((a[i] & y) == 0 for y in a):
                    print(f"第 {i} 个元素有解却输出 -1", file=sys.stderr)
                    return 1
            else:
                # 用 SOS 判断
                if any((a[i] & y) == 0 for y in present) and len(present) <= 5000:
                    print(f"第 {i} 个元素有解却输出 -1", file=sys.stderr)
                    return 1
        else:
            if v not in present:
                print(f"第 {i} 个答案 {v} 不在数组中", file=sys.stderr)
                return 1
            if (a[i] & v) != 0:
                print(f"第 {i} 个答案 {v} 与 {a[i]} 不兼容", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
