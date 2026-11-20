#!/usr/bin/env python3
"""CF134C Swaps 的校验器（方案不唯一，特殊评测）。

用法: python3 cf134c.py <input> <output> [expected]
  input：n s / c_1..c_n
  output：No，或 Yes + k + k 行 "a b"

校验条件：
  1. 可行性用独立的 Havel–Hakimi 判定（并要求 Σc=s、Σc 偶、c_i≤n-1）；
  2. 输出 No 时必须确实不可行；
  3. 输出 Yes 时必须是 k 条边、无自环、无重边，且每个点的度数恰为 c_i。
"""
import sys


def feasible(c, n):
    if sum(c) % 2 != 0 or any(x < 0 or x > n - 1 for x in c):
        return False
    d = sorted(c, reverse=True)
    while d and d[0] > 0:
        k = d[0]
        d = d[1:]
        if k > len(d):
            return False
        for i in range(k):
            d[i] -= 1
            if d[i] < 0:
                return False
        d.sort(reverse=True)
    return True


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, s = int(data[0]), int(data[1])
    c = [int(t) for t in data[2:2 + n]]
    out = open(sys.argv[2]).read().split('\n')
    first = out[0].strip()
    ok_possible = (sum(c) == s) and feasible(c, n)
    if first == 'No':
        if ok_possible:
            print('FAIL: 可行却输出 No')
            return 1
        return 0
    if first != 'Yes':
        print('FAIL: 首行既不是 Yes 也不是 No')
        return 1
    if not ok_possible:
        print('FAIL: 不可行却输出 Yes')
        return 1
    k = int(out[1].strip())
    seen = set()
    deg = [0] * n
    for line in out[2:2 + k]:
        a, b = (int(x) - 1 for x in line.split())
        if not (0 <= a < n and 0 <= b < n) or a == b:
            print('FAIL: 非法端点', a, b)
            return 1
        e = (min(a, b), max(a, b))
        if e in seen:
            print('FAIL: 重边', e)
            return 1
        seen.add(e)
        deg[a] += 1
        deg[b] += 1
    if deg != c:
        print('FAIL: 度数不符', deg, c)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
