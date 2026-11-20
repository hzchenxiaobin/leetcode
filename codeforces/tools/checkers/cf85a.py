#!/usr/bin/env python3
"""85A Domino 的 checker（构造题，答案不唯一）。

用法: python3 cf85a.py <input> <output> <answer>
校验：
  1. 输出为 -1 时：用 4 位掩码 DP 独立确认确实无解；
  2. 否则必须恰好 4 行、每行 n 个小写字母；
  3. 同色细胞必须恰好两两相邻成一个骨牌（每个格子的同色正交邻居恰为 1 个）；
  4. 每个竖切（第 j 与 j+1 列之间，1 <= j < n）至少被一个横骨牌穿过。
"""
import sys

ROWS = 4


def feasible(n):
    """4 位掩码 DP：每列填充，cut 必须被横骨牌穿过。"""
    fill = {}

    def gen(mask_in):
        out = set()

        def dfs(row, used, mask_out):
            if row == ROWS:
                out.add(mask_out)
                return
            if used & (1 << row):
                dfs(row + 1, used, mask_out)
                return
            if row + 1 < ROWS and not (used & (1 << (row + 1))):
                dfs(row + 2, used | (1 << row) | (1 << (row + 1)), mask_out)
            dfs(row + 1, used | (1 << row), mask_out | (1 << row))

        dfs(0, mask_in, 0)
        return out

    for m in range(16):
        fill[m] = gen(m)
    reach = [set() for _ in range(n + 1)]
    reach[0].add(0)
    for j in range(n):
        for m in reach[j]:
            for mo in fill[m]:
                if j < n - 1:
                    if mo == 0:
                        continue
                elif mo != 0:
                    continue
                reach[j + 1].add(mo)
    return 0 in reach[n]


def main():
    inp = open(sys.argv[1]).read().split()
    out_lines = [l.rstrip("\n") for l in open(sys.argv[2]).read().splitlines()]
    n = int(inp[0])
    body = [l for l in out_lines if l.strip() != ""]
    if body and body[0].strip() == "-1":
        sys.exit(0 if not feasible(n) else 1)
    if len(body) != ROWS:
        sys.exit(1)
    g = body
    for r in range(ROWS):
        if len(g[r]) != n:
            sys.exit(1)
        for ch in g[r]:
            if not ('a' <= ch <= 'z'):
                sys.exit(1)
    # 每个格子必须恰有 1 个同色正交邻居（否则同色骨牌相邻或形状不是骨牌）
    for r in range(ROWS):
        for c in range(n):
            cnt = 0
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < n and g[nr][nc] == g[r][c]:
                    cnt += 1
            if cnt != 1:
                sys.exit(1)
    # 每个竖切至少被一个横骨牌穿过
    for c in range(n - 1):
        ok = False
        for r in range(ROWS):
            if g[r][c] == g[r][c + 1]:
                ok = True
                break
        if not ok:
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
