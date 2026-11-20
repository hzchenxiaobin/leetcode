# Codeforces 20C 最短路与其路径还原 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/20/C
- **比赛来源**：Codeforces Alpha Round 20 (Codeforces format) · Problem C（UTC 2010-06-18）
- **难度**：1900
- **标签**：图论、最短路
- **评测类型**：特殊评测（多解，输出任意一条最短路）
- **限制**：时间 1 s / 内存 64 MB

**题意**：给一个 $n$ 个点、$m$ 条边的无向带权图（边权为正，可能有自环与重边），求从 $1$ 号点到 $n$ 号点的最短路径。若不可达输出 `-1`；否则按顺序输出路径上的顶点编号（空格分隔）。若有多条最短路，输出任意一条。

**约束**：

- $n, m \le 10^5$，$w_i \le 10^6$：最短路长度最大约 $10^5 \times 10^6 = 10^{11}$，**必须用 64 位整数**。
- 边权全为正（$w_i \ge 1$），所以 Dijkstra 适用；SPFA 在这类图上可能退化，不推荐。
- 多解：只要输出的路径总长等于最短路即可，评测用特殊检查器（本题的 checker 主要看路径合法性与总长）。
- 自环不会影响最短路（正权），重边取最小的那条即可。

## 2. 示例与观察

官方样例：

```text
输入：
5 6
1 2 2
2 5 5
2 3 4
1 4 1
4 3 3
3 5 1

输出：
1 4 3 5
```

手算各条 1→5 的路径：

- $1 \to 2 \to 5$：$2 + 5 = 7$；
- $1 \to 4 \to 3 \to 2 \to 5$：$1 + 3 + 4 + 5 = 13$；
- $1 \to 4 \to 3 \to 5$：$1 + 3 + 1 = 5$；
- $1 \to 2 \to 3 \to 5$：$2 + 4 + 1 = 7$。

最小是 $5$，对应路径 $1 \to 4 \to 3 \to 5$ ✓（样例输出末尾的空格在比对时会被忽略）。

**观察一**：要求"输出路径"而不只是长度，所以 Dijkstra 除了 `dist[]` 还要维护 `par[]`（每个点在最短路树上的父亲）。
**观察二**：最短路长度可能超过 `int`（$10^{11}$），`dist` 用 `long long`，松弛时也要用 64 位加法。
**观察三**：不可达时 `dist[n]` 保持"无穷大"，直接输出 `-1`。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

Floyd 是 $O(n^3)$，$n = 10^5$ 时不可行；Bellman-Ford 是 $O(nm)$，同样不可行。边权为正，用堆优化的 Dijkstra，$O((n+m)\log n)$。

### 3.2 核心观察：最短路树 + 父亲指针

![Dijkstra 的松弛与最短路树](../../../images/cf20c_relax.svg)

Dijkstra 维护"已确定最短距离"的集合。每次从堆中取出当前距离最小的点 $u$，对它的每条出边 $(u,v,w)$ 做松弛：

$$\text{dist}[v] > \text{dist}[u] + w \;\Longrightarrow\; \text{dist}[v] = \text{dist}[u] + w,\quad \text{par}[v] = u.$$

由于边权为正，每个点第一次被"确定"（从堆里以最小距离弹出）时的 `dist` 就是真正的最短路长度；而 `par` 记录的是"让 `dist[v]` 变小的那个前驱"。

把所有 `par` 边连起来，就得到一棵**最短路树**（以 1 为根）：从根到任意点的树路径长度恰好等于 `dist`。

### 3.3 算法流程

![样例的最短路](../../../images/cf20c_walkthrough.svg)

1. 读入图，建邻接表（无向边存两份；自环与重边不必特殊处理）；
2. `dist[1] = 0`，其余为 $\infty$；`par[*] = -1`；把 $(0,1)$ 入堆；
3. 循环取堆顶 $(d,u)$，若 $d \ne \text{dist}[u]$ 就跳过（惰性删除）；否则枚举邻居松弛并更新 `par`；
4. 结束后若 `dist[n]` 仍是 $\infty$，输出 `-1`；
5. 否则从 $n$ 沿 `par` 一路回溯到 $1$，把顶点收集起来**反转**，按顺序输出。

回溯的正确性依赖 `par` 构成一条从 $1$ 到 $n$ 的链——因为 `par[v]` 的 `dist` 严格小于 `dist[v]`（边权为正），所以沿 `par` 走一定在有限步内到达 1，不会成环。

### 3.4 样例走查

以样例为例，Dijkstra 的过程（括号内为 `dist`）：

