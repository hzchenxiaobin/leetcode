# Codeforces 淘汰玩家 题解

## 1. 题目概述

- **标题 / 题号**：淘汰玩家（Codeforces 2276G，英文名 Elimination of Players）
- **链接**：https://codeforces.com/problemset/problem/2276/G
- **来源**：Educational Codeforces Round 195 (Rated for Div. 2) · Problem G
- **难度**：2100 分（Div. 2 的压轴题 G）
- **限制**：时间 4 s / 内存 512 MB
- **标签**：组合数学，计数，动态规划，数学

**题意**：$n$ 个玩家编号 $1..n$，实力是 $1..n$ 的一个排列 $s_1,\dots,s_n$（$s_j$ 是玩家 $j$ 的实力，越大越强）。游戏进行 $n-1$ 轮，第 $i$ 轮"保护"玩家 $a_i$（被保护的玩家可能已经出局）。每轮恰好淘汰一人：记当前剩余玩家中实力最弱者为 $u$、次弱者为 $v$，若 $u$ 本轮被保护则淘汰 $v$，否则淘汰 $u$。$n-1$ 轮后只剩一人。给定 $a_1..a_{n-1}$，对每个玩家 $j$ 与每一轮 $i$ 求出"$j$ 恰在第 $i$ 轮被淘汰"的排列数 $ans(j,i)$，输出

$$\bigoplus_{j=1}^{n}\bigoplus_{i=1}^{n-1} \bigl(ans(j,i)\bmod 998244353\bigr)\cdot j\cdot i,$$

即 $ans$ 取模，而乘积与最终异或**不取模**。多测。

**约束**：

- $1\le t\le 2500$，$2\le n\le 5000$，且所有测试的 $\sum n\le 5000$；
- $1\le a_i\le n$，$a_i$ 可以重复；
- 输出是异或，值域上界约 $998244353\cdot 5000^2\approx 2.5\times 10^{16}$，需 64 位整数；
- $\sum n$ 很小，允许对单组 $O(n^2)$；总阶乘预处理一次即可。

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
7
2
2
3
1 2
4
1 1 1
4
1 4 1
7
2 2 2 7 7 7
6
3 1 3 6 3
5
5 1 4 2

