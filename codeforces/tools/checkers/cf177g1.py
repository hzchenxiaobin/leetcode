#!/usr/bin/env python3
"""CF177G1 Fibonacci Strings（30 分档）的 checker。

用法：python3 cf177g1.py <input> <output> <answer>

校验条件：
  1. 输出恰好 m 个整数，每个都在 [0, 1e9+7)；
  2. 独立重算（与正文的两条路径都不同）：
     - 当 k 不大时：维护 pre/suf 窗口，逐项用 ans_i = ans_{i-1}+ans_{i-2}+cross_i 递推，
       每一步的 cross_i 都在窗口里现场数出来（不预先抽常数）；
     - 当 k 很大时：用 Fibonacci 和的闭式公式，完全不做矩阵乘法；
  3. 若 stdin 给了期望输出，也要求逐行一致。
"""
import sys

MOD = 10 ** 9 + 7
CAP = 4 * 10 ** 18


# ---------- 公共：KMP ----------
def prefix_function(pat):
    L = len(pat)
    pi = [0] * L
    for i in range(1, L):
        j = pi[i - 1]
        while j > 0 and pat[i] != pat[j]:
            j = pi[j - 1]
        if pat[i] == pat[j]:
            j += 1
        pi[i] = j
    return pi


def count_all(text, pat):
    cnt = 0
    start = 0
    while True:
        p = text.find(pat, start)
        if p < 0:
            return cnt
        cnt += 1
        start = p + 1


def count_cross(window, pat):
    L = len(pat)
    cnt = 0
    start = 0
    while True:
        p = window.find(pat, start)
        if p < 0:
            return cnt
        if p <= L - 2 and p + L - 1 >= L - 1:
            cnt += 1
        start = p + 1


# ---------- 路径 A：逐项递推（每个 cross 现场数） ----------
def solve_direct(k, s):
    L = len(s)
    r = L - 1
    lens = [0, 1, 1]
    while len(lens) <= k:
        lens.append(lens[-1] + lens[-2])
    f = ["", "a", "b"]
    i = 2
    while i < k and len(f[i]) <= r:
        i += 1
        f.append(f[i - 1] + f[i - 2])
    b = len(f) - 1
    pre = [""] * (k + 1)
    suf = [""] * (k + 1)
    for j in range(1, b + 1):
        pre[j] = f[j][:r]
        suf[j] = f[j][-r:] if r > 0 else ""
    for j in range(b + 1, k + 1):
        if lens[j - 1] >= r:
            pre[j] = pre[j - 1]
        else:
            pre[j] = (f[j - 1] + pre[j - 2])[:r]
        suf[j] = (suf[j - 1] + suf[j - 2])[-r:] if r > 0 else ""
    ans = [0] * (k + 1)
    for j in range(1, min(b, k) + 1):
        ans[j] = count_all(f[j], s) % MOD
    for j in range(b + 1, k + 1):
        cnt = count_cross(suf[j - 1] + pre[j - 2], s)
        ans[j] = (ans[j - 1] + ans[j - 2] + cnt) % MOD
    return ans[k]


# ---------- 路径 B：Fibonacci 和闭式（无矩阵） ----------
def fib_pair(n):
    if n == 0:
        return 0, 1
    a, b = fib_pair(n >> 1)
    c = a * ((2 * b - a) % MOD) % MOD
    d = (a * a + b * b) % MOD
    return (d, (c + d) % MOD) if n & 1 else (c, d)


def fib(n):
    return fib_pair(n)[0] if n >= 0 else 0


def solve_closed(k, s):
    L = len(s)
    length = [0, 1, 1]

    def ensure(upto):
        while len(length) - 1 < upto:
            length.append(min(length[-1] + length[-2], CAP))

    need = max(0, L - 1)
    i0 = 1
    ensure(i0)
    while length[i0] < need:
        i0 += 1
        ensure(i0)
    M = i0 + 3
    J = M + 1
    ensure(J)
    f = [""] * (J + 1)
    f[1], f[2] = "a", "b"
    for i in range(3, J + 1):
        f[i] = f[i - 1] + f[i - 2]
    ans = [0] * (J + 1)
    for i in range(1, J + 1):
        ans[i] = count_all(f[i], s) % MOD if len(f[i]) >= L else 0
    if k <= J:
        return ans[k]
    cpar = [0, 0]
    cpar[M & 1] = (ans[M] - ans[M - 1] - ans[M - 2]) % MOD
    cpar[(M + 1) & 1] = (ans[M + 1] - ans[M] - ans[M - 1]) % MOD
    base = (fib(k - M - 1) * ans[M] + fib(k - M) * ans[M + 1]) % MOD
    D = k - M - 1
    s_odd = fib(D + 1) if D % 2 == 1 else fib(D)
    s_all = (fib(D + 2) - 1) % MOD
    s_even = (s_all - s_odd) % MOD
    tail = (cpar[(k + 1) & 1] * s_even + cpar[k & 1] * s_odd) % MOD
    return (base + tail) % MOD


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    k = int(data[0])
    m = int(data[1])
    queries = [data[2 + i].decode() if isinstance(data[2 + i], bytes) else data[2 + i]
               for i in range(m)]

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != m:
        print(f'输出应为 {m} 个整数，实际 {len(toks)} 个 token')
        return 1
    got = []
    for tk in toks:
        try:
            v = int(tk)
        except ValueError:
            print(f'输出不是整数: {tk!r}')
            return 1
        if not (0 <= v < MOD):
            print(f'输出越界（应在 [0, 1e9+7)）：{v}')
            return 1
        got.append(v)

    exp = []
    for s in queries:
        L = len(s)
        if k <= 4000 and k * max(1, 2 * L) <= 2 * 10 ** 7:
            exp.append(solve_direct(k, s))
        else:
            exp.append(solve_closed(k, s))

    if got != exp:
        for i in range(m):
            if got[i] != exp[i]:
                print(f'第 {i + 1} 个询问错误：独立重算 {exp[i]}，实际 {got[i]}（s={queries[i][:30]!r}）')
                return 1

    try:
        ref = sys.stdin.read().split()
    except Exception:
        ref = []
    if ref:
        if len(ref) != m or [int(x) for x in ref] != exp:
            print('与期望输出不一致')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
