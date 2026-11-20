import random, subprocess, os, sys
from collections import deque
D = os.path.dirname(os.path.abspath(__file__))

def brute(n, mx, reg, pw, dg):
    start = (mx, 0)
    seen = {start}
    layer = [start]
    t = 0
    while layer:
        nxt = []
        for hp, mask in layer:
            total = sum(dg[i] for i in range(n) if mask >> i & 1)
            hp2 = hp - total + reg
            if hp2 > mx: hp2 = mx
            if hp2 <= 0:
                return t
            # 选项：跳过 / 用一个可用卷轴
            cand = [(hp2, mask)]
            for i in range(n):
                if mask >> i & 1: continue
                if hp2 * 100 <= pw[i] * mx:
                    cand.append((hp2, mask | (1 << i)))
            for st in cand:
                if st not in seen:
                    seen.add(st); nxt.append(st)
        layer = nxt
        t += 1
        if t > 4000: return None
    return None

def check_out(n, mx, reg, pw, dg, out):
    tok = out.split()
    if not tok: return None, 'empty'
    if tok[0] == 'NO': return None, None
    T = int(tok[1]); K = int(tok[2])
    if len(tok) != 3 + 2 * K: return None, 'bad K'
    used = set(); total = 0; hp = mx; ev = []
    for k in range(K):
        tt = int(tok[3 + 2*k]); a = int(tok[4 + 2*k]) - 1
        if not (0 <= a < n): return None, 'bad scroll id'
        if a in used: return None, 'scroll reused'
        if not (0 <= tt < T): return None, 'time out of range'
        if k and tt < int(tok[1 + 2*k]): return None, 'times not sorted'
        ev.append((tt, a))
    # 模拟
    hp = mx; total = 0; ei = 0; used = set()
    for t in range(T + 1):
        hp -= total
        hp += reg
        if hp > mx: hp = mx
        if hp <= 0:
            return (t if t == T else None), ('win at %d != T %d' % (t, T) if t != T else None)
        while ei < K and ev[ei][0] == t:
            a = ev[ei][1]
            if hp * 100 > pw[a] * mx: return None, 'used while not allowed'
            used.add(a); total += dg[a]; ei += 1
        if ei < K and ev[ei][0] < t: return None, 'missed event'
    return None, 'no win within T'

random.seed(37)
cases = []
for _ in range(220):
    n = random.randint(1, 4)
    mx = random.randint(1, 25)
    reg = random.randint(1, 6)
    pw = [random.randint(1, 100) for _ in range(n)]
    dg = [random.randint(1, 12) for _ in range(n)]
    cases.append((n, mx, reg, pw, dg))
bad = 0
for (n, mx, reg, pw, dg) in cases:
    inp = f"{n} {mx} {reg}\n" + ''.join(f"{pw[i]} {dg[i]}\n" for i in range(n))
    out = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout
    outp = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout
    b = brute(n, mx, reg, pw, dg)
    winT, err = check_out(n, mx, reg, pw, dg, out)
    claimed = None if out.split()[0] == 'NO' else int(out.split()[1])
    if err is not None:
        bad += 1; print('INVALID OUT', err, inp.replace('\n','|'), out.replace('\n','|'))
    elif b is None and claimed is not None:
        bad += 1; print('brute NO but prog claims', claimed, inp.replace('\n','|'))
    elif b is not None and claimed != b:
        bad += 1; print('time mismatch brute', b, 'prog', claimed, inp.replace('\n','|'))
    if outp.split()[0] != out.split()[0]:
        bad += 1; print('py/cpp differ', inp.replace('\n','|'))
print('cases', len(cases), 'bad', bad)
