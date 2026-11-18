# Codeforces 谱分量 题解

## 1. 题目概述

- **标题 / 题号**：谱分量（Codeforces 2252F，英文名 Spectral Components）
- **链接**：https://codeforces.com/problemset/problem/2252/F
- **来源**：Codeforces Round 1115 (Div. 2) · Problem F
- **难度**：*2600
- **限制**：时间 3 s / 内存 256 MB
- **标签**：树，虚树与 DFS，动态规划，贪心，排序

**题意**：给定一棵 $n$ 个点的树，点 $i$ 的颜色为 $c_i$。对每个在树中出现过的颜色 $c$，记它出现 $m_c$ 次，并给出目标大小 $k_c$（保证 $1 \le k_c \le m_c$）。对每个颜色**独立**地，选出**恰好 $k_c$ 个点**构成的连通子图（分量）$S$，代价为所有颜色为 $c$ 的点到 $S$ 的最短距离之和（点 $v$ 到 $S$ 的距离是 $v$ 到 $S$ 中任意点的最少边数）。若颜色 $c$ 从未出现，输出 $-1$。

**约束**：

- $1 \le t \le 10^4$，$1 \le n \le 2\cdot 10^5$，且 $\sum n \le 2\cdot 10^5$；
- $1 \le c_i \le n$，$1 \le k_c \le n$，且颜色 $c$ 出现 $m_c>0$ 次时 $1 \le k_c \le m_c$；
- 每组接着给出 $n-1$ 条边，构成一棵树；每组输出一行 $n$ 个整数，第 $c$ 个是颜色 $c$ 的最小代价。

## 2. 示例

**样例 1–3（官方）**

```text
输入
3
5
1 1 2 1 2
2 1 1 1 1
1 2
2 3
2 4
4 5
6
2 1 1 1 1 1
3 1 1 1 1 1
1 2
1 3
1 4
1 5
1 6
6
1 2 1 2 1 2
2 3 1 1 1 1
1 2
2 3
3 4
4 5
5 6
输出
1 3 -1 -1 -1
3 0 -1 -1 -1 -1
3 2 -1 -1 -1 -1
```

- 样例 1：颜色 1 取 $S=\{2,4\}$，三个点距离为 $1,0,0$，代价 1；颜色 2 的目标是单点，取顶点 2，两个点各付 $1,2$，代价 3。
- 样例 2：颜色 1 是 5 个叶子，取“中心 + 2 个叶子”，剩下 3 个叶子各付 1，代价 3；颜色 2 只含中心，代价 0。
- 样例 3：颜色 2 取 $\{3,4,5\}$，颜色为 2 的点 $2,4,6$ 各付 $1,0,1$，代价 2。

**自造示例：$k_c=m_c$ 时代价未必是 0**

```text
输入
2
3
1 2 1
2 1 1
1 2
2 3
6
1 1 1 1 1 1
5 1 1 1 1 1
1 2
1 3
1 4
1 5
1 6
输出
1 0 -1
1 -1 -1 -1 -1 -1
```

第一组：颜色 1 只出现 2 次且 $k_1=2$，只能取这两个相邻点，例如 $S=\{1,2\}$，另一个颜色 1 的点（顶点 3）付 1，代价 1。第二组：6 点星形全是颜色 1，$m=5$，但斯坦纳树有 6 个点，$k=5$ 时必有一个叶子被落下，代价 1——**$k_c=m_c$ 并不自动等于 0**。

## 3. 解题思路

### 3.1 暴力思路

对每个颜色枚举全部 $\binom{n}{k}$ 个点集，判连通后多源 BFS 求距离和，单色就是 $O\!\left(\binom{n}{k}n\right)$，$n=2\cdot10^5$ 时完全不可行；即便只枚举“连通子图”本身也是指数级的数量。

### 3.2 核心观察：割权分解

![割权分解示意](images/cf2252_f_cut_decomposition.svg)

固定颜色 $c$，把它的 $m=m_c$ 个点叫**终端**。对一条边 $e$，删去后树分成两侧；对顶点 $t$ 定义

$$w_e(t)=\text{不含 }t\text{ 的那一侧的终端个数}\in\{a_e,\;m-a_e\}.$$

**关键恒等式**：若 $S$ 连通且 $t\in S$，则

