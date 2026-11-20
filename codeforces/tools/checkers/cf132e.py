#!/usr/bin/env python3
"""CF132E Bits of merry old England 的答案校验器（最优程序不唯一）。

用法: python3 cf132e.py <input> <output> <expected>

输入：n m，随后 n 个整数。
输出：第一行 "L P"（行数与总惩罚），随后 L 行，每行是 "x=int" 或 "print(x)"（x 为小写字母）。

校验条件：
  1. L 与实际行数一致；每行格式合法（变量名是单个小写字母，且最多用到 m 个变量）；
  2. 模拟程序：print 出来的序列必须与输入序列逐项相同（顺序、长度都对）；
  3. 惩罚 = 所有 "x=int" 里 int 的 popcount 之和，必须等于声明的 P；
  4. P 不超过 expected（官方输出）里的惩罚——官方输出已是最优，所以相等即证明最优；
     expected 缺失时跳过这一条（用独立暴力/对拍另行确认最优性）。
"""
import re
import sys

ASSIGN_RE = re.compile(r"^([a-z])=(\d+)$")
PRINT_RE = re.compile(r"^print\(([a-z])\)$")


def popcount(x):
    return bin(x).count("1")


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, m = int(data[0]), int(data[1])
    seq = [int(x) for x in data[2:2 + n]]

    lines = [l.strip() for l in open(sys.argv[2]).read().split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    if not lines:
        print("输出为空", file=sys.stderr)
        return 1
    head = lines[0].split()
    if len(head) != 2:
        print("第一行应为 'L P'", file=sys.stderr)
        return 1
    try:
        L, P = int(head[0]), int(head[1])
    except ValueError:
        print("第一行的两个数不是整数", file=sys.stderr)
        return 1
    body = lines[1:]
    if L != len(body):
        print(f"声明 {L} 行，实际 {len(body)} 行", file=sys.stderr)
        return 1

    var = {}
    used = set()
    penalty = 0
    printed = []
    for i, line in enumerate(body):
        ma = ASSIGN_RE.match(line)
        mp = PRINT_RE.match(line)
        if ma:
            name, val = ma.group(1), int(ma.group(2))
            used.add(name)
            var[name] = val
            penalty += popcount(val)
        elif mp:
            name = mp.group(1)
            if name not in var:
                print(f"第 {i + 2} 行 print 了未赋值的变量 {name}", file=sys.stderr)
                return 1
            printed.append(var[name])
        else:
            print(f"第 {i + 2} 行格式不对: {line!r}", file=sys.stderr)
            return 1
    if len(used) > m:
        print(f"用了 {len(used)} 个变量，超过 m={m}", file=sys.stderr)
        return 1
    if printed != seq:
        print(f"打印序列不对：得到 {printed[:10]}...，期望 {seq[:10]}...", file=sys.stderr)
        return 1
    if penalty != P:
        print(f"声明惩罚 {P}，实际 {penalty}", file=sys.stderr)
        return 1
    # 与官方输出（最优解）比较
    if len(sys.argv) > 3:
        exp = open(sys.argv[3]).read().split()
        if len(exp) >= 2:
            try:
                expP = int(exp[1])
            except ValueError:
                expP = None
            if expP is not None and P > expP:
                print(f"惩罚 {P} 比官方最优 {expP} 更差", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
