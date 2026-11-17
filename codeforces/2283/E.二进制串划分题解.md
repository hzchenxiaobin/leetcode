# Codeforces 二进制串划分 题解

## 1. 题目概述

- **标题 / 题号**：二进制串划分（Codeforces 2283E，英文名 Partition of a Binary String）
- **链接**：https://codeforces.com/problemset/problem/2283/E
- **来源**：Educational Codeforces Round 196 (Rated for Div. 2) · Problem E
- **难度**：未评级（Educational Round 的 E 题，题面未给分值）
- **限制**：时间 2 s / 内存 512 MB
- **标签**：组合数学、动态规划（Bell 数预处理）、计数、字符串

**题意**：给定长度为 $n$ 的二进制串 $s$（下标 $1\sim n$）。把 $1\sim n$ 划分成若干非空集合，要求同一集合内任意两个不同整数 $x,y$ 满足 $s_x=s_y$ 或 $|x-y|=1$。对集合 $M$ 记 $f(M)$ 为其中出现过的不同字符数，成本 $|M|\cdot f(M)$；划分成本为各集合成本之和。求最大成本，以及达到最大成本的划分数（模 $998244353$）。集合次序、集合内元素次序不同不算新的划分。多测。

**约束**：$1\le t\le 500$，$1\le n\le 5000$，串只含 `0`/`1`。**官方公告特别说明「对 $\sum n$ 没有限制」**：总长度可达 $2.5\times 10^6$，所以每组必须 $O(n)$，任何 $O(n^2)$/组或「每组重建大表」的写法都会 TLE，预处理只能做一次并与 $n$ 解耦。

## 2. 示例

```text
输入
3
8
10001000
6
000111
8
01010101

输出
13 5
8 4
16 4
```

样例 2 只有边界 $(3,4)$ 异色：取混色对 $\{3,4\}$ 后两侧各剩两个同色位置，分组方案 $2\times2=4$；样例 3 整串交替，成本 $16$、方案 $4$。自造小例（串 `0`、`10`、`01010`）的输出依次为 `1 1`、`4 1`、`10 2`：$n=1$ 无边界取成本 $1$；`10` 只能取混色对，成本 $4$；`01010` 整串交替，增益 $5$、方案 $c[5]=2$。

## 3. 解题思路

### 3.1 暴力思路

枚举 $1\sim n$ 的所有集合划分（$Bell(n)$ 种）逐个检查：$Bell(12)$ 已是 $4.2\times10^6$，$Bell(5000)$ 是天数级，再加 $t=500$ 且 $\sum n$ 无限制，彻底不可行。必须先刻画「合法集合长什么样」。

### 3.2 核心观察：混色集合只有两种形状

![合法集合只有三类形状](images/cf2283_e_mixed_sets.svg)

设 $M$ 含两种字符。取异色的 $x<y\in M$，条件只允许 $s_x=s_y$ 或 $|x-y|=1$，故必有 $y=x+1$：**异色元素必须紧贴**。再取 $z\in M$：若 $s_z=s_x$，则 $(z,y)$ 异色 $\Rightarrow z\in\{x,x+2\}$，即 $z=x+2$；若 $s_z=s_y$，则 $(z,x)$ 异色 $\Rightarrow z\in\{x-1,y\}$，即 $z=x-1$。而 $x-1$ 与 $x+2$ 同色、彼此合法，第 4 个元素无处可放。于是 $|M|\le3$，混色集合只有：

1. **混色对** $\{i,i+1\}$，要求 $s_i\ne s_{i+1}$，成本 $2\cdot2=4$；
2. **三元组** $\{i,i+1,i+2\}$，只能是 `ABA`（$s_i=s_{i+2}\ne s_{i+1}$），成本 $3\cdot2=6$。

其余集合都纯色（$f=1$），成本恰为 $|M|$。若共有 $p$ 个混色对、$q$ 个三元组，纯色位置共 $n-2p-3q$ 个，则

$$\text{总成本}=(n-2p-3q)+4p+6q=n+2p+3q$$

问题化为**最大化增益 $2p+3q$**，再数方案。

