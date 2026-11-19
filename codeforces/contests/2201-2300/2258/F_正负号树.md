# Codeforces 2258F 正负号树 题解

## 1. 题目概述

- **标题 / 题号**：正负号树（Codeforces 2258F，英文名 Plus Minus Tree）
- **链接**：https://codeforces.com/problemset/problem/2258/F
- **来源**：Codeforces Round 1118 (Div. 2) · Problem F
- **难度**：3000（3000 分，本场压轴）
- **限制**：时间 3 s / 内存 256 MB
- **标签**：树形 DP、凸函数（斜率技巧）、可合并有序多重集、贪心、DFS

**题意**：给定一棵以 $1$ 为根的树，每个点有初始权 $a_v\in\{-1,0,+1\}$。把所有 $a_v=0$ 的点改写成 $-1$ 或 $+1$，得到最终权 $x_v\in\{-1,+1\}$（非零点不变）。记 $T_v$ 为 $v$ 的子树，子树权 $f(v)=\sum_{u\in T_v}x_u$，点 $v$ 的代价是 $|f(v)|$，整棵树的总代价是 $\sum_{v}|f(v)|$。求最小的总代价。

多测：第一行 $t$；每组第一行 $n$，第二行 $a_1,\dots,a_n$，随后 $n-1$ 行边。对每组输出一个整数。

**约束**：

- $1\le t\le 10^4$，$2\le n\le 2\times 10^5$，$\sum n\le 2\times 10^5$，$a_i\in\{-1,0,1\}$；
- 每个 $f(v)$ 与子树大小 $s_v$ 同奇偶，且 $|f(v)|\le s_v$——这是所有"下界"论证的来源；
- 答案上界：链且全固定 $+1$ 时 $\sum_v s_v=\frac{n(n+1)}{2}\approx 2\times 10^{10}$，**必须用 `long long`**；
- 时限 3 s 且 $\sum n\le 2\times10^5$，需要 $O(n\log n)$ 级别（逐点枚举 $k$ 是 $O(n^2)$）。

## 2. 示例与观察
官方样例：

```text
输入
2
5
0 1 -1 0 1
1 2
1 3
2 4
2 5
8
1 -1 1 -1 1 -1 1 -1
1 2
2 3
2 4
3 5
4 6
6 7
2 8

输出
5
7
```

- 第 1 组：自由点是 $1$ 和 $4$，取 $x=[-1,+1,-1,-1,+1]$（或把 $x_1$ 换成 $+1$）时，每个点都有 $|f(v)|=1$，总代价 $5$，正好等于下界（只有 $s_v$ 为奇数的点必须付 $1$）。
- 第 2 组：全点固定，唯一方案。$f_5=1$，于是 $f_3=x_3+f_5=2$，尽管 $s_3=2$ 是偶数、本该白拿 $0$；下界 $\sum(s_v\bmod 2)=5$，而答案是 $7$——**"每点都取到下界"一般做不到**，这正是本题要 DP 的原因。

**自造样例**（全自由链 / 混合 / 全固定链）

```text
输入
3
4
0 0 0 0
1 2
2 3
3 4
3
0 1 0
1 2
2 3
3
1 1 1
1 2
2 3

输出
2
2
6
```

- 第 1 组：$s=(4,3,2,1)$，奇数大小的点有 $2$ 个，答案 $2$ 达到下界；
- 第 2 组：$f_3$ 只能取 $0$（$x_3$ 自由），$f_2=x_2+f_3=1$，$f_1=x_1+1\in\{0,2\}$，故 $|f|=1+1+0=2$；
- 第 3 组：全固定 $+1$，各点 $|f(v)|=s_v$，答案 $3+2+1=6$。

## 3. 解题思路

### 3.1 暴力思路

自由点有 $m=\#\{v:a_v=0\}$ 个，枚举 $2^m$ 种赋值，每次 $O(n)$ 自底向上求和再累加 $|f(v)|$，复杂度 $O(2^m n)$。

不存在自由点时它退化成唯一解；但只要自由点多（比如一条 $2\times10^5$ 的全零链）就完全不可行。更糟的是：**每个点独立取"最小可能的 $|f(v)|$"也不行**。样例 2 里 $f_3$ 被儿子钉死成 $2$（$s_3$ 是偶数却付 $2$）；而且为了凑出父结点更划算的 $f(v)$，有时必须让某个儿子偏离它自己的最优值——例如链 $1-2-3-4-5$、$a=(+1,+1,+1,0,0)$，最优赋值是 $f=(1,0,-1,-2,-1)$、代价 $5$，其中 $f_4=-2$（自己最优本是 $0$、代价 $1$）被换成了代价 $3$，只为让 $f_2=0$、$f_1=1$。所以必须把"代价关于 $f(v)$ 的完整曲线"一路传上去。

