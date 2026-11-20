# 校验 28E 输出的可行性：落点必须在多边形内/边界，且 t1,t2>=0、z2>=0、 zv*t1>=0
import sys

def main():
    d = open(sys.argv[1]).read().split()
    p = 0
    n = int(d[p]); p += 1
    poly = []
    for _ in range(n):
        poly.append((float(d[p]), float(d[p+1]))); p += 2
    ax, ay = float(d[p]), float(d[p+1]); p += 2
    vx, vy, vz = float(d[p]), float(d[p+1]), float(d[p+2]); p += 3
    fd = float(d[p]); p += 1
    ux, uy, uz = float(d[p]), float(d[p+1]), float(d[p+2]); p += 3
    out = open(sys.argv[2]).read().split()
    t1, t2 = float(out[0]), float(out[1])
    if t1 < 0 and t2 < 0:
        return 0        # 声明无解，交给网格/暴力判
    if t1 < -1e-9 or t2 < -1e-9:
        print('negative t'); return 1
    z2 = vz*t1 + fd*t2
    if z2 < -1e-7:
        print('z2 negative'); return 1
    if vz*t1 < -1e-7:
        print('plane underground'); return 1
    x2 = ax + vx*t1; y2 = ay + vy*t1
    if uz < 0:
        tau = -z2/uz
        px, py = x2 + ux*tau, y2 + uy*tau
    else:
        if abs(z2) > 1e-6:
            print('parachute can not land'); return 1
        px, py = x2, y2
    def on_seg(px, py, x1, y1, x2_, y2_):
        cr = (x2_-x1)*(py-y1) - (y2_-y1)*(px-x1)
        if abs(cr) > 1e-7: return False
        dot = (px-x1)*(x2_-x1) + (py-y1)*(y2_-y1)
        l2 = (x2_-x1)**2 + (y2_-y1)**2
        return -1e-7 <= dot <= l2 + 1e-7
    inn = False
    for i in range(n):
        x1, y1 = poly[i]; x2_, y2_ = poly[(i+1) % n]
        if on_seg(px, py, x1, y1, x2_, y2_): return 0
        if (y1 > py) != (y2_ > py):
            xt = (x2_-x1)*(py-y1)/(y2_-y1) + x1
            if px < xt: inn = not inn
    if not inn:
        print('landing point outside polygon: %.6f %.6f' % (px, py)); return 1
    return 0

sys.exit(main())