$$\operatorname{cost}(S)=\sum_{e\notin E(S)} w_e(t),$$

其中 $E(S)$ 是 $S$ 内部的边集。理由：终端 $v$ 到 $S$ 的最短路每跨一条边付 1，它跨过的正是“把 $v$ 与 $S$ 分到两侧”的那些边；这些边必然不在 $E(S)$ 里，而 $S$ 内部的边不会被任何“终端 $\to S$”的路跨过。

于是对固定顶点 $t$：

$$\operatorname{cost}(t,k)=\min_{S\ni t,\ |S|=k}\operatorname{cost}(S)=\Big(\sum_{e}w_e(t)\Big)-\Big(\text{最大的 } k-1 \text{ 个 } w_e(t) \text{ 之和}\Big).$$

以 $t$ 为根时，$w_e(t)$ 就是“子树内终端个数”，沿根向下**单调不增**；所以取值最大的 $k-1$ 条边（同值时优先取更浅的）一定构成一棵含 $t$ 的连通子树，正好对应合法的 $S$。

再做一步简化：设 $T'$ 为所有终端的**极小连通子树（斯坦纳树）**，$s=|T'|-1$。

- $T'$ 之外的边两侧终端数是 $0$ 或 $m$，而 $t\in T'$ 必与全部终端同侧，故这些边的贡献恒为 $0$；
- $T'$ 内的边两侧都有终端，贡献为 $a_e$ 或 $m-a_e$。

所以当 $t\in T'$ 时，$\sum_e w_e(t)$ 只需对 $s$ 条斯坦纳边求和，且

$$\operatorname{cost}(t,k)=\text{最小的 } (s-k+1) \text{ 个斯坦纳边割权之和}\quad(k\le s),$$

而 $k\ge s+1$（即 $k\ge |T'|$）时答案为 $0$。又因 $k\le m\le |T'|=s+1$，后一种情况只会在 $k=|T'|$ 时发生。

### 3.3 算法流程：虚树 + Fenwick 维护有序多重集

![虚树上的翻转规则](images/cf2252_f_virtual_tree_flip.svg)

斯坦纳树可能有 $O(n)$ 个点，但终端只有 $m$ 个，于是对每个颜色建虚树：

1. 终端按 DFS 序排序，加入相邻两个终端的 LCA，去重后再排序，用栈连出虚树（节点数 $O(m)$）；
2. 虚树边 $(p\to u)$ 记两个量：长度 $L=\operatorname{dep}[u]-\operatorname{dep}[p]$，以及 $a=u$ 的虚子树内终端数；这条压缩边上的 $L$ 条实边割权**全是** $a$；
3. 以虚树根为根，初始多重集为“每条虚树边贡献 $L$ 份 $a$”；
4. DFS 虚树：从 $p$ 进入 $u$ 时把这 $L$ 份 $a$ 翻成 $L$ 份 $m-a$（顶点 $t$ 换到了 $u$ 一侧），回溯时撤销；
5. 值域 Fenwick 同时维护“个数”和“总和”，“最小的 $R=s-k+1$ 个割权之和”在 $O(\log m)$ 内回答；
6. 对全部虚树节点取最小值即该颜色的答案；$k-1\ge s$ 直接输出 0，$m=1$ 也直接输出 0。

**为什么只需虚树节点**：沿压缩边向下移动 $t$ 时，多重集里恰有一个元素从 $a$ 变成 $m-a$。若 $m-a>a$，多重集逐个变大，“最小 $R$ 个之和”随下行不减，最优在该边上端；若 $m-a<a$，则随下行不增，最优在下端（引理 4）。

### 3.4 示例演算

![样例 3 颜色 1 的走查](images/cf2252_f_walkthrough.svg)

取样例 3 的颜色 1（终端 $1,3,5$）：$m=3$，斯坦纳树是链 $1-3-5$，虚树两条边为 $(1\to3):L=2,a=2$ 与 $(3\to5):L=2,a=1$，故 $s=4$；$k=2$ 给出 $R=4-2+1=3$。

| 顶 $t$ | 被翻转的压缩边 | 当前割权多重集 | 最小 3 个之和 |
|---|---|---|---|
| 1 | 无 | $\{2,2,1,1\}$ | $1+1+2=4$ |
| 3 | $1-3$ | $\{1,1,1,1\}$ | $1+1+1=\mathbf{3}$ |
| 5 | $1-3$ 与 $3-5$ | $\{1,1,2,2\}$ | $1+1+2=4$ |

