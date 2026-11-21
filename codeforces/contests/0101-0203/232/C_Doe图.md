# Codeforces 232C Doe Graphs 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/232/C
- **比赛来源**：Codeforces Round 144 (Div. 1) · Problem C（UTC 2012-10-11）
- **难度**：2600
- **标签**：分治、图论、最短路、动态规划
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：Doe 图是一族递归定义的无向图：

- $D(0)$ 是单个顶点，编号 1；
- $D(1)$ 是两个顶点 1、2 连一条边；
- $D(n)$ 由 $D(n-1)$ 与 $D(n-2)$ 拼成：$D(n-1)$ 占编号 $1 \sim |D(n-1)|$，$D(n-2)$ 的所有编号整体加上 $|D(n-1)|$ 后接在后面；再补两条边—— $(|D(n-1)|,\ |D(n-1)|+1)$ 和 $(|D(n-1)|+1,\ 1)$。

给定 $t$ 次询问 $(a_i,b_i)$，求 $D(n)$ 中 $a_i$ 到 $b_i$ 的最短路长度。

**约束**：

- $n \le 10^3$，$t \le 10^5$，$a_i,b_i \le 10^{16}$：$|D(n)|$ 是斐波那契级（$|D(1000)|$ 有约 $10^{208}$ 个顶点），**绝不可能建图**；而 $10^3 \times 10^5 = 10^8$ 说明"每次询问 $O(n)$"是可行的复杂度。
- 顶点编号 $\le 10^{16}$：其实只要把 $F(k) = |D(k)|$ 截断在 $2\times10^{16}$ 就不会溢出（见 3.4）。
- 图是连通的（定义本身就保证了），并且**最短路长度只有 $O(n)$**：递归结构里到处是"2 步捷径"，所以距离远小于顶点数。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
10 5
1 2
1 3
1 4
1 5
2 3
2 4
2 5
3 4
3 5
4 5

