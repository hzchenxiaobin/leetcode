#!/usr/bin/env python3
"""CF260E Dividing Kingdom 的 checker（多解）。

输出两行：x1 x2（不同，且没有城市落在上面，容差 1e-6）与 y1 y2（同理）。
要求 4 条线切出的 9 个区域的城市数（多重集）等于输入的 9 个数。
"""
import sys

EPS = 1e-6


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    pts = []
    pos = 1
    for _ in range(n):
        pts.append((int(data[pos]), int(data[pos + 1]))); pos += 2
    need = sorted(int(v) for v in data[pos:pos + 9])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if out == ['-1']:
        return 0
    if len(out) != 4:
        print('WA: 应输出 4 个数或 -1')
        return 1
    x1, x2, y1, y2 = (float(v) for v in out)
    if abs(x1 - x2) <= EPS or abs(y1 - y2) <= EPS:
        print('WA: 同方向的两条线重合')
        return 1
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    for (px, py) in pts:
        if abs(px - x1) <= EPS or abs(px - x2) <= EPS:
            print('WA: 有城市落在竖线上')
            return 1
        if abs(py - y1) <= EPS or abs(py - y2) <= EPS:
            print('WA: 有城市落在横线上')
            return 1
    cells = [0] * 9
    for (px, py) in pts:
        cx = 0 if px < x1 else (1 if px < x2 else 2)
        cy = 0 if py < y1 else (1 if py < y2 else 2)
        cells[cy * 3 + cx] += 1
    if sorted(cells) != need:
        print('WA: 九块城市数 %s 与要求 %s 不符' % (sorted(cells), need))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