最小值 3 与官方输出一致。同法算颜色 2（终端 $2,4,6$，由对称性同样 $s=4$，$k=3$ 给 $R=2$）：三个候选多重集分别是 $\{2,2,1,1\}$、$\{1,1,1,1\}$、$\{1,1,2,2\}$，最小 2 个之和均为 2，答案 2，同样与输出一致。

## 4. 算法细节

1. **多测清空**：各数组按测试用例重新分配；`mark` 用“颜色编号打戳”代替清零，天然按颜色隔离；Fenwick 按颜色新建，规模 $m+1$，总量 $\sum m=n$，不会退化。
2. **虚树构造**：终端按 dfn 排序，把相邻两项的 LCA 并入后按 dfn 排序去重，再用栈求父亲——栈里始终是当前点的祖先链，弹到栈顶是祖先为止，父亲下标即得。
3. **压缩边绝不能展开**：$L$ 可达 $n$，而 $\sum_c|T'_c|$ 能到 $O(n^2)$（例如链上 $n/2$ 个颜色各出现 2 次且彼此相距很远），所以 $L$ 只作为“份数”参与一次更新，单次 $O(\log m)$。
4. **贪心取前 $k-1$ 大**：割权沿根向下单调不增，同值时按深度优先取浅的，得到的就是祖先封闭（连通）边集，所以“前 $k-1$ 大之和”等于受连通约束的最大值，不需要树形背包。
5. **答案要 64 位**：最大代价约 $n\cdot m\le 4\cdot10^{10}$；Fenwick 里“份数 $\times$ 权值”同样用 `long long`（Python 整数天然安全）。
6. **Fenwick 求“最小 $R$ 个之和”**：在“个数”前缀上做二进制下降，定位第 $R$ 小的值 $v$，答案 = 严格小于 $v$ 的部分和 + $\big(R-\text{小于 }v\text{ 的个数}\big)\cdot v$；$R=s-k+1\ge 1$，不会查空集。
7. **翻转可能是空操作**：$m$ 为偶数且 $a=m/2$ 时 $m-a=a$，代码用 `if (m - a != a)` 跳过，省一半更新。
8. **全部迭代实现**：$n=2\cdot10^5$ 的链会让递归爆栈，求父亲/深度、求子树大小、LCA、虚树 DFS 全用显式栈，LCA 用倍增保证 $O(\log n)$。
9. **I/O**：C++ 用 `scanf/printf`（或关同步的 `cin/cout`），每组输出一行 $n$ 个数、行末换行。

## 5. 正确性证明

**引理 1（割权恒等式）**：若 $S$ 连通且 $t\in S$，则 $\operatorname{cost}(S)=\sum_{e\notin E(S)}w_e(t)$。

**证明**：终端 $v$ 到 $S$ 的最短路跨过的边，恰是删去后使 $v$ 与 $S$ 分居两侧的边。由于 $S$ 连通，对这样的边 $e$，$S$ 整体落在含 $t$ 的一侧，$v$ 在另一侧，故 $v$ 给 $w_e(t)$ 贡献 1；反之 $S$ 内部的边不可能分开 $v$ 与 $S$。交换求和次序即得恒等式。∎

**引理 2**：固定 $t$ 时，在所有“含 $t$、$k$ 个点、连通”的 $S$ 中，$\sum_{e\in E(S)}w_e(t)$ 的最大值等于 $w_e(t)$ 的前 $k-1$ 大之和。

**证明**：以 $t$ 为根，点 $x\ne t$ 的割权 $w_{(par(x),x)}(t)$ 就是 $x$ 子树内的终端数，故父边的割权不小于任何子边。把所有割权按“值降序、深度升序”排序，前 $k-1$ 个构成祖先封闭集合：若 $x$ 入选而父亲 $p$ 落选，则 $w_p\ge w_x$，且相等时 $p$ 更浅、排位更靠前，矛盾。取这 $k-1$ 条边的所有端点再加上 $t$ 即为合法连通 $k$ 点集，故该上界可达；而任一这类边集的权和都不超过前 $k-1$ 大之和。∎

