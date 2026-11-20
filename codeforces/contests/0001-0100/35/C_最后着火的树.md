# Codeforces 35C 最后着火的树 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/35/C
- **比赛来源**：Codeforces Beta Round 35 · Problem C
- **难度**：1500
- **标签**：暴力、BFS、最短路
- **评测类型**：特殊评测（多解，输出任意一个）
- **限制**：时间 2 s / 内存 64 MB

**题意**：森林是 $N \times M$ 的网格，坐标 $(x,y)$（$1 \le x \le N$，$1 \le y \le M$）。$K$ 个格子同时起火，每分钟火蔓延到与已燃格子**曼哈顿距离为 1** 的格子。求**最后一个**着火的格子；有多个时输出任意一个。

**约束**：

- $N, M \le 2000$：最多 $4\times10^6$ 个格子。
- $K \le 10$：源点很少。
- 每个格子的着火时间 = 到最近源点的曼哈顿距离。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 3
1
2 2

输出：
1 1
```

唯一的源在中心，四个角 $(1,1),(1,3),(3,1),(3,3)$ 都是第 2 分钟着火，输出任意一个 ✓。

官方样例 2：

```text
输入：
3 3
1
1 1

输出：
3 3
```

源在左上角，最远的是右下角（距离 4）✓。

官方样例 3：

```text
输入：
3 3
2
1 1 3 3

