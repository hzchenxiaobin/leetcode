#!/usr/bin/env python3
"""CF106E Space Rescuers 的校验器（浮点答案，点不唯一）。

用法: python3 cf106e.py <input> <output> [expected]
  input：n / n 行 "x y z"
  output：三个实数 x0 y0 z0

校验条件：
  1. 输出三个有限实数；
  2. 用精确的最小包围球（Welzl 随机增量，基集大小 ≤ 4）算出最优半径 R；
  3. 输出点到最远行星的距离 d 必须满足 |d - R| <= 1e-6 * max(1, R) 或 |d-R| <= 1e-6。
"""
import sys
import random


def sub(a, b):
    return [a[i] - b[i] for i in range(3)]


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def norm(a):
    return dot(a, a) ** 0.5


def ball1(p):
    return (list(p), 0.0)


def ball2(a, b):
    c = [(a[i] + b[i]) / 2 for i in range(3)]
    return (c, norm(sub(a, b)) / 2)


def ball3(a, b, c):
    ab = sub(b, a)
    ac = sub(c, a)
    nrm = cross(ab, ac)
    if norm(nrm) < 1e-12:                       # 共线
        cands = [ball2(a, b), ball2(a, c), ball2(b, c)]
        return max(cands, key=lambda t: t[1])
    A11 = dot(ab, ab)
    A12 = dot(ab, ac)
    A22 = dot(ac, ac)
    b1 = A11 / 2
    b2 = A22 / 2
    det = A11 * A22 - A12 * A12
    u = (b1 * A22 - b2 * A12) / det
    v = (A11 * b2 - A12 * b1) / det
    cen = [a[i] + u * ab[i] + v * ac[i] for i in range(3)]
    return (cen, norm(sub(cen, a)))


def ball4(a, b, c, d):
    M = []
    rhs = []
    for q in (b, c, d):
        M.append([2 * (q[i] - a[i]) for i in range(3)])
        rhs.append(sum(q[i] * q[i] - a[i] * a[i] for i in range(3)))

    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    D = det(M)
    if abs(D) < 1e-9:                           # 共面
        return max([ball3(a, b, c), ball3(a, b, d), ball3(a, c, d), ball3(b, c, d)], key=lambda t: t[1])
    sol = []
    for col in range(3):
        Mc = [row[:] for row in M]
        for i in range(3):
            Mc[i][col] = rhs[i]
        sol.append(det(Mc) / D)
    return (sol, norm(sub(sol, a)))


def ball_from(basis):
    if not basis:
        return (None, -1.0)
    if len(basis) == 1:
        return ball1(basis[0])
    if len(basis) == 2:
        return ball2(basis[0], basis[1])
    if len(basis) == 3:
        return ball3(basis[0], basis[1], basis[2])
    return ball4(basis[0], basis[1], basis[2], basis[3])


def contains(ball, p, eps=1e-9):
    c, r = ball
    if c is None:
        return False
    return norm(sub(p, c)) <= r + eps


def miniball_rec(pts, basis, rng):
    if len(basis) == 4 or not pts:
        return ball_from(basis)
    p = pts[-1]
    rest = pts[:-1]
    b = miniball_rec(rest, basis, rng)
    if p is not None and not contains(b, p):
        return miniball_rec(rest, basis + [p], rng)
    return b


def miniball(points):
    pts = list(points)
    rng = random.Random(12345)
    rng.shuffle(pts)
    ball = (None, -1.0)
    for i, p in enumerate(pts):
        if not contains(ball, p):
            ball = miniball_rec(pts[:i], [p], rng)
    return ball


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    pts = []
    for i in range(n):
        pts.append(tuple(float(x) for x in data[1 + 3 * i:4 + 3 * i]))
    toks = open(sys.argv[2]).read().split()
    if len(toks) < 3:
        print("应输出三个实数", file=sys.stderr)
        return 1
    try:
        q = tuple(float(t) for t in toks[:3])
    except ValueError:
        print("坐标不是实数", file=sys.stderr)
        return 1
    if any(abs(v) > 1e12 for v in q):
        print("坐标过大", file=sys.stderr)
        return 1
    d = max(norm(sub(q, p)) for p in pts)
    c, R = miniball(pts)
    tol = 1e-6 * max(1.0, R)
    if abs(d - R) > tol:
        print(f"最远距离 {d} 与最优半径 {R} 相差超过容差 {tol}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
