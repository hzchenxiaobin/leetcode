import random, subprocess, os
from collections import Counter
D=os.path.dirname(os.path.abspath(__file__))

def feasible_brute(arr):
    """回溯：反复取出一个“1..k 恰各一次”的集合"""
    from functools import lru_cache
    vals = sorted(arr)
    n = len(vals)
    # 状态：剩余多重集（用计数向量表示）
    mx = max(vals)
    start = tuple(Counter(vals).get(v, 0) for v in range(1, mx+1))
    seen = set()
    def rec(state):
        if all(c == 0 for c in state): return True
        if state in seen: return False
        seen.add(state)
        # 必须用 1..k 中所有存在的值各一次，k 由“最小非零下标”决定
        k = 0
        # 找到最小的 v 使 state[v-1] > 0 -> 必须以 v 为长度起点？说明该排列长度 >= v
        for v in range(1, mx+1):
            if state[v-1] > 0: k = v; break
        # 尝试长度 L in [k, mx]，要求 state[v-1] > 0 for all v<=L
        for L in range(k, mx+1):
            if any(state[v-1] == 0 for v in range(1, L+1)): break
            ns = list(state)
            for v in range(1, L+1): ns[v-1] -= 1
            if rec(tuple(ns)): return True
        return False
    ok = rec(start)
    return ok

def check_out(arr, out, mx):
    tok = out.split()
    if not tok: return False, 'empty'
    if tok[0] == '-1': return True, None
    K = int(tok[0]); lab = [int(x) for x in tok[1:]]
    if len(lab) != len(arr): return False, 'bad len'
    if any(not (1 <= x <= K) for x in lab): return False, 'label range'
    # 每个 label 的集合必须是 {1..L}
    groups = {}
    for v, l in zip(arr, lab): groups.setdefault(l, []).append(v)
    for l, vs in groups.items():
        if sorted(vs) != list(range(1, len(vs)+1)): return False, 'not a permutation prefix'
    return True, K

random.seed(481)
cases = [open(f's{k}.txt').read() for k in (1,2,3)]
for _ in range(240):
    n = random.randint(1, 8)
    mx = random.randint(1, 4)
    arr = [random.randint(1, mx) for _ in range(n)]
    if 1 not in arr and max(arr) > 1: continue
    cases.append(f"{n}\n{' '.join(map(str,arr))}\n")
bad = 0
for inp in cases:
    tok = inp.split(); n = int(tok[0]); arr = [int(x) for x in tok[1:1+n]]
    o = subprocess.run([os.path.join(D,'main')], input=inp, capture_output=True, text=True).stdout
    p = subprocess.run(['python3', os.path.join(D,'main.py')], input=inp, capture_output=True, text=True).stdout
    want = feasible_brute(arr)
    got = o.split()[0] != '-1'
    ok1, _ = check_out(arr, o, max(arr))
    ok2, _ = check_out(arr, p, max(arr))
    if got != want or not ok1 or not ok2:
        bad += 1
        if bad <= 5: print('MISMATCH', inp.replace('\n','|'), 'brute', want, 'cpp yes?', got, 'valid1', ok1, 'valid2', ok2)
print('cases', len(cases), 'bad', bad)
