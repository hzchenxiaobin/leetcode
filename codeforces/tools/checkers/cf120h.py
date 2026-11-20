#!/usr/bin/env python3
"""CF120H Brevity is Soul of Wit 的校验器（答案不唯一）。

用法: python3 cf120h.py <input> <output> [expected]
  input：n + n 行单词
  output：n 行缩写，或 -1

校验条件：
  1. 输出 -1 时，必须确实不存在完美匹配（校验器自己跑一遍匹配）；
  2. 否则必须 n 行、每行是原词的子序列、长度 1..4、且 n 个缩写两两不同。
"""
import sys


def candidates(w):
    ln = len(w)
    mx = min(4, ln)
    out = set()
    for mask in range(1, 1 << ln):
        if bin(mask).count('1') > mx:
            continue
        out.add(''.join(w[b] for b in range(ln) if mask >> b & 1))
    return out


def feasible(words):
    n = len(words)
    cands = [candidates(w) for w in words]
    match = {}

    def dfs(u, seen):
        for t in cands[u]:
            if t in seen:
                continue
            seen.add(t)
            if t not in match or dfs(match[t], seen):
                match[t] = u
                return True
        return False

    for i in range(n):
        if not dfs(i, set()):
            return False
    return True


def main() -> int:
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    words = [data[1 + i] for i in range(n)]
    lines = [ln.strip() for ln in open(sys.argv[2]) if ln.strip()]
    if len(lines) == 1 and lines[0] == '-1':
        if feasible(words):
            print("存在解，不应输出 -1", file=sys.stderr)
            return 1
        return 0
    if len(lines) != n:
        print(f"应输出 {n} 行，实际 {len(lines)} 行", file=sys.stderr)
        return 1
    if len(set(lines)) != n:
        print("缩写有重复", file=sys.stderr)
        return 1
    for w, t in zip(words, lines):
        if not (1 <= len(t) <= 4):
            print(f"缩写长度非法: {t}", file=sys.stderr)
            return 1
        it = iter(w)
        if not all(ch in it for ch in t):
            print(f"{t} 不是 {w} 的子序列", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
