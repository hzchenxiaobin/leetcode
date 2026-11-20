import sys

def main():
    inp, outp, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(open(inp).read().split()[0])
    toks = open(outp).read().split()
    if len(toks) != n:
        print("WRONG: expected %d numbers, got %d" % (n, len(toks)))
        sys.exit(1)
    p = [int(t) for t in toks]
    if sorted(p) != list(range(1, n + 1)):
        print("WRONG: not a permutation")
        sys.exit(1)
    # 统计"分布的因数个数"：i 满足存在 j 使 i|j 且 i|p[j]
    cnt = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            if p[j - 1] % i == 0:
                cnt += 1
                break
    if cnt != 1:
        print("WRONG: divisor count %d != 1" % cnt)
        sys.exit(1)
    sys.exit(0)

main()
