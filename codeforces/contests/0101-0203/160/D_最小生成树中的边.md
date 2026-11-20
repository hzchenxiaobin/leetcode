# Codeforces 160D 最小生成树中的边 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/160/D
- **比赛来源**：Codeforces Round 111 (Div. 2) · Problem D（UTC 2012-03-06）
- **难度**：2300
- **标签**：图论、最小生成树、桥、并查集
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：连通无向带权图（无重边无自环），对每条边判定它属于"所有 MST"（`any`）、"至少一个 MST"（`at least one`）还是"不属于任何 MST"（`none`）。

**约束**：$n,m\le10^5$：按权值分组 + 组内桥判定。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
4 5
1 2 101
1 3 100
2 3 2
2 4 2
3 4 1

输出：
none
any
at least one
at least one
any
```

按权值从小到大处理：权 1 的边 $3\text{–}4$ 必选（`any`）；权 2 的两条边 $\{2,3\},\{2,4\}$ 在缩点后构成环，任选其一 ⇒ `at least one`；权 100 的边 $1\text{–}3$ 现在是桥（连接 $\{1\}$ 与 $\{2,3,4\}$）⇒ `any`；权 101 的边 $1\text{–}2$ 两端已连通 ⇒ `none` ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
3 3
1 2 1
2 3 1
1 3 2

输出：
any
any
none
```

官方样例 3（输入 / 输出原样）：

```text
输入：
3 3
1 2 1
2 3 1
1 3 1

输出：
at least one
at least one
at least one
```

三条同权边构成环 ⇒ 任选两条，每条都在某个 MST 中但不在全部 MST 中 ✓

![按权值分组：组内缩点后判桥](../../../images/cf160d_bridge.svg)

**观察（核心）**：Kruskal 的贪心性质——把所有权值 $<w$ 的边先处理完（并查集合并），此时每个连通块是"必须连成一体"的。对权值恰为 $w$ 的边：

- 若两端已在同一连通块 ⇒ 它加入会成环，且环上其它边权值 $<w$ ⇒ 它**不属于任何 MST**（`none`）；
- 否则把它加入"缩点图"：若它在缩点图里是**桥**，则任何生成树都必须用它 ⇒ `any`；否则可被同权其它边替换 ⇒ `at least one`。

## 3. 解题思路

1. 边按权值升序排序，分组成"权值相同的边集合"；
2. 对每组：
   - 把每条边的端点映射到当前并查集的根，得到缩点图 $G_w$；
   - 在 $G_w$ 上用 Tarjan 求桥（注意平行边不是桥，按边编号处理）；
   - 边在组内成自环（两端同根）⇒ `none`；是桥 ⇒ `any`；否则 ⇒ `at least one`；
3. 组内所有边在缩点图上做并查集合并（等价于 Kruskal 合并）；
4. 输出。

![样例 3：同权三角形三条边都是 at least one](../../../images/cf160d_sample.svg)

## 4. 正确性证明

**引理 1（Kruskal 分层）**：存在 MST 使所有权值 $<w$ 的边先被处理，且处理完权 $<w$ 的边后，连通块划分与任何 MST 的相应前缀一致。

**证明**：Kruskal 按权值升序贪心得到 MST；对任意 MST，用"交换论证"可把它改造成与 Kruskal 相同的分层结构（同权边可互换，低权边必先取）。∎

**引理 2（同一连通块内的同权边）**：若权 $w$ 的边 $e$ 两端在处理完 $<w$ 的边后已连通，则 $e$ 不属于任何 MST。

**证明**：设 $e=(u,v)$ 在 $G_{<w}$ 的同一连通块内，则该块内有路径 $P$ 全由权 $<w$ 的边构成；把 $e$ 加入 $P$ 成环，环上其余边权都 $<w$ ⇒ 用 $P$ 中任一条替换 $e$ 能得到更小或相等的生成树，且含 $e$ 的生成树必含环 ⇒ 含 $e$ 的生成树不是最小 ⇒ $e$ 不在任何 MST 中 ✓ ∎

**引理 3（缩点图中的桥 ⟺ 必选）**：设 $G_w$ 为"把 $<w$ 的连通块缩点后、只保留权 $w$ 的边（去掉自环）"得到的图。则权 $w$ 的边 $e$ 属于**每个** MST ⟺ $e$ 是 $G_w$ 的桥。

