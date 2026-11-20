"""65E checker：读输入 + 选手输出，模拟并校验全部约束。返回 0 = 通过。

校验项：
 1. 首行 YES / NO；NO 时通过（YES/NO 的正确性由与暴力对拍保证）。
 2. 接下来的数字流必须构成 [走法] (楼梯移动 走法)* 且移动次数与第二行一致、<= m。
 3. 每条走法列表内部相邻楼层在当时必须由一条楼梯直连，相邻不能是同一楼层。
 4. 每个楼梯最多移动一次；新位置必须保留原来某一端、另一端换成任意不等于这两个端点的楼层。
 5. 第一个走法必须以 1 号楼层开头；所有 n 层楼至少被访问一次；总元素数 <= 1e6。
 6. 附加（仅提示，不判错）：官方样例的走法列表允许不从哈利当前位置开始，
    这里额外统计"是否严格连续"，用于确认我们自己的方案物理可行。
"""
import sys

def fail(msg):
    print("checker:", msg)
    return 1

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    p = 0
    n = int(data[p]); p += 1
    m = int(data[p]); p += 1
    ea = [0]*m; eb = [0]*m
    for i in range(m):
        ea[i] = int(data[p]) - 1; eb[i] = int(data[p+1]) - 1; p += 2
    toks = open(outp).read().split()
    q = 0
    def nxt():
        nonlocal q
        if q >= len(toks):
            raise SystemExit("checker: 输出提前结束")
        t = toks[q]; q += 1
        return t
    first = nxt()
    if first == 'NO':
        if q != len(toks):
            return fail("NO 后面还有多余输出")
        return 0
    if first != 'YES':
        return fail("首行不是 YES/NO")
    try:
        M = int(nxt())
    except ValueError:
        return fail("第二行不是整数")
    if M < 0 or M > m:
        return fail("移动次数越界")
    walks, moves = [], []
    try:
        for i in range(M + 1):
            k = int(nxt())
            if k < 0:
                return fail("走法长度非法")
            w = [int(nxt()) - 1 for _ in range(k)]
            walks.append(w)
            if i < M:
                e = int(nxt()) - 1; u = int(nxt()) - 1; v = int(nxt()) - 1
                moves.append((e, u, v))
    except SystemExit as ex:
        raise
    if q != len(toks):
        return fail("输出尾部有多余内容")
    total = sum(len(w) for w in walks)
    if total > 10**6:
        return fail("总元素数超过 1e6: %d" % total)
    if not walks[0] or walks[0][0] != 0:
        return fail("第一个走法没有从 1 号楼层开始")

    used = [False]*m
    adjcnt = [dict() for _ in range(n)]
    def add_edge(v, w):
        adjcnt[v][w] = adjcnt[v].get(w, 0) + 1
        adjcnt[w][v] = adjcnt[w].get(v, 0) + 1
    def del_edge(v, w):
        adjcnt[v][w] -= 1
        if adjcnt[v][w] == 0: del adjcnt[v][w]
        adjcnt[w][v] -= 1
        if adjcnt[w][v] == 0: del adjcnt[w][v]
    for i in range(m):
        add_edge(ea[i], eb[i])

    visited = [False]*n
    pos = 0
    strict_ok = True
    for i in range(M + 1):
        w = walks[i]
        if not w:
            if i == 0:
                return fail("第一个走法不能为空")
            continue
        if i > 0 and w[0] != pos:
            strict_ok = False
        visited[w[0]] = True
        pos = w[0]
        for j in range(1, len(w)):
            if w[j] == w[j-1]:
                return fail("相邻两次访问了同一楼层")
            if adjcnt[w[j-1]].get(w[j], 0) == 0:
                return fail("时刻 %d 的走法不连通: %d->%d" % (i, w[j-1]+1, w[j]+1))
            pos = w[j]; visited[pos] = True
        if i < M:
            e, u, v = moves[i]
            if not (0 <= e < m and 0 <= u < n and 0 <= v < n):
                return fail("移动参数越界")
            if used[e]:
                return fail("楼梯 %d 被移动了两次" % (e+1))
            a, b = ea[e], eb[e]
            if u == v:
                return fail("楼梯变成自环")
            keep = None
            if u == a or u == b: keep, other = u, v
            elif v == a or v == b: keep, other = v, u
            else:
                return fail("新位置没有保留原来的任何一端")
            if other == a or other == b:
                return fail("新位置与原位置完全相同(没换端点)")
            del_edge(a, b)
            ea[e], eb[e] = keep, other
            add_edge(keep, other)
            used[e] = True
            pos = keep
    if not all(visited):
        miss = [i+1 for i in range(n) if not visited[i]]
        return fail("有楼层没被访问: %s" % miss[:10])
    if not strict_ok:
        print("checker 提示: 走法不是严格从当前位置开始（题目允许）")
    return 0

sys.exit(main())
