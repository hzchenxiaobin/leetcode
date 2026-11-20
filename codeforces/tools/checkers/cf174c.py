#!/usr/bin/env python3
"""CF174C Range Increments 的合法性校验器。

用法：python3 cf174c.py <input> <output> <answer>
`answer` 由 verify_solution.py 通过 /dev/stdin 传入期望输出（第一行是最少次数）。

校验：
  1. 第一行 t 与后面的区间行数一致；
  2. 每个区间满足 1 <= l <= r <= n；
  3. 把这些区间都 +1 之后得到的数组与输入完全一致；
  4. t 等于参考输出给出的最少次数（构造题的“最少”由 jury 保证）。
退出码 0 表示通过。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if not toks:
        print('empty output')
        return 1
    t = int(toks[0])
    rest = toks[1:]
    if len(rest) != 2 * t:
        print(f'expected {2*t} numbers after t, got {len(rest)}')
        return 1
    diff = [0] * (n + 2)
    for i in range(t):
        l, r = int(rest[2 * i]), int(rest[2 * i + 1])
        if not (1 <= l <= r <= n):
            print(f'bad segment {l} {r}')
            return 1
        diff[l] += 1
        diff[r + 1] -= 1
    cur = 0
    for i in range(1, n + 1):
        cur += diff[i]
        if cur != a[i - 1]:
            print(f'position {i}: got {cur}, expected {a[i-1]}')
            return 1
    expected = ''
    try:
        expected = sys.stdin.read().split()[0]
    except Exception:
        expected = ''
    if expected and int(expected) != t:
        print(f'not minimal: got {t}, minimum is {expected}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