输出：
2 2
```

两个源在对角，$(2,2)$、$(1,3)$、$(3,1)$ 都是第 2 分钟着火，输出 $(2,2)$ ✓。

**观察一**：着火时间 $t(x,y) = \min_k \bigl(|x-x_k| + |y-y_k|\bigr)$。
**观察二**：答案就是 $t$ 最大的格子。
**观察三**：多源最短路的特殊结构——曼哈顿距离可以用**两遍扫描**（距离变换）在 $O(NM)$ 内求出，不必真的跑 BFS。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

对每个格子枚举 $K$ 个源点算最小距离：$O(NMK) = 4\times10^6 \times 10 = 4\times10^7$，C++ 可以过但偏慢；多源 BFS 是 $O(NM)$，更快。

### 3.2 核心观察：两遍扫描的距离变换

![两遍扫描传播距离](../../../images/cf35c_sweep.svg)

先把源点置 $0$、其它置 $\infty$，然后：

1. **正向扫描**（$i$ 从小到大、$j$ 从小到大）：
   $$d[i][j] = \min\bigl(d[i][j],\ d[i-1][j]+1,\ d[i][j-1]+1\bigr);$$
2. **反向扫描**（$i$ 从大到小、$j$ 从大到小）：
   $$d[i][j] = \min\bigl(d[i][j],\ d[i+1][j]+1,\ d[i][j+1]+1\bigr).$$

两遍之后 $d[i][j]$ 就是到最近源点的曼哈顿距离。

**为什么两遍就够？** 从源点到 $(i,j)$ 的最短曼哈顿路径可以取"先只向上/左走，再只向下/右走"的形式（四个方向可以重排），正向扫描处理了"从上/左来"的部分，反向扫描处理了"从下/右来"的部分，合起来覆盖所有情况（见第 4 节）。

### 3.3 统计答案

![样例 3 的距离场](../../../images/cf35c_field.svg)

扫一遍所有格子，取 $d$ 的最大值。题目允许多解，本实现按 $( \max(x,y),\ x,\ y )$ 最小的规则挑一个（恰好与三组样例一致）；这对正确性没有影响。

### 3.4 样例走查

样例 1（$3\times3$，源 $(2,2)$）的距离场：

| | 1 | 2 | 3 |
|---|---|---|---|
| 1 | 2 | 1 | 2 |
| 2 | 1 | 0 | 1 |
| 3 | 2 | 1 | 2 |

最大值 2，出现在四个角，按规则取 $(1,1)$ ✓。

## 4. 正确性证明

**引理 1（距离变换的正确性）**：两遍扫描后 $d[i][j] = \min_k \bigl(|i-x_k| + |j-y_k|\bigr)$。

**证明**：记 $D[i][j]$ 为真正的最近距离。

(≥) 每次更新都是沿着一条合法的网格路径把某个源点的距离传过来（每步 +1），所以 $d[i][j] \ge D[i][j]$（归纳）。

(≤) 取最近的源点 $s$，考虑从 $s$ 到 $(i,j)$ 的一条最短曼哈顿路径。把这条路径拆成"先按行、再按列"的两段：先从 $s$ 沿行走到 $i$，再沿列走到 $j$（或反之）。对任意 $s$ 与 $(i,j)$，总可以选一种拆分使第一步的移动方向是"向上或向左"、第二步是"向下或向右"（把负方向的位移放在第一段、正方向的放在第二段）。第一段由正向扫描累加（它可以只需要从上/左邻居取 +1 逐步传播），第二段由反向扫描累加，于是 $d[i][j] \le D[i][j]$ ✓。

两者夹住得等号。∎

**引理 2（最大距离即最后着火）**：格子 $(i,j)$ 的着火时间就是 $D[i][j]$，所以 $D$ 最大的格子最后着火。

**证明**：火每分钟沿网格边扩散一格，$t$ 分钟能到达的正是与某源点曼哈顿距离 $\le t$ 的格子，故着火时间 $=D[i][j]$ ✓。∎

**定理**：算法输出的格子是所有格子中最后着火的（之一）。

**证明**：引理 1 给出正确的距离场，引理 2 说明取最大值即最后着火；并列时输出任意一个符合题面 ✓。∎

## 5. 复杂度分析

- **时间**：$O(NM)$，两遍扫描；$4\times10^6$ 个格子。
- **空间**：$O(NM)$ 的距离数组（约 16 MB）。
- **与时限的关系**：C++ 实测约 $0.03$ s；Python 约 $2.6$ s（CPython 逐格循环偏慢，建议 PyPy3）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int N, M;
    if (scanf("%d %d", &N, &M) != 2) return 0;
    int K;
    scanf("%d", &K);
    const int INF = 1e9;
    vector<int> d((size_t)N * M, INF);
    for (int i = 0; i < K; i++) {
        int x, y;
        scanf("%d %d", &x, &y);
        d[(size_t)(x - 1) * M + (y - 1)] = 0;
    }
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++) {
            int &cur = d[(size_t)i * M + j];
            if (i > 0) cur = min(cur, d[(size_t)(i - 1) * M + j] + 1);
            if (j > 0) cur = min(cur, d[(size_t)i * M + j - 1] + 1);
        }
    for (int i = N - 1; i >= 0; i--)
        for (int j = M - 1; j >= 0; j--) {
            int &cur = d[(size_t)i * M + j];
            if (i + 1 < N) cur = min(cur, d[(size_t)(i + 1) * M + j] + 1);
            if (j + 1 < M) cur = min(cur, d[(size_t)i * M + j + 1] + 1);
        }
    int best = -1, bx = 1, by = 1, bmax = INT_MAX;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++) {
            int v = d[(size_t)i * M + j];
            int mx = max(i + 1, j + 1);
            if (v > best || (v == best && (mx < bmax || (mx == bmax && (i + 1 < bx || (i + 1 == bx && j + 1 < by)))))) {
                best = v; bx = i + 1; by = j + 1; bmax = mx;
            }
        }
    printf("%d %d\n", bx, by);
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    N, M = int(data[0]), int(data[1])
    K = int(data[2])
    INF = 1 << 30
    d = [INF] * (N * M)
    pos = 3
    for _ in range(K):
        x, y = int(data[pos]) - 1, int(data[pos + 1]) - 1
        pos += 2
        d[x * M + y] = 0
    for i in range(N):
        base = i * M
        up = base - M
        for j in range(M):
            cur = d[base + j]
            if i > 0:
                v = d[up + j] + 1
                if v < cur:
                    cur = v
            if j > 0:
                v = d[base + j - 1] + 1
                if v < cur:
                    cur = v
            d[base + j] = cur
    for i in range(N - 1, -1, -1):
        base = i * M
        down = base + M
        for j in range(M - 1, -1, -1):
            cur = d[base + j]
            if i + 1 < N:
                v = d[down + j] + 1
                if v < cur:
                    cur = v
            if j + 1 < M:
                v = d[base + j + 1] + 1
                if v < cur:
                    cur = v
            d[base + j] = cur
    best = -1
    bx, by, bmax = 1, 1, INF
    for i in range(N):
        base = i * M
        for j in range(M):
            v = d[base + j]
            mx = i + 1 if i + 1 > j + 1 else j + 1
            if v > best or (v == best and (mx < bmax or (mx == bmax and (i + 1 < bx or (i + 1 == bx and j + 1 < by))))):
                best, bx, by, bmax = v, i + 1, j + 1, mx
    sys.stdout.write("%d %d\n" % (bx, by))


main()
```