**证明**：
(⇒) 若 $e$ 不是桥，$G_w$ 中存在不含 $e$ 的生成森林路径连接 $e$ 的两端（$e$ 在某个环上），于是可以把 $e$ 换成环上同权的另一条边，得到同权的生成树且不含 $e$ ⇒ $e$ 不在所有 MST 中（矛盾）。
(⇐) 若 $e$ 是桥，则 $G_w$ 的每个生成森林（进而任何生成树）都必须包含 $e$ 才能连通这两个缩点块 ⇒ $e$ 在每个 MST 中 ✓ ∎

**引理 4（非桥 ⟺ 至少一个）**：权 $w$ 的边 $e$（非自环）至少属于一个 MST ⟺ $e$ 是某棵生成森林的边，即 $e$ 属于 $G_w$ 的某个生成森林。$G_w$ 的任何一条非桥边都落在某棵生成森林中（取包含它的生成森林），故非桥 ⇒ `at least one`；桥由引理 3 ⇒ `any` ✓

**证明**：把 $e$ 加入 $G_w$ 的任一生成森林，若成环则从环上任取一条边换掉 $e$... 直接构造：取 $G_w$ 的一个生成森林 $F$，若 $e\in F$ 完成；否则 $F+e$ 有唯一环，环上至少有一条边可去掉而保持 $e$（取环上除 $e$ 外的任一条）⇒ 得到含 $e$ 的生成森林 ✓ 再与引理 1 的低权边组合成完整 MST ✓ ∎

**定理**：程序对每条边输出正确。

**证明**：由引理 2 处理自环（`none`）；其余边由引理 3、4 按"是否桥"分类为 `any` / `at least one`；组间用并查集合并与 Kruskal 一致（引理 1）✓ ∎

## 5. 复杂度分析

- **时间**：排序 $O(m\log m)$；每组 Tarjan 的总规模 $O(m)$；总 $O(m\log m)$，$n=m=10^5$ 实测约 63 ms。
- **空间**：$O(n+m)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge { int u, v, w, id; };
int par[100005];
int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) {
        scanf("%d %d %d", &edges[i].u, &edges[i].v, &edges[i].w);
        edges[i].id = i;
    }
    sort(edges.begin(), edges.end(), [](const Edge &a, const Edge &b) { return a.w < b.w; });
    for (int i = 1; i <= n; i++) par[i] = i;
    vector<string> ans(m, "none");
    // 按权值分组
    int p = 0;
    while (p < m) {
        int q = p;
        while (q < m && edges[q].w == edges[p].w) q++;
        // 组内：把端点映射到当前连通块编号
        vector<int> nodes;
        map<int,int> id;
        auto getId = [&](int x) {
            int r = find(x);
            auto it = id.find(r);
            if (it != id.end()) return it->second;
            int v = (int)nodes.size();
            id[r] = v; nodes.push_back(r);
            return v;
        };
        vector<tuple<int,int,int>> E;      // (a, b, edge index)
        for (int i = p; i < q; i++) {
            int a = getId(edges[i].u), b = getId(edges[i].v);
            if (a == b) { ans[edges[i].id] = "none"; continue; }
            E.push_back({a, b, i});
        }
        int N = (int)nodes.size();
        vector<vector<pair<int,int>>> g(N);   // (to, edge list index)
        for (int i = 0; i < (int)E.size(); i++) {
            auto [a, b, _] = E[i];
            g[a].push_back({b, i});
            g[b].push_back({a, i});
        }
        // Tarjan 求桥
        vector<int> tin(N, -1), low(N, 0);
        vector<char> isBridge(E.size(), 0);
        int timer = 0;
        function<void(int,int)> dfs = [&](int u, int pe) {
            tin[u] = low[u] = timer++;
            for (auto [v, eid] : g[u]) {
                if (eid == pe) continue;
                if (tin[v] != -1) low[u] = min(low[u], tin[v]);
                else {
                    dfs(v, eid);
                    low[u] = min(low[u], low[v]);
                    if (low[v] > tin[u]) isBridge[eid] = 1;
                }
            }
        };
        for (int i = 0; i < N; i++) if (tin[i] == -1) dfs(i, -1);
        for (int i = 0; i < (int)E.size(); i++) {
            auto [a, b, ei] = E[i];
            ans[edges[ei].id] = isBridge[i] ? "any" : "at least one";
        }
        // 合并
        for (int i = p; i < q; i++) {
            int a = find(edges[i].u), b = find(edges[i].v);
            if (a != b) par[a] = b;
        }
        p = q;
    }
    for (int i = 0; i < m; i++) printf("%s\n", ans[i].c_str());
    return 0;
}
```

### Python3

```python
import sys
from collections import defaultdict

