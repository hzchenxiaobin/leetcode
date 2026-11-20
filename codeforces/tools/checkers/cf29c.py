#!/usr/bin/env python3
"""29C checker：路线必须是 n+1 个互不相同的城市，且相邻两城之间有一枚邮戳。"""
import sys


def main():
    if len(sys.argv) < 3:
        print("usage: chk.py input output")
        return 2
    data = list(map(int, open(sys.argv[1]).read().split()))
    n = data[0]
    stamps = set()
    p = 1
    for _ in range(n):
        a, b = data[p], data[p + 1]
        p += 2
        stamps.add((a, b))
        stamps.add((b, a))
    out = list(map(int, open(sys.argv[2]).read().split()))
    if len(out) != n + 1:
        print(f"FAIL: expected {n+1} cities, got {len(out)}")
        return 1
    if len(set(out)) != n + 1:
        print("FAIL: repeated city")
        return 1
    for i in range(n):
        if (out[i], out[i + 1]) not in stamps:
            print(f"FAIL: no stamp between {out[i]} and {out[i+1]}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
