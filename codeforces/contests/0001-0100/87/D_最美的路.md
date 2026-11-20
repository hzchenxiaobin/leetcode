# Codeforces 87D 最美的路 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/87/D
- **比赛来源**：Codeforces Beta Round 73 (Div. 1 Only) · Problem D（UTC 2011-06-07）
- **难度**：2300
- **标签**：树、并查集、按权值分层、树形统计
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：$n$ 座城市由 $n-1$ 条道路连成一棵树，第 $i$ 条道路需要走 $d_i$ 天。历史上每座城市都**攻打过其他每一座城市各一次**，所以共有 $n(n-1)$ 次「有序对」$(u,v)$ 的远征（$u \ne v$）。一次从 $u$ 到 $v$ 的远征会沿着树上唯一路径走，军队在路径上**耗时最长的那条路**旁种一棵树；若路径上有并列最长的多条路，则每条都种一棵。

求：种树最多的那条路上一共种了多少棵树，以及所有达到这个数量的路的编号（升序输出）。道路按输入顺序从 1 编号。

**约束**：

- $n \le 10^5$：不能对每对城市求路径（$10^{10}$）。
- $d_i \le 10^9$：权值很大，只能排序后按权值分组处理。
- 答案最大是 $n(n-1) \approx 10^{10}$，必须用 64 位。
- 时间只有 1 s：需要近似线性的做法（排序 + 并查集 + 每层一次的树形统计）。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
2
2 1 5

输出：
2 1
1 
```

```text
输入：
6
1 2 1
1 3 5
3 4 2
3 5 3
3 6 4