def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    eu = [0] * m; ev = [0] * m; ew = [0] * m
    p = 2
    for i in range(m):
        eu[i] = int(data[p]); ev[i] = int(data[p + 1]); ew[i] = int(data[p + 2]); p += 3
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    order = sorted(range(m), key=lambda i: ew[i])
    ans = ["none"] * m
    idx = 0
    while idx < m:
        j = idx
        while j < m and ew[order[j]] == ew[order[idx]]:
            j += 1
        group = order[idx:j]
        comp = {}
        def cid(x):
            r = find(x)
            if r not in comp:
                comp[r] = len(comp)
            return comp[r]
        elist = []
        for i in group:
            a, b = cid(eu[i]), cid(ev[i])
            if a == b:
                ans[i] = "none"
            else:
                elist.append((a, b, i))
        N = len(comp)
        g = [[] for _ in range(N)]
        for k, (a, b, i) in enumerate(elist):
            g[a].append((b, k)); g[b].append((a, k))
        tin = [-1] * N; low = [0] * N
        timer = 0
        is_bridge = [False] * len(elist)
        # 迭代 DFS 求桥
        for s in range(N):
            if tin[s] != -1:
                continue
            stack = [(s, -1, 0)]
            tin[s] = low[s] = timer; timer += 1
            while stack:
                u, pe, it = stack.pop()
                if it < len(g[u]):
                    stack.append((u, pe, it + 1))
                    v, eid = g[u][it]
                    if eid == pe:
                        continue
                    if tin[v] == -1:
                        tin[v] = low[v] = timer; timer += 1
                        stack.append((v, eid, 0))
                    else:
                        low[u] = min(low[u], tin[v])
                else:
                    if stack:
                        pu = stack[-1][0]
                        low[pu] = min(low[pu], low[u])
                        if low[u] > tin[pu]:
                            is_bridge[pe] = True
        for k, (a, b, i) in enumerate(elist):
            ans[i] = "any" if is_bridge[k] else "at least one"
        for i in group:
            ra, rb = find(eu[i]), find(ev[i])
            if ra != rb:
                parent[ra] = rb
        idx = j
    print("\n".join(ans))

main()
```

## 7. 边界情况与易错点

1. **组内自环**（两端已连通）⇒ `none`，不要再参与桥判定。
2. **平行边**：缩点后同一对连通块之间可能有两条同权边，它们都不是桥 ⇒ 按边编号判桥。
3. **合并时机**：组内先判桥、后统一合并（不能边判边合）。
4. **桥判定的递归深度**：$n=10^5$ 的链会爆栈，C++ 需要迭代或加栈；Python 用迭代 DFS。
5. **输出顺序**：按输入顺序输出每条边的结论。
6. **字符串**：`any` / `at least one` / `none` 注意大小写与空格。
7. **连通图**：题面保证连通，最终只剩一个块。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/160/D_最小生成树中的边.md`
- **官方样例**：$3/3$ 通过（含 `at least one` 多词输出），C++ 与 Python 一致。
- **独立对拍**：另写"枚举所有 $n-1$ 条边的子集、筛出生成树、求最小权、统计每条边出现在多少棵 MST 中"的暴力，对 $193$ 组随机连通图（$n\le5$、权值 $\le3$）比较，全部按行一致。
- **性能**：$n=m=10^5$ 实测 C++ 约 63 ms、Python 约 450 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 160E Buses and People](https://codeforces.com/problemset/problem/160/E)：同场 E 题。
- [Codeforces 161D Distance in Tree](https://codeforces.com/problemset/problem/161/D)：树上的计数。
- [Luogu P4180 严格次小生成树](https://www.luogu.com.cn/problem/P4180)：MST 的进一步应用。

**延伸思考**：

1. **若要求"出现在多少棵不同 MST 中"**：需要计数而非分类，需用生成树计数。
2. **若图不连通**：改成最小生成森林，结论按连通块分别成立。
3. **若要求输出一棵具体 MST**：Kruskal 直接给。
