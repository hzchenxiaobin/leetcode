#!/usr/bin/env python3
"""CF282B Painting Eggs 的 checker（多解）。校验：长度 n、只含 A/G、|Sa-Sg|<=500。"""
import sys

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    d = [int(x) for x in open(inp).read().split()]
    n = d[0]
    eggs = [(d[1 + 2 * i], d[2 + 2 * i]) for i in range(n)]
    toks = open(out).read().split()
    if len(toks) != 1:
        print('CHECKER FAIL: 应输出一行，实际 %d 个 token' % len(toks))
        return 1
    s = toks[0]
    if s == '-1':
        # 独立判定：贪心的不变式说明总有解，这里用 DP/回溯确认（小 n 时才可能无解）
        from functools import lru_cache
        @lru_cache(maxsize=None)
        def can(i, diff):
            if i == n:
                return abs(diff) <= 500
            a, g = eggs[i]
            return can(i + 1, diff + a) or can(i + 1, diff - g)
        if can(0, 0):
            print('CHECKER FAIL: 输出 -1，但存在合法分配')
            return 1
        return 0
    if len(s) != n:
        print('CHECKER FAIL: 长度应为 %d，实际 %d' % (n, len(s)))
        return 1
    sa = sg = 0
    for i, ch in enumerate(s):
        if ch == 'A':
            sa += eggs[i][0]
        elif ch == 'G':
            sg += eggs[i][1]
        else:
            print('CHECKER FAIL: 第 %d 个字符非法 %r' % (i + 1, ch))
            return 1
    if abs(sa - sg) > 500:
        print('CHECKER FAIL: |Sa-Sg|=%d > 500' % abs(sa - sg))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
