#!/usr/bin/env python3
"""CF260D Black and White Tree 的 checker（多解）。

输出 n-1 条边 (u,v,w)：要求构成一棵树、两端颜色不同、权非负，
且每个点的"关联边权和"等于输入的 s_v。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    col = [0] * (n + 1); s = [0] * (n + 1)
    pos = 1
    for i in range(1, n + 1):
        col[i] = int(data[pos]); s[i] = int(data[pos + 1]); pos += 2
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if len(out) != 3 * (n - 1):
        print('WA: 应输出 %d 条边' % (n - 1))
        return 1
    par = list(range(n + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    tot = [0] * (n + 1)
    p = 0
    for _ in range(n - 1):
        u, v, w = int(out[p]), int(out[p + 1]), int(out[p + 2]); p += 3
        if not (1 <= u <= n and 1 <= v <= n) or u == v:
            print('WA: 边的端点非法')
            return 1
        if not (0 <= w <= 10**9):
            print('WA: 边权越界')
            return 1
        if col[u] == col[v]:
            print('WA: 边 (%d,%d) 两端同色' % (u, v))
            return 1
        a, b = find(u), find(v)
        if a == b:
            print('WA: 出现环')
            return 1
        par[a] = b
        tot[u] += w; tot[v] += w
    for v in range(1, n + 1):
        if tot[v] != s[v]:
            print('WA: 点 %d 的边权和 %d 应为 %d' % (v, tot[v], s[v]))
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
