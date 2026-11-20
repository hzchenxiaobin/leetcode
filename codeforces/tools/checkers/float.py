#!/usr/bin/env python3
"""通用浮点答案 checker（误差判定）。

约定：python3 float.py <input> <output> <answer>，返回 0 表示通过。
逐个 token 比较：数值 token 用 |a-b| <= max(abs_tol, rel_tol*|b|)；非数值 token 要求完全相同。
默认 abs/rel 容差 1e-6，可用环境变量 CF_ABS_TOL / CF_REL_TOL 覆盖。
"""
import os, sys


def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    abs_tol = float(os.environ.get('CF_ABS_TOL', '1e-6'))
    rel_tol = float(os.environ.get('CF_REL_TOL', '1e-6'))
    a = open(out).read().split()
    b = open(ans).read().split()
    if len(a) != len(b):
        print(f'CHECKER FAIL: token 数不同 {len(a)} != {len(b)}')
        return 1
    for i, (x, y) in enumerate(zip(a, b)):
        try:
            fx, fy = float(x), float(y)
        except ValueError:
            if x != y:
                print(f'CHECKER FAIL: 第 {i+1} 个 token {x!r} != {y!r}')
                return 1
            continue
        if abs(fx - fy) > max(abs_tol, rel_tol * abs(fy)):
            print(f'CHECKER FAIL: 第 {i+1} 个 token {fx} vs {fy}（容差 {max(abs_tol, rel_tol*abs(fy)):.3g}）')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
