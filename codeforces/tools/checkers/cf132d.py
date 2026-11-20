#!/usr/bin/env python3
"""CF132D Constants in the language of Shakespeare 的答案校验器（答案不唯一）。

用法: python3 cf132d.py <input> <output> <expected>

输入：一个正整数的二进制表示 s（可能长达 10^6 位）。
输出：第一行 m，随后 m 行形如 "+2^x" 或 "-2^x"。

校验条件：
  1. 第一行是整数 m，之后恰好 m 行，每行匹配 ^[+-]2\\^(\\d+)$；
  2. 这些项按符号求和必须恰好等于 n（用 Python 大整数精确计算）；
  3. m 必须等于最小项数（checker 用「低位到高位 + 进位状态」的 DP 独立求出，
     与题解里的贪心是两套写法）。
"""
import re
import sys

LINE_RE = re.compile(r"^([+-])2\^(\d+)$")


def min_terms(s):
    """从最低位到最高位的进位 DP：dp[c] = 处理完低位后、当前进位为 c 时的最少项数。"""
    ln = len(s)
    INF = 10 ** 9
    dp = [0, INF]  # carry 0 / 1
    bits = s[::-1]
    for i in range(ln):
        b = int(bits[i])
        nd = [INF, INF]
        for c in (0, 1):
            cur = dp[c]
            if cur >= INF:
                continue
            t = b + c
            if t == 0:
                nd[0] = min(nd[0], cur)
            elif t == 2:
                nd[1] = min(nd[1], cur)
            else:  # t == 1：放 +1（进位 0）或 -1（进位 1），各用一个项
                nd[0] = min(nd[0], cur + 1)
                nd[1] = min(nd[1], cur + 1)
        dp = nd
    # 处理完所有位后，若还有进位，需要额外一个 +2^len 的项
    return min(dp[0], dp[1] + 1)


def main() -> int:
    s = open(sys.argv[1]).read().split()[0]
    n = int(s, 2)

    lines = [l.strip() for l in open(sys.argv[2]).read().split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    if not lines:
        print("输出为空", file=sys.stderr)
        return 1
    try:
        m = int(lines[0])
    except ValueError:
        print("第一行不是整数", file=sys.stderr)
        return 1
    body = lines[1:]
    if len(body) != m:
        print(f"声明 {m} 项，实际 {len(body)} 项", file=sys.stderr)
        return 1
    total = 0
    for i, line in enumerate(body):
        mt = LINE_RE.match(line)
        if not mt:
            print(f"第 {i + 2} 行格式不对: {line!r}", file=sys.stderr)
            return 1
        sign = 1 if mt.group(1) == "+" else -1
        x = int(mt.group(2))
        total += sign * (1 << x)
    if total != n:
        print("这些项的和不等于 n", file=sys.stderr)
        return 1
    best = min_terms(s)
    if m != best:
        print(f"项数 {m} 不是最小值 {best}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
