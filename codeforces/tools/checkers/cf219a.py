#!/usr/bin/env python3
"""CF 219A k-String 的构造合法性 checker。

校验条件：
  1. 若原串各字母出现次数存在不能被 k 整除者，输出必须恰为 -1；
  2. 否则输出必须是一个与 s 等长、字母多重集相同的字符串，且形如
     "base 重复 k 次"（即前 |s|/k 个字符循环 k 遍）。

约定：python3 cf219a.py <input> <output> <answer>，返回 0 表示通过。
"""
import sys
from collections import Counter


def main():
    data = open(sys.argv[1]).read().split()
    k = int(data[0])
    s = data[1]
    cnt = Counter(s)
    possible = all(v % k == 0 for v in cnt.values())
    got = open(sys.argv[2]).read().strip()
    if not possible:
        if got != '-1':
            print(f'CHECKER FAIL: 无解时输出应为 -1，实际 {got[:40]!r}')
            return 1
        return 0
    if got == '-1':
        print('CHECKER FAIL: 有解却输出 -1')
        return 1
    if len(got) != len(s):
        print(f'CHECKER FAIL: 长度 {len(got)} != {len(s)}')
        return 1
    if Counter(got) != cnt:
        print('CHECKER FAIL: 字母多重集与原串不同')
        return 1
    L = len(s)
    if L % k != 0:
        print('CHECKER FAIL: |s| 不能被 k 整除（不应有解）')
        return 1
    base = got[:L // k]
    if got != base * k:
        print('CHECKER FAIL: 输出不是 k 个相同块的拼接')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
