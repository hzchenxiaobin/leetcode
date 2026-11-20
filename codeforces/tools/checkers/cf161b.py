#!/usr/bin/env python3
"""CF161B Discounts 的答案校验器（购物车分配不唯一）。

用法: python3 cf161b.py <input> <output> <expected>

校验：
  1. 第一行总价（一位小数）与官方最优总价一致；
  2. 后面 k 行分别给出每辆车的商品：每件商品恰出现一次、每辆车非空；
  3. 按题面规则（含凳子的车最便宜商品半价）重算总价，须与第一行一致。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, k = int(data[0]), int(data[1])
    price = [0] * (n + 1)
    typ = [0] * (n + 1)
    p = 2
    for i in range(1, n + 1):
        price[i] = int(data[p]); typ[i] = int(data[p + 1]); p += 2

    out = [l for l in open(sys.argv[2]).read().split("\n") if l.strip()]
    if len(out) != k + 1:
        print(f"应输出 {k + 1} 行，实际 {len(out)} 行", file=sys.stderr)
        return 1
    try:
        val = float(out[0].split()[0])
    except ValueError:
        print("第一行不是实数", file=sys.stderr)
        return 1
    seen = [0] * (n + 1)
    total = 0.0
    for i in range(1, k + 1):
        parts = [int(x) for x in out[i].split()]
        cnt = parts[0]
        items = parts[1:1 + cnt]
        if len(items) != cnt or cnt == 0:
            print(f"第 {i + 1} 行商品数量不符或为空车", file=sys.stderr)
            return 1
        for it in items:
            if not (1 <= it <= n) or seen[it]:
                print(f"商品编号 {it} 非法或重复", file=sys.stderr)
                return 1
            seen[it] = 1
        s = sum(price[it] for it in items)
        if any(typ[it] == 1 for it in items):
            s -= min(price[it] for it in items) / 2.0
        total += s
    if sum(seen[1:]) != n:
        print("有商品未被分配", file=sys.stderr)
        return 1
    if abs(total - val) > 1e-6:
        print(f"第一行总价 {val} 与方案重算 {total} 不符", file=sys.stderr)
        return 1
    exp = open(sys.argv[3]).read().split()
    if exp:
        try:
            best = float(exp[0])
        except ValueError:
            best = None
        if best is not None and abs(val - best) > 1e-6:
            print(f"总价 {val} 不等于最优 {best}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
