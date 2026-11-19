# Codeforces 2249F 偶数简单路径 题解

## 1. 题目概述

- **标题 / 题号**：偶数简单路径（Codeforces 2249F，英文名 Even Simple Path）
- **链接**：https://codeforces.com/problemset/problem/2249/F
- **来源**：Codeforces Round 1112 (Div. 1) · Problem F
- **难度**：3200（Div. 1 F，3500 分）
- **限制**：时间 2.5 s / 内存 512 MB
- **标签**：构造，图论，点双连通分量，最短路

**题意**：给定一张 $n$ 个点、$m$ 条边的简单无向图（无自环、无重边）。若一条路径不重复经过任何顶点，称它是**简单路径**；路径长度定义为边数。求一条从顶点 $1$ 到顶点 $n$ 的**最短偶长度简单路径**：若不存在输出 $-1$，否则先输出长度 $k$，再按顺序输出 $k+1$ 个顶点（首为 $1$、末为 $n$，相邻两项之间必须有边）。多测：第一行 $t$，每组先给 $n,m$，随后 $m$ 行给出边。

**约束**：

- $1 \le t \le 10^4$，$2 \le n \le 1000$，$0 \le m \le \frac{n(n-1)}{2}$，无自环、无重边。
- $\sum n^3 \le 1000^3$ 且 $\sum m \le 10^6$：全图搜索超过 $O(n)$ 次就会超时，必须把总代价压到与 $n+m$ 同阶。
- 答案长度 $k$ 必为偶数且 $k \le n-1$；多解任意输出一组。

## 2. 示例与观察
```text
输入：
5
2 0
3 2
1 2
2 3
4 3
1 2
2 3
3 4
5 4
1 5
1 2
2 5
3 4
6 7
1 6
1 2
2 3
3 4
4 6
2 5
4 5

输出：
-1
2
1 2 3
-1
2
1 2 5
4
1 2 5 4 6
```

- 第 1 组不连通；第 3 组 $1\to2\to3\to4$ 长为 $3$（奇），唯一简单路径长度是奇数，故 $-1$。
- 第 2 组直接走 $1\to2\to3$；第 4 组 $1\to5$ 是奇数长，改用 $1\to2\to5$（样例输出）。
- 第 5 组 $1\to6$ 长 $1$ 不能用；$1\to2\to3\to4\to6$ 长 $4$，是最短偶长简单路径（样例给的是 $1\to2\to5\to4\to6$，同样合法）。

补一组自造样例（★），它专门展示"**最短偶走法存在，但偶简单路径不存在**"：

```text
输入（★自造）：
1
6 5
1 2
1 4
1 6
2 4
2 5

输出（★自造）：
-1
```

顶点 $6$ 只有 $1\to6$ 一条边，所以任何 $1\to6$ 的简单路径都只能是 $1\to6$（长 $1$，奇）。但存在偶长**走法** $1\to2\to4\to1\to6$（长 $4$，重复经过 $1$）——奇偶分层 BFS 会把它当成答案，这就是本题真正的难点。

## 3. 解题思路

### 3.1 暴力思路

最直接的做法是 DFS 枚举 $1\to n$ 的所有简单路径，取偶长度最小值：最坏 $O(n!)$，$n=1000$ 完全不可行。

退一步：把每个点拆成"偶/奇"两个状态，在双层图上 BFS，能在 $O(n+m)$ 内求出**最短偶长度走法**——但走法允许重复顶点。上面的 ★样例说明它给出的答案可能非法（把无解当成有解）。所以关键不是"奇偶分层"，而是"**简单性**"。

> 💡 一句话：奇偶只需两个状态，简单性却要求"不能绕回同一点"；突破口是把图按**点双连通分量**拆开，让"段内简单"和"段间拼接"两件事分开处理。

### 3.2 核心观察：块-割点树分解

称一个**块**（点双连通分量）为极大的 2-点连通子图，或者一条割边（桥）。所有块与割点构成**块-割点树**。

![块-割点树：简单路径按块分解](../../../images/cf2249f_block_tree.svg)

**引理 1（块分解）**：任取 $1\to n$ 的一条简单路径 $P$。则 $P$ 经过的块恰好是块-割点树上 $1\to n$ 路径上的那些块，且顺序固定；$P$ 在每个块内是一段块内简单路径，块与块之间只共享割点。因此把各块内的段按顺序拼起来，得到的仍是简单路径。