### 3.2 核心观察：凸代价函数 + 「每降 2 的边际代价」

![g_v(k) 是凸函数：只需记录把 f(v) 再降 2 的边际代价](../../../images/cf2258f_convex_dp.svg)

固定一个点 $v$，定义

$$g_v(k)=\min\{\text{子树 }v\text{ 内部总代价}:\ f(v)=k\}.$$

**关键事实 1（可达集是区间）**：$g_v$ 的定义域是公差为 $2$ 的区间 $[lo_v,hi_v]$。设 $t=\sum_{c}f(c)$，则 $t$ 的可达集是各儿子区间的 Minkowski 和，仍是公差 $2$ 的区间 $[\sum lo_c,\sum hi_c]$；再由 $f(v)=t+x_v$：

$$lo_v=\sum_c lo_c+\begin{cases}a_v,&a_v\neq 0\\-1,&a_v=0\end{cases},\qquad
hi_v=\sum_c hi_c+\begin{cases}a_v,&a_v\neq 0\\+1,&a_v=0\end{cases}$$

**关键事实 2（凸性）**：把 $k$ 换成下标 $i=\frac{s_v-k}{2}$ 后，$g_v$ 关于 $i$ 是离散凸的，即"增量"

$$e(i)=g_v(i)-g_v(i-1)\quad(i=lo_v+1,\dots,hi_v)$$

整体非降。于是**整条曲线只需一个有序多重集**：把 $e(lo_v+1),\dots,e(hi_v)$ 排好序存下来。语义上，$e$ 就是**把 $f(v)$ 再往下压 $2$（让 $x$ 们更偏 $-1$）的边际代价**。

自底向上只有三种动作，全部落在"多重集"上：

| 动作 | 对增量多重集的影响 |
|------|------------------|
| 合并所有儿子（$t=\sum_c f(c)$） | 多重集**求并**（谁便宜就先压谁，来源被"池化"） |
| $a_v=0$（自由） | **插入一个 $0$**：翻转 $x_v$ 恰好白换一步 |
| $a_v=\pm1$（固定） | 不插；窗口整体平移（$a_v=-1$ 时右移一格） |
| 加上 $|f(v)|=|s_v-2i|$ | 位置 $i\le A$ 的增量 $-2$，$i\ge B+1$ 的 $+2$ |

最后一条的直觉：$|k|$ 在 $k>0$ 一侧每降 $2$ 就省 $2$，在 $k<0$ 一侧每降 $2$ 反而多花 $2$，而 $i$ 与 $k$ 是一一对应的（$k=s_v-2i$），所以"正侧整段 $-2$、负侧整段 $+2$"。当 $S+1$ 为奇数时还有**一格**，它恰好是从 $k=+1$ 跨到 $k=-1$ 的那一步，$|k|$ 不增不减，加 $0$。

### 3.3 算法流程

![并 → 插入 → 按名次切三段](../../../images/cf2258f_slope_ops.svg)

记 $S=s_v-1=\sum_c s_c$，$A=\lfloor (S+1)/2\rfloor$，$B=\lceil (S+1)/2\rceil$，$ninc=hi_v-lo_v$。

1. **并**：递归算完所有儿子，把它们的 treap 用 `unite` 两两并起来（多重集求并），同时累加 $S$、$\sum lo_c$、$\sum hi_c$、$\sum at\_lo_c$。
2. **顶点自己**：若 $a_v=0$，插入一个增量 $0$，并令 $hi\mathrel{+}=1$；若 $a_v=-1$，令 $lo,hi$ 同时 $+1$（窗口右移）；$a_v=+1$ 时不动。
3. **切三段**：按名次把多重集分成 $[1,k_1]$、$(k_1,k_1+cnt]$、$(k_1+cnt,ninc]$，其中
   $$k_1=\operatorname{clamp}(A-lo,0,ninc),\qquad k_2=\operatorname{clamp}(B-lo,0,ninc),\qquad cnt=ninc-k_2 .$$
   前缀整段 $-2$，中段（最多一个元素）不动，后缀整段 $+2$（均用 lazy 标记，$O(1)$）。
