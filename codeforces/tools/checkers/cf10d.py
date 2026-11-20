# CF10D 特殊评测校验器：checker.py <input> <output> <answer>
import sys


def lcis_len(a, b):
    n, m = len(a), len(b)
    f = [0] * (m + 1)
    ans = 0
    for i in range(1, n + 1):
        cur = 0
        for j in range(1, m + 1):
            if a[i - 1] > b[j - 1]:
                cur = max(cur, f[j])
            elif a[i - 1] == b[j - 1]:
                f[j] = max(f[j], cur + 1)
            ans = max(ans, f[j])
    return ans


def is_subseq_of(seq, arr):
    it = iter(arr)
    return all(any(x == y for y in it) for x in seq)


def main():
    data = open(sys.argv[1]).read().split()
    p = 0
    n = int(data[p]); p += 1
    a = [int(x) for x in data[p:p + n]]; p += n
    m = int(data[p]); p += 1
    b = [int(x) for x in data[p:p + m]]; p += m
    out = open(sys.argv[2]).read().split()
    if not out:
        print('empty output'); return 1
    try:
        k = int(out[0])
    except ValueError:
        print('first token not integer'); return 1
    try:
        seq = [int(x) for x in out[1:]]
    except ValueError:
        print('non-integer in sequence'); return 1
    want = lcis_len(a, b)
    if k != want:
        print(f'length {k} != {want}'); return 1
    if len(seq) != k:
        print(f'sequence has {len(seq)} elements, expected {k}'); return 1
    if any(seq[t] >= seq[t + 1] for t in range(k - 1)):
        print('not strictly increasing'); return 1
    if not is_subseq_of(seq, a):
        print('not a subsequence of a'); return 1
    if not is_subseq_of(seq, b):
        print('not a subsequence of b'); return 1
    return 0


sys.exit(main())
