#!/usr/bin/env python3
"""CF105C Item World 的构造校验器（答案不唯一）。

用法: python3 cf105c.py <input> <output> [expected]
  input：n / n 行 "name class atk def res size" / k / k 行 "name type bonus home"
  output：三行，依次是 weapon、armor、defensive orb：
          "itemName cnt r1 r2 ... rcnt"

校验条件：
  1. 三行的物品存在、类别依次是 weapon / armor / orb，且互不相同；
  2. 每行列出的居民存在、全局不重复（一个居民不能同时在两件物品里），
     且数量不超过该物品的 size；
  3. 若所有物品的总容量恰好等于居民总数（一个空位都没有），则什么都不能移动：
     列出的居民必须恰好是该物品原本就有的那些；
  4. 目标值必须最优（字典序）：weapon 的 atk、armor 的 def、orb 的 res 分别等于
     "最优可重排"（或"不可移动"）情形下的最大值。由于三类居民只分别加成
     atk / def / res，三个最大值可以独立取到，所以分别比较即可。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    p = 0
    n = int(data[p]); p += 1
    items = []
    for _ in range(n):
        items.append((data[p], data[p + 1], int(data[p + 2]), int(data[p + 3]),
                      int(data[p + 4]), int(data[p + 5])))
        p += 6
    k = int(data[p]); p += 1
    res = []
    for _ in range(k):
        res.append((data[p], data[p + 1], int(data[p + 2]), data[p + 3]))
        p += 4
    name2item = {it[0]: i for i, it in enumerate(items)}
    name2res = {r[0]: i for i, r in enumerate(res)}
    total_cap = sum(it[5] for it in items)
    frozen = (total_cap == k)

    init = [[] for _ in range(n)]
    for ri, r in enumerate(res):
        init[name2item[r[3]]].append(ri)

    def pref(t):
        v = sorted((r[2] for r in res if r[1] == t), reverse=True)
        pre = [0]
        for x in v:
            pre.append(pre[-1] + x)
        return pre

    preQ = {"gladiator": pref("gladiator"), "sentry": pref("sentry"), "physician": pref("physician")}
    idxOf = {"weapon": 2, "armor": 3, "orb": 4}
    typeOf = {"weapon": "gladiator", "armor": "sentry", "orb": "physician"}

    best = {}
    for cls in ("weapon", "armor", "orb"):
        t = typeOf[cls]
        pre = preQ[t]
        b = -1
        for i, it in enumerate(items):
            if it[1] != cls:
                continue
            add = sum(res[ri][2] for ri in init[i] if res[ri][1] == t) if frozen else pre[min(it[5], len(pre) - 1)]
            b = max(b, it[idxOf[cls]] + add)
        best[cls] = b

    lines = [ln.split() for ln in open(sys.argv[2]).read().splitlines() if ln.split()]
    if len(lines) != 3:
        print("应输出恰好三行", file=sys.stderr)
        return 1
    used_items = []
    used_res = set()
    got = {}
    for li, cls in enumerate(("weapon", "armor", "orb")):
        line = lines[li]
        if len(line) < 2:
            print(f"第 {li+1} 行格式错误", file=sys.stderr)
            return 1
        iname = line[0]
        if iname not in name2item:
            print(f"物品 {iname} 不存在", file=sys.stderr)
            return 1
        ii = name2item[iname]
        used_items.append(ii)
        if items[ii][1] != cls:
            print(f"第 {li+1} 行物品类别应为 {cls}，实际 {items[ii][1]}", file=sys.stderr)
            return 1
        try:
            cnt = int(line[1])
        except ValueError:
            print("数量不是整数", file=sys.stderr)
            return 1
        names = line[2:]
        if len(names) != cnt:
            print(f"第 {li+1} 行声明 {cnt} 个居民，实际列出 {len(names)} 个", file=sys.stderr)
            return 1
        if cnt > items[ii][5]:
            print(f"物品 {iname} 容量 {items[ii][5]}，放了 {cnt} 个", file=sys.stderr)
            return 1
        listed = []
        for rn in names:
            if rn not in name2res:
                print(f"居民 {rn} 不存在", file=sys.stderr)
                return 1
            ri = name2res[rn]
            if ri in used_res:
                print(f"居民 {rn} 被重复放置", file=sys.stderr)
                return 1
            used_res.add(ri)
            listed.append(ri)
        if frozen:
            if sorted(listed) != sorted(init[ii]):
                print(f"没有空位时物品 {iname} 的居民不能改变", file=sys.stderr)
                return 1
        t = typeOf[cls]
        got[cls] = items[ii][idxOf[cls]] + sum(res[ri][2] for ri in listed if res[ri][1] == t)
    if len(set(used_items)) != 3:
        print("三件物品必须互不相同", file=sys.stderr)
        return 1
    for cls in ("weapon", "armor", "orb"):
        if got[cls] != best[cls]:
            print(f"{cls} 的目标值 {got[cls]} 不是最优 {best[cls]}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
