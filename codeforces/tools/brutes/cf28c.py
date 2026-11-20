import random, subprocess, os, itertools, math
D = os.path.dirname(os.path.abspath(__file__))

def brute_exact(n, m, a):
    tot = 0.0
    cnt = 0
    for assign in itertools.product(range(m), repeat=n):
        k = [0]*m
        for room in assign: k[room] += 1
        mx = max((k[i] + a[i] - 1)//a[i] for i in range(m))
        tot += mx; cnt += 1
    return tot / cnt

def monte(n, m, a, trials=200000):
    import random as rnd
    s = 0
    for _ in range(trials):
        k = [0]*m
        for _ in range(n):
            k[rnd.randrange(m)] += 1
        s += max((k[i] + a[i] - 1)//a[i] for i in range(m))
    return s / trials

random.seed(28)
cases = [(open(f's{k}.txt').read(), None) for k in (1,2,3,4)]
small = []
for _ in range(120):
    n = random.randint(1, 5); m = random.randint(1, 4)
    a = [random.randint(1, 4) for _ in range(m)]
    inp = f"{n} {m}\n{' '.join(map(str,a))}\n"
    small.append((inp, brute_exact(n, m, a)))
    cases.append((inp, None))
medium = []
for _ in range(20):
    n = random.randint(6, 10); m = random.randint(1, 5)
    a = [random.randint(1, 6) for _ in range(m)]
    inp = f"{n} {m}\n{' '.join(map(str,a))}\n"
    medium.append((inp, monte(n, m, a, 40000)))
bad = 0
for inp, exact in small:
    o = float(subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout)
    op = float(subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout)
    if exact is not None and (abs(o-exact) > 1e-9 or abs(op-exact) > 1e-9):
        bad += 1; print('EXACT MISMATCH', inp.replace('\n','|'), 'exact', exact, 'cpp', o, 'py', op)
for inp, mc in medium:
    o = float(subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout)
    if abs(o - mc) > 5e-3:
        bad += 1; print('MC MISMATCH', inp.replace('\n','|'), 'mc', mc, 'cpp', o)
print('exact cases', len(small), 'mc cases', len(medium), 'bad', bad)
