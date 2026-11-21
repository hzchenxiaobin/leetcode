#!/usr/bin/env python3
"""CF286C 的 checker（多解）：验证符号正确、强制位为负、括号序列正确。"""
import sys

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    d = [int(x) for x in open(inp).read().split()]
    p = 0
    n = d[p]; p += 1
    a = [0] + d[p:p + n]; p += n
    t = d[p]; p += 1
    forced = set(d[p:p + t])
    toks = open(out).read().split()
    if not toks:
        print('CHECKER FAIL: 空输出')
        return 1
    if toks[0] == 'NO':
        return 0
    if toks[0] != 'YES' or len(toks) != n + 1:
        print('CHECKER FAIL: 输出格式不对')
        return 1
    x = [int(v) for v in toks[1:]]
    st = []
    for i in range(1, n + 1):
        if abs(x[i - 1]) != a[i]:
            print('CHECKER FAIL: 第 %d 个数绝对值错' % i)
            return 1
        if x[i - 1] > 0:
            if i in forced:
                print('CHECKER FAIL: 第 %d 位被强制为负却给了正号' % i)
                return 1
            st.append(x[i - 1])
        else:
            if not st or st[-1] != -x[i - 1]:
                print('CHECKER FAIL: 第 %d 位无法匹配栈顶' % i)
                return 1
            st.pop()
    if st:
        print('CHECKER FAIL: 结束时栈非空')
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
