#!/usr/bin/env python3
"""CF2249F 校验器（特殊评测：输出任意一条最短偶长度简单路径）。

用法: cf2249f.py <input> <output> <answer>

逐测试组校验：
  1) 若输出 -1：用奇偶分层 BFS 独立确认 1 到 n 确实不存在偶长度路径；
  2) 否则：k 为偶数；k+1 个顶点构成简单路径（顶点互异）；
     p0=1、pk=n；相邻顶点之间有边；且 k 等于分层 BFS 算出的最短偶长度。
"""
import sys
from collections import deque


def fail(msg):
    print("WRONG: " + msg)
    sys.exit(1)


def main():
    inp = open(sys.argv[1], encoding='utf-8').read().split()
    out_lines = [ln for ln in open(sys.argv[2], encoding='utf-8').read().split('\n') if ln.strip() != '']
    it = iter(inp)
    T = int(next(it))
    oi = 0
    for _ in range(T):
        n, m = int(next(it)), int(next(it))
        adj = [[] for _ in range(n + 1)]
        eset = set()
        for _ in range(m):
            u, v = int(next(it)), int(next(it))
            adj[u].append(v)
            adj[v].append(u)
            eset.add((u, v) if u < v else (v, u))
        # 奇偶分层 BFS：(顶点, 奇偶) —— 起点为 1、长度 0（偶）
        INF = -1
        dist = [[INF, INF] for _ in range(n + 1)]
        dist[1][0] = 0
        dq = deque([(1, 0)])
        while dq:
            v, p = dq.popleft()
            for w in adj[v]:
                np = p ^ 1
                if dist[w][np] == INF:
                    dist[w][np] = dist[v][p] + 1
                    dq.append((w, np))
        best = dist[n][0]  # 1→n 的最短偶长度

        if oi >= len(out_lines):
            fail("输出行数不足")
        first = out_lines[oi].strip()
        if first == '-1':
            oi += 1
            if best != INF:
                fail("存在偶长度路径（最短 %d），不应输出 -1" % best)
            continue
        if not first.lstrip('-').isdigit():
            fail("无法解析的行: " + first)
        k = int(first)
        oi += 1
        if best == INF:
            fail("不存在偶长度路径，应输出 -1")
        if k != best:
            fail("长度 %d 不是最短偶长度（应为 %d）" % (k, best))
        if k % 2 != 0:
            fail("长度 %d 不是偶数" % k)
        if oi >= len(out_lines):
            fail("缺少路径行")
        parts = out_lines[oi].split()
        oi += 1
        if len(parts) != k + 1:
            fail("应有 %d 个顶点，实际 %d 个" % (k + 1, len(parts)))
        try:
            path = [int(x) for x in parts]
        except ValueError:
            fail("路径含非数字")
        if path[0] != 1 or path[k] != n:
            fail("路径端点应为 1 和 %d" % n)
        if len(set(path)) != len(path):
            fail("路径顶点重复，不是简单路径")
        for a, b in zip(path, path[1:]):
            if ((a, b) if a < b else (b, a)) not in eset:
                fail("边 (%d, %d) 不存在" % (a, b))
    if oi != len(out_lines):
        fail("输出含多余行")


main()
