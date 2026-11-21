#!/usr/bin/env python3
"""CF180A Defragmentation 的 checker（构造题，任意合法方案都接受）。

用法（与 verify_solution.py 约定一致）：
    python3 cf180a.py <input> <output> <answer>

校验条件：
  1. 输出第一行是操作数 k，须满足 0 <= k <= 2n；
  2. 接下来恰好 k 行，每行两个整数 i j，1 <= i,j <= n 且 i != j（复制 i 到 j）；
  3. 按顺序模拟 copy 操作后，前 N 个簇（N = 所有文件片段总数）恰好是
     「若干个文件按任意顺序依次首尾相接、每个文件内部保持原片段顺序」；
     其余簇（N+1..n）已声明为不可用，内容不限。
"""
import sys


def main() -> int:
    data = open(sys.argv[1], encoding='utf-8').read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    m = int(data[pos]); pos += 1
    files = []
    total = 0
    for _ in range(m):
        cnt = int(data[pos]); pos += 1
        cells = [int(data[pos + j]) for j in range(cnt)]
        pos += cnt
        files.append(cells)
        total += cnt

    token_at = {}          # 初始每个簇里的 token 编号
    token_file = []        # token -> 所属文件
    token_index = []       # token -> 在该文件里的序号
    tok = 0
    for f, cells in enumerate(files):
        for idx, cell in enumerate(cells):
            token_at[cell] = tok
            token_file.append(f)
            token_index.append(idx)
            tok += 1

    out = open(sys.argv[2], encoding='utf-8').read().split()
    if not out:
        print('输出为空')
        return 1
    try:
        k = int(out[0])
    except ValueError:
        print('第一行不是整数')
        return 1
    if not 0 <= k <= 2 * n:
        print(f'操作数 {k} 不在 [0, {2 * n}] 内')
        return 1
    if len(out) != 1 + 2 * k:
        print(f'操作数 {k}，但后面有 {len(out) - 1} 个 token（应为 {2 * k}）')
        return 1

    content = [-1] * (n + 1)
    for cell, t in token_at.items():
        content[cell] = t
    for i in range(k):
        a = int(out[1 + 2 * i])
        b = int(out[2 + 2 * i])
        if not (1 <= a <= n and 1 <= b <= n):
            print(f'第 {i + 1} 个操作的下标越界: {a} {b}')
            return 1
        if a == b:
            print(f'第 {i + 1} 个操作 i == j: {a}')
            return 1
        content[b] = content[a]

    # 前 total 个簇必须拼成所有文件的一个排列，文件内部顺序不变
    used = [False] * m
    cell = 1
    while cell <= total:
        t = content[cell]
        if t < 0 or t >= tok:
            print(f'第 {cell} 个簇不是任何文件片段')
            return 1
        f = token_file[t]
        if used[f]:
            print(f'文件 {f + 1} 出现了两次')
            return 1
        used[f] = True
        for idx in range(len(files[f])):
            if cell > total or content[cell] != sum(len(files[x]) for x in range(f)) + idx:
                print(f'文件 {f + 1} 的第 {idx + 1} 个片段不在位置 {cell}')
                return 1
            cell += 1
    if not all(used):
        print('有文件没出现在前 N 个簇里')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
