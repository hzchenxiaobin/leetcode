#!/usr/bin/env python3
"""CF82D Two out of Three 的 checker。

题意：队列 n 个人，每阶段从「队首三人」中挑两人同时服务，耗时 max(a_i,a_j)；
只剩一人时单独服务，耗时 a_i。求最短总时间并给出方案（多解）。

校验：
1. 第一行是总时间，必须等于 checker 独立 DP 算出的最优值；
2. 后续每行 1 或 2 个人：2 人时两人必须都在当前队首三人之内，且恰好去掉他们；
   1 人时必须是队列里仅剩的那个人；行数必须为 ceil(n/2)；
3. 所有人恰好被服务一次，累加耗时与第一行一致。

用法: python3 cf82d.py <input> <output> <answer>；返回 0 通过。
"""
import sys


def optimum(a, n):
    INF = float('inf')
    # dp[x][k]：队首残留 x（0 表示无），下一个未处理的人是 k
    dp = [[INF] * (n + 3) for _ in range(n + 2)]
    for k in range(n + 1, 0, -1):
        for x in range(0, n + 1):
            if x != 0 and x >= k:
                continue
            if k == n + 1:
                dp[x][k] = 0 if x == 0 else a[x]
            elif x == 0:
                if k == n:
                    dp[x][k] = a[k]
                elif k == n - 1:
                    dp[x][k] = max(a[k], a[k + 1]) + dp[0][n + 1]
                else:
                    dp[x][k] = min(max(a[k], a[k + 1]) + dp[k + 2][k + 3],
                                   max(a[k], a[k + 2]) + dp[k + 1][k + 3],
                                   max(a[k + 1], a[k + 2]) + dp[k][k + 3])
            else:
                if k == n:
                    dp[x][k] = max(a[x], a[n]) + dp[0][n + 1]
                else:
                    dp[x][k] = min(max(a[x], a[k]) + dp[0][k + 1],
                                   max(a[x], a[k + 1]) + dp[k][k + 2],
                                   max(a[k], a[k + 1]) + dp[x][k + 2])
    return dp[0][1]


def main():
    inp, out = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    n = int(data[0])
    a = [0] * (n + 2)
    for i in range(1, n + 1):
        a[i] = int(data[i])

    raw = [l for l in open(out).read().split('\n') if l.strip()]
    if not raw:
        print('CHECKER FAIL: 空输出')
        return 1
    head = raw[0].split()
    if len(head) != 1:
        print('CHECKER FAIL: 第一行应为单个总时间')
        return 1
    printed = int(head[0])
    best = optimum(a, n)
    if printed != best:
        print(f'CHECKER FAIL: 输出总时间 {printed}，最优是 {best}')
        return 1

    queue = list(range(1, n + 1))
    served = []
    total = 0
    stages = 0
    for line in raw[1:]:
        t = [int(x) for x in line.split()]
        stages += 1
        if len(t) == 1:
            if len(queue) != 1 or t[0] != queue[0]:
                print('CHECKER FAIL: 单人阶段必须是队列里仅剩的那个人')
                return 1
            total += a[t[0]]
            served.append(queue.pop())
        elif len(t) == 2:
            if len(queue) < 2:
                print('CHECKER FAIL: 队列人数不足')
                return 1
            front = queue[:3]
            if t[0] not in front or t[1] not in front or t[0] == t[1]:
                print(f'CHECKER FAIL: {t} 不是队首三人中的两个（队首 {front}）')
                return 1
            total += max(a[t[0]], a[t[1]])
            for x in t:
                queue.remove(x)
            served.extend(t)
        else:
            print('CHECKER FAIL: 每行只能是 1 或 2 个人')
            return 1
    if queue:
        print('CHECKER FAIL: 还有人没被服务')
        return 1
    if sorted(served) != list(range(1, n + 1)):
        print('CHECKER FAIL: 有人被重复/遗漏服务')
        return 1
    if stages != (n + 1) // 2:
        print(f'CHECKER FAIL: 阶段数 {stages} != {(n + 1) // 2}')
        return 1
    if total != printed:
        print(f'CHECKER FAIL: 方案累加耗时 {total} != 输出总时间 {printed}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
