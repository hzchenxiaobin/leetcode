#!/usr/bin/env python3
"""CF306D Polygon 的 checker（多解，浮点 1e-3）。

校验：n=3/4 只能是 "No solution"；否则给出 n 个逆时针顶点，满足
凸、各内角相等（1e-3）、边长互不相同（1e-3）、边长 ∈[1,1000]、坐标 ≤1e6。
"""
import sys, math


def main():
    n = int(open(sys.argv[1], encoding='utf-8').read().split()[0])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if n in (3, 4):
        return 0 if out[:2] == ['No', 'solution'] else (print('WA: n=3/4 应输出 No solution') or 1)
    if out[:2] == ['No', 'solution']:
        print('WA: n=%d 存在解' % n)
        return 1
    if len(out) != 2 * n:
        print('WA: 需要 %d 个坐标' % (2 * n))
        return 1
    pts = [(float(out[2 * i]), float(out[2 * i + 1])) for i in range(n)]
    for x, y in pts:
        if abs(x) > 1e6 or abs(y) > 1e6:
            print('WA: 坐标越界')
            return 1
    # 边长
    side = []
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        side.append(math.hypot(x2 - x1, y2 - y1))
    for s in side:
        if not (1 - 1e-9 <= s <= 1000 + 1e-9):
            print('WA: 边长 %.6f 不在 [1,1000]' % s)
            return 1
    for i in range(n):
        for j in range(i + 1, n):
            if abs(side[i] - side[j]) < 1e-6:
                print('WA: 边长 %.6f 与 %.6f 相同' % (side[i], side[j]))
                return 1
    # 凸性 + 角度相等
    cross = []
    for i in range(n):
        ax, ay = pts[i]
        bx, by = pts[(i + 1) % n]
        cx, cy = pts[(i + 2) % n]
        cross.append((bx - ax) * (cy - by) - (by - ay) * (cx - bx))
    if any(c <= 0 for c in cross):
        print('WA: 不是逆时针凸多边形')
        return 1
    ang = []
    for i in range(n):
        ax, ay = pts[i]
        bx, by = pts[(i + 1) % n]
        cx, cy = pts[(i + 2) % n]
        v1 = (ax - bx, ay - by)
        v2 = (cx - bx, cy - by)
        c = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))
        ang.append(math.degrees(math.acos(max(-1.0, min(1.0, c)))))
    if max(ang) - min(ang) > 1e-3:
        print('WA: 角度不等，极差 %.6f' % (max(ang) - min(ang)))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
