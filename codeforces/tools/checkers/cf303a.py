#!/usr/bin/env python3
"""CF303A 的 checker（多解）：校验输出要么是合法的排列三元组，要么是正解的 -1。"""
import sys

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(open(inp).read().split()[0])
    toks = open(out).read().split()
    if toks == ['-1']:
        if n % 2 == 0:
            return 0
        print('CHECKER FAIL: 奇数 n 有解，不能输出 -1')
        return 1
    if len(toks) != 3 * n:
        print('CHECKER FAIL: 需要 3n = %d 个数，实际 %d' % (3 * n, len(toks)))
        return 1
    vals = list(map(int, toks))
    a, b, c = vals[:n], vals[n:2 * n], vals[2 * n:]
    want = list(range(n))
    for name, arr in (('a', a), ('b', b), ('c', c)):
        if sorted(arr) != want:
            print('CHECKER FAIL: %s 不是 0..%d 的排列' % (name, n - 1))
            return 1
    for i in range(n):
        if (a[i] + b[i]) % n != c[i] % n:
            print('CHECKER FAIL: 第 %d 位 a+b != c (mod n)' % i)
            return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