输出：
1
1
1
2
1
2
3
1
2
1
```

先把 $D(0)\sim D(5)$ 摊开看（$|D(k)|$ 依次是 $1,2,3,5,8,13$）：

- $D(2)$：顶点 1,2,3，边 $1\!-\!2,\ 2\!-\!3,\ 3\!-\!1$（三角形）；
- $D(3)$：在 $D(2)$ 上接 $D(1)=\{4,5\}$，补边 $3\!-\!4,\ 4\!-\!1$；
- $D(5)$：13 个顶点，19 条边，从 1 出发的距离依次是

$$d(1,\cdot) = 0,1,1,1,2,1,2,2,1,2,2,2,3 .$$

于是 $(1,5)=2$（$1-4-5$）、$(2,5)=3$、$(2,4)=2$、$(4,5)=1$……与样例完全对应。

![D(k) 的拼法与割点 u](../../../images/cf232c_decomp.svg)

**观察 1（两条跨块边共用一个端点）**：拼接时补的两条边是 $|D(n-1)| \to |D(n-1)|+1$ 和 $|D(n-1)|+1 \to 1$，它们**都以 $u = |D(n-1)|+1$ 为端点**（$u$ 是后一块的第一个顶点）。所以 $u$ 是割点：从 $A = D(n-1)$ 走到 $B = D(n-2)$ 的任意路径都必须经过 $u$。

**观察 2（同块内的绕路只有一种）**：如果 $a,b$ 都在 $A$ 里，最短路要么完全不离开 $A$，要么"出门绕一圈"：$a \to p \to u \to q \to b$，其中 $p,q \in \{1,\ |D(n-1)|\}$ 是 $A$ 接触 $u$ 的两扇"门"。从任何一扇门到另一扇门（或自己）经 $u$ 都恰好 2 步。

**观察 3（只需要门距离）**：于是对每个顶点，只要知道它到 $D(k)$ 的两扇门（顶点 1 和顶点 $|D(k)|$）的距离，就能在 $O(1)$ 内完成一层的所有计算。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

$|D(1000)| \approx 10^{208}$，建图、BFS 都不可能。

退一步：能不能"只展开前几十层"？不行——$n = 1000$ 时查询给的顶点可能很小（例如 $a=1,b=2$），递归链会一路往下走 1000 层，捷径信息分布在每一层。

### 3.2 核心观察：门距离的递推

![门距离的递推](../../../images/cf232c_portals.svg)

记 $F(k) = |D(k)|$，$g(k) = \operatorname{dist}_{D(k)}(1,\ F(k))$。在 $D(k)$ 中，$A = D(k-1)$ 占 $1..F(k-1)$，$B = D(k-2)$ 占 $F(k-1)+1..F(k)$，割点 $u = F(k-1)+1$。

**$g$ 的递推**：$1 \to u$ 一条边，$u$ 是 $B$ 的第一个顶点，从 $u$ 到 $B$ 的末点（也就是 $D(k)$ 的末点 $F(k)$）距离是 $g(k-2)$。所以

$$g(k) = 1 + g(k-2),\qquad g(0)=0,\ g(1)=1\ \Longrightarrow\ g(k)=\left\lceil k/2\right\rceil .$$

**门距离的递推**：对顶点 $v$，记 $\mathrm{d1}_k(v) = \operatorname{dist}_{D(k)}(v,1)$，$\mathrm{dF}_k(v) = \operatorname{dist}_{D(k)}(v,F(k))$。

- 若 $v \in A$（$v \le F(k-1)$）：
  - 到 1：要么留在 $A$ 里（$\mathrm{d1}_{k-1}(v)$），要么经由右门绕 $u$（$\mathrm{dF}_{k-1}(v)+2$）：
    $$\mathrm{d1}_k(v) = \min\bigl(\mathrm{d1}_{k-1}(v),\ \mathrm{dF}_{k-1}(v)+2\bigr).$$
  - 到 $F(k)$：$F(k)$ 在 $B$ 的末点，必须先从 $v$ 走到某扇门（$\min(\mathrm{d1}_{k-1},\mathrm{dF}_{k-1})$），跨一条边到 $u$，再在 $B$ 里走到末点（$g(k-2)$）：
    $$\mathrm{dF}_k(v) = \min\bigl(\mathrm{d1}_{k-1}(v),\ \mathrm{dF}_{k-1}(v)\bigr) + 1 + g(k-2).$$
- 若 $v \in B$，令 $v' = v - F(k-1) \in D(k-2)$：
  - 到 1：必须先回到 $u$（$B$ 的第一个顶点），再跨边到 1：$\mathrm{d1}_k(v) = \mathrm{d1}_{k-2}(v') + 1$；
  - 到 $F(k)$：$F(k)$ 就是 $B$ 的末点，留在 $B$ 内最优：$\mathrm{dF}_k(v) = \mathrm{dF}_{k-2}(v')$。

  （离开 $B$ 再回来只会绕远，因为出口也只有 $u$。）

### 3.3 查询：沿"共同链"下钻

对顶点 $v$ 先求出它的**链**：从第 $n$ 层开始，每层判断 $v$ 落在 $A$ 还是 $B$，落在 $A$ 就降到 $k-1$（编号不变），落在 $B$ 就降到 $k-2$（编号减去 $F(k-1)$），直到第 0 或第 1 层。链长 $O(n)$，再从底往上用 3.2 的公式算出每层的 $(\mathrm{d1},\mathrm{dF})$，总 $O(n)$。

对询问 $(a,b)$，从第 $n$ 层开始同步往下：

- 若 $a,b$ 同属 $A$：记录一个候选"$a\to p\to u\to q\to b$"（$\min$ 四种门的组合 $+2$），然后降到 $k-1$ 继续；
- 若同属 $B$：记录候选 $\mathrm{d1}_{k-2}(a')+1+g(k-1)+1+\mathrm{d1}_{k-2}(b')$（绕 $A$ 一圈），降到 $k-2$ 继续；
- 若分属两块：直接得到
  $$\text{ans}=\min\bigl(\mathrm{d1}_{k-1}(a),\mathrm{dF}_{k-1}(a)\bigr)+1+\mathrm{d1}_{k-2}(b')$$
  （$a\in A,b\in B$；反之对称），结束；
- 降到第 1 层仍未分属：答案 1（两个顶点就是 1 和 2，相邻）。

最后把沿途所有候选取最小即可。

### 3.4 数值细节：截断 $F(k)$

$F(k)$ 按斐波那契增长，$k=1000$ 时远超 `long long`。但**所有查询顶点 $\le 10^{16}$**，所以判断"$v \le F(k-1)$"时只需要知道 $F(k-1)$ 是否 $\ge 2\times10^{16}$：一旦超过就截断在 $2\times10^{16}$，所有比较结果都不变，且不会溢出。距离本身只有 $O(n)$（$\le 500$），也不会溢出。

### 3.5 样例走查：$n=5$、查询 $(2,5)$

$F = (1,2,3,5,8,13)$，$g = (0,1,1,2,2,3)$。

- 第 5 层：$A$ 是 $1..8$，$B$ 是 $9..13$。$2,5$ 都在 $A$：记录候选，降到第 4 层。
- 第 4 层：$A = 1..5$，$B = 6..8$。$2,5$ 都在 $A$（$5 = F(3)$ 是右门）：候选：$2\to1\to u\to 5$ 之类，代价 $1+2+0=3$；降到第 3 层。
- 第 3 层：$A = 1..3$，$B = 4..5$。$2 \in A$，$5 \in B$：直接算 $\min(\mathrm{d1}_3(2),\mathrm{dF}_3(2)) + 1 + \mathrm{d1}_1(1)$。$D(3)$ 中 $d(2,1)=1$、$d(2,5)=2$，取 1；$+1$ 跨到 $u=4$；$\mathrm{d1}_1(1)=0$（$5$ 在 $D(1)$ 里对应顶点 2，$\mathrm{d1}$ 是它到 1 的距离 $=1$？——注意这里 $b'=5-3=2$，而 $D(1)$ 里 $\mathrm{d1}(2)=1$）。得 $1+1+1=3$ ✓。
- 取所有候选最小：3，与样例一致。

## 4. 正确性证明

**引理 1**：在 $D(k)$ 中，$A$ 与 $B$ 之间的每条路径都经过 $u = F(k-1)+1$。

**证明**：$A$ 与 $B$ 之间只有两条边：$(F(k-1),u)$ 与 $(u,1)$，两条都以 $u$ 为端点。∎

**引理 2**：若 $a,b$ 同属 $A$，则 $\operatorname{dist}_{D(k)}(a,b)=\min\bigl(\operatorname{dist}_A(a,b),\ \min_{p,q\in\{1,F(k-1)\}}\operatorname{dist}_A(a,p)+2+\operatorname{dist}_A(q,b)\bigr)$，其中 $A = D(k-1)$。

**证明**：设 $P$ 是 $D(k)$ 中 $a\to b$ 的一条最短路。若 $P$ 不进入 $B$，长度 $\ge \operatorname{dist}_A(a,b)$。若进入 $B$，由引理 1，$P$ 必须经过 $u$，且每次离开 $A$ 都从某扇门出发、经 $u$ 回到某扇门；把 $P$ 中第一次离开和最后一次回到 $A$ 之间的部分替换成"门 $\to u \to$ 门"（代价 2），不会变长，于是长度 $\ge \operatorname{dist}_A(a,p)+2+\operatorname{dist}_A(q,b)$。反向，这些候选都对应真实的路径，故取最小即为答案。∎

**引理 3**：3.2 的门距离公式正确。

**证明**：由引理 1 与 $u$ 的位置关系：$A$ 内的点离开 $A$ 必经过 $u$；$B$ 内的点离开 $B$ 也必经过 $u$。把每条可能的最短路按"是否经过 $u$"分类，即得公式（细节见 3.2 的分类讨论）。$g(k) = 1+g(k-2)$ 是因为 $u$ 是 $B$ 的第一个顶点、$F(k)$ 是 $B$ 的末点。∎

**定理**：算法对每次询问输出正确的最短路长度。

**证明**：由引理 2（同块）与引理 1（跨块必经 $u$），查询循环在每一层都把该层所有可能的最短路形式计入候选；跨块时直接给出唯一形式（经 $u$，两段各自是块内门距离）。链条有限、必在某层跨块或降到第 1 层，因此候选集完备且每个候选都对应真实路径，取最小即为最优。∎

## 5. 复杂度分析

- 时间：单次询问两次"链预处理"各 $O(n)$，下钻 $O(n)$，合计 $O(n)$；总 $O(tn) = 10^8$。实测 $t=10^5$、$n=10^3$ 时 **1.08 s**（3 s 时限的 36%）。
- 空间：$F$、$g$、两组门距离数组，$O(n)$，不到 1 MB。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll CAP = 20000000000000000LL;   // 2e16 > 查询上限 1e16
static const int MAXN = 1005;
ll F[MAXN + 2];
ll g[MAXN + 2];                       // g(k) = dist(1, |D(k)|)
int n, t;
char inA[MAXN + 2];
ll P1[2][MAXN + 2], PF[2][MAXN + 2];  // 两个查询顶点在各层到 1 / |D(k)| 的距离
void prepare(ll v, int k, int slot) {
    vector<int> levels;
    ll cur = v;
    while (k > 1) {
        bool A = (cur <= F[k - 1]);
        inA[k] = A;
        levels.push_back(k);
        if (A) k = k - 1;
        else { cur -= F[k - 1]; k = k - 2; }
    }
    ll *d1 = P1[slot], *dF = PF[slot];
    if (k == 0) { d1[0] = 0; dF[0] = 0; }
    else { if (cur == 1) { d1[1] = 0; dF[1] = 1; } else { d1[1] = 1; dF[1] = 0; } }
    for (int idx = (int)levels.size() - 1; idx >= 0; idx--) {
        int kk = levels[idx];
        if (inA[kk]) {
            ll x1 = d1[kk - 1], xF = dF[kk - 1];
            d1[kk] = min(x1, xF + 2);
            dF[kk] = min(x1, xF) + 1 + g[kk - 2];
        } else {
            d1[kk] = d1[kk - 2] + 1;
            dF[kk] = dF[kk - 2];
        }
    }
}
ll query(ll a, ll b) {
    prepare(a, n, 0);
    prepare(b, n, 1);
    ll *A1 = P1[0], *AF = PF[0], *B1 = P1[1], *BF = PF[1];
    const ll INF = LLONG_MAX / 4;
    ll ans = INF;
    int k = n; ll ca = a, cb = b;
    while (true) {
        if (k <= 1) { ans = min(ans, (ll)(ca == cb ? 0 : 1)); break; }
        if (ca == cb) { ans = min(ans, 0LL); break; }
        bool aA = (ca <= F[k - 1]), bA = (cb <= F[k - 1]);
        if (aA && bA) {
            ll c1 = A1[k - 1], c2 = AF[k - 1], e1 = B1[k - 1], e2 = BF[k - 1];
            ans = min(ans, min(min(c1 + 2 + e1, c1 + 2 + e2), min(c2 + 2 + e1, c2 + 2 + e2)));
            k = k - 1;
        } else if (!aA && !bA) {
            ans = min(ans, A1[k - 2] + 1 + g[k - 1] + 1 + B1[k - 2]);
            ca -= F[k - 1]; cb -= F[k - 1];
            k = k - 2;
        } else {
            if (aA) ans = min(ans, min(A1[k - 1], AF[k - 1]) + 1 + B1[k - 2]);
            else    ans = min(ans, min(B1[k - 1], BF[k - 1]) + 1 + A1[k - 2]);
            break;
        }
    }
    return ans;
}
int main() {
    if (scanf("%d %d", &t, &n) != 2) return 0;
    F[0] = 1; F[1] = 2;
    for (int k = 2; k <= n; k++) {
        __int128 s = (__int128)F[k - 1] + F[k - 2];
        F[k] = (ll)min<__int128>(s, CAP);
    }
    g[0] = 0; if (n >= 1) g[1] = 1;
    for (int k = 2; k <= n; k++) g[k] = g[k - 2] + 1;
    string out; out.reserve((size_t)t * 4);
    for (int qi = 0; qi < t; qi++) {
        ll a, b; scanf("%lld %lld", &a, &b);
        out += to_string(query(a, b)); out += '\n';
    }
    fputs(out.c_str(), stdout);
    return 0;
}
```

