#!/usr/bin/env python3
"""CF114B PFAST Inc. 的答案校验器（答案不唯一：相同人数的合法队伍都算对）。

用法: python3 cf114b.py <input> <output> [expected]

输入：n m，随后 n 行姓名，随后 m 行「不和的两人」。
输出：第一行 k，随后 k 行队员姓名（要求字典序）。

校验条件：
  1. 第一行是整数 k，之后恰好 k 行、每行一个姓名；
  2. 姓名互不相同，且都出现在输入的 n 个姓名里；
  3. 选出的任意两人之间都没有"不和"关系（即队伍内部无冲突边）；
  4. 姓名按字典序升序输出；
  5. k 等于最大独立集大小（本 checker 独立用 2^n 全枚举求出），
     即不接受"人数不是最多"的合法队伍。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, m = int(data[0]), int(data[1])
    pos = 2
    names = data[pos:pos + n]
    pos += n
    idx = {s: i for i, s in enumerate(names)}
    bad = [0] * n
    for _ in range(m):
        u, v = idx[data[pos]], idx[data[pos + 1]]
        pos += 2
        bad[u] |= 1 << v
        bad[v] |= 1 << u

    # 独立求出最大可行队伍人数
    best = 0
    for mask in range(1, 1 << n):
        c = bin(mask).count("1")
        if c <= best:
            continue
        ok = True
        for i in range(n):
            if mask >> i & 1 and bad[i] & mask:
                ok = False
                break
        if ok:
            best = c

    lines = [l for l in open(sys.argv[2]).read().split("\n")]
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        print("输出为空", file=sys.stderr)
        return 1
    try:
        k = int(lines[0].strip())
    except ValueError:
        print("第一行不是整数", file=sys.stderr)
        return 1
    team = [l.strip() for l in lines[1:]]
    if len(team) != k:
        print(f"声明 k={k}，实际给出 {len(team)} 个姓名", file=sys.stderr)
        return 1
    if len(set(team)) != k:
        print("姓名有重复", file=sys.stderr)
        return 1
    for s in team:
        if s not in idx:
            print(f"姓名 {s!r} 不在输入中", file=sys.stderr)
            return 1
    for i in range(k):
        for j in range(i + 1, k):
            if bad[idx[team[i]]] >> idx[team[j]] & 1:
                print(f"{team[i]} 和 {team[j]} 不和", file=sys.stderr)
                return 1
    if team != sorted(team):
        print("姓名未按字典序输出", file=sys.stderr)
        return 1
    if k != best:
        print(f"人数 {k} 不是最大值 {best}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
