#!/usr/bin/env python3
"""CF152E Garden 的答案校验器（方案不唯一）。

用法: python3 cf152e.py <input> <output> <expected>

校验：
  1. 第一行 cost 与棋盘尺寸正确；
  2. 所有重要格子都被铺上（X）；
  3. 所有 X 格子连通（四邻接）；
  4. cost == 所有 X 格子的花数之和；
  5. 若给出 expected（官方输出），cost 必须等于官方的最优值。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    p = 0
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    p = 3
    a = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            a[i][j] = int(data[p]); p += 1
    imp = []
    for _ in range(k):
        x, y = int(data[p]) - 1, int(data[p + 1]) - 1; p += 2
        imp.append((x, y))

    lines = [l.rstrip("\n") for l in open(sys.argv[2]).read().split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    if len(lines) != n + 1:
        print(f"应输出 {n + 1} 行，实际 {len(lines)}", file=sys.stderr)
        return 1
    try:
        cost = int(lines[0].strip())
    except ValueError:
        print("第一行不是整数", file=sys.stderr)
        return 1
    grid = lines[1:]
    for i, row in enumerate(grid):
        if len(row) != m:
            print(f"第 {i + 2} 行长度 {len(row)} != {m}", file=sys.stderr)
            return 1
        if any(c not in "X." for c in row):
            print(f"第 {i + 2} 行含非法字符", file=sys.stderr)
            return 1
    covered = [(i, j) for i in range(n) for j in range(m) if grid[i][j] == "X"]
    for (x, y) in imp:
        if grid[x][y] != "X":
            print(f"重要格子 ({x + 1},{y + 1}) 未铺", file=sys.stderr)
            return 1
    s = sum(a[i][j] for (i, j) in covered)
    if s != cost:
        print(f"cost {cost} != 覆盖花数和 {s}", file=sys.stderr)
        return 1
    # 连通性
    if covered:
        seen = {covered[0]}
        stack = [covered[0]]
        covset = set(covered)
        while stack:
            i, j = stack.pop()
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (i + di, j + dj)
                if nb in covset and nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if len(seen) != len(covered):
            print("覆盖的格子不连通", file=sys.stderr)
            return 1
    if len(sys.argv) > 3:
        exp = open(sys.argv[3]).read().split()
        if exp:
            try:
                expc = int(exp[0])
            except ValueError:
                expc = None
            if expc is not None and cost != expc:
                print(f"cost {cost} != 最优 {expc}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
