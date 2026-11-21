#!/usr/bin/env python3
"""CF 234G Practice 的 checker：校验练习方案覆盖所有对且次数最少。"""
import sys


def main():
    n = int(open(sys.argv[1]).read().split()[0])
    lines = [ln.split() for ln in open(sys.argv[2]).read().splitlines() if ln.strip()]
    if not lines:
        print('CHECKER FAIL: 输出为空')
        return 1
    m = int(lines[0][0])
    best = 0
    while (1 << best) < n:
        best += 1
    if m != best:
        print(f'CHECKER FAIL: 次数 {m} 不是最少 {best}')
        return 1
    if len(lines) - 1 != m:
        print('CHECKER FAIL: 行数不对')
        return 1
    sep = [[False] * (n + 1) for _ in range(n + 1)]
    for ln in lines[1:]:
        f = int(ln[0])
        team = set(int(x) for x in ln[1:1 + f])
        if len(team) != f or f < 1 or f >= n:
            print('CHECKER FAIL: 队伍大小/编号非法')
            return 1
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if (i in team) != (j in team):
                    sep[i][j] = True
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if not sep[i][j]:
                print(f'CHECKER FAIL: 对 ({i},{j}) 从未分开')
                return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