4. **记录左端值**：$at\_lo_v=\sum_c at\_lo_c+|hi_v|$，它等于"所有自由点都取 $+1$"时的子树代价，也就是窗口最左端（$k=hi_v$）的函数值。
5. 根节点算完后，答案 $=at\_lo_1+\sum_{e<0}e$：增量非降，从最左端一路向右走，先把所有负增量（省钱的步）走完就是最小值。

### 3.4 示例演算

![样例 1 走查：自底向上，增量多重集怎样长出来](../../../images/cf2258f_walkthrough.svg)

以第 1 组为例（$s=(5,3,1,1,1)$，自由点为 $1,4$），自底向上：

| 顶点 | $a_v$ | $f(v)$ 区间 | 增量表 | 代价 $k:cost$ |
|------|-------|-------------|--------|----------------|
| 4 | $0$（自由叶子） | $[-1,1]$ | $[0]$ | $-1:1,\ 1:1$ |
| 5 | $+1$（固定叶子） | $\{1\}$ | $\varnothing$ | $1:1$ |
| 3 | $-1$（固定叶子） | $\{-1\}$ | $\varnothing$ | $-1:1$ |
| 2 | $+1$ | $[1,3]$ | $[-2]$ | $3:5,\ 1:3$ |
| 1 | $0$ | $[-1,3]$ | $[-4,0]$ | $3:9,\ 1:5,\ -1:5$ |

- 叶子 $4$：$S=0$，$A=0$，$B=1$。合并为空，自由点插入 $[0]$，位置 $1=B$ 是中段 ⇒ 仍是 $[0]$；两端 $|k|=1$。
- 顶点 $2$：$S=2$（儿子 $4,5$），$A=B=1$；合并后 $[0]$ 位于位置 $1\le A$ ⇒ 变 $[-2]$。$at\_lo_2=1+1+|3|=5$。
- 顶点 $1$：$S=4$，$A=2$，$B=3$，窗口 $i\in[1,3]$。合并 $2,3$ 的增量得 $[-2]$，自由点插入 $0$ 得 $[-2,0]$，分别落在位置 $2,3$：位置 $2\le A$ 领 $-2$，位置 $3=B$ 是中段不动 ⇒ $[-4,0]$。$at\_lo_1=5+1+|3|=9$。
- 答案 $=9+(-4)+0=5$。

对照样例 2（全固定）：每个窗口都退化成单点，所有增量表为空，答案就是唯一的 $at\_lo_1=7$——与下界 $5$ 差 $2$，差的正是 $f_3$ 被钉死在 $2$ 的那一步。

## 4. 算法细节

1. **迭代建根序**：$n$ 可达 $2\times10^5$ 且树可能是链，绝不能用递归 DFS。用队列/栈求出 `par` 与 BFS 序，再倒序累加 `sub`，最后倒序做 DP。
2. **数据结构**：可合并平衡树（随机 treap），每个结点存 `键 / 左 / 右 / 子树大小 / lazy`。需要四种操作：按名次 `split`、按键 `split`、两树 `unite`、整树 `add`。
3. **键必须互不相同**：把键打包成 `(增量值 << 20) | 唯一编号`。若直接用增量值当键，星形图里所有增量都是 $0$，treap 求并会退化成一条右链，$n=2\times10^5$ 时从 $0.5$ s 变成 $240$ s（本实现实测），但答案仍正确——这是纯粹的复杂度陷阱。
4. **lazy 下推时机**：`split` 与 `unite` 向下走之前必须 `push`，否则子树的真实键值不对，切分位置会错。
5. **下标换算与 clamp**：位置 $p$ 对应 $k=s_v-2p$，所以"位置 $\le A$"的数量是 $A-lo$，需要 clamp 到 $[0,ninc]$；窗口整体偏在中心一侧时，前缀可能为空、后缀可能全满。
6. **中段那一格**：仅当 $S+1$ 为奇数时存在，位置恰为 $B$，它加 $0$（既不是 $-2$ 也不是 $+2$），实现上就是分割出的中段不做任何改动。
7. **多测清理**：treap 数组按测试点重建（总结点数 $O(\sum n)$，不会超内存）；`lo/hi/at/rt/sub/par` 全部按当前 $n$ 重新分配。
8. **溢出与 I/O**：`at_lo` 与答案用 `long long`（上界 $2\times10^{10}$）；C++ 关闭同步，Python 用 `sys.stdin.buffer.read().split()`。