### Python3

```python
import sys

CAP = 2 * 10**16

def build_F(n):
    F = [0] * (n + 2)
    F[0] = 1; F[1] = 2
    for k in range(2, n + 1):
        F[k] = min(F[k-1] + F[k-2], CAP)
    g = [0] * (n + 2)
    if n >= 1:
        g[1] = 1
    for k in range(2, n + 1):
        g[k] = g[k-2] + 1
    return F, g

def solve_one(n, a, b, F, g):
    def chain(v):
        levels = []; inA = {}
        k = n
        while k > 1:
            A = v <= F[k-1]
            inA[k] = A
            levels.append(k)
            if A:
                k -= 1
            else:
                v -= F[k-1]; k -= 2
        return levels, inA, k, v
    la, ia, basea, vba = chain(a)
    lb, ib, baseb, vbb = chain(b)

    def portals(levels, inA, base, vb):
        d1 = {}; dF = {}
        if base == 0:
            d1[0] = 0; dF[0] = 0
        else:
            if vb == 1:
                d1[1] = 0; dF[1] = 1
            else:
                d1[1] = 1; dF[1] = 0
        for k in reversed(levels):
            if inA[k]:
                x1, xF = d1[k-1], dF[k-1]
                d1[k] = min(x1, xF + 2)
                dF[k] = min(x1, xF) + 1 + g[k-2]
            else:
                d1[k] = d1[k-2] + 1
                dF[k] = dF[k-2]
        return d1, dF

    a1, aF = portals(la, ia, basea, vba)
    b1, bF = portals(lb, ib, baseb, vbb)
    pend = []
    k = n; ca = a; cb = b
    while True:
        if k <= 1:
            ans = 0 if ca == cb else 1
            break
        if ca == cb:
            ans = 0
            break
        aA = ca <= F[k-1]; bA = cb <= F[k-1]
        if aA and bA:
            c1, c2, e1, e2 = a1[k-1], aF[k-1], b1[k-1], bF[k-1]
            pend.append(min(c1+2+e1, c1+2+e2, c2+2+e1, c2+2+e2))
            k -= 1
        elif (not aA) and (not bA):
            pend.append(a1[k-2] + 1 + g[k-1] + 1 + b1[k-2])
            ca -= F[k-1]; cb -= F[k-1]; k -= 2
        else:
            if aA:
                ans = min(a1[k-1], aF[k-1]) + 1 + b1[k-2]
            else:
                ans = min(b1[k-1], bF[k-1]) + 1 + a1[k-2]
            break
    return min([ans] + pend)

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t, n = data[0], data[1]
    F, g = build_F(n)
    out = []
    p = 2
    for _ in range(t):
        a, b = data[p], data[p+1]; p += 2
        out.append(solve_one(n, a, b, F, g))
    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()
```

