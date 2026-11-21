#!/usr/bin/env python3
"""CF193C Hamming Distance 的 checker（答案不唯一：任意最短长度的合法字符串组均可）。

约定：python3 cf193c.py <input> <output> <answer>，返回 0 表示通过。
校验：
  1. 输出第一行是长度 len，随后四行等长的 a/b 串；
  2. len 等于期望答案（标准答案）的第一行；
  3. 四串两两 Hamming 距离与输入完全一致。
"""
import sys


def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    d = {}
    vals = [int(x) for x in data[:6]]
    d[(1, 2)], d[(1, 3)], d[(1, 4)] = vals[0], vals[1], vals[2]
    d[(2, 3)], d[(2, 4)] = vals[3], vals[4]
    d[(3, 4)] = vals[5]

    lines = [ln.strip() for ln in open(out).read().splitlines() if ln.strip()]
    if len(lines) < 5:
        print('CHECKER FAIL: 输出不足 5 行')
        return 1
    try:
        length = int(lines[0])
    except ValueError:
        print('CHECKER FAIL: 第一行不是整数')
        return 1
    strs = lines[1:5]
    if any(len(s) != length for s in strs):
        print('CHECKER FAIL: 字符串长度与声明的 len 不符')
        return 1
    if any(ch not in 'ab' for s in strs for ch in s):
        print('CHECKER FAIL: 字符串里出现 a/b 之外的字符')
        return 1
    for i in range(4):
        for j in range(i + 1, 4):
            h = sum(1 for x, y in zip(strs[i], strs[j]) if x != y)
            if h != d[(i + 1, j + 1)]:
                print(f'CHECKER FAIL: h({i+1},{j+1}) = {h}，要求 {d[(i+1, j+1)]}')
                return 1

    exp = [ln.strip() for ln in open(ans).read().splitlines() if ln.strip()]
    try:
        exp_len = int(exp[0])
    except (ValueError, IndexError):
        print('CHECKER FAIL: 标准答案格式异常')
        return 1
    if length != exp_len:
        print(f'CHECKER FAIL: 长度 {length} != 最短长度 {exp_len}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