## 7. 边界情况与易错点

1. **$1 \times 1$ 网格**：唯一的格子就是火源，输出 `1 1`。
2. **源点就是答案**：若所有格子都着火（$K$ 覆盖全图），最大距离为 0，输出任意源点。
3. **多解**：题面允许任意一个，本实现用固定的取舍规则（评测器对并列不敏感）。
4. **距离数组用 `int`**：最大距离 $N+M \le 4000$，不会溢出。
5. **下标**：输入是 1-based，数组是 0-based，别弄混。
6. **两遍扫描的方向**：正向用"上、左"，反向用"下、右"；顺序反了会得到错误距离。
7. **Python 性能**：$2000\times2000$ 在 CPython 下约 2.6 s，建议 PyPy3。
8. **内存**：$4\times10^6$ 个 `int` 约 16 MB，在 64 MB 限制内。

## 8. 验证记录

- **编译环境与命令**：`Apple clang 21.0.0` + 兼容头，`clang++ -std=c++17 -O2`；Python 3.9.6。
- **官方样例**：3 / 3 通过（`1 1`、`3 3`、`2 2`），`verify_solution.py` 报告 `CF35C: samples 3 / C++ 编译 OK, 样例 3/3 / Python 语法 OK, 样例 3/3`。
- **独立对拍**：随机 $N, M \in [1,9]$、$K \le \min(10, NM)$ 共 **300 组**。独立校验：直接对每个格子计算 $\min_k(|x-x_k|+|y-y_k|)$，求出最大值，并检查程序输出的格子（在范围内且）距离等于最大值。300 组全部一致。
- **边界用例**：$1\times1$、单行、单列、源在对角、所有格子都是源。
- **最大约束性能**：$N = M = 2000$、$K = 10$，C++ 端到端约 $0.03$ s，Python 约 $2.6$ s。
- **图片校验**：两张 SVG 均通过 `ElementTree.parse`，文本包围盒估算无越界、无重叠。
- **公式校验**：KaTeX（`throwOnError`）无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 35B Warehouse](https://codeforces.com/problemset/problem/35/B)：同场 B 题，模拟。
- [Codeforces 35E Parade](https://codeforces.com/problemset/problem/35/E)：同场 E 题，扫描线。
- [LeetCode 542. 01 矩阵](https://leetcode.cn/problems/01-matrix/)：多源 BFS / 距离变换，与本题同源。
- [Codeforces 35D Animals](https://codeforces.com/problemset/problem/35/D)：同场 D 题，贪心。

**延伸思考**：

1. **如果火按欧氏距离蔓延**？距离变换要换成欧氏距离变换（更复杂，通常用抛物线包络）。
2. **如果要求输出所有最后着火的格子**？扫一遍收集所有最大值格子即可。
3. **如果 $K$ 很大（如 $10^5$）**？两遍扫描仍然 $O(NM)$，与 $K$ 无关（只有置 0 是 $O(K)$）。
4. **如果网格是稀疏的（只给障碍物）**？需要 BFS 而不是距离变换。
