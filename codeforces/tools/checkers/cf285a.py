#!/usr/bin/env python3
"""CF285A 的 checker（多解）：验证输出是 1..n 的排列且下降系数恰为 k。"""
import sys

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    n, k = map(int, open(inp).read().split())
    toks = open(out).read().split()
    if len(toks) != n:
        print('CHECKER FAIL: 需要 %d 个数，实际 %d' % (n, len(toks)))
        return 1
    try:
        p = [int(x) for x in toks]
    except ValueError:
        print('CHECKER FAIL: 非整数')
        return 1
    if sorted(p) != list(range(1, n + 1)):
        print('CHECKER FAIL: 不是 1..%d 的排列' % n)
        return 1
    d = sum(1 for i in range(n - 1) if p[i] > p[i + 1])
    if d != k:
        print('CHECKER FAIL: 下降系数 %d != %d' % (d, k))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
