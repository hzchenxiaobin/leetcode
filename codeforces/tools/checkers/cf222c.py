#!/usr/bin/env python3
"""222C Reducing Fractions 校验器：python3 cf222c.py <input> <output> <answer>，0 表示通过。
检查：分子/分母乘积之比的分数值等于输入分数，且已约分（gcd=1），每边至少 1 个数。"""
import sys
from math import gcd
from functools import reduce


def main() -> None:
    inp = open(sys.argv[1]).read().split()
    part = open(sys.argv[2]).read().split()
    n, m = int(inp[0]), int(inp[1])
    a = [int(x) for x in inp[2:2 + n]]
    b = [int(x) for x in inp[2 + n:2 + n + m]]
    if not part:
        print('WA: empty'); return 1
    try:
        no, mo = int(part[0]), int(part[1])
        oa = [int(x) for x in part[2:2 + no]]
        ob = [int(x) for x in part[2 + no:2 + no + mo]]
    except ValueError:
        print('WA: bad integers'); return 1
    if no < 1 or mo < 1 or no > 10 ** 5 or mo > 10 ** 5 or len(oa) != no or len(ob) != mo:
        print('WA: bad counts'); return 1
    if any(not (1 <= x <= 10 ** 7) for x in oa + ob):
        print('WA: value out of range'); return 1
    A = reduce(lambda x, y: x * y, a, 1)
    B = reduce(lambda x, y: x * y, b, 1)
    A2 = reduce(lambda x, y: x * y, oa, 1)
    B2 = reduce(lambda x, y: x * y, ob, 1)
    if A * B2 != B * A2:
        print('WA: fraction changed'); return 1
    if gcd(A2, B2) != 1:
        print('WA: not reduced'); return 1
    print('OK'); return 0


sys.exit(main())