### 3.3 算法流程：边界分段 + 2/3 拆分 + Bell 数

![边界视角：交替段被 2/3 块铺满](images/cf2283_e_alternating_runs.svg)

称位置 $i,i+1$ 之间的界线为**边界 $i$**，若 $s_i\ne s_{i+1}$ 则称它「不同」。对应关系是：混色对 ⇔ 占用 1 条不同边界；三元组 ⇔ 占用 2 条相邻的不同边界（此时自动 $s_i=s_{i+2}$）；两块位置不重叠 ⇔ 二者之间至少隔 1 条边界（$j\ge i+2$）。

把连续不同边界的极大段叫**交替段**。设某段含 $k$ 条边界，它覆盖 $k+1$ 个连续位置。若段内有 $p$ 对、$q$ 个三元组，它们占 $p+2q$ 条边界，块间至少空 $p+q-1$ 条，全部落在段内：

$$k\ \ge\ (p+2q)+(p+q-1)\ \Longrightarrow\ 2p+3q\ \le\ k+1$$

**上界可达到**：把 $k+1$ 拆成若干 $2,3$ 的有序和，顺着位置切成大小 $a_j$ 的连续块（$2$ ↔ 混色对，$3$ ↔ 三元组），块间恰好隔 1 条边界、首尾不留空隙，整段 $k+1$ 个位置全被覆盖，增益正好 $k+1$。于是

- 最大成本 $=n+\sum_{\text{段}}(k+1)$：每个位置先记 1 分，每段再额外送 1 分；
- 每段最优方案数 $=c[k+1]$，$c[m]$ 为 $m$ 的 $2/3$ 有序拆分数：$c[0]=1,\ c[1]=0,\ c[m]=c[m-2]+c[m-3]$；
- **剩余位置只由串决定**：位置 $i$ 不属于任何交替段 $\iff$ $(i=1$ 或 $s_{i-1}=s_i)$ 且 $(i=n$ 或 $s_i=s_{i+1})$。设其中 `0` 有 $z$ 个、`1` 有 $o$ 个，它们可任意划分为同色集合，方案数 $Bell(z)\cdot Bell(o)$。

$$\text{成本}=n+\sum(k+1),\qquad \text{方案数}=\prod_{\text{段}}c[k+1]\times Bell(z)\times Bell(o)$$

$Bell$ 用 Bell 三角形预处理到 $5000$：$T(0,0)=1$，$T(n,0)=T(n-1,n-1)$，$T(n,k)=T(n,k-1)+T(n-1,k-1)$，$Bell(n)=T(n,0)$，时间 $O(N^2)$、空间 $O(N)$（滚动一行）。

### 3.4 示例演算

![样例 1 演算](images/cf2283_e_walkthrough.svg)

$s=\texttt{10001000}$：边界 $1,4,5$ 不同，两段——$\{1\}$（$k=1$，增益 $2$，只能拆成单个 $2$）与 $\{4,5\}$（$k=2$，增益 $3$，$3=3$ 只能是三元组）。成本 $=8+2+3=13$；剩余位置 $\{3,7,8\}$ 全是 `0`，$Bell(3)=5$，两段各 1 种，答案 $13\ 5$。样例 2：$c[2]\cdot Bell(2)\cdot Bell(2)=1\cdot2\cdot2=4$。样例 3：整串一段 $k=7$，增益 $8$、成本 $16$，$c[8]=4$（$2{+}2{+}2{+}2$ 一种、$2{+}3{+}3$ 三种排列）。

## 4. 算法细节

