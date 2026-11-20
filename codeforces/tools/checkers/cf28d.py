# CF28D 特殊评测：合法性 + 最优性（用独立实现的最大价值 DP 复核）
import sys
from collections import defaultdict

data = open(sys.argv[1]).read().split()
p = 0
n = int(data[p]); p += 1
trucks = []
for _ in range(n):
    v, c, l, r = (int(data[p]), int(data[p+1]), int(data[p+2]), int(data[p+3]))
    p += 4
    trucks.append((v, c, l, r))

# 独立求最大总价值
best = 0
state = {}   # (K, p) -> 最大价值
for (v, c, l, r) in trucks:
    K = l + c + r
    if l == 0:
        cand = v
    else:
        cand = state.get((K, l), None)
        if cand is None:
            continue
        cand += v
    key = (K, l + c)
    if state.get(key, -1) < cand:
        state[key] = cand
        if l + c == K:
            best = max(best, cand)

out = open(sys.argv[2]).read().split()
if not out:
    print('empty output'); sys.exit(1)
try:
    k = int(out[0]); ids = [int(x) for x in out[1:]]
except ValueError:
    print('bad numbers'); sys.exit(1)
if len(ids) != k:
    print('k mismatch'); sys.exit(1)
if any(ids[i] >= ids[i+1] for i in range(k-1)):
    print('ids not increasing'); sys.exit(1)
val = 0; pref = 0
for pos, i in enumerate(ids):
    if not (1 <= i <= n):
        print('id out of range'); sys.exit(1)
    v, c, l, r = trucks[i-1]
    after = sum(trucks[j-1][1] for j in ids[pos+1:])
    if l != pref or r != after:
        print('constraint violated at truck %d' % i); sys.exit(1)
    pref += c; val += v
if val != best:
    print('not optimal: %d vs %d' % (val, best)); sys.exit(1)
sys.exit(0)
