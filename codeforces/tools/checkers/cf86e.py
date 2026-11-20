#!/usr/bin/env python3
"""86E Long sequence 的 checker（构造题，答案不唯一）。

用法: python3 cf86e.py <input> <output> <answer>

校验条件：
  1. 第一行 k 个数 c_1..c_k、第二行 k 个数 a_0..a_{k-1}，全部为 0/1；
  2. 至少有一个 c_i = 1，且初始状态 (a_0..a_{k-1}) 非零；
  3. 令 f(x) = x^k + c_1 x^{k-1} + ... + c_k（GF(2) 上），则 x 在 Z2[x]/f 中的
     乘法阶恰为 2^k-1。这等价于 f 本原，也就等价于任一非零初值生成的序列
     最小周期恰为 2^k-1（非零状态在 2^k-1 个位置里恰好走一遍）。
  4. 因此在 2..50 范围内一定存在长序列，输出 -1 一律判错。
"""
import sys


def factor(n):
    f = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f.append(n)
    return f


def mulmod(a, b, k, red):
    res = 0
    while b:
        if b & 1:
            res ^= a
        b >>= 1
        a <<= 1
        if (a >> k) & 1:
            a ^= red
    return res


def powmod(a, e, k, red):
    res = 1
    while e:
        if e & 1:
            res = mulmod(res, a, k, red)
        a = mulmod(a, a, k, red)
        e >>= 1
    return res


def main():
    k = int(open(sys.argv[1]).read().split()[0])
    out = open(sys.argv[2]).read().split()
    if not out:
        print('CHECKER FAIL: 空输出')
        return 1
    if out[0] == '-1':
        print(f'CHECKER FAIL: k={k} 时一定存在长序列，不能输出 -1')
        return 1
    if len(out) != 2 * k:
        print(f'CHECKER FAIL: 应有 {2*k} 个数，实际 {len(out)}')
        return 1
    try:
        bits = [int(x) for x in out]
    except ValueError:
        print('CHECKER FAIL: 出现非整数 token')
        return 1
    if any(b not in (0, 1) for b in bits):
        print('CHECKER FAIL: 出现 0/1 以外的数')
        return 1
    c = bits[:k]
    a = bits[k:]
    if all(x == 0 for x in c):
        print('CHECKER FAIL: 至少需要一个 c_i = 1')
        return 1
    if all(x == 0 for x in a):
        print('CHECKER FAIL: 初始状态全 0，序列恒为 0，周期是 1')
        return 1

    red = (1 << k) | sum(c[i] << (k - 1 - i) for i in range(k))   # f(x)
    m = (1 << k) - 1
    if powmod(2, m, k, red) != 1:
        print('CHECKER FAIL: x^(2^k-1) != 1 mod f，2^k-1 不是周期')
        return 1
    for q in factor(m):
        if powmod(2, m // q, k, red) == 1:
            print(f'CHECKER FAIL: x^((2^k-1)/{q}) == 1 mod f，周期更小')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