输出：
16 1
2 
```

**样例 1 解释**：只有一条路（长度 5）。两次远征 $(1,2)$ 与 $(2,1)$ 的路径都只有它，各在它旁边种一棵树 → $2$ 棵，编号 1。

**样例 2 解释**：树为 $1-2(1)$、$1-3(5)$、$3-4(2)$、$3-5(3)$、$3-6(4)$。最长的路是 $1-3$（长度 5）：

- 跨过它的有序对：一端在 $\{1,2\}$、另一端在 $\{3,4,5,6\}$，共 $2 \times 4 \times 2 = 16$ 个有序对；
- 这些路径上 $1-3$ 是唯一的最长边（长度 5 是全局最大），所以它被种 16 棵树；
- 其它边（1、3、4、5 号）各自的最大值都小于 5，且路径一旦跨过 $1-3$ 就不以它们为最长边，贡献都更小。

输出 `16 1` 与 `2`，与样例一致。

**观察一（判定标准）**：对一条权值为 $w$ 的边 $e$，它是路径 $(u,v)$ 的「最长边之一」当且仅当

1. 路径经过 $e$；
2. 路径上**没有权值 $> w$ 的边**。

**观察二（分层）**：把边按权值从小到大处理。处理权值 $w$ 时，所有 $< w$ 的边已经合并成并查集的分量——这些分量正是「用 $<w$ 的边能互相到达」的极大块。把每个分量缩成一个点，权值为 $w$ 的边把这些点连成一片森林（其实是树，因为原图是树）。在缩点后的树上，一条 $w$ 边两侧的城市数 $s$ 与 $S-s$ 决定了贡献 $2s(S-s)$。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

对每个有序对 $(u,v)$ 求路径、找最大边：$O(n^2 \cdot n)$，完全不可行。即使只对每条边统计「路径经过它且它最长」的对数，也需要更聪明的批量方法。

### 3.2 算法：按权值从小到大 + 缩点树形统计

![按边权从小到大合并：每层算 2·s·(S−s)](../../../images/cf87d_dsu.svg)

1. 把 $n-1$ 条边按 $d$ 升序排序，按权值分组。
2. 维护并查集 `DSU`，初始每个城市自成一个分量；同时维护每个分量的城市数 `sz`。
3. 依次处理每一组（权值 $w$ 相同的边）：
   - 此时 `DSU` 的分量由所有权值 $< w$ 的边合并而成；
   - 选出这组里两端**属于不同分量**的边（同一分量内的 $w$ 边不可能出现在某条路径的「最长边」上，因为路径上已有更小的边连通它们……更准确地说，同分量内的边两侧不可能只靠 $<w$ 的边连通，见引理 1）；
   - 把这些边的端点分量缩成点，用这组边建图。由于原图是树，缩点后得到的是一棵（或一片）**树**，没有环；
   - 对每棵缩点树做一次迭代 DFS，求出每条 $w$ 边两侧的城市数 $s$ 与整棵树的城市总数 $S$，则该边的贡献为 $2s(S-s)$（有序对）；
   - 最后把这一组的边全部 `union`，进入下一组。
4. 取贡献的最大值，收集所有达到最大值的边编号，升序输出。

![样例 2：升序逐层合并](../../../images/cf87d_walk.svg)

### 3.3 样例 2 走查

按权值升序：$1:(1,2)$、$2:(3,4)$、$3:(3,5)$、$4:(3,6)$、$5:(1,3)$。

| 处理 | 缩点前分量 | 两侧城市数 | 贡献 | 得树的边 |
|---|---|---|---|---|
| $w=1$，边 1 | $\{1\},\{2\}$ | $1$ 与 $1$ | $2\cdot1\cdot1=2$ | 1 |
| $w=2$，边 3 | $\{3\},\{4\}$ | $1$ 与 $1$ | $2$ | 3 |
| $w=3$，边 4 | $\{3,4\},\{5\}$ | $1$ 与 $2$ | $2\cdot1\cdot2=4$ | 4 |
| $w=4$，边 5 | $\{3,4,5\},\{6\}$ | $1$ 与 $3$ | $2\cdot1\cdot3=6$ | 5 |
| $w=5$，边 2 | $\{1,2\},\{3,4,5,6\}$ | $2$ 与 $4$ | $2\cdot2\cdot4=16$ | 2 |

最大值 16，只有边 2 → 输出 `16 1` 与 `2` ✓。

## 4. 正确性证明

**引理 1（计数刻画）**：设边 $e$ 的权值为 $w$。有序对 $(u,v)$ 使 $e$ 成为路径上最长边之一，当且仅当 $u,v$ 在用「权值 $\le w$ 的边」构成的连通块中、且 $e$ 位于 $u$ 到 $v$ 的路径上（等价于 $u,v$ 在删掉 $e$ 后分处两侧）。

**证明**：路径经过 $e$ 且没有 $>w$ 的边 ⇔ 路径上所有边 $\le w$ 且经过 $e$ ⇔ $u,v$ 在「$\le w$ 边」的同一连通块内且被 $e$ 分开。∎

**引理 2（缩点后无环）**：处理权值 $w$ 时，把 $<w$ 的分量缩成点、只保留 $w$ 边，得到的图是一个森林（没有环，也没有重边）。

**证明**：原图是树。若缩点后出现环 $C$，则把 $C$ 上的每条 $w$ 边替换成它在原树中对应的边，再加上各分量内部连接这些端点的路径，就得到原树里的一个环，矛盾（树的任意子图无环）。重边同理：两条 $w$ 边连接同一对分量会与原树无环矛盾。∎

**引理 3（贡献公式）**：在缩点树中，一条 $w$ 边把树分成城市数 $s$ 与 $S-s$ 的两部分，则使该边成为最长边的有序对恰有 $2s(S-s)$ 个。

**证明**：由引理 1，这些有序对正是「一侧取 $u$、另一侧取 $v$」的有序对；一侧有 $s$ 个城市、另一侧有 $S-s$ 个，有序对数为 $s(S-s) + (S-s)s = 2s(S-s)$。∎

**定理**：按上述分层算法算出的计数就是每条边被种树的数量；取最大并列出所有达到最大值的边即为答案。

**证明**：每条边 $e$（权值 $w$）恰在「处理权值 $w$」这一层被统计一次（权值分组互不重叠）。由引理 2 该层缩点图是森林，DFS 求子树城市数正确；由引理 3 得到的就是 $e$ 被种树的数量。所有贡献都算对后，取最大值并收集并列者即可。∎

## 5. 复杂度分析

- **时间**：排序 $O(n\log n)$；每条边只属于一个权值组，缩点建图与 DFS 的总代价 $O(n)$；并查集 $O(n\alpha)$。总体 $O(n\log n)$，$n=10^5$ 实测端到端 **0.06 s**。
- **空间**：$O(n)$ 存边、并查集、缩点邻接表与临时数组，约 6 MB。
- **数值范围**：贡献最大 $n(n-1) \approx 10^{10}$，用 `long long`；$d_i \le 10^9$ 用 `long long` 排序。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
// 87D：按边权从小到大合并；同一权值的一层里，把 <w 的分量当成点，
// 求出每个 w 边两侧的城市数 s 与整棵树总数 S，贡献 2*s*(S-s)。
struct Edge { int u, v, id; long long w; };
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<Edge> es(n - 1);
    for (int i = 0; i < n - 1; i++) {
        scanf("%d %d %lld", &es[i].u, &es[i].v, &es[i].w);
        es[i].id = i;
    }
    sort(es.begin(), es.end(), [](const Edge &a, const Edge &b) { return a.w < b.w; });
    vector<int> par(n + 1), sz(n + 1, 1);
    for (int i = 1; i <= n; i++) par[i] = i;
    function<int(int)> find = [&](int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    auto unite = [&](int a, int b) { a = find(a); b = find(b); if (a == b) return; if (sz[a] < sz[b]) swap(a, b); par[b] = a; sz[a] += sz[b]; };

    vector<long long> cnt(n - 1, 0);
    int p = 0;
    while (p < n - 1) {
        int q = p;
        while (q < n - 1 && es[q].w == es[p].w) q++;
        // 只保留「跨分量」的边
        vector<Edge> g;
        for (int i = p; i < q; i++) if (find(es[i].u) != find(es[i].v)) g.push_back(es[i]);
        if (!g.empty()) {
            // 给分量编号
            unordered_map<int,int> id;
            vector<int> weight;   // 每个分量包含的城市数
            vector<vector<pair<int,int>>> adj;  // (邻居, 边在 g 中的下标)
            auto getid = [&](int r) {
                auto it = id.find(r);
                if (it != id.end()) return it->second;
                int k = (int)weight.size();
                id[r] = k;
                weight.push_back(sz[r]);
                adj.push_back({});
                return k;
            };
            for (int i = 0; i < (int)g.size(); i++) {
                int a = getid(find(g[i].u)), b = getid(find(g[i].v));
                adj[a].push_back({b, i});
                adj[b].push_back({a, i});
            }
            int K = weight.size();
            vector<char> vis(K, 0);
            vector<int> parentNode(K, -1), parentEdge(K, -1), order;
            // 每棵子树：统计总城市数 S；对每条边计算两侧城市数
            vector<long long> sub(K, 0);
            for (int s0 = 0; s0 < K; s0++) {
                if (vis[s0]) continue;
                // 迭代 DFS
                order.clear();
                vector<int> st{s0};
                vis[s0] = 1; parentNode[s0] = -1; parentEdge[s0] = -1;
                while (!st.empty()) {
                    int v = st.back(); st.pop_back();
                    order.push_back(v);
                    for (auto &e : adj[v]) {
                        if (vis[e.first]) continue;
                        vis[e.first] = 1;
                        parentNode[e.first] = v;
                        parentEdge[e.first] = e.second;
                        st.push_back(e.first);
                    }
                }
                long long S = 0;
                for (int v : order) S += weight[v];
                for (int v : order) sub[v] = weight[v];
                for (int i = (int)order.size() - 1; i >= 1; i--) {
                    int v = order[i];
                    sub[parentNode[v]] += sub[v];
                }
                for (int i = (int)order.size() - 1; i >= 0; i--) {
                    int v = order[i];
                    if (parentEdge[v] < 0) continue;
                    long long sside = sub[v];
                    cnt[g[parentEdge[v]].id] = 2LL * sside * (S - sside);
                }
            }
        }
        for (int i = p; i < q; i++) unite(es[i].u, es[i].v);
        p = q;
    }
    long long best = 0;
    for (long long v : cnt) best = max(best, v);
    vector<int> ids;
    for (int i = 0; i < n - 1; i++) if (cnt[i] == best) ids.push_back(i + 1);
    printf("%lld %d\n", best, (int)ids.size());
    for (int i = 0; i < (int)ids.size(); i++) printf("%d%c", ids[i], i + 1 == (int)ids.size() ? '\n' : ' ');
    if (ids.empty()) printf("\n");
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    es = []
    for i in range(n - 1):
        u = int(next(it)); v = int(next(it)); w = int(next(it))
        es.append((w, u, v, i))
    es.sort(key=lambda e: e[0])
    par = list(range(n + 1))
    sz = [1] * (n + 1)

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def unite(a, b):
        a, b = find(a), find(b)
        if a == b:
            return
        if sz[a] < sz[b]:
            a, b = b, a
        par[b] = a
        sz[a] += sz[b]

    cnt = [0] * (n - 1)
    p = 0
    while p < n - 1:
        q = p
        while q < n - 1 and es[q][0] == es[p][0]:
            q += 1
        g = [(w, u, v, i) for (w, u, v, i) in es[p:q] if find(u) != find(v)]
        if g:
            idx = {}
            weight = []
            adj = []

            def getid(r):
                if r in idx:
                    return idx[r]
                k = len(weight)
                idx[r] = k
                weight.append(sz[r])
                adj.append([])
                return k

            for j, (w, u, v, i) in enumerate(g):
                a, b = getid(find(u)), getid(find(v))
                adj[a].append((b, j))
                adj[b].append((a, j))
            K = len(weight)
            vis = [False] * K
            for s0 in range(K):
                if vis[s0]:
                    continue
                order = []
                st = [s0]
                vis[s0] = True
                pn = {s0: -1}
                pe = {s0: -1}
                while st:
                    v = st.pop()
                    order.append(v)
                    for (u2, j) in adj[v]:
                        if not vis[u2]:
                            vis[u2] = True
                            pn[u2] = v
                            pe[u2] = j
                            st.append(u2)
                S = sum(weight[v] for v in order)
                sub = {v: weight[v] for v in order}
                for v in reversed(order[1:]):
                    sub[pn[v]] += sub[v]
                for v in reversed(order):
                    if pe[v] < 0:
                        continue
                    ss = sub[v]
                    cnt[g[pe[v]][3]] = 2 * ss * (S - ss)
        for (w, u, v, i) in es[p:q]:
            unite(u, v)
        p = q
    best = max(cnt) if cnt else 0
    ids = [i + 1 for i in range(n - 1) if cnt[i] == best]
    sys.stdout.write(f"{best} {len(ids)}\n")
    sys.stdout.write(" ".join(map(str, ids)) + " \n")


main()
```

