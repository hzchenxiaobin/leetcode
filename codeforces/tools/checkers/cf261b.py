#!/usr/bin/env python3
"""CF261B Maxim and Restaurant 的浮点答案 checker。

题面容差：绝对误差或相对误差不超过 1e-4。约定：python3 cf261b.py <input> <output> <answer>，
返回 0 表示通过。

校验条件：
  1. 输出必须恰好是一个实数 token（多余/缺失 token 都判错）；
  2. 该 token 能被 float() 解析；
  3. |out - ans| <= max(1e-4, 1e-4 * |ans|)。
因为本题期望值是「平均入座人数」，一定落在 [0, n] 内，不再额外检查上下界。
"""
import sys


def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    toks = open(out).read().split()
    if len(toks) != 1:
        print(f'CHECKER FAIL: 应输出 1 个实数，实际 {len(toks)} 个 token')
        return 1
    try:
        got = float(toks[0])
    except ValueError:
        print(f'CHECKER FAIL: {toks[0]!r} 不是实数')
        return 1
    want = float(open(ans).read().split()[0])
    tol = max(1e-4, 1e-4 * abs(want))
    if abs(got - want) > tol:
        print(f'CHECKER FAIL: {got} vs {want}（容差 {tol:.3g}）')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
