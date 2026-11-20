# 独立暴力：对 2..n 的每个素数 p，直接枚举所有"相邻素数对"，看是否有 p = q1 + q2 + 1。
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])

    def is_prime(x):
        if x < 2:
            return False
        d = 2
        while d * d <= x:
            if x % d == 0:
                return False
            d += 1
        return True

    primes = [p for p in range(2, n + 1) if is_prime(p)]
    cnt = 0
    for p in primes:
        ok = False
        for i in range(len(primes) - 1):
            if primes[i] + primes[i + 1] + 1 == p:
                ok = True
                break
        if ok:
            cnt += 1
    print("YES" if cnt >= k else "NO")


main()
