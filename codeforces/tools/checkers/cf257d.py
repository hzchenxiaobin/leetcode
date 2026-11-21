#!/usr/bin/env python3
"""CF257D Sum 的校验器（多解）。

输入：n，然后 n 个正整数 a_i（已保证 a_i <= a_{i+1} <= 2 a_i）。
输出：一行长度恰为 n 的字符串，只含 '+' 和 '-'。
要求：0 <= sum(s_i * a_i) <= a_1。
"""
import sys


def read_all():
    data = sys.stdin.read().split()
    if not data:
        return None, None
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    return n, a


def check(inp: str, out: str) -> bool:
    data = inp.split()
    if not data:
        return False
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    toks = out.split()
    if len(toks) != 1:
        print("输出必须恰好是一行符号串")
        return False
    s = toks[0]
    if len(s) != n:
        print("符号串长度应为 %d，实际 %d" % (n, len(s)))
        return False
    total = 0
    for i, ch in enumerate(s):
        if ch == '+':
            total += a[i]
        elif ch == '-':
            total -= a[i]
        else:
            print("第 %d 个字符 %r 不是 '+' 或 '-'" % (i + 1, ch))
            return False
    if total < 0 or total > a[0]:
        print("和 %d 不在 [0, %d] 内" % (total, a[0]))
        return False
    return True


if __name__ == '__main__':
    inp = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    out = open(sys.argv[2]).read() if len(sys.argv) > 2 else ''
    ok = check(inp, out)
    print("OK" if ok else "WRONG")
    sys.exit(0 if ok else 1)