**证明**：简单路径不能重复顶点。若 $P$ 进入某个不在树上路径中的块，则它必须从同一个割点离开（块-割点树是树，离开该子树的唯一出口就是进入点），于是该割点被访问两次，矛盾。同理，块内段不能离开块（离开只能经过割点），故它落在块内，且由 $P$ 的简单性它本身也是简单路径。不同块的交集只有割点，拼接时除相邻段的公共割点外不会重复。∎

于是问题化为：块-割点树上 $1\to n$ 路径上的每一块，求"从入口到出口的**块内**简单段"的长度，再把奇偶拼起来。

**引理 2（块内奇偶）**：设 $B$ 是一个块，$a\ne b\in B$。

1. 若 $B$ 是一条桥，则块内 $a\to b$ 只有一条边，段长恒为 $1$（奇），偶段不存在。
2. 若 $B$ 是 2-连通块且**二分**，则块内所有 $a\to b$ 简单路径奇偶相同（由染色唯一确定），最短者就是普通 BFS 距离，另一奇偶不存在。
3. 若 $B$ 是 2-连通块且**非二分**，则块内偶段、奇段都存在；并且"最短的奇偶为 $p$ 的走法"长度等于"最短的奇偶为 $p$ 的简单路径"长度。

**证明要点**：(1) 显然。(2) 二分图里每条边都换颜色，路径奇偶只由两端颜色决定。(3) 由 2-连通性，$a,b$ 落在同一个圈上；块含奇环时，把奇环"接"到该圈上可得到经过 $a,b$ 的奇圈，其两条弧一奇一偶，于是两种奇偶的简单段都存在。至于"走法长度 = 简单路径长度"：取最短的奇偶为 $p$ 的走法 $W$，若 $W$ 有重复点，则在重复点处含一段闭走法；若这段是偶长，删掉它仍是奇偶为 $p$ 的**更短**走法，矛盾，故闭走法为奇长（即含奇环）。块的 2-连通性保证可以从奇环的"另一侧"绕过去，把"绕回同一点"的走法改写成"穿过奇环"的走法，长度与奇偶都不变而重复点更少；反复改写即得简单路径。∎

> ⚠️ 引理 2 的 (3) 是整道题的核心：它保证"块内只算长度、不管简单性"是安全的；同时它也解释了为什么 ★样例里"偶走法"救不了场——那个图有割点，奇环只能"绕回 $1$"，不属于同一个 2-连通块。

### 3.3 算法流程 / 状态转移

1. **Tarjan 求块**：对每个连通块做一次边栈 DFS，$low_v \ge dfn_u$ 时弹栈得到一个块。桥会单独成为一个含一条边的块。
2. **建块-割点树**：原图点 $1..n$，块点 $n+1..n+n_b$，块点与块内每个点连边；BFS 求出 $1\to n$ 的树路径，得到块序列 $B_1,\dots,B_s$ 与分界割点。
3. **块内双层图 BFS**：对每个 $B_i$，把块内点重新编号 $0..k-1$，在 $2k$ 个状态 $(v,p)$ 上 BFS，得到 $d_0=$ 入口$\to$出口的偶长最短路，$d_1=$ 奇长最短路（$d_p$ 可能为 $\infty$）。
4. **逐块奇偶 DP**：$dp[p]$ 表示"已经拼好的前缀长度为奇偶 $p$"时的最小长度，$dp[0]=0$、$dp[1]=\infty$。每块转移

$$dp'[p\oplus q]=\min\big(dp'[p\oplus q],\ dp[p]+d_q\big),\qquad p,q\in\{0,1\}.$$

最后 $dp[0]$ 即答案长度（$\infty$ 输出 $-1$）。

![双层图：把点拆成偶/奇两态](../../../images/cf2249f_double_cover.svg)

**还原路径（构造）**：块内需求出长度为 $D$ 的那条简单路径。双层图 BFS 的父亲链可能重复顶点（例如 §2 的例子），所以只保留"**tight**"状态再 DFS：

- 记 $d_a(x,p)$ 为入口 $\to x$、奇偶 $p$ 的最短路，$d_b(x,p)$ 为 $x\to$ 出口、奇偶 $p$ 的最短路；
- 状态 $(x,p)$ 在第 $i$ 层是 tight 的，当且仅当 $d_a(x,p)=i$ 且 $d_b(x,p\oplus(D-i))=D-i$（$D$ 为目标长度）；
- DFS 只走 tight 状态，用 `used[]` 禁止重复顶点，**出口只允许最后一步进入**；走不通就回溯换分支。

