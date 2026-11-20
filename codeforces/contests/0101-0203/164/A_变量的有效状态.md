# Codeforces 164A 变量的有效状态 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/164/A
- **比赛来源**：VK Cup 2012 Round 3 · Problem A（UTC 2012-04-08）
- **难度**：1700
- **标签**：图论、可达性
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个状态，每个状态对变量 Vasya 做一件事：$f_i=1$ 赋值、$f_i=2$ 使用、$f_i=0$ 忽略。给出 $m$ 条有向转移。若存在一条路径 $p_1..p_k$，其中 $p_1$ 赋值、$p_k$ 使用、除 $p_1$ 外没有赋值状态，且状态 $v$ 出现在该路径上，则称 $v$ 处的值"对世界有意义"。求所有有意义的状态。

**约束**：$n,m\le10^5$：两遍 BFS。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
4 3
1 0 0 2
1 2
2 3
3 4
输出：
1
1
1
1
```

路径 1→2→3→4：起点赋值、终点使用、中间无赋值 ⇒ 4 个状态全有意义 ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
3 1
1 0 2
1 3
输出：
1
0
1
```

1 赋值、3 使用、1→3 ⇒ 状态 1、3 有意义；状态 2 不在任何这样的路径上 ✓

官方样例 3（输入 / 输出原样）：

```text
输入：
3 1
2 0 1
1 3
输出：
0
0
0
```

赋值的是状态 3、使用的是状态 1，而边是 1→3（方向反了）⇒ 无意义 ✓

![正向从赋值出发、反向从使用出发](../../../images/cf164a_reach.svg)

**观察**：一条合法路径 = "从某个赋值状态出发（之后不再经过赋值）" 的一段 + "到某个使用状态结束（中间不经过赋值）" 的一段。于是

- $F[v]$：$v$ 可由某个赋值状态**经非赋值中间状态**到达；
- $G[v]$：从 $v$ 出发**经非赋值中间状态**能到达某个使用状态。

$v$ 有意义 ⟺ $F[v]\wedge G[v]$（赋值状态自身视为 $F$ 为真）。两遍 BFS 即可：$F$ 从所有赋值状态向非赋值后继扩展；$G$ 从所有使用状态沿反向边向"其前驱非赋值"扩展。

## 3. 解题思路

1. 读图，建正向与反向邻接表；
2. 正向 BFS：从每个赋值状态出发，只走入非赋值状态，标记 $F$；
3. 反向 BFS：从每个使用状态出发，对前驱 $u$（要求当前点 $v$ 非赋值，即路径中间不出现赋值）标记 $G$；
4. 输出 $F[v]\vee(f_v=1)$ 且 $G[v]$ 的状态为 1。

![样例 2：状态 1（赋值）与 3（使用）有意义](../../../images/cf164a_sample.svg)

## 4. 正确性证明

**引理 1（$F$ 的语义）**：$F[v]$ 为真 ⟺ 存在路径 $u\to\cdots\to v$，$u$ 是赋值状态，且除 $u$ 外路径上无赋值状态。

**证明**：正向 BFS 的每一步都要求目标非赋值，且起点为赋值状态 ⇒ 每条被标记的路径满足条件 ✓ 反之满足条件的路径可逐步被 BFS 走过（归纳于步数）✓ ∎

**引理 2（$G$ 的语义）**：$G[v]$ 为真 ⟺ 存在路径 $v\to\cdots\to w$，$w$ 是使用状态，且除起点外路径上无赋值状态。

**证明**：反向 BFS 中，只有当被扩展的当前点 $v$ 非赋值时才向它的前驱传播 ⇒ 传播路径上的中间点均非赋值，终点为使用状态 ✓ 反之同理 ∎

**定理**：状态 $v$ 有意义 ⟺ $\big(F[v]\vee f_v=1\big)\wedge G[v]$。

**证明**：
(⇐) 设 $F[v]$ 真（或 $v$ 本身是赋值状态），则存在从赋值到 $v$ 的合法前段（引理 1）；再由 $G[v]$ 存在从 $v$ 到使用状态的合法后段（引理 2）。拼接得路径：起点赋值、终点使用、除起点外无赋值，且经过 $v$ ⇒ 有意义 ✓
(⇒) 设有意义，取该合法路径经过 $v$：$v$ 之前的部分给出"从赋值到 $v$ 且中间无赋值"（若 $v$ 之前没有赋值点则 $v$ 是起点赋值）⇒ $F[v]$ 或 $f_v=1$；$v$ 之后的部分给出 $G[v]$ ✓ ∎

## 5. 复杂度分析

