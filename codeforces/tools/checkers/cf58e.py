import sys

def is_sub(t, s):
    j = 0
    for ch in t:
        if j < len(s) and ch == s[j]:
            j += 1
    return j == len(s)

def main():
    expr = open(sys.argv[1]).read().strip()
    raw = open(sys.argv[2]).read()
    p1 = expr.index('+'); p2 = expr.index('=')
    A, B, C = expr[:p1], expr[p1+1:p2], expr[p2+1:]

    out = raw.strip()
    if out != raw.strip('\n') and out != raw:
        print("行首/行尾有多余空白"); return 1
    if out.count('+') != 1 or out.count('=') != 1:
        print("运算符个数不对"); return 1
    q1 = out.index('+'); q2 = out.index('=')
    X, Y, Z = out[:q1], out[q1+1:q2], out[q2+1:]
    for s in (X, Y, Z):
        if not s.isdigit():
            print("不是数字:", s); return 1
        if len(s) > 1 and s[0] == '0':
            print("有前导零:", s); return 1
    if not (is_sub(X, A) and is_sub(Y, B) and is_sub(Z, C)):
        print("a+b=c 不是子序列"); return 1
    if int(X) + int(Y) != int(Z):
        print("加法不成立"); return 1

    Lout = len(X) + len(Y) + len(Z)
    if Lout <= 7:
        # 枚举所有更短的表达式，确认没有更短解
        for Lx in range(1, Lout - 1):
            for Ly in range(1, Lout - Lx):
                if Lx + Ly + 1 > Lout: continue
                for x in range(10 ** (Lx - 1), 10 ** Lx):
                    sx = str(x)
                    if not is_sub(sx, A): continue
                    for y in range(10 ** (Ly - 1), 10 ** Ly):
                        sy = str(y)
                        if not is_sub(sy, B): continue
                        sz = str(x + y)
                        if len(sx) + len(sy) + len(sz) < Lout and is_sub(sz, C):
                            print("存在更短解:", sx, sy, sz); return 1
    return 0

sys.exit(main())