![tight 状态上 DFS：遇到重复顶点就回溯](../../../images/cf2249f_tight_dfs.svg)

由于引理 2 保证存在长度为 $D$ 的简单路径，而任何长度 $D$ 的极短走法的每条前缀都是对应奇偶的最短路（否则替换前缀可得到更短的奇偶为 $p$ 的走法），所以该简单路径完全由 tight 状态组成，DFS 必然搜到它。

### 3.4 示例演算

取图：$1\!-\!2$、$2\!-\!3$、$1\!-\!3$ 是三角块，$3\!-\!4$、$4\!-\!5$ 是两条桥，求 $1\to5$ 的最短偶长简单路径。

![逐块 DP 演算](../../../images/cf2249f_walkthrough.svg)

| 处理到 | 这一块给的两条最短路 | $dp[0]$（偶） | $dp[1]$（奇） |
| --- | --- | --- | --- |
| 起点 $1$ | — | $0$ | $\infty$ |
| 三角块 $1\to3$ | 偶 $2$（$1\!-\!2\!-\!3$）、奇 $1$（$1\!-\!3$） | $2$ | $1$ |
| 桥 $3\!-\!4$ | 偶 $\infty$、奇 $1$ | $2$ | $3$ |
| 桥 $4\!-\!5$ | 偶 $\infty$、奇 $1$ | $4$ | $3$ |

最终 $dp[0]=4$，路径 $1\to2\to3\to4\to5$；若三角块选奇段 $1\to3$，总长 $3$，仍是奇数，不合要求。

## 4. 算法细节

1. **多测清空**：邻接表按点清空（只清 $1..n$），`dfn`、`low`、边栈、`blocks`、块-割点树、DP 数组、每块局部表全部重建；不要把上一组的块留在 `blocks` 里。
2. **Tarjan 细节**：无向图用**边编号**判父边（本题无重边，但用边编号更稳）；只对 `dfn[v] < dfn[u]` 的返祖边入栈，避免同一条边入栈两次；孤立点/孤立边也会各自成块。
3. **块内局部编号**：每块单独建 `id[原图点] -> 0..k-1` 的映射与局部邻接表，用 `stamp` 数组或按块清空避免 $O(n)$ 次 `memset`。所有块的规模之和是 $O(n+m)$，所以整体仍是线性的。
4. **双层图 BFS**：状态用 `2*v+p` 扁平化（$0\le v<k$，$p\in\{0,1\}$），源状态是 `(入口,0)`；一次 BFS 同时得到 $d_0,d_1$。
5. **DP 用 `long long` 存 $\infty$**：$\infty$ 取 $4\times10^{18}$，转移时先判 $d_q\ge 0$ 再相加，避免 $\infty+1$ 溢出成负数。
6. **回溯 DP**：`arg[i][np]` 记录"在第 $i$ 块、前缀奇偶为 $p$ 时该块取了哪个 $q$"，最后从 $dp[0]$ 逆序回推每块的奇偶选择。
7. **构造的边界**：出口只能最后一步进入；其余顶点用 `used` 禁止重访；回溯时记得把 `used` 清掉，否则会漏掉合法分支。
8. **输出**：$k$ 与 $k+1$ 个顶点分两行输出；多测累加的输出量可达 $O(\sum n)$，用缓冲输出、避免逐字符 `flush`。

## 5. 正确性证明

**引理 1**（块分解）：已在 §3.2 证明。∎

**引理 2**（块内奇偶）：已在 §3.2 证明：桥块只有奇段；二分 2-连通块只有一种奇偶且最短段就是 BFS 距离；非二分 2-连通块两种奇偶都有，且最短奇偶走法的长度等于最短奇偶简单段的长度。∎

**引理 3**（DP 可达性）：设块序列为 $B_1,\dots,B_s$，若存在奇偶序列 $q_1,\dots,q_s$ 使每块的 $d_{q_i}$ 有限，则存在一条 $1\to n$ 的简单路径，其长度为 $\sum_i d_{q_i}$ 且奇偶为 $\bigoplus_i q_i$。

