import sys, itertools

def main():
    data = open(sys.argv[1]).read().split()
    raw = open(sys.argv[2]).read()
    p = 0
    n = int(data[p]); p += 1
    names = data[p:p+n]; p += n
    sur = data[p:p+n]; p += n

    if raw.endswith('\n'):
        raw = raw[:-1]
    if raw != raw.strip():
        print("行首/行尾有多余空白"); return 1
    if raw.endswith(',') or raw.endswith(' '):
        print("行末不能有逗号或空格"); return 1
    parts = raw.split(', ')
    if len(parts) != n:
        print("配对数不对", len(parts), n); return 1
    used_names, used_sur = [], []
    for part in parts:
        t = part.split(' ')
        if len(t) != 2 or not t[0] or not t[1]:
            print("格式错误:", repr(part)); return 1
        used_names.append(t[0]); used_sur.append(t[1])
    if sorted(used_names) != sorted(names):
        print("名字没有恰好用完"); return 1
    if sorted(used_sur) != sorted(sur):
        print("附名没有恰好用完"); return 1

    M = 0
    for c in set(x[0] for x in names):
        M += min(sum(1 for x in names if x[0] == c), sum(1 for x in sur if x[0] == c))
    same = sum(1 for a, b in zip(used_names, used_sur) if a[0] == b[0])
    if same != M:
        print("同首字母对数不是最优:", same, M); return 1

    if n <= 8:
        order = sorted(names)
        best = None
        for perm in itertools.permutations(sur):
            line = ', '.join(order[i] + ' ' + perm[i] for i in range(n))
            s2 = sum(1 for i in range(n) if order[i][0] == perm[i][0])
            key = (-s2, line)
            if best is None or key < best:
                best = key
        if raw != best[1]:
            print("不是字典序最小:\n got:", raw, "\n exp:", best[1]); return 1
    else:
        # n>8：不重算答案，直接验证"逐位最小性证书"：
        # 设输出第 i 位为 (name_i, s_i)，前缀固定的同字母对数 fixed，
        # 则必须 fixed + gain(s_i) + remMax(去掉前缀) == M，且任何比 s_i 小的未用附名都做不到这一点。
        order = sorted(names)
        if used_names != order:
            print("配对没有按名字升序排列"); return 1
        rn = [0] * 26
        rs = [0] * 26
        for s in names: rn[ord(s[0]) - 65] += 1
        for s in sur: rs[ord(s[0]) - 65] += 1
        Mv = sum(min(rn[c], rs[c]) for c in range(26))
        used = set()
        fixed = 0
        for i in range(n):
            cn = ord(order[i][0]) - 65
            rn[cn] -= 1
            chosen = used_sur[i]
            ok = False
            for cand in sorted(sur):
                if cand in used: continue
                cs = ord(cand[0]) - 65
                rs[cs] -= 1
                gain = 1 if cs == cn else 0
                rem = sum(min(rn[c], rs[c]) for c in range(26))
                feasible = (fixed + gain + rem == Mv)
                if cand == chosen:
                    if not feasible:
                        print("第", i, "位选择不可行:", cand); return 1
                    ok = True
                else:
                    if feasible:
                        print("第", i, "位存在更小的可行附名:", cand, "<", chosen); return 1
                rs[cs] += 1
                if cand == chosen:
                    break
            if not ok:
                print("第", i, "位没找到可行选择"); return 1
            cs = ord(chosen[0]) - 65
            rs[cs] -= 1
            used.add(chosen)
            fixed += 1 if cs == cn else 0
    return 0

sys.exit(main())
