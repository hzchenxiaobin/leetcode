"""97A checker（特殊评测：答案不唯一）。

约定：python3 cf97a.py <input> <output> <answer>，返回 0 表示通过；参考答案（样例输出）从 stdin 读入。

校验条件：
1. 第一行是正整数 c，随后恰好 n 行、每行 m 个字符，`'.'` 的位置与输入完全一致，
   其余位置是 `0`-`6` 的数字；
2. 每个 chip（同一字母的两格）构成无序数对，28 个 chip 的数对两两不同
   （因此恰好用完整副 28 张骨牌）；
3. 数字场能被 14 个 2x2 的同色方块恰好覆盖（用"最上最左未覆盖格"的贪心，
   该贪心给出的覆盖若存在则唯一）；
4. c 与 checker 独立重算的答案一致（贪心遮盖 + 纤维匹配枚举），
   若参考答案可读到且首行是整数，还要求 c 与之相等。
"""
import sys
from itertools import permutations


def fail(msg):
    print('CHECKER FAIL:', msg)
    return 1


def count_ways(g, n, m):
    """独立重算：贪心 2x2 遮盖 + 每位数恰两块 + 纤维匹配枚举。"""
    sq = [[-1] * m for _ in range(n)]
    nsq = 0
    for r in range(n):
        for c in range(m):
            if g[r][c] == '.' or sq[r][c] != -1:
                continue
            if r + 1 >= n or c + 1 >= m:
                return 0
            for dr in range(2):
                for dc in range(2):
                    if g[r + dr][c + dc] == '.' or sq[r + dr][c + dc] != -1:
                        return 0
            for dr in range(2):
                for dc in range(2):
                    sq[r + dr][c + dc] = nsq
            nsq += 1
    if nsq != 14:
        return 0
    chips = {}
    for r in range(n):
        for c in range(m):
            if g[r][c] != '.':
                chips.setdefault(g[r][c], []).append((r, c))
    internal = [0] * nsq
    adj = [[0] * nsq for _ in range(nsq)]
    for cells in chips.values():
        (r1, c1), (r2, c2) = cells
        s1, s2 = sq[r1][c1], sq[r2][c2]
        if s1 == s2:
            internal[s1] += 1
        else:
            adj[s1][s2] += 1
            adj[s2][s1] += 1
    anchors = [s for s in range(nsq) if internal[s] == 1]
    frees = [s for s in range(nsq) if internal[s] == 0]
    if len(anchors) != 7 or len(frees) != 7:
        return 0
    valid = 0
    for perm in permutations(frees):
        ok = True
        for k in range(7):
            if adj[anchors[k]][perm[k]]:
                ok = False
                break
        if ok:
            for a in range(7):
                for b in range(a + 1, 7):
                    cnt = (adj[anchors[a]][anchors[b]] + adj[anchors[a]][perm[b]]
                           + adj[perm[a]][anchors[b]] + adj[perm[a]][perm[b]])
                    if cnt != 1:
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            valid += 1
    return valid * 5040


def main():
    inp, outp, ansp = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split('\n')
    n, m = map(int, data[0].split())
    g = data[1:1 + n]
    if len(g) != n or any(len(row) != m for row in g):
        return fail('输入网格解析失败')

    toks = open(outp).read().split()
    if len(toks) != n + 1:
        return fail('输出应为 1 个计数 + n 行网格，实际 token 数 %d' % len(toks))
    try:
        c = int(toks[0])
    except ValueError:
        return fail('第一行不是整数')
    rows = toks[1:]
    for r in range(n):
        if len(rows[r]) != m:
            return fail('第 %d 行长度不是 %d' % (r + 1, m))
        for c2 in range(m):
            ch, ch2 = g[r][c2], rows[r][c2]
            if ch == '.':
                if ch2 != '.':
                    return fail('空格处应为 "."')
            else:
                if ch2 not in '0123456':
                    return fail('chip 处应为数字 0-6')

    chips = {}
    for r in range(n):
        for c2 in range(m):
            if g[r][c2] != '.':
                chips.setdefault(g[r][c2], []).append((r, c2))
    if len(chips) != 28 or any(len(v) != 2 for v in chips.values()):
        return fail('输入里不是 28 个双格 chip')
    pairs = set()
    for cells in chips.values():
        (r1, c1), (r2, c2) = cells
        p = tuple(sorted((rows[r1][c1], rows[r2][c2])))
        if p in pairs:
            return fail('有两张 chip 用了同一张骨牌 %s' % (p,))
        pairs.add(p)
    if len(pairs) != 28:
        return fail('骨牌不是 28 张互不相同')

    # 2x2 同色覆盖（贪心；若存在则唯一）
    sq = [[-1] * m for _ in range(n)]
    nsq = 0
    for r in range(n):
        for c2 in range(m):
            if g[r][c2] == '.' or sq[r][c2] != -1:
                continue
            if r + 1 >= n or c2 + 1 >= m:
                return fail('数字场不能被 2x2 方块覆盖')
            vals = set()
            for dr in range(2):
                for dc in range(2):
                    if g[r + dr][c2 + dc] == '.' or sq[r + dr][c2 + dc] != -1:
                        return fail('数字场不能被 2x2 方块覆盖')
                    vals.add(rows[r + dr][c2 + dc])
            if len(vals) != 1:
                return fail('2x2 方块内数字不全相同')
            for dr in range(2):
                for dc in range(2):
                    sq[r + dr][c2 + dc] = nsq
            nsq += 1

    want = count_ways(g, n, m)
    if c != want:
        return fail('计数错误：输出 %d，正确 %d' % (c, want))
    expected = ''
    try:
        expected = sys.stdin.read()
    except Exception:
        expected = ''
    if not expected.strip() and ansp not in ('/dev/stdin',):
        try:
            expected = open(ansp).read()
        except Exception:
            expected = ''
    etok = expected.split()
    if etok:
        try:
            if int(etok[0]) != c:
                return fail('与参考答案计数不符：%s vs %d' % (etok[0], c))
        except ValueError:
            pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
