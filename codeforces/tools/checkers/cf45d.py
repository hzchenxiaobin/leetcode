import sys

def main():
    data = open(sys.argv[1]).read().split()
    out = open(sys.argv[2]).read().split()
    p = 0
    n = int(data[p]); p += 1
    segs = []
    for _ in range(n):
        l = int(data[p]); r = int(data[p+1]); p += 2
        segs.append((l, r))
    if len(out) != n:
        print("wrong count", len(out), n); return 1
    used = set()
    for i, tok in enumerate(out):
        d = int(tok)
        l, r = segs[i]
        if not (l <= d <= r):
            print("event", i, "day", d, "not in", (l, r)); return 1
        if d in used:
            print("day reused", d); return 1
        used.add(d)
    return 0

sys.exit(main())
