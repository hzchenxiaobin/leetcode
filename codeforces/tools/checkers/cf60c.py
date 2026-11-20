#!/usr/bin/env python3
"""60C 的 checker：校验输出的格式与合法性。

用法: python3 checker.py <input> <output>   （第三参数"标准答案"可忽略）

校验内容：
  * 第一行只能是 YES 或 NO；
  * 输出 NO：本 checker 直接接受（"确实无解"等价于把题再做一遍，
    因此在正文的验证记录里，NO 的正确性由"小值域全枚举暴力"另行核对）；
  * 输出 YES：必须恰好有 n 个正整数，且对输入的每条边 (u,v,gcd,lcm) 都有
    gcd(a_u,a_v)=gcd 且 lcm(a_u,a_v)=lcm；
  * 不允许缺数或多出 token。
"""
import sys
from math import gcd


def main():
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    n, m = int(data[0]), int(data[1])
    p = 2
    edges = []
    for _ in range(m):
        u, v, g, l = (int(x) for x in data[p:p + 4])
        p += 4
        edges.append((u - 1, v - 1, g, l))
    out = open(outp).read().split()
    if not out:
        sys.exit(1)
    if out[0] == "NO":
        if len(out) != 1:
            sys.exit(1)
        return
    if out[0] != "YES":
        sys.exit(1)
    vals = out[1:]
    if len(vals) != n:
        sys.exit(1)
    a = []
    for t in vals:
        if not t.isdigit():
            sys.exit(1)
        a.append(int(t))
    if any(x < 1 for x in a):
        sys.exit(1)
    for u, v, g, l in edges:
        gg = gcd(a[u], a[v])
        if gg != g:
            sys.exit(1)
        if a[u] // gg * a[v] != l:
            sys.exit(1)


main()
