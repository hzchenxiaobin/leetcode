import random, subprocess, os, itertools
from collections import deque
D = os.path.dirname(os.path.abspath(__file__))

def reachable(n, d):
    start = tuple(range(1, n+1))
    seen = {start}
    q = deque([start])
    while q:
        cur = q.popleft()
        for i in range(n):
            for j in (i + d[i], i - d[i]):
                if 0 <= j < n:
                    nxt = list(cur); nxt[i], nxt[j] = nxt[j], nxt[i]
                    t = tuple(nxt)
                    if t not in seen: seen.add(t); q.append(t)
    return seen

random.seed(28)
cases = [open(f's{k}.txt').read() for k in (1,2,3)]
for _ in range(300):
    n = random.randint(1, 7)
    perm = list(range(1, n+1)); random.shuffle(perm)
    d = [random.randint(1, n) for _ in range(n)]
    cases.append(f"{n}\n{' '.join(map(str,perm))}\n{' '.join(map(str,d))}\n")
bad = 0
for inp in cases:
    n = int(inp.split()[0])
    perm = tuple(int(x) for x in inp.split()[1:1+n])
    d = [int(x) for x in inp.split()[1+n:1+2*n]]
    ok = perm in reachable(n, d)
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout.strip()
    op = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout.strip()
    want = 'YES' if ok else 'NO'
    if o != want or op != want:
        bad += 1
        print('MISMATCH', inp.replace('\n','|'), 'want', want, 'cpp', o, 'py', op)
        if bad > 5: break
print('cases', len(cases), 'bad', bad)