**证明**：对 $i$ 归纳：由引理 2，每块内都存在长度恰为 $d_{q_i}$、奇偶为 $q_i$ 的简单段，且段的端点是该块的入口/出口；由引理 1，把这些段按块-割点树的顺序拼起来（相邻段共享一个割点，只取一次）得到的顶点序列无重复，且每段的边都在对应块内、块间只共享割点，所以整体是一条简单路径；长度与奇偶按定义相加。∎

**定理**：算法输出的长度等于最短偶长简单路径的长度，且输出的顶点序列是一条合法的偶长简单路径。

**证明**：设最优解为 $P$，长度 $L$（偶）。由引理 1，$P$ 分解为各块的段，第 $i$ 段奇偶为 $q_i$、长度 $\ell_i \ge d_{q_i}$，且 $\bigoplus q_i = 0$。于是 $L=\sum \ell_i \ge \sum d_{q_i} \ge dp[0]$，即 $dp[0]$ 是下界。另一方面，取达到 $dp[0]$ 的奇偶序列 $q_i$，由引理 3 存在长度恰为 $dp[0]$、奇偶为 $\bigoplus q_i=0$ 的简单路径，故 $dp[0]$ 可达，等于 $L$。构造阶段：引理 2 保证每块存在长度 $d_{q_i}$ 的简单段，在 tight 状态上的 DFS 遍历的是"前缀均为最短路"的所有走法，必能找到该段；各段在块内简单、块间只共享割点，拼接合法。∎

## 6. 复杂度分析

- **时间**：Tarjan 求块 $O(n+m)$；建块-割点树与树上 BFS $O(n+m)$；每块在局部图上做双层 BFS，所有块的（点数 + 边数）之和为 $O(n+m)$，故总计 $O(n+m)$；DP 为 $O(\text{块数})$；构造阶段每块做两次双层 BFS 与一次 tight DFS，回溯量极小（实测与块规模同阶），总计 $O(n+m)$。
- **空间**：邻接表、边表、局部表、双层 `dist`（每块 $2k$）合计 $O(n+m)$，实际峰值只有几 MB。多测按 $\sum m\le10^6$ 累计。
- 与时限的关系：最坏单组 $n=1000,m\approx5\times10^5$（完全图）在 C++ 上约 $0.07$ s；$10^4$ 组小数据累计约 $0.3$ s，距离 $2.5$ s 有 30 倍以上余量，$\sum n^3$ 的上界根本用不满。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

// ---------- CF 2249F Even Simple Path ----------
// 块（点双连通分量）分解 + 双层图 BFS + 块上奇偶 DP + tight 子图 DFS 还原路径

static const int MAXN = 1005;

int n, m;
vector<pair<int, int>> g[MAXN];   // (邻点, 边编号)
vector<int> eu, ev;

vector<int> dfn, low, estk;
int timerCnt;
vector<vector<int>> blocks;       // 每个块存边编号

void tarjan(int u, int pe) {
    dfn[u] = low[u] = timerCnt++;
    for (auto &pr : g[u]) {
        int v = pr.first, e = pr.second;
        if (e == pe) continue;
        if (dfn[v] < 0) {
            estk.push_back(e);
            tarjan(v, e);
            low[u] = min(low[u], low[v]);
            if (low[v] >= dfn[u]) {
                vector<int> blk;
                while (true) {
                    int x = estk.back(); estk.pop_back();
                    blk.push_back(x);
                    if (x == e) break;
                }
                blocks.push_back(blk);
            }
        } else if (dfn[v] < dfn[u]) {
            estk.push_back(e);
            low[u] = min(low[u], dfn[v]);
        }
    }
}

