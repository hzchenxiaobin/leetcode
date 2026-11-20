# 28E 独立暴力：在 (t1,t2) 网格上采样，找出可行（落点在多边形内或边界）且字典序最小的点
import sys

def main():
    d = sys.stdin.read().split()
    p = 0
    n = int(d[p]); p += 1
    poly = []
    for _ in range(n):
        poly.append((float(d[p]), float(d[p+1]))); p += 2
    ax, ay = float(d[p]), float(d[p+1]); p += 2
    vx, vy, vz = float(d[p]), float(d[p+1]), float(d[p+2]); p += 3
    fd = float(d[p]); p += 1
    ux, uy, uz = float(d[p]), float(d[p+1]), float(d[p+2]); p += 3
    EPS = 1e-9

    def on_seg(px, py, x1, y1, x2, y2):
        cr = (x2-x1)*(py-y1) - (y2-y1)*(px-x1)
        if abs(cr) > 1e-9: return False
        dot = (px-x1)*(x2-x1) + (py-y1)*(y2-y1)
        l2 = (x2-x1)**2 + (y2-y1)**2
        return -1e-9 <= dot <= l2 + 1e-9

    def inside(px, py):
        inn = False
        for i in range(n):
            x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
            if on_seg(px, py, x1, y1, x2, y2): return True
            if (y1 > py) != (y2 > py):
                xt = (x2-x1)*(py-y1)/(y2-y1) + x1
                if px < xt: inn = not inn
        return inn

    def land(t1, t2):
        x2 = ax + vx*t1; y2 = ay + vy*t1; z2 = vz*t1 + fd*t2
        if z2 < -EPS: return None
        if vz*t1 < -EPS: return None
        if uz < 0:
            tau = -z2/uz
            return (x2 + ux*tau, y2 + uy*tau)
        else:
            if abs(z2) > EPS: return None
            return (x2, y2)

    T = 6.0; H = 0.02
    best = None
    steps = int(T/H) + 1
    for i in range(steps):
        t1 = i*H
        for j in range(steps):
            t2 = j*H
            L = land(t1, t2)
            if L is None: continue
            if inside(L[0], L[1]):
                if best is None or (t1, t2) < best: best = (t1, t2)
                break   # 同一 t1 下 t2 最小即可
    if best is None: print('-1')
    else: print('%.6f %.6f' % best)

main()
