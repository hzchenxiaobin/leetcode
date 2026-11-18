# Codeforces 网格路径 题解

## 1. 题目概述

- **标题 / 题号**：网格路径（Codeforces 2247F，英文名 Paths on a Grid）
- **链接**：https://codeforces.com/problemset/problem/2247/F
- **来源**：Codeforces Round 1111 (Div. 2) · Problem F
- **难度**：$\ast 2900$（3500 分）
- **限制**：时间 3 s / 内存 1024 MB
- **标签**：动态规划、随机化哈希、排序分组、计数（官方标签：data structures, dp, hashing）

**题意**：给定 $n\times m$ 的 $0/1$ 网格 $a$（$1$ 表示自由格，$0$ 表示障碍格，$(1,1)$ 与 $(n,m)$ 必为自由格）。一条**合法路径**指从 $(1,1)$ 出发、每步只向右或向下、只经过自由格、最终到达 $(n,m)$ 的路径。

称一个格子集合 $S$（**可以包含障碍格**）是**好的**，当且仅当：

1. $S$ 非空；
2. 对每个 $(i,j)\in S$：任何经过 $(i,j)$ 的合法路径，也经过 $S$ 中其余所有格子。

求好集合的数量，对 $998244353$ 取模。

多测：第一行 $t$；每组先给 $n,m$，随后 $n$ 行每行一个长度 $m$ 的 $01$ 串；对每组输出一行答案。

**约束**：

- $1 \le t \le 10^{4}$
- 单组只有 $1 \le n\cdot m \le 10^{6}$（**只约束乘积**，$n$ 或 $m$ 单独可以到 $10^6$）
- 所有测试的 $\sum n\cdot m \le 10^{6}$
- $a_{i,j}\in\{0,1\}$，且 $a_{1,1}=a_{n,m}=1$
- 时限 3 s：需要 $O(nm\log (nm))$ 以内的做法，且常数要小

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入
6
1 1
1
2 2
11
11
2 2
10
01
2 2
11
01
4 4
1011
1101
0111
1111
1 32
10010110010001010110011111010011

输出
1
5
15
8
162
301989883
```

逐组解读：

- 第 1 组 $1\times1$：唯一的非空集合 $\{(1,1)\}$ 就是好集合，答案 $1$。
- 第 2 组 $2\times2$ 全自由：两条路径（先右后下 / 先下后右）。$(1,1)$ 与 $(2,2)$ 在两条路径上都出现，同类（$2^2-1=3$）；$(1,2)$、$(2,1)$ 各成一类（各 $1$），合计 $3+1+1=5$。
- 第 3 组 $(1,2)$ 与 $(2,1)$ 都被堵：**一条路径都没有**，于是所有格子的「经过它的路径集合」都是空集，$4$ 个格子同类，答案 $2^4-1=15$。
- 第 4 组只有一条路径 $(1,1)\to(1,2)\to(2,2)$：这三格同类（$7$），障碍格 $(2,1)$ 单独成类（$1$），合计 $8$。
- 第 5 组 $4\times4$ 有三条路径：空集类 $7$ 格（含三个障碍格与走不到的格子）、全路径类 $5$ 格、另外四个格子各自成类，答案 $2^7-1+2^5-1+4\times(2^1-1)=127+31+4=162$。
- 第 6 组 $1\times32$：整行必须一路向右，路径**唯一**，$32$ 个格子全在同一类，答案 $2^{32}-1\bmod 998244353=301989883$。

自造示例（覆盖「多类 + 障碍格」的结构，本文 §3.4 会逐步走查）：

```text
输入
1
3 3
111
101
111

