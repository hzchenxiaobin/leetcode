#!/usr/bin/env python3
"""CF309B Context Advertising 的 checker（多解）。

校验横幅：行数 <= r、每行 <= c 字符、词序列是原文的连续子段、且词数 = 官方最优。
"""
import sys


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n, r, c = int(data[0]), int(data[1]), int(data[2])
    words = data[3:3 + n]
    exp = open(sys.argv[3], encoding='utf-8').read()
    out = open(sys.argv[2], encoding='utf-8').read()
    # 官方的"最优词数"：官方输出本身也是最优横幅
    exp_lines = [l for l in exp.split('\n') if l.strip() != '']
    exp_cnt = sum(len(l.split()) for l in exp_lines)
    lines = [l for l in out.split('\n') if l.strip() != '']
    if len(lines) > r:
        print('WA: 行数 %d 超过 r=%d' % (len(lines), r))
        return 1
    got = []
    for l in lines:
        if len(l) > c:
            print('WA: 行宽 %d 超过 c=%d' % (len(l), c))
            return 1
        got += l.split()
    m = len(got)
    ok = False
    for st in range(n - m + 1):
        if words[st:st + m] == got:
            ok = True
            break
    if not ok:
        print('WA: 词序列不是原文的连续子段')
        return 1
    if m != exp_cnt:
        print('WA: 词数 %d 不是最优 %d' % (m, exp_cnt))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
