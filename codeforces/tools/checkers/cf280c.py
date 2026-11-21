#!/usr/bin/env python3
"""CF280C Game on Tree 的 checker（浮点期望，相对/绝对误差 1e-6）。"""
import sys


def main():
    ans = open(sys.argv[3], encoding='utf-8').read().split()
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if not out:
        print('WA: 空输出')
        return 1
    try:
        a = float(ans[0]); b = float(out[0])
    except ValueError:
        print('WA: 输出不是实数')
        return 1
    if abs(a - b) <= 1e-6 or abs(a - b) <= 1e-6 * abs(a):
        return 0
    print('WA: 期望 %.10f 实际 %.10f' % (a, b))
    return 1


if __name__ == '__main__':
    sys.exit(main())
