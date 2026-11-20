#!/usr/bin/env python3
"""CF166D Shoe Store 的答案校验器（方案不唯一）。

用法: python3 cf166d.py <input> <output> <expected>

校验：每行 (顾客, 鞋) 合法（编号有效、不重复、钱够、脚码匹配），
      总收益等于最优值（小规模用暴力求最优，大规模退化为只校验可行性）。
"""
import sys


def brute_opt(n, m, price, size_, money, foot):
    # 最大权匹配（规模小）：枚举鞋子的子集 + 二分图匹配判定
    best = 0
    shoe_list = list(range(n))
    for mask in range(1 << n):
        chosen = [i for i in shoe_list if mask >> i & 1]
        # 判定 chosen 能否被匹配
        adj = []
        for si in chosen:
            cand = [ci for ci in range(m) if foot[ci] in (size_[si] - 1, size_[si]) and money[ci] >= price[si]]
            adj.append(cand)
        match = [-1] * m

        def aug(k, seen):
            for ci in adj[k]:
                if seen[ci]:
                    continue
                seen[ci] = True
                if match[ci] == -1 or aug(match[ci], seen):
                    match[ci] = k
                    return True
            return False

        ok = True
        for k in range(len(chosen)):
            if not aug(k, [False] * m):
                ok = False
                break
        if ok:
            best = max(best, sum(price[si] for si in chosen))
    return best


def main() -> int:
    data = open(sys.argv[1]).read().split()
    p = 0
    n = int(data[p]); p += 1
    price = [0] * n
    size_ = [0] * n
    for i in range(n):
        price[i] = int(data[p]); size_[i] = int(data[p + 1]); p += 2
    m = int(data[p]); p += 1
    money = [0] * m
    foot = [0] * m
    for i in range(m):
        money[i] = int(data[p]); foot[i] = int(data[p + 1]); p += 2

    lines = [l for l in open(sys.argv[2]).read().split("\n") if l.strip()]
    if len(lines) < 2:
        print("输出至少两行", file=sys.stderr)
        return 1
    try:
        total = int(lines[0].split()[0])
        k = int(lines[1].split()[0])
    except ValueError:
        print("前两行应为整数", file=sys.stderr)
        return 1
    if len(lines) - 2 != k:
        print(f"声明卖出 {k} 双，实际列出 {len(lines) - 2} 行", file=sys.stderr)
        return 1
    used_c = set()
    used_s = set()
    s_total = 0
    for line in lines[2:]:
        ci, si = (int(x) - 1 for x in line.split()[:2])
        if not (0 <= ci < m) or not (0 <= si < n):
            print("编号越界", file=sys.stderr)
            return 1
        if ci in used_c or si in used_s:
            print("顾客或鞋子重复", file=sys.stderr)
            return 1
        if money[ci] < price[si]:
            print(f"顾客 {ci + 1} 钱不够买鞋 {si + 1}", file=sys.stderr)
            return 1
        if size_[si] not in (foot[ci], foot[ci] + 1):
            print(f"顾客 {ci + 1} 脚码与鞋 {si + 1} 不匹配", file=sys.stderr)
            return 1
        used_c.add(ci); used_s.add(si); s_total += price[si]
    if s_total != total:
        print(f"总收益 {total} 与明细和 {s_total} 不符", file=sys.stderr)
        return 1
    if n <= 10 and m <= 10:
        opt = brute_opt(n, m, price, size_, money, foot)
        if total != opt:
            print(f"总收益 {total} 不是最优 {opt}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
