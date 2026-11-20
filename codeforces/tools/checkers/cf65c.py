"""65C checker：输入 + 选手输出 + 参考答案（样例输出）。返回 0 表示通过。

校验条件：
1. 输出 NO 时：独立逐段二次不等式参考也必须判定追不上；
2. 输出 YES 时：必须 3 行（YES / t / X Y Z），t 与独立参考的最早时刻相差 <= 1e-6（相对），
   坐标点在时刻 t 的折线位置上（误差 <= 1e-6），且 dist(P, 点) <= vp*t + 1e-6。
"""
import sys
sys.path.insert(0, '/tmp/cf_verify_65_C')
from brute import earliest, at, build

def main():
    inp, outp, _ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    p = 0
    n = int(data[p]); p += 1
    pts = []
    for _ in range(n + 1):
        pts.append((float(data[p]), float(data[p+1]), float(data[p+2]))); p += 3
    vp = float(data[p]); vs = float(data[p+1]); p += 2
    P = (float(data[p]), float(data[p+1]), float(data[p+2]))

    found, T, pt = earliest(pts, vp, vs, P)
    toks = open(outp).read().split()
    if not toks:
        print('checker: 空输出'); return 1
    if toks[0] == 'NO':
        if found:
            print('checker: 其实追得上（T*=%r）却输出 NO' % T); return 1
        return 0
    if toks[0] != 'YES':
        print('checker: 首行不是 YES/NO'); return 1
    if not found:
        print('checker: 追不上却输出 YES'); return 1
    if len(toks) != 5:
        print('checker: 需要 3 行（YES / t / 三个坐标）'); return 1
    try:
        t = float(toks[1])
        got = (float(toks[2]), float(toks[3]), float(toks[4]))
    except ValueError:
        print('checker: 有非数字'); return 1
    tol_t = 1e-6 * max(1.0, abs(T))
    if abs(t - T) > tol_t:
        print('checker: 时刻 %r 不是最早（参考 %r）' % (t, T)); return 1
    if t < -1e-9:
        print('checker: 时刻为负'); return 1
    pref = build(pts, vp, vs)
    sx, sy, sz = at(pts, pref, vp, vs, t)
    d = ((sx-got[0])**2 + (sy-got[1])**2 + (sz-got[2])**2) ** 0.5
    if d > 1e-6 * max(1.0, abs(sx) + abs(sy) + abs(sz)):
        print('checker: 坐标不在折线上的对应位置', d); return 1
    reach = ((got[0]-P[0])**2 + (got[1]-P[1])**2 + (got[2]-P[2])**2) ** 0.5
    if reach > vp * t + 1e-6:
        print('checker: 哈利跑不到该点', reach, vp*t); return 1
    return 0

sys.exit(main())
