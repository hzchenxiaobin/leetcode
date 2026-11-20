#!/usr/bin/env python3
"""CF164C Machine Programming 的答案校验器（方案不唯一）。

用法: python3 cf164c.py <input> <output> <expected>

校验：输出 n 个 0/1；所选任务能在 k 台机器上完成（按开始时间贪心分配）；
      总收益等于最优值（用 2^n 枚举求最优）。
"""
import sys


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, k = int(data[0]), int(data[1])
    s, t, c = [], [], []
    p = 2
    for _ in range(n):
        s.append(int(data[p])); t.append(int(data[p + 1])); c.append(int(data[p + 2])); p += 3
    out = [int(x) for x in open(sys.argv[2]).read().split()]
    if len(out) != n or any(x not in (0, 1) for x in out):
        print("输出必须是 n 个 0/1", file=sys.stderr)
        return 1
    sel = [i for i in range(n) if out[i] == 1]
    # 可行性：按开始时间排序后贪心分配机器
    free = [0] * k
    for i in sorted(sel, key=lambda i: s[i]):
        j = min(range(k), key=lambda x: free[x])
        if free[j] > s[i]:
            print("所选任务无法在 k 台机器上完成", file=sys.stderr)
            return 1
        free[j] = s[i] + t[i]
    profit = sum(c[i] for i in sel)
    # 最优值：枚举子集
    best = 0
    for mask in range(1 << n):
        sub = [i for i in range(n) if mask >> i & 1]
        free = [0] * k
        ok = True
        for i in sorted(sub, key=lambda i: s[i]):
            j = min(range(k), key=lambda x: free[x])
            if free[j] > s[i]:
                ok = False
                break
            free[j] = s[i] + t[i]
        if ok:
            best = max(best, sum(c[i] for i in sub))
    if profit != best:
        print(f"收益 {profit} 不是最优 {best}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
