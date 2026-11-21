#!/usr/bin/env python3
"""CF286A 的 checker（多解）：验证 p 是 1..n 的排列且 p[p[i]] = n-i+1。"""
import sys

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(open(inp).read().split()[0])
    toks = open(out).read().split()
    if n % 4 in (2, 3):
        if toks and toks[0] == '-1':
            return 0
        print('CHECKER FAIL: 应输出 -1')
        return 1
    if len(toks) != n:
        print('CHECKER FAIL: 需要 %d 个数，实际 %d' % (n, len(toks)))
        return 1
    p = [0] + [int(x) for x in toks]
    if sorted(p[1:]) != list(range(1, n + 1)):
        print('CHECKER FAIL: 不是 1..%d 的排列' % n)
        return 1
    for i in range(1, n + 1):
        if p[p[i]] != n - i + 1:
            print('CHECKER FAIL: p[p[%d]] = %d != %d' % (i, p[p[i]], n - i + 1))
            return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
