#!/usr/bin/env python3
"""86B Tetris revisited 的 checker（构造题，答案不唯一）。

用法: python3 cf86b.py <input> <output> <answer>

校验条件（与题面一致）：
  1. 若输出 "-1"：要求确实无解，即存在一个上下左右都没有空格邻居的空格子；
  2. 否则输出必须是 n 行、每行 m 个字符，'#' 的位置与输入完全一致；
     空格子处必须是数字 '0'..'9'（每个图形用一个数字表示）；
  3. 把空格子按「数字相同且四连通」划分成图形，每个图形的大小必须在 2..5 之间
     （任何 2..5 格的连通图形都在 dashboard 里，因此连通性 + 大小就是全部要求）；
  4. 相邻图形自然拿不同数字（否则它们会被并成同一个图形），故条件 3 已隐含
     “相邻图形数字不同”。
"""
import sys


def read_grid(text):
    lines = [l.rstrip('\n') for l in text.split('\n')]
    while lines and lines[-1] == '':
        lines.pop()
    return lines


def main():
    inp, out = sys.argv[1], sys.argv[2]
    data = read_grid(open(inp).read())
    n, m = map(int, data[0].split())
    g = data[1:1 + n]
    res = read_grid(open(out).read())

    # 无解的判据：存在没有任何空格邻居的空格子
    dr = (1, -1, 0, 0)
    dc = (0, 0, 1, -1)
    isolated = any(
        g[i][j] == '.' and not any(
            0 <= i + dr[d] < n and 0 <= j + dc[d] < m and g[i + dr[d]][j + dc[d]] == '.'
            for d in range(4))
        for i in range(n) for j in range(m))

    if len(res) == 1 and res[0].strip() == '-1':
        if isolated:
            return 0
        print('CHECKER FAIL: 存在合法覆盖，但输出是 -1')
        return 1
    if isolated:
        print('CHECKER FAIL: 有孤立空格子，应当输出 -1')
        return 1
    if len(res) != n:
        print(f'CHECKER FAIL: 输出行数 {len(res)} != {n}')
        return 1
    for i in range(n):
        if len(res[i]) != m:
            print(f'CHECKER FAIL: 第 {i+1} 行长度 {len(res[i])} != {m}')
            return 1
        for j in range(m):
            if g[i][j] == '#':
                if res[i][j] != '#':
                    print(f'CHECKER FAIL: ({i+1},{j+1}) 原本是 # 却被改动')
                    return 1
            else:
                if not ('0' <= res[i][j] <= '9'):
                    print(f'CHECKER FAIL: ({i+1},{j+1}) 空格子被填成了 {res[i][j]!r}')
                    return 1

    seen = [[False] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if g[i][j] == '#' or seen[i][j]:
                continue
            col = res[i][j]
            stack = [(i, j)]
            seen[i][j] = True
            size = 0
            while stack:
                r, c = stack.pop()
                size += 1
                for d in range(4):
                    nr, nc = r + dr[d], c + dc[d]
                    if 0 <= nr < n and 0 <= nc < m and not seen[nr][nc] \
                            and g[nr][nc] == '.' and res[nr][nc] == col:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            if not (2 <= size <= 5):
                print(f'CHECKER FAIL: 从 ({i+1},{j+1}) 出发的数字 {col!r} 图形大小 {size} 不在 2..5')
                return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
