#!/usr/bin/env python3
"""CF298A 的 checker（多解）：在长度受限的走法空间里验证 (s,t) 确实能产生给定足迹。

做法：从 s 出发做带记忆化的 DFS（步数 <= 3n，状态 = (位置, 足迹串)），
      若存在一条走到 t 且足迹恰为输入的路径，则接受。
"""
import sys

def main():
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    n = int(data[0]); fp = data[1]
    toks = open(out).read().split()
    if len(toks) != 2:
        print('CHECKER FAIL: 需要两个整数')
        return 1
    s, t = int(toks[0]), int(toks[1])
    if not (1 <= s <= n and 1 <= t <= n):
        print('CHECKER FAIL: s/t 越界')
        return 1
    if n > 60:
        print('CHECKER SKIP: n 太大（本 checker 只用于样例规模）')
        return 0
    maxlen = 3 * n
    seen = set()
    sys.setrecursionlimit(10000)
    def dfs(cur, steps, f):
        if steps > maxlen:
            return False
        key = (cur, f, steps)
        if key in seen:
            return False
        seen.add(key)
        if cur == t and f == fp:
            return True
        if steps == maxlen:
            return False
        for d in (-1, 1):
            nx = cur + d
            if 1 <= nx <= n:
                lf = list(f)
                lf[cur - 1] = 'R' if d > 0 else 'L'
                if dfs(nx, steps + 1, ''.join(lf)):
                    return True
        return False
    if dfs(s, 0, '.' * n):
        return 0
    print('CHECKER FAIL: (%d,%d) 无法产生给定足迹' % (s, t))
    return 1

if __name__ == '__main__':
    sys.exit(main())
