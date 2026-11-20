import random, subprocess, os
D = os.path.dirname(os.path.abspath(__file__))

def kraft_ok(lengths):
    # Kraft-McMillan：无前缀码存在 ⟺ Σ 2^{-l_i} <= 1（用整数精确比较）
    mx = max(lengths)
    s = sum(1 << (mx - l) for l in lengths)
    return s <= (1 << mx)

def check_words(lengths, out):
    tok = out.split()
    if not tok: return False, 'empty'
    if tok[0] == 'NO': return (not kraft_ok(lengths)), None
    if tok[0] != 'YES': return False, 'bad header'
    if len(tok) != 1 + len(lengths): return False, 'bad count'
    words = tok[1:]
    for w, l in zip(words, lengths):
        if len(w) != l or any(ch not in '01' for ch in w): return False, 'bad word'
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j and words[j].startswith(words[i]): return False, 'prefix!'
    return True, None

random.seed(373)
cases = [open(f's{k}.txt').read() for k in (1,2)]
for _ in range(240):
    n = random.randint(1, 7)
    ls = [random.randint(1, 6) for _ in range(n)]
    cases.append(f"{n}\n{' '.join(map(str,ls))}\n")
bad = 0
for inp in cases:
    n = int(inp.split()[0]); ls = [int(x) for x in inp.split()[1:1+n]]
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout
    p = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout
    ok, err = check_words(ls, o)
    ok2, err2 = check_words(ls, p)
    want = kraft_ok(ls)
    got = o.split()[0] == 'YES'
    if not ok or not ok2 or got != want:
        bad += 1
        if bad <= 5: print('MISMATCH', inp.replace('\n','|'), 'kraft', want, 'cpp', o.split()[:3], err, err2)
print('cases', len(cases), 'bad', bad)
