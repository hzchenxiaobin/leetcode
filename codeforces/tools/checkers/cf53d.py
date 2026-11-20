import sys

def main():
    data = open(sys.argv[1]).read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    b0 = list(map(int, data[1 + n:1 + 2 * n]))
    out = open(sys.argv[2]).read().split()
    if not out:
        print('FAIL empty'); sys.exit(1)
    k = int(out[0])
    if k < 0 or k > 10 ** 6:
        print('FAIL k out of range'); sys.exit(1)
    if len(out) != 1 + 2 * k:
        print('FAIL wrong number of tokens'); sys.exit(1)
    b = b0[:]
    pos = 1
    for _ in range(k):
        p = int(out[pos]); q = int(out[pos + 1]); pos += 2
        if not (1 <= p <= n - 1) or q != p + 1:
            print('FAIL bad swap', p, q); sys.exit(1)
        b[p - 1], b[p] = b[p], b[p - 1]
    if b != a:
        print('FAIL final arrangement differs'); sys.exit(1)
    print('OK')

main()
