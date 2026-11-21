#!/usr/bin/env python3
"""CF245B Internet Address 校验器（多个合法地址，多解）。

约定：python3 cf245b.py <input> <output> <answer>，返回 0 表示通过。
校验条件：
1. 输出一行形如 `<http|ftp>://<domain>.ru[/<context>]`：domain、context 均为
   非空小写字母串（context 可缺省）；
2. 把输出里的 ':' '/' '.' 全部删掉后，必须与输入串完全相同
   （即输出确实是「同一个地址去掉标点」的还原）。
"""
import re
import sys

PAT = re.compile(r'^(http|ftp)://([a-z]+)\.ru(?:/([a-z]+))?$')


def main():
    if len(sys.argv) < 3:
        print('CHECKER FAIL: 用法 cf245b.py <input> <output> <answer>')
        sys.exit(1)
    inp = open(sys.argv[1]).read().strip()
    out = open(sys.argv[2]).read().strip()

    def bad(msg):
        print('CHECKER FAIL:', msg)
        sys.exit(1)

    m = PAT.match(out)
    if not m:
        bad('地址格式不合法: %r' % out)
    if m.group(2) == '' or (m.group(3) is not None and m.group(3) == ''):
        bad('domain / context 不能为空')
    stripped = out.replace(':', '').replace('/', '').replace('.', '')
    if stripped != inp:
        bad('去掉标点后与输入不一致: %r != %r' % (stripped, inp))


if __name__ == '__main__':
    main()
