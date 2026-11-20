#!/usr/bin/env python3
"""CF159E Zebra Tower 的答案校验器（塔的两种朝向都合法）。

用法: python3 cf159e.py <input> <output> <expected>

校验：
  1. 第二行数量与第三行编号个数一致、编号互不相同且在 1..n 内；
  2. 这些编号构成"恰好两种颜色交替"的塔；
  3. 第一行高度 = 这些方块尺寸之和；
  4. 若给出 expected（官方输出），高度必须等于官方的最优高度。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    c = [0] * (n + 1)
    s = [0] * (n + 1)
    p = 1
    for i in range(1, n + 1):
        c[i] = int(data[p]); s[i] = int(data[p + 1]); p += 2

    out = [l for l in open(sys.argv[2]).read().split("\n") if l.strip()]
    if len(out) != 3:
        print("输出应为三行", file=sys.stderr)
        return 1
    try:
        height = int(out[0].split()[0])
        cnt = int(out[1].split()[0])
    except ValueError:
        print("前两行应为整数", file=sys.stderr)
        return 1
    idx = [int(x) for x in out[2].split()]
    if len(idx) != cnt:
        print(f"声明 {cnt} 个方块，实际 {len(idx)} 个", file=sys.stderr)
        return 1
    if cnt < 2:
        print("塔至少要有 2 个方块", file=sys.stderr)
        return 1
    if len(set(idx)) != cnt or any(not (1 <= i <= n) for i in idx):
        print("编号非法或重复", file=sys.stderr)
        return 1
    colors = {c[i] for i in idx}
    if len(colors) != 2:
        print(f"塔必须恰好用两种颜色，实际 {len(colors)} 种", file=sys.stderr)
        return 1
    for a, b in zip(idx, idx[1:]):
        if c[a] == c[b]:
            print("相邻方块颜色相同", file=sys.stderr)
            return 1
    if sum(s[i] for i in idx) != height:
        print(f"高度 {height} != 尺寸和 {sum(s[i] for i in idx)}", file=sys.stderr)
        return 1
    if len(sys.argv) > 3:
        exp = open(sys.argv[3]).read().split()
        if exp:
            try:
                eh = int(exp[0])
            except ValueError:
                eh = None
            if eh is not None and height != eh:
                print(f"高度 {height} 不等于最优 {eh}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
