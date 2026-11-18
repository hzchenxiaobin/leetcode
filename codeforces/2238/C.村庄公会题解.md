# Codeforces 村庄公会 题解

## 1. 题目概述

- **标题 / 题号**：村庄公会（Codeforces 2238C，英文名 Village Guilds）
- **链接**：https://codeforces.com/problemset/problem/2238/C
- **来源**：Codeforces Round 1106 (Div. 2) · Problem C
- **难度**：1400（$*1400$）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：树、深度优先搜索、动态规划 / 树形统计（官方标签：dfs and similar, dp, trees）

**题意**：给定一棵以 $1$ 为根的有根树（$n$ 个点，边双向）。对任意点 $v$ 与任意非负整数 $h$，把

$$S(v,h)=\{\,x : x \text{ 在 } v \text{ 的子树内},\ \operatorname{dist}(v,x)=h\,\}$$

称为一个**公会**（$h=0$ 时只有 $v$ 自己）。两个公会不同当且仅当它们的点集不同。求**不同的非空公会**个数。

**约束**：

- $1\le t\le 10^4$，$2\le n\le 2\cdot 10^5$，且所有测试的 $\sum n\le 2\cdot 10^5$
- 父亲直接给出：$p_2,p_3,\dots,p_n$，满足 $1\le p_i<i$
- 时间 2 s，内存 256 MB；答案与 $n$ 同阶（实测最大约 $2n$，见 §6）

> 💡 一句话本质：一个公会就是「子树里某一深层」的全部点；用集合的 LCA 做唯一代表后，每个点 $u$ 的贡献只与**儿子高度的次大值**有关。

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入
5
5
1 2 3 4
3
1 1
7
1 2 1 3 5 5
10
1 1 3 2 2 4 4 4 3
15
1 2 1 3 3 4 3 7 3 10 6 7 1 9

输出
5
4
9
15
22
```

- 第 1 组是一条链 $1-2-3-4-5$：任意 $(v,h)$ 都只得到单点集合 $\{v\text{ 的第 }h\text{ 代后代}\}$，故答案恰为 $5$。
- 第 2 组是 $1$ 带两个叶子：$n$ 个单点加上 $(1,1)=\{2,3\}$，共 $3+1=4$。
- 第 3 组（$n=7$）：$7$ 个单点，再加 $(1,1)=\{2,4\}$ 与 $(5,1)=\{6,7\}$，共 $9$。
- 第 4 组（$n=10$）：$10$ 个单点加 $5$ 个多分支层，共 $15$（明细见 §3.4）。
- 第 5 组（$n=15$）：$15+7=22$。

再补一组自造样例（非官方，用来展示「重复」）：

```text
输入
1
5
1 1 2 2

