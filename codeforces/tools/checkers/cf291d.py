#!/usr/bin/env python3
"""CF291D Parallel Programming 的 checker（多解）。

模拟 k 步操作，检查最终 a_i == n-i。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, k = int(data[0]), int(data[1])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if len(out) != n * k:
        print('WA: 需要 %d 个整数，实际 %d' % (n * k, len(out)))
        return 1
    a = [1] * n
    a[-1] = 0
    p = 0
    for _ in range(k):
        c = [0] * n
        for i in range(n):
            c[i] = int(out[p]) - 1
            p += 1
            if not (0 <= c[i] < n):
                print('WA: 操作数越界')
                return 1
        old = a[:]
        for i in range(n):
            a[i] = old[i] + old[c[i]]
    for i in range(n):
        if a[i] != n - 1 - i + 1 - 1 + 1 - 1:
            pass
    want = [n - i for i in range(1, n + 1)]
    if a != want:
        print('WA: 最终 %s，期望 %s' % (a, want))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