## 5. 正确性证明

**引理 1**：对每个 $v$，可达的 $f(v)$ 构成公差 $2$ 的区间 $[lo_v,hi_v]$，且 $lo_v,hi_v$ 满足 3.2 的递推。

**证明**：对深度归纳。儿子的可达集都是公差 $2$ 的区间，其和集（Minkowski 和）仍是公差 $2$ 的区间 $[\sum lo_c,\sum hi_c]$（两个公差 $2$ 的整数区间之和仍连续）。固定点只有一个平移；自由点是两个相差 $2$ 的平移区间之并，因首尾相距 $2$ 而恰好拼成 $[\sum lo_c-1,\sum hi_c+1]$。∎

**引理 2**：以 $i=\frac{s_v-k}{2}$ 为自变量，$g_v$ 是离散凸的（增量非降）。

**证明**：归纳。儿子的 $g_c$ 凸；离散凸序列的 min-plus 卷积仍凸（它是若干线性函数的逐点最小值）；$|k|=|s_v-2i|$ 的增量序列是 $(-2,\dots,-2,0?,+2,\dots,+2)$，非降，加上去不破坏凸性；自由点的 $\min\{h(k-1),h(k+1)\}$ 是与两点序列 $\{0,0\}$ 的 min-plus 卷积，同理保持凸性。∎

**引理 3**（卷积 = 增量求并）：设 $f,g$ 是离散凸序列，增量多重集为 $E_f,E_g$，则 $h(t)=\min_{a+b=t}\big(f(a)+g(b)\big)$ 的增量多重集是 $E_f\cup E_g$ 排序后的结果。

**证明**：设 $f,g$ 的最小值取在 $0$（否则先平移），则 $f(a)=f(0)+\sum_{r\le a}e_f(r)$，$g(b)=g(0)+\sum_{r\le b}e_g(r)$。于是 $h(t)=f(0)+g(0)+\min\{\text{两组各自取前缀、总步数 }t\text{ 的最小和}\}$。由于两组增量都非降，"共取 $t$ 个前缀步"的最优方案就是取全体 $E_f\cup E_g$ 中最小的 $t$ 个（全局最小 $t$ 个自动对每个序列封闭成前缀）。因此第 $t$ 步的边际值恰为并集排序后的第 $t$ 个元素。∎

**引理 4**（三种局部操作）：设 $h$ 是儿子们的卷积。
（a）$a_v\neq0$：$g_v(k)=|k|+h(k-a_v)$，$a_v=+1$ 时窗口不动、$a_v=-1$ 时窗口右移一格，增量均不变；
（b）$a_v=0$：$g_v(k)=|k|+\min\{h(k-1),h(k+1)\}$，增量多重集为 $E_h\cup\{0\}$，$k$ 空间里窗口两端各扩一格（$i$ 下标里即 $hi\mathrel{+}=1$）；
（c）加上 $|k|$：位置 $i\le A$ 的增量 $-2$，位置 $i=B$（$S+1$ 为奇时）加 $0$，位置 $i\ge B+1$ 的 $+2$，其中 $A=\lfloor\frac{S+1}{2}\rfloor$，$B=\lceil\frac{S+1}{2}\rceil$。

**证明**：（a）是变量替换 $i\mapsto i+1$（或不变），增量序列逐项相同。（b）$\min\{h(k-1),h(k+1)\}$ 即 $h$ 与两点序列 $(0,0)$ 的 min-plus 卷积，而 $(0,0)$ 的唯一增量是 $0$，由引理 3 得 $E_h\cup\{0\}$。（c）设 $u=S+1-2i$，则 $|k|$ 贡献的增量是 $|u|-|u+2|$：$u\ge0$ 时等于 $-2$，$u=-1$ 时等于 $0$，$u\le-2$ 时等于 $+2$；而 $u\ge0\iff i\le\lfloor\frac{S+1}{2}\rfloor$，$u=-1\iff i=\frac{S+2}{2}$（只有 $S+1$ 为奇数时它才是整数，即中段那一格），$u\le-2\iff i\ge\lceil\frac{S+1}{2}\rceil+1$。∎

**定理**：算法对每个 $v$ 正确维护了 $g_v$ 的增量多重集与 $at\_lo_v$，并输出 $\min_k g_1(k)$。

