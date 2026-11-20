import random, subprocess, os
from fractions import Fraction
D=os.path.dirname(os.path.abspath(__file__))

def sim(alpha, cnt):
    fuel = alpha; stops = []
    k = 0
    while len(stops) < cnt:
        k += 1
        fuel -= 10
        if fuel < 10:
            stops.append(k)
            fuel += alpha
        if k > 10**7: break
    return stops

def brute_next(stops):
    n = len(stops)
    cands = set()
    step = Fraction(1, 3)
    a = Fraction(10)
    while a < Fraction(600):
        if sim(a, n) == stops:
            full = sim(a, n + 1)
            cands.add(full[n] if len(full) > n else None)
        a += step
    return cands

random.seed(48)
cases = []
for _ in range(60):
    q = random.randint(1, 20)
    r = random.randint(0, 39)
    alpha = Fraction(10 * q) + Fraction(r, 4)
    if alpha < 10: continue
    n = random.randint(1, 4)
    stops = sim(alpha, n)
    if not stops or stops[-1] > 10**6: continue
    cases.append(stops)
bad = 0
for stops in cases:
    inp = f"{len(stops)}\n{' '.join(map(str,stops))}\n"
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout.split()
    cands = brute_next(stops)
    want_unique = len(cands) == 1
    got_unique = o[0] == 'unique'
    ok = got_unique == want_unique and (not got_unique or int(o[1]) in cands)
    if not ok:
        bad += 1
        if bad <= 5: print('MISMATCH', inp.replace('\n','|'), 'grid cands', sorted(x for x in cands if x is not None)[:5], 'cpp', o)
print('cases', len(cases), 'bad', bad)
