#!/usr/bin/env python3
"""CF148C Terse princess 的答案校验器（序列不唯一）。

用法: python3 cf148c.py <input> <output> <expected>

输入：n a b（保证 n > a+b）。
输出：一行 n 个整数，或单独一个 -1。

校验条件：
  1. 若输出 -1：检查"必要元素数" 1 + b + [b==0 and a>0] + a 确实 > n；
  2. 否则：必须恰好 n 个整数，且每个在 [1, 50000]；
  3. 按题面规则重新数一遍：t_i > 前缀和 ⇒ Wow；否则 t_i > 前缀最大值 ⇒ Oh；
     第一位不计数。要求 Oh 次数 = a、Wow 次数 = b。
"""
import sys

LIMIT = 50000


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n, a, b = int(data[0]), int(data[1]), int(data[2])

    out = open(sys.argv[2]).read().split()
    if not out:
        print("输出为空", file=sys.stderr)
        return 1

    if out == ["-1"]:
        need = 1 + b + (1 if (b == 0 and a > 0) else 0) + a
        if need <= n:
            print(f"-1 不成立：按必要元素数 {need} <= n={n} 应可构造", file=sys.stderr)
            return 1
        return 0

    if len(out) != n:
        print(f"应输出 {n} 个数，实际 {len(out)} 个", file=sys.stderr)
        return 1
    try:
        t = [int(x) for x in out]
    except ValueError:
        print("输出含非整数", file=sys.stderr)
        return 1
    for x in t:
        if x < 1 or x > LIMIT:
            print(f"财富 {x} 超出 [1,{LIMIT}]", file=sys.stderr)
            return 1

    oh = wow = 0
    mx = t[0]
    total = t[0]
    for x in t[1:]:
        if x > total:
            wow += 1
        elif x > mx:
            oh += 1
        if x > mx:
            mx = x
        total += x
    if oh != a or wow != b:
        print(f"感叹次数不符：得到 Oh={oh}, Wow={wow}，期望 Oh={a}, Wow={b}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