**证明**：转移的每个环节（并、插入 $0$、平移、加 $|k|$、以及"按位置切段"）都由引理 1–4 保证；位置与名次的对应关系 $p=lo+r$ 保证切段范围正确。$at\_lo_v=\sum_c at\_lo_c+|hi_v|$ 由归纳可得：左端 $k=hi_v$ 时所有自由点取 $+1$、各儿子也在各自左端，故总代价等于 $|hi_v|$ 加各儿子左端代价。最后由引理 2 增量非降，从最左端出发累加增量，取完所有负增量后取到最小值，即 $at\_lo_1+\sum_{e<0}e$。∎

## 6. 复杂度分析

- **时间**：每个顶点做 $O(1)$ 次 treap 切分/合并（各 $O(\log n)$ 期望）与 $O(1)$ 次整段 lazy；treap 求并按随机优先级进行，把大小为 $m$ 的树并进大小为 $n$ 的树期望 $O\!\left(m\log\frac{n}{m}\right)$，沿树累计为 $O(n\log n)$。加上建树与遍历，总 $O(n\log n)$（期望）。
- **空间**：treap 结点数等于"历史上插入过的增量个数"，每个自由点只插一个 $0$，其余靠继承与合并复用 ⇒ $O(n)$ 个结点；value/id/sub/at/lo/hi 等数组 $O(n)$。总计 $O(n)$。
- **实测**（$n=2\times 10^5$，C++17 `-O2`，每种形态取三次最慢）：长链全零 $0.82$ s、长链随机固定 $0.66$ s、随机树全零 $0.86$ s、完全二叉树全零 $0.68$ s、菊花全零 $0.55$ s、扫帚形 $0.62$ s、$t=10^4$ 组 $n=20$ 共 $0.50$ s；最坏 $0.86$ s，峰值内存约 $29$ MB。相对 $3$ s 至少有 $3.4$ 倍余量。
- **Python**：同一算法的移植，最坏形态（长链 + 全自由点，treap 规模最大）在 CPython 下约 $11$ s，会超时；随机树/菊花/二叉树约 $3$–$4$ s。**正式提交建议用 PyPy 或 C++**；本题解仍给出等价的 Python 实现供对照。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

static const int SHIFT = 20;              // 结点编号 < 2^20
static const ll  SCALE = 1LL << SHIFT;    // 键 = 增量值 * SCALE + 编号