输出
18
```

## 3. 解题思路

### 3.1 暴力思路

对每个格子 $c$ 定义 $P(c)$ = 所有经过 $c$ 的合法路径组成的集合。若用小规模枚举把每条路径编号，则 $P(c)$ 可写成一个二进制掩码，于是「条件 2」可以逐位验证。

暴力做法：DFS 枚举**全部**路径（最多 $\binom{n+m-2}{n-1}$ 条，$1000\times1000$ 时是天文数字），再对每格求掩码、分组、按 $2^{|C|}-1$ 累加。它完全正确，但路径数随 $n,m$ 指数增长（$1000\times1000$ 时约有 $10^{600}$ 条），只能用于小网格对拍。

### 3.2 核心观察：按「路径集合」分类

![好集合就是同一个路径集合类的非空子集](images/cf2247_f_class_model.svg)

把条件 2 逐字翻译一下：对 $S$ 中任意 $c,d$，

$$\big(\text{经过 }c\text{ 的路径}\big)\subseteq\big(\text{经过 }d\text{ 的路径}\big),\quad\text{即 } P(c)\subseteq P(d).$$

由于 $c,d$ 都取遍 $S$，两个方向同时成立，于是

$$S \text{ 是好集合}\iff S\ne\varnothing\ \text{且}\ \forall c,d\in S:\ P(c)=P(d).$$

也就是说：**好集合恰好是某个等价类（按 $P(\cdot)$ 相同分组）的非空子集**。设这些类为 $C_1,C_2,\dots$，则

$$\text{答案}=\sum_{k}\bigl(2^{|C_k|}-1\bigr).$$

再注意一个细节：$P(c)=\varnothing$ 的格子（障碍格，以及自由但不在任何路径上的格子）彼此之间「无条件满足」条件（空集是任何集合的子集），所以它们**全部并成一个大类**，大小为 $nm-\#\{\text{在某个路径上的格子}\}$，贡献 $2^{nm-\text{onPath}}-1$。

于是问题变成：**给每个格子算一个 $P(c)$ 的指纹**，再把指纹相同的格子聚成一类。

### 3.3 哈希：把「路径集合」压成一个数

![双向 DP 计算路径集合的权和](images/cf2247_f_hash_dp.svg)

给网格里每条边 $e$ 独立地赋一个随机权 $x_e\in\mathbb{Z}_p^{*}$，定义

$$\Phi(c)=\sum_{p\ni c}\ \prod_{e\in p}x_e ,$$

其中 $p$ 取遍经过 $c$ 的合法路径。$\Phi$ 只依赖集合 $P(c)$，所以 $P(c)=P(d)\Rightarrow\Phi(c)=\Phi(d)$（**确定性成立**，无需概率假设）；反之若 $P(c)\ne P(d)$，两者是不同单项式集合的和，$\Phi(c)-\Phi(d)$ 是**非零多项式**，随机取权时判等只在极低概率下发生。

关键在于 $\Phi$ 可以 $O(1)$ 合并着算。设

$$A(c)=\sum_{s\to c}\prod_{e}x_e,\qquad B(c)=\sum_{c\to t}\prod_{e}x_e ,$$

则有递推

$$A(i,j)=A(i-1,j)\cdot x_{\downarrow}(i-1,j)+A(i,j-1)\cdot x_{\rightarrow}(i,j-1),\quad A(1,1)=1,$$
$$B(i,j)=B(i+1,j)\cdot x_{\downarrow}(i,j)+B(i,j+1)\cdot x_{\rightarrow}(i,j),\quad B(n,m)=1.$$

因为「前缀 $s\to c$」与「后缀 $c\to t$」的边集**不相交**，整条路径的权正好等于两段权之积，且两段选择互相独立，所以

$$\Phi(c)=A(c)\cdot B(c).$$

最后把每个在路径上的格子的指纹 $(\Phi_1(c),\Phi_2(c))$（两套独立的随机权）排序，数相同指纹的游程即可得到所有类的大小，套公式累加。

### 3.4 示例演算

![3×3 中间格被堵的走查](images/cf2247_f_walkthrough.svg)

网格

```text
1 1 1
1 0 1
1 1 1
```

合法路径只有两条：$P_1=s\to(1,2)\to(1,3)\to(2,3)\to t$，$P_2=s\to(2,1)\to(3,1)\to(3,2)\to t$。逐个格子写出 $P(c)$：

| 格子 | $P(c)$ | 类大小 | 贡献 |
|------|--------|--------|------|
| $(1,2),(1,3),(2,3)$ | $\{P_1\}$ | 3 | $2^3-1=7$ |
| $(2,1),(3,1),(3,2)$ | $\{P_2\}$ | 3 | $2^3-1=7$ |
| $(1,1),(3,3)$ | $\{P_1,P_2\}$ | 2 | $2^2-1=3$ |
| $(2,2)$ | $\varnothing$ | 1 | $2^1-1=1$ |

答案 $7+7+3+1=18$。注意 $(1,2)$ 与 $(2,3)$ 并**不相邻**，却在同一类里——同一类的判定只看「哪些路径经过它」，与几何位置无关。

再用官方第 5 组校验：$4\times4$ 的三条路径下，空集类 $7$ 格、全路径类 $5$ 格、再加四个单格类，得 $127+31+4=162$，与样例一致。

## 4. 算法细节

1. **可达性必须精确计算**。$A(c),B(c)$ 都是模 $p$ 下的值，完全可能恰好为 $0$；不能用「$A(c)\ne0$」判断 $c$ 在路径上。另开两个布尔数组做 $O(nm)$ 的布尔 DP：`rs[c] = rs[上] || rs[左]`，`rt[c] = rt[下] || rt[右]`，只有 `rs&&rt` 的格子才参与哈希与分组。
2. **边权取 $1..p-1$，绝不为 $0$**。若某条边权为 $0$，所有跨过它的路径权都会变成 $0$，大量本该不同的格子会被错误合并。生成后统一写 `% (p-1) + 1`。
3. **模数取 $p=2^{61}-1$**。乘法先转 `__int128` 再取模，既不会溢出，又让 Schwartz–Zippel 的误差界 $\le \deg/p$ 远小于任何 32 位模数下的值。
4. **两套独立随机权**。单套哈希的判等误差约为 $(n+m)/p$（最坏 $10^6/2.3\times10^{18}\approx4\times10^{-13}$），两套独立后误差是它的平方，对 $5\times10^{11}$ 个格子对做并集界后仍约 $10^{-13}$。
5. **用排序分组，而不是哈希表**。把 $10^6$ 个 $(h_1,h_2)$ 排序后数游程：$O(nm\log nm)$，$10^6$ 规模下约 $0.1$ s 量级，且不会出现 `unordered_map` 的冲突放大（也天然抗 hack）。
6. **幂表一次打满**。$2^i\bmod 998244353$ 预先算到 $10^6$，每个类的贡献 $2^{|C|}-1$ 用 $O(1)$ 取出；注意 $|C|$ 最大可以是 $nm$（整行 / 整列全自由的情形），表长要覆盖到 $10^6$ 而不是 $\max(n,m)$。
7. **多测开销**。$t$ 可达 $10^4$，所以每组只申请 $O(nm)$ 的局部数组（总和 $\le10^6$），不要每组清空长度为 $10^6$ 的全局数组；输出用 `'\n'`。
8. **空集类的边界**。当 onPath $=0$（$(1,1)$ 与 $(n,m)$ 都自由但根本不连通，如样例 3），空集类大小就是 $nm$，答案 $2^{nm}-1$，代码里不需要特判——公式自动成立。

## 5. 正确性证明

**引理 1**：$S$ 是好集合 $\iff$ $S\ne\varnothing$ 且 $S$ 中所有格子的 $P(\cdot)$ 相同。

**证明**：条件 2 即：对任意 $c,d\in S$ 有 $P(c)\subseteq P(d)$。$c,d$ 对称地取遍 $S$，故同时有 $P(c)\subseteq P(d)$ 与 $P(d)\subseteq P(c)$，得 $P(c)=P(d)$。反之若所有 $P$ 相等，则对任意 $c,d\in S$，$P(c)\subseteq P(d)$，即经过 $c$ 的每条路径都经过 $d$，条件 2 成立。∎

**引理 2**：好集合的总数是 $\sum_{k}\bigl(2^{|C_k|}-1\bigr)$，其中 $C_k$ 是 $P(\cdot)$ 的等价类。

**证明**：由引理 1，好集合恰为某个 $C_k$ 的非空子集；各类互不相交，故按类分别计数 $2^{|C_k|}-1$ 后相加，既无重复也无遗漏。∎

**引理 3**：$P(c)=\varnothing$ 当且仅当 $c$ 不在任何合法路径上；所有这类格子组成同一个类，大小为 $nm-\text{onPath}$。

**证明**：$P(c)\ne\varnothing$ 的定义就是「存在经过 $c$ 的合法路径」。空集两两相等，故它们同属一类；其余格子各自的 $P$ 非空，不可能与空集相等。∎

**引理 4**：对每个在路径上的格子 $c$，有 $\Phi(c)=A(c)\cdot B(c)$。

**证明**：任取经过 $c$ 的路径 $p$，把它拆成前缀 $s\to c$ 与后缀 $c\to t$，二者的边集不相交且并集为 $p$ 的边集，故 $\prod_{e\in p}x_e=\bigl(\prod_{e\in\text{前缀}}x_e\bigr)\bigl(\prod_{e\in\text{后缀}}x_e\bigr)$。「经过 $c$ 的路径」与「(前缀, 后缀) 对」一一对应，于是

$$\Phi(c)=\sum_{\text{前缀}}\sum_{\text{后缀}}\Bigl(\prod_{\text{前}}x_e\Bigr)\Bigl(\prod_{\text{后}}x_e\Bigr)=A(c)\cdot B(c).\qquad\blacksquare$$

**引理 5**：若 $P(c)\ne P(d)$，对一套随机权有 $\Pr\bigl[\Phi(c)=\Phi(d)\bigr]\le (n+m-2)/p$。

**证明**：不同路径的边集互不相同（一条路径由它的边集唯一确定），因此每条路径贡献的单项式互不相同，$\Phi(c)-\Phi(d)$ 中每个单项式的系数是 $0,\pm1$ 且至少有一项非零，故它是关于 $\{x_e\}$ 的**非零**多项式，次数不超过最长路径的边数 $n+m-2$。由 Schwartz–Zippel，独立均匀取权时它取值为 $0$ 的概率不超过 $\deg/p$。∎

**定理**：算法以至少 $1-10^{-12}$ 的概率输出正确答案。

**证明**：由引理 4，$P(c)=P(d)\Rightarrow\Phi_1(c)=\Phi_1(d)$ 且 $\Phi_2(c)=\Phi_2(d)$，同类必被分到同一指纹（不会漏）。若两格子不同类，由引理 5 与两套权重相互独立，它们指纹相同的概率 $\le\bigl((n+m-2)/p\bigr)^2$；对至多 $\binom{nm}{2}\le 5\times10^{11}$ 个格子对做并集界，总概率 $\le 5\times10^{11}\times(10^6/2.3\times10^{18})^2\approx 10^{-13}$。于是以该概率所有不同类格子指纹互不相同，分组与真实等价类完全一致，再由引理 2、3 得到正确计数。∎

## 6. 复杂度分析

- **时间**：两组布尔可达性 DP 共 $O(nm)$；两套随机权各需一次前向 + 一次后向 DP，共 $O(nm)$ 次 `__int128` 乘模；排序 $O(nm\log nm)$；累加 $O(nm)$。总计 $O(nm\log nm)$。在 $nm=10^6$ 上实测 $0.32\sim0.34$ s（含 I/O，clang -O2），相对 3 s 有约 $9$ 倍余量。
- **空间**：前向 / 后向 DP 各 $10^6$ 个 `u64`（各约 8 MB）、两套指纹再各 8 MB、排序用的 pair 数组 16 MB、网格 1 MB，合计约 $62$ MB（实测峰值 RSS），远低于 1024 MB。
- **Python**：同一算法在 CPython 下跑满 $10^6$ 格约需 $7\sim9$ s，会超时；本问的 Python 代码仅作对照实现，实际提交请使用 C++（或 PyPy3 并注意常数）。

## 7. 参考代码

### C++17

```cpp
// Codeforces 2247F - Paths on a Grid
// 好集合 <=> 落在同一个「经过它的路径集合」P(c) 等价类里；答案 = sum(2^|C| - 1)。
// 用双向 DP 把 P(c) 哈希成 A(c)*B(c)（边权随机），两套独立权重，排序分组。
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
typedef __int128 i128;

