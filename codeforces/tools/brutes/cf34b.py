# 独立暴力：枚举所有"至多 m 台"的子集，取最大收益（n 很小时可行）。
import sys
from itertools import combinations


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    best = 0
    for k in range(0, min(m, n) + 1):
        for comb in combinations(a, k):
            earn = -sum(comb)               # 花掉的钱 = 收益的相反数
            if earn > best:
                best = earn
    print(best)


main()
