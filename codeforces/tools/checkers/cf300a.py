#!/usr/bin/env python3
"""CF300A Array 的 checker（多解）：把数组分成三个非空集合，乘积分别 <0、>0、=0。"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0]); vals = [int(v) for v in data[1:1 + n]]
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if len(out) < 6:
        print('WA: 输出太短'); return 1
    idx = 0; sets = []
    for _ in range(3):
        if idx >= len(out):
            print('WA: 缺少分组'); return 1
        k = int(out[idx]); idx += 1
        if k <= 0:
            print('WA: 存在空集合'); return 1
        if idx + k > len(out):
            print('WA: 元素个数不足'); return 1
        sets.append([int(x) for x in out[idx:idx + k]]); idx += k
    if idx != len(out):
        print('WA: 多余输出'); return 1
    flat = sorted(x for s in sets for x in s)
    if flat != sorted(vals):
        print('WA: 分组不是原数组的划分'); return 1
    prod = []
    for s in sets:
        p = 1
        for x in s:
            p *= x
        prod.append(p)
    if not (prod[0] < 0 and prod[1] > 0 and prod[2] == 0):
        print('WA: 乘积条件不满足 %s' % prod); return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