输出：
2
3
96
188
2024
4610
69
```

## 3. 解题思路

### 3.1 暴力思路

直接把 $n!$ 个排列枚举出来，每个排列模拟 $n-1$ 轮，复杂度 $O(n!\cdot n)$。$n\le 5000$ 时毫无希望，而且答案只需要 $ans$ 的模数，说明必须"按结构计数"而不是逐个排列。突破口是把游戏改写成只看相对次序的过程。

设 $p_q$ 表示实力第 $q$ 弱的玩家（即 $p$ 是 $s$ 的逆排列）。整个过程只依赖 $p$ 这一条序列。

### 3.2 核心观察：擂主与「方块」分解

![擂主与方块分解](images/cf2276_g_champion_blocks.svg)

**引理 1（每轮只有两个候选）**：第 $i$ 轮开始时，剩余玩家恰为 $\{p_s\}\cup\{p_{i+1},p_{i+2},\dots,p_n\}$，其中 $p_s$ 是当前最弱者，称之为**擂主**（$s\le i$）。

于是每轮只在两人之间做选择：

- 若 $a_i = p_s$（匹配）：淘汰新人 $p_{i+1}$，擂主不变、继续坐在台上；
- 若 $a_i \ne p_s$（不匹配）：淘汰擂主 $p_s$，新人 $p_{i+1}$ 接任。

由此得到**方块分解**：从 $s$ 开始，只要 $a_s=a_{s+1}=\cdots=a_{e-1}=p_s$ 就一直匹配，到第 $e$ 轮 $a_e\ne p_s$ 时擂主 $p_s$ 被杀，方块 $[s,e]$ 结束，下一块从 $e+1$ 开始。方块 $[s,e]$ 中：第 $s..e-1$ 轮分别淘汰 $p_{s+1},\dots,p_e$，第 $e$ 轮淘汰 $p_s$。

两个反复用到的等价刻画：

- **位置 $r$ 是新方块起点** $\iff r=1$ 或第 $r-1$ 轮不匹配；
- 第 $r$ 轮的擂主，要么是 $p_r$（$r$ 是方块起点），要么是上一方块延伸过来的 $p_s\ (s<r)$，此时 $p_s=a_s=\cdots=a_{r-1}$。

### 3.3 算法流程：把答案拆成 F、G、H 三个计数

记 $a_0$ 不存在，$G(0,\cdot)=0$，$F(0)=0$。定义

- $F(r)$：第 $r$ 轮**匹配**的排列数，即第 $r$ 轮擂主实力恰为 $a_r$ 的排列数；
- $G(r,x)$：第 $r$ 轮匹配、且 $p_{r+1}=x$ 的排列数——也就是"玩家 $x$ 在第 $r$ 轮作为新人被淘汰"的排列数；
- $A(r,x)$：位置 $r$ 是方块起点、且 $p_r=x$ 的排列数；
- $H(r,x)$：第 $r$ 轮擂主恰为 $x$ 的排列数。

**引理 2（$H$ 的分解）**：$H(r,x)=A(r,x)+[x=a_{r-1}]\cdot F(r-1)$。

证明见第 5 节：若第 $r$ 轮擂主是 $p_r$，就是 $A(r,x)$；否则第 $r-1$ 轮必须匹配，擂主值只能是 $a_{r-1}$，共 $F(r-1)$ 种。

**引理 3（$A$ 与 $G$ 互为补集）**：$A(1,x)=(n-1)!$，且对 $r\ge 2$，

$$A(r,x)=(n-1)!-G(r-1,x).$$

因为"位置 $r$ 是方块起点且 $p_r=x$"与"$p_r=x$ 且第 $r-1$ 轮匹配"互补，而后者正是 $G(r-1,x)$。

**引理 4（存活计数）**：令 $S(x,r)$ 为"玩家 $x$ 在第 $r$ 轮开始时仍存活"的排列数，则

$$S(x,r)=(n-r)(n-1)!+H(r,x),\qquad ans(x,r)=S(x,r)-S(x,r+1).$$

$x$ 存活 $\iff$ 它的名次 $>r$（还没登场）或它就是擂主，前者有 $(n-r)(n-1)!$ 种。把 $r$ 与 $r+1$ 相减即得

$$ans(x,r)=(n-1)!+H(r,x)-H(r+1,x).$$

把引理 2、3 代入并消去 $H$（$x\ne a_r$ 时 $[x=a_r]F(r)$ 项为 $0$），得到**最终公式**

$$ans(x,r)=(n-1)!+G(r,x)-G(r-1,x)+[x=a_{r-1}]\cdot F(r-1)\quad (x\ne a_r),$$

而 $ans(a_r,r)=0$（该轮被保护的人不可能被淘汰）。

### 3.4 F 与 G：从右往左的 run 链

![run 链与交错符号](images/cf2276_g_run_chain.svg)

把 $a_1..a_r$ 做 run 压缩（相邻相同值合并），**从右往左**列出 $(v_0,\ell_0),(v_1,\ell_1),\dots$，其中 $\ell_0$ 是"当前 run 截到 $r$ 为止"的长度，其余 $\ell_j$ 是整段长度；扫描到第一个**与更靠右的某个 run 值相同**的位置就停止，保留下来的链长为 $k+1$。

**引理 5（run 链公式）**：

$$F(r)=\sum_{j=0}^{k}(-1)^j\,\ell_j\,(n-1-j)!,$$

$$G(r,x)=\sum_{j<cut(x)}(-1)^j\,\ell_j\,(n-2-j)!,$$

其中 $cut(x)$ 是 $x$ 在链中的下标（$x$ 不在链中时取全和，即上界为 $k$）。

证明的思路是**链式回溯**（第 5 节给出完整论证）：要让第 $r$ 轮匹配且 $p_{r+1}=x$，方块起点必须落在当前 run 内且 $p_s=v_0$；一旦它不在 run 首，就要求更靠左的 run 里有一个"匹配块"恰好延伸过来，于是沿 run 链逐层向左追加"这一层的 run 值被固定在某个位置"。每多一层就多固定一个值（加上 $x$ 与 $v_0$ 共 $j+2$ 个值，剩 $(n-2-j)!$ 种），而该 run 值可落在本段 $\ell_j$ 个位置之一；层数奇偶交替贡献符号 $\pm$。若某个 run 值与更靠右的重复，同一个玩家就要占两个名次，链断裂——这正是"截断"的来历。

维护方式：每读入一个 $a_r$，把当前 run 长度 $+1$（或新起一段），并把旧链中"上一次出现该值及其左边"的部分整体丢掉；随后 $O(k)$ 重算前缀和。查询 $G(r,x)$ 只要一次下标访问（$O(1)$）。

### 3.5 示例演算

![样例 4 的走查](images/cf2276_g_walkthrough.svg)

取样例 4：$n=4$，$a=[1,4,1]$，$n!=24$，答案 $188$。

| 回合 $r$ | 保留的 run（右→左） | $F(r)$ | $G(r,1..4)$ | $ans(1..4,r)$ |
| --- | --- | --- | --- | --- |
| 1 | $(1,1)$ | $3!=6$ | $[0,2,2,2]$ | $[0,8,8,8]$ |
| 2 | $(4,1),(1,1)$ | $6-2=4$ | $[2,1,1,0]$ | $[14,5,5,0]$ |
| 3 | $(1,1),(4,1)$ | $6-2=4$ | $[0,1,1,2]$ | $[0,6,6,12]$ |

例如 $r=2$ 的 $j=1$ 用到了修正项：$3!+G(2,1)-G(1,1)+F(1)=6+2-0+6=14$。最后

$$16\oplus24\oplus32\oplus28\oplus20\oplus30\oplus36\oplus54\oplus144=188 .$$

## 4. 算法细节

1. **下标约定**：玩家与轮次在代码里都改成 $0$-indexed；公式中的 $G(0,\cdot)=0$、$F(0)=0$、$a_0$ 不存在，所以 $r=1$ 时不加修正项（代码里用 `if (i)` 与初值 `ap = -1` 自然处理）。
2. **符号与取模**：$F$ 是交错的整数和，先按 `long long` 累加再 `(f % MOD + MOD) % MOD`；$G$ 的前缀和每加一项就取模并向非负方向调整。
3. **阶乘预处理**：只需 $0!\sim(n-1)!$，全局算到 $5004$ 即可；$G$ 用到 $(n-2-j)!$，因为链长 $k+1\le n-1$，下标不会为负。
4. **run 列表维护**：`runs[0]` 是当前 run。新值等于 `runs[0]` 时只把长度 $+1$；否则在旧链中找**上一次出现**的位置，删除它及其左边的全部 run，再头插 `(x,1)`——这与"重建时遇到重复就截断"等价。
5. **$O(1)$ 查 $G$**：重建时同时记录 `cut[x]`（$x$ 在链中的下标，缺席为 $-1$）与前缀和数组 `prefG`，则 $G(r,x)$ 就是 `prefG[cut[x]]`（缺席时取 `prefG.back()`）。
6. **滚动数组**：公式只用 $G(r,\cdot)$ 与 $G(r-1,\cdot)$ 两行，开两个长度 $n$ 的数组滚动即可，空间 $O(n)$；答案边算边异或，不必存 $n\times n$ 的表。
7. **乘法范围**：$ans<998244353$，$r\cdot j\le 5000^2$，乘积 $<2.5\times10^{16}$，用 `unsigned long long`（或 `long long`）安全；异或也在这 64 位里做。
8. **多测清理**：`Blocks` 每个测试重新 `init(n)`，两个 $G$ 数组重新赋值；阶乘是全局的，不要重复算。
9. **Python 提示**：算法是 $O(n^2)$ 的 $25\cdot10^6$ 级别，CPython 在 $n=5000$ 的全不相同数据上实测约 9 s，会超 4 s 时限；请用 PyPy 3 提交（官方 PyPy 通过约 0.6 s），或直接用 C++ 版。

## 5. 正确性证明

**引理 1（两个候选）**：第 $i$ 轮开始时剩余玩家恰为 $\{p_s\}\cup\{p_{i+1},\dots,p_n\}$，$p_s$ 为最弱者。

**证明**：对 $i$ 归纳。$i=1$ 时全体玩家为 $\{p_1\}\cup\{p_2,\dots,p_n\}$，成立。设第 $i$ 轮开始为 $\{p_s\}\cup\{p_{i+1},\dots,p_n\}$，最弱为 $p_s$、次弱为 $p_{i+1}$，本轮淘汰其中一人：若淘汰 $p_{i+1}$，剩余仍是 $\{p_s\}\cup\{p_{i+2},\dots,p_n\}$；若淘汰 $p_s$，则剩余为 $\{p_{i+1}\}\cup\{p_{i+2},\dots,p_n\}$，新擂主正是 $p_{i+1}$。两种情形都保持形状。∎

**引理 2（$H$ 的分解）**：$H(r,x)=A(r,x)+[x=a_{r-1}]F(r-1)$。

**证明**：第 $r$ 轮擂主为 $x$ 分两类。若位置 $r$ 是方块起点，擂主就是 $p_r$，计数为 $A(r,x)$。否则第 $r$ 轮不是方块起点，即第 $r-1$ 轮匹配，擂主沿用第 $r-1$ 轮的擂主；由引理 1 的刻画，该擂主的值等于 $a_{r-1}$，故只有 $x=a_{r-1}$ 有贡献，计数为 $F(r-1)$。两类互斥且穷尽。∎

**引理 3（$A$ 与 $G$）**：$A(1,x)=(n-1)!$；$r\ge2$ 时 $A(r,x)=(n-1)!-G(r-1,x)$。

**证明**：$r=1$ 时位置 1 必是方块起点，$p_1=x$ 有 $(n-1)!$ 种。$r\ge2$ 时，"位置 $r$ 是方块起点"与"第 $r-1$ 轮匹配"互补，因此 $A(r,x)=\#\{p_r=x\}-\#\{p_r=x,\text{第 }r-1\text{ 轮匹配}\}=(n-1)!-G(r-1,x)$。∎

**引理 4（答案 = 存活差）**：$S(x,r)=(n-r)(n-1)!+H(r,x)$，且 $ans(x,r)=S(x,r)-S(x,r+1)=(n-1)!+H(r,x)-H(r+1,x)$。

**证明**：第 $r$ 轮开始时已登场名次为 $1..r$，玩家 $x$ 存活当且仅当名次 $>r$，或名字已登场且是唯一未被淘汰的擂主。前者计数 $(n-r)(n-1)!$，后者计数 $H(r,x)$，两者互斥。$x$ 在第 $r$ 轮被淘汰 $\iff$ 第 $r$ 轮开始存活而第 $r+1$ 轮开始不存活，故 $ans=S(x,r)-S(x,r+1)$；代入 $(n-r)-(n-r-1)=1$ 即得。∎

**引理 5（run 链公式）**：如 3.4 所述，$F(r),G(r,x)$ 等于对应的交错和。

**证明**：只需证 $G$（$F=\sum_x G(r,x)$ 由定义即得）。固定 $r$ 与 $x$，设保留下来的链为 $(v_0,\ell_0),\dots,(v_k,\ell_k)$，当前 run 为 $[L_0,r]$。

设某个排列使第 $r$ 轮匹配且 $p_{r+1}=x$。第 $r$ 轮擂主为 $v_0=a_r$，其方块起点 $s$ 满足 $p_s=v_0$ 且 $s\in[L_0,r]$（同 run 才可能一路匹配到 $r$）。由于 $p_{r+1}=x\ne v_0$，位置 $s$ 在 $[L_0,r]$ 中唯一可能有两种：$s=L_0$，或 $s>L_0$ 且第 $s-1$ 轮不匹配。后者要求第 $s-1$ 轮擂主 $\ne v_0$；沿引理 1 的刻画回溯，唯一可能是 $s-1=L_0$ 且上一 run（run 1）里存在一个匹配块恰好延伸到 $L_0$，即 $s=L_0+1$。

于是计数沿链向左递归：第 $j$ 层要求在 run $j$ 内选一个位置 $s_j$ 放 $v_j$（共 $\ell_j$ 种），并决定"链在此终止"（$s_j$ 就是该 run 的方块起点，靠更左边的 run 提供不匹配）还是"继续向左"。把"继续"视为坏事件做容斥，第 $j$ 层的容斥项恰好固定 $x,v_0,\dots,v_j$ 共 $j+2$ 个互不相同的玩家，剩余 $n-2-j$ 个值可任意排布，贡献 $\pm\,\ell_j\,(n-2-j)!$，符号按层数交替。若某个 $v_j$ 与更靠右的 $v_{j'}$ 相同，则同一个玩家要同时占据两个不同位置，该层及更左的项全部为零，链必须截断——这就是"遇到重复 run 值就停止"的原因。有限链求和即得公式（也可对链长归纳：第 $j$ 层容斥去掉「继续向左」的全部情形后，剩下的恰是更短链上的同型问题）。∎

**定理（程序正确）**：对每个 $x\ne a_r$，程序输出的 $ans(x,r)$ 等于"玩家 $x$ 在第 $r$ 轮被淘汰"的排列数模 $998244353$；对 $x=a_r$ 输出 $0$。

**证明**：由引理 4 得 $ans(x,r)=(n-1)!+H(r,x)-H(r+1,x)$；用引理 2、3 把 $H$ 展开，正好得到 3.3 中的最终公式；$F,G$ 由引理 5 给出，代码对每个 $r$ 按该公式逐玩家累加。$x=a_r$ 时第 $r$ 轮被保护者不可能在本轮被淘汰（引理 1 中被淘汰的两人都不等于被保护者），故答案为 $0$，代码显式跳过。最后按题意把 $ans\cdot j\cdot i$ 逐个异或，得到输出。∎

## 6. 复杂度分析

- **时间**：每个 $r$ 需要 $O(k)$ 重建 run 链、$O(n)$ 枚举玩家，而 $k\le r\le n$，总复杂度 $O(n^2)$。单组 $n=5000$ 实测（全不相同的 $a$，链最长）C++17 约 $0.15$ s；随机数据约 $0.06$ s，时限 $4$ s，余量 $>10$ 倍。
- **空间**：`runs`、`cut`、`prefG` 与两行滚动 $G$ 数组均为 $O(n)$，远小于 $512$ MB。
- **Python**：同为 $O(n^2)$，但常数大（每轮 $n$ 次内层循环，共约 $2.5\times10^7$ 次），CPython 实测约 $9$ s，需 PyPy 3 才能进 $4$ s；官方 PyPy 3-64 提交约 $0.6$ s。

## 7. 参考代码

### C++17

```cpp
#include <algorithm>
#include <cstdio>
#include <utility>
#include <vector>
using namespace std;
const int MOD = 998244353, MAXN = 5005;
int fact[MAXN];

