#!/usr/bin/env python3
"""CF173D Deputies 的合法性校验器。

用法（与 verify_solution.py 约定一致）：
    python3 cf173d.py <input> <output> <answer>
`answer` 通过 /dev/stdin 传入（verify_solution.py 会把期望输出喂到 stdin）。

构造函数题，任何合法方案都接受。校验内容：
  1. 首行必须是 YES / NO；
  2. 若输出 NO，要求题目给出的参考输出也是 NO（否则选手漏解）；
  3. 若输出 YES，则必须恰好 n 个编号、取值范围 1..k、每个编号恰好出现 3 次，
     且每个编号负责的三座城市之间没有任何一座桥。
退出码 0 表示通过。
"""
import sys


def main() -> int:
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp, encoding='utf-8').read().split()
    n, m = int(data[0]), int(data[1])
    edge = set()
    p = 2
    for _ in range(m):
        a, b = int(data[p]) - 1, int(data[p + 1]) - 1
        p += 2
        edge.add((a, b))
        edge.add((b, a))

    toks = open(outp, encoding='utf-8').read().split()
    if not toks:
        print('empty output')
        return 1
    expected = ''
    try:
        expected = sys.stdin.read().split()[0]
    except Exception:
        expected = ''

    if toks[0] == 'NO':
        if len(toks) != 1:
            print('extra tokens after NO')
            return 1
        if expected and expected != 'NO':
            print('claimed NO but a construction exists')
            return 1
        return 0
    if toks[0] != 'YES':
        print('first token must be YES or NO')
        return 1
    if expected and expected == 'NO':
        print('claimed YES but the answer is NO')
        return 1

    ids = toks[1:]
    if len(ids) != n:
        print(f'expected {n} numbers, got {len(ids)}')
        return 1
    k = n // 3
    groups = {}
    for city, dep in enumerate(ids):
        if not dep.isdigit() or not (1 <= int(dep) <= k):
            print(f'deputy id out of range: {dep}')
            return 1
        groups.setdefault(int(dep), []).append(city)
    if len(groups) != k:
        print(f'expected {k} distinct deputies, got {len(groups)}')
        return 1
    for dep, cities in groups.items():
        if len(cities) != 3:
            print(f'deputy {dep} has {len(cities)} cities')
            return 1
        for i in range(3):
            for j in range(i + 1, 3):
                if (cities[i], cities[j]) in edge:
                    print(f'deputy {dep} gets an edge {cities[i]+1}-{cities[j]+1}')
                    return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
