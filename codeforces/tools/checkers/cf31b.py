#!/usr/bin/env python3
"""31B 的 checker：输出要么是 No solution（确实无解），要么是逗号分隔的合法邮箱列表，
拼起来（去掉逗号）恰好等于输入。

用法: python3 checker.py <input> <output> <answer>
"""
import re
import sys

ADDR = re.compile(r'^[a-z]+@[a-z]+$')


def solvable(s: str) -> bool:
    n = len(s)
    f = [False] * (n + 1)
    f[0] = True
    for i in range(n):
        if not f[i]:
            continue
        for j in range(i + 1, n + 1):
            if ADDR.match(s[i:j]):
                f[j] = True
    return f[n]


def main() -> int:
    s = open(sys.argv[1]).read().strip()
    out = open(sys.argv[2]).read().strip()

    if out == "No solution":
        return 0 if not solvable(s) else 1
    parts = out.split(",")
    if any(not ADDR.match(p) for p in parts):
        print("存在不合法的邮箱片段")
        return 1
    if "".join(parts) != s:
        print("拼起来与原串不一致")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
