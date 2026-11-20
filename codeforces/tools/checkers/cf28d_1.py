import random, subprocess, os, itertools
D = os.path.dirname(os.path.abspath(__file__))

def brute(n, trucks):
    best = 0          # 空集也合法（价值 0）
    for mask in range(1 << n):
        idx = [i for i in range(n) if mask >> i & 1]
        if not idx:
            continue
        pref = 0
        ok = True
        vals = 0
        for i in idx:
            v, c, l, r = trucks[i]
            if l != pref: ok = False; break
            pref += c
            vals += v
        if not ok: continue
        # 校验每辆车的 r：其后再无人时 r 必须为 0
        pref = 0
        for k, i in enumerate(idx):
            v, c, l, r = trucks[i]
            after = sum(trucks[j][1] for j in idx[k+1:])
            if l != pref or r != after: ok = False; break
            pref += c
        if not ok: continue
        if best is None or vals > best: best = vals
    return best

def check_out(n, trucks, out):
    tok = out.split()
    if not tok: return False, None
    k = int(tok[0]); ids = [int(x) for x in tok[1:]]
    if len(ids) != k: return False, None
    if any(ids[i] >= ids[i+1] for i in range(k-1)): return False, None
    pref = 0; val = 0
    for pos, i in enumerate(ids):
        if not (1 <= i <= n): return False, None
        v, c, l, r = trucks[i-1]
        after = sum(trucks[j-1][1] for j in ids[pos+1:])
        if l != pref or r != after: return False, None
        pref += c; val += v
    return True, val

random.seed(28)
cases = [(open(f's{k}.txt').read(), None) for k in (1,2)]
for _ in range(300):
    n = random.randint(1, 8)
    trucks = []
    for _ in range(n):
        c = random.randint(1, 3)
        l = random.randint(0, 5)
        r = random.randint(0, 5)
        v = random.randint(1, 20)
        trucks.append((v, c, l, r))
    inp = f"{n}\n" + ''.join(f"{v} {c} {l} {r}\n" for v,c,l,r in trucks)
    cases.append((inp, trucks))
bad = 0
for inp, trucks in cases:
    if trucks is None: continue
    b = brute(len(trucks), trucks)
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout
    op = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout
    ok, val = check_out(len(trucks), trucks, o)
    if not ok or val != b:
        bad += 1
        print('MISMATCH', inp.replace('\n','|'), 'brute', b, 'cpp', o.split()[:6], 'val', val)
        if bad > 5: break
    if op.split()[0] != o.split()[0]:
        bad += 1; print('C++/Py 车数不同', inp.replace('\n','|'))
print('cases', len(cases), 'bad', bad)
