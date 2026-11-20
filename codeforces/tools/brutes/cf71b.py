import sys


def main():
    n, k, t = map(int, sys.stdin.read().split())
    # 独立实现：直接枚举所有合法界面（位置 i 与部分值 a），
    # 取满足 100*sum <= t*n*k 的最大 sum 所对应的那一个界面。
    best_p, best_i, best_a = -1, 1, 0
    for i in range(1, n + 1):
        for a in range(k + 1):
            p = (i - 1) * k + a
            if 100 * p <= t * n * k and p > best_p:
                best_p, best_i, best_a = p, i, a
    res = [k] * (best_i - 1) + [best_a] + [0] * (n - best_i)
    sys.stdout.write(" ".join(map(str, res)) + "\n")


main()
