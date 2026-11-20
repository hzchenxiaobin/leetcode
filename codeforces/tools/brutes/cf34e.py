# 独立暴力/交叉验证：用极小步长的数值模拟（dt = 1e-5）推进，检测到重叠就按弹性公式反弹，
# 并在碰撞后把两球位置放回接触点。它不使用"事件驱动"，是另一套完全不同的实现。
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, t = int(data[0]), int(data[1])
    x0 = [0.0] * n
    v0 = [0.0] * n
    m0 = [0.0] * n
    p = 2
    for i in range(n):
        x0[i] = float(data[p]); v0[i] = float(data[p + 1]); m0[i] = float(data[p + 2])
        p += 3

    order = sorted(range(n), key=lambda i: x0[i])
    x = [x0[i] for i in order]
    v = [v0[i] for i in order]
    m = [m0[i] for i in order]

    dt = 1e-5
    cur = 0.0
    while cur < t:
        step = min(dt, t - cur)
        for i in range(n):
            x[i] += v[i] * step
        cur += step
        # 处理所有重叠的相邻对（多为一次一对）
        for _ in range(4):
            changed = False
            for i in range(n - 1):
                if x[i + 1] - x[i] < 0.0:
                    m1, m2, u1, u2 = m[i], m[i + 1], v[i], v[i + 1]
                    # 先把两球放回中点接触位置，避免穿透
                    mid = (x[i] + x[i + 1]) / 2.0
                    x[i] = mid
                    x[i + 1] = mid
                    v[i] = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
                    v[i + 1] = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)
                    changed = True
            if not changed:
                break

    res = [0.0] * n
    for k, i in enumerate(order):
        res[i] = x[k]
    print("\n".join(f"{res[i]:.9f}" for i in range(n)))


main()
