# 校验 CF125E（根结点 1 恰好 k 条边的最小生成树，多解）：
#   1) 输出必须是生成树，且恰好 k 条边与 1 相连；
#   2) 总权必须等于参考答案（官方样例给的树）的总权 → 由此确认最优性；
#   3) 输出 -1 时：n <= 8 且 m <= 20 用全枚举独立确认确实无解，否则拒绝。
import itertools
import sys


def main():
    data = open(sys.argv[1]).read().split()
    p = 0
    n, m, k = int(data[0]), int(data[1]), int(data[2]); p = 3
    eu, ev, ew = [], [], []
    for _ in range(m):
        eu.append(int(data[p])); ev.append(int(data[p + 1])); ew.append(int(data[p + 2])); p += 3
    out = open(sys.argv[2]).read().split()
    ans = open(sys.argv[3]).read().split()

    def cost(ids):                      # ids 为 0 基边号，返回 (是否生成树, 首都边数, 总权)
        par = list(range(n + 1))

        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        reds = 0; w = 0
        for i in ids:
            if not (0 <= i < m):
                return (False, 0, 0)
            a, b = f(eu[i]), f(ev[i])
            if a == b:
                return (False, 0, 0)
            par[a] = b
            w += ew[i]
            if eu[i] == 1 or ev[i] == 1:
                reds += 1
        ok = len(set(f(v) for v in range(1, n + 1))) == 1 and len(set(ids)) == len(ids)
        return (ok, reds, w)

    if len(out) >= 1 and out[0] == '-1':
        if n <= 8 and m <= 20:
            for r in range(m + 1):
                for comb in itertools.combinations(range(m), r):
                    ok, reds, _ = cost(list(comb))
                    if ok and reds == k:
                        print('claimed -1 but a valid set exists:', [i + 1 for i in comb])
                        return 1
            return 0
        print('cannot verify -1 for this size')
        return 1

    cnt = int(out[0])
    ids = [int(x) - 1 for x in out[1:1 + cnt]]
    if len(ids) != cnt:
        print('fewer edge ids than announced')
        return 1
    if cnt != n - 1:
        print('expect %d edges, got %d' % (n - 1, cnt))
        return 1
    ok, reds, w = cost(ids)
    if not ok:
        print('not a spanning tree')
        return 1
    if reds != k:
        print('capital edges %d != k %d' % (reds, k))
        return 1
    # 参考答案的总权（官方样例保证最优）
    ref_cnt = int(ans[0]); ref_ids = [int(x) - 1 for x in ans[1:1 + ref_cnt]]
    rok, rreds, rw = cost(ref_ids)
    if not rok:
        print('reference answer unparsable')
        return 1
    if w != rw:
        print('total weight %d != optimum %d' % (w, rw))
        return 1
    return 0


sys.exit(main())
