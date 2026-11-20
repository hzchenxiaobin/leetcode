# Codeforces 81E Pairs 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/81/E
- **比赛来源**：Yandex.Algorithm Open 2011: Qualification 1 · Problem E（UTC 2011-05-04）
- **难度**：2700
- **标签**：图论、树形 DP、基环树、匹配
- **评测类型**：多解（special judge：先最大化对数，再最大化男女混合对数）
- **限制**：时间 1 s / 内存 256 MB

**题意**：有 $n$ 个学生，第 $i$ 个学生有一个"最好的朋友" $f_i$（$f_i \ne i$），性别为 $s_i \in \{1, 2\}$。老师要把学生**两两配对**，每对必须由"某个学生和它的最好朋友"组成，即一对 $\{u, v\}$ 合法当且仅当 $f_u = v$ 或 $f_v = u$。每个学生至多出现在一对里。要求：先让**对数最多**，在同样多的方案里让**男女搭配的对数最多**。输出对数 $t$、混合对数 $e$，再输出这 $t$ 对。

**约束**：

- $n \le 10^5$：必须 $O(n)$ 或 $O(n \log n)$；任何一般图最大匹配算法（$O(n^3)$、$O(n^2 \sqrt n)$）都不可行。
- 每个学生恰好一条出边、没有自环：这个特殊结构叫**基环树森林**（functional graph），每个连通分量恰有一个环，环上挂着若干棵树。
- 输出任意方案，但 $t$ 与 $e$ 必须是全局最优。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
5
5 2
3 2
5 1
2 1
4 2

输出：
2 2
5 3
4 2
```

官方样例 2（输入 / 输出原样）：

```text
输入：
6
5 2
3 2
5 1
2 1
4 2
3 1

输出：
3 1
4 2
5 1
3 6
```

官方样例 3（输入 / 输出原样）：

```text
输入：
8
2 2
3 2
5 1
3 1
6 1
5 1
8 2
7 1

