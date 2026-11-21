#!/usr/bin/env python3
"""CF253E Printer 的 checker（多解）。

校验条件：
  1. 输出第一行 p_x 在 [1, 1e9] 内，且与其它任务的优先级都不相同；
  2. 第二行恰好 n 个整数，是各任务最后一页打完的时刻；
  3. 用"逐页模拟"（每次打印 1 页，独立于参考实现的批量事件模拟）重放该优先级，
     得到的完成时刻必须与输出完全一致；
  4. 未知任务 x 的完成时刻必须等于输入给出的 T。

用法: python3 cf253e.py <input> <output> <answer>
"""
import sys


def simulate(n, tasks, x, px):
    order = sorted(range(n), key=lambda i: (tasks[i][0], i))
    fin = [None] * n
    rem = [tasks[i][1] for i in range(n)]
    prio = [px if i == x else tasks[i][2] for i in range(n)]
    cur = 0
    idx = 0
    done = 0
    while done < n:
        while idx < n and tasks[order[idx]][0] <= cur:
            idx += 1
        # 候选中选优先级最高的未完成任务（平手取输入下标大的）
        best = -1
        for k in range(idx):
            i = order[k]
            if rem[i] > 0:
                if best < 0 or prio[i] > prio[best] or (prio[i] == prio[best] and i > best):
                    best = i
        if best < 0:
            cur = tasks[order[idx]][0]          # 空闲，等到下一个任务到达
            continue
        rem[best] -= 1
        cur += 1
        if rem[best] == 0:
            fin[best] = cur
            done += 1
    return fin


def main():
    data = open(sys.argv[1], encoding='utf-8').read().split()
    n = int(data[0])
    tasks = []
    pos = 1
    for _ in range(n):
        tasks.append((int(data[pos]), int(data[pos + 1]), int(data[pos + 2])))
        pos += 3
    T = int(data[pos])
    out = open(sys.argv[2], encoding='utf-8').read().split()
    if len(out) != n + 1:
        print('WA: 输出应为 1 + %d 个整数，实际 %d 个' % (n, len(out)))
        return 1
    px = int(out[0])
    got = [int(v) for v in out[1:]]
    x = [i for i in range(n) if tasks[i][2] == -1][0]
    if not (1 <= px <= 10 ** 9):
        print('WA: 优先级 %d 超出 [1,1e9]' % px)
        return 1
    for i in range(n):
        if i != x and tasks[i][2] == px:
            print('WA: 优先级 %d 与任务 %d 重复' % (px, i + 1))
            return 1
    exp = simulate(n, tasks, x, px)
    if got != exp:
        for i in range(n):
            if got[i] != exp[i]:
                print('WA: 任务 %d 完成时刻 %d，重放得到 %d' % (i + 1, got[i], exp[i]))
                break
        return 1
    if got[x] != T:
        print('WA: 未知任务的完成时刻 %d，题面给出 %d' % (got[x], T))
        return 1
    return 0


sys.exit(main())
