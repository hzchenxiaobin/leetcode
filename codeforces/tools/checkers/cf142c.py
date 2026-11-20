#!/usr/bin/env python3
"""CF142C Help Caretaker 的答案校验器（最优摆放方案不唯一）。

用法: python3 cf142c.py <input> <output> <expected>

输入：n m（1 ≤ n,m ≤ 9）。
输出：第一行 k，随后 n 行、每行 m 个字符，'.' 表示空，连续大写字母表示各台涡轮犁。

校验条件：
  1. 行数/列数正确，第一行 k 是非负整数；
  2. 出现的大写字母恰好是 A, B, ..., 连续 k 个，每个字母恰好 5 个格子；
  3. 每个字母的 5 个格子归一化（各自减去最小行、最小列）后必须等于四种 T 形五连块之一；
  4. 若提供了 expected（官方输出），则 k 必须等于官方输出的 k（官方已是最优）。
"""
import sys

SHAPES = [
    {(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)},
    {(0, 2), (1, 2), (2, 2), (1, 0), (1, 1)},
    {(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)},
]


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, m = int(data[0]), int(data[1])

    lines = [l.rstrip("\n") for l in open(sys.argv[2]).read().split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    if not lines:
        print("输出为空", file=sys.stderr)
        return 1
    try:
        k = int(lines[0].strip())
    except ValueError:
        print("第一行不是整数", file=sys.stderr)
        return 1
    grid = lines[1:]
    if len(grid) != n:
        print(f"应输出 {n} 行棋盘，实际 {len(grid)} 行", file=sys.stderr)
        return 1
    for i, row in enumerate(grid):
        if len(row) != m:
            print(f"第 {i + 2} 行长度 {len(row)} != {m}", file=sys.stderr)
            return 1

    cells = {}
    for i in range(n):
        for j in range(m):
            ch = grid[i][j]
            if ch == '.':
                continue
            if not ('A' <= ch <= 'Z'):
                print(f"非法字符 {ch!r}", file=sys.stderr)
                return 1
            cells.setdefault(ch, []).append((i, j))
    letters = sorted(cells)
    expect = [chr(ord('A') + t) for t in range(k)]
    if letters != expect:
        print(f"字母应为 A..{chr(ord('A') + k - 1)}，实际 {letters}", file=sys.stderr)
        return 1
    for ch in letters:
        pts = cells[ch]
        if len(pts) != 5:
            print(f"{ch} 占了 {len(pts)} 格（应为 5）", file=sys.stderr)
            return 1
        r0 = min(p[0] for p in pts)
        c0 = min(p[1] for p in pts)
        norm = {(r - r0, c - c0) for r, c in pts}
        if norm not in SHAPES:
            print(f"{ch} 的形状不是 T 形五连块: {sorted(norm)}", file=sys.stderr)
            return 1
    if len(sys.argv) > 3:
        exp = open(sys.argv[3]).read().split()
        if exp:
            try:
                expk = int(exp[0])
            except ValueError:
                expk = None
            if expk is not None and k != expk:
                print(f"数量 {k} 不等于最优值 {expk}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
