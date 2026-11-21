#!/usr/bin/env python3
"""CF244A Dividing Orange 校验器（每个孩子的编号顺序任意，多解）。

约定：python3 cf244a.py <input> <output> <answer>，返回 0 表示通过。
校验条件：
1. 输出必须恰好 n*k 个整数，且是 1..n*k 的一个排列（每个分段恰好分给一个人）；
2. 每 n 个整数为一组，共 k 组；第 i 组必须包含 a_i；
3. 组内不能有重复（由第 1 条的全排列性质保证，但仍逐组检查）。
"""
import sys


def main():
    if len(sys.argv) < 3:
        print('CHECKER FAIL: 用法 cf244a.py <input> <output> <answer>')
        sys.exit(1)
    data = open(sys.argv[1]).read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + k]]
    out = open(sys.argv[2]).read().split()

    def bad(msg):
        print('CHECKER FAIL:', msg)
        sys.exit(1)

    total = n * k
    if len(out) != total:
        bad('需要 %d 个整数，实际 %d 个' % (total, len(out)))
    vals = []
    for t in out:
        try:
            vals.append(int(t))
        except ValueError:
            bad('非整数: %r' % t)
    if sorted(vals) != list(range(1, total + 1)):
        bad('输出不是 1..n*k 的排列')
    for i in range(k):
        grp = vals[i * n:(i + 1) * n]
        if len(set(grp)) != n:
            bad('第 %d 组有重复编号' % (i + 1))
        if a[i] not in grp:
            bad('第 %d 组没有包含 a_i=%d' % (i + 1, a[i]))


if __name__ == '__main__':
    main()