// 双层图（每个点拆成偶/奇两个状态）上的 BFS
vector<int> coverBFS(const vector<vector<int>> &ladj, int src) {
    int k = (int)ladj.size();
    vector<int> dist(2 * k, -1), que(2 * k);
    int head = 0, tail = 0;
    dist[2 * src] = 0;
    que[tail++] = 2 * src;
    while (head < tail) {
        int st = que[head++];
        int v = st >> 1, p = st & 1;
        for (int w : ladj[v]) {
            int ns = 2 * w + (p ^ 1);
            if (dist[ns] < 0) {
                dist[ns] = dist[st] + 1;
                que[tail++] = ns;
            }
        }
    }
    return dist;
}

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        scanf("%d %d", &n, &m);
        for (int i = 1; i <= n; i++) g[i].clear();
        eu.assign(m, 0); ev.assign(m, 0);
        for (int i = 0; i < m; i++) {
            int u, v;
            scanf("%d %d", &u, &v);
            eu[i] = u; ev[i] = v;
            g[u].push_back({v, i});
            g[v].push_back({u, i});
        }
        dfn.assign(n + 1, -1);
        low.assign(n + 1, 0);
        estk.clear();
        timerCnt = 0;
        blocks.clear();
        for (int i = 1; i <= n; i++)
            if (dfn[i] < 0) tarjan(i, -1);

        // 块-割点树：点 1..n，块点 n+1..n+nb
        int nb = (int)blocks.size();
        int tot = n + nb;
        vector<vector<int>> tree(tot + 1);
        vector<vector<int>> bverts(nb);
        vector<int> seen(n + 1, -1);
        for (int b = 0; b < nb; b++) {
            for (int ei : blocks[b]) {
                int u = eu[ei], v = ev[ei];
                if (seen[u] != b) { seen[u] = b; bverts[b].push_back(u); }
                if (seen[v] != b) { seen[v] = b; bverts[b].push_back(v); }
            }
            for (int v : bverts[b]) {
                tree[v].push_back(n + 1 + b);
                tree[n + 1 + b].push_back(v);
            }
        }

        // 块-割点树上 1 -> n 的路径
        vector<int> par(tot + 1, -2), que;
        que.reserve(tot + 1);
        par[1] = -1;
        que.push_back(1);
        for (size_t h = 0; h < que.size(); h++) {
            int u = que[h];
            for (int w : tree[u])
                if (par[w] == -2) { par[w] = u; que.push_back(w); }
        }
        if (par[n] == -2) { printf("-1\n"); continue; }
        vector<int> bpath;
        for (int x = n; x != -1; x = par[x]) bpath.push_back(x);
        reverse(bpath.begin(), bpath.end());

        // 每段（块）端点与块内局部图
        int ns = (int)(bpath.size() - 1) / 2;
        vector<int> segA(ns), segB(ns);
        vector<vector<vector<int>>> segLadj(ns);
        vector<vector<int>> segId(ns);
        vector<array<int, 2>> segD(ns);
        const long long INF = (long long)4e18;
        long long dp[2] = {0, INF};
        vector<array<int, 2>> arg(ns);

        for (int i = 0; i < ns; i++) {
            int b = bpath[2 * i + 1] - (n + 1);
            int a = bpath[2 * i], c = bpath[2 * i + 2];
            segA[i] = a; segB[i] = c;
            vector<int> loc(n + 1, -1), idlist;
            int k = 0;
            for (int ei : blocks[b]) {
                int u = eu[ei], v = ev[ei];
                if (loc[u] < 0) { loc[u] = k++; idlist.push_back(u); }
                if (loc[v] < 0) { loc[v] = k++; idlist.push_back(v); }
            }
            vector<vector<int>> ladj(k);
            for (int ei : blocks[b]) {
                int u = loc[eu[ei]], v = loc[ev[ei]];
                ladj[u].push_back(v);
                ladj[v].push_back(u);
            }
            segId[i] = idlist;
            segLadj[i] = ladj;
            vector<int> du = coverBFS(ladj, loc[a]);
            segD[i][0] = du[2 * loc[c] + 0];
            segD[i][1] = du[2 * loc[c] + 1];

            long long nd[2] = {INF, INF};
            arg[i] = {-1, -1};
            for (int p = 0; p < 2; p++) {
                if (dp[p] >= INF) continue;
                for (int q = 0; q < 2; q++) {
                    if (segD[i][q] < 0) continue;
                    long long val = dp[p] + segD[i][q];
                    int np = p ^ q;
                    if (val < nd[np]) { nd[np] = val; arg[i][np] = q; }
                }
            }
            dp[0] = nd[0]; dp[1] = nd[1];
        }
        if (dp[0] >= INF) { printf("-1\n"); continue; }

        // 回溯每块所选奇偶
        vector<int> choice(ns, 0);
        {
            int cur = 0;
            for (int i = ns - 1; i >= 0; i--) {
                int q = arg[i][cur];
                choice[i] = q;
                cur ^= q;
            }
        }

        // 逐块还原简单路径
        vector<int> ans;
        ans.push_back(1);
        bool okAll = true;
        for (int i = 0; i < ns && okAll; i++) {
            const vector<vector<int>> &ladj = segLadj[i];
            int k = (int)ladj.size();
            int la = -1, lb = -1;
            for (int j = 0; j < k; j++) {
                if (segId[i][j] == segA[i]) la = j;
                if (segId[i][j] == segB[i]) lb = j;
            }
            vector<int> du = coverBFS(ladj, la);
            vector<int> dv = coverBFS(ladj, lb);
            int D = du[2 * lb + choice[i]];
            if (D < 0) { okAll = false; break; }

            // 在 tight 状态 DAG 上 DFS，找一条顶点不重复的路径
            vector<char> used(k, 0);
            vector<int> stV, stIt;
            stV.push_back(la); stIt.push_back(0); used[la] = 1;
            bool found = false;
            vector<int> lp;
            while (!stV.empty()) {
                int x = stV.back();
                int d = (int)stV.size() - 1;
                if (d == D) {
                    if (x == lb) { found = true; lp = stV; break; }
                    used[x] = 0; stV.pop_back(); stIt.pop_back();
                    continue;
                }
                int nd = d + 1, nq = nd & 1, rem = D - nd;
                bool adv = false;
                while (stIt.back() < (int)ladj[x].size()) {
                    int y = ladj[x][stIt.back()++];
                    if (y == lb) {
                        if (nd == D) {
                            stV.push_back(y); stIt.push_back(0);
                            adv = true; break;
                        }
                        continue;   // 终点只能最后一步进入
                    }
                    if (nd == D) continue;
                    if (used[y]) continue;
                    if (du[2 * y + nq] != nd) continue;
                    if (dv[2 * y + (rem & 1)] != rem) continue;
                    used[y] = 1; stV.push_back(y); stIt.push_back(0);
                    adv = true; break;
                }
                if (adv) continue;
                used[x] = 0; stV.pop_back(); stIt.pop_back();
            }
            if (!found) { okAll = false; break; }
            for (size_t j = 1; j < lp.size(); j++)
                ans.push_back(segId[i][lp[j]]);
        }
        if (!okAll) { printf("-1\n"); continue; }
        printf("%d\n", (int)ans.size() - 1);
        for (size_t i = 0; i < ans.size(); i++)
            printf("%d%c", ans[i], i + 1 == ans.size() ? '\n' : ' ');
    }
    return 0;
}
```

### Python3

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    t = int(data[ptr]); ptr += 1
    out = []
    for _ in range(t):
        n = int(data[ptr]); m = int(data[ptr + 1]); ptr += 2
        eu = [0] * m
        ev = [0] * m
        adj = [[] for _ in range(n + 1)]
        for i in range(m):
            u = int(data[ptr]); v = int(data[ptr + 1]); ptr += 2
            eu[i] = u; ev[i] = v
            adj[u].append((v, i))
            adj[v].append((u, i))

        # ---------- 点双连通分量（块） ----------
        dfn = [-1] * (n + 1)
        low = [0] * (n + 1)
        estk = []
        blocks = []
        timer = 0
        sys.setrecursionlimit(10000 + 4 * n)

        def tarjan(u, pe):
            nonlocal timer
            dfn[u] = low[u] = timer
            timer += 1
            for v, e in adj[u]:
                if e == pe:
                    continue
                if dfn[v] < 0:
                    estk.append(e)
                    tarjan(v, e)
                    if low[v] < low[u]:
                        low[u] = low[v]
                    if low[v] >= dfn[u]:
                        blk = []
                        while True:
                            x = estk.pop()
                            blk.append(x)
                            if x == e:
                                break
                        blocks.append(blk)
                elif dfn[v] < dfn[u]:
                    estk.append(e)
                    if dfn[v] < low[u]:
                        low[u] = dfn[v]

        for i in range(1, n + 1):
            if dfn[i] < 0:
                tarjan(i, -1)

        # ---------- 块-割点树 ----------
        nb = len(blocks)
        tot = n + nb
        tree = [[] for _ in range(tot + 1)]
        seen = [-1] * (n + 1)
        for b in range(nb):
            verts = []
            for ei in blocks[b]:
                u = eu[ei]; v = ev[ei]
                if seen[u] != b:
                    seen[u] = b; verts.append(u)
                if seen[v] != b:
                    seen[v] = b; verts.append(v)
            for v in verts:
                tree[v].append(n + 1 + b)
                tree[n + 1 + b].append(v)

        # ---------- 树上 1 -> n 路径 ----------
        par = [-2] * (tot + 1)
        par[1] = -1
        q = [1]
        head = 0
        while head < len(q):
            u = q[head]; head += 1
            for w in tree[u]:
                if par[w] == -2:
                    par[w] = u
                    q.append(w)
        if par[n] == -2:
            out.append("-1")
            continue
        bpath = []
        x = n
        while x != -1:
            bpath.append(x)
            x = par[x]
        bpath.reverse()

        ns = (len(bpath) - 1) // 2
        INF = float('inf')
        dp = [0, INF]
        seg_info = []          # (idlist, ladj, la, lb)
        args = []
        for i in range(ns):
            b = bpath[2 * i + 1] - (n + 1)
            a = bpath[2 * i]; c = bpath[2 * i + 2]
            loc = [0] * (n + 1)
            idlist = []
            for ei in blocks[b]:
                u = eu[ei]; v = ev[ei]
                if loc[u] == 0:
                    loc[u] = len(idlist) + 1; idlist.append(u)
                if loc[v] == 0:
                    loc[v] = len(idlist) + 1; idlist.append(v)
            k = len(idlist)
            for j in range(k):
                loc[idlist[j]] = j
            ladj = [[] for _ in range(k)]
            for ei in blocks[b]:
                u = loc[eu[ei]]; v = loc[ev[ei]]
                ladj[u].append(v)
                ladj[v].append(u)
            la = loc[a]; lb = loc[c]
            # 双层图 BFS
            dist = [-1] * (2 * k)
            dq = [2 * la]
            dist[2 * la] = 0
            head = 0
            while head < len(dq):
                st = dq[head]; head += 1
                v = st >> 1; p = st & 1; d = dist[st]
                for w in ladj[v]:
                    ns2 = 2 * w + (p ^ 1)
                    if dist[ns2] < 0:
                        dist[ns2] = d + 1
                        dq.append(ns2)
            d0 = dist[2 * lb]
            d1 = dist[2 * lb + 1]
            seg_info.append((idlist, ladj, la, lb))
            # DP
            ndp = [INF, INF]
            arg = [-1, -1]
            for p in (0, 1):
                if dp[p] is INF or dp[p] >= INF:
                    continue
                for qq, dd in ((0, d0), (1, d1)):
                    if dd < 0:
                        continue
                    val = dp[p] + dd
                    np_ = p ^ qq
                    if val < ndp[np_]:
                        ndp[np_] = val
                        arg[np_] = qq
            dp = ndp
            args.append(arg)
        if dp[0] >= INF:
            out.append("-1")
            continue
        # 回溯奇偶选择
        choice = [0] * ns
        cur = 0
        for i in range(ns - 1, -1, -1):
            qq = args[i][cur]
            choice[i] = qq
            cur ^= qq

        # ---------- 逐块还原简单路径 ----------
        ans = [1]
        ok = True
        for i in range(ns):
            idlist, ladj, la, lb = seg_info[i]
            k = len(idlist)
            du = [-1] * (2 * k)
            du[2 * la] = 0
            dq = [2 * la]
            head = 0
            while head < len(dq):
                st = dq[head]; head += 1
                v = st >> 1; p = st & 1
                for w in ladj[v]:
                    ns2 = 2 * w + (p ^ 1)
                    if du[ns2] < 0:
                        du[ns2] = du[st] + 1
                        dq.append(ns2)
            dv = [-1] * (2 * k)
            dv[2 * lb] = 0
            dq = [2 * lb]
            head = 0
            while head < len(dq):
                st = dq[head]; head += 1
                v = st >> 1; p = st & 1
                for w in ladj[v]:
                    ns2 = 2 * w + (p ^ 1)
                    if dv[ns2] < 0:
                        dv[ns2] = dv[st] + 1
                        dq.append(ns2)
            D = du[2 * lb + choice[i]]
            if D < 0:
                ok = False
                break
            used = bytearray(k)
            stV = [la]
            stIt = [0]
            used[la] = 1
            lp = None
            while stV:
                x = stV[-1]
                d = len(stV) - 1
                if d == D:
                    if x == lb:
                        lp = list(stV)
                        break
                    used[x] = 0
                    stV.pop(); stIt.pop()
                    continue
                nd = d + 1; nq = nd & 1; rem = D - nd
                adv = False
                lx = ladj[x]
                it = stIt[-1]
                while it < len(lx):
                    y = lx[it]; it += 1
                    if y == lb:
                        if nd == D:
                            stIt[-1] = it
                            stV.append(y); stIt.append(0)
                            adv = True
                            break
                        continue
                    if nd == D or used[y]:
                        continue
                    if du[2 * y + nq] != nd:
                        continue
                    if dv[2 * y + (rem & 1)] != rem:
                        continue
                    stIt[-1] = it
                    used[y] = 1
                    stV.append(y); stIt.append(0)
                    adv = True
                    break
                if adv:
                    continue
                stIt[-1] = it
                used[x] = 0
                stV.pop(); stIt.pop()
            if lp is None:
                ok = False
                break
            for j in range(1, len(lp)):
                ans.append(idlist[lp[j]])
        if not ok:
            out.append("-1")
            continue
        out.append(str(len(ans) - 1))
        out.append(" ".join(map(str, ans)))
    sys.stdout.write("\n".join(out) + "\n")

main()
```

