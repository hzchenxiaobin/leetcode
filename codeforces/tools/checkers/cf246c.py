#!/usr/bin/env python3
"""CF246C Beauty Pageant 校验器（多解）。

约定：python3 cf246c.py <input> <output> <answer>，返回 0 表示通过。
校验条件：恰好 k 行；每行 "c p1 .. pc"，1<=c<=n，给出的美丽值互不相同、
都来自输入数组（且使用次数不超过该值的出现次数——输入保证互不相同，故直接
检查每个值至多出现一次），且 k 行的和两两不同。
"""
import sys
from collections import Counter


def main():
    if len(sys.argv) < 3:
        print('CHECKER FAIL: 用法 cf246c.py <input> <output> <answer>')
        sys.exit(1)
    data = open(sys.argv[1]).read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    cnt = Counter(a)
    lines = [l for l in open(sys.argv[2]).read().split('\n') if l.strip()]

    def bad(msg):
        print('CHECKER FAIL:', msg)
        sys.exit(1)

    if len(lines) != k:
        bad('需要 %d 行，实际 %d 行' % (k, len(lines)))
    sums = set()
    for i, line in enumerate(lines):
        v = list(map(int, line.split()))
        c = v[0]
        sel = v[1:]
        if c != len(sel) or c < 1:
            bad('第 %d 行计数与元素个数不符' % (i + 1))
        if len(set(sel)) != c:
            bad('第 %d 行有重复士兵' % (i + 1))
        used = Counter(sel)
        for x, t in used.items():
            if cnt[x] < t:
                bad('第 %d 行使用了不存在的美丽值 %d' % (i + 1, x))
        s = sum(sel)
        if s in sums:
            bad('第 %d 行的和 %d 与前面重复' % (i + 1, s))
        sums.add(s)


if __name__ == '__main__':
    main()
