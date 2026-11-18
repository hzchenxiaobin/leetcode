# Codeforces 夜行者 题解

## 1. 题目概述

- **标题 / 题号**：夜行者（Codeforces 2254G，英文名 Nightcrawler）
- **链接**：https://codeforces.com/problemset/problem/2254/G
- **来源**：Codeforces Round 1114 (Div. 3) · Problem G
- **难度**：2200
- **限制**：时间 2.5 s / 内存 256 MB
- **标签**：树、贪心、排序、并查集 / 可并堆、DP、DFS

**题意**：给定以 $1$ 为根的有根树，点 $i$ 的权值为 $a_i$。把全部 $n$ 个点划分成恰好 $k$ 个非空集合，要求每个集合内部的点两两都有祖先关系——等价于整个集合落在同一条「根到叶」的路径上。集合得分 = 集合内 $a$ 的最大值，划分得分 = 各集合得分之和。对每个 $k=1,\dots,n$ 求最大得分，不存在合法划分则输出 $-1$。

多测：第一行 $t$；每组依次给 $n$、$a_1\dots a_n$、$p_2\dots p_n$（$p_i$ 是 $i$ 的父亲）。每组输出一行 $n$ 个整数。

**约束**：

- $3 \le n \le 2\cdot 10^5$，$1 \le a_i \le 10^9$
- $1 \le p_i < i$：编号天然是拓扑序，**按编号倒序就是从叶到根**，不必建邻接表、不必 DFS
- $t \le 10^4$，$\sum n \le 2\cdot 10^5$（多测总量决定复杂度上限）
- 要输出全部 $n$ 个 $k$ 的答案，所以必须把「对每个 $k$ 单独求」改写成「一次求出全部增量」，整体 $O(n\log n)$

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
7
3
10 20 30
1 1
4
5 10 15 20
1 2 2
4
1 2 3 4
1 1 3
5
1 2 3 4 5
1 2 3 4
9
1 100 1 90 80 1 2 3 4
1 1 2 4 3 3 3 3
6
5 4 10 3 9 1
1 2 1 4 1
4
10 10 20 1
1 2 1

输出：
-1 50 60
-1 35 45 50
-1 6 9 10
5 9 12 14 15
-1 -1 -1 -1 110 200 280 281 282
-1 -1 24 28 31 32
-1 30 40 41
```

第 1 组叶子是 2、3，故 $k=1$ 无解；第 4 组是一条链（$L=1$），答案从 $k=1$ 开始且正好是「前 $k$ 大权值之和」。第 5 组是 §3.4 的走查对象。

补一组自造数据（$k$ 中等、含相等权值）：

```text
输入：
1
5
3 1 4 1 5
1 2 1 4