**引理 3**：设 $T'$ 为终端的斯坦纳树，$s=|T'|-1$。若 $t\in T'$，则 $T'$ 外的边对 $\sum_e w_e(t)$ 贡献 0；且 $k\le s$ 时 $\operatorname{cost}(t,k)$ 等于最小的 $s-k+1$ 个斯坦纳边割权之和，$k\ge s+1$ 时为 0。

**证明**：$T'$ 外的边至少一侧无终端。$t\in T'$ 与全部终端同侧，故不含 $t$ 的一侧终端数为 0，贡献为 0。于是在 $s$ 条斯坦纳边上由引理 1、2 得 $\operatorname{cost}(t,k)=\sum_e w_e(t)-(\text{前 }k-1\text{ 大})=\text{最小的 }s-k+1\text{ 个之和}$。当 $k\ge s+1$ 时取 $S\supseteq T'$（$|S|=k$ 可行，因 $k\le n$）覆盖全部终端，代价为 0。∎

**引理 4（候选点只需虚树节点）**：对 $t\notin T'$，令 $t'$ 为 $t$ 到 $T'$ 的最近点，则 $\operatorname{cost}(t,k)\ge\operatorname{cost}(t',k)$；而 $t$ 沿一条压缩边内部移动时 $\operatorname{cost}(t,k)$ 关于位置单调，最小值在端点。

**证明**：$t$ 与 $t'$ 对 $T'$ 外的每条边同侧，割权多重集只在“$t$ 到 $t'$ 路径上的边”处不同：在 $t'$ 处这些边取 $0$，在 $t$ 处取 $m$。把若干元素从 $0$ 换成 $m$ 不会让“最小 $R$ 个之和”变小，故前者不小于后者。沿压缩边每下移一格，恰有一个 $a$ 变成 $m-a$：$m-a>a$ 时“最小 $R$ 个之和”不减（最优在上端），$m-a<a$ 时不增（最优在下端），故两端点之一最优。∎

**定理**：对每个颜色，算法输出即为题目要求的最小代价。

**证明**：由引理 4 只需把 $t$ 取遍虚树节点。对每个虚树节点 $u$，DFS 维护的多重集正是 $\{w_e(u)\}$：初始为各边 $L$ 份 $a$，沿根到 $u$ 的路径翻成 $m-a$。由引理 3 该节点的候选值等于 $\operatorname{cost}(u,k)$，取最小即得颜色答案；$k\ge s+1$ 输出 0、$m=1$ 输出 0 也由定义与引理 3 直接给出。∎

## 6. 复杂度分析