## 7. 边界情况与易错点

1. **必须从小到大处理**：从大到小合并会得到「用 $>w$ 的边连通」的分量，与引理 1 的判定相反，样例 2 会算成 10 而不是 16。
2. **答案要乘 2**：$(u,v)$ 与 $(v,u)$ 是两次远征，公式是 $2s(S-s)$；漏掉因子 2 会得到一半。
3. **`long long`**：最大计数 $n(n-1) \approx 10^{10}$，`int` 会溢出。
4. **同一权值的多条边**：必须**整组一起**处理（先统计、后合并），否则同权值的边会互相影响，把并列最长的边漏算。
5. **同一分量内部的边**：处理权值 $w$ 时，若一条 $w$ 边的两端已经被 $<w$ 的边连通，那么任意经过它的路径都会带上更小的边，它不可能成为「路径上的最长边之一」，贡献为 0，直接跳过；只有跨分量的 $w$ 边才进入本层的缩点树。
6. **输出格式**：第一行两个数（最大树数、达到最大的道路条数），第二行升序输出编号，每个编号后跟一个空格（样例如此）；末尾多一个空格不影响评测（按 token 比较）。
7. **$n = 2$**：只有一条边，答案 $2\times1\times1 = 2$，编号 1。
8. **权值相同且都在一条路径上**：例如三个点两条等长边，路径 $(1,3)$ 上两条边都是最长边，各得一棵树——同权值整组处理保证两条边都被统计到。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2 -Wall`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；代码可原样提交 GNU C++17），Python `3.9.6`。文档级验证：
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0001-0100/87/D_最美的路.md`
- **官方样例**：2 / 2 通过（C++ 与 Python 均输出 `2 1 / 1` 与 `16 1 / 2`）。
- **独立暴力对拍**：暴力对每个有序对 $(u,v)$（$u\ne v$）用 BFS 找回路径，求路径最大权值，再给路径上所有取到最大值的边各加一，最后取最大并列出编号——与主程序无共享逻辑。对 $n \in [2,9]$、权值 $\in [1,5]$（刻意制造大量并列）的 **300 组**随机树，主程序、Python 版、暴力**全部一致**（包括最大值的边集合）。
- **最大约束性能**：$n = 10^5$ 的链与星形两种形态、权值随机 $10^9$，C++ 端到端均为 **0.06 s**，峰值内存 5.9 MB；1 s 时限下余量充足。
- **复核状态**：verified（样例、暴力对拍、两种最坏形态性能均实跑通过）。

