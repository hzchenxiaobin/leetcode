#!/usr/bin/env python3
"""CF266D BerDonalds 的 checker（浮点，误差 1e-9）。"""
import sys


def main():
    out = open(sys.argv[2], encoding='utf-8').read().split()
    ans = open(sys.argv[3], encoding='utf-8').read().split()
    if len(out) != 1:
        print('WA: 应输出一个实数')
        return 1
    a = float(out[0])
    b = float(ans[0]) if ans else None
    if b is None:
        print('NO_ANSWER')
        return 1
    if abs(a - b) > 1e-9 * max(1.0, abs(b)):
        print('WA: %.12f vs %.12f' % (a, b))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
