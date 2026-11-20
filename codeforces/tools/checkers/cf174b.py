#!/usr/bin/env python3
"""CF174B File List 的合法性校验器。

用法：python3 cf174b.py <input> <output> <answer>
`answer` 由 verify_solution.py 通过 /dev/stdin 传入期望输出。

校验：
  1. 首行必须是 YES / NO；
  2. 输出 NO 时，要求参考输出也是 NO；
  3. 输出 YES 时，各段按顺序拼接必须恰好等于原串；每段恰好含一个点，
     点左边 1..8 个小写字母、右边 1..3 个小写字母。
退出码 0 表示通过。
"""
import sys


def main() -> int:
    s = open(sys.argv[1], encoding='utf-8').read().split()[0]
    toks = open(sys.argv[2], encoding='utf-8').read().split()
    expected = ''
    try:
        expected = sys.stdin.read().split()[0]
    except Exception:
        expected = ''
    if not toks:
        print('empty output')
        return 1
    if toks[0] == 'NO':
        if len(toks) != 1:
            print('extra tokens after NO')
            return 1
        if expected and expected != 'NO':
            print('claimed NO but a partition exists')
            return 1
        return 0
    if toks[0] != 'YES':
        print('first token must be YES or NO')
        return 1
    if expected and expected == 'NO':
        print('claimed YES but the answer is NO')
        return 1
    parts = toks[1:]
    if not parts:
        print('no parts')
        return 1
    if ''.join(parts) != s:
        print('parts do not concatenate to the input')
        return 1
    for p in parts:
        if p.count('.') != 1:
            print(f'part {p!r} does not contain exactly one dot')
            return 1
        name, ext = p.split('.')
        if not (1 <= len(name) <= 8) or not name.isalpha() or not name.islower():
            print(f'bad name in {p!r}')
            return 1
        if not (1 <= len(ext) <= 3) or not ext.isalpha() or not ext.islower():
            print(f'bad ext in {p!r}')
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