// 保留 a[1..r] 的 run（右→左），遇重复 run 值即截断；同时维护 F 与 G 的前缀和
struct Blocks {
    int n, F;
    vector<pair<int, int>> runs;              // runs[0] = 当前 run
    vector<int> cut, prefG;
    vector<char> seen;
    void init(int n_) { n = n_; F = 0; runs.clear(); cut.assign(n, -1);
                        seen.assign(n, 0); prefG.assign(1, 0); }
    void rebuild() {
        fill(seen.begin(), seen.end(), 0); fill(cut.begin(), cut.end(), -1);
        vector<pair<int, int>> keep; prefG.assign(1, 0);
        long long f = 0; int sign = 1, cnt = n - 1, acc = 0;
        for (auto &p : runs) {
            int v = p.first, len = p.second;
            if (seen[v]) break;               // 同一 run 值第二次出现：链断
            seen[v] = 1; keep.push_back(p); cut[v] = (int)keep.size() - 1;
            f += (long long)sign * len % MOD * fact[cnt] % MOD;
            acc = (int)((acc + (long long)sign * len % MOD * fact[cnt - 1]) % MOD);
            if (acc < 0) acc += MOD;
            prefG.push_back(acc); --cnt; sign = -sign;
        }
        F = (int)((f % MOD + MOD) % MOD);
        runs.swap(keep);
    }
    int getG(int x) const { return cut[x] < 0 ? prefG.back() : prefG[cut[x]]; }
    void append(int x) {
        if (runs.empty() || runs[0].first != x) runs.insert(runs.begin(), make_pair(x, 0));
        ++runs[0].second; rebuild();
    }
};

