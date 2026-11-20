#!/usr/bin/env python3
"""CF163D Large Refrigerator 的答案校验器（三条棱的顺序任意）。

用法: python3 cf163d.py <input> <output> <expected>

校验：每条棱为正整数、abc = V、2(ab+bc+ca) 等于官方输出给出的最小表面积。
"""
import sys


def parse_v(data, pos):
    k = int(data[pos]); pos += 1
    v = 1
    for _ in range(k):
        p = int(data[pos]); a = int(data[pos + 1]); pos += 2
        v *= p ** a
    return v, pos


def main() -> int:
    data = open(sys.argv[1]).read().split()
    t = int(data[0])
    pos = 1
    vs = []
    for _ in range(t):
        v, pos = parse_v(data, pos)
        vs.append(v)

    out = []
    for line in open(sys.argv[2]).read().split("\n"):
        parts = line.split()
        if parts:
            out.append([int(x) for x in parts])
    if len(out) != t:
        print(f"应输出 {t} 行，实际 {len(out)} 行", file=sys.stderr)
        return 1
    exp = [[int(x) for x in l.split()] for l in open(sys.argv[3]).read().split("\n") if l.strip()]
    for i in range(t):
        if len(out[i]) != 4:
            print(f"第 {i + 1} 行应为四个整数", file=sys.stderr)
            return 1
        S, a, b, c = out[i]
        if min(a, b, c) < 1:
            print("棱长必须为正", file=sys.stderr)
            return 1
        if a * b * c != vs[i]:
            print(f"abc = {a * b * c} != V = {vs[i]}", file=sys.stderr)
            return 1
        s2 = 2 * (a * b + b * c + a * c)
        if s2 != S:
            print(f"表面积 {S} 与 2(ab+bc+ca) = {s2} 不符", file=sys.stderr)
            return 1
        if i < len(exp) and exp[i]:
            if S != exp[i][0]:
                print(f"第 {i + 1} 组表面积 {S} 不是最小 {exp[i][0]}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