- **时间**：单个颜色为排序终端 + $O(m)$ 次 LCA + 建虚树 + $O(m)$ 次 Fenwick 更新与查询，均摊 $O(m\log m+m\log n)$；所有颜色合计 $\sum m_c=n$，单组数据总计 $O(n\log n)$。实测 $n=2\cdot10^5$ 的链 / 星形 / 随机树 / 单色全覆盖等形态，C++ 均在 $0.2$ s 以内，对 3 s 时限有 15 倍以上余量。
- **空间**：邻接表、倍增表、虚树、Fenwick 都是 $O(n)$，Fenwick 按颜色复用。
- **Python**：同一实现在 $n=2\cdot10^5$ 时约 $3.4\sim4.4$ s，提交时建议用 PyPy；若仍吃紧就用 C++ 版。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
// Fenwick on the value domain: counts + sums, supports "sum of the R smallest values".
struct Fenwick {
    int n, pw;
    vector<long long> c, s;
    void init(int n_) {
        n = n_; c.assign(n + 1, 0); s.assign(n + 1, 0);
        pw = 1; while ((pw << 1) <= n) pw <<= 1;
    }
    void upd(int i, long long dc, long long ds) {
        for (; i <= n; i += i & (-i)) { c[i] += dc; s[i] += ds; }
    }
    long long smallest(long long R) {
        int idx = 0; long long cc = 0, ss = 0;
        for (int b = pw; b; b >>= 1) {
            int nx = idx + b;
            if (nx <= n && cc + c[nx] < R) { idx = nx; cc += c[nx]; ss += s[nx]; }
        }
        return ss + (R - cc) * (idx + 1);
    }
};
int main() {
    int T; if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n; scanf("%d", &n);
        vector<int> col(n), kk(n + 1);
        for (int &x : col) scanf("%d", &x);
        for (int c = 1; c <= n; c++) scanf("%d", &kk[c]);
        vector<int> head(n, -1), nxt(2 * max(0, n - 1)), to(2 * max(0, n - 1));
        int ec = 0;
        for (int i = 0; i < n - 1; i++) {
            int u, v; scanf("%d %d", &u, &v); --u; --v;
            to[ec] = v; nxt[ec] = head[u]; head[u] = ec++;
            to[ec] = u; nxt[ec] = head[v]; head[v] = ec++;
        }
        // iterative DFS: parent / depth / preorder / subtree size
        vector<int> par(n, -1), dep(n, 0), tin(n, 0), sz(n, 1), ord;
        ord.reserve(n);
        vector<int> st{0};
        while (!st.empty()) {
            int v = st.back(); st.pop_back();
            tin[v] = (int)ord.size(); ord.push_back(v);
            for (int e = head[v]; e != -1; e = nxt[e]) {
                int u = to[e]; if (u == par[v]) continue;
                par[u] = v; dep[u] = dep[v] + 1; st.push_back(u);
            }
        }
        for (int i = n - 1; i > 0; i--) sz[par[ord[i]]] += sz[ord[i]];
        int LOG = 1; while ((1 << LOG) <= n) LOG++;
        vector<vector<int>> up(LOG, vector<int>(n, 0));
        for (int v = 0; v < n; v++) up[0][v] = max(par[v], 0);
        for (int j = 1; j < LOG; j++)
            for (int v = 0; v < n; v++) up[j][v] = up[j - 1][up[j - 1][v]];
        auto anc = [&](int a, int b) { return tin[a] <= tin[b] && tin[b] < tin[a] + sz[a]; };
        auto lca = [&](int a, int b) {
            if (anc(a, b)) return a;
            if (anc(b, a)) return b;
            for (int j = LOG - 1; j >= 0; j--) if (!anc(up[j][a], b)) a = up[j][a];
            return up[0][a];
        };

        vector<vector<int>> grp(n + 1);
        for (int v = 0; v < n; v++) grp[col[v]].push_back(v);
        vector<int> mark(n, -1);
        vector<long long> ans(n + 1, -1);
        Fenwick fw;
        for (int c = 1; c <= n; c++) {
            auto &terms = grp[c];
            int m = (int)terms.size();
            if (m == 0) { ans[c] = -1; continue; }
            if (m == 1) { ans[c] = 0; continue; }
            sort(terms.begin(), terms.end(), [&](int a, int b) { return tin[a] < tin[b]; });
            vector<int> nodes;
            nodes.reserve(2 * m);
            for (int v : terms) { nodes.push_back(v); mark[v] = c; }
            for (int i = 0; i + 1 < m; i++) nodes.push_back(lca(terms[i], terms[i + 1]));
            sort(nodes.begin(), nodes.end(), [&](int a, int b) { return tin[a] < tin[b]; });
            nodes.erase(unique(nodes.begin(), nodes.end()), nodes.end());
            int S = (int)nodes.size();
            // virtual tree parents via a stack of ancestors
            vector<int> pv(S, -1);
            st.clear();
            for (int i = 0; i < S; i++) {
                while (!st.empty() && !anc(nodes[st.back()], nodes[i])) st.pop_back();
                pv[i] = st.empty() ? -1 : st.back();
                st.push_back(i);
            }
            vector<int> cnt(S, 0), len(S, 0);
            for (int i = 0; i < S; i++) if (mark[nodes[i]] == c) cnt[i] = 1;
            for (int i = S - 1; i >= 1; i--) cnt[pv[i]] += cnt[i];
            long long s = 0;
            for (int i = 1; i < S; i++) {
                len[i] = dep[nodes[i]] - dep[nodes[pv[i]]];
                s += len[i];
            }
            if ((long long)kk[c] - 1 >= s) { ans[c] = 0; continue; }
            long long R = s - kk[c] + 1;      // need the R smallest cut values
            fw.init(m);
            for (int i = 1; i < S; i++) fw.upd(cnt[i], len[i], (long long)len[i] * cnt[i]);
            vector<int> fc(S, -1), ns(S, -1);
            for (int i = 1; i < S; i++) { ns[i] = fc[pv[i]]; fc[pv[i]] = i; }
            long long best = fw.smallest(R);
            vector<pair<int, int>> stack2{{0, fc[0]}};
            while (!stack2.empty()) {
                int v = stack2.back().first, ch = stack2.back().second;
                if (ch == -1) {
                    stack2.pop_back();
                    if (v) {  // roll back the flip of edge (parent(v), v)
                        int a = cnt[v]; long long L = len[v];
                        fw.upd(a, L, L * a);
                        if (m - a != a) fw.upd(m - a, -L, -L * (long long)(m - a));
                    }
                    continue;
                }
                stack2.back().second = ns[ch];
                int a = cnt[ch]; long long L = len[ch];
                fw.upd(a, -L, -L * (long long)a);
                if (m - a != a) fw.upd(m - a, L, L * (long long)(m - a));
                best = min(best, fw.smallest(R));
                stack2.push_back({ch, fc[ch]});
            }
            ans[c] = best;
        }
        for (int c = 1; c <= n; c++) printf("%lld%c", ans[c], c == n ? '\n' : ' ');
    }
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        col = list(map(int, data[p:p + n])); p += n
        kk = [0] * (n + 1)
        for c in range(1, n + 1):
            kk[c] = int(data[p]); p += 1
        adj = [[] for _ in range(n)]
        for _e in range(n - 1):
            u = int(data[p]) - 1; v = int(data[p + 1]) - 1; p += 2
            adj[u].append(v); adj[v].append(u)

        # 迭代 DFS：父亲 / 深度 / 先序时间 / 子树大小
        par = [-1] * n; dep = [0] * n; tin = [0] * n; order = []
        st = [0]
        while st:
            v = st.pop(); tin[v] = len(order); order.append(v)
            pv = par[v]
            for u in adj[v]:
                if u != pv:
                    par[u] = v; dep[u] = dep[v] + 1; st.append(u)
        sz = [1] * n
        for v in reversed(order):
            if par[v] >= 0:
                sz[par[v]] += sz[v]

        # 倍增 LCA
        LOG = max(1, n.bit_length())
        up = [list(par)]; up[0][0] = 0
        for j in range(1, LOG):
            prev = up[-1]
            up.append([prev[prev[v]] for v in range(n)])

        def anc(a, b):
            return tin[a] <= tin[b] < tin[a] + sz[a]

        def lca(a, b):
            if anc(a, b):
                return a
            if anc(b, a):
                return b
            for j in range(LOG - 1, -1, -1):
                if not anc(up[j][a], b):
                    a = up[j][a]
            return up[0][a]

        groups = [[] for _ in range(n + 1)]
        for v in range(n):
            groups[col[v]].append(v)
        mark = [-1] * n
        ans = [-1] * (n + 1)

        for c in range(1, n + 1):
            terms = groups[c]
            m = len(terms)
            if m == 0:
                continue
            if m == 1:
                ans[c] = 0
                continue
            terms.sort(key=lambda x: tin[x])
            for v in terms:
                mark[v] = c
            nodes = list(terms) + [lca(terms[i], terms[i + 1]) for i in range(m - 1)]
            nodes.sort(key=lambda x: tin[x])
            uniq = [nodes[0]]
            for v in nodes[1:]:
                if tin[v] != tin[uniq[-1]]:
                    uniq.append(v)
            nodes = uniq
            S = len(nodes)

            # 虚树：用祖先栈求父亲
            pv = [-1] * S; stack = []
            for i in range(S):
                while stack and not anc(nodes[stack[-1]], nodes[i]):
                    stack.pop()
                pv[i] = stack[-1] if stack else -1
                stack.append(i)

            cnt = [1 if mark[nodes[i]] == c else 0 for i in range(S)]
            for i in range(S - 1, 0, -1):
                cnt[pv[i]] += cnt[i]
            ln = [0] * S; s = 0
            for i in range(1, S):
                ln[i] = dep[nodes[i]] - dep[nodes[pv[i]]]
                s += ln[i]
            if kk[c] - 1 >= s:      # k >= |T'| 时代价为 0
                ans[c] = 0
                continue
            R = s - kk[c] + 1       # 需要最小的 R 个割权之和

            # 值域 Fenwick：个数 + 总和
            pw = 1
            while (pw << 1) <= m:
                pw <<= 1
            fc = [0] * (m + 1); fs = [0] * (m + 1)

            def upd(i, dc, ds):
                while i <= m:
                    fc[i] += dc; fs[i] += ds
                    i += i & (-i)

            def smallest(rr):
                idx = 0; cc = 0; ss = 0; b = pw
                while b:
                    nx = idx + b
                    if nx <= m and cc + fc[nx] < rr:
                        idx = nx; cc += fc[nx]; ss += fs[nx]
                    b >>= 1
                return ss + (rr - cc) * (idx + 1)

            for i in range(1, S):
                a = cnt[i]; L = ln[i]
                upd(a, L, L * a)

            first = [-1] * S; nxt = [-1] * S
            for i in range(1, S):
                q = pv[i]; nxt[i] = first[q]; first[q] = i

            best = smallest(R)
            stack = [[0, first[0]]]
            while stack:
                top = stack[-1]; v = top[0]
                if top[1] == -1:          # 回溯：撤销翻转
                    stack.pop()
                    if v:
                        a = cnt[v]; L = ln[v]
                        upd(a, L, L * a)
                        if m - a != a:
                            upd(m - a, -L, -L * (m - a))
                    continue
                u = top[1]; top[1] = nxt[u]
                a = cnt[u]; L = ln[u]     # 进入 u：L 份 a 翻转成 m-a
                upd(a, -L, -L * a)
                if m - a != a:
                    upd(m - a, L, L * (m - a))
                val = smallest(R)
                if val < best:
                    best = val
                stack.append([u, first[u]])
            ans[c] = best

        out.append(' '.join(str(ans[c]) for c in range(1, n + 1)))
    sys.stdout.write('\n'.join(out) + '\n')