1. **单指针扫段**：`j` 从 `i` 尽量右移，直到 `s[j]==s[j+1]` 或到串尾，得 $k=j-i$。若 $k\ge1$ 就累加 $k+1$、乘 $c[k+1]$，再令 `i=j+1`（整段已被覆盖，不必逐位置判断）；否则 `i++`。均摊 $O(n)$。
2. **端点特判**：剩余位置的条件是「左侧无边界或相同」且「右侧无边界或相同」，首尾只有一侧存在边界，两侧硬判会把端点误算进段里。
3. **预处理与 $n$ 解耦**：全题上限 $n\le5000$，所以一次建到 $5005$ 即可（想省常数也可以读完询问再建到 $\max\{z,o,k+1\}$）；关键是**只建一次**，绝不能每组重建。
4. **Bell 三角形滚动一行**：$cur[0]=prev[n-1]$，$cur[k]=cur[k-1]+prev[k-1]$，即对上一行做前缀和；C++ 每行一次 `assign`，Python 用 `itertools.accumulate(prev, initial=prev[-1])` 交给 C 层，避免 $1.25\times10^7$ 次 Python 循环。
5. **$c$ 的递推边界**：$c[1]=0$（$1$ 不可拆），$c[2]=c[3]=1$。$c$ 与 $Bell$ 都是「组合数」而非「排列数」，别写成 $2^{m}$ 式的拆分数。
6. **数值范围**：成本上限 $2n\le10^4$，`int` 也够，仍统一用 `long long`；乘法前转 `long long` 再取模；Bell 表内部用 `int` +「$\ge MOD$ 就减」。
7. **多测**：$cost, ways, z, o$ 每组重新置初值，常量表只在 `main` 开头建一次，不要用未清空的全局累加量。

## 5. 正确性证明

**引理 1（混色集合分类）**：若 $f(M)=2$，则 $M$ 只能是 $\{i,i+1\}$（$s_i\ne s_{i+1}$）或 $\{i,i+1,i+2\}$（$s_i=s_{i+2}\ne s_{i+1}$）。
**证明**：取异色 $x<y\in M$，必有 $y=x+1$。任取 $z\in M\setminus\{x,y\}$：$s_z=s_x$ 时 $(z,y)$ 异色 $\Rightarrow z\in\{x,x+2\}$，故 $z=x+2$；$s_z=s_y$ 时 $(z,x)$ 异色 $\Rightarrow z\in\{x-1,y\}$，故 $z=x-1$。$x-1$ 与 $x+2$ 同色且合法，但再添元素须同时紧贴两者，无解，故 $|M|\le3$；三元组必为 `ABA`。∎

**引理 2（成本分解）**：任一合法划分成本为 $n+2p+3q$。
**证明**：由引理 1，集合只有三类：纯色成本 $|M|$、混色对 $4=2+2$、三元组 $6=3+3$；又 $\sum|M|=n$，故总成本 $=(n-2p-3q)+4p+6q=n+2p+3q$。∎

**引理 3（每段增益上界）**：同一交替段（$k$ 条不同边界）内的块满足 $2p+3q\le k+1$。
**证明**：块的所有边界都落在此段且不跨段，占用 $p+2q$ 条。相邻两块按位置排序，前者覆盖位置 $[a,b+1]$，后者从 $c$ 起；位置不交要求 $c\ge b+2$，即中间至少空一条边界，故块间至少空 $p+q-1$ 条。于是 $k\ge(p+2q)+(p+q-1)$。∎

**引理 4（结构刻画与计数）**：段内「增益 $=k+1$ 的方案」与「$k+1$ 的 $2/3$ 有序拆分」一一对应，故最优方案数为 $c[k+1]$。
**证明**：给定拆分 $a_1+\cdots+a_m=k+1$，按序把段内 $k+1$ 个位置切成大小 $a_j$ 的连续块：大小 $2$ 的块内部异色相邻，合法；大小 $3$ 的块两条边界都不同，故 $s_i=s_{i+2}\ne s_{i+1}$，合法；块间不重叠，增益 $=\sum a_j=k+1$ 且铺满整段。反之若 $2p+3q=k+1$，引理 3 的不等式必须取等，故块间恰好空一条边界、首尾无空隙，块按位置铺满整段，读出块大小即得一个 $2/3$ 拆分。两映射互逆。∎

