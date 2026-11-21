#!/usr/bin/env python3
"""CF288C 的 checker（多解）：校验第一行是最大美丽值、第二行是排列且美丽值等于它。"""
import sys

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(open(inp).read().split()[0])
    toks = open(out).read().split()
    if len(toks) != n + 2:
        print('CHECKER FAIL: 需要 1+%d 个数，实际 %d' % (n + 1, len(toks)))
        return 1
    m = int(toks[0])
    p = [int(x) for x in toks[1:]]
    if sorted(p) != list(range(0, n + 1)):
        print('CHECKER FAIL: 第二行不是 0..%d 的排列' % n)
        return 1
    real = sum(i ^ p[i] for i in range(n + 1))
    if real != m:
        print('CHECKER FAIL: 排列的美丽值 %d != 声明的 %d' % (real, m))
        return 1
    std = int(open(ans).read().split()[0])
    if m != std:
        print('CHECKER FAIL: 美丽值 %d != 标准答案 %d' % (m, std))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