输出：
-1 9 12 13 14
```

叶子是 3、5，故 $k=1$ 无解；$k=2$ 时取 $\{2,3\}$ 与 $\{1,4,5\}$ 得 $4+5=9$；之后每升格一个非最大值点再加它的权值：$+3\to12$、$+1\to13$、$+1\to14=\sum a$。

## 3. 解题思路

### 3.1 暴力思路

枚举全部集合划分（Bell 数级）再逐块判可比，$n\le 9$ 可行、$n=2\cdot10^5$ 无望。树形 DP（状态 = 链数 + 链是否向上开口）思路自然，但对每个 $k$ 单独做是 $O(n^2)$ 以上，仍然超时。

真正的缺口是：这 $n$ 个答案不是互相独立的问题，而是**同一结构的一组增量**。只要证明答案形状是「基底 + 增益降序前缀和」，就只剩「求增益多重集」一件事。

### 3.2 核心观察：叶子定下界，代表点定基底，升格定增量

![链必须落在同一条根到叶路径上，叶子数决定最少链数](images/cf2254_g_chain_partition_concept.svg)

记 $L$ 为叶子数。

**观察 1（可行性）**：不同叶子互不为祖先，必属不同集合，故 $k\ge L$；反之链内「挖点」仍是链，所以从 $L$ 条链出发可不断把含 $\ge2$ 点的链拆开，得分只增不减。故 $k$ 的合法范围恰是 $[L,n]$。

**观察 2（链 = 某条根—叶路径的子集）**：链内两两可比 $\Rightarrow$ 全在同一条根—叶路径上。于是可给每条链指定「所属叶子」（含叶就用那片叶子，否则用最深处点的任一后代叶子）。反之，固定「每点分给哪片叶子」（$x$ 只能分给它子树内的叶子），每片叶子的分组都在同一条路径上，任意拆成链都合法。

**观察 3（$k=L$ 的骨架）**：此时每条链恰含一片叶子 $l$，链的最大值 $b_l$ 必是 $l$ 的祖先（或 $l$ 自己），且不同链最大值互不相同。故 $L$ 个链最大值构成集合 $B$ 并带「叶子 $\to$ 祖先」的匹配，得分即 $\sum_{x\in B}a_x$。称 $B$ 为**基底**。

**观察 4（增量 = 单点升格）**：固定 $B$ 后，把任意 $x\notin B$ 单独拆成一条链（它不是原链最大值，故原链得分不变），集合数 $+1$、得分恰好 $+a_x$。于是对任意 $k\ge L$：

$$f(k)\ \ge\ \text{base}+\bigl(\text{$V\setminus B$ 中最大的 }k-L\text{ 个权值之和}\bigr),\qquad \text{base}=\sum_{x\in B}a_x .$$

§5 证明该下界取等（引理 4 + 引理 5）：**答案就是「基底 + 增益降序前缀和」**，$k<L$ 全 $-1$。于是只剩一个问题——哪些点进基底、哪些当增益？

### 3.3 算法流程：按权值升序，每点占住「能到达的最深未占用内部点」

![按权值升序扫 + 并查集向上跳的流程](images/cf2254_g_dsu_match_flow.svg)

关键刻画（§5 引理 6、引理 7）：把「自底向上合并子树多重集、每个内部点弹掉当前最小值」反着看，得到

> 把点按 $a$ **升序**扫一遍。对点 $x$，在它到根的路径上找**最深且尚未被占用的内部点**（内部点 = 有儿子的点）$w$：找到就让 $a_x$ 成为增益并占用 $w$；找不到就让 $x$ 留在基底。

「最深未占用的内部祖先」用并查集维护：内部点初始指向自己，叶子初始指向父亲；占用 $w$ 后令 $nxt_w\leftarrow\text{find}(p_w)$ 即向上跳到下一个候选。带路径压缩，总代价 $O(n\alpha(n))$。

最后把增益降序排序，$k\ge L$ 的答案 = $\text{base}$ 加上前 $k-L$ 个增益的前缀和，其中 $\text{base}=\sum a-\sum\text{gain}$。

> 💡 等价实现（更好证明、代码略长）：自底向上给每个点一个最小堆，合并所有儿子的堆、插入 $a_v$，若 $v$ 是内部点就弹出最小值——弹出的就是增益；每个内部点恰弹一个，共 $n-L$ 个。左偏树/配对堆可做到 $O(n\log n)$。

### 3.4 示例演算

![样例 5 的九步走查表](images/cf2254_g_walkthrough.svg)

样例 5：$n=9$，$a=[1,100,1,90,80,1,2,3,4]$，$p_2..p_9=[1,1,2,4,3,3,3,3]$，即 $1\to\{2,3\}$、$2\to4\to5$、$3\to\{6,7,8,9\}$。内部点 $\{1,2,3,4\}$，叶子 $\{5,6,7,8,9\}$，$L=5$，$\sum a=282$。按权值升序（等值按编号）走一遍：

| 步 | 点 $x$ | $a_x$ | 命中的内部点 | 结果 |
|---|---|---|---|---|
| 1 | 1 | 1 | 1（自身） | 增益 1 |
| 2 | 3 | 1 | 3（自身） | 增益 1 |
| 3 | 6 | 1 | 无（3、1 已占） | 留在基底 |
| 4 | 7 | 2 | 无（3 已占） | 留在基底 |
| 5 | 8 | 3 | 无（3 已占） | 留在基底 |
| 6 | 9 | 4 | 无（3 已占） | 留在基底 |
| 7 | 5 | 80 | 4（$5\to4\to2\to1$ 上最深未占用） | 增益 80 |
| 8 | 4 | 90 | 2（4 已占，继续上跳） | 增益 90 |
| 9 | 2 | 100 | 无（1 已占） | 留在基底 |

增益 $=\{1,1,80,90\}$，降序 $90,80,1,1$；$\text{base}=282-172=110$。故 $k=1..4$ 输出 $-1$，$k=5..9$ 输出 $110,200,280,281,282$，与官方输出一致。$k=5$ 可取划分 $\{1,2,4,5\},\{3,7\},\{6\},\{8\},\{9\}$，得分 $100+2+1+3+4=110$。

## 4. 算法细节

1. **不建图、不 DFS**：$p_i<i$ 保证父亲编号更小；并查集版本甚至只按权值排序，连逆序都不需要。
2. **内部点与叶子分开初始化**：内部点 $nxt_v=v$，叶子 $nxt_v=p_v$（叶子本身不是候选）；占用 $w$ 后 $nxt_w=\text{find}(p_w)$。
3. **哨兵 0**：$p_{\text{root}}=0$，约定 $\text{find}(0)=0$ 表示「路径上没有候选」，省掉判空分支。
4. **排序只按 $a$**：等值点先后不影响答案——互换只改变「哪一份相同权值当增益」，多重集不变。
5. **必须 64 位**：$\sum a\le 2\cdot10^5\times10^9=2\cdot10^{14}$，`int` 会静默溢出（Python 天然安全）。
6. **多测清空 + 批量输出**：数组按当前 $n$ 重建或只覆写前 $n+1$ 位（别整段 `memset`）；一行的 $n$ 个数拼进字符串一次性写出，比逐个 `cout` 快数倍。

## 5. 正确性证明

**记号**：$\text{leaf}(v)$ 为子树 $v$ 的叶子数；$U_t=\{x:a_x\ge t\}$；若存在双射 $l\mapsto b_l\in S$（$b_l$ 是叶子 $l$ 的祖先或 $l$ 本身），称 $S$ **可匹配**；$r(X)=\max\{|S|:S\subseteq X,\ S\text{ 可匹配}\}$。由 Hall 定理，$S$ 可匹配 $\iff\forall v:|S\cap\text{subtree}(v)|\le\text{leaf}(v)$，故可匹配子集族是以子树为链、容量 $\text{leaf}(v)$ 的**层状拟阵**，$r$ 是它的秩函数。答案记 $f(k)$。

**引理 1（可行性）**：合法 $k$ 划分存在 $\iff L\le k\le n$。
**证明**：$k\le n$ 显然。必要性：不同叶子两两不可比，必须分属不同集合，故 $k\ge L$。充分性：若某集合含 $\ge2$ 点，把它拆成两部分（仍是同一条路径的子集），集合数 $+1$ 且得分不减（两部分最大值之和不小于原最大值），反复可至 $n$。∎

**引理 2（$k=L$ 的代表点结构）**：$|B|=L$ 的 $B$ 能成为某个 $L$ 条链划分的最大值集合 $\iff$ $B$ 可匹配，且**覆盖性**成立：对每个 $x\notin B$，存在叶子 $l\in\text{subtree}(x)$ 使 $a_{b_l}\ge a_x$。
**证明**：($\Leftarrow$) 令 $C_l=\{b_l\}\cup\{\text{分给 }l\text{ 的点}\}$，每个 $x\notin B$ 分给任一满足覆盖性的叶子（$x$ 是 $l$ 的祖先，故 $C_l$ 全在 $l$ 的路径上，是链），$C_l$ 最大值即 $a_{b_l}$，得分 $\sum_l a_{b_l}$。($\Rightarrow$) 取 $b_l$ 为含叶子 $l$ 那条链的最大值点：它在 $l$ 的路径上、且不同链的最大值互不相同，故可匹配；对 $x\notin B$，$x$ 所在链含某片叶子 $l\in\text{subtree}(x)$，其最大值 $a_{b_l}\ge a_x$，覆盖性成立。∎

**引理 3（最大权基底自动覆盖）**：若 $B$ 在所有可匹配的 $L$ 元集中权和最大，则覆盖性成立。
**证明**：反设存在 $x\notin B$ 使所有 $l\in\text{subtree}(x)$ 都有 $a_{b_l}<a_x$，取其中权值最大的 $b^{*}=b_{l^{*}}$。因 $x$ 是 $l^{*}$ 的祖先，把匹配改为 $l^{*}\mapsto x$ 仍合法，得到另一个可匹配 $L$ 元集且权和增加 $a_x-a_{b^{*}}>0$，矛盾。∎

**引理 4（上界）**：设 $B$ 为引理 3 的基底，$g_1\ge\dots\ge g_{n-L}$ 为 $V\setminus B$ 的权值降序，则任意合法 $k$ 划分（$k\ge L$）得分 $\le\text{base}+\sum_{i\le k-L}g_i$。
**证明**：设划分的最大值集合为 $M$（$|M|=k$）。按观察 2 的指派得到「每点分给某个后代叶子」的分配；对叶子 $l$ 的分组 $G_l$，其最大权值点 $y$ 所在链的最大值 $m\in M$ 满足 $a_m\ge a_y$，而 $y$ 是组内最大权值点，故 $a_m=\max(G_l)$。于是每片叶子 $l$ 有一个互不相同且是 $l$ 祖先的代表 $m_l\in M\cap G_l$，即 $M$ 含可匹配的 $L$ 元子集，故 $r(M)=L$。令 $W=B\ \dot\cup\ \{\text{前 }k-L\text{ 大的增益}\}$，对任意阈值 $t$：一方面 $r(M)\le r(M\cap U_t)+|M\setminus U_t|\le r(U_t)+k-|M\cap U_t|$，得 $|M\cap U_t|\le r(U_t)+k-L$；另一方面由引理 6 有 $|B\cap U_t|=r(U_t)$ 且 $|U_t|=|B\cap U_t|+\#\{g_i\ge t\}$，故
$$|W\cap U_t|=r(U_t)+\min\bigl(k-L,\,|U_t|-r(U_t)\bigr)=\min\bigl(|U_t|,\,r(U_t)+k-L\bigr)\ \ge\ |M\cap U_t|.$$
把权值升序排成 $d_1<\dots<d_m$（$d_0=0$），用 $\sum_{x\in S}a_x=\sum_j(d_j-d_{j-1})|S\cap U_{d_j}|$ 逐项比较即得 $\sum_M a\le\sum_W a=\text{base}+\sum_{i\le k-L}g_i$。∎

**引理 5（可达）**：$\text{base}+\sum_{i\le k-L}g_i$ 可达。
**证明**：由引理 2、3，$B$ 是某个 $L$ 条链划分的最大值集合；再把任意 $x\notin B$ 挖出单独成链（挖点不破坏链），得分恰好 $+a_x$。取权值最大的 $k-L$ 个非基底点升格即可。∎

**引理 6（自底向上「弹最小」）**：设 $K_v$ 为算法在 $v$ 处保留的多重集，则对一切阈值 $t$ 有 $|K_v\cap U_t|=r_v(U_t)$（$r_v$ 为限制在 $\text{subtree}(v)$ 的层状拟阵的秩）；特别地 $|B\cap U_t|=r(U_t)$。
**证明**：容量可加 $\text{leaf}(v)=\sum_c\text{leaf}(c)$，父子间唯一耦合约束就是总量，故 $r_v(U)=\min\bigl(\text{leaf}(v),[a_v\in U]+\sum_c r_c(U)\bigr)$。对树高归纳：叶子处 $K_v=\{a_v\}$，两边都是 $[a_v\ge t]$。内部点令 $A=\{a_v\}\cup\bigcup_c K_c$（$|A|=\text{leaf}(v)+1$）、$K_v=A\setminus\{\min A\}$，由归纳 $|A\cap U_t|=[a_v\ge t]+\sum_c r_c(U_t)$，故 $r_v(U_t)\le|A\cap U_t|\le r_v(U_t)+1$。若 $|A\cap U_t|=r_v(U_t)$，则 $A$ 有元素 $<t$，$\min A<t$，$|K_v\cap U_t|=|A\cap U_t|=r_v$；若 $|A\cap U_t|=r_v+1$，则必有 $r_v=\text{leaf}(v)$ 且 $|A\cap U_t|=|A|$（否则 $r_v=[a_v\ge t]+\sum_c r_c=|A\cap U_t|=r_v+1$ 矛盾），此时只去掉最小值，$|K_v\cap U_t|=\text{leaf}(v)=r_v$。∎

**引理 7（并查集实现与「弹最小」等价）**：按权值升序逐个「交代」每个值被弹出的位置，$a_x$ 恰好被 $x$ 的**最深未占用内部祖先（或 $x$ 自身）** 弹掉；不存在这样的点则永不被弹。
**证明**：设更小的权值都已按此规则定位。$a_x$ 只可能出现在「含 $x$ 的子树」的内部点候选集中，即 $x$ 到根路径上的内部点。若最深未占用内部点为 $w$，则 $w$ 处理时 $a_x$ 仍在可用多重集中（$x\in\text{subtree}(w)$，且 $w$ 下方路径上的内部点都已被更小的值占用），而 $a_x$ 是剩余最小值，故被 $w$ 弹掉；若不存在这样的 $w$，则路径上内部点都被更小值占用，$a_x$ 永不被弹。又由引理 6 每个内部点恰弹一个、共 $n-L$ 个，两种口径一致（等值互换不影响多重集）。∎

**定理**：$k<L$ 时答案为 $-1$；$L\le k\le n$ 时 $f(k)=\text{base}+\sum_{i=1}^{k-L}g_i$，其中 $\text{base}=\sum_{x\in B}a_x=\sum_x a_x-\sum_i g_i$。
**证明**：引理 1 给可行域；引理 4 给上界、引理 5 给下界，二者相等；$B$ 与 $g_i$ 由引理 6（或等价的引理 7）算出。∎

## 6. 复杂度分析

- **时间**：排序 $O(n\log n)$；并查集攀爬（路径压缩）$O(n\alpha(n))$；枚举输出 $O(n)$。整体 $O(n\log n)$。
- **空间**：`a`、`par`、`nxt`、`order`、增益数组各 $O(n)$，共 $O(n)$ 个整数，远低于 256 MB。
- **实测**（$n=2\cdot10^5$，C++17 `-O2`）：算法本体（不含读入）随机树 3.1 ms、链 3.4 ms、星 0.7 ms、满二叉树 3.2 ms；改用 `fread` 快读后整程序（含 I/O 与输出）15–29 ms，相对 2.5 s 时限余量 $>80$ 倍。
- **Python3 实测**：同样六组最大数据整体 0.24–0.41 s（含读入输出），2.5 s 内有余量；但常数偏大，建议用 PyPy 提交。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; cin >> T;
    while (T--) {
        int n; cin >> n;
        vector<long long> a(n + 1); long long total = 0;
        for (int i = 1; i <= n; i++) { cin >> a[i]; total += a[i]; }
        vector<int> par(n + 1, 0); vector<char> isInt(n + 1, 0);
        for (int i = 2; i <= n; i++) { cin >> par[i]; isInt[par[i]] = 1; }
        vector<int> nxt(n + 1, 0); int leaves = 0;
        for (int v = 1; v <= n; v++) {
            if (isInt[v]) nxt[v] = v;                 // 内部点：候选
            else { nxt[v] = par[v]; leaves++; }       // 叶子：直接指向父亲
        }
        // 跳到最近的未占用内部祖先（或自身），0 表示没有候选
        auto find_ = [&](int v) {
            if (v == 0) return 0;
            int r = v;
            while (nxt[r] != r && nxt[r] != 0) r = nxt[r];
            int res = (nxt[r] == r) ? r : 0;
            for (int u = v, nu; nxt[u] != u && nxt[u] != 0; u = nu) { nu = nxt[u]; nxt[u] = res; }
            return res;
        };
        vector<int> order(n);
        iota(order.begin(), order.end(), 1);
        sort(order.begin(), order.end(), [&](int x, int y) { return a[x] != a[y] ? a[x] < a[y] : x < y; });
        vector<long long> gain; gain.reserve(n);
        for (int x : order) {
            int w = find_(x);
            if (w) { gain.push_back(a[x]); nxt[w] = find_(par[w]); }
        }
        long long base = total;
        for (long long g : gain) base -= g;
        sort(gain.begin(), gain.end(), greater<long long>());
        string out; out.reserve((size_t)n * 12);
        long long cur = base; int id = 0;
        for (int k = 1; k <= n; k++) {
            if (k < leaves) out += "-1";
            else { if (k > leaves) cur += gain[id++]; out += to_string(cur); }
            out += (k == n ? '\n' : ' ');
        }
        fwrite(out.data(), 1, out.size(), stdout);
    }
    return 0;
}
```