- **时间**：两遍 BFS，$O(n+m)$，实测 < 20 ms。
- **空间**：$O(n+m)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<int> f(n);
    for (int i = 0; i < n; i++) scanf("%d", &f[i]);
    vector<vector<int>> g(n), rg(n);
    for (int i = 0; i < m; i++) {
        int a, b;
        scanf("%d %d", &a, &b);
        a--; b--;
        g[a].push_back(b);
        rg[b].push_back(a);
    }
    // F[v]：v 可被某个赋值状态到达，且路径中间状态都不是赋值
    vector<char> F(n, 0);
    {
        queue<int> q;
        for (int v = 0; v < n; v++)
            if (f[v] == 1) {                 // 赋值状态作为起点
                for (int u : g[v]) if (f[u] != 1) { if (!F[u]) { F[u] = 1; q.push(u); } }
            }
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (int u : g[v]) if (f[u] != 1 && !F[u]) { F[u] = 1; q.push(u); }
        }
    }
    // G[v]：从 v 出发（第一步之后中间状态都不是赋值）能到达某个使用状态
    vector<char> G(n, 0);
    {
        queue<int> q;
        for (int v = 0; v < n; v++) if (f[v] == 2) { G[v] = 1; q.push(v); }
        while (!q.empty()) {
            int v = q.front(); q.pop();
            for (int u : rg[v]) if (f[v] != 1 && !G[u]) { G[u] = 1; q.push(u); }
        }
    }
    for (int v = 0; v < n; v++) {
        bool reach = (f[v] == 1) ? true : F[v];      // 能否从赋值状态"带着值"到达
        bool use = G[v];
        printf("%d%c", (reach && use) ? 1 : 0, v + 1 == n ? '\n' : ' ');
    }
    return 0;
}
```

### Python3

```python
import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    f = [int(x) for x in data[2:2 + n]]
    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]
    p = 2 + n
    for _ in range(m):
        a = int(data[p]) - 1; b = int(data[p + 1]) - 1; p += 2
        g[a].append(b)
        rg[b].append(a)
    F = [False] * n
    q = deque()
    for v in range(n):
        if f[v] == 1:
            for u in g[v]:
                if f[u] != 1 and not F[u]:
                    F[u] = True; q.append(u)
    while q:
        v = q.popleft()
        for u in g[v]:
            if f[u] != 1 and not F[u]:
                F[u] = True; q.append(u)
    G = [False] * n
    q = deque()
    for v in range(n):
        if f[v] == 2:
            G[v] = True; q.append(v)
    while q:
        v = q.popleft()
        for u in rg[v]:
            if f[v] != 1 and not G[u]:
                G[u] = True; q.append(u)
    out = []
    for v in range(n):
        reach = True if f[v] == 1 else F[v]
        out.append("1" if (reach and G[v]) else "0")
    print(" ".join(out))


main()
```

## 7. 边界情况与易错点

1. **路径允许重复经过状态**：所以"先正向标记、再反向标记"的做法正确，不要假设路径简单。
2. **$G$ 的传播条件**：是"当前点 $v$ 非赋值"（不是前驱），因为中间点不能是赋值。
3. **赋值状态自身**：$F$ 视为真（它是起点）。
4. **过程量状态**：路径中间可以出现"使用"状态（题面只禁止赋值）✓。
5. **$m$ 可到 $10^5$**：用邻接表。
6. **自环/重边**：不影响 BFS。
7. **下标**：输入 1 基，转 0 基。
8. **输出**：$n$ 个 0/1，空格或换行分隔均可。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/164/A_变量的有效状态.md`
- **官方样例**：$3/3$ 通过。
- **独立对拍**：另写"枚举每个赋值起点、DFS 枚举长度 ≤ 2n 的所有走法（允许重复经过状态）、把经过的状态标记"的暴力，对 $200$ 组随机图（$n\le5$、$m\le7$、随机 $f$）比较，全部一致。（初版暴力用"简单路径"假设、且输入没转 0 基，两处都已在复核中修正。）
- **性能**：$n=m=10^5$ 单次约 20 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 164B Ancient Berland Hieroglyphs](https://codeforces.com/problemset/problem/164/B)：同场 B 题。
- [Codeforces 164C Machine Programming](https://codeforces.com/problemset/problem/164/C)：同场 C 题。
- [LeetCode 1971. 寻找图中是否存在路径](https://leetcode.cn/problems/find-if-path-exists-in-graph/)：可达性。

**延伸思考**：

1. **若要求路径不重复经过状态**：变成"经过某点的简单路径"问题，需 DP/流。
2. **若赋值可以在中间出现**：值会被覆盖，语义要重新定义。
3. **若要求统计路径条数**：需要计数 DP（可能有环，需矩阵/生成函数）。