输出：
4 1
5 6
3 4
2 1
7 8
```

**样例 1 走查**：边为 $1-5, 2-3, 3-5, 4-2, 5-4$。图是一个 $5$ 个点的环 $1 \to 5 \to 4 \to 2 \to 3 \to 5$？注意 $f_2 = 3, f_3 = 5, f_5 = 4, f_4 = 2$，所以环是 $2 \to 3 \to 5 \to 4 \to 2$，而 $1$ 挂在 $5$ 上（$f_1 = 5$）。最大匹配为 $2$ 对；样例选的是 $\{5,3\}$ 与 $\{4,2\}$（都是男女搭配，$e = 2$）。

**样例 2 走查**：在上面的基础上加一条 $6 \to 3$，于是 $3$ 有两个孩子 $2$（环上）之外还有 $6$。最大匹配变成 $3$ 对，样例给的 $\{4,2\}, \{5,1\}, \{3,6\}$ 中只有 $\{4,2\}$ 是男女搭配（$s_4 = 1, s_2 = 2$），$e = 1$。

**样例 3 走查**：$n = 8$ 时最大匹配 $4$ 对，最多 $1$ 对男女搭配。这说明**在最大化对数之后，混合对数可能远小于对数**，两个目标不能混为一谈。

**观察 1（配对 = 匹配）**：把每条"最好朋友"关系看成**无向边** $\{i, f_i\}$（$i$ 与 $f_i$ 互为好友时两条有向边合成一条无向边）。一个合法方案就是一个**匹配**（每个点至多一条边）。

**观察 2（图的结构）**：每个点出度为 $1$、无自环，所以每个连通分量恰含一个长度 $\ge 2$ 的环，环上的每个点还挂着若干棵内向树。

**观察 3（两个目标的处理）**：把每条匹配边的权值设为 $M + [\text{男女搭配}]$，其中 $M = n + 1$。由于混合对数 $e \le t \le n/2 < M$，最大化总权 $M t + e$ 恰好等价于"先最大化 $t$，再最大化 $e$"。这就是把字典序目标变成标量目标的标准技巧。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

直接求一般图的最大匹配：$n = 10^5$ 时带花树（$O(n^3)$）不可能。注意到图是基环树森林后，可以用**树形 DP + 环上 DP** 做到 $O(n)$。难点在于：既要算出最优值，又要**还原出具体的配对方案**。

### 3.2 核心观察：树形 DP + 环上 DP

![基环树的结构](../../../images/cf81e_structure.svg)

**树上部分。** 对每个节点 $u$，定义（子树指以 $u$ 为根、沿着"孩子"方向的那部分）：

- $dp_0[u]$：$u$ **不与任何孩子配对**时，子树内的最大总权；
- $dp_1[u]$：$u$ **恰好与一个孩子配对**时，子树内的最大总权。

设 $\mathrm{best}[v] = \max(dp_0[v], dp_1[v])$，则

$$dp_0[u] = \sum_{v \in \mathrm{child}(u)} \mathrm{best}[v], \qquad dp_1[u] = \max_{v \in \mathrm{child}(u)} \Bigl( dp_0[u] - \mathrm{best}[v] + w(u,v) + dp_0[v] \Bigr).$$

直观理解：$u$ 不占用孩子时，每个孩子可以自由选择"连自己的孩子"或"不连"；$u$ 与某个孩子 $v$ 配对时，$v$ 就被 $u$ 占用，不能再连自己的孩子，所以该分支从 $\mathrm{best}[v]$ 换成 $w(u,v) + dp_0[v]$。

**环上部分。** 环上的每个节点 $c$ 先把它挂着的树"汇总"成两个数：

- $A[c] = \sum_{\text{树孩子 } v} \mathrm{best}[v]$：$c$ 不连树孩子时的贡献；
- $B[c] = A[c] + \max_{v} \bigl(w(c,v) + dp_0[v] - \mathrm{best}[v]\bigr)$：$c$ 连某个树孩子时的贡献。

然后沿环做 DP。设环上节点为 $c_0 \to c_1 \to \dots \to c_{L-1} \to c_0$（$f_{c_i} = c_{i+1}$）。对每个节点，只有"被前一条环边占用 / 不被占用"两种状态；分**两种情况**处理：环边 $(c_{L-1}, c_0)$ 不用（情况 0）与用（情况 1），这样就把环"剪"成了一条链。

**$L = 2$ 的特判**：两个点互相是对方的好友时，无向图里只有**一条**边，按"环边"处理会重复计算，所以直接按"两个点之间至多配一对"处理：$\max(\mathrm{best}[c_0] + \mathrm{best}[c_1],\ A[c_0] + A[c_1] + w(c_0,c_1))$。

### 3.3 算法流程

![DP 状态与转移](../../../images/cf81e_dp.svg)

1. 读入 $f_i, s_i$，建内向邻接表与入度；把边去重（只对 $2$ 环可能有重复）。
2. **拓扑剥叶**：把所有入度为 $0$ 的点依次弹出，按弹出顺序可以得到"孩子先于父亲"的拓扑序；最后剩下的点就是所有环上的点。
3. 按拓扑序对树上的点做 3.2 的 $dp_0/dp_1$，并记录 `gainChild[u]`（$dp_1$ 选的那个孩子）与 `bestChoice[u]`（$\mathrm{best}$ 取 $dp_0$ 还是 $dp_1$）。
4. 对每个环：先算环上点的 $A, B$（只看树孩子），再按 3.2 的两种情况做环上 DP，记录转移前驱以便还原。取较优的那种情况。
5. **还原匹配**：从环上的决策出发，确定每个环点是"被环边占用"还是"用树孩子/空闲"；然后按拓扑序的**逆序**（父亲先于孩子）自顶向下决定每个树点是否与父亲配对。
6. 统计对数 $t$ 与混合对数 $e$，输出。

### 3.4 样例走查

![样例 3 的基环树与匹配](../../../images/cf81e_walkthrough.svg)

样例 3：$f = (2, 3, 5, 3, 6, 5, 8, 7)$，即边 $1-2, 2-3, 3-5, 4-3, 5-6, 6-5, 7-8, 8-7$。分量一：$5 \leftrightarrow 6$ 是 2 环，$3 \to 5$、$4 \to 3$、$2 \to 3$、$1 \to 2$ 构成挂在 $3$ 上的链；分量二：$7 \leftrightarrow 8$ 是 2 环。

- 分量二：直接配对 $\{7,8\}$（一对）。
- 分量一：环边 $\{5,6\}$ 用掉一对；剩下的树是 $3 - 4$、$3 - 2 - 1$。若 $3$ 与 $4$ 配对，则 $2$ 不能再连 $3$（$3$ 已占用），可以连 $1$：得 $\{3,4\}$ 与 $\{2,1\}$，共两对。于是总数 $2 + 2 = 4$ 对。
- 混合对数：$s = (2,2,1,1,1,1,2,1)$，四对中只有 $\{7,8\}$（$2$ 与 $1$）是混合，$e = 1$，与样例一致。

这个例子说明"先最大化对数"可能牺牲混合对数——若为了多混合对而少配一对，就不是最优。

## 4. 正确性证明

**引理 1（配对 = 匹配）**：合法方案与无向图 $G = (V, E)$（$E = \{\{i, f_i\}\}$）的匹配一一对应。

**证明**：一对 $\{u,v\}$ 合法 $\iff$ $f_u = v$ 或 $f_v = u$ $\iff$ $\{u,v\} \in E$；"每个学生至多在一对里"就是匹配的定义。∎

**引理 2（图的结构）**：$G$ 的每个连通分量恰有一个长度 $\ge 2$ 的环，环上每个点挂着若干棵树。

**证明**：每个点出度恰为 $1$、无自环，所以沿 $f$ 走必然进入一个长度 $\ge 2$ 的环；环外的点沿 $f$ 最终都汇入某个环，构成内向树。∎

**引理 3（树形 DP 正确）**：对树上的 $u$，$dp_0[u]$、$dp_1[u]$ 的定义式给出子树内最优总权。

**证明**：对子树大小归纳。$u$ 的状态只有"不连孩子"与"连恰好一个孩子"两类（$u$ 与父亲的关系在父节点处处理）。不连孩子时各子树独立，取 $\mathrm{best}$ 之和；连孩子 $v$ 时该分支被占用，贡献变成 $w(u,v) + dp_0[v]$，其余分支仍取 $\mathrm{best}$。所有可能的孩子都枚举到，故取到最优。∎

**引理 4（环上 DP 正确）**：把环边 $(c_{L-1}, c_0)$ 的用/不用分成两种情况后，环上 DP 枚举了环上所有可能的匹配，并取到最优。

**证明**：环上的匹配只能是"若干条不相邻的环边"。固定 $(c_{L-1},c_0)$ 是否被选后，剩余部分是一条链 $c_0, c_1, \dots, c_{L-1}$，链上每个点要么被前一条链边占用、要么不被占用；DP 的两种状态恰好覆盖这两种情形，转移枚举了"占用下一条边"与"不占用"两种选择。故两种情况合起来覆盖所有环上匹配。∎

**引理 5（权值编码等价）**：设 $M = n + 1$，每条配对边权为 $M + [\text{混合}]$，则最大化总权等价于先最大化对数、再最大化混合对数。

**证明**：总权 $= M t + e$，其中 $0 \le e \le t \le \lfloor n/2\rfloor < M$。若 $t_1 > t_2$，则 $M t_1 + e_1 \ge M t_1 > M t_2 + M > M t_2 + e_2$；若 $t_1 = t_2$，则比较 $e$。所以总权序与 $(t, e)$ 的字典序一致。∎

**定理**：算法输出的 $t, e$ 与配对方案都是最优的。

**证明**：由引理 1、2，问题化为基环树森林上的最大权匹配；由引理 3、4，树上与环上的 DP 各自取到该部分最优，组合后得到全局最大权；由引理 5，最大权解恰是"对数最多、其次混合最多"的解；还原过程依据 DP 的决策，输出的边集与 DP 值一致，故方案可行且达到最优。∎

## 5. 复杂度分析

- **时间**：拓扑剥叶 $O(n)$；树上 DP 每条边被处理常数次，$O(n)$；环上 DP 每个环点 $O(1)$，$O(n)$；还原 $O(n)$。总计 $O(n)$，$n = 10^5$ 时实测 C++ 端到端约 $0.34$ s，其中约 $0.32$ s 是本机 libc++ 用 `cin >>` 读 $7.9 \times 10^5$ 字节输入的开销，DP 本体只有十几毫秒。
- **空间**：$O(n)$ 的邻接表、DP 数组与决策数组。
- **与时限的关系**：1 s 时限下 C++ 余量约 3 倍（$10^5$ 规模的主要开销是读入）；Python 版本用 `read().split()` 读入，总耗时约 $0.19$ s。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
static const ll NEG = LLONG_MIN / 4;

int n;
vector<int> f, sex;
vector<vector<int>> inL;
vector<int> indeg;
vector<ll> dp0, dp1;                 // 环上节点存 A / B；树上节点存"自由"/"连一个孩子"
vector<int> bestChoice, gainChild;
vector<char> onCycle, matchedParent;
vector<pair<int,int>> pairs;
ll MULT;

inline ll W(int u, int v) { return MULT + (sex[u] != sex[v] ? 1 : 0); }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n)) return 0;
    f.assign(n + 1, 0); sex.assign(n + 1, 0);
    inL.assign(n + 1, {});
    indeg.assign(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        cin >> f[i] >> sex[i];
        inL[f[i]].push_back(i);
        indeg[f[i]]++;
    }
    MULT = n + 1;                         // 先最大化对数，再最大化男女混合对数

    // 拓扑剥叶子，剩下的节点在环上
    vector<int> order;
    {
        queue<int> q;
        for (int i = 1; i <= n; ++i) if (indeg[i] == 0) q.push(i);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(u);
            int p = f[u];
            if (--indeg[p] == 0) q.push(p);
        }
    }
    onCycle.assign(n + 1, 0);
    for (int i = 1; i <= n; ++i) onCycle[i] = (indeg[i] > 0);

    dp0.assign(n + 1, 0); dp1.assign(n + 1, NEG);
    bestChoice.assign(n + 1, 0); gainChild.assign(n + 1, -1);
    matchedParent.assign(n + 1, 0);

    // 树上 DP：order 中孩子先于父亲出队
    for (int u : order) {
        ll base = 0;
        for (int v : inL[u]) base += max(dp0[v], dp1[v]);
        dp0[u] = base;
        ll bestGain = NEG; int arg = -1;
        for (int v : inL[u]) {
            ll b = max(dp0[v], dp1[v]);
            ll gain = W(u, v) + dp0[v] - b;
            if (gain > bestGain) { bestGain = gain; arg = v; }
        }
        dp1[u] = (arg < 0 ? NEG : base + bestGain);
        gainChild[u] = arg;
        bestChoice[u] = (dp1[u] > dp0[u]) ? 1 : 0;
    }

    vector<char> seen(n + 1, 0);
    for (int s = 1; s <= n; ++s) {
        if (!onCycle[s] || seen[s]) continue;
        vector<int> cyc;
        int u = s;
        while (!seen[u]) { seen[u] = 1; cyc.push_back(u); u = f[u]; }
        const int L = (int)cyc.size();

        // 环上节点的"树部分"：排除环上的前驱
        for (int c : cyc) {
            ll base = 0;
            for (int v : inL[c]) if (!onCycle[v]) base += max(dp0[v], dp1[v]);
            dp0[c] = base;
            ll bestGain = NEG; int arg = -1;
            for (int v : inL[c]) if (!onCycle[v]) {
                ll b = max(dp0[v], dp1[v]);
                ll gain = W(c, v) + dp0[v] - b;
                if (gain > bestGain) { bestGain = gain; arg = v; }
            }
            dp1[c] = (arg < 0 ? NEG : base + bestGain);
            gainChild[c] = arg;
            bestChoice[c] = (dp1[c] > dp0[c]) ? 1 : 0;
        }

        vector<char> usedNext(L, 0), usedPrev(L, 0);
        if (L == 2) {
            int c0 = cyc[0], c1 = cyc[1];
            ll no = max(dp0[c0], dp1[c0]) + max(dp0[c1], dp1[c1]);
            ll use = dp0[c0] + dp0[c1] + W(c0, c1);
            if (use > no) {
                usedNext[0] = 1; usedPrev[1] = 1;
                pairs.push_back({c0, c1});
            }
        } else {
            // 情况 0：wrap 边不用；情况 1：wrap 边使用
            vector<array<ll,2>> tab0(L + 1), tab1(L);
            vector<array<int,2>> pred0(L + 1), pred1(L);
            for (auto& t : tab0) t = {NEG, NEG};
            for (auto& t : tab1) t = {NEG, NEG};
            for (auto& t : pred0) t = {-1, -1};
            for (auto& t : pred1) t = {-1, -1};
            tab0[0][0] = 0;
            for (int i = 0; i < L; ++i) {
                int ci = cyc[i];
                ll A = dp0[ci], B = dp1[ci], best = max(A, B);
                ll wi = W(ci, cyc[(i + 1) % L]);
                array<ll,2> nd = {NEG, NEG}; array<int,2> pd = {-1, -1};
                for (int st = 0; st < 2; ++st) {
                    if (tab0[i][st] <= NEG / 2) continue;
                    if (st == 1) {
                        ll val = tab0[i][st] + A;
                        if (val > nd[0]) { nd[0] = val; pd[0] = st; }
                    } else {
                        ll val = tab0[i][st] + best;
                        if (val > nd[0]) { nd[0] = val; pd[0] = st; }
                        if (i < L - 1) {
                            ll v2 = tab0[i][st] + A + wi;
                            if (v2 > nd[1]) { nd[1] = v2; pd[1] = st; }
                        }
                    }
                }
                tab0[i + 1] = nd; pred0[i + 1] = pd;
            }
            tab1[0][1] = W(cyc[L - 1], cyc[0]);   // 只记 wrap 边的权，c_0 的贡献在 i=0 处加
            for (int i = 0; i < L - 1; ++i) {
                int ci = cyc[i];
                ll A = dp0[ci], B = dp1[ci], best = max(A, B);
                ll wi = W(ci, cyc[i + 1]);
                array<ll,2> nd = {NEG, NEG}; array<int,2> pd = {-1, -1};
                for (int st = 0; st < 2; ++st) {
                    if (tab1[i][st] <= NEG / 2) continue;
                    if (st == 1) {
                        ll val = tab1[i][st] + A;
                        if (val > nd[0]) { nd[0] = val; pd[0] = st; }
                    } else {
                        ll val = tab1[i][st] + best;
                        if (val > nd[0]) { nd[0] = val; pd[0] = st; }
                        ll v2 = tab1[i][st] + A + wi;
                        if (v2 > nd[1]) { nd[1] = v2; pd[1] = st; }
                    }
                }
                tab1[i + 1] = nd; pred1[i + 1] = pd;
            }
            ll v0 = tab0[L][0];
            ll v1 = (tab1[L - 1][0] <= NEG / 2 ? NEG : tab1[L - 1][0] + dp0[cyc[L - 1]]);
            if (v1 > v0) {
                // wrap 边 (cyc[L-1], cyc[0]) 被使用
                usedNext[L - 1] = 1; usedPrev[0] = 1;
                int i = L - 1, st = 0;
                while (i > 0) {
                    int p = pred1[i][st];
                    if (st == 1) { usedNext[i - 1] = 1; usedPrev[i % L] = 1; }
                    else if (p == 1) { usedPrev[i - 1] = 1; }
                    i -= 1; st = p;
                }
            } else {
                int i = L, st = 0;
                while (i > 0) {
                    int p = pred0[i][st];
                    if (st == 1) { usedNext[i - 1] = 1; usedPrev[i % L] = 1; }
                    else if (p == 1) { usedPrev[i - 1] = 1; }
                    i -= 1; st = p;
                }
            }
            for (int k = 0; k < L; ++k)
                if (usedNext[k]) pairs.push_back({cyc[k], cyc[(k + 1) % L]});
        }
        // 环上没被环边用掉的节点，可以选择连自己的孩子
        for (int k = 0; k < L; ++k) {
            int c = cyc[k];
            if (usedNext[k] || usedPrev[k]) continue;
            if (bestChoice[c] == 1) matchedParent[gainChild[c]] = 1;
        }
    }

    // 自顶向下决定树上的匹配
    for (int idx = (int)order.size() - 1; idx >= 0; --idx) {
        int u = order[idx];
        if (matchedParent[u]) continue;
        if (bestChoice[u] == 1) matchedParent[gainChild[u]] = 1;
    }
    for (int u = 1; u <= n; ++u)
        if (matchedParent[u]) pairs.push_back({u, f[u]});

    // 统计
    int t = 0, e = 0;
    for (auto& pr : pairs) {
        ++t;
        if (sex[pr.first] != sex[pr.second]) ++e;
    }
    cout << t << ' ' << e << '\n';
    for (auto& pr : pairs) cout << pr.first << ' ' << pr.second << '\n';
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
    n = int(data[0])
    f = [0] * (n + 1)
    sex = [0] * (n + 1)
    inL = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    pos = 1
    for i in range(1, n + 1):
        f[i] = int(data[pos]); sex[i] = int(data[pos + 1]); pos += 2
        inL[f[i]].append(i)
        indeg[f[i]] += 1

    MULT = n + 1                     # 先最大化对数，再最大化男女混合对数
    NEG = -(1 << 60)

    def w(u, v):
        return MULT + (1 if sex[u] != sex[v] else 0)

    # 拓扑剥叶子：剩下的就是环上的点
    order = [i for i in range(1, n + 1) if indeg[i] == 0]
    head = 0
    while head < len(order):
        u = order[head]; head += 1
        p = f[u]
        indeg[p] -= 1
        if indeg[p] == 0:
            order.append(p)
    on_cycle = [indeg[i] > 0 for i in range(n + 1)]

    dp0 = [0] * (n + 1)              # 环上节点存 A；树上节点存"自由"
    dp1 = [NEG] * (n + 1)            # 环上节点存 B；树上节点存"连一个孩子"
    best_choice = [0] * (n + 1)
    gain_child = [-1] * (n + 1)
    matched_parent = [False] * (n + 1)
    pairs = []

    # 树的 DP：order 中孩子先于父亲
    for u in order:
        base = 0
        for v in inL[u]:
            base += dp0[v] if dp0[v] > dp1[v] else dp1[v]
        dp0[u] = base
        best_gain = NEG
        arg = -1
        for v in inL[u]:
            b = dp0[v] if dp0[v] > dp1[v] else dp1[v]
            g = w(u, v) + dp0[v] - b
            if g > best_gain:
                best_gain = g
                arg = v
        dp1[u] = NEG if arg < 0 else base + best_gain
        gain_child[u] = arg
        best_choice[u] = 1 if dp1[u] > dp0[u] else 0

    seen = [False] * (n + 1)
    for s in range(1, n + 1):
        if not on_cycle[s] or seen[s]:
            continue
        cyc = []
        u = s
        while not seen[u]:
            seen[u] = True
            cyc.append(u)
            u = f[u]
        L = len(cyc)

        # 环上节点的"树部分"（排除环上的前驱）
        for c in cyc:
            base = 0
            for v in inL[c]:
                if not on_cycle[v]:
                    base += dp0[v] if dp0[v] > dp1[v] else dp1[v]
            dp0[c] = base
            best_gain = NEG
            arg = -1
            for v in inL[c]:
                if on_cycle[v]:
                    continue
                b = dp0[v] if dp0[v] > dp1[v] else dp1[v]
                g = w(c, v) + dp0[v] - b
                if g > best_gain:
                    best_gain = g
                    arg = v
            dp1[c] = NEG if arg < 0 else base + best_gain
            gain_child[c] = arg
            best_choice[c] = 1 if dp1[c] > dp0[c] else 0

        used_next = [0] * L
        used_prev = [0] * L
        if L == 2:
            c0, c1 = cyc[0], cyc[1]
            no = (dp0[c0] if dp0[c0] > dp1[c0] else dp1[c0]) + (dp0[c1] if dp0[c1] > dp1[c1] else dp1[c1])
            use = dp0[c0] + dp0[c1] + w(c0, c1)
            if use > no:
                used_next[0] = 1
                used_prev[1] = 1
                pairs.append((c0, c1))
        else:
            # 情况 0：wrap 边不用；情况 1：wrap 边使用
            tab0 = [[NEG, NEG] for _ in range(L + 1)]
            tab1 = [[NEG, NEG] for _ in range(L)]
            pred0 = [[-1, -1] for _ in range(L + 1)]
            pred1 = [[-1, -1] for _ in range(L)]
            tab0[0][0] = 0
            for i in range(L):
                ci = cyc[i]
                A, B = dp0[ci], dp1[ci]
                best = A if A > B else B
                wi = w(ci, cyc[(i + 1) % L])
                nd = [NEG, NEG]
                pd = [-1, -1]
                for st in (0, 1):
                    cur = tab0[i][st]
                    if cur <= NEG // 2:
                        continue
                    if st == 1:
                        val = cur + A
                        if val > nd[0]:
                            nd[0] = val; pd[0] = st
                    else:
                        val = cur + best
                        if val > nd[0]:
                            nd[0] = val; pd[0] = st
                        if i < L - 1:
                            v2 = cur + A + wi
                            if v2 > nd[1]:
                                nd[1] = v2; pd[1] = st
                tab0[i + 1] = nd
                pred0[i + 1] = pd
            tab1[0][1] = w(cyc[L - 1], cyc[0])      # 只记 wrap 边权
            for i in range(L - 1):
                ci = cyc[i]
                A, B = dp0[ci], dp1[ci]
                best = A if A > B else B
                wi = w(ci, cyc[i + 1])
                nd = [NEG, NEG]
                pd = [-1, -1]
                for st in (0, 1):
                    cur = tab1[i][st]
                    if cur <= NEG // 2:
                        continue
                    if st == 1:
                        val = cur + A
                        if val > nd[0]:
                            nd[0] = val; pd[0] = st
                    else:
                        val = cur + best
                        if val > nd[0]:
                            nd[0] = val; pd[0] = st
                        v2 = cur + A + wi
                        if v2 > nd[1]:
                            nd[1] = v2; pd[1] = st
                tab1[i + 1] = nd
                pred1[i + 1] = pd
            v0 = tab0[L][0]
            v1 = NEG if tab1[L - 1][0] <= NEG // 2 else tab1[L - 1][0] + dp0[cyc[L - 1]]
            if v1 > v0:
                used_next[L - 1] = 1
                used_prev[0] = 1
                i, st = L - 1, 0
                while i > 0:
                    p = pred1[i][st]
                    if st == 1:
                        used_next[i - 1] = 1
                        used_prev[i % L] = 1
                    elif p == 1:
                        used_prev[i - 1] = 1
                    i -= 1
                    st = p
            else:
                i, st = L, 0
                while i > 0:
                    p = pred0[i][st]
                    if st == 1:
                        used_next[i - 1] = 1
                        used_prev[i % L] = 1
                    elif p == 1:
                        used_prev[i - 1] = 1
                    i -= 1
                    st = p
            for k in range(L):
                if used_next[k]:
                    pairs.append((cyc[k], cyc[(k + 1) % L]))
        for k in range(L):
            c = cyc[k]
            if used_next[k] or used_prev[k]:
                continue
            if best_choice[c] == 1:
                matched_parent[gain_child[c]] = True

    # 自顶向下决定树上的匹配
    for idx2 in range(len(order) - 1, -1, -1):
        u = order[idx2]
        if matched_parent[u]:
            continue
        if best_choice[u] == 1:
            matched_parent[gain_child[u]] = True
    for u in range(1, n + 1):
        if matched_parent[u]:
            pairs.append((u, f[u]))

    t = len(pairs)
    e = sum(1 for a, b in pairs if sex[a] != sex[b])
    out = [f"{t} {e}"]
    for a, b in pairs:
        out.append(f"{a} {b}")
    sys.stdout.write("\n".join(out) + "\n")


main()
```