static uint64_t rngState = 0x243F6A8885A308D3ULL;
static inline uint64_t nextRand() {       // splitmix64：给 treap 随机优先级
    uint64_t z = (rngState += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

struct Treap {                            // 有序多重集：中序即排序后的增量
    vector<int> lc, rc, sz;
    vector<uint32_t> pri;
    vector<ll> key, lz;                   // lz 已乘过 SCALE

    Treap() {
        lc.assign(1, 0); rc.assign(1, 0); sz.assign(1, 0);
        pri.assign(1, 0); key.assign(1, 0); lz.assign(1, 0);
    }
    int newNode(ll v, int id) {
        lc.push_back(0); rc.push_back(0); sz.push_back(1);
        pri.push_back((uint32_t)(nextRand() >> 11));
        key.push_back(v * SCALE + id); lz.push_back(0);
        return (int)sz.size() - 1;
    }
    inline int size(int t) const { return t ? sz[t] : 0; }
    inline void applyAdd(int t, ll d) { if (t) { key[t] += d; lz[t] += d; } }
    inline void push(int t) {
        ll d = lz[t];
        if (d) { applyAdd(lc[t], d); applyAdd(rc[t], d); lz[t] = 0; }
    }
    inline void pull(int t) { if (t) sz[t] = 1 + size(lc[t]) + size(rc[t]); }

    void splitRank(int t, int k, int &A, int &B) {   // 前 k 个 -> A
        if (!t) { A = B = 0; return; }
        push(t);
        if (size(lc[t]) >= k) { int tmp; splitRank(lc[t], k, A, tmp); lc[t] = tmp; B = t; pull(B); }
        else { int tmp; splitRank(rc[t], k - size(lc[t]) - 1, tmp, B); rc[t] = tmp; A = t; pull(A); }
    }
    void splitKey(int t, ll v, int &A, int &B) {      // 键 < v -> A
        if (!t) { A = B = 0; return; }
        push(t);
        if (key[t] < v) { int tmp; splitKey(rc[t], v, tmp, B); rc[t] = tmp; A = t; pull(A); }
        else { int tmp; splitKey(lc[t], v, A, tmp); lc[t] = tmp; B = t; pull(B); }
    }
    int meldSorted(int a, int b) {                    // a 的键全部小于 b 的键
        if (!a) return b;
        if (!b) return a;
        if (pri[a] > pri[b]) { push(a); rc[a] = meldSorted(rc[a], b); pull(a); return a; }
        else { push(b); lc[b] = meldSorted(a, lc[b]); pull(b); return b; }
    }
    int unite(int a, int b) {                         // 多重集求并
        if (!a) return b;
        if (!b) return a;
        if (pri[a] < pri[b]) swap(a, b);
        push(a);
        int b1, b2;
        splitKey(b, key[a], b1, b2);
        lc[a] = unite(lc[a], b1);
        rc[a] = unite(rc[a], b2);
        pull(a);
        return a;
    }
};

static inline ll floorDivScale(ll k) {    // 键 -> 增量值（向负无穷取整）
    ll v = k / SCALE;
    if (k < 0 && k % SCALE != 0) v--;
    return v;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int TC;
    if (!(cin >> TC)) return 0;
    int idCounter = 0;
    while (TC--) {
        int n;
        cin >> n;
        vector<int> a(n + 1);
        for (int i = 1; i <= n; i++) cin >> a[i];
        vector<vector<int>> adj(n + 1);
        for (int i = 0; i < n - 1; i++) {
            int u, v; cin >> u >> v;
            adj[u].push_back(v); adj[v].push_back(u);
        }
        // 迭代建根：par 与 BFS 序
        vector<int> par(n + 1, 0), order, stk;
        order.reserve(n); stk.reserve(n);
        order.push_back(1); par[1] = -1;
        for (size_t i = 0; i < order.size(); i++) {
            int v = order[i];
            for (int w : adj[v]) if (w != par[v]) { par[w] = v; order.push_back(w); }
        }
        vector<int> sub(n + 1, 1);
        for (int i = n - 1; i > 0; i--) sub[par[order[i]]] += sub[order[i]];

        Treap tp;
        vector<int> rt(n + 1, 0), lo(n + 1, 0), hi(n + 1, 0), kh(n + 1, 0);
        vector<ll> at(n + 1, 0);

        for (int idx = n - 1; idx >= 0; idx--) {      // 逆 BFS 序 = 自底向上
            int v = order[idx];
            int S = 0, cLo = 0, cHi = 0, cKh = 0, root = 0;
            ll cAt = 0;
            for (int w : adj[v]) if (par[w] == v) {
                S += sub[w];
                cLo += lo[w]; cHi += hi[w]; cKh += kh[w]; cAt += at[w];
                root = tp.unite(root, rt[w]);
            }
            int av = a[v];
            if (av == 0) {                            // 自由点：多一个 0 增量
                root = tp.unite(root, tp.newNode(0, idCounter++));
                cHi++;
            } else if (av == -1) {                    // 固定 -1：窗口右移
                cLo++; cHi++;
            }
            // 加 |k|，k = s_v - 2i：位置 <= A 减 2，位置 >= B+1 加 2
            int ninc = cHi - cLo;
            int A_pos = (S + 1) / 2, B_pos = (S + 2) / 2;
            int k1 = A_pos - cLo; if (k1 < 0) k1 = 0; if (k1 > ninc) k1 = ninc;
            int k2 = B_pos - cLo; if (k2 < 0) k2 = 0; if (k2 > ninc) k2 = ninc;
            int cntPlus = ninc - k2;
            int Lp, rest, Mid, Rp;
            tp.splitRank(root, k1, Lp, rest);
            tp.splitRank(rest, ninc - k1 - cntPlus, Mid, Rp);
            tp.applyAdd(Lp, -2 * SCALE);
            tp.applyAdd(Rp, +2 * SCALE);
            root = tp.meldSorted(Lp, tp.meldSorted(Mid, Rp));

            int khv = cKh + (av >= 0 ? 1 : -1);
            cAt += (ll)llabs((ll)khv);
            lo[v] = cLo; hi[v] = cHi; kh[v] = khv; at[v] = cAt; rt[v] = root;
        }

        ll ans = at[1];                               // 左端值
        stk.clear(); stk.push_back(rt[1]);            // 再把所有负增量取走
        while (!stk.empty()) {
            int t = stk.back(); stk.pop_back();
            if (!t) continue;
            tp.push(t);
            ll v = floorDivScale(tp.key[t]);
            if (v < 0) ans += v;
            stk.push_back(tp.lc[t]);
            stk.push_back(tp.rc[t]);
        }
        cout << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    MASK = (1 << 64) - 1
    SHIFT = 20
    SCALE = 1 << SHIFT
    rng = [0x243F6A8885A308D3]

    def nxt():
        rng[0] = (rng[0] + 0x9E3779B97F4A7C15) & MASK
        z = rng[0]
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return (z ^ (z >> 31)) & MASK

    sys.setrecursionlimit(1 << 20)
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = [0] * (n + 1)
        for i in range(1, n + 1):
            a[i] = int(data[pos]); pos += 1
        adj = [[] for _ in range(n + 1)]
        for _e in range(n - 1):
            u = int(data[pos]); v = int(data[pos + 1]); pos += 2
            adj[u].append(v); adj[v].append(u)
        par = [0] * (n + 1)
        order = [1]; par[1] = -1
        head = 0
        while head < len(order):
            v = order[head]; head += 1
            pv = par[v]
            for w in adj[v]:
                if w != pv:
                    par[w] = v; order.append(w)
        sub = [1] * (n + 1)
        for i in range(n - 1, 0, -1):
            sub[par[order[i]]] += sub[order[i]]

        # 可合并 treap：键 = 增量值 * SCALE + 唯一编号
        lc = [0]; rc = [0]; sz = [0]; pri = [0]; key = [0]; lz = [0]

        def new_node(val, uid):
            lc.append(0); rc.append(0); sz.append(1)
            pri.append(nxt()); key.append(val * SCALE + uid); lz.append(0)
            return len(sz) - 1

        def push(x):
            d = lz[x]
            if d:
                y = lc[x]
                if y: key[y] += d; lz[y] += d
                y = rc[x]
                if y: key[y] += d; lz[y] += d
                lz[x] = 0

        def pull(x):
            sz[x] = 1 + sz[lc[x]] + sz[rc[x]]

        def splitRank(x, k):
            if not x:
                return 0, 0
            push(x)
            if sz[lc[x]] >= k:
                A, t = splitRank(lc[x], k)
                lc[x] = t; pull(x); return A, x
            else:
                t, B = splitRank(rc[x], k - sz[lc[x]] - 1)
                rc[x] = t; pull(x); return x, B

        def splitKey(x, v):
            if not x:
                return 0, 0
            push(x)
            if key[x] < v:
                t, B = splitKey(rc[x], v)
                rc[x] = t; pull(x); return x, B
            else:
                A, t = splitKey(lc[x], v)
                lc[x] = t; pull(x); return A, x

        def meldSorted(A, B):
            if not A: return B
            if not B: return A
            if pri[A] > pri[B]:
                push(A); rc[A] = meldSorted(rc[A], B); pull(A); return A
            else:
                push(B); lc[B] = meldSorted(A, lc[B]); pull(B); return B

        def unite(A, B):
            if not A: return B
            if not B: return A
            if pri[A] < pri[B]:
                A, B = B, A
            push(A)
            b1, b2 = splitKey(B, key[A])
            lc[A] = unite(lc[A], b1)
            rc[A] = unite(rc[A], b2)
            pull(A)
            return A

        rt = [0] * (n + 1); lo = [0] * (n + 1); hi = [0] * (n + 1)
        kh = [0] * (n + 1); at = [0] * (n + 1)
        uid = 0
        for idx in range(n - 1, -1, -1):
            v = order[idx]
            S = cLo = cHi = cKh = 0
            cAt = 0
            root = 0
            for w in adj[v]:
                if par[w] == v:
                    S += sub[w]
                    cLo += lo[w]; cHi += hi[w]; cKh += kh[w]; cAt += at[w]
                    root = unite(root, rt[w])
            av = a[v]
            if av == 0:
                root = unite(root, new_node(0, uid)); uid += 1
                cHi += 1
            elif av == -1:
                cLo += 1; cHi += 1
            ninc = cHi - cLo
            A_pos = (S + 1) // 2
            B_pos = (S + 2) // 2
            k1 = A_pos - cLo
            if k1 < 0: k1 = 0
            if k1 > ninc: k1 = ninc
            k2 = B_pos - cLo
            if k2 < 0: k2 = 0
            if k2 > ninc: k2 = ninc
            cntPlus = ninc - k2
            Lp, rest = splitRank(root, k1)
            Mid, Rp = splitRank(rest, ninc - k1 - cntPlus)
            if Lp:
                key[Lp] -= 2 * SCALE; lz[Lp] -= 2 * SCALE
            if Rp:
                key[Rp] += 2 * SCALE; lz[Rp] += 2 * SCALE
            root = meldSorted(Lp, meldSorted(Mid, Rp))
            khv = cKh + (1 if av >= 0 else -1)
            cAt += abs(khv)
            lo[v] = cLo; hi[v] = cHi; kh[v] = khv; at[v] = cAt; rt[v] = root

        ans = at[1]
        stack = [rt[1]]
        while stack:
            x = stack.pop()
            if not x: continue
            push(x)
            val = key[x] // SCALE          # Python 的 // 就是向下取整
            if val < 0: ans += val
            stack.append(lc[x]); stack.append(rc[x])
        out.append(str(ans))
    sys.stdout.write('\n'.join(out) + '\n')

main()
```

## 8. 边界情况与易错点

1. **没有自由点**（全固定）：每个窗口退化为单点，增量表全空，答案 $=at\_lo_1$，即唯一解的代价（样例 2）。此时任何"插 $0$"的写法都会立刻把答案算小。
2. **$n=2$**：最小规模，$a=[-1,1]$ 时 $f_2=1,f_1=0$，答案 $1$；$a=[1,-1]$ 时 $f_2=-1,f_1=0$，答案同样是 $1$；若写成"$at\_lo$ 加上所有负增量"，注意空增量表也要能正常返回 $at\_lo$。
3. **全自由链**：可以取到理论下界 $\sum_v(s_v\bmod 2)$（$n$ 偶时为 $n/2$）；这是检验实现有没有"多算"的基准。
4. **clamp 不能省**：当窗口整体偏在中心一侧（例如全固定 $-1$ 的链，窗口退化成单点且 $lo=s_v$ 很大）时，$A-lo$ 可能是负数而 $B-lo$ 可能大于 $ninc$，必须 clamp，否则切分返回错误的三段。
5. **中段那一格**：$S+1$ 为奇数时，位置 $B$ 的增量加 $0$，不是 $\pm2$。写错这一格会稳定偏差 $2$。
6. **键重复的性能陷阱**：增量值大量重复（菊花图全是 $0$）时，如果直接拿增量值当 treap 键，求并会退化成链，复杂度变 $O(n^2)$（本实现实测 $n=2\times10^5$ 从 $0.5$ s 变成 $240$ s），所以键要打包唯一编号。
7. **答案溢出**：链 + 全固定 $+1$ 时 $\sum s_v\approx 2\times10^{10}$，`int` 会溢出，必须 `long long`。
8. **多测**：treap 的数组、`uid`、各 DP 数组都按测试点重置；总插入量是 $O(\sum n)$，不会超内存，但绝不能跨测试点复用旧 treap。
9. **深链爆栈**：建根序与 DP 全部用迭代（队列 + 逆序），递归只出现在 treap 内部（期望深度 $O(\log n)$）。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：1 / 1 通过（按 Codeforces 标准 checker 的 token 比对，忽略空白与大小写）。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [Codeforces 713C Sonya and Problem Wihtout a Legend](https://codeforces.com/problemset/problem/713/C)：斜率技巧（slope trick）的入门题，同样是"凸代价 + 只改整段"。
- [Codeforces 1009F Dominant Indices](https://codeforces.com/problemset/problem/1009/F)：树形 DP 里"把儿子的结构合并上来"的另一种经典写法（长链剖分 / 按深度合并）。
- [Slope Trick 教程（zscoder）](https://codeforces.com/blog/entry/77298)：维护凸分段线性函数的堆式技巧，可与本题的"增量多重集"对照。

**延伸思考**：

1. 把 $|f(v)|$ 换成 $f(v)^2$：增量不再只有 $\pm2$ 两档，而是随位置线性增长，需要"带权斜率技巧"（李超树或对偶线段树），层次更高一层。
2. 若要求输出一组最优赋值：需要额外记录每个增量对应"哪一次压缩"，可以在 treap 结点上挂标记，回溯时还原每个自由点的 $x_v$。
3. 把"子树"换成"树上路径"：$f$ 的定义变了，可达集不再是简单区间，代价函数也未必凸，本题的两条主线（区间 + 凸）都会断掉。
4. 若把 $a_v\in\{-1,0,1\}$ 放宽到任意整数：自由点变成"可以取任意 $\pm1$ 的整数倍"，增量会变成等差结构，可用"等差数列 + 偏移量"的技巧压缩。
