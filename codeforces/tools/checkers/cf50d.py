#!/usr/bin/env python3
"""50D 样例校验器：答案在 1e-6 绝对/相对误差内即通过（与 Codeforces 本题的 checker 一致）。

用法：python3 checker.py <input> <output> <answer>
其中 <answer> 为 /dev/stdin 时从标准输入读取（verify_solution.py 的约定）。
"""
import sys

def main() -> int:
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    expected_text = sys.stdin.read() if ans == "/dev/stdin" else open(ans).read()
    got = open(out).read().split()
    exp = expected_text.split()
    if len(got) != 1:
        print("输出应为单个实数，实际 token 数: %d" % len(got)); return 1
    try:
        g = float(got[0]); e = float(exp[0])
    except ValueError:
        print("无法解析为实数"); return 1
    diff = abs(g - e)
    if diff <= 1e-6 or diff <= 1e-6 * abs(e):
        return 0
    print("误差过大: got=%r expected=%r diff=%g" % (g, e, diff)); return 1

sys.exit(main())