## 相关题目与扩展

- [Codeforces 87A Trains](https://codeforces.com/problemset/problem/87/A)、[87B Vasya and Types](https://codeforces.com/problemset/problem/87/B)、[87C Interesting Game](https://codeforces.com/problemset/problem/87/C)、[87E Mogohu-Rea Idol](https://codeforces.com/problemset/problem/87/E)：同场题目。
- [Codeforces 160D Edges in MST](https://codeforces.com/problemset/problem/160/D)：按边权分层判断边在 MST 中的状态，思路与本题高度一致。
- [Codeforces 609E Minimum spanning tree for each edge](https://codeforces.com/problemset/problem/609/E)：树上路径最大值 + 替换边，同样需要「路径最值」视角。
- [Codeforces 1108F MST Unification](https://codeforces.com/problemset/problem/1108/F)：同权值边的批处理技巧。
- [LeetCode 2846. 边权重均等查询](https://leetcode.cn/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/)：树上路径与边权统计，和本题的「路径最长边」互为镜像。

**延伸思考**：

1. **如果求「路径最短边」**：把边权从大到小处理即可，结构完全对偶。
2. **如果求「路径上恰好第 k 长的边」**：本方法失效，需要树分治或可持久化结构。
3. **如果图不是树**：路径不唯一，需要先取最小生成树或最短路树，问题语义会变。
4. **如果要求输出每棵树被种的次数**：本题已经算出每条边的计数，直接输出即可。
5. **如果把「有序对」改成「无序对」**：把所有答案除以 2 即可（因为 $2s(S-s)$ 中的 2 正是来自有序性）。