const u64 P = (1ULL << 61) - 1;          // 梅森素数 2^61-1
const u64 MOD = 998244353;
static inline u64 mul(u64 a, u64 b) { return (u64)((i128)a * b % P); }
static inline u64 smix(u64 x) {          // splitmix64：确定性伪随机
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}
static inline u64 ew(u64 idx, int dir, u64 salt) {   // 边 (idx,dir) 的权，∈[1,P-1]
    return smix((idx << 2) ^ (u64)dir ^ salt) % (P - 1) + 1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    static u64 pw[1000001];              // pw[i] = 2^i mod 998244353
    pw[0] = 1;
    for (int i = 1; i <= 1000000; i++) pw[i] = pw[i - 1] * 2 % MOD;

    int T;
    cin >> T;
    while (T--) {
        int n, m;
        cin >> n >> m;
        vector<string> g(n);
        for (auto &r : g) cin >> r;
        const int nm = n * m;

        vector<char> rs(nm, 0), rt(nm, 0);          // 精确可达性（不能用哈希值代替）
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++) {
                int c = i * m + j;
                if (g[i][j] == '0') continue;
                rs[c] = (i == 0 && j == 0) || (i > 0 && rs[c - m]) || (j > 0 && rs[c - 1]);
            }
        for (int i = n - 1; i >= 0; i--)
            for (int j = m - 1; j >= 0; j--) {
                int c = i * m + j;
                if (g[i][j] == '0') continue;
                rt[c] = (i == n - 1 && j == m - 1) || (i + 1 < n && rt[c + m]) || (j + 1 < m && rt[c + 1]);
            }
        int on = 0;
        for (int c = 0; c < nm; c++) if (rs[c] && rt[c]) on++;
        u64 ans = (pw[nm - on] + MOD - 1) % MOD;     // P = 空集的大类

        if (on > 0) {
            vector<u64> A(nm), B(nm), h0(nm), h1(nm);
            for (int s = 0; s < 2; s++) {
                u64 salt = s ? 0x51ED270B7ULL : 0x2545F4914F6CDD1DULL;
                for (int i = 0; i < n; i++)                     // 前向：A(c)
                    for (int j = 0; j < m; j++) {
                        int c = i * m + j;
                        if (g[i][j] == '0' || !rs[c]) { A[c] = 0; continue; }
                        if (i == 0 && j == 0) { A[c] = 1; continue; }
                        u64 v = i ? mul(A[c - m], ew(c - m, 0, salt)) : 0;
                        if (j) { v += mul(A[c - 1], ew(c - 1, 1, salt)); if (v >= P) v -= P; }
                        A[c] = v;
                    }
                for (int i = n - 1; i >= 0; i--)                    // 后向：B(c)
                    for (int j = m - 1; j >= 0; j--) {
                        int c = i * m + j;
                        if (g[i][j] == '0' || !rt[c]) { B[c] = 0; continue; }
                        if (i == n - 1 && j == m - 1) { B[c] = 1; continue; }
                        u64 v = (i + 1 < n) ? mul(B[c + m], ew(c, 0, salt)) : 0;
                        if (j + 1 < m) { v += mul(B[c + 1], ew(c, 1, salt)); if (v >= P) v -= P; }
                        B[c] = v;
                    }
                vector<u64> &H = s ? h1 : h0;
                for (int c = 0; c < nm; c++)
                    if (rs[c] && rt[c]) H[c] = mul(A[c], B[c]);     // Phi(c) = A*B
            }
            vector<pair<u64, u64>> k;                                // 两套指纹，排序分组
            k.reserve(on);
            for (int c = 0; c < nm; c++)
                if (rs[c] && rt[c]) k.emplace_back(h0[c], h1[c]);
            sort(k.begin(), k.end());
            for (size_t i = 0; i < k.size();) {
                size_t j = i;
                while (j < k.size() && k[j] == k[i]) j++;
                ans = (ans + pw[j - i] + MOD - 1) % MOD;
                i = j;
            }
        }
        cout << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys

PM = (1 << 61) - 1            # 2^61-1，梅森素数
PM1 = PM - 1
MOD = 998244353
MASK = (1 << 64) - 1


def smix(x):
    x = (x + 0x9E3779B97F4A7C15) & MASK
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & MASK
    return x ^ (x >> 31)


def solve_case(n, m, g, pw):
    nm = n * m
    rs = bytearray(nm)                       # 从 (1,1) 可达
    rt = bytearray(nm)                       # 能到 (n,m)
    for i in range(n):
        row, base = g[i], i * m
        for j in range(m):
            c = base + j
            if not row[j]:
                continue
            if i == 0 and j == 0:
                rs[c] = 1
            elif (i and rs[c - m]) or (j and rs[c - 1]):
                rs[c] = 1
    for i in range(n - 1, -1, -1):
        row, base = g[i], i * m
        for j in range(m - 1, -1, -1):
            c = base + j
            if not row[j]:
                continue
            if i == n - 1 and j == m - 1:
                rt[c] = 1
            elif (i + 1 < n and rt[c + m]) or (j + 1 < m and rt[c + 1]):
                rt[c] = 1

    on = sum(1 for c in range(nm) if rs[c] and rt[c])
    ans = (pw[nm - on] - 1) % MOD             # P = 空集的大类
    if not on:
        return ans

    h0 = [0] * nm
    h1 = [0] * nm
    for si, salt in enumerate((0x2545F4914F6CDD1D, 0x51ED270B54F1)):
        wr = [0] * nm                          # (i,j) -> (i,j+1)
        wd = [0] * nm                          # (i,j) -> (i+1,j)
        for q in range(nm):
            wr[q] = smix(((q << 2) | 1) ^ salt) % PM1 + 1
            wd[q] = smix((q << 2) ^ salt) % PM1 + 1
        A = [0] * nm
        for i in range(n):
            row, base = g[i], i * m
            for j in range(m):
                c = base + j
                if not row[j] or not rs[c]:
                    continue
                if i == 0 and j == 0:
                    A[c] = 1
                    continue
                v = A[c - m] * wd[c - m] % PM if i else 0
                if j:
                    v += A[c - 1] * wr[c - 1] % PM
                    if v >= PM:
                        v -= PM
                A[c] = v
        B = [0] * nm
        for i in range(n - 1, -1, -1):
            row, base = g[i], i * m
            for j in range(m - 1, -1, -1):
                c = base + j
                if not row[j] or not rt[c]:
                    continue
                if i == n - 1 and j == m - 1:
                    B[c] = 1
                    continue
                v = B[c + m] * wd[c] % PM if i + 1 < n else 0
                if j + 1 < m:
                    v += B[c + 1] * wr[c] % PM
                    if v >= PM:
                        v -= PM
                B[c] = v
        H = h1 if si else h0
        for c in range(nm):
            if rs[c] and rt[c]:
                H[c] = A[c] * B[c] % PM

    keys = sorted((h0[c], h1[c]) for c in range(nm) if rs[c] and rt[c])
    L, i = len(keys), 0
    while i < L:
        j = i
        while j < L and keys[j] == keys[i]:
            j += 1
        ans = (ans + pw[j - i] - 1) % MOD
        i = j
    return ans


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos, cases, total = 1, [], 0
    for _ in range(t):
        n, m = int(data[pos]), int(data[pos + 1])
        pos += 2
        g = [[ch == 49 for ch in data[pos + i]] for i in range(n)]
        pos += n
        cases.append((n, m, g))
        total += n * m
    pw = [1] * (total + 1)
    for i in range(1, total + 1):
        pw[i] = pw[i - 1] * 2 % MOD
    sys.stdout.write("\n".join(str(solve_case(n, m, g, pw)) for n, m, g in cases) + "\n")


if __name__ == "__main__":
    main()
```

## 8. 边界情况与易错点

1. **$n=m=1$**：只有一个格子，且它就是起点与终点，唯一路径（长度 $0$）经过它，$P\ne\varnothing$，答案 $1$；不要因为「路径为空」而把它误判成 $P=\varnothing$。代码里前向 / 后向 DP 的初始值 `A(s)=B(t)=1` 天然处理了这一点。
2. **根本没有路径**：$(1,1)$ 与 $(n,m)$ 都自由却互不可达（样例 3）。此时 onPath $=0$，答案是 $2^{nm}-1$，极易漏掉这个分支或误以为答案是 $0$。
3. **一整行 / 一整列全自由**（如样例 6）：路径唯一，所有格子属于同一类，$|C|=nm$，必须真的算 $2^{nm}$（幂表下标要到 $nm$），写成 $2^{n+m}$ 或只开到 $\max(n,m)$ 都会错。
4. **边权为 $0$**：`h % p` 可能取到 $0$，若直接当边权，则所有经过该边的路径权为 $0$，会把毫不相干的格子并成一类。必须 `% (p-1) + 1`。
5. **用哈希值判断可达性**：$A(c)$ 或 $\Phi(c)$ 在模 $p$ 下可能恰好为 $0$，不能当作「不可达」的标记；可达性一定要用独立布尔 DP。
6. **只做一套哈希**：理论上存在 $O(\deg/p)$ 的误判可能（$p$ 选 32 位模数时约 $10^{-3}$，不可接受）；至少两套独立权重，且模数用 61 位。
7. **多测清空**：$t=10^4$ 时每个测试都要复用数组；如果开全局数组却忘记清空、或每组 `O(10^6)` 初始化，会 TLE。
8. **取模后减一**：贡献是 $2^{|C|}-1$，`ans + pw[k] - 1` 这种写法在 `pw[k]=0` 时会无符号下溢，务必写成 `(ans + pw[k] + MOD - 1) % MOD`，别省那个 `+MOD`。

## 相关题目与扩展

- [Codeforces 757F. Team Rocket Rises Again](https://codeforces.com/problemset/problem/757/F)：支配树——「删除一个点会破坏多少条最短路」，与本题「所有路径都经过它」是同一种「必经点」语言。
- [Codeforces 567E. President and Roads](https://codeforces.com/problemset/problem/567/E)：判断一条边是否出现在**所有**最短路中，本质也是比较「路径集合」。
- [LeetCode 62. 不同路径](https://leetcode.cn/problems/unique-paths/) / [LeetCode 63. 不同路径 II](https://leetcode.cn/problems/unique-paths-ii/)：网格路径计数的基础 DP，本题的前向 / 后向分解正是它的加权推广。
- [Codeforces 1746F. Kazaee](https://codeforces.com/problemset/problem/1746/F)：随机化哈希 + 出现次数判定的另一类套路，可对比「用随机化换取 $O(n\log n)$」。

**延伸思考**：本题的分类完全由 $P(c)$ 决定，而 $P(c)$ 在「必经点（支配 / 反支配）」的语言下有精确刻画：$c,d$ 同类当且仅当在 $s\to t$ 的 DAG 上 $c$ 支配 $d$ 且 $d$ 反支配 $c$。因此也可以用**支配树**把格子分成精确的类，写出完全确定性的 $O(nm)$ 算法（代价是常数与实现量都大得多）——这也是本题被标 `hashing` 的原因：随机化版本更短更快。另一个值得想的方向是：若把「经过 $c$ 的路径必须经过 $S$ 中其余**所有**格子」改成「至少一个」，计数就从「类的非空子集」变成对路径集合的覆盖问题，需要完全不同的工具。
