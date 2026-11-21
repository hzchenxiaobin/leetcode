#!/usr/bin/env python3
"""CF243B Hydra 校验器（多解）。

约定：python3 cf243b.py <input> <output> <answer>，返回 0 表示通过。
校验条件：
1. YES：u,v 必须是图中的边；给出恰好 h 个「头」与 t 个「尾」，
   头都与 u 相邻且不等于 v，尾都与 v 相邻且不等于 u，且 h+t+2 个点两两不同。
2. NO：n 较小时用独立判定（枚举每条边，检查 |N(u)\{v}| >= h、|N(v)\{u}| >= t、
   |(N(u)\\{v}) ∪ (N(v)\\{u})| >= h+t，三者等价于存在 hydra）；n 大时只查格式。
"""
import sys

BRUTE_MAX = 400


def main():
    if len(sys.argv) < 3:
        print('CHECKER FAIL: 用法 cf243b.py <input> <output> <answer>')
        sys.exit(1)
    data = open(sys.argv[1]).read().split()
    n, m, h, t = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    adj = [set() for _ in range(n + 1)]
    p = 4
    for _ in range(m):
        a, b = int(data[p]), int(data[p + 1])
        p += 2
        adj[a].add(b)
        adj[b].add(a)
    out = open(sys.argv[2]).read().split()

    def bad(msg):
        print('CHECKER FAIL:', msg)
        sys.exit(1)

    def exists():
        for u in range(1, n + 1):
            if len(adj[u]) < h + 1:
                continue
            for v in adj[u]:
                if len(adj[v]) < t + 1:
                    continue
                A = adj[u] - {v}
                B = adj[v] - {u}
                if len(A) >= h and len(B) >= t and len(A | B) >= h + t:
                    return True
        return False

    if not out:
        bad('输出为空')
    if out[0] == 'NO':
        if len(out) != 1:
            bad('NO 之后不应再有内容')
        if n <= BRUTE_MAX and exists():
            bad('存在 hydra，但输出 NO')
        return
    if out[0] != 'YES':
        bad('第一行必须是 YES 或 NO')
    if len(out) < 3:
        bad('输出行数不足')
    u, v = int(out[1]), int(out[2])
    if not (1 <= u <= n and 1 <= v <= n):
        bad('u,v 越界')
    if v not in adj[u]:
        bad('u 与 v 不相邻')
    rest = out[3:]
    if len(rest) != h + t:
        bad('需要 h+t = %d 个点，实际 %d' % (h + t, len(rest)))
    hs = [int(x) for x in rest[:h]]
    ts = [int(x) for x in rest[h:]]
    allv = [u, v] + hs + ts
    if len(set(allv)) != len(allv):
        bad('点有重复')
    for x in hs:
        if x not in adj[u]:
            bad('头 %d 不与 %d 相邻' % (x, u))
    for x in ts:
        if x not in adj[v]:
            bad('尾 %d 不与 %d 相邻' % (x, v))


if __name__ == '__main__':
    main()
