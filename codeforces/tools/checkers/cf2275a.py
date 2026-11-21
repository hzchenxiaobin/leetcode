#!/usr/bin/env python3
"""CF2275A 校验器（特殊评测：输出任意一个合法整点）。

用法: cf2275a.py <input> <output> <answer>

对每组 (x0, y0, R)：校验输出的 (x, y) 是整点且 (x-x0)^2+(y-y0)^2 == R^2。
"""
import sys


def fail(msg):
    print("WRONG: " + msg)
    sys.exit(1)


def main():
    inp = open(sys.argv[1], encoding='utf-8').read().split()
    out = open(sys.argv[2], encoding='utf-8').read().split()
    t = int(inp[0])
    if len(out) != 2 * t:
        fail("应有 %d 个数，实际 %d 个" % (2 * t, len(out)))
    try:
        nums = [int(v) for v in out]
    except ValueError:
        fail("输出含非整数")
    idx = 1
    for tc in range(t):
        x0, y0, r = int(inp[idx]), int(inp[idx + 1]), int(inp[idx + 2])
        idx += 3
        x, y = nums[2 * tc], nums[2 * tc + 1]
        dx, dy = x - x0, y - y0
        if dx * dx + dy * dy != r * r:
            fail("第 %d 组：(%d,%d) 到 (%d,%d) 的平方距离为 %d，应为 %d"
                 % (tc + 1, x, y, x0, y0, dx * dx + dy * dy, r * r))


main()
