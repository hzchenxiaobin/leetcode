import random, subprocess, os
D=os.path.dirname(os.path.abspath(__file__))
def brute(n,m,a,A,B):
    best=None
    for (h,w) in ((A,B),(B,A)):
        if h>n or w>m: continue
        for i in range(n-h+1):
            for j in range(m-w+1):
                s=sum(a[i+di][j+dj] for di in range(h) for dj in range(w))
                best=s if best is None else min(best,s)
    return best
random.seed(48)
cases=[open(f's{k}.txt').read() for k in (1,2)]
for _ in range(240):
    n=random.randint(1,7); m=random.randint(1,7)
    a=[[random.randint(0,1) for _ in range(m)] for _ in range(n)]
    while True:
        A=random.randint(1,7); B=random.randint(1,7)
        if (A<=n and B<=m) or (A<=m and B<=n): break
    inp=f'{n} {m}\n'+''.join(' '.join(map(str,r))+'\n' for r in a)+f'{A} {B}\n'
    cases.append(inp)
bad=0
for inp in cases:
    tok=inp.split(); p=0
    n=int(tok[p]); m=int(tok[p+1]); p+=2
    a=[[int(tok[p+i*m+j]) for j in range(m)] for i in range(n)]; p+=n*m
    A=int(tok[p]); B=int(tok[p+1])
    w=brute(n,m,a,A,B)
    o=subprocess.run([os.path.join(D,'main')],input=inp,capture_output=True,text=True).stdout.strip()
    q=subprocess.run(['python3',os.path.join(D,'main.py')],input=inp,capture_output=True,text=True).stdout.strip()
    if o!=str(w) or q!=str(w):
        bad+=1
        if bad<=5: print('MISMATCH',inp.replace('\n','|'),'want',w,'cpp',o,'py',q)
print('cases',len(cases),'bad',bad)