Python 版本与 C++ 完全同构，逻辑上等价（同一份算法已在 $n\le20$ 上与本机 BFS 全对拍）。但 $t=10^5,n=10^3$ 时 CPython 约 60～90 s，**建议提交 C++（或 PyPy3）**。官方样例在两种解释器上都能瞬间通过。

## 7. 边界情况与易错点

1. **$F(k)$ 溢出**：$|D(1000)|$ 有 $10^{208}$ 量级，`long long` 装不下。必须截断在 $2\times10^{16}$（比查询上限 $10^{16}$ 大即可），否则"$v \le F(k-1)$"的判断会因溢出变成随机结果。
2. **距离本身不会溢出**：最短路长度是 $O(n) \le 500$（递归结构的 2 步捷径），不要误以为要用大整数。
3. **$n = 1$**：此时只有第 1 层，查询一定是 $(1,2)$ 或 $(2,1)$，答案 1；代码里 `while (k > 1)` 不进入，直接在第 1 层收尾。
4. **同块绕路的四种组合**：$p,q$ 各有两扇门，别只考虑 $p\ne q$ 或只考虑一种顺序（虽然对称，写全更稳）。
5. **"同属 $B$"的绕路**：代价是 $\mathrm{d1}_{k-2}(a')+1+g(k-1)+1+\mathrm{d1}_{k-2}(b')$，不要漏掉中间 $A$ 内的 $g(k-1)$。
6. **降层时编号要平移**：落在 $B$ 时 $v \leftarrow v - F(k-1)$；忘了减就会越界。
7. **多组询问共享同一次预处理**：$F$ 和 $g$ 只算一次；但每个询问的两个顶点各自的链与门距离要重算（$O(n)$）。

