import sys

def die(msg):
    print("FAIL:", msg)
    sys.exit(1)

def brute_possible(grid, n, m):
    # independent exact-cover backtracking over black cells (n*m <= 30 assumed)
    cells = {}
    for r in range(n):
        for c in range(m):
            if grid[r][c] != '.':
                cells[(r, c)] = grid[r][c]
    whites = {p for p, v in cells.items() if v == 'w'}
    blacks = [p for p, v in cells.items() if v == 'b']
    if len(whites) != 2 * len(blacks):
        return False
    opt = []
    for (r, c) in blacks:
        o = []
        if (r, c - 1) in whites and (r, c + 1) in whites:
            o.append(('H', (r, c - 1), (r, c + 1)))
        if (r - 1, c) in whites and (r + 1, c) in whites:
            o.append(('V', (r - 1, c), (r + 1, c)))
        opt.append(o)
    covered = set()
    order = sorted(range(len(blacks)), key=lambda i: len(opt[i]))
    def rec(k):
        if k == len(order):
            return len(covered) == len(whites)
        i = order[k]
        for _, a, b in opt[i]:
            if a in covered or b in covered:
                continue
            covered.add(a); covered.add(b)
            if rec(k + 1):
                return True
            covered.discard(a); covered.discard(b)
        return False
    return rec(0)

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    n, m = int(data[0]), int(data[1])
    grid = data[2:2 + n]
    toks = open(outp).read().split()
    if not toks:
        die("empty output")
    verdict = toks[0]
    if verdict.upper() == 'NO':
        if n * m > 64:
            die("NO on large board cannot be verified")
        if brute_possible(grid, n, m):
            die("NO but a tiling exists")
        return
    if verdict.upper() != 'YES':
        die("first token must be YES or NO")
    if len(toks) != 1 + n:
        die("expected %d board lines" % n)
    out = toks[1:]
    for i in range(n):
        if len(out[i]) != m:
            die("row %d length %d != %d" % (i, len(out[i]), m))
        for j in range(m):
            if (grid[i][j] == '.') != (out[i][j] == '.'):
                die("cell (%d,%d): cut mismatch" % (i, j))
            if grid[i][j] != '.' and out[i][j] not in 'abcd':
                die("cell (%d,%d): bad symbol %r" % (i, j, out[i][j]))
    # split same-symbol cells into 4-connected components
    seen = [[False] * m for _ in range(n)]
    bars = []
    for i in range(n):
        for j in range(m):
            if out[i][j] == '.' or seen[i][j]:
                continue
            sym = out[i][j]
            stack = [(i, j)]
            seen[i][j] = True
            comp = []
            while stack:
                r, c = stack.pop()
                comp.append((r, c))
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m and not seen[nr][nc] and out[nr][nc] == sym:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            bars.append((sym, sorted(comp)))
    for sym, comp in bars:
        if len(comp) != 3:
            die("symbol component of size %d (symbol %s)" % (len(comp), sym))
        rs = [p[0] for p in comp]; cs = [p[1] for p in comp]
        if not ((rs[0] == rs[1] == rs[2] and cs[1] == cs[0] + 1 and cs[2] == cs[0] + 2) or
                (cs[0] == cs[1] == cs[2] and rs[1] == rs[0] + 1 and rs[2] == rs[0] + 2)):
            die("component not a straight 3-line: %s" % (comp,))
        for k, (r, c) in enumerate(comp):
            want = 'b' if k == 1 else 'w'
            if grid[r][c] != want:
                die("cell (%d,%d) is %s but bar needs %s" % (r, c, grid[r][c], want))
    print("OK")
if __name__ == "__main__":
    main()
