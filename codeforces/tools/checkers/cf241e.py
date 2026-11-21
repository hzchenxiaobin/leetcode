#!/usr/bin/env python3
"""CF241E Flights 校验器（多解 + No 需独立判定）。

约定：python3 cf241e.py <input> <output> <answer>，返回 0 表示输出合法。
因为答案不唯一（样例 3 的官方输出就与参考解不同），这里只校验合法性：

1. 若输出为 No：用差分约束（Bellman-Ford 找正环）独立判定「确实不可行」；
   若实际可行则拒绝。
2. 若输出为 Yes：必须恰好 m 个整数，每个属于 {1,2}；把 1..n 的所有路线
   看成 DAG，用两次 DP 求 1 -> n 路线长度的最小值 mn 与最大值 mx，
   只有 mn == mx 才说明「每条 1 -> n 的路线等长」，否则拒绝。
3. 其他输出（token 不匹配 / 行数不对）一律拒绝。
"""
import sys


def fail(msg):
    print('CHECKER FAIL:', msg)
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        fail('用法: cf241e.py <input> <output> <answer>')
    it = iter(open(sys.argv[1]).read().split())
    try:
        n = int(next(it)); m = int(next(it))
    except StopIteration:
        fail('输入不完整')
    a = [0] * m
    b = [0] * m
    out_edges = [[] for _ in range(n + 1)]
    in_edges = [[] for _ in range(n + 1)]
    for i in range(m):
        a[i] = int(next(it)); b[i] = int(next(it))
        if not (1 <= a[i] < b[i] <= n):
            fail('输入边不满足 a_i < b_i')
        out_edges[a[i]].append((b[i], i))
        in_edges[b[i]].append(a[i])

    # 落在某条 1 -> n 路径上的点 / 边
    fr = [False] * (n + 1)
    fr[1] = True
    for v in range(1, n + 1):
        if fr[v]:
            for to, _ in out_edges[v]:
                fr[to] = True
    br = [False] * (n + 1)
    br[n] = True
    for v in range(n, 0, -1):
        if br[v]:
            for s in in_edges[v]:
                br[s] = True
    rel = [i for i in range(m) if fr[a[i]] and br[b[i]]]

    if not fr[n]:
        fail('输入不满足「保证存在 1 -> n 的路线」')

    # 差分约束可行性：d[v] >= d[u]+1 与 d[u] >= d[v]-2，无正环即可行
    feasible = True
    d = [0] * (n + 1)
    for it_r in range(n + 1):
        changed = False
        for i in rel:
            u, v = a[i], b[i]
            if d[v] < d[u] + 1:
                d[v] = d[u] + 1; changed = True
            if d[u] < d[v] - 2:
                d[u] = d[v] - 2; changed = True
        if not changed:
            break
        if it_r == n:
            feasible = False
            break

    toks = open(sys.argv[2]).read().split()
    if not toks:
        fail('输出为空')
    if toks[0].lower() == 'no':
        if len(toks) != 1:
            fail('No 之后不应再有内容')
        if feasible:
            fail('答案不可行，但输出 No')
        return
    if toks[0].lower() != 'yes':
        fail('第一行必须是 Yes 或 No')
    if not feasible:
        fail('答案可行，但输出 No 之外的内容（应为 Yes）')
    w = toks[1:]
    if len(w) != m:
        fail('期望 %d 个航程，实际 %d 个' % (m, len(w)))
    wv = []
    for t in w:
        try:
            x = int(t)
        except ValueError:
            fail('航程不是整数: %r' % t)
        if x not in (1, 2):
            fail('航程必须为 1 或 2，实际 %d' % x)
        wv.append(x)

    INF = 10 ** 18
    mn = [INF] * (n + 1)
    mx = [-INF] * (n + 1)
    mn[1] = mx[1] = 0
    # 按顶点编号从小到大推进（a_i < b_i 保证这是拓扑序）
    for v in range(1, n + 1):
        if mn[v] >= INF:
            continue
        for to, i in out_edges[v]:
            if mn[v] + wv[i] < mn[to]:
                mn[to] = mn[v] + wv[i]
            if mx[v] + wv[i] > mx[to]:
                mx[to] = mx[v] + wv[i]
    if mn[n] >= INF:
        fail('按输出的航程，1 无法到达 n')
    if mn[n] != mx[n]:
        fail('不同 1 -> n 路线耗时不同：最短 %d，最长 %d' % (mn[n], mx[n]))


if __name__ == '__main__':
    main()