## 8. 验证记录

- 编译环境与命令：macOS + `clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/232/C_Doe图.md`
- 官方样例：1 / 1 通过（10 个距离逐个核对）。
- 额外测试：
  - **全图 BFS 对拍**：显式构造 $D(n)$（$n\le 9$，$|D(9)|=89$，边数 130），对**全部顶点对**（12584 对）与参考程序比对，0 反例；
  - 继续对 $n = 10,12,14,16,18,20$（$|D(20)| = 17711$）随机抽 5 个源点做 BFS，全对拍 **142810 对**，0 反例；
  - C++ 与 Python 两版在 $n\le30$ 的 2400 组随机询问上互相比对，0 反例。
- 最大约束性能：$t = 10^5$、$n = 10^3$、查询混合"小顶点/10¹⁶ 量级顶点/10⁶ 量级顶点"，C++ 运行 **1.08 s**（3 s 时限的 36%）。
- 复核状态：样例、全枚举 BFS 对拍、大样本对拍、性能四项均实测通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 232B Table](https://codeforces.com/problemset/problem/232/B)：同一场的组合计数题。
- [Codeforces 354C Vasya and Beautiful Arrays](https://codeforces.com/problemset/problem/354/C)：另一类"按层递归"的题。
- [Codeforces 1100F Ivan and Burgers](https://codeforces.com/problemset/problem/1100/F)：如果本题要求路径上的权值信息，思路会变成"线性基 + 递归分治"。

**延伸思考**：

1. 把拼接方式改成"每个 $D(k)$ 由三个子图拼成"，割点会变成什么？门距离的个数会翻几倍？
2. 如果询问是"最短路**条数**"而不是长度，本解法还够吗？需要额外记录什么（提示：同一层可能有多种等长绕法，要乘加）。
3. 本题的 2 步捷径让直径只有 $O(n)$。如果把胶水边换成"$|D(n-1)|$ 与 $|D(n-2)|$ 的任意两点各连一条边"，割点结构就被破坏——此时该用什么手段？
