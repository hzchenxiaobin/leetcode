#!/usr/bin/env python3
"""CF272E Dima and Horses 的 checker（多解）。

输出 n 个 0/1，要求每个骑士在本党内的敌人数 <= 1。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    p = 2
    for _ in range(m):
        a, b = int(data[p]), int(data[p + 1]); p += 2
        adj[a].append(b); adj[b].append(a)
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out and out[0] == '-1':
        return 0
    s = out[0] if out else ''
    if len(s) != n:
        print('WA: 应输出 %d 个字符' % n)
        return 1
    for v in range(1, n + 1):
        if s[v - 1] not in '01':
            print('WA: 只能包含 0/1')
            return 1
        bad = sum(1 for u in adj[v] if s[u - 1] == s[v - 1])
        if bad > 1:
            print('WA: 骑士 %d 党内有 %d 个敌人' % (v, bad))
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