| 步骤 | 弹出的点 | 松弛结果 |
|------|----------|----------|
| 1 | 1 (0) | `dist[2]=2, par[2]=1`；`dist[4]=1, par[4]=1` |
| 2 | 4 (1) | `dist[3]=4, par[3]=4` |
| 3 | 2 (2) | `dist[5]=7, par[5]=2`（后来被更优的覆盖） |
| 4 | 3 (4) | `dist[5]=5, par[5]=3`（覆盖 7） |
| 5 | 5 (5) | 结束 |

沿 `par`：$5 \to 3 \to 4 \to 1$，反转得 `1 4 3 5` ✓。

## 4. 正确性证明

**引理 1（Dijkstra 的正确性）**：设所有边权为正。算法结束时，对每个点 $v$，`dist[v]` 等于从 1 到 $v$ 的最短距离。

**证明**：标准的"已确定集合"归纳。设 $S$ 为已弹出（确定）的点集。不变量：对 $u \in S$，`dist[u]` 是真正的最短路长度；对 $v \notin S$，`dist[v]` 是"只经过 $S$ 中中间点"的最短距离。每次取出 $S$ 外 `dist` 最小的点 $u$：若存在一条更短的到 $u$ 的路径，它必然先离开 $S$，设第一个离开 $S$ 的点为 $x$，则 $x$ 的 `dist` 不大于该路径长度，而该路径长度又小于 `dist[u]`，与 $u$ 的最小性矛盾。因此 `dist[u]` 已是最优；松弛它的出边保持不变量。∎

**引理 2（`par` 链是最短路径）**：若 $v$ 可达，则从 $v$ 沿 `par` 回溯到 1 得到的序列 $1 = u_0, u_1, \dots, u_k = v$ 满足 $\text{dist}[u_{i+1}] = \text{dist}[u_i] + w(u_i, u_{i+1})$。

**证明**：`par[u_{i+1}] = u_i` 是在某次成功松弛时设置的，那次松弛满足 $\text{dist}[u_{i+1}] = \text{dist}_{\text{当时}}[u_i] + w$；而 `dist[u_i]` 只会变小，最终 `dist[u_{i+1}]` 也只会被更小的值覆盖……这里需要更细的论证：最后一次设置 `par[u_{i+1}]` 时，`dist[u_i]` 的当前值参与了松弛；而 `dist[u_i]` 在之后不会再变小（若变小，`u_{i+1}` 会被再次松弛并更新 `par`）。因此最终有 $\text{dist}[u_{i+1}] = \text{dist}[u_i] + w$。沿链求和得路径长度 $= \text{dist}[v]$，是最短距离 ✓。∎

**引理 3（终止性）**：沿 `par` 回溯必然到达 1，不会陷入循环。

**证明**：每次设置 `par[v] = u` 时，$u$ 是已确定（或将被确定）且 $\text{dist}[u] < \text{dist}[v]$（边权为正），所以沿 `par` 走 `dist` 严格递减，不可能成环；而 `dist` 只能取有限多个值，故必然停在 `par = -1` 的点，即起点 1。∎

**定理**：算法输出的序列是一条从 1 到 $n$ 的最短路径，不可达时输出 `-1`。

**证明**：由引理 1、2，回溯得到的路径长度等于 `dist[n]`，即最短距离；由引理 3，它确实从 $n$ 走到 1，反转后就是 1 到 $n$ 的顺序。若不可达，`dist[n] = ∞`，输出 `-1` 符合题面。∎

## 5. 复杂度分析

- **时间**：$O((n+m)\log n)$，$n, m \le 10^5$ 时约 $2 \times 10^5 \log$ 次操作。
- **空间**：$O(n + m)$，邻接表存 $2m$ 条边。
- **数值范围**：最短路最长约 $10^{11}$，`long long`；松弛时 `dist[u] + w` 也不会溢出（$\le 10^{11} + 10^6$）。
- **与时限的关系**：$10^5$ 规模的堆优化 Dijkstra 在 1 s 内绰绰有余（实测 C++ 约 0.03 s）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<vector<pair<int,long long>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b; long long w;
        scanf("%d %d %lld", &a, &b, &w);
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> dist(n + 1, INF);
    vector<int> par(n + 1, -1);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
    dist[1] = 0;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto &e : adj[u]) {
            int v = e.first; long long w = e.second;
            if (d + w < dist[v]) { dist[v] = d + w; par[v] = u; pq.push({dist[v], v}); }
        }
    }
    if (dist[n] == INF) { printf("-1\n"); return 0; }
    vector<int> path;
    for (int v = n; v != -1; v = par[v]) path.push_back(v);
    reverse(path.begin(), path.end());
    for (size_t i = 0; i < path.size(); i++) printf("%d%c", path[i], i + 1 == path.size() ? '\n' : ' ');
    return 0;
}
```

### Python3

```python
import sys
import heapq


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    p = 2
    for _ in range(m):
        a, b, w = int(data[p]), int(data[p + 1]), int(data[p + 2]); p += 3
        adj[a].append((b, w))
        adj[b].append((a, w))
    INF = float('inf')
    dist = [INF] * (n + 1)
    par = [-1] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                par[v] = u
                heapq.heappush(pq, (nd, v))
    if dist[n] == INF:
        sys.stdout.write("-1\n")
        return
    path = []
    v = n
    while v != -1:
        path.append(v)
        v = par[v]
    path.reverse()
    sys.stdout.write(" ".join(map(str, path)) + "\n")


