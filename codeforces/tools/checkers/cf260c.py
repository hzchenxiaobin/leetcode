#!/usr/bin/env python3
"""CF260C Balls and Boxes 的 checker（多解）。

输出初始的 n 个非负整数 b[]；要求存在某个盒子 i（b[i]>=1），把 b[i] 个球依次放进
i+1, i+2, ...（循环），使得最终得到给定的 a[]，且最后一个球落在盒子 x。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, x = int(data[0]), int(data[1])
    a = [int(v) for v in data[2:2 + n]]
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if len(out) != n:
        print('WA: 应输出 %d 个整数' % n)
        return 1
    b = [int(v) for v in out]
    if any(v < 0 for v in b):
        print('WA: 初始球数不能为负')
        return 1
    x0 = x - 1
    for i in range(n):
        c = b[i]
        if c <= 0:
            continue
        if (i + c) % n != x0:          # 最后一个球必须落在 x
            continue
        R, s = divmod(c, n)
        ok = True
        for j in range(n):
            if j == i:
                got = R
                if b[i] != c or got != a[i]:
                    ok = False
                    break
                continue
            r = (j - i) % n
            got = R + 1 if r <= s else (0 if R == 0 else R)
            if b[j] < 0 or b[j] + got != a[j]:
                ok = False
                break
        if ok:
            return 0
    print('WA: 找不到任何一个被清空的盒子能重现给定的终态')
    return 1


if __name__ == '__main__':
    sys.exit(main())
