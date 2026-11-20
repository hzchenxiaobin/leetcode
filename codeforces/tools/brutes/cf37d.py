import random, subprocess, os, itertools
D = os.path.dirname(os.path.abspath(__file__))

def brute(m, x, y):
    n = sum(x)
    best = 0
    for assign in itertools.product(range(m), repeat=2 * n):
        ps = assign[:n]; qs = assign[n:]
        if any(ps[g] > qs[g] for g in range(n)): continue
        a = [0]*m; b = [0]*m
        for g in range(n): a[ps[g]] += 1; b[qs[g]] += 1
        if a != x: continue                     # 第一节课：第 i 间恰有 x_i 组
        if any(b[i] > y[i] for i in range(m)): continue
        best += 1
    return best

random.seed(3737)
cases = []
for _ in range(210):
    m = random.randint(1, 3)
    x = [random.randint(0, 2) for _ in range(m)]
    if sum(x) == 0: x[0] = 1
    if sum(x) > 4: continue
    y = [random.randint(0, 3) for _ in range(m)]
    cases.append((m, x, y))
bad = 0
for (m, x, y) in cases:
    inp = f"{m}\n{' '.join(map(str,x))}\n{' '.join(map(str,y))}\n"
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout.strip()
    p = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout.strip()
    b = brute(m, x, y) % (10**9+7)
    if o != str(b) or p != str(b):
        bad += 1
        print('MISMATCH', inp.replace('\n','|'), 'brute', b, 'cpp', o, 'py', p)
        if bad > 5: break
print('cases', len(cases), 'bad', bad)
