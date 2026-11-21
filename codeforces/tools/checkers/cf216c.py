#!/usr/bin/env python3
"""216C Hiring Staff 校验器：python3 cf216c.py <input> <output> <answer>，0 表示通过。
检查：人数等于下界 max(ceil(k*T/n), ceil(T/(n-1)))、每天覆盖 >= k、钥匙可沿雇佣链传递。"""
import sys


def main() -> None:
    inp = open(sys.argv[1]).read().split()
    part = open(sys.argv[2]).read().split()
    n, m, k = int(inp[0]), int(inp[1]), int(inp[2])
    T = n + m
    need = max((k * T + n - 1) // n, (T + n - 2) // (n - 1))
    if not part:
        print('WA: empty output'); return 1
    try:
        z = int(part[0])
        days = [int(x) for x in part[1:1 + z]]
    except ValueError:
        print('WA: bad integers'); return 1
    if z != need or len(days) != z:
        print('WA: count %d, expected %d' % (z, need)); return 1
    for x in days:
        if not (1 <= x <= 10 ** 4):
            print('WA: hire day out of range'); return 1
    zero = [d - 1 for d in days]
    ds = {}
    for t in zero:
        ds[t] = ds.get(t, 0) + 1
    for d in range(T):
        cov = 0
        for t, c in ds.items():
            if (d - t) % T < n:
                cov += c
        if cov < k:
            print('WA: day %d has only %d employees' % (d + 1, cov)); return 1
    keys = sorted(ds)
    for i in range(len(keys)):
        gap = (keys[(i + 1) % len(keys)] - keys[i]) % T
        if len(keys) > 1 and gap == 0:
            gap = T
        if gap > n - 1:
            print('WA: key cannot be handed over'); return 1
    print('OK'); return 0


sys.exit(main())
