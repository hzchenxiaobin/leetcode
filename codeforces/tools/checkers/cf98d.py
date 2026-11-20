#!/usr/bin/env python3
"""CF98D Help Monks 的构造校验器（答案序列不唯一）。

用法: python3 cf98d.py <input> <output> [expected]
  input：n / d_1 ... d_n（从底到顶，直径递减，允许相等）
  output：m / 之后 m 行 "s t"，表示把 s 号柱最上面的盘子移到 t 号柱

校验条件：
  1. 行数恰好是 1 + m，且每个盘子的移动都合法（源柱非空；大盘不能压在小盘上，
     直径相等可以压）；
  2. 最终所有盘子按 1..n 顺序落在 3 号柱上（1 号盘在最底下）；
  3. m 必须等于最优移动数：把连续等直径的盘子分成"组"，设底组大小 m_1、……、
     顶组大小 m_k，则
         P_k = 2*m_k - 1,  F_k = m_k
         若 m_i == 1： P_i = F_i = 1 + 2*F_{i+1}
         否则：       P_i = P_{i+1} + 2*m_i + 2*F_{i+1},  F_i = m_i + 2*F_{i+1}
     答案就是 P_1（与 P 表示"整体顺序保持"的最优值）。
"""
import sys


def optimal(d):
    n = len(d)
    comps = []
    i = 0
    while i < n:
        j = i
        while j < n and d[j] == d[i]:
            j += 1
        comps.append(j - i)
        i = j
    k = len(comps)
    P = F = 0
    for idx in range(k - 1, -1, -1):
        m = comps[idx]
        if idx == k - 1:
            P, F = 2 * m - 1, m
        elif m == 1:
            P = F = 1 + 2 * F
        else:
            P, F = P + 2 * m + 2 * F, m + 2 * F
    return P


def main() -> int:
    inp_path, out_path = sys.argv[1], sys.argv[2]
    data = open(inp_path).read().split()
    n = int(data[0])
    d = [int(x) for x in data[1:1 + n]]
    best = optimal(d)

    lines = [ln.split() for ln in open(out_path).read().splitlines() if ln.split()]
    if not lines:
        print("输出为空", file=sys.stderr)
        return 1
    try:
        m = int(lines[0][0])
    except ValueError:
        print("第一行不是整数", file=sys.stderr)
        return 1
    if len(lines[0]) != 1:
        print("第一行应只有一个整数 m", file=sys.stderr)
        return 1
    if m != best:
        print(f"移动数 {m} 不是最优值 {best}", file=sys.stderr)
        return 1
    if len(lines) - 1 != m:
        print(f"应输出 {m} 行移动，实际 {len(lines) - 1} 行", file=sys.stderr)
        return 1

    pillars = [list(range(n)), [], []]
    for k in range(1, m + 1):
        if len(lines[k]) != 2:
            print(f"第 {k} 行应为两个整数", file=sys.stderr)
            return 1
        try:
            s, t = int(lines[k][0]), int(lines[k][1])
        except ValueError:
            print(f"第 {k} 行存在非整数", file=sys.stderr)
            return 1
        if not (1 <= s <= 3 and 1 <= t <= 3) or s == t:
            print(f"第 {k} 行的柱号非法：{s} {t}", file=sys.stderr)
            return 1
        src, dst = pillars[s - 1], pillars[t - 1]
        if not src:
            print(f"第 {k} 行从空柱 {s} 取盘", file=sys.stderr)
            return 1
        disk = src[-1]
        if dst and d[dst[-1]] < d[disk]:
            print(f"第 {k} 行把直径 {d[disk]} 的盘子压到直径 {d[dst[-1]]} 上", file=sys.stderr)
            return 1
        src.pop()
        dst.append(disk)
    if pillars[0] or pillars[1]:
        print("移动结束后仍有盘子不在 3 号柱", file=sys.stderr)
        return 1
    if pillars[2] != list(range(n)):
        print("3 号柱上的盘子顺序不对", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
