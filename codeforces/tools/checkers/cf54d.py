#!/usr/bin/env python3
"""54D 的 checker：验证输出字符串是否恰好满足题目要求；
输出 "No solution" 时用独立的回溯搜索确认确实无解。

用法：python3 checker.py <input> <output> <answer>（<answer> 为 /dev/stdin 时从标准输入读）
"""
import sys


def feasible(n, k, p, b):
    """独立回溯：是否存在长度 n、字母表前 k 个、出现位置恰好为 b 的字符串。"""
    m = len(p)
    dom = [list(range(k)) for _ in range(n)]
    pc = [ord(ch) - 97 for ch in p]
    for i in range(n - m + 1):
        if b[i] == '1':
            for j in range(m):
                c = pc[j]
                if c not in dom[i + j]:
                    return False
                dom[i + j] = [c]

    s = [-1] * n
    nodes = [0]

    def window_ok(pos):
        st = pos - m + 1
        if st < 0:
            return True
        match = all(s[st + j] == pc[j] for j in range(m))
        return match if b[st] == '1' else not match

    def dfs(i):
        if i == n:
            return True
        nodes[0] += 1
        if nodes[0] > 300000:
            raise TimeoutError
        for c in dom[i]:
            s[i] = c
            if window_ok(i) and dfs(i + 1):
                return True
        s[i] = -1
        return False

    try:
        return dfs(0)
    except TimeoutError:
        return None


def main() -> int:
    inp, out, ans = sys.argv[1], sys.argv[2], sys.argv[3]
    data = open(inp).read().split()
    n, k = int(data[0]), int(data[1])
    p, b = data[2], data[3]
    m = len(p)
    expected = (sys.stdin.read() if ans == "/dev/stdin" else open(ans).read()).strip()
    got = open(out).read().strip()

    if got == "No solution":
        ok = feasible(n, k, p, b)
        if ok is None:                      # 搜索超限：退回与参考答案一致即可
            return 0 if expected == "No solution" else 1
        if ok:
            print("应为有解，但输出 No solution")
            return 1
        return 0

    # 验证字符串
    if len(got) != n:
        print("长度错误: %d != %d" % (len(got), n)); return 1
    if any(ord(ch) - 97 >= k or ord(ch) < 97 for ch in got):
        print("使用了字母表以外的字符"); return 1
    for i in range(n - m + 1):
        occ = got[i:i + m] == p
        if occ != (b[i] == '1'):
            print("位置 %d 的出现情况不符: 实际 %s, 要求 %s" % (i, occ, b[i] == '1'))
            return 1
    return 0


sys.exit(main())
