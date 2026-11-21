#!/usr/bin/env python3
"""CF 228B Two Tables 的 checker：校验给出的平移达到最大重叠度。

用法：python3 cf228b.py <input> <output> <answer>
用整行位运算（Python 大整数）计算重叠度，与主解的逐格枚举实现独立。
"""
import sys


def main():
    data = open(sys.argv[1]).read().split()
    p = 0
    na, ma = int(data[0]), int(data[1]); p = 2
    a = data[p:p + na]; p += na
    nb, mb = int(data[p]), int(data[p + 1]); p += 2
    b = data[p:p + nb]

    def rows_to_bits(rows, m):
        out = []
        for r in rows:
            v = 0
            for j, ch in enumerate(r):
                if ch == '1':
                    v |= 1 << j
            out.append(v)
        return out

    ab = rows_to_bits(a, ma)
    bb = rows_to_bits(b, mb)

    def overlap(x, y):
        total = 0
        for i in range(na):
            bi = i + x
            if bi < 0 or bi >= nb:
                continue
            rv = bb[bi]
            if y >= 0:
                rv >>= y
            else:
                rv <<= -y
            total += bin(ab[i] & rv).count("1")
        return total

    best = 0
    for x in range(1 - na, nb):
        for y in range(1 - ma, mb):
            v = overlap(x, y)
            if v > best:
                best = v

    tokens = open(sys.argv[2]).read().split()
    if len(tokens) < 2:
        print('CHECKER FAIL: 输出不足两个整数')
        return 1
    try:
        x, y = int(tokens[0]), int(tokens[1])
    except ValueError:
        print('CHECKER FAIL: 无法解析输出')
        return 1
    if abs(x) > 10 ** 9 or abs(y) > 10 ** 9:
        print('CHECKER FAIL: 平移超出 1e9')
        return 1
    if overlap(x, y) != best:
        print("CHECKER FAIL: 重叠度 %d 不是最大值 %d" % (overlap(x, y), best))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
