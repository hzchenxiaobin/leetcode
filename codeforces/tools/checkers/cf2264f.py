#!/usr/bin/env python3
"""CF2264F 校验器（特殊评测：输出任意合法 DC 表达式）。

用法: cf2264f.py <input> <output> <answer>

对输出表达式（只含 round()+-*/ 和 n）在 n=2..k 上逐一求值：
  - 语法必须可解析；除零视为非法；
  - 每个值必须等于错排数 D(n)（D(1)=0, D(2)=1, D(n)=(n-1)(D(n-1)+D(n-2))）。
不与 answer 做逐 token 比较（answer 只是官方给的一种可行写法）。
"""
import sys
from fractions import Fraction


class Parser:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ''

    def eat(self, ch):
        if self.peek() != ch:
            raise ValueError('期望 %r，得到 %r（位置 %d）' % (ch, self.peek(), self.i))
        self.i += 1

    def expr(self, n):
        v = self.term(n)
        while self.peek() in ('+', '-'):
            op = self.s[self.i]; self.i += 1
            w = self.term(n)
            v = v + w if op == '+' else v - w
        return v

    def term(self, n):
        v = self.factor(n)
        while self.peek() in ('*', '/'):
            op = self.s[self.i]; self.i += 1
            w = self.factor(n)
            if op == '*':
                v = v * w
            else:
                if w == 0:
                    raise ZeroDivisionError('除零（位置 %d）' % self.i)
                v = v / w
        return v

    def factor(self, n):
        c = self.peek()
        if c == 'n':
            self.i += 1
            return Fraction(n)
        if c == '(':
            self.i += 1
            v = self.expr(n)
            self.eat(')')
            return v
        if c == 'r':  # round(...)
            if not self.s.startswith('round(', self.i):
                raise ValueError('未知记号（位置 %d）' % self.i)
            self.i += len('round(')
            v = self.expr(n)
            self.eat(')')
            # round：四舍五入到最近整数（.5 取远离 0 的一侧）
            num, den = v.numerator, v.denominator
            if den == 1:
                return v
            q, r = divmod(abs(num), den)
            if 2 * r >= den:
                q += 1
            return Fraction(-q if num < 0 else q)
        raise ValueError('非法字符 %r（位置 %d）' % (c, self.i))


def main():
    k = int(open(sys.argv[1], encoding='utf-8').read().split()[0])
    expr = open(sys.argv[2], encoding='utf-8').read().strip()
    if len(expr) > 10000:
        print('WRONG: 表达式超过 10000 字符')
        sys.exit(1)
    allowed = set('round()+-*/n ')
    bad = set(expr) - allowed
    if bad:
        print('WRONG: 含非法字符 %s' % sorted(bad))
        sys.exit(1)
    expr = expr.replace(' ', '')

    # 错排数表
    D = {1: 0, 2: 1}
    for i in range(3, k + 1):
        D[i] = (i - 1) * (D[i - 1] + D[i - 2])

    try:
        for n in range(2, k + 1):
            p = Parser(expr)
            v = p.expr(n)
            if p.i != len(expr):
                raise ValueError('表达式尾部有多余内容（位置 %d）' % p.i)
            if v.denominator != 1 or int(v) != D[n]:
                print('WRONG: n=%d 时值为 %s，应为错排数 %d' % (n, v, D[n]))
                sys.exit(1)
    except (ValueError, ZeroDivisionError) as e:
        print('WRONG: %s' % e)
        sys.exit(1)


main()