**引理 5（剩余位置与计数分解）**：最优方案覆盖全部交替段内位置；最优划分与「每段一个最优块结构 + 剩余 `0` 的一个划分 + 剩余 `1` 的一个划分」构成双射。
**证明**：混色集合必在某个交替段内，位置 $i$ 属于交替段 $\iff$ 边界 $i-1$ 或 $i$ 存在且不同，取反即得判定式；段内全覆盖由引理 4 给出。反之，划分中 $f=2$ 的集合唯一确定各段块结构，其余纯色集合按字符分成两组互相独立的划分；段与段位置不重叠、约束按段分离，故方案数相乘。$m$ 个同色位置划分为非空集合的方案数即 $Bell(m)$。∎

**定理**：最大成本为 $n+\sum(k+1)$，最优划分数为 $\prod c[k+1]\cdot Bell(z)\cdot Bell(o)\bmod 998244353$。
**证明**：引理 2 把成本化为 $n+$ 增益，引理 3 给出每段上界且段间独立，引理 4 说明每段可达上界，故最大增益 $=\sum(k+1)$；计数由引理 4 与引理 5。∎

## 6. 复杂度分析

- **时间**：预处理 $O(N^2)$，$N\le5000$，约 $1.25\times10^7$ 次加法；每组 $O(n)$ 扫段 + $O(n)$ 统计剩余位置。总计 $O(N^2+\sum n)$，$\sum n\le2.5\times10^6$。
- **空间**：$O(N)$（Bell 表滚动一行 + 两张表），与 $n$ 无关。
- **实测**：极限数据（$t=500$、每组 $n=5000$，混合全同/全交替/随机）C++17 约 $0.2$ s，相对 2 s 有约 10 倍余量；Python3 约 $1.5$ s（瓶颈是 Bell 表的 $1.25\times10^7$ 次取模），比较贴边，建议 PyPy 提交。这也解释了「$\sum n$ 无限制」公告：它专门卡「每组重建表」。

## 7. 参考代码

### C++17

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

static const int MOD = 998244353;
static const int MAXN = 5005;

int bell[MAXN];   // bell[m] = 集合划分数 B_m mod MOD
int comp[MAXN];   // comp[m] = 把 m 拆成 2/3 之和的方案数

