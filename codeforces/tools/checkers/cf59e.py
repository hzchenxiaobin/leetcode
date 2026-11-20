import sys
from collections import deque


def main():
    inp, outp, _ = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp, 'rb').read().split()
    p = 0
    n = int(data[p]); m = int(data[p + 1]); k = int(data[p + 2]); p += 3
    edges = set()
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        x = int(data[p]); y = int(data[p + 1]); p += 2
        edges.add((x, y)); edges.add((y, x))
        adj[x].append(y); adj[y].append(x)
    bad = set()
    for _ in range(k):
        bad.add((int(data[p]), int(data[p + 1]), int(data[p + 2])))
        p += 3
    exp_tokens = sys.stdin.read().split()
    exp_d = int(exp_tokens[0]) if exp_tokens else None
    toks = open(outp).read().split()
    if not toks:
        print("WRONG: empty output"); sys.exit(1)
    if toks[0] == '-1':
        if len(toks) != 1 or exp_d != -1:
            print("WRONG: -1 mismatch"); sys.exit(1)
        sys.exit(0)
    if len(toks) < 2:
        print("WRONG: missing path"); sys.exit(1)
    d = int(toks[0])
    path = [int(x) for x in toks[1:]]
    if len(path) != d + 1:
        print("WRONG: path has %d vertices, d=%d" % (len(path), d)); sys.exit(1)
    if path[0] != 1 or path[-1] != n:
        print("WRONG: path endpoints"); sys.exit(1)
    for a, b in zip(path, path[1:]):
        if (a, b) not in edges:
            print("WRONG: %d-%d is not a road" % (a, b)); sys.exit(1)
    for i in range(d - 1):
        if (path[i], path[i + 1], path[i + 2]) in bad:
            print("WRONG: forbidden triplet at %d" % (i + 1)); sys.exit(1)
    if exp_d is not None and d != exp_d:
        print("WRONG: d=%d expected %d" % (d, exp_d)); sys.exit(1)
    sys.exit(0)


main()
