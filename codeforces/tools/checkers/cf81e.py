#!/usr/bin/env python3
"""CF81E Pairs 的答案校验器（答案不唯一）。

用法: python3 cf81e.py <input> <output> [expected]
  input：n / 每行 f_i s_i
  output：第一行 t e，随后 t 行每行一对学生
  expected（第 3 个参数，通常是 /dev/stdin，从标准输入读）：官方答案，用来核对 (t, e)

校验条件：
  1. 方案本身合法：每对 (a,b) 必须满足 f_a == b 或 f_b == a；每个学生至多出现一次；
     第一行的 t 等于对数，e 等于这些对里男女搭配的对数。
  2. 最优性：t 与 e 必须等于官方答案的 t, e（t, e 由问题唯一确定）。
     如果没有给出官方答案（或为空），对 |E| <= 22 的小数据用暴力枚举所有匹配求 (t, e) 并比对；
     再大的数据只做第 1 条的结构校验（此时仍可保证输出方案合法）。
"""
import sys


def parse_input(text):
    tok = text.split()
    n = int(tok[0])
    f = [0] * (n + 1)
    sex = [0] * (n + 1)
    p = 1
    for i in range(1, n + 1):
        f[i] = int(tok[p]); sex[i] = int(tok[p + 1]); p += 2
    return n, f, sex


def brute_best(n, f, sex):
    edges, seen = [], set()
    for i in range(1, n + 1):
        a, b = i, f[i]
        key = (min(a, b), max(a, b))
        if key in seen:
            continue
        seen.add(key)
        edges.append((a, b))
    m = len(edges)
    used = [False] * (n + 1)
    best = (0, 0)

    def rec(idx, t, e):
        nonlocal best
        if idx == m:
            if (t, e) > best:
                best = (t, e)
            return
        # 剩余边数不够超过当前最优时剪枝（仍保证正确）
        if t + (m - idx) <= best[0]:
            # 还有可能通过 e 变好？只有当 t 相同才需要比 e，这里保守地不剪枝
            pass
        rec(idx + 1, t, e)
        a, b = edges[idx]
        if not used[a] and not used[b]:
            used[a] = used[b] = True
            rec(idx + 1, t + 1, e + (1 if sex[a] != sex[b] else 0))
            used[a] = used[b] = False

    rec(0, 0, 0)
    return best


def main() -> int:
    inp_path, out_path = sys.argv[1], sys.argv[2]
    n, f, sex = parse_input(open(inp_path).read())

    toks = open(out_path).read().split()
    if len(toks) < 2:
        print("输出太短", file=sys.stderr)
        return 1
    t, e = int(toks[0]), int(toks[1])
    rest = toks[2:]
    if len(rest) != 2 * t:
        print(f"声称 {t} 对，实际给了 {len(rest) // 2} 对", file=sys.stderr)
        return 1
    used = [False] * (n + 1)
    mixed = 0
    for k in range(t):
        a, b = int(rest[2 * k]), int(rest[2 * k + 1])
        if not (1 <= a <= n and 1 <= b <= n):
            print(f"学生编号越界: {a} {b}", file=sys.stderr)
            return 1
        if a == b:
            print(f"非法：自己与自己配对 {a}", file=sys.stderr)
            return 1
        if f[a] != b and f[b] != a:
            print(f"{a} 与 {b} 不是好友关系", file=sys.stderr)
            return 1
        if used[a] or used[b]:
            print(f"学生重复出现: {a} {b}", file=sys.stderr)
            return 1
        used[a] = used[b] = True
        if sex[a] != sex[b]:
            mixed += 1
    if mixed != e:
        print(f"e 声明为 {e}，实际混合对 {mixed}", file=sys.stderr)
        return 1

    # 最优性核对
    expected = ""
    if len(sys.argv) > 3:
        expected = sys.stdin.read()
    exp_tok = expected.split()
    if len(exp_tok) >= 2:
        et, ee = int(exp_tok[0]), int(exp_tok[1])
        if (t, e) != (et, ee):
            print(f"(t,e) = ({t},{e})，官方最优为 ({et},{ee})", file=sys.stderr)
            return 1
        return 0
    # 没有官方答案：小数据用暴力确认最优
    edges_cnt = len({(min(i, f[i]), max(i, f[i])) for i in range(1, n + 1)})
    if edges_cnt <= 22:
        bt, be = brute_best(n, f, sex)
        if (t, e) != (bt, be):
            print(f"(t,e) = ({t},{e})，暴力最优为 ({bt},{be})", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