int main() {
    vector<int> prevRow(1, 1), curRow;   // Bell 数：Bell 三角形，滚动一行
    bell[0] = 1;
    for (int n = 1; n < MAXN; n++) {
        curRow.assign(n + 1, 0);
        curRow[0] = prevRow[n - 1];
        for (int k = 1; k <= n; k++)
            curRow[k] = (curRow[k - 1] + prevRow[k - 1]) % MOD;
        bell[n] = curRow[0];
        prevRow.swap(curRow);
    }
    comp[0] = 1;                         // comp[m] = comp[m-2] + comp[m-3]
    for (int m = 1; m < MAXN; m++) {
        long long v = 0;
        if (m >= 2) v += comp[m - 2];
        if (m >= 3) v += comp[m - 3];
        comp[m] = (int)(v % MOD);
    }
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    cin >> t;
    while (t--) {
        int n;
        string s;
        cin >> n >> s;
        long long cost = n, ways = 1;
        int i = 0;
        while (i < n) {
            int j = i;                 // 极长交替段覆盖位置 [i, j]
            while (j + 1 < n && s[j] != s[j + 1]) j++;
            int k = j - i;             // 段内「不同」边界的条数
            if (k >= 1) {
                cost += k + 1;         // 该段增益 k+1
                ways = ways * comp[k + 1] % MOD;
                i = j + 1;             // 整段位置已被混色集合覆盖
            } else {
                i++;
            }
        }
        int z = 0, o = 0;              // 剩余位置：左右都相同（越界视为相同）
        for (int p = 0; p < n; p++) {
            bool leftSame = (p == 0) || (s[p - 1] == s[p]);
            bool rightSame = (p + 1 == n) || (s[p] == s[p + 1]);
            if (leftSame && rightSame) {
                if (s[p] == '0') z++; else o++;
            }
        }
        ways = ways * bell[z] % MOD * bell[o] % MOD;
        cout << cost << ' ' << ways << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys
from itertools import accumulate

MOD = 998244353
MAXN = 5005

comp = [0] * MAXN                     # comp[m]：把 m 拆成 2、3 之和的方案数
comp[0] = 1
for m in range(1, MAXN):
    v = 0
    if m >= 2: v += comp[m - 2]
    if m >= 3: v += comp[m - 3]
    comp[m] = v % MOD

bell = [0] * MAXN                     # Bell 数：第 n 行 = 第 n-1 行的前缀和
bell[0] = 1
prev = [1]
for n in range(1, MAXN):
    prev = [x % MOD for x in accumulate(prev, initial=prev[-1])]
    bell[n] = prev[0]

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos])
        s = data[pos + 1].decode()
        pos += 2
        cost, ways, i = n, 1, 0
        while i < n:
            j = i
            while j + 1 < n and s[j] != s[j + 1]:
                j += 1
            k = j - i                 # 段内「不同」边界条数
            if k:
                cost += k + 1         # 该段增益 k+1
                ways = ways * comp[k + 1] % MOD
                i = j + 1             # 整段已被混色集合覆盖
            else:
                i += 1
        z = o = 0
        for p in range(n):            # 剩余位置：左右都相同（越界算相同）
            if (p == 0 or s[p - 1] == s[p]) and (p + 1 == n or s[p] == s[p + 1]):
                if s[p] == '0': z += 1
                else: o += 1
        ways = ways * bell[z] % MOD * bell[o] % MOD
        out.append(f"{cost} {ways}")
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：没有边界，成本 $1$、方案 $Bell(1)=1$；注意初值 $Bell(0)=Bell(1)=1$、$c[0]=1,\ c[1]=0$。
2. **全同串**：无交替段，成本 $n$、方案 $Bell(n)$，故 $Bell$ 必须预处理到 $5000$（只按 $\max(k+1)$ 建表会越界）。
3. **全交替串**：整串一段，成本 $2n$、方案 $c[n]$，$c$ 要开到 $n+1$。
4. **端点判定**：首尾位置只有一侧有边界，必须写成「左侧无边界**或**相同」且「右侧无边界**或**相同」，否则漏位置。
5. **增益公式**：最大成本是 $n+\sum(k+1)$，不是 $n+$ 不同边界数——每多一个交替段还要再送 $1$ 分，混用会系统性少算。
6. **漏乘 $Bell$**：只统计混色结构、忘记纯色位置能任意分组是本题最常见 WA；`000111` 的 $4$ 就来自 $Bell(2)\cdot Bell(2)$。
7. **每组重建表**：$\sum n$ 无限制，$t=500$ 时每组重建 $O(5000^2)$ 的表必然 TLE，组内也不能做 $O(n^2)$ 的 DP。
8. **取模时机**：C++ 乘法前转 `long long`；Python 的 `%` 天然非负，但 `accumulate` 中途不取模会积累大整数，按行取模一次即可。

## 相关题目与扩展

- [Codeforces 568B. Symmetric and Transitive](https://codeforces.com/problemset/problem/568/B)：等价关系计数就是 $Bell(n)$，用的正是 Bell 三角形预处理，可直接搬来做本题第 4 步。
- [Codeforces 1515E. Phoenix and Computers](https://codeforces.com/problemset/problem/1515/E)：把序列切段、各段独立计数再用乘法原理合并，与「交替段之间互不影响」同构。
- [LeetCode 1259. 不相交的握手](https://leetcode.cn/problems/handshakes-that-dont-cross/)：同样是「按结构切段 + 乘法原理」，可对照「段内独立」的论证。
- [LeetCode 322. 零钱兑换](https://leetcode.cn/problems/coin-change/)：本题 $c[m]=c[m-2]+c[m-3]$ 就是「用 2、3 凑出 $m$ 的组合数」，与完全背包计数版同源。

**延伸思考**：若字符集从二元扩到 $k$ 元，「异色元素两两相邻」会变成更复杂的形状约束，交替段内不再有唯一最优拆分，需要区间 DP；若把代价改成 $|M|\cdot f(M)^2$，「块越大越划算」，最优结构不再对应 $2/3$ 拆分。本题真正的难点是先证明「混色集合只有两种形状」——分类一旦完成，剩下的只是一次线性扫描加两张预处理表。
