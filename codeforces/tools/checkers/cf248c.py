#!/usr/bin/env python3
"""CF248C Robo-Footballer 的 checker（多解：任何合法的 x_w 都接受）。

用法：python3 cf248c.py <input> <output> <answer>
返回 0 表示通过。

合法性（按题面几何）：球心轨迹 (xb,yb) -> (xw, y_w-r) -> (0, yc)，
  * 只撞一次顶墙 y=y_w（球心撞墙高度 y_w-r）；
  * 球（半径 r）不穿地板、不穿顶墙；
  * 球心 x<r 的位置，圆盘必须整个落在门洞 [y1,y2] 内（否则蹭左墙/门柱）；
  * 球心穿过 x=0 时 y_c ∈ [y1+r, y2-r]。
输出 "-1" 时，独立用几何扫描确认无解。
"""
import sys

def parse(inp, out):
    d = [float(x) for x in open(inp).read().split()]
    y1, y2, yw, xb, yb, r = d[:6]
    toks = open(out).read().split()
    return (y1, y2, yw, xb, yb, r), toks

def traj_valid(y1, y2, yw, xb, yb, r, xw, eps=1e-7):
    A = yw - r                       # 球心撞墙高度
    if not (xw > r + 1e-12):
        return False, 'xw<=r（弹跳点贴左墙）'
    if not (xb > r + 1e-12):
        return False, 'xb<=r（起点贴左墙）'
    if yb < r - eps:
        return False, 'yb<r（起点穿地板）'
    if not (A > yb + eps):
        return False, '弹跳点不在球的上方'
    if not (xw < xb - eps):
        return False, '水平分量朝右，反射后不会飞向 x=0'
    k = (A - yb) / (xw - xb)         # 入射斜率（按 x 参数化）
    yc = A + xw * k                  # 反射后到 x=0 时的高度：y=A - (x-xw)*k，代 x=0
    # 反射后方向：dx = xw-xb < 0（向左），dy = -(A-yb)（向下）
    if not (y1 + r - eps <= yc <= y2 - r + eps):
        return False, '球心过门时不在门洞内 (yc=%.9f)' % yc
    if yc < r - eps:
        return False, '贴地板'
    if xw > r:
        yr = yc + (A - yc) * r / xw  # 第二段 y(x) = yc + (A-yc)*x/xw
        if yr + r > y2 + eps:
            return False, '蹭到门柱上方的墙 (yr+r=%.9f)' % (yr + r)
        if yr - r < y1 - eps:
            return False, '蹭到门柱下方的墙'
    return True, 'ok(yc=%.9f)' % yc

def feasible(y1, y2, yw, xb, yb, r, steps=20000):
    lo, hi = y1 + r, y2 - r
    A = yw - r
    for k in range(steps + 1):
        yc = lo + (hi - lo) * k / steps
        den = yc - 2 * A + yb
        if abs(den) < 1e-15:
            continue
        xw = xb * (yc - A) / den
        ok, _ = traj_valid(y1, y2, yw, xb, yb, r, xw)
        if ok:
            return True, xw
    return False, None

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    (y1, y2, yw, xb, yb, r), toks = parse(inp, out)
    if len(toks) != 1:
        print('CHECKER FAIL: 应输出 1 个数，实际 %d 个' % len(toks))
        return 1
    if toks[0].strip() == '-1':
        ok, xw = feasible(y1, y2, yw, xb, yb, r)
        if ok:
            print('CHECKER FAIL: 输出 -1，但存在解 xw=%.9f' % xw)
            return 1
        want = open(ans).read().split()[0]
        if want.strip() != '-1':
            print('CHECKER FAIL: 标准答案 %s，但判为无解' % want)
            return 1
        return 0
    try:
        xw = float(toks[0])
    except ValueError:
        print('CHECKER FAIL: 非数字')
        return 1
    ok, why = traj_valid(y1, y2, yw, xb, yb, r, xw)
    if not ok:
        print('CHECKER FAIL: xw=%.9f 不合法：%s' % (xw, why))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
