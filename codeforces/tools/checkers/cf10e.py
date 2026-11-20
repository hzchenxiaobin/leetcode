# 独立暴力：对每个金额 S 从小到大算「贪心枚数」与「完全背包最优枚数」，第一个不相等的 S 就是最小反例
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    LIM = 3000

    def greedy(s):
        c = 0
        for v in a:
            c += s // v
            s %= v
        return c

    best = [0] + [10 ** 9] * LIM
    for s in range(1, LIM + 1):
        b = 10 ** 9
        for v in a:
            if v <= s and best[s - v] + 1 < b:
                b = best[s - v] + 1
        best[s] = b
    for s in range(1, LIM + 1):
        if greedy(s) > best[s]:
            print(s)
            return
    print(-1)


main()
