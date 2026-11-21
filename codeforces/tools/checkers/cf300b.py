#!/usr/bin/env python3
"""CF300B Coach 的 checker（多解）：每队三人、覆盖全体、满足全部"必须同队"约束。"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, m = int(data[0]), int(data[1])
    pairs = []
    p = 2
    for _ in range(m):
        pairs.append((int(data[p]), int(data[p + 1]))); p += 2
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        return 0
    if len(out) != n:
        print('WA: 应输出 %d 个数，实际 %d' % (n, len(out))); return 1
    grp = {}
    for t in range(n // 3):
        team = out[3 * t:3 * t + 3]
        for x in team:
            x = int(x)
            if not (1 <= x <= n):
                print('WA: 编号越界'); return 1
            if x in grp:
                print('WA: 学生 %d 重复' % x); return 1
            grp[x] = t
    if sorted(grp) != list(range(1, n + 1)):
        print('WA: 没有覆盖全体'); return 1
    for a, b in pairs:
        if grp[a] != grp[b]:
            print('WA: 约束 (%d,%d) 未满足' % (a, b)); return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
