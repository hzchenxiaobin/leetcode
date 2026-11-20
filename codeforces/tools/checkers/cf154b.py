#!/usr/bin/env python3
"""CF154B Colliders 的答案校验器（"Conflict with j" 里的 j 可以是任意冲突者）。

用法: python3 cf154b.py <input> <output> <expected>

逐条校验：Success / Already on / Already off 必须严格正确；"Conflict with j" 中的 j
必须当时处于激活状态，且 gcd(i, j) > 1（即确实冲突）。同时按规则模拟状态。
"""
import sys
from math import gcd


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, m = int(data[0]), int(data[1])
    ops = []
    p = 2
    for _ in range(m):
        ops.append((data[p], int(data[p + 1])))
        p += 2

    out = [l.strip() for l in open(sys.argv[2]).read().split("\n") if l.strip()]
    if len(out) != m:
        print(f"应输出 {m} 行，实际 {len(out)} 行", file=sys.stderr)
        return 1

    on = set()
    for idx, ((op, x), line) in enumerate(zip(ops, out)):
        if op == '+':
            if x in on:
                if line != "Already on":
                    print(f"第 {idx + 1} 条应为 Already on，实际 {line!r}", file=sys.stderr)
                    return 1
                continue
            conflict = next((y for y in on if gcd(x, y) > 1), None)
            if conflict is None:
                if line != "Success":
                    print(f"第 {idx + 1} 条应为 Success，实际 {line!r}", file=sys.stderr)
                    return 1
                on.add(x)
            else:
                if not line.startswith("Conflict with "):
                    print(f"第 {idx + 1} 条应为 Conflict with …，实际 {line!r}", file=sys.stderr)
                    return 1
                try:
                    j = int(line.split()[-1])
                except ValueError:
                    print(f"第 {idx + 1} 条冲突编号非法", file=sys.stderr)
                    return 1
                if j not in on or gcd(x, j) == 1:
                    print(f"第 {idx + 1} 条冲突编号 {j} 不合法", file=sys.stderr)
                    return 1
        else:
            if x not in on:
                if line != "Already off":
                    print(f"第 {idx + 1} 条应为 Already off，实际 {line!r}", file=sys.stderr)
                    return 1
            else:
                if line != "Success":
                    print(f"第 {idx + 1} 条应为 Success，实际 {line!r}", file=sys.stderr)
                    return 1
                on.discard(x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