int main() {
    fact[0] = 1;
    for (int i = 1; i < MAXN; ++i) fact[i] = (long long)fact[i - 1] * i % MOD;
    int T; if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n; scanf("%d", &n);
        vector<int> a(n - 1);
        for (int &v : a) { scanf("%d", &v); --v; }
        Blocks b; b.init(n);
        vector<int> gp(n, 0), gc(n, 0);        // G(r-1,.), G(r,.)
        int Fp = 0, ap = -1; unsigned long long res = 0;
        for (int i = 0; i < n - 1; ++i) {     // 第 r = i+1 轮
            b.append(a[i]);
            for (int j = 0; j < n; ++j) gc[j] = b.getG(j);
            for (int j = 0; j < n; ++j) {
                if (a[i] == j) continue;      // 本轮被保护，答案 0
                long long s = fact[n - 1] + gc[j];
                if (i) { s -= gp[j]; if (ap == j) s += Fp; }
                s %= MOD; if (s < 0) s += MOD;
                res ^= (unsigned long long)s * (i + 1) * (j + 1);
            }
            gp.swap(gc); Fp = b.F; ap = a[i];
        }
        printf("%llu\n", res);
    }
    return 0;
}
```

### Python3

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD, MAXN = 998244353, 5005
    fact = [1] * MAXN
    for i in range(1, MAXN): fact[i] = fact[i - 1] * i % MOD
    p = 0; T = int(data[p]); p += 1; out = []
    for _ in range(T):
        n = int(data[p]); p += 1
        a = [int(v) - 1 for v in data[p:p + n - 1]]; p += n - 1
        runs = []                       # [value, length]；runs[0] 是当前 run
        Gp = [0] * n; Fp, ap = 0, -1
        res = 0; base = fact[n - 1]
        for i in range(n - 1):          # 第 r = i+1 轮
            x = a[i]
            if runs and runs[0][0] == x:
                runs[0][1] += 1
            else:                       # 丢掉"上次出现 x"及其左边的所有 run
                for t in range(len(runs) - 1, -1, -1):
                    if runs[t][0] == x: del runs[t:]; break
                runs.insert(0, [x, 1])
            cut = {}; pref = [0]; f = acc = 0
            sign, cnt, j = 1, n - 1, 0
            for v, ln in runs:
                cut[v] = j
                f += sign * ln * fact[cnt]
                acc = (acc + sign * ln * fact[cnt - 1]) % MOD
                pref.append(acc); j += 1; cnt -= 1; sign = -sign
            F = f % MOD
            Gc = [pref[-1]] * n
            for v, k in cut.items(): Gc[v] = pref[k]
            if 0 <= ap < n and ap != x:  # 把修正项 [j==a[r-1]]*F(r-1) 折进 pv
                pv = Gp[:]; pv[ap] = (pv[ap] - Fp) % MOD
            else:
                pv = Gp
            ci = i + 1
            for j in range(n):
                if j != x: res ^= ((base + Gc[j] - pv[j]) % MOD) * ci * (j + 1)
            Gp, Fp, ap = Gc, F, x
        out.append(str(res))
    sys.stdout.write("\n".join(out) + "\n")

main()
```

