#!/usr/bin/env python3
"""CF 226D The table 的构造合法性 checker。

校验条件：
  1. 第一行形如 "a r1 r2 ... ra"，第二行形如 "b c1 c2 ... cb"；
  2. 行号在 [1,n] 内且互不相同，列号在 [1,m] 内且互不相同；
  3. 按这些行、列把对应元素取反后，每一行、每一列的和都非负。

约定：python3 cf226d.py <input> <output> <answer>，返回 0 表示通过。
"""
import sys


def main():
    data = open(sys.argv[1]).read().split()
    n, m = int(data[0]), int(data[1])
    vals = [int(x) for x in data[2:2 + n * m]]
    a = [[vals[i * m + j] for j in range(m)] for i in range(n)]
    lines = [ln.split() for ln in open(sys.argv[2]).read().splitlines() if ln.strip()]
    if len(lines) != 2:
        print('CHECKER FAIL: 输出应为两行')
        return 1
    try:
        cnt_r = int(lines[0][0]); rows = [int(x) for x in lines[0][1:]]
        cnt_c = int(lines[1][0]); cols = [int(x) for x in lines[1][1:]]
    except (ValueError, IndexError):
        print('CHECKER FAIL: 无法解析输出')
        return 1
    if cnt_r != len(rows) or cnt_c != len(cols):
        print('CHECKER FAIL: 行/列个数与列表长度不一致')
        return 1
    if len(set(rows)) != len(rows) or any(not (1 <= x <= n) for x in rows):
        print('CHECKER FAIL: 行号非法或重复')
        return 1
    if len(set(cols)) != len(cols) or any(not (1 <= x <= m) for x in cols):
        print('CHECKER FAIL: 列号非法或重复')
        return 1
    for i in rows:
        for j in range(m):
            a[i - 1][j] = -a[i - 1][j]
    for j in cols:
        for i in range(n):
            a[i][j - 1] = -a[i][j - 1]
    for i in range(n):
        if sum(a[i]) < 0:
            print(f'CHECKER FAIL: 第 {i + 1} 行和为负')
            return 1
    for j in range(m):
        if sum(a[i][j] for i in range(n)) < 0:
            print(f'CHECKER FAIL: 第 {j + 1} 列和为负')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
