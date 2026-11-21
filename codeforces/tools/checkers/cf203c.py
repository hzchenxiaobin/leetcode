#!/usr/bin/env python3
"""CF203C Photographer 的特殊评测器（多解：服务人数最大即可，客户顺序任意）。

约定：python3 cf203c.py <input> <output> <answer>，返回 0 表示通过。

校验条件：
1. 第一行是整数 k，第二行恰好 k 个互不相同的客户编号，均落在 [1, n]；
2. 这些客户的总内存 a*x_i + b*y_i 之和不超过相机容量 d（缺省按 0 个客户处理空行）；
3. k 等于最优值（评测器内部用"按花费升序取前缀"独立算出）。
"""
import sys


def main():
    inp, out = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    n, d = int(data[0]), int(data[1])
    a, b = int(data[2]), int(data[3])
    cost = [0] * (n + 1)
    pos = 4
    for i in range(1, n + 1):
        x, y = int(data[pos]), int(data[pos + 1])
        pos += 2
        cost[i] = a * x + b * y

    # 评测器独立求最优：按单个客户花费升序取前缀
    best, used = 0, 0
    for c in sorted(cost[1:]):
        if used + c > d:
            break
        used += c
        best += 1

    toks = open(out).read().split()
    if not toks:
        return 1
    try:
        k = int(toks[0])
    except ValueError:
        print('CHECKER FAIL: 第一行不是整数')
        return 1
    ids = toks[1:]
    if len(ids) != k:
        print(f'CHECKER FAIL: 声明 {k} 个客户但给出 {len(ids)} 个编号')
        return 1
    seen = set()
    total = 0
    for s in ids:
        try:
            i = int(s)
        except ValueError:
            print(f'CHECKER FAIL: 编号 {s!r} 不是整数')
            return 1
        if not 1 <= i <= n:
            print(f'CHECKER FAIL: 编号 {i} 越界')
            return 1
        if i in seen:
            print(f'CHECKER FAIL: 编号 {i} 重复')
            return 1
        seen.add(i)
        total += cost[i]
    if total > d:
        print(f'CHECKER FAIL: 总内存 {total} 超过容量 {d}')
        return 1
    if k != best:
        print(f'CHECKER FAIL: 服务 {k} 人，最优为 {best} 人')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