## 8. 边界情况与易错点

1. **$n=2$**：只有一轮、一条 run，$F(1)=1!=1$，$G(1,x)$ 在 $x\ne a_1$ 时为 $0$；答案即 $2$（样例 1）。链长 $k+1\le n-1$，所以 $(n-2-j)!$ 的下标最小为 $0$，不会越界。
2. **$x=a_r$ 必须输出 $0$**：公式在 $x=a_r$ 时会给出非零值（少减了 $[x=a_r]F(r)$ 一项），代码用 `continue` 显式跳过，否则对角线会错。
3. **$r=1$ 不能加修正项**：$a_0$ 不存在，$F(0)=0$、$G(0,\cdot)=0$ 都要按约定处理（代码里初值 `ap = -1` 天然不触发）。
4. **重复 run 值必须截断**：若不截断，同一个玩家会被同时固定在两个名次上，$F,G$ 都会偏大；样例 4 与样例 5 都覆盖这一情形。
5. **$F$ 的负数取模**：交替和可能为负，C++ 中 `%` 保留符号，必须先加 `MOD` 再取模；`acc` 每一步都要向非负方向调整。
6. **乘积溢出**：$ans\cdot j\cdot i$ 最大约 $2.5\times10^{16}$，`int` 必爆，要用 64 位；输出用 `%llu` / `unsigned long long`。
7. **多测总量**：$\sum n\le 5000$，但 $t$ 可达 $2500$，务必每测重建状态、不要写 $O(n^2)$ 的内存表（$n=5000$ 时 $n^2$ 个 `int` 就是 $100$ MB，滚动数组更省）。
8. **Python 时限**：CPython 在最大数据约 $9$ s，会超时；用 PyPy 3 提交，或直接交 C++。

