# 独立暴力：对每发炮弹按 x 从小到大扫描所有墙，找第一堵“挡住”它的墙（0 ≤ y(x) ≤ 墙高）。
# n、m 很小时可行，与参考解的“区间 + 并查集”完全不同的思路。
import sys
from math import tan, sin

G = 9.8


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); V = float(data[1])
    alpha = [float(x) for x in data[2:2 + n]]
    p = 2 + n
    m = int(data[p]); p += 1
    walls = []
    for _ in range(m):
        walls.append((float(data[p]), float(data[p + 1])))
        p += 2
    walls.sort()

    out = []
    for a in alpha:
        u = tan(a)
        hit = None
        for x, y in walls:
            c = G * x * x / (2 * V * V)
            yb = x * u - c * (1 + u * u)
            if yb >= -1e-12 and yb <= y + 1e-12:
                hit = (x, yb)
                break
        if hit is None:
            out.append(f"{V * V * sin(2 * a) / G:.9f} 0.000000000")
        else:
            out.append(f"{hit[0]:.9f} {hit[1]:.9f}")
    print("\n".join(out))


main()
