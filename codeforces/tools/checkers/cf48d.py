# CF48D 特殊评测：输出若为 -1 需与独立搜索一致；否则校验每个编号组恰是 {1..size}
import sys
from collections import Counter, defaultdict

data = open(sys.argv[1]).read().split()
n = int(data[0]); arr = [int(x) for x in data[1:1 + n]]

def feasible():
    mx = max(arr)
    start = tuple(Counter(arr).get(v, 0) for v in range(1, mx + 1))
    seen = set()
    def rec(state):
        if all(c == 0 for c in state):
            return True
        if state in seen:
            return False
        seen.add(state)
        k = next((v for v in range(1, mx + 1) if state[v - 1] > 0), mx)
        for L in range(k, mx + 1):
            if any(state[v - 1] == 0 for v in range(1, L + 1)):
                break
            ns = list(state)
            for v in range(1, L + 1):
                ns[v - 1] -= 1
            if rec(tuple(ns)):
                return True
        return False
    return rec(start)

out = open(sys.argv[2]).read().split()
if not out:
    print('empty'); sys.exit(1)
if out[0] == '-1':
    if feasible():
        print('said -1 but solution exists'); sys.exit(1)
    sys.exit(0)
if not feasible():
    print('solution exists? no'); sys.exit(1)
try:
    K = int(out[0]); lab = [int(x) for x in out[1:]]
except ValueError:
    print('bad numbers'); sys.exit(1)
if len(lab) != n:
    print('label count mismatch'); sys.exit(1)
if any(not (1 <= x <= K) for x in lab):
    print('label out of range'); sys.exit(1)
groups = defaultdict(list)
for v, l in zip(arr, lab):
    groups[l].append(v)
if len(groups) != K:
    print('not all labels used: %d vs %d' % (len(groups), K)); sys.exit(1)
for l, vs in groups.items():
    if sorted(vs) != list(range(1, len(vs) + 1)):
        print('group %d is not a permutation of 1..%d' % (l, len(vs))); sys.exit(1)
sys.exit(0)
