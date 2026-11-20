import sys

def rev(x):
    r = 0
    while x:
        r = r * 10 + x % 10
        x //= 10
    return r

def brute(mx, my, w):
    cnt = [[0] * (my + 1) for _ in range(mx + 1)]
    for a in range(1, mx + 1):
        ra = rev(a)
        for b in range(1, my + 1):
            if a * b == ra * rev(b):
                cnt[a][b] = 1
    for i in range(1, mx + 1):
        row = cnt[i]
        prev = cnt[i - 1]
        for j in range(1, my + 1):
            row[j] += row[j - 1] + prev[j] - prev[j - 1]
    best = None
    for x in range(1, mx + 1):
        for y in range(1, my + 1):
            if cnt[x][y] >= w:
                area = x * y
                if best is None or area < best:
                    best = area
    return best, cnt

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    mx, my, w = map(int, open(inp).read().split()[:3])
    toks = open(out).read().split()
    best, cnt = brute(mx, my, w)
    if best is None:
        sys.exit(0 if toks == ['-1'] else 1)
    if len(toks) != 2:
        sys.exit(1)
    x, y = int(toks[0]), int(toks[1])
    if not (1 <= x <= mx and 1 <= y <= my):
        sys.exit(1)
    if cnt[x][y] < w:
        sys.exit(1)
    if x * y != best:
        sys.exit(1)
    sys.exit(0)

main()