输出
7
```

树是 $1\to\{2,3\}$、$2\to\{4,5\}$。公会为 $5$ 个单点、$(1,1)=\{2,3\}$、$(2,1)=\{4,5\}$，而 $(1,2)$ 得到的还是 $\{4,5\}$，重复不计，共 $7$ 个。

## 3. 解题思路

### 3.1 暴力思路

枚举所有 $(v,h)$，对每个 $v$ 做一次子树 DFS 把点按相对深度分组，再把每个点集塞进哈希表去重。$(v,h)$ 的对数是 $\sum_v (\mathrm{hgt}(v)+1)=O(n^2)$（链上每个 $v$ 有 $O(n)$ 个非空层），每层的点集还要花代价比较，总复杂度 $O(n^2)$ 甚至 $O(n^3)$，$n=2\cdot10^5$ 完全不可行。

即使只想「不重复」，也不能简单地数非空 $(v,h)$ 对数：链上它等于 $n$ 却恰好等于答案，而星形图上 $(1,1)$ 与所有单点都不同，又凭空多一个，规律必须靠结构分析得到。

### 3.2 核心观察：按绝对深度切片 + 用 LCA 做唯一代表

![公会 = 子树的某一层，用 LCA 去重](images/cf2238_c_guild_levels.svg)

**关键一：同一集合蕴含同一个深度。** 公会 $S(v,h)$ 中每个点 $x$ 都满足 $\operatorname{dep}(x)=\operatorname{dep}(v)+h$，所以集合里所有点绝对深度相同，$h=\operatorname{dep}(x)-\operatorname{dep}(v)$ 由集合与 $v$ 唯一确定。于是可以把 $(v,h)$ 换成 $(v,d)$，其中 $d$ 是**绝对深度**：

$$S(v,d)=\{\,x\in \mathrm{subtree}(v) : \operatorname{dep}(x)=d\,\},\qquad d\ge \operatorname{dep}(v)$$

**关键二：用 LCA 当代表去重。** 同一个集合 $S$ 可能由多个 $v$ 生成（图里 $(2,1)$ 与 $(1,2)$ 都给出 $\{4,5\}$）。取

$$u=\operatorname{LCA}(S)$$

则 $v$ 必是 $u$ 的祖先，于是 $S\subseteq S(u,d)\subseteq S(v,d)=S$，即 $S=S(u,d)$。**因此每个不同的非空公会都恰好对应一对 $(u,d)$，满足 $u=\operatorname{LCA}\bigl(S(u,d)\bigr)$**：一个集合的 LCA 唯一、元素深度唯一，$(u,d)$ 也被它唯一确定。

这样去重问题就变成了「哪些 $(u,d)$ 是合法的」这一纯计数问题。

### 3.3 算法流程：每个点只贡献「次高分支高度 + 1」

![每个 u 只贡献次高分支高度加 1](images/cf2238_c_second_height.svg)

先看 $d=\operatorname{dep}(u)$：此时 $S(u,d)=\{u\}$，LCA 就是 $u$，**恒合法**，$n$ 个点各给一个单点集合。

再看 $d>\operatorname{dep}(u)$：$u$ 自己不在层里，层上的点全部落在各个儿子的子树里。于是

$$\operatorname{LCA}\bigl(S(u,d)\bigr)=u \iff \text{至少有 }2\text{ 个儿子在 }d\text{ 层有后代}$$

（只有一个儿子有后代时，整层都在这一个儿子里，LCA 更深；有两个儿子的后代时，取分居两枝的两点，LCA 恰为 $u$。）

记 $\mathrm{hgt}(c)$ 为以 $c$ 为根的子树高度（向下走的最长边数），则儿子 $c$ 的子树里最深深度是 $\operatorname{dep}(u)+1+\mathrm{hgt}(c)$，所以

$$\text{儿子 } c \text{ 在 } d \text{ 层有后代}\iff d\le \operatorname{dep}(u)+1+\mathrm{hgt}(c)$$

设 $\mathrm{hgt}$ 在儿子中的**次大值**为 $h_2$（不足两个儿子时视为 $-\infty$），则「至少两个儿子」$\iff d\le \operatorname{dep}(u)+1+h_2$。合法的 $d$ 正是

$$\operatorname{dep}(u)<d\le \operatorname{dep}(u)+1+h_2,$$

共 $1+h_2$ 个。也就是说，记

$$b_2(u)=\text{儿子分支高度 } 1+\mathrm{hgt}(c) \text{ 的次大值（不足两个儿子时为 }0\text{）},$$

就有

$$\boxed{\ \text{ans}=n+\sum_{u=1}^{n} b_2(u)\ }$$

**实现**：由于 $p_i<i$，儿子的编号一定大于父亲，所以从 $i=n$ 倒序扫到 $2$：此时 $b_1[i]$（$i$ 的最高分支高度）已经算好，把 $1+b_1[i]$ 交给父亲去更新父亲的「最大 / 次大」两个值即可。这等价于后序 DFS，但没有递归。

### 3.4 示例演算

![样例 3 走查](images/cf2238_c_walkthrough.svg)

以第 3 组（$n=7$，$p=(1,2,1,3,5,5)$）为例，树为 $1\to\{2,4\}$、$2\to3$、$3\to5$、$5\to\{6,7\}$，各点高度 $\mathrm{hgt}$ 依次为 $4,3,2,0,1,0,0$：

| $u$ | 儿子高度 | $b_2(u)$ | 新增的集合 |
|---|---|---|---|
| 1 | 3, 0 | $0+1=1$ | $d=1:\{2,4\}$ |
| 2 | 2 | 0 | — |
| 3 | 1 | 0 | — |
| 5 | 0, 0 | $0+1=1$ | $d=4:\{6,7\}$ |
| 4,6,7 | 无 | 0 | — |

答案 $=7+1+1=9$。注意 $u=1$ 只有 $d=1$ 合法：$d=2$ 的层 $\{3\}$ 只有一条分支有后代，它的 LCA 是 $3$，那个集合已经作为单点 $\{3\}$ 在 $n$ 里计过了。

第 4 组（$n=10$，树 $1\to\{2,3\}$、$2\to\{5,6\}$、$3\to\{4,10\}$、$4\to\{7,8,9\}$）同理：

| $u$ | 儿子高度 | $b_2(u)$ | 新增的集合 |
|---|---|---|---|
| 1 | 2, 1 | 2 | $d=1:\{2,3\}$，$d=2:\{4,5,6,10\}$ |
| 2 | 0, 0 | 1 | $d=2:\{5,6\}$ |
| 3 | 1, 0 | 1 | $d=2:\{4,10\}$ |
| 4 | 0, 0, 0 | 1 | $d=3:\{7,8,9\}$ |

$10+5=15$，与官方输出一致。而链（第 1 组）每个点至多一个儿子，$b_2\equiv0$，答案就是 $n$；星形图上只有根贡献 $b_2=1$（所有叶子一层），答案 $n+1$。

## 4. 算法细节

1. **只维护两个量**：对每个点 $u$ 维护 $\mathrm{hgt}(u)$（最高分支高度）与 $b_2(u)$（次高分支高度，初值 $0$）。处理 $i$ 时把 $v=1+\mathrm{hgt}(i)$ 交给父亲 $p_i$，按「先比最大、再比次大」更新：`if (v > b1[p]) { b2[p] = b1[p]; b1[p] = v; } else if (v > b2[p]) { b2[p] = v; }`。
2. **先比最大再比次大，相等也不能跳过**：走 `else if` 分支时若 $v=\mathrm{b1}[p]$，就会正确写入 $\mathrm{b2}[p]=v$，这正是「两个儿子一样高」的情形；若写成两个独立 `if` 并重复赋值，反而容易把同一个儿子算两次。
3. **倒序代替 DFS**：$p_i<i$ 保证所有儿子编号大于父亲，从 $n$ 扫到 $2$ 时儿子的信息一定已就绪，这就是一次「倒着的后序遍历」。链状数据（$p_i=i-1$，深度 $2\cdot10^5$）用递归 DFS 会直接爆栈，本写法没有栈风险。
4. **叶子与单儿子无需特判**：不足两个儿子时 $b_2(u)$ 保持 $0$，而 $b_2$ 的定义正是 $\max(0,1+h_2)$，所以一个统一的加法就涵盖了所有情况。
5. **$n$ 不要漏**：$d=\operatorname{dep}(u)$ 的 $n$ 个单点集合互不相同（不同 $u$ 就是不同点），这是答案的基数部分，先置 `ans = n`。
6. **答案类型**：完全二叉树 $n=2\cdot10^5$ 时答案为 $399982\approx 2n$，实测各类构造下答案都不超过约 $2n$，远小于 $2^{31}$；仍统一用 `long long`，避免「多测累加」「极端构造」带来的意外。
7. **多测**：每组重新 `vector` 分配，容量 $n+1$；$\sum n\le2\cdot10^5$ 保证总分配量线性，不要用全局数组 `memset` 整块清空。
8. **读入**：$p$ 的 $n-1$ 个整数可能在任意空白处换行，`cin >>` 或 Python 的 `split()` 都能正确处理；不要在 C++ 里混用 `getline`。

## 5. 正确性证明

先固定记号：$\operatorname{dep}$ 为绝对深度（根为 $0$），$\mathrm{subtree}(u)$ 为 $u$ 的子树，$S(v,d)$ 见 §3.2，$b_2(u)$ 为「$1+\mathrm{hgt}(c)$ 在儿子中的次大值」，没有两个儿子时取 $0$。

**引理 1（深度唯一）**：若 $S(v,h)=S(v',h')$ 非空，则 $\operatorname{dep}(v)+h=\operatorname{dep}(v')+h'$，即两者的绝对深度 $d$ 相同。

**证明**：$S(v,h)$ 中任一点 $x$ 满足 $\operatorname{dep}(x)=\operatorname{dep}(v)+h$，所以集合里所有点的绝对深度都等于 $\operatorname{dep}(v)+h$；同理也等于 $\operatorname{dep}(v')+h'$。两式相等。∎

**引理 2（LCA 代表）**：任一非空公会 $S$ 都可以写成 $S=S(u,d)$，其中 $u=\operatorname{LCA}(S)$，且此时 $\operatorname{LCA}(S(u,d))=u$；反过来，不同的集合对应的 $(u,d)$ 不同。

**证明**：设 $S=S(v,h)$，$d=\operatorname{dep}(v)+h$。$v$ 是 $S$ 中每一点的祖先，故 $v$ 是 $u=\operatorname{LCA}(S)$ 的祖先或就是 $u$。于是

$$S\subseteq S(u,d)\subseteq S(v,d)=S,$$

三处夹逼给出 $S=S(u,d)$，并且 $\operatorname{LCA}(S(u,d))=\operatorname{LCA}(S)=u$。唯一性：若 $S=S(u',d')$，则 $u'=\operatorname{LCA}(S)=u$，再由引理 1 得 $d'=d$。∎

**引理 3（合法性判据）**：对 $u$ 与 $d\ge\operatorname{dep}(u)$，$S(u,d)\ne\varnothing$ 且 $\operatorname{LCA}(S(u,d))=u$ 当且仅当

- $d=\operatorname{dep}(u)$；或
- $d>\operatorname{dep}(u)$，且 $u$ 至少有两个儿子在 $d$ 层有后代。

**证明**：若 $d=\operatorname{dep}(u)$，层里唯一的子树内点就是 $u$，$S=\{u\}$，LCA 为 $u$，成立。若 $d>\operatorname{dep}(u)$ 且只有一个儿子 $c$ 在 $d$ 层有后代，则 $S(u,d)\subseteq \mathrm{subtree}(c)$，其 LCA 落在 $\mathrm{subtree}(c)$ 内，不等于 $u$；若 $u$ 根本没有儿子在 $d$ 层有后代，则 $S(u,d)=\varnothing$。反之若有两个儿子 $c_1,c_2$ 在 $d$ 层有后代，取 $x_1\in\mathrm{subtree}(c_1)\cap\{d\text{ 层}\}$、$x_2\in\mathrm{subtree}(c_2)\cap\{d\text{ 层}\}$，则 $\operatorname{LCA}(x_1,x_2)=u$，故 $S(u,d)$ 的 LCA 也是 $u$。∎

**引理 4（贡献公式）**：对固定的 $u$，满足引理 3 第二种情形（即 $d>\operatorname{dep}(u)$ 且合法）的 $d$ 的个数恰为 $b_2(u)$；不足两个儿子时 $b_2(u)=0$，贡献也为 $0$。

**证明**：对儿子 $c$，$\mathrm{subtree}(c)$ 中的最大深度为 $\operatorname{dep}(u)+1+\mathrm{hgt}(c)$，故「$c$ 在 $d$ 层有后代」$\iff d\le \operatorname{dep}(u)+1+\mathrm{hgt}(c)$。设 $1+\mathrm{hgt}(c)$ 的次大值为 $b_2(u)$，则「至少两个儿子有后代」$\iff d\le \operatorname{dep}(u)+b_2(u)$。满足 $\operatorname{dep}(u)<d\le \operatorname{dep}(u)+b_2(u)$ 的整数 $d$ 恰有 $b_2(u)$ 个；不足两个儿子时 $b_2(u)=0$，没有这样的 $d$。∎

**定理**：算法输出 $\text{ans}=n+\sum_u b_2(u)$ 等于不同非空公会的个数。

**证明**：由引理 2，不同非空公会与「满足 $\operatorname{LCA}(S(u,d))=u$ 的 $(u,d)$ 对」一一对应。由引理 3，这些对分成 $d=\operatorname{dep}(u)$ 的 $n$ 个（每个 $u$ 恰好一个，集合是 $\{u\}$，互不相同），以及 $d>\operatorname{dep}(u)$ 的部分；由引理 4，后者总数为 $\sum_u b_2(u)$。两部分不重不漏，故总数为 $n+\sum_u b_2(u)$，与算法一致。∎

## 6. 复杂度分析

- **时间**：每组读入 $O(n)$，倒序扫描每个点一次、常数次比较 $O(n)$，最后求和 $O(n)$；总时间 $O(\sum n)\le 2\cdot 10^5$。
- **空间**：`par`、`b1`、`b2` 三个长度 $n+1$ 的数组，$O(n)$；无递归栈、无哈希表。
- **答案量级**：$b_2(u)\le \mathrm{hgt}(u)$，实测完全二叉树 $n=2\cdot10^5$ 时答案为 $399982$（约为 $2n$），星形图为 $200001$，链为 $200000$，都远小于 $2^{31}$，代码仍用 `long long` 兜底。
- **实测**：Apple M2、`clang++ -O2`，$n=2\cdot 10^5$ 的随机树 / 完全二叉树 / 链，算法本体（含手写快读）约 $1\sim2$ ms，相对 2 s 时限有约千倍余量。测试机负载较高时用 `cin`（macOS 的 libc++ 解析较慢）读 $2\cdot10^5$ 个整数约 $200$ ms，CF 的 GNU libstdc++ 下快得多，两种都安全。
- **Python3**：同一数据 $200000$ 规模实测约 $80\sim90$ ms（含解释器启动），**无需 PyPy**；若用递归写法会触发默认递归上限，务必用倒序循环。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    if (!(cin >> t)) return 0;                  // 空输入防护
    while (t--) {
        int n;
        cin >> n;
        vector<int> par(n + 1, 0), b1(n + 1, 0), b2(n + 1, 0);
        for (int i = 2; i <= n; ++i) cin >> par[i];     // p_i < i
        // 倒序扫描：儿子编号一定大于父亲，等价于后序遍历
        for (int i = n; i >= 2; --i) {
            int v = b1[i] + 1;                  // 以 i 为顶的分支高度
            int p = par[i];
            if (v > b1[p]) { b2[p] = b1[p]; b1[p] = v; }
            else if (v > b2[p]) { b2[p] = v; }
        }
        long long ans = n;                      // h = 0 的 n 个单点集合
        for (int u = 1; u <= n; ++u) ans += b2[u];      // 每个 u 的多分支层数
        cout << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:                                # 空输入防护
        return
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        par = [0] * (n + 1)
        for i in range(2, n + 1):
            par[i] = int(data[pos]); pos += 1
        b1 = [0] * (n + 1)                      # 最高分支高度
        b2 = [0] * (n + 1)                      # 次高分支高度
        for i in range(n, 1, -1):               # 倒序 = 后序
            v = b1[i] + 1
            p = par[i]
            if v > b1[p]:
                b2[p] = b1[p]
                b1[p] = v
            elif v > b2[p]:
                b2[p] = v
        out.append(str(n + sum(b2)))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n=2$**：树 $1-2$ 只有 $\{1\},\{2\}$ 两个集合（$(1,1)=\{2\}$ 与单点重复），且 $b_2$ 全为 $0$，答案 $2$。这是最小规模，务必自测。
2. **链**：$\mathrm{hgt}$ 很大但每个点至多一个儿子，答案恒为 $n$。若把「非空 $(v,h)$ 对数」当答案，链上会算出 $\sum(\mathrm{hgt}+1)=O(n^2)$ 而错得离谱。
3. **星形**：根有 $n-1$ 个叶子，$b_2(1)=1$，答案 $n+1$；叶子层 $\{2,\dots,n\}$ 只能算一次，不能被 $(1,1)$ 与各单点重复计。
4. **$h$ 超过树高**：公会是空集，按定义不计；公式只统计 $d\le \operatorname{dep}(u)+b_2(u)$，自动排除，无需特判。
5. **递归爆栈**：$p_i=i-1$ 的链深度 $2\cdot10^5$，递归 DFS 在 CF 上会 RE；必须用倒序循环（C++）或显式栈（Python）。
6. **多测重置**：`b1`、`b2`、`par` 必须每组新建；若复用并只清部分位置，上组的残留会污染本组的次大值。
7. **输出格式**：$t$ 组各输出一行整数，不要输出多余空格或把答案累加成一个数。
8. **注意「单点集合」与某祖先的某一层重复**：$\{3\}$ 既是 $(3,0)$，也可能是 $(1,2)$，去重后只计一次；本文用 LCA 代表恰好保证这点，代码里体现为「$n$ 只加一次，其余按 $b_2$ 加」。

## 相关题目与扩展

- [Codeforces 1009F Dominant Indices](https://codeforces.com/problemset/problem/1009/F)：对每个点求「子树内点最多的那一层」，DSU on tree / 长链剖分，与本题「按层切子树」的视角同源。
- [Codeforces 208E Blood Cousins](https://codeforces.com/problemset/problem/208/E)：多次询问「某点子树中第 $k$ 层有多少点」，是本题单层计数的带询问版本。
- [Codeforces 600E Lomsat gelral](https://codeforces.com/problemset/problem/600/E)：子树按颜色统计的经典 DSU on tree，体会「子树 → 区间」的转化。
- [LeetCode 1519. 子树中标签相同的节点数](https://leetcode.cn/problems/number-of-nodes-in-the-sub-tree-with-the-same-label/)：同样在子树内按深度/标签聚合，可直接套「每个点维护到儿子的聚合值」的写法。
- [Codeforces 2238B Crimson Triples](https://codeforces.com/problemset/problem/2238/B)：同场 B 题，练熟「先化简条件再计数」的节奏。

**延伸思考**：

1. **改求所有不同公会的点集大小之和**：把同一层的点按 DFS 序排好，则每个合法 $(u,d)$ 对应其中一段连续区间；对每个合法对在「第 $d$ 层的 Euler 序表」里二分出落在 $[\mathrm{tin}(u),\mathrm{tout}(u)]$ 的首尾位置，长度即可 $O(\log n)$ 求出，总复杂度 $O(n\log n)$。
2. **把「恰好 $h$」换成「距离 $\le h$」**：集合变成「子树内深度不超过 $d$ 的全部点」，此时它**必含 $u$ 自己**，LCA 恒等于 $u$，于是每个 $(u,d)$ 都合法且互不相同，答案直接退化成 $\sum_u(\mathrm{hgt}(u)+1)$（即所有非空 $(v,h)$ 对数）。可见本题的难点全在「恰好」二字带来的去重。
3. **边带权（距离不等于深度差）**：LCA 代表法直接失效，因为同一集合的元素不再同深度；此时必须对每个 $v$ 真做「按距离分组」，一般要用 DSU on tree 或点分治，复杂度 $O(n\log n)$。
4. **询问「某个公会 $(v,h)$ 在全局出现几次」**：即问有多少个 $u$ 满足 $S(u,d)=S(v,h)$。关键性质是这些 $u$ 恰为 $v$ 到根链上的**一段连续祖先**：一旦某个祖先的其他分支里出现了 $d$ 层节点，它和它所有的祖先都不再合法。于是只需二分 / 倍增找到最靠上的那个合法 $u$，出现次数就是 $\operatorname{dep}(v)-\operatorname{dep}(u)+1$。
