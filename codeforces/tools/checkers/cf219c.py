#!/usr/bin/env python3
"""CF 219C Color Stripe 的 checker（本题多解）。

校验条件：
  1. 第一行是整数 m，第二行是长度 n、只用前 k 个字母的串 t；
  2. t 中没有相邻同色；
  3. t 与 s 不同的位置数恰为 m；
  4. m 等于理论最小值：k >= 3 时为各极大同色段长度除 2 之和；
     k == 2 时合法的串只能是两种交替串，取两者中改动数较小者。

约定：python3 cf219c.py <input> <output> <answer>，返回 0 表示通过。
"""
import sys


def minimum(n, k, s):
    if k == 2:
        c0 = sum(1 for i in range(n) if s[i] != ('A' if i % 2 == 0 else 'B'))
        c1 = n - c0
        return min(c0, c1)
    total, run = 0, 1
    for i in range(1, n):
        if s[i] == s[i - 1]:
            run += 1
        else:
            total += run // 2
            run = 1
    total += run // 2
    return total


def main():
    data = open(sys.argv[1]).read().split()
    n, k = int(data[0]), int(data[1])
    s = data[2]
    lines = open(sys.argv[2]).read().split()
    if len(lines) != 2:
        print('CHECKER FAIL: 输出应为两行（最小改动数 + 重涂后的串）')
        return 1
    try:
        m = int(lines[0])
    except ValueError:
        print('CHECKER FAIL: 第一行不是整数')
        return 1
    t = lines[1]
    if len(t) != n:
        print(f'CHECKER FAIL: 串长 {len(t)} != {n}')
        return 1
    if any(ch < 'A' or ch >= chr(ord('A') + k) for ch in t):
        print('CHECKER FAIL: 使用了超出前 k 个字母的颜色')
        return 1
    if any(t[i] == t[i + 1] for i in range(n - 1)):
        print('CHECKER FAIL: 存在相邻同色')
        return 1
    real = sum(1 for i in range(n) if t[i] != s[i])
    if real != m:
        print(f'CHECKER FAIL: 实际改动 {real} 处，输出声称 {m}')
        return 1
    mn = minimum(n, k, s)
    if m != mn:
        print(f'CHECKER FAIL: 改动数 {m} 不是最小值 {mn}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
