#!/usr/bin/env python3
"""CF260A Adding Digits 的 checker（多解）。

输出：一个数（长度 = len(a)+n，以 a 开头，且每一步得到的前缀都能被 b 整除），或 -1。
-1 仅在"第一步就无解"时允许。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    a, b, n = int(data[0]), int(data[1]), int(data[2])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        ok = all((a * 10 + d) % b != 0 for d in range(10))
        if not ok:
            print('WA: 明明可以继续，却输出了 -1')
            return 1
        return 0
    if len(out) != 1:
        print('WA: 应输出一个整数或 -1')
        return 1
    s = out[0]
    sa = str(a)
    if not s.startswith(sa) or len(s) != len(sa) + n:
        print('WA: 长度或前缀不符（应为 %s + %d 位）' % (sa, n))
        return 1
    if not s.isdigit():
        print('WA: 非数字')
        return 1
    cur = a
    for i in range(n):
        cur = cur * 10 + int(s[len(sa) + i])
        if cur % b != 0:
            print('WA: 第 %d 步得到的 %d 不能被 %d 整除' % (i + 1, cur, b))
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