两份代码都只用标准库，可原样提交。注意 Python 版对 $n = 10^5$ 的深链没有递归，使用的是迭代式 DP。

## 7. 边界情况与易错点

1. **$2$ 环（两个学生互为好友）**：无向图里只有一条边，按"$L = 2$ 的环"跑环上 DP 会把同一条边算两次（$e_0$ 与 $e_1$ 是同一条边）。必须特判成"两个点之间至多配一对"。
2. **奖金编码的基数**：用 $M = n + 1$，必须保证 $e < M$。若写成 $M = 2$（只区分有没有混合），最大化总权就变成"混合对的个数优先"，与题目要求相反。
3. **环上 DP 的两种情况的初始化**：情况 1（`wrap` 边使用）里 $c_0$ 的贡献是 $A[c_0]$，且 `wrap` 边的权只算一次；第一版实现里把 $A[c_0]$ 既放在初值里又在转移里加了一遍，导致权值虚高、选错方案（随机对拍立刻发现）。
4. **`usedNext`/`usedPrev` 与索引**：`wrap` 边对应的是 `usedNext[L-1]` 与 `usedPrev[0]`；若误标成 `usedNext[0]`，会同时把 $c_0$ 与 $c_1$ 的环边也算上，输出里同一个学生出现两次。
5. **树与环分界**：环上节点的"孩子"必须排除它在环上的前驱（即 `f[prev] = c` 的那个点）；否则环边会被当成树边重复考虑。
6. **`dp1` 的 $-\infty$**：没有孩子时 $dp_1$ 无意义，必须用足够小的负数（代码用 `LLONG_MIN/4` 防止加法溢出），且比较时不要把它当成可行值。
7. **还原顺序**：树上的还原必须"父亲先于孩子"（按剥叶拓扑序的**逆序**），否则父亲占用某个孩子后，孩子还会错误地再去连自己的孩子。
8. **输出格式**：第一行两个数 $t, e$；接下来 $t$ 行每行一对。对内的两个数顺序任意，对与对的顺序任意，但必须每个学生至多出现一次。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：3 / 3 通过。三组样例的 $(t, e)$ 分别是 $(2,2)$、$(3,1)$、$(4,1)$，与题面一致；输出的配对也逐对检查过合法性。
- **checker**：`codeforces/tools/checkers/cf81e.py`，校验三条：① 每对必须是好友关系（$f_a = b$ 或 $f_b = a$）、每个学生至多出现一次；② 声明的 $t$、$e$ 与实际对数、实际男女搭配对数一致；③ $(t, e)$ 必须等于官方答案的最优值（没有官方答案时，小数据用"枚举所有边集"的暴力独立求最优再比对）。本地验证时用 `verify_solution.py <doc> --checker codeforces/tools/checkers/cf81e.py`，样例 3 / 3 通过（输出的具体配对与样例不同，但 $(t,e)$ 一致、方案合法）。
- **额外测试（与暴力对拍）**：另写暴力——枚举所有边集子集（边数 $\le 12$ 时最多 $2^{12}$ 种），取出所有匹配并按 $(t, e)$ 字典序取最优；对 **2000 组**随机小规模输入（$2 \le n \le 12$，随机函数图与混合性别，包含大量 2 环、纯树、纯大环、星形等结构）与 C++ 实现比对，**2000 / 2000 全部一致**；同时校验输出方案本身（每对必须是好友、每个学生至多一次、$(t,e)$ 与暴力一致）。
- **C++ / Python 一致性**：$n = 10^5$ 的随机大输入上两个实现输出完全一致（$t = 43314$，$e = 26918$）。
- **最大约束性能**：$n = 10^5$ 的随机函数图（输入 $7.9 \times 10^5$ 字节），C++ 端到端 15 次平均 $337.6$ ms，Python $185.6$ ms（含进程启动与输入解析）。C++ 的读入单独插桩测得 $322.7$ ms，即耗时几乎全在本机 libc++ 的 iostream 上；相对 1 s 时限仍有约 3 倍余量。
- **图片校验**：三张 SVG（`cf81e_structure.svg`、`cf81e_dp.svg`、`cf81e_walkthrough.svg`）通过 `xml.etree.ElementTree.parse`，文本块估算未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError: true`）渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 161D Distance in Tree](https://codeforces.com/problemset/problem/161/D)：树上计数 DP 的入门，与本题的树形 DP 同源。
- [Codeforces 1084D The Fair Nut and the Best Path](https://codeforces.com/problemset/problem/1084/D)：树上路径/子树 DP，练习状态设计。
- [Codeforces 835F Roads in the Kingdom](https://codeforces.com/problemset/problem/835/F)：基环树 + 环上 DP，与本题的"环 + 树"结构完全一致。
- [LeetCode 198. 打家劫舍](https://leetcode.cn/problems/house-robber/)：线状 DP 的"选/不选"状态，是环上 DP 的最简版本。
- [LeetCode 213. 打家劫舍 II](https://leetcode.cn/problems/house-robber-ii/)：把线变成环，用"分两种情况（首尾是否同时选）"破环——与本题环上 DP 的破环技巧一模一样。

**延伸思考**：

1. **如果每个学生可以出现在多对里**（即求"最大边集使每个点度数 $\le k$"）：DP 状态要从"是否被父亲占用"扩展成 $0..k$ 个占用数，复杂度变成 $O(nk^2)$。
2. **如果除"对数"与"混合对数"外还有第三个目标**（例如尽量让好朋友编号小）：把权值编码改成三进制即可，只要每一级的基数大于下一级的最大值，字典序与标量和就等价。
3. **如果图不是函数图而是任意图**：基环树 DP 不再适用，需要一般图最大匹配（带花树），$n = 10^5$ 无法在 1 s 内完成——本题的结构假设是全部效率的来源。
4. **如果要求输出"字典序最小"的配对方案**：在 DP 值相同的情况下需要额外的取舍规则（例如优先让小编号的学生与他的好友配对），这会让还原过程复杂不少，但仍是 $O(n)$ 的。
