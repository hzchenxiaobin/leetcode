# 校验 CF125D 的输出：两行各是一个等差数列，且按原序构成输入的划分（多解，故不能逐字比对）。
# 输出 "No solution" 时：n <= 20 用全枚举独立确认确实无解，否则无法独立确认（返回失败，避免放过）。
import itertools
import sys


def is_ap(seq):
    if len(seq) <= 2:
        return True
    d = seq[1] - seq[0]
    return all(seq[i + 1] - seq[i] == d for i in range(1, len(seq) - 1))


def brute_solvable(a):
    n = len(a)
    for mask in range(1, (1 << n) - 1):          # 两个数列都非空
        p = [a[i] for i in range(n) if (mask >> i) & 1]
        q = [a[i] for i in range(n) if not ((mask >> i) & 1)]
        if is_ap(p) and is_ap(q):
            return p, q
    return None


def as_subsequence(line, a):
    """line 必须是 a 的子序列（值互不相同，贪心匹配唯一）；返回用掉的下标集合或 None。"""
    used, j = set(), 0
    for v in line:
        while j < len(a) and a[j] != v:
            j += 1
        if j == len(a):
            return None
        used.add(j)
        j += 1
    return used


def main():
    data = open(sys.argv[1]).read().split()
    out = open(sys.argv[2]).read()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    toks = out.split()
    if toks and toks[0] == 'No' and len(toks) == 2 and toks[1] == 'solution':
        if n <= 20:
            if brute_solvable(a):
                print('claimed no solution, but one exists')
                return 1
        else:
            print('cannot verify impossibility for n > 20')
            return 1
        return 0
    lines = [ln for ln in out.splitlines() if ln.strip()]
    if len(lines) != 2:
        print('expect exactly two progressions, got %d lines' % len(lines))
        return 1
    seqs = [[int(x) for x in ln.split()] for ln in lines]
    used = [False] * n
    for s in seqs:
        if not s:
            print('empty progression')
            return 1
        if not is_ap(s):
            print('not an arithmetic progression:', s)
            return 1
        got = as_subsequence(s, a)
        if got is None:
            print('progression is not a subsequence of the input:', s)
            return 1
        for idx in got:
            if used[idx]:
                print('element %d used twice' % idx)
                return 1
            used[idx] = True
    if not all(used):
        miss = [i for i in range(n) if not used[i]]
        print('elements not covered:', miss)
        return 1
    return 0


sys.exit(main())
