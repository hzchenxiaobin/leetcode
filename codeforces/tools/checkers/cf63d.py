import sys
from collections import deque


def main():
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    a, b, c, d, n = (int(v) for v in data[:5])
    x = [int(v) for v in data[5:5 + n]]
    toks = open(outp).read().split('\n')
    if not toks or toks[0].strip() not in ('YES', 'NO'):
        print('WRONG: first line'); sys.exit(1)
    if toks[0].strip() == 'NO':
        print('WRONG: claimed NO'); sys.exit(1)
    H, W = max(b, d), a + c
    rows = [r for r in toks[1:] if r.strip() != '']
    # 保持行原样（含点），去掉可能的行尾空白
    rows = [r.rstrip() for r in rows]
    if len(rows) != H:
        print('WRONG: row count %d != %d' % (len(rows), H)); sys.exit(1)
    for r in rows:
        if len(r) != W:
            print('WRONG: row width', len(r)); sys.exit(1)
    def island(r, col):
        return (r < b and col < a) or (r < d and a <= col < a + c)
    cnt = [0] * n
    for r in range(H):
        for col in range(W):
            ch = rows[r][col]
            if not island(r, col):
                if ch != '.':
                    print('WRONG: sea cell is not dot', r, col); sys.exit(1)
                continue
            if not ('a' <= ch < chr(ord('a') + n)):
                print('WRONG: island cell bad letter', r, col, repr(ch)); sys.exit(1)
            cnt[ord(ch) - 97] += 1
    if cnt != x:
        print('WRONG: sizes', cnt, '!=', x); sys.exit(1)
    # 连通性
    for p in range(n):
        ch = chr(97 + p)
        cells = [(r, col) for r in range(H) for col in range(W)
                 if island(r, col) and rows[r][col] == ch]
        seen = {cells[0]}
        q = deque([cells[0]])
        cellset = set(cells)
        while q:
            r, col = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (r + dr, col + dc)
                if nb in cellset and nb not in seen:
                    seen.add(nb); q.append(nb)
        if len(seen) != len(cells):
            print('WRONG: party %s not connected' % ch); sys.exit(1)
    sys.exit(0)


main()