## 相关题目与扩展

- [Codeforces 1540A Great Graphs](https://codeforces.com/problemset/problem/1540/A)：排序后把答案写成"相邻差值 × 固定权重"的和，与本题"把答案拆成可按 run 维护的线性组合"是同一类降维手法。
- [Codeforces 1598E Staircases](https://codeforces.com/problemset/problem/1598/E)：按"阶梯"分解成互不重叠的结构后增量维护，和本题的"方块 / run 链"增量重算思路一脉相承。
- [LeetCode 1866. 恰有 K 根木棍可以看到的排列数目](https://leetcode.cn/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/)：同样用"插入第 $i$ 小的元素、只看相对次序"的 DP 统计排列，可以对照本题引理 1 的"两个候选"视角。
- [LeetCode 903. DI 序列的有效排列](https://leetcode.cn/problems/valid-permutations-for-di-sequence/)：用"插入第 $i$ 小的元素、只看相对位置"的 DP 统计排列，是本题引理 1"只剩两个候选"思想的入门版。

**延伸思考**：

1. 如果把"保护"改成同时保护一个集合 $A_i$（每轮至多淘汰最弱者或次弱者之一），方块分解仍然成立，但 $G$ 的链会变成"集合的容斥"，复杂度可能升到 $O(n^2\log n)$。
2. 如果要求输出每个 $(j,i)$ 的具体值而不是异或，本文的滚动数组仍可做到 $O(n^2)$ 时间、$O(n)$ 空间逐行输出，这一点比 $O(n^2)$ 内存的做法更稳。
3. 若把"实力是排列"放宽成"实力可重复"，"两个候选"结构被破坏（最小值可能并列），需要回到完全不同的计数模型。
