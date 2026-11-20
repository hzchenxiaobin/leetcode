#!/usr/bin/env python3
"""CF141E Clearing Up 的校验器（方案不唯一；-1 也需独立判定）。

用法: python3 cf141e.py <input> <output> [expected]

校验条件：
  1. 独立算可行性：全图连通、n-1 为偶数，且 (n-1)/2 落在 [minS, maxS] 内
     （minS / maxS 分别由「M 优先」「S 优先」两遍 Kruskal 得到，S 边数可取遍区间）；
  2. 输出 -1 时要求恰好不可行；
  3. 否则：恰好 n-1 条（n=1 时 0 条）、编号互异不越界、选出的边无环且连通、S 与 M 各占一半。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, m = int(data[0]), int(data[1])
    edges = []
    pos = 2
    for _ in range(m):
        edges.append((int(data[pos]) - 1, int(data[pos + 1]) - 1, data[pos + 2]))
        pos += 3

    def kruskal(first_s):
        p = list(range(n))

        def find(x):
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            return x

        sc = 0
        for want_s in (first_s, not first_s):
            for u, v, c in edges:
                if (c == 'S') != want_s:
                    continue
                a, b = find(u), find(v)
                if a != b:
                    p[a] = b
                    if c == 'S':
                        sc += 1
        return sc, len({find(i) for i in range(n)}) == 1

    max_s, conn = kruskal(True)
    min_s, conn2 = kruskal(False)
    conn = conn and conn2
    feasible = (n == 1) or (conn and (n - 1) % 2 == 0 and min_s <= (n - 1) // 2 <= max_s)

    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out and out[0] == '-1':
        return 0 if not feasible else 1
    if not feasible:
        print('FAIL: 不可行却给出了方案')
        return 1
    k = int(out[0])
    ids = [int(v) for v in out[1:]]
    if len(ids) != k:
        print('FAIL: 声明 %d 条，实际列出 %d 条' % (k, len(ids)))
        return 1
    if len(set(ids)) != len(ids):
        print('FAIL: 边重复')
        return 1
    if any(not (1 <= v <= m) for v in ids):
        print('FAIL: 边编号越界')
        return 1
    if n == 1:
        if k != 0:
            print('FAIL: n=1 应为 0 条')
            return 1
        return 0
    if k != n - 1:
        print('FAIL: 条数不是 n-1')
        return 1
    p = list(range(n))

    def find2(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    cs = cm = 0
    for v in ids:
        u, w, c = edges[v - 1]
        ru, rw = find2(u), find2(w)
        if ru == rw:
            print('FAIL: 选出的边成环（边 %d）' % v)
            return 1
        p[ru] = rw
        if c == 'S':
            cs += 1
        else:
            cm += 1
    if len({find2(i) for i in range(n)}) != 1:
        print('FAIL: 不连通')
        return 1
    if cs != cm:
        print('FAIL: S=%d, M=%d 不等' % (cs, cm))
        return 1
    return 0


sys.exit(main())
