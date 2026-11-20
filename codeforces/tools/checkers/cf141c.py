#!/usr/bin/env python3
"""CF141C Queue 的校验器（方案不唯一，输出 -1 也可判定）。

用法: python3 cf141c.py <input> <output> [expected]

校验条件：
  1. 可行性判据：把 a 升序排列后须满足 a_(k) <= k（0 起算），否则答案必须是 -1；
  2. 输出非 -1 时：人名恰好是输入的每个人各一次、身高的整数在 [1, 10^9]；
  3. 逐位置统计「前面比他高的人数」，必须等于该人的 a。
"""
import sys


def main() -> int:
    lines = [ln.strip() for ln in open(sys.argv[1], encoding='utf-8') if ln.strip()]
    n = int(lines[0])
    a_of, names = {}, []
    for ln in lines[1:1 + n]:
        name, a = ln.split()
        a_of[name] = int(a)
        names.append(name)
    feasible = all(v <= k for k, v in enumerate(sorted(a_of.values())))

    out = [ln.strip() for ln in open(sys.argv[2], encoding='utf-8') if ln.strip()]
    if len(out) == 1 and out[0] == '-1':
        return 0 if not feasible else 1
    if not feasible:
        print('FAIL: 不可行却给出了方案')
        return 1
    if len(out) != n:
        print('FAIL: 输出行数不是 n')
        return 1
    seen, hs = set(), []
    for ln in out:
        parts = ln.split()
        if len(parts) != 2:
            print('FAIL: 行格式', ln)
            return 1
        name, h = parts[0], parts[1]
        if name not in a_of or name in seen:
            print('FAIL: 人名非法或重复', name)
            return 1
        seen.add(name)
        try:
            hv = int(h)
        except ValueError:
            print('FAIL: 身高不是整数', h)
            return 1
        if not (1 <= hv <= 10 ** 9):
            print('FAIL: 身高越界', hv)
            return 1
        hs.append((name, hv))
    if seen != set(names):
        print('FAIL: 人名集合不符')
        return 1
    for i, (name, hv) in enumerate(hs):
        taller = sum(1 for j in range(i) if hs[j][1] > hv)
        if taller != a_of[name]:
            print('FAIL: %s 前面比他高的人数 %d != a=%d' % (name, taller, a_of[name]))
            return 1
    return 0


sys.exit(main())