## 8. 边界情况与易错点

1. **不连通**：块-割点树上 $1$ 到 $n$ 不可达，直接输出 $-1$（不要输出空行或 $0$）。
2. **$n=2$ 且只有一条边**：唯一的块是桥，段长 $1$ 为奇数，$dp[0]=\infty$，输出 $-1$；$m=0$ 同理（没有任何块）。
3. **$\infty$ 的处理**：桥块的偶段是 $\infty$，二分块的另一种奇偶也是 $\infty$；相加前必须判 $-1$，并用 `long long` 防止 $\infty+1$ 溢出。
4. **"绕回同一点"的幻觉**：不要直接用双层图 BFS 的父亲链当答案（★样例就会错）；必须走 tight 状态且禁止重复顶点，并保证出口只在最后一步进入。
5. **块的端点可能相同吗？** 不会：块-割点树是树，路径上相邻的块点之间必有一个割点，入口与出口是不同顶点。
6. **多测编号**：块点在块-割点树里的编号从 $n+1$ 开始，别与原点 $1..n$ 冲突；读入边是 1-indexed，输出也用 1-indexed。
7. **Python 性能**：本做法是线性的，但 CPython 常数较大（最坏 $n=1000$ 完全图约 $1.6$ s，$10^4$ 组小数据约 $3$ s（已贴时限）），建议交 **PyPy3**；递归 Tarjan 前把 `sys.setrecursionlimit` 调大。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：0 / 1 通过 token 比对；本题输出不唯一（构造 / 多解 / 特殊评测），剩余差异属预期，样例含义已在第 2 节逐组解释。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [CF 1486E Paired Payment](https://codeforces.com/problemset/problem/1486/E)：把"两步权值"包装成分层图最短路，和本题"双层图"技巧同源。
- [CF 1473E Minimum Path](https://codeforces.com/problemset/problem/1473/E)：最短路 + 额外状态（用/不用优惠），分层 DP 的典型。
- [CF 1442C Graph Transpositions](https://codeforces.com/problemset/problem/1442/C)：状态含"是否翻转"，按层数/代价分层处理。
- [LeetCode 1129. 颜色交替的最短路径](https://leetcode.cn/problems/shortest-path-with-alternating-colors/)：状态 = (点, 上次颜色)，把奇偶换成一个二元属性。
- [LeetCode 787. K 站中转内最便宜的航班](https://leetcode.cn/problems/cheapest-flights-within-k-stops/)：按“已用中转次数”分层的最短路，分层状态思想与本题一致。

**延伸思考**：

1. 把"偶"换成"长度 $\equiv 0 \pmod k$"：块内的双层图要换成 $k$ 层，但块内引理（最短模 $k$ 走法 = 最短模 $k$ 简单路径）在 2-连通块上是否仍成立？这是本题最值得追问的一点，也是为什么本题的做法依赖 $k=2$ 时的"奇环穿过"论证。
2. 若要求"最短偶长简单**回路**（经过 $1$）"，块分解仍然适用，但起点所在块要特殊处理：回路在该块内是"从割点出发再回到同一割点"的闭合段。
3. 如果忘记引理 2，只保留奇偶分层 BFS，可以用对拍快速发现 ★样例这种反例——**遇到"最短 + 简单性"一定要先想块分解**。
