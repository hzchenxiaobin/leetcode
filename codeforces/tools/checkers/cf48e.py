import random, subprocess, os
from collections import deque
D = os.path.dirname(os.path.abspath(__file__))

def solve_brute(H, T, R, hg, tg):
    n = len(hg) - 1; m = len(tg) - 1
    def moves(h, t):
        out = []
        for i in range(1, min(n, h) + 1):
            nh, nt = h - i + hg[i][0], t + hg[i][1]
            if nh >= 0 and nt >= 0 and nh + nt <= R: out.append((nh, nt))
        for i in range(1, min(m, t) + 1):
            nh, nt = h + tg[i][0], t - i + tg[i][1]
            if nh >= 0 and nt >= 0 and nh + nt <= R: out.append((nh, nt))
        return out
    # 可达
    reach = {(H, T)}
    dq = deque([(H, T)])
    while dq:
        s = dq.popleft()
        for nx in moves(*s):
            if nx not in reach:
                reach.add(nx); dq.append(nx)
    # 到 (0,0) 最短
    if (0, 0) in reach:
        dist = {(H, T): 0}
        q = deque([(H, T)])
        while q:
            s = q.popleft()
            if s == (0, 0): return ('Ivan', dist[s])
            for nx in moves(*s):
                if nx in reach and nx not in dist:
                    dist[nx] = dist[s] + 1; q.append(nx)
    # 环：某可达状态能回到自己（长度 >= 1）
    adj = {s: moves(*s) for s in reach}
    has_cycle = False
    for s in reach:
        seen = set()
        st = list(adj[s])
        while st:
            v = st.pop()
            if v == s: has_cycle = True; break
            if v in seen: continue
            seen.add(v); st.extend(adj[v])
        if has_cycle: break
    if has_cycle: return ('Draw', None)
    memo = {}
    def longest(s):
        if s in memo: return memo[s]
        best = 0
        for nx in adj[s]:
            best = max(best, 1 + longest(nx))
        memo[s] = best
        return best
    return ('Zmey', longest((H, T)) + 1)

random.seed(48)
cases = [('2 2 4\n2\n1 0\n0 1\n3\n0 1\n0 1\n0 0\n', None),
         ('2 2 4\n1\n0 1\n1\n1 0\n', None),
         ('2 2 5\n1\n1 1\n1\n3 0\n', None)]
for _ in range(220):
    H = random.randint(0, 4); T = random.randint(0, 4)
    if H + T == 0: H = 1
    R = random.randint(H + T, H + T + 5)
    n = random.randint(1, 3); m = random.randint(1, 3)
    hg = [(0, 0)] + [(random.randint(0, 3), random.randint(0, 3)) for _ in range(n)]
    tg = [(0, 0)] + [(random.randint(0, 3), random.randint(0, 3)) for _ in range(m)]
    inp = f"{H} {T} {R}\n{n}\n" + ''.join(f"{a} {b}\n" for a, b in hg[1:]) + f"{m}\n" + ''.join(f"{a} {b}\n" for a, b in tg[1:])
    cases.append((inp, (H, T, R, hg, tg)))
bad = 0
for inp, meta in cases:
    o = subprocess.run([os.path.join(D, 'main')], input=inp, capture_output=True, text=True).stdout.split()
    p = subprocess.run(['python3', os.path.join(D, 'main.py')], input=inp, capture_output=True, text=True).stdout.split()
    if meta is None: continue
    H, T, R, hg, tg = meta
    want = solve_brute(H, T, R, hg, tg)
    got = (o[0], int(o[1]) if len(o) > 1 else None)
    if got != want or (p[0], int(p[1]) if len(p) > 1 else None) != want:
        bad += 1
        if bad <= 5: print('MISMATCH', inp.replace('\n', '|'), 'brute', want, 'cpp', o, 'py', p)
print('cases', len(cases), 'bad', bad)
