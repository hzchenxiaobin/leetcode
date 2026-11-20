#!/usr/bin/env python3
"""79C Beaver 的 checker（答案不唯一：只要求最长子串长度最优，起点任意）。

用法: python3 cf79c.py <input> <output> <answer>
校验：
  1. 输出恰为两个整数 len pos；
  2. 0 <= pos <= |s|-len，且 s[pos:pos+len] 不包含任何 b_i（区分大小写）；
  3. len 等于真实最优长度——用与题解不同的「双指针 + 出现位置」实现独立求出，
     因此起点不同但长度最优的输出同样判对。
"""
import sys


def optimal(s, bad):
    """返回不含任何 b_i 的最长连续子串长度（双指针独立实现）。"""
    L = len(s)
    endlen = [0] * L          # endlen[e]：以 e 结尾的模式中最短者的长度（= 起点最大者）
    for b in bad:
        ln = len(b)
        st = 0
        while True:
            p = s.find(b, st)
            if p < 0:
                break
            e = p + ln - 1
            if endlen[e] == 0 or ln < endlen[e]:
                endlen[e] = ln
            st = p + 1
    left = 0
    best = 0
    for right in range(L):
        if endlen[right]:
            start = right - endlen[right] + 1
            if start + 1 > left:
                left = start + 1
        if right - left + 1 > best:
            best = right - left + 1
    return best


def main():
    inp = open(sys.argv[1]).read().split()
    out = open(sys.argv[2]).read().split()
    s = inp[0]
    n = int(inp[1])
    bad = inp[2:2 + n]
    if len(out) != 2:
        sys.exit(1)
    try:
        ln, pos = int(out[0]), int(out[1])
    except ValueError:
        sys.exit(1)
    L = len(s)
    if ln < 0 or pos < 0 or pos + ln > L:
        sys.exit(1)
    sub = s[pos:pos + ln]
    if any(b in sub for b in bad):
        sys.exit(1)
    if ln != optimal(s, bad):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
