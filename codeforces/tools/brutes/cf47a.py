# 独立暴力：用公式反解 k = (sqrt(8n+1)-1)/2，再检查 2n 是否等于 k(k+1)。
# 与参考解的"枚举 k"完全不同路，可互相验证。
import sys
from math import isqrt


def main() -> None:
    n = int(sys.stdin.read().split()[0])
    d = 8 * n + 1
    r = isqrt(d)
    ok = r * r == d and (r - 1) % 2 == 0 and (r - 1) // 2 * ((r - 1) // 2 + 1) // 2 == n
    print("YES" if ok else "NO")


main()
