import random, subprocess, os
D = os.path.dirname(os.path.abspath(__file__))

def brute(n, edges):
    INF = 10**15
    d = [[INF]*(n+1) for _ in range(n+1)]
    for i in range(1, n+1): d[i][i] = 0
    for a,b,w in edges:
        d[a][b] = min(d[a][b], w); d[b][a] = min(d[b][a], w)
    for k in range(1, n+1):
        for i in range(1, n+1):
            if d[i][k] >= INF: continue
            for j in range(1, n+1):
                if d[k][j] < INF and d[i][k]+d[k][j] < d[i][j]: d[i][j] = d[i][k]+d[k][j]
    return [sum(d[i][j] for j in range(1, n+1) if j != i) for i in range(1, n+1)]

random.seed(48)
bad = 0
for it in range(220):
    n = random.randint(3, 9)
    # 随机树
    edges = []
    have = set()
    for v in range(2, n+1):
        u = random.randint(1, v-1)
        w = random.randint(1, 9)
        edges.append((u, v, w)); have.add((min(u,v), max(u,v)))
    # 加一条不重复的边形成单环
    for _ in range(200):
        a = random.randint(1, n); b = random.randint(1, n)
        if a == b: continue
        key = (min(a,b), max(a,b))
        if key in have: continue
        edges.append((a, b, random.randint(1, 9))); break
    inp = f"{n}\n" + ''.join(f"{a} {b} {w}\n" for a,b,w in edges)
    want = brute(n, edges)
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout.split()
    p = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout.split()
    got = [int(x) for x in o]
    if got != want or [int(x) for x in p] != want:
        bad += 1
        if bad <= 5: print('MISMATCH', inp.replace('\n','|'), 'want', want, 'cpp', got, 'py', p)
print('cases 220, bad', bad)
