import sys

def main():
    inp, out = sys.argv[1], sys.argv[2]
    data = list(map(int, open(inp).read().split()))
    pos = 0
    n, k = data[pos], data[pos+1]; pos += 2
    d = [0]*n
    for i in range(1, n):
        d[i] = data[pos]; pos += 1
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        a, b = data[pos]-1, data[pos+1]-1; pos += 2
        adj[a].append(b); adj[b].append(a)
    dist = [[-1]*n for _ in range(n)]
    for s in range(n):
        dist[s][s] = 0
        q = [s]
        for v in q:
            for u in adj[v]:
                if dist[s][u] < 0:
                    dist[s][u] = dist[s][v]+1
                    q.append(u)
    best = None
    for mask in range(1, 1 << n):
        cost = k * bin(mask).count('1')
        for v in range(n):
            if mask >> v & 1:
                continue
            cost += d[min(dist[v][c] for c in range(n) if mask >> c & 1)]
        if best is None or cost < best:
            best = cost
    toks = open(out).read().split()
    if len(toks) < n + 1:
        sys.exit(1)
    cost = int(toks[0])
    assign = [int(t)-1 for t in toks[1:1+n]]
    if cost != best:
        sys.exit(1)
    sets = [i for i in range(n) if assign[i] == i]
    if not sets:
        sys.exit(1)
    for i, c in enumerate(assign):
        if not (0 <= c < n):
            sys.exit(1)
        if c != i and assign[c] != c:
            sys.exit(1)
    real = k * len(sets)
    for i, c in enumerate(assign):
        if c != i:
            real += d[dist[i][c]]
    if real != cost:
        sys.exit(1)
    sys.exit(0)

main()
