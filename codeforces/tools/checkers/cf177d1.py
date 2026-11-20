#!/usr/bin/env python3
"""CF177D1 Encrypting Messages 的 checker。

用法：python3 cf177d1.py <input> <output> <answer>

校验条件：
  1. 输出恰好 n 个整数，每个都在 [0, c-1]；
  2. 与「按定义逐步把 b 加到 a 的每一段、每步取模」独立模拟的结果逐位一致；
  3. 若 stdin 给了期望答案，也要求逐位一致。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    m = int(data[pos]); pos += 1
    c = int(data[pos]); pos += 1
    a = [int(x) for x in data[pos:pos + n]]
    pos += n
    b = [int(x) for x in data[pos:pos + m]]

    sim = list(a)
    for s in range(n - m + 1):
        for j in range(m):
            sim[s + j] = (sim[s + j] + b[j]) % c

    toks = open(sys.argv[2], encoding='utf-8').read().split()
    if len(toks) != n:
        print(f'输出应为 {n} 个整数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = [int(t) for t in toks]
    except ValueError:
        print('输出含非整数 token')
        return 1
    for i, v in enumerate(got):
        if not 0 <= v < c:
            print(f'第 {i + 1} 个数 {v} 不在 [0, {c - 1}] 内')
            return 1
    if got != sim:
        diff = next(i for i in range(n) if got[i] != sim[i])
        print(f'第 {diff + 1} 位不符：期望 {sim[diff]}，实际 {got[diff]}')
        return 1
    ref = sys.stdin.read().split()
    if ref and [int(t) for t in ref] != got:
        print('与题面答案不一致')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
