# 独立暴力：枚举"每个人选哪条申请当上司"（或选作根）的所有组合，
# 要求恰好一个根、每条边 q 严格下降、无环，取最小总花费。
import sys
from itertools import product


def main() -> None:
    data = sys.stdin.read().split()
    k = 0
    n = int(data[k]); k += 1
    q = [0] + [int(x) for x in data[k:k + n]]; k += n
    m = int(data[k]); k += 1
    apps = []
    for _ in range(m):
        a, b, c = int(data[k]), int(data[k + 1]), int(data[k + 2])
        k += 3
        apps.append((a, b, c))

    choices = [[] for _ in range(n + 1)]
    for idx, (a, b, c) in enumerate(apps):
        choices[b].append(idx)

    best = None
    options = [[None] + choices[b] for b in range(1, n + 1)]
    for pick in product(*options):
        if sum(1 for x in pick if x is None) != 1:
            continue
        boss = [0] * (n + 1)
        cost = 0
        ok = True
        for b in range(1, n + 1):
            idx = pick[b - 1]
            if idx is None:
                continue
            a, bb, c = apps[idx]
            if q[a] <= q[bb]:
                ok = False
                break
            boss[b] = a
            cost += c
        if not ok:
            continue
        for b in range(1, n + 1):          # 沿上司链走到根，检测环
            seen = set()
            x = b
            while boss[x] != 0:
                if x in seen:
                    ok = False
                    break
                seen.add(x)
                x = boss[x]
            if not ok:
                break
        if ok and (best is None or cost < best):
            best = cost

    print(best if best is not None else -1)


main()
