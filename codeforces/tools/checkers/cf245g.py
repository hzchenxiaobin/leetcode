#!/usr/bin/env python3
"""CF245G Suggested Friends 校验器（输出顺序任意，多解）。

约定：python3 cf245g.py <input> <output> <answer>，返回 0 表示通过。
校验条件：
1. 第一行 n 必须等于输入中出现的不同用户名个数；随后恰好 n 行
   "<name> <count>"，用户名恰好是全部用户各一次；
2. count 必须等于该用户的推荐好友数：
   max_{y 非好友, y != x} |N(x) ∩ N(y)| 的取到者个数（没有候选时为 0）。
"""
import sys


def main():
    if len(sys.argv) < 3:
        print('CHECKER FAIL: 用法 cf245g.py <input> <output> <answer>')
        sys.exit(1)
    data = open(sys.argv[1]).read().split()
    m = int(data[0])
    users = []
    idx = {}
    edges = []
    p = 1
    for _ in range(m):
        a, b = data[p], data[p + 1]
        p += 2
        for nm in (a, b):
            if nm not in idx:
                idx[nm] = len(users)
                users.append(nm)
        edges.append((idx[a], idx[b]))
    n = len(users)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    want = [0] * n
    for x in range(n):
        best, cnt = -1, 0
        for y in range(n):
            if y == x or y in adj[x]:
                continue
            c = len(adj[x] & adj[y])
            if c > best:
                best, cnt = c, 1
            elif c == best:
                cnt += 1
        want[x] = max(cnt, 0) if best >= 0 else 0

    out = open(sys.argv[2]).read().split()
    def bad(msg):
        print('CHECKER FAIL:', msg)
        sys.exit(1)
    if not out:
        bad('输出为空')
    if int(out[0]) != n:
        bad('用户数应为 %d，实际 %s' % (n, out[0]))
    if len(out) != 1 + 2 * n:
        bad('需要 1 + 2n 个 token，实际 %d' % len(out))
    seen = set()
    for i in range(n):
        nm = out[1 + 2 * i]
        val = int(out[2 + 2 * i])
        if nm not in idx:
            bad('未知用户名 %r' % nm)
        if nm in seen:
            bad('用户名重复 %r' % nm)
        seen.add(nm)
        if val != want[idx[nm]]:
            bad('%s 的推荐好友数应为 %d，实际 %d' % (nm, want[idx[nm]], val))


if __name__ == '__main__':
    main()
