#!/usr/bin/env python3
"""CF140C New Year Snowmen 的校验器（方案不唯一）。

用法: python3 cf140c.py <input> <output> [expected]
  input：n / r_1..r_n
  output：k + k 行 "big medium small"

校验条件：
  1. 每个雪人三个半径两两不同且递减；
  2. 所有用到的半径不超过输入中该半径的出现次数；
  3. k 等于独立实现（优先队列贪心）算出的最大值。
"""
import heapq
import sys
from collections import Counter


def maxk(counter):
    h = [-v for v in counter.values()]
    heapq.heapify(h)
    k = 0
    while len(h) >= 3:
        a = -heapq.heappop(h); b = -heapq.heappop(h); c = -heapq.heappop(h)
        k += 1
        for v in (a - 1, b - 1, c - 1):
            if v > 0:
                heapq.heappush(h, -v)
    return k


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    arr = [int(t) for t in data[1:1 + n]]
    counter = Counter(arr)
    out = [ln for ln in open(sys.argv[2]).read().split('\n') if ln.strip()]
    k = int(out[0])
    if k != maxk(counter):
        print('FAIL: k 不是最大，', k, 'vs', maxk(counter))
        return 1
    used = Counter()
    for ln in out[1:1 + k]:
        t = [int(x) for x in ln.split()]
        if len(t) != 3 or len(set(t)) != 3 or not (t[0] > t[1] > t[2]):
            print('FAIL: 三元组非法', t)
            return 1
        for x in t:
            used[x] += 1
    for x, v in used.items():
        if v > counter[x]:
            print('FAIL: 半径用量超限', x, v, counter[x])
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
