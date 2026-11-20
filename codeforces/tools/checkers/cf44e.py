#!/usr/bin/env python3
"""CF44E checker：校验分段方案。

用法：python3 checker.py <input> <output> <answer>
通过条件：
  1. 若 std 输出 "No solution"，则 output 必须也只输出 "No solution"（且本 checker 独立判定确实无解）；
  2. 否则 output 必须恰好 k 行，每行长度在 [a,b] 内，拼接后与原串完全一致，
     并且独立判定确实有解（否则 std 的 "No solution" 会被判错）。
"""
import sys


def solve_exists(k, a, b, n):
    return k * a <= n <= k * b


def main():
    inp, out, _ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    k, a, b = int(data[0]), int(data[1]), int(data[2])
    s = data[3]
    n = len(s)
    exists = solve_exists(k, a, b, n)

    lines = [l for l in open(out).read().split('\n')]
    while lines and lines[-1] == '':
        lines.pop()

    if lines == ['No solution']:
        ok = not exists
        if not ok:
            print('checker: 有解却输出 No solution')
        sys.exit(0 if ok else 1)

    if not exists:
        print('checker: 无解却输出了方案')
        sys.exit(1)
    if len(lines) != k:
        print('checker: 行数 %d != k=%d' % (len(lines), k))
        sys.exit(1)
    for i, line in enumerate(lines):
        if not (a <= len(line) <= b):
            print('checker: 第 %d 行长度 %d 不在 [%d,%d]' % (i + 1, len(line), a, b))
            sys.exit(1)
        if any(ch < 'a' or ch > 'z' for ch in line):
            print('checker: 第 %d 行含非小写字母' % (i + 1))
            sys.exit(1)
    if ''.join(lines) != s:
        print('checker: 拼接结果与原串不一致')
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
