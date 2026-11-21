#!/usr/bin/env python3
"""CF 228E The Road to Berland is Paved With Good Intentions 的 checker。

校验：答案要么是 Impossible（与参考解一致时才算对——但本题多解，这里只校验
"给出方案时方案合法"；若输出 Impossible 而输入其实可行，则判定失败），要么是
至多 n 个城市编号，按顺序模拟翻转后所有道路都变成 1。

用法：python3 cf228e.py <input> <output> <answer>
"""
import sys


def main():
    data = open(sys.argv[1]).read().split()
    n, m = int(data[0]), int(data[1])
    edges = []
    p = 2
    for _ in range(m):
        edges.append((int(data[p]), int(data[p + 1]), int(data[p + 2])))
        p += 3
    tokens = open(sys.argv[2]).read().split()
    if not tokens:
        print('CHECKER FAIL: 输出为空')
        return 1
    if tokens[0] == 'Impossible':
        # 只有当真的无解时才算对：用并查集独立判定
        parent = list(range(n + 1))
        xr = [0] * (n + 1)

        def find(x):
            if parent[x] == x:
                return x
            r = find(parent[x])
            xr[x] ^= xr[parent[x]]
            parent[x] = r
            return r

        for a, b, c in edges:
            ra, rb = find(a), find(b)
            want = 1 ^ c
            if ra == rb:
                if (xr[a] ^ xr[b]) != want:
                    return 0
            else:
                parent[ra] = rb
                xr[ra] = xr[a] ^ xr[b] ^ want
        print('CHECKER FAIL: 有解却输出 Impossible')
        return 1
    try:
        x = int(tokens[0])
        picks = [int(v) for v in tokens[1:1 + x]]
    except ValueError:
        print('CHECKER FAIL: 无法解析输出')
        return 1
    if len(picks) != x or x > n:
        print('CHECKER FAIL: 天数与列表长度不符或超过 n')
        return 1
    if any(not (1 <= v <= n) for v in picks):
        print('CHECKER FAIL: 城市编号越界')
        return 1
    flip = [0] * (n + 1)
    for v in picks:
        flip[v] ^= 1
    for a, b, c in edges:
        if (c ^ flip[a] ^ flip[b]) != 1:
            print('CHECKER FAIL: 仍有未沥青的道路')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
