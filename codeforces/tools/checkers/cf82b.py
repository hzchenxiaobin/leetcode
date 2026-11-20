#!/usr/bin/env python3
"""CF82B Sets 的 checker。

题意：n 个互不相交的非空集合，输入给出所有两两并集（顺序、数字顺序都被打乱），
要求还原出这 n 个集合；多解，任意顺序输出均可。

校验：
1. 输出恰好 n 行，每行「k 后面跟 k 个数」，k >= 1，行内数字互不相同；
2. 所有输出数字恰好等于输入里出现过的数字集合，每个出现一次（即自动互不相交）；
3. 这 n 个集合的两两并集（作为可重集合）与输入纸条的可重集合逐一相同。

用法: python3 cf82b.py <input> <output> <answer>；返回 0 通过。
"""
import sys
from collections import Counter


def main():
    inp, out = sys.argv[1], sys.argv[2]
    tok = open(inp).read().split()
    pos = 0
    n = int(tok[pos]); pos += 1
    papers = []
    for _ in range(n * (n - 1) // 2):
        k = int(tok[pos]); pos += 1
        papers.append(frozenset(int(x) for x in tok[pos:pos + k]))
        pos += k
    allnums = set()
    for s in papers:
        allnums |= s

    raw = open(out).read().split('\n')
    lines = [l for l in raw if l.strip()]
    if len(lines) != n:
        print(f'CHECKER FAIL: 需要 {n} 行，实际 {len(lines)} 行')
        return 1
    sets, used = [], []
    for line in lines:
        t = line.split()
        k = int(t[0])
        if len(t) != k + 1 or k < 1:
            print(f'CHECKER FAIL: 行格式不对: {line!r}')
            return 1
        vals = [int(x) for x in t[1:]]
        if len(set(vals)) != k:
            print('CHECKER FAIL: 同一行有重复数字')
            return 1
        sets.append(frozenset(vals))
        used.extend(vals)
    if sorted(used) != sorted(allnums):
        print('CHECKER FAIL: 输出的数字与输入出现过的数字集合不一致（或重复/遗漏）')
        return 1
    unions = []
    for i in range(n):
        for j in range(i + 1, n):
            unions.append(sets[i] | sets[j])
    if Counter(unions) != Counter(papers):
        print('CHECKER FAIL: 还原集合的两两并集与输入纸条不一致')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
