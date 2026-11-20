#!/usr/bin/env python3
"""36E checker：两条路径覆盖全部边、互不重复、每条都是合法步行。"""
import sys


def valid_walk(edges, seq):
    if not seq:
        return False
    used = set()
    cur = None
    for idx in seq:
        if idx < 1 or idx > len(edges) or idx in used:
            return False
        used.add(idx)
        a, b = edges[idx - 1]
        if cur is None:
            # 第一条边：任选一个端点作为起点
            cur = a
            nxt = b
        else:
            if a == cur:
                nxt = b
            elif b == cur:
                nxt = a
            else:
                return False
        cur = nxt
    return True


def valid_walk_either(edges, seq):
    if not seq:
        return False
    a, b = edges[seq[0] - 1]
    for st in (a, b):
        cur = st
        ok = True
        for idx in seq:
            x, y = edges[idx - 1]
            if x == cur:
                cur = y
            elif y == cur:
                cur = x
            else:
                ok = False
                break
        if ok:
            return True
    return False


def main():
    if len(sys.argv) < 3:
        return 2
    data = list(map(int, open(sys.argv[1]).read().split()))
    m = data[0]
    edges = []
    p = 1
    for _ in range(m):
        edges.append((data[p], data[p + 1]))
        p += 2
    out = list(map(int, open(sys.argv[2]).read().split()))
    if not out:
        print("FAIL: empty output")
        return 1
    if out[0] == -1:
        if len(out) != 1:
            print("FAIL: -1 with extra tokens")
            return 1
        return 0
    idx = 0
    paths = []
    for _ in range(2):
        if idx >= len(out):
            print("FAIL: missing length")
            return 1
        L = out[idx]
        idx += 1
        if L <= 0 or idx + L > len(out):
            print(f"FAIL: bad length {L}")
            return 1
        paths.append(out[idx:idx + L])
        idx += L
    if idx != len(out):
        print("FAIL: extra tokens")
        return 1
    all_edges = paths[0] + paths[1]
    if sorted(all_edges) != list(range(1, m + 1)):
        print("FAIL: not a partition of all papers")
        return 1
    for path in paths:
        if not valid_walk_either(edges, path):
            print("FAIL: path is not a legal walk")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