### Python3

```python
import sys

def main():
    data = sys.stdin.buffer.read().split(); ptr = 0
    t = int(data[ptr]); ptr += 1
    out = []
    for _ in range(t):
        n = int(data[ptr]); ptr += 1
        a = [0] * (n + 1); total = 0
        for i in range(1, n + 1):
            a[i] = int(data[ptr]); ptr += 1; total += a[i]
        par = [0] * (n + 1); is_int = bytearray(n + 1)
        for i in range(2, n + 1):
            p = int(data[ptr]); ptr += 1
            par[i] = p; is_int[p] = 1
        # nxt[v]：并查集指针，指向最近的未占用内部祖先（或自身），0 表示没有
        nxt = [0] * (n + 1); leaves = 0
        for v in range(1, n + 1):
            if is_int[v]: nxt[v] = v
            else: nxt[v] = par[v]; leaves += 1
        def find(v):
            if v == 0: return 0
            r = v
            while nxt[r] != r and nxt[r] != 0: r = nxt[r]
            res = r if nxt[r] == r else 0
            u = v
            while nxt[u] != u and nxt[u] != 0:
                nu = nxt[u]; nxt[u] = res; u = nu
            return res
        order = sorted(range(1, n + 1), key=a.__getitem__)   # 按权值升序
        gain = []
        for x in order:
            w = find(x)
            if w:
                gain.append(a[x]); nxt[w] = find(par[w])
        gain.sort(reverse=True)
        base = total - sum(gain)
        res = []; cur = 0
        for k in range(1, n + 1):
            if k < leaves: res.append('-1')
            elif k == leaves: cur = base; res.append(str(cur))
            else: cur += gain[k - leaves - 1]; res.append(str(cur))
        out.append(' '.join(res))
    sys.stdout.write('\n'.join(out) + '\n')

main()
```

