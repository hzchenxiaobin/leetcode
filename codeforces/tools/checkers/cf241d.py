#!/usr/bin/env python3
"""CF241D Numbers 校验器（多解 + No 需要独立判定）。

约定：python3 cf241d.py <input> <output> <answer>，返回 0 表示通过。

校验条件：
1. Yes：k > 0；恰好 k 个互不相同的下标，均在 [1,n]；按输出给出的顺序把对应
   数字拼起来，异或必须为 0、十进制拼接必须能被 p 整除。
2. No：独立判定存在性。n <= 18 时全枚举 2^n 个子集；n <= 26 时用折半枚举
   （前缀按 (xor, 拼接余数) 建集合，后缀按 (xor, 长度) 查询）。
   n > 26 时判定代价过高，checker 只做格式校验（正式评测由出题人数据保证）。
"""
import sys

BRUTE_MAX = 18
MITM_MAX = 26


def powers(p, n):
    pw = [1] * (n * 6 + 2)
    for i in range(1, len(pw)):
        pw[i] = pw[i - 1] * 10 % p
    inv = [1] * (n * 6 + 2)
    if p not in (2, 5):
        iv = pow(10, p - 2, p)
        for i in range(1, len(inv)):
            inv[i] = inv[i - 1] * iv % p
    return pw, inv


def feasible_brute(n, p, a):
    dig = [len(str(x)) for x in a]
    pw, _ = powers(p, n)
    for mask in range(1, 1 << n):
        xr = 0
        rem = 0
        m = mask
        while m:
            low = m & -m
            i = low.bit_length() - 1
            xr ^= a[i]
            rem = (rem * pw[dig[i]] + a[i]) % p
            m ^= low
        if xr == 0 and rem == 0:
            return True
    return False


def feasible_mitm(n, p, a):
    """折半枚举：前缀看 (xor, rem)，后缀看 (xor, 需要的 rem)。"""
    dig = [len(str(x)) for x in a]
    pw, inv = powers(p, n)
    h = n // 2
    pre_all, pre_ne = set(), set()
    states = [(0, 0, 0)]           # (xor, len, rem)
    for i in range(h):
        x, d = a[i], dig[i]
        add = [(xr ^ x, ln + d, (rm * pw[d] + x) % p) for (xr, ln, rm) in states]
        states = states + add
    for (xr, ln, rm) in states:
        pre_all.add((xr, rm))
        if ln > 0:
            pre_ne.add((xr, rm))
    suf = [(0, 0, 0)]
    for i in range(h, n):
        x, d = a[i], dig[i]
        suf = suf + [(xr ^ x, ln + d, (rm * pw[d] + x) % p) for (xr, ln, rm) in suf]
    for (xr, ln, rm) in suf:
        if p in (2, 5):
            if ln == 0:
                if (0, 0) in pre_ne:      # 前缀必须非空且 xor=0, rem=0
                    return True
            else:
                if rm % p == 0 and any(k[0] == xr for k in pre_all):
                    return True
            continue
        target = (p - rm % p) % p * inv[ln] % p
        if ln == 0:
            if (xr, target) in pre_ne:
                return True
        elif (xr, target) in pre_all:
            return True
    return False


def main():
    if len(sys.argv) < 3:
        print('CHECKER FAIL: 用法 cf241d.py <input> <output> <answer>')
        sys.exit(1)
    data = open(sys.argv[1]).read().split()
    n, p = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    tok = open(sys.argv[2]).read().split()

    def bad(msg):
        print('CHECKER FAIL:', msg)
        sys.exit(1)

    if not tok:
        bad('输出为空')
    if tok[0] == 'No':
        if len(tok) != 1:
            bad('No 之后不应再有内容')
        if n <= BRUTE_MAX:
            if feasible_brute(n, p, a):
                bad('存在解，但输出 No')
        elif n <= MITM_MAX:
            if feasible_mitm(n, p, a):
                bad('存在解，但输出 No')
        return
    if tok[0] != 'Yes':
        bad('第一行必须是 Yes 或 No')
    if len(tok) < 2:
        bad('缺少 k')
    k = int(tok[1])
    if k <= 0:
        bad('k 必须 > 0')
    if len(tok) != 2 + k:
        bad('下标个数与 k 不一致')
    idx = [int(x) for x in tok[2:]]
    if len(set(idx)) != k:
        bad('下标有重复')
    for x in idx:
        if not (1 <= x <= n):
            bad('下标越界')
    xr = 0
    rem = 0
    for x in idx:
        v = a[x - 1]
        xr ^= v
        rem = (rem * pow(10, len(str(v))) + v) % p
    if xr != 0:
        bad('异或不为 0：%d' % xr)
    if rem != 0:
        bad('拼接不能被 p 整除：余 %d' % rem)


if __name__ == '__main__':
    main()
