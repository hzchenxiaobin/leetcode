#!/usr/bin/env python3
"""51C checker: 校验输出两行（d 与三个基站坐标），确认 d 与最优值一致且覆盖所有房屋。

用法: python3 checker.py <input> <output> <answer|/dev/stdin>
输出: 退出码 0 通过，1 拒绝（stderr 给出原因）。
"""
import re
import sys

EPS = 1e-6


def optimal_two_d(x):
    """二分最小整数 k = 2d，使 3 个长度 k 的区间能盖住全部点。"""
    x = sorted(x)
    n = len(x)

    def ok(k):
        i = 0
        for _ in range(3):
            if i >= n:
                return True
            reach = x[i] + k
            while i < n and x[i] <= reach:
                i += 1
        return i >= n

    lo, hi = 0, x[-1] - x[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def main() -> None:
    inp_path, out_path = sys.argv[1], sys.argv[2]
    data = open(inp_path).read().split()
    n = int(data[0])
    x = [int(v) for v in data[1:1 + n]]
    out = open(out_path).read()
    raw = out.strip("\n")
    if not raw.strip():
        print("checker: empty output", file=sys.stderr)
        sys.exit(1)
    lines = [l for l in raw.split("\n") if l.strip()]
    if len(lines) != 2:
        print(f"checker: expected 2 non-empty lines, got {len(lines)}", file=sys.stderr)
        sys.exit(1)
    first = lines[0].split()
    second = lines[1].split()
    if len(first) != 1 or len(second) != 3:
        print(f"checker: wrong token counts {len(first)} {len(second)}", file=sys.stderr)
        sys.exit(1)
    num = re.compile(r"^[+-]?\d+(?:\.\d+)?$")
    if not all(num.match(t) for t in first + second):
        print("checker: non-numeric token", file=sys.stderr)
        sys.exit(1)
    d = float(first[0])
    pos = [float(t) for t in second]
    if d < -EPS:
        print("checker: negative d", file=sys.stderr)
        sys.exit(1)
    two_d = optimal_two_d(x)
    opt = two_d / 2.0
    if abs(d - opt) > EPS:
        print(f"checker: d={d} but optimum={opt}", file=sys.stderr)
        sys.exit(1)
    for p in pos:
        if p < -EPS or p > 2e9 + EPS:
            print(f"checker: station {p} out of [0,2e9]", file=sys.stderr)
            sys.exit(1)
    for v in x:
        if not any(abs(v - p) <= d + EPS for p in pos):
            print(f"checker: house {v} not covered (d={d}, pos={pos})", file=sys.stderr)
            sys.exit(1)
    sys.exit(0)


main()
