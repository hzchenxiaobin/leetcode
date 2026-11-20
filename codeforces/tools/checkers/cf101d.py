#!/usr/bin/env python3
"""101D Castle 的 checker（浮点答案，允许格式差异）。

用法: python3 cf101d.py <input> <output> <answer>
Codeforces 官方样例里期望输出是 "1.0"、"4.333333333333334" 这类
"最短往返格式"，与常见的 printf("%.10f") 字面不同；真实评测按
绝对/相对误差 1e-6 比较，因此这里也按数值比较：
  1. 输出必须恰好一个实数（可带正负号/小数/指数）；
  2. 与答案文件的第一个实数在 1e-6 相对或绝对误差内即接受。
"""
import sys


def main():
    try:
        out_tok = open(sys.argv[2]).read().split()
        ans_tok = open(sys.argv[3]).read().split()
    except Exception:
        sys.exit(1)
    if not out_tok or not ans_tok:
        sys.exit(1)
    try:
        got = float(out_tok[0])
        exp = float(ans_tok[0])
    except ValueError:
        sys.exit(1)
    if len(out_tok) > 1:
        sys.exit(1)
    if any(c not in "0123456789+-.eE" for c in out_tok[0]):
        sys.exit(1)
    tol = 1e-6
    if abs(got - exp) <= tol * max(1.0, abs(exp)):
        sys.exit(0)
    sys.exit(1)


main()