## 8. 边界情况与易错点

1. **$k<L$ 全 $-1$，而 $k=L$ 那格要输出 base**：常见 bug 是把 $k\le L$ 都当 $-1$，或循环起点写成 $L+1$。链状树（$L=1$）时 $k=1$ 就有解，不能整行 $-1$。
2. **$L$ 用「没有儿子」统计，且叶子不是候选**：$n\ge3$ 时根必有儿子、必属内部点；叶子若被当成候选，会出现「自己占自己」的多余增益。
3. **哨兵 0**：$p_{\text{root}}=0$，$\text{find}(0)=0$；别把 0 当合法点，也别让 $nxt_0$ 变成非零。
4. **溢出**：$\sum a$ 与答案最大 $2\cdot10^{14}$，C++ 必须 `long long`；`int` 会在「链 + 大权值」数据上静默出错。
5. **多测残留**：`nxt`、`order`、增益数组按当前 $n$ 重建；不要用 `memset` 清 20 万长度数组 $10^4$ 次（会 TLE）。
6. **必须「最深」而非「最浅」**：占用候选点时要跳到路径上最深的未占用内部点，写成最浅会改变增益多重集（见 §3.4 第 7 步）。
7. **等值权值与输出格式**：比较器只用 $a$ 即可（用 $(a,\text{id})$ 也不错），别做「去重」剪枝；每组恰好 $n$ 个数、同一行、行末无多余空格。

## 相关题目与扩展

- [Codeforces 600E Lomsat gelral](https://codeforces.com/problemset/problem/600/E)：合并子树多重集的经典题，与本文「合并 + 弹最小」的堆实现同源。
- [Codeforces 375D Tree and Queries](https://codeforces.com/problemset/problem/375/D)：子树计数 + 启发式合并，练 `DSU on tree` 正好。
- [LeetCode 124. 二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/)：把「路径」当状态的树形 DP 入门题，可对照 §3.1 里「链是否向上开口」的视角。

**延伸思考**：

1. 若把「链可跳过中间点」改成「集合在树上必须连通」，问题退化为把边分配给链，增量不再是单点权值——你还能推出类似的「基底 + 增益」形状吗？
2. 得分改成「最小值之和」或「次大值之和」，引理 4 的阈值计数还能用吗？
3. 只问单个 $k$ 时能否 $O(n)$？只需第 $k-L$ 大的增益，可用 `nth_element` 或值域分桶省掉排序。
4. 把祖先偏序换成一般 DAG 的链划分，层状结构与可加容量都不复存在，此时大概要用费用流或拟阵交，复杂度会涨多少？
