import random, subprocess, os, itertools, sys
D = os.path.dirname(os.path.abspath(__file__))

def gen_poly(rng, n):
    # 交替水平/垂直位移，分别求和为 0
    while True:
        hs = [rng.choice([-3,-2,-1,1,2,3]) for _ in range(n//2 - 1)]
        last = -sum(hs)
        if last == 0 or abs(last) > 6: continue
        hs.append(last)
        vs = [rng.choice([-3,-2,-1,1,2,3]) for _ in range(n//2 - 1)]
        lastv = -sum(vs)
        if lastv == 0 or abs(lastv) > 6: continue
        vs.append(lastv)
        pts = [(0,0)]
        x = y = 0
        for k in range(n//2):
            x += hs[k]; pts.append((x,y))
            y += vs[k]; pts.append((x,y))
        pts.pop()
        return pts[:n]

def brute(pts, rods):
    n = len(pts)
    need = []
    for i in range(n):
        pre, nxt = (i-1) % n, (i+1) % n
        need.append(abs(pts[i][0]-pts[pre][0])+abs(pts[i][1]-pts[pre][1])
                    + abs(pts[nxt][0]-pts[i][0])+abs(pts[nxt][1]-pts[i][1]))
    best = None
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        ok = True
        for i in S:
            for j in S:
                if i != j and (abs(i-j) % n in (1, n-1)): ok = False
        if not ok: continue
        # 覆盖所有线段
        for i in range(n):
            if not ((mask >> i & 1) or (mask >> ((i+1) % n) & 1)): ok = False
        if not ok: continue
        # 杆的多重集匹配
        want = sorted(need[i] for i in S)
        have = sorted(rods)
        if len(want) > len(have): continue
        used = [False]*len(have)
        good = True
        for L in want:
            hit = -1
            for j, R in enumerate(have):
                if not used[j] and R == L: hit = j; break
            if hit < 0: good = False; break
            used[hit] = True
        if not good: continue
        return True, need
    return False, need

def check_out(pts, rods, out, need):
    tok = out.split()
    if not tok: return False
    if tok[0] == 'NO': return len(tok) == 1
    if tok[0] != 'YES' or len(tok) != 1 + len(pts): return False
    used = set(); S = []
    for i in range(len(pts)):
        x = int(tok[1+i])
        if x == -1: continue
        if not (1 <= x <= len(rods)): return False
        if rods[x-1] != need[i]: return False
        if x in used: return False
        used.add(x); S.append(i)
    for i in S:
        for j in S:
            if i != j and (abs(i-j) % len(pts) in (1, len(pts)-1)): return False
    for i in range(len(pts)):
        if i not in S and ((i+1) % len(pts)) not in S: return False
    return True

random.seed(20260328)
cases = [(open(f's{k}.txt').read(), None) for k in (1,2,3)]
for _ in range(260):
    n = random.choice([4,6,8,10])
    pts = gen_poly(random, n)
    # 一半数据构造出“能匹配”的杆，一半完全随机
    if random.random() < 0.5:
        need = []
        for i in range(n):
            pre, nxt = (i-1)%n, (i+1)%n
            need.append(abs(pts[i][0]-pts[pre][0])+abs(pts[i][1]-pts[pre][1])
                        + abs(pts[nxt][0]-pts[i][0])+abs(pts[nxt][1]-pts[i][1]))
        par = random.choice([0,1])
        rods = [need[i] for i in range(par, n, 2)]
        rods += [random.randint(1,12) for _ in range(random.randint(0,2))]
        random.shuffle(rods)
    else:
        rods = [random.randint(1,12) for _ in range(random.randint(2,6))]
    cases.append((f"{n} {len(rods)}\n" + ''.join(f"{x} {y}\n" for x,y in pts) + ' '.join(map(str,rods)) + '\n', (pts, rods)))

bad = 0
for inp, meta in cases:
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout
    op = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout
    if meta is None:
        # 官方样例：只比对 YES/NO 与各自合法
        if o.split()[0] != op.split()[0]: bad += 1; print('sample parity mismatch')
        continue
    pts, rods = meta
    ok, need = brute(pts, rods)
    yes = bool(o.split()) and o.split()[0] == 'YES'
    if yes != ok or not check_out(pts, rods, o, need) or op.split()[0] != o.split()[0]:
        bad += 1
        print('MISMATCH', inp.replace('\n','|'), 'brute', ok, 'cpp', o.split()[:2], 'py', op.split()[:2])
        if bad > 5: break
print('cases', len(cases), 'bad', bad)
