# 独立暴力：用 Python 大整数直接算出总数 N = (b-1) * b^(n-1)，再取 (N-1) mod c + 1。
import sys


def main() -> None:
    data = sys.stdin.read().split()
    b, n, c = int(data[0]), int(data[1]), int(data[2])
    total = (b - 1) * pow(b, n - 1)
    print((total - 1) % c + 1)


main()
