"""97B checker（构造题，答案不唯一）。

约定：python3 cf97b.py <input> <output> <answer>，返回 0 表示通过。

校验条件：
1. 第一行 m 满足 n <= m <= 2*10^5，随后恰好 m 个整点，坐标 |x|,|y| <= 10^9，互不相同；
2. 输入点集是输出点集的子集；
3. 「好集合」性质：任意两点，或者同 x、或者同 y、或者其包围盒（闭矩形）内还有第三个点，
   等价于"任意两点确定的闭矩形内（含边界）至少还有第 3 个点"。
   m <= 600 时用 y 位集精确校验全部点对；m 更大时校验 x 序相邻 64 邻域内的点对
   与 20 万组随机点对（抽样：只会漏判不可能误判）。
"""
import random
import sys


def exact_good(pts):
    """pts 已按 (x, y) 排序。用 y 序号位集做 O(m^2 * m/64) 的精确校验。"""
    m = len(pts)
    order = sorted(range(m), key=lambda i: (pts[i][1], pts[i][0]))
    rank = [0] * m
    for r, i in enumerate(order):
        rank[i] = r
    # 每个 x 组的位集
    groups = []
    i = 0
    while i < m:
        j = i
        mask = 0
        while j < m and pts[j][0] == pts[i][0]:
            mask |= 1 << rank[j]
            j += 1
        groups.append((pts[i][0], i, j, mask))
        i = j
    gi = [0] * m
    for g, (_, a, b, _) in enumerate(groups):
        for k in range(a, b):
            gi[k] = g

    ys = sorted(pts[i][1] for i in range(m))
    for i in range(m):
        x1, y1 = pts[i]
        mask = 0
        g = gi[i]
        gx = groups[g][0]
        # 先并上 x == x1 这一整组（同 x 的点也可能是见证）
        mask |= groups[g][3]
        gg = g
        for j in range(i + 1, m):
            x2, y2 = pts[j]
            if x2 == x1 or y2 == y1:
                continue
            # 把 (x1, x2) 之间以及 x2 组的点并进来
            while gg + 1 <= gi[j]:
                gg += 1
                mask |= groups[gg][3]
            lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
            a = lower_bound(ys, lo)
            b = upper_bound(ys, hi)
            interval = ((1 << b) - 1) ^ ((1 << a) - 1)
            if bin(mask & interval).count('1') < 3:
                return (x1, y1), (x2, y2)
    return None


def lower_bound(a, v):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < v:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(a, v):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= v:
            lo = mid + 1
        else:
            hi = mid
    return lo


def sampled_good(pts, rnd):
    """抽样校验：对每个点对扫 [x1, x2] 区间内的所有点（含同一 x 的边界点），命中即停。"""
    m = len(pts)
    xs = [p[0] for p in pts]
    pairs = [(i, j) for i in range(m) for j in range(i + 1, min(m, i + 65))]
    for _ in range(200000):
        i = rnd.randrange(m)
        j = rnd.randrange(m)
        if i == j:
            continue
        if i > j:
            i, j = j, i
        pairs.append((i, j))
    for i, j in pairs:
        x1, y1 = pts[i]
        x2, y2 = pts[j]
        if x1 == x2 or y1 == y2:
            continue
        lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
        a = lower_bound(xs, x1)
        b = upper_bound(xs, x2)
        ok = False
        for k in range(a, b):
            if k == i or k == j:
                continue
            if lo <= pts[k][1] <= hi:
                ok = True
                break
        if not ok:
            return (x1, y1), (x2, y2)
    return None


def main():
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    n = int(data[0])
    orig = {(int(data[1 + 2 * i]), int(data[2 + 2 * i])) for i in range(n)}
    toks = open(outp).read().split()
    if not toks:
        return fail('输出为空')
    try:
        m = int(toks[0])
    except ValueError:
        return fail('第一行不是整数')
    if len(toks) != 1 + 2 * m:
        return fail('点个数与声明不符')
    if not (n <= m <= 200000):
        return fail('m=%d 不在 [%d, 200000] 内' % (m, n))
    pts = []
    for i in range(m):
        try:
            x, y = int(toks[1 + 2 * i]), int(toks[2 + 2 * i])
        except ValueError:
            return fail('坐标不是整数')
        if abs(x) > 10 ** 9 or abs(y) > 10 ** 9:
            return fail('坐标超出 10^9')
        pts.append((x, y))
    if len(set(pts)) != m:
        return fail('输出点有重复')
    if not orig <= set(pts):
        return fail('输出不是输入点集的超集')
    pts.sort()
    bad = exact_good(pts) if m <= 600 else sampled_good(pts, random.Random(20240918))
    if bad:
        return fail('包围盒内没有第三个点：%s 与 %s' % (bad[0], bad[1]))
    return 0


def fail(msg):
    print('CHECKER FAIL:', msg)
    return 1


if __name__ == '__main__':
    sys.exit(main())
