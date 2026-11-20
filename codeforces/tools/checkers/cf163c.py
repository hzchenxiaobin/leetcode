#!/usr/bin/env python3
"""CF163C Conveyor 的答案校验器（输出 n+1 个概率，允许 1e-9 误差）。

用法: python3 cf163c.py <input> <output> <expected>

校验：共 n+1 个数；与官方输出逐个比较，绝对或相对误差 ≤ 1e-9；
      并且所有概率之和与 1 的偏差 ≤ 1e-6。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    got = [float(x) for x in open(sys.argv[2]).read().split()]
    if len(got) != n + 1:
        print(f"应输出 {n + 1} 个数，实际 {len(got)} 个", file=sys.stderr)
        return 1
    exp = [float(x) for x in open(sys.argv[3]).read().split()]
    if len(exp) == n + 1:
        for i in range(n + 1):
            if abs(got[i] - exp[i]) > 1e-9 * max(1.0, abs(exp[i])):
                print(f"第 {i} 个概率 {got[i]} 与 {exp[i]} 相差过大", file=sys.stderr)
                return 1
    if abs(sum(got) - 1.0) > 1e-6:
        print(f"概率和 {sum(got)} 不为 1", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
