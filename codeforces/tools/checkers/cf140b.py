#!/usr/bin/env python3
"""CF140B New Year Cards 的校验器（方案不唯一）。

用法: python3 cf140b.py <input> <output> [expected]

规则（题意）：第 t 张卡片到达后，Alexander 手里的卡片是 1..t；他要寄给朋友 i 时，
先排除卡片 i（规则 1），再在剩下的卡片里挑自己最喜欢的那张（规则 2）。
校验条件：
  1. 输出 n 个数，都在 1..n；
  2. 每个朋友 i 收到的卡片，是他在所有可能时刻 t 里能得到的最喜欢的一张
     （按朋友 i 自己的偏好排名比较），且该时刻确实有可寄的卡片。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    pos = 1
    rank_f = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for r in range(1, n + 1):
            rank_f[i][int(data[pos])] = r
            pos += 1
    alex = [int(data[pos + r]) for r in range(n)]

    best = [0] * (n + 1)
    second = [0] * (n + 1)
    for t in range(1, n + 1):
        got = [c for c in alex if c <= t]
        best[t] = got[0] if got else 0
        second[t] = got[1] if len(got) > 1 else 0

    out = [int(v) for v in open(sys.argv[2], encoding='utf-8').read().split()]
    if len(out) != n:
        print('FAIL: 应输出 %d 个数，实际 %d' % (n, len(out)))
        return 1
    if any(not (1 <= v <= n) for v in out):
        print('FAIL: 数值越界')
        return 1
    for i in range(1, n + 1):
        got_ranks = []
        for t in range(1, n + 1):
            card = best[t] if best[t] != i else second[t]
            if card == 0:
                continue
            got_ranks.append(rank_f[i][card])
        if not got_ranks:
            print('FAIL: 朋友 %d 任何时刻都收不到卡片' % i)
            return 1
        want = min(got_ranks)
        t = out[i - 1]
        card = best[t] if best[t] != i else second[t]
        if card == 0:
            print('FAIL: 朋友 %d 在时刻 %d 没有可寄的卡片' % (i, t))
            return 1
        if rank_f[i][card] != want:
            print('FAIL: 朋友 %d 在时刻 %d 收到卡片 %d（名次 %d），本可得名次 %d'
                  % (i, t, card, rank_f[i][card], want))
            return 1
    return 0


sys.exit(main())
