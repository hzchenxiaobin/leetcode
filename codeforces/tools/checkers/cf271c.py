#!/usr/bin/env python3
"""CF271C Secret 的 checker（多解）。

输出 n 个 1..k 的整数（第 i 个表示第 i 个词分给谁），要求：
每个 Keeper 得到的词数 >= 3（且非空），且每组词不构成等差数列。
-1 表示无解（仅当 3k > n 时允许）。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, k = int(data[0]), int(data[1])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        if 3 * k <= n:
            print('WA: 3k <= n 时应当有解')
            return 1
        return 0
    if len(out) != n:
        print('WA: 应输出 %d 个数' % n)
        return 1
    groups = [[] for _ in range(k + 1)]
    for i, v in enumerate(out):
        g = int(v)
        if not (1 <= g <= k):
            print('WA: Keeper 编号越界')
            return 1
        groups[g].append(i + 1)
    for g in range(1, k + 1):
        s = sorted(groups[g])
        if len(s) < 3:
            print('WA: Keeper %d 只有 %d 个词（<3）' % (g, len(s)))
            return 1
        d = s[1] - s[0]
        if all(s[i + 1] - s[i] == d for i in range(len(s) - 1)):
            print('WA: Keeper %d 的词构成等差数列' % g)
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
