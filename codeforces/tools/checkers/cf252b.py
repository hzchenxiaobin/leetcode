#!/usr/bin/env python3
"""CF252B Unsorting Array 的 checker（多解）。

校验条件：
  1. 输出要么是 "-1"，要么是两个不同的下标 i<j；
  2. 若给出下标：两处元素必须不同，交换后数组既非非降也非非增；
  3. 若输出 "-1"：n 较小时用 O(n^2) 穷举确认确实不存在合法交换。

用法: python3 cf252b.py <input> <output> <answer>
"""
import sys


def sorted_ok(a):
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1)) or \
           all(a[i] >= a[i + 1] for i in range(len(a) - 1))


def exists(a):
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] == a[j]:
                continue
            b = a[:]
            b[i], b[j] = b[j], b[i]
            if not sorted_ok(b):
                return True
    return False


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        if n <= 3000 and exists(a):
            print('WA: 存在合法交换，却输出了 -1')
            return 1
        return 0
    if len(out) != 2:
        print('WA: 输出格式应为两个下标或 -1')
        return 1
    i, j = int(out[0]) - 1, int(out[1]) - 1
    if not (0 <= i < n and 0 <= j < n) or i == j:
        print('WA: 下标越界或相同')
        return 1
    if a[i] == a[j]:
        print('WA: 交换的两个数相等，题面不允许')
        return 1
    b = a[:]
    b[i], b[j] = b[j], b[i]
    if sorted_ok(b):
        print('WA: 交换后数组仍然有序')
        return 1
    return 0


sys.exit(main())
