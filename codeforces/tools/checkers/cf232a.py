#!/usr/bin/env python3
"""CF 232A Cycles 的 checker：校验构造图恰有 k 个三角形。

用法：python3 cf232a.py <input> <output> <answer>
"""
import sys


def main():
    k = int(open(sys.argv[1]).read().split()[0])
    data = open(sys.argv[2]).read().split()
    if not data:
        print('CHECKER FAIL: 输出为空')
        return 1
    n = int(data[0])
    if not (3 <= n <= 100):
        print('CHECKER FAIL: n 超出 [3,100]')
        return 1
    rows = data[1:1 + n]
    if len(rows) != n or any(len(r) != n for r in rows):
        print('CHECKER FAIL: 矩阵尺寸不对')
        return 1
    for i in range(n):
        if rows[i][i] != '0':
            print('CHECKER FAIL: 存在自环')
            return 1
        for j in range(n):
            if rows[i][j] != rows[j][i]:
                print('CHECKER FAIL: 矩阵不对称')
                return 1
    adj = [[rows[i][j] == '1' for j in range(n)] for i in range(n)]
    cnt = 0
    for a in range(n):
        for b in range(a + 1, n):
            if not adj[a][b]:
                continue
            for c in range(b + 1, n):
                if adj[a][c] and adj[b][c]:
                    cnt += 1
    if cnt != k:
        print(f'CHECKER FAIL: 三角形数 {cnt} != {k}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
