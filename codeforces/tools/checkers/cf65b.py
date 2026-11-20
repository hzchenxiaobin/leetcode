"""65B checker：输入 + 选手输出 + 参考答案（样例输出）。返回 0 表示通过。

校验条件：
1. 若输出 "No solution"：独立 DP 判定确实无解；
2. 否则必须恰好 n 行整数 z_i，满足 1000 <= z_i <= 2011、与 y_i 至多一位数字不同、
   且 z 单调不减；
3. 若独立 DP 判定有解而选手给 "No solution"，拒绝。
"""
import sys

LO, HI = 1000, 2011


def candidates(y):
    d = [y // 1000, y // 100 % 10, y // 10 % 10, y % 10]
    s = set()
    for pos in range(-1, 4):
        for nd in range(10):
            if pos >= 0 and nd == d[pos]:
                continue
            v = 0
            for k in range(4):
                v = v * 10 + (nd if k == pos else d[k])
            if LO <= v <= HI:
                s.add(v)
    return s


def feasible(ys):
    """独立判定：维护每步可达取值集合的最小值（集合只由最小元决定后续可行性）。"""
    cur_min = LO           # 第一步之前允许的下界是 1000
    for y in ys:
        vals = [v for v in candidates(y) if v >= cur_min]
        if not vals:
            return False
        cur_min = min(vals)
    return True


def main():
    inp, outp, _ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    n = int(data[0])
    ys = [int(x) for x in data[1:1 + n]]
    toks = open(outp).read().split()
    ok_exist = feasible(ys)
    if toks and toks[0].lower() == 'no' and len(toks) >= 2 and toks[1].lower() == 'solution':
        if ok_exist:
            print('checker: 有解却输出 No solution')
            return 1
        return 0
    if not ok_exist:
        print('checker: 无解却输出了序列')
        return 1
    if len(toks) != n:
        print('checker: 数字个数不是 n')
        return 1
    try:
        zs = [int(t) for t in toks]
    except ValueError:
        print('checker: 有非整数 token')
        return 1
    for i in range(n):
        if not (LO <= zs[i] <= HI):
            print('checker: 越界', zs[i])
            return 1
        diff = sum(1 for k in range(4)
                   if (zs[i] // (10 ** (3 - k)) % 10) != (ys[i] // (10 ** (3 - k)) % 10))
        if diff > 1:
            print('checker: 改了不止一位', zs[i], ys[i])
            return 1
        if i and zs[i] < zs[i - 1]:
            print('checker: 不是非降序')
            return 1
    return 0


sys.exit(main())
