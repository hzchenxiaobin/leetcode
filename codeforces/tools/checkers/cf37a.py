import random, subprocess, os
D = os.path.dirname(os.path.abspath(__file__))

def brute(lengths):
    # 独立做法：排序后做“行程长度编码”——每种长度是一摞塔，塔高 = 该长度的个数
    a = sorted(lengths)
    towers = 0; mx = 0; i = 0
    while i < len(a):
        j = i
        while j < len(a) and a[j] == a[i]:
            j += 1
        towers += 1
        mx = max(mx, j - i)
        i = j
    return mx, towers
random.seed(37)
cases = [open(f's{k}.txt').read() for k in (1,2)]
for _ in range(260):
    n = random.randint(1, 12)
    vmax = random.choice([2,3,5,10,999])
    ls = [random.randint(1, vmax) for _ in range(n)]
    cases.append(f"{n}\n{' '.join(map(str,ls))}\n")
bad = 0
for inp in cases:
    n = int(inp.split()[0]); ls = [int(x) for x in inp.split()[1:1+n]]
    mx, tw = brute(ls)
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout.split()
    p = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout.split()
    if o != [str(mx), str(tw)] or p != o:
        bad += 1
        if bad <= 5: print('MISMATCH', inp.replace('\n','|'), 'brute', mx, tw, 'cpp', o, 'py', p)
print('cases', len(cases), 'bad', bad)