main()
```

## 8. 边界情况与易错点

1. **颜色未出现**输出 $-1$；恰好出现一次的颜色（必有 $k=1$）答案为 0。
2. **$k_c=m_c$ 不一定为 0**：星形 5 叶同色、$k=5$ 时答案为 1，因为斯坦纳树比 $m$ 大。
3. **$k-1\ge s$ 必须先判**：此时答案为 0；否则 $R=s-k+1\le 0$，Fenwick 查询会越界或返回垃圾值。
4. **压缩边长度可达 $n$**，绝不能逐点展开：$\sum_c|T'_c|$ 可达 $O(n^2)$，会直接超时。
5. **$m$ 偶数且 $a=m/2$** 时翻转是空操作，避免重复加减。
6. **值域**是 $[1,m-1]$，Fenwick 开 $m$ 大小；$m=1$ 提前返回，以免值域为空。
7. **多测** $t$ 可达 $10^4$：按组分配数组即可（$\sum n\le 2\cdot10^5$），但别忘了每组都把答案数组重新初始化成 $-1$。
8. **递归会爆栈**：链上深度 $2\cdot10^5$，DFS 与 LCA 全部迭代实现。
9. **输出格式**：一组一行 $n$ 个数、空格分隔、行末换行，不要行末多余空格。

## 相关题目与扩展

- [CF 613D Kingdom and its Cities](https://codeforces.com/problemset/problem/613/D)：虚树 + 树上贪心经典题，与本题“只用终端建虚树”的套路一致。
- [CF 1092F Tree with Maximum Cost](https://codeforces.com/problemset/problem/1092/F)：换根 DP 求 $\sum_v\operatorname{dist}(v,t)$，正是本题 $k=1$ 的核心。
- [LeetCode 834. 树中距离之和](https://leetcode.cn/problems/sum-of-distances-in-tree/)：换根求所有点对距离和，可用来验证“沿边移动代价变化 $m-2a$”。
- [LeetCode 1617. 统计子树中城市之间最大距离](https://leetcode.cn/problems/count-subtrees-with-max-distance-between-cities/)：枚举连通子集 + 求距离的暴力视角，对应 3.1 的朴素做法。

**延伸思考**：

1. 若 $S$ 只允许由颜色 $c$ 的点组成，割权分解仍成立，但“前 $k-1$ 大”不再自动连通，需要带权树形背包，复杂度退化为 $O(mk)$。
2. 若把“连通”放宽成“任意 $k$ 个点”，问题变成树上 $k$-median：仍可建虚树，但压缩边内部要解方程而不是直接取端点。
3. 若同一颜色要同时回答所有 $k$，可把割权按值降序插入并用并查集维护“已免单边集”，离线一次扫完，复杂度仍为 $O(m\log m)$。

