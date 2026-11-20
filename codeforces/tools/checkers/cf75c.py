import sys
from math import gcd


def main():
    data = list(map(int, sys.stdin.read().split()))
    a, b = data[0], data[1]
    g = gcd(a, b)
    divs = [d for d in range(1, g + 1) if g % d == 0]   # 直接试除全部候选
    n = data[2]
    out = []
    for k in range(n):
        lo, hi = data[3 + 2 * k], data[4 + 2 * k]
        best = -1
        for d in divs:
            if lo <= d <= hi:
                best = d
        out.append(str(best))
    print("\n".join(out))


main()
