import sys

def brute_next(n, m, p):
    eid = {}
    for t in range(m):
        u, v = p[t], p[t + 1]
        eid[(u, v)] = eid[(v, u)] = t
    used = [False] * m
    cur = [p[0]]
    res = []
    def dfs(v, cnt):
        if cnt == m:
            if v == p[0]:
                res.append(tuple(cur))
            return
        for w in range(1, n + 1):
            if w == v:
                continue
            k = eid.get((v, w))
            if k is None or used[k]:
                continue
            used[k] = True
            cur.append(w)
            dfs(w, cnt + 1)
            cur.pop()
            used[k] = False
    dfs(p[0], 0)
    res = sorted(set(res))
    old = tuple(p)
    i = res.index(old)
    return res[i + 1] if i + 1 < len(res) else None

def main():
    data = open(sys.argv[1]).read().split()
    n = int(data[0]); m = int(data[1])
    p = [int(x) for x in data[2:2 + m + 1]]
    out = open(sys.argv[2]).read().split()
    if not out:
        print("FAIL empty output"); sys.exit(1)
    if out[0] == "No":
        if len(out) != 2 or out[1] != "solution":
            print("FAIL bad No solution line"); sys.exit(1)
        if m <= 9:
            nxt = brute_next(n, m, p)
            if nxt is not None:
                print("FAIL claimed no solution but exists"); sys.exit(1)
        print("OK")
        return
    if len(out) != m + 1:
        print("FAIL expected %d vertices" % (m + 1)); sys.exit(1)
    q = [int(x) for x in out]
    if q[0] != p[0] or q[-1] != p[0]:
        print("FAIL start/end mismatch"); sys.exit(1)
    eid = {}
    for t in range(m):
        u, v = p[t], p[t + 1]
        eid[(u, v)] = eid[(v, u)] = t
    used = [False] * m
    for t in range(m):
        u, v = q[t], q[t + 1]
        k = eid.get((u, v))
        if k is None:
            print("FAIL nonexistent edge", u, v); sys.exit(1)
        if used[k]:
            print("FAIL edge reused", u, v); sys.exit(1)
        used[k] = True
    if any(not x for x in used):
        print("FAIL not all edges used"); sys.exit(1)
    if q <= p:
        print("FAIL not lexicographically greater"); sys.exit(1)
    if m <= 9:
        nxt = brute_next(n, m, p)
        if nxt is None or tuple(q) != nxt:
            print("FAIL not the lexicographically smallest next circuit"); sys.exit(1)
    print("OK")

main()
