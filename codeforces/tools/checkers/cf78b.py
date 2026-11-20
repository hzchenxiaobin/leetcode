#!/usr/bin/env python3
"""CF78B Easter Eggs 的构造校验器（本题是 special judge，答案不唯一）。

用法: python3 cf78b.py <input> <output> [expected]
  input：一行一个整数 n（7 <= n <= 100）
  output：一行 n 个字符，取自 R O Y G B I V

校验条件（与题面逐条对应）：
  1. 输出恰好一行、恰好 n 个字符，且每个字符都在 "ROYGBIV" 中；
  2. 七种颜色每种至少出现一次；
  3. 圆环上任意连续 4 个彩蛋颜色两两不同（含跨越末尾回到开头的情况）。
"""
import sys

COLORS = "ROYGBIV"


def main() -> int:
    inp_path, out_path = sys.argv[1], sys.argv[2]
    n = int(open(inp_path).read().split()[0])
    raw = open(out_path).read()
    lines = [ln.strip() for ln in raw.replace("\r\n", "\n").split("\n") if ln.strip()]
    if len(lines) != 1:
        print(f"应输出恰好一行非空内容，实际 {len(lines)} 行", file=sys.stderr)
        return 1
    s = lines[0]
    if len(s) != n:
        print(f"长度应为 {n}，实际 {len(s)}", file=sys.stderr)
        return 1
    bad = sorted(set(ch for ch in s if ch not in COLORS))
    if bad:
        print(f"出现非法颜色字符 {bad}", file=sys.stderr)
        return 1
    missing = [c for c in COLORS if c not in s]
    if missing:
        print(f"缺少颜色 {missing}（七种颜色必须都用至少一次）", file=sys.stderr)
        return 1
    for i in range(n):
        four = [s[(i + k) % n] for k in range(4)]
        if len(set(four)) != 4:
            print(f"位置 {i} 起连续 4 个彩蛋出现同色: {''.join(four)}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
