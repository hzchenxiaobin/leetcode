#!/usr/bin/env python3
"""225B Well-known Numbers 校验器：python3 cf225b.py <input> <output> <answer>，0 表示通过。
检查项数 >=2、各数互异、和为 s、每个数都是 k-bonacci 数。"""
import sys


def main() -> None:
    inp = open(sys.argv[1]).read().split()
    part = open(sys.argv[2]).read().split()
    s = int(inp[0]); k = int(inp[1])
    if not part:
        print('WA: empty'); return 1
    try:
        m = int(part[0])
        vals = [int(x) for x in part[1:1 + m]]
    except ValueError:
        print('WA: bad integers'); return 1
    if m < 2 or len(vals) != m:
        print('WA: count'); return 1
    if len(set(vals)) != m:
        print('WA: duplicates'); return 1
    if sum(vals) != s:
        print('WA: sum != s'); return 1
    seq = [0]
    n = 1
    while True:
        n += 1
        if n < k:
            v = 0
        elif n == k:
            v = 1
        else:
            v = sum(seq[max(0, len(seq) - k):])
        seq.append(v)
        if (v > s and n > k) or len(seq) > 5000:
            break
    S = {x for x in seq if x <= s}
    for v in vals:
        if v not in S:
            print('WA: not k-bonacci: %d' % v); return 1
    print('OK'); return 0


sys.exit(main())