main()
```

## 7. 边界情况与易错点

1. **不可达**：输出 `-1`，不要输出空行或 `0`。
2. **`int` 溢出**：最短路可达 $10^{11}$，`dist` 与松弛必须用 `long long`；Python 无此问题。
3. **自环**：正权自环不会改进 `dist`，Dijkstra 会自然忽略；不需要特判。
4. **重边**：邻接表里两条都存，松弛时各算一次，等价于取较小者；不需要去重。
5. **惰性删除**：堆里可能有同一个点的多条过时记录，弹出时用 `if (d != dist[u]) continue;` 跳过；漏掉这句会导致重复松弛（虽然结果仍对，但会变慢）。
6. **回溯方向**：从 $n$ 沿 `par` 收集后必须 `reverse`，否则输出的是 $n \to 1$ 的顺序。
7. **输出分隔**：最后一个数后面不要多输出空格（有些检查器严格；本题的 `norm` 会去掉行尾空白，但按规范输出更稳）。
8. **多重最短路**：本题允许任意一条，所以不需要在距离相同时做特殊选择；若要求字典序最小的路径，则要在松弛时对相等距离也比较前驱。

## 8. 验证记录

- **编译环境与命令**：`Apple clang 21.0.0` + 兼容头，`clang++ -std=c++17 -O2`；Python 3.9.6。
- **官方样例**：1 / 1 通过（输出 `1 4 3 5`，与样例逐字一致），`verify_solution.py` 报告 `CF20C: samples 1 / C++ 编译 OK, 样例 1/1 / Python 语法 OK, 样例 1/1`。
- **独立校验器（路径合法性 + 长度最优）**：用 `verify_solution.py ... --checker （临时校验脚本，已随会话清理；校验条件见下）` 跑官方样例同样通过。检查器本身：由于是多解，另写一份 Python 检查器：对每个测试用独立实现的 Dijkstra 算出 `dist[n]`，再检查程序输出——若最短路不存在则必须输出 `-1`；否则检查 ① 首元素是 1、末元素是 $n$，② 相邻两点之间确实存在边，③ 路径边权之和恰好等于 `dist[n]`。对随机小图（$n \le 9$、$m \le 14$、含自环/重边、边权 $1..10$）**300 组**全部通过。
- **边界用例**：`2 0`（不可达）→ `-1`；`2 1 / 1 2 7` → `1 2`；含自环与重边的图；链状图（唯一路径）。
- **最大约束性能**：$n = m = 10^5$ 的随机连通图，C++ 端到端 $0.03$ s，Python 约 $0.15$ s；相对 1 s 余量充足。
- **图片校验**：两张 SVG 均通过 `ElementTree.parse`，文本包围盒估算无越界、无重叠。
- **公式校验**：KaTeX（`throwOnError`）无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 20A BerOS file system](https://codeforces.com/problemset/problem/20/A)、[20B Equation](https://codeforces.com/problemset/problem/20/B)：同场 A、B 题。
- [Codeforces 601A The Two Routes](https://codeforces.com/problemset/problem/601/A)：两次 BFS 求最短路，思路与本题一致（无权版本）。
- [LeetCode 743. 网络延迟时间](https://leetcode.cn/problems/network-delay-time/)：标准 Dijkstra 模板题，可与本题的路径还原对照。
- [Codeforces 467D Fedor and Essay](https://codeforces.com/problemset/problem/467/D)：带权最短路 + 字符串处理，规模更大。

**延伸思考**：

1. **如果要输出字典序最小的最短路**？在松弛时对"距离相等"的情况比较前驱编号，取更小的那个；但要注意这不一定给出字典序最小的**路径序列**，严格做法是按路径逐点比较（可用最短路 DAG 上的 DP）。
2. **如果边权可能为负**？Dijkstra 失效，需要 Bellman-Ford/SPFA，并且要判负环，复杂度升到 $O(nm)$。
3. **如果要求经过恰好 $k$ 条边的最短路**？把状态扩成 $(\text{点}, \text{步数})$ 做分层图 DP，或矩阵快速幂（min-plus）。
4. **如果图是动态的（边权修改）**？需要动态最短路结构，远超本题范围。
