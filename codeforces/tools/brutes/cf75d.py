import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0], data[1]
    p = 2
    arrs = []
    for i in range(n):
        l = data[p]
        p += 1
        arrs.append(data[p:p + l])
        p += l
    big = []
    for k in range(m):
        big += arrs[data[p + k] - 1]
    # 朴素 Kadane（非空）
    best = big[0]
    cur = big[0]
    for x in big[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    print(best)


main()
