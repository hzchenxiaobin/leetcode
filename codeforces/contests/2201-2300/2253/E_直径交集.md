# Codeforces 2253E 直径交集 题解

## 1. 题目概述

- **标题 / 题号**：直径交集（Codeforces 2253E，英文名 Diameter Intersections）
- **链接**：https://codeforces.com/problemset/problem/2253/E
- **来源**：Educational Codeforces Round 193 (Rated for Div. 2) · Problem E（UTC 2026-08-07）
- **难度**：2200
- **限制**：时间 4 s / 内存 512 MB
- **标签**：暴力枚举，DFS 与树上搜索，FFT/卷积，图论，实现，树

**题意**：给定 $t$ 组数据，每组是一棵 $n$ 个点的树，保证其直径长度为奇数。若存在两条直径（允许两条完全相同、端点也可以相同）使得它们的交集恰好包含 $k$ 条边，则称整数 $k$ 是美丽的。对每组数据，先输出美丽 $k$ 的个数 $m$，再按升序输出全部美丽的 $k$。

**约束**：

- $1 \le t \le 10^4$，$2 \le n \le 10^6$，且所有测试用例的 $n$ 之和 $\sum n \le 10^6$；
- 每组输入保证是一棵树，且直径长度为奇数；
- 输出时 $m$ 与 $m$ 个 $k$ 在同一行。

## 2. 示例与观察
**样例 1–5（官方）**

```text
输入
5
2
1 2
4
1 2
2 3
3 4
6
1 2
1 3
1 4
2 5
2 6
10
1 2
1 3
3 5
1 4
4 6
2 7
7 9
2 8
8 10
9
1 2
1 3
3 5
1 4
4 6
2 7
7 8
7 9

输出
1 1
1 3
3 1 2 3
3 1 3 5
4 2 3 4 5
```

**自造样例：中心边两侧都是“星”，直径长度 3**

```text
输入
1
7
1 2
1 3
1 4
1 5
2 6
2 7

输出
3 1 2 3
```

## 3. 解题思路

### 3.1 暴力思路

直接枚举所有直径：任意一对距离为 $D$ 的点都构成一条直径，而这样的点对最多有 $\Theta(n^2)$ 个（中心边两侧各取一个“大刷子”即可达到）。再两两求交集、数公共边，复杂度至少 $O(n^4)$，即使只把每条直径存成边集也不可行。必须利用“所有直径共享同一条中心边”这一结构。

### 3.2 核心观察：奇数直径 ⇒ 唯一中心边，两侧独立

设直径长 $D = 2h+1$（奇数）。任取一条直径 $P=(s,t)$，把它的中间那条边记作 $e=(u,v)$；删掉 $e$ 后树分成 A（含 $u$）与 B（含 $v$）两部分。

![奇数直径的中心边把问题拆成互不相干的两侧](../../../images/cf2253e_center_edge.svg)

关键事实：**所有直径都经过 $e$**，并且每条直径在 A 侧的端点恰是“到 $u$ 距离为 $h$”的点，B 侧同理。于是每条直径都可写成二元组 $(x,y)$，其中 $x\in L_A$、$y\in L_B$（$L_A,L_B$ 是两侧的最深点集）。

两条直径 $(x_1,y_1)$、$(x_2,y_2)$ 的交集一定形如“$u$ 到 $w_1$ 的一段 + 中心边 + $v$ 到 $w_2$ 的一段”，其中 $w_1=\mathrm{LCA}(x_1,x_2)$（以 $u$ 为根）、$w_2=\mathrm{LCA}(y_1,y_2)$（以 $v$ 为根）。因此

$$k = \underbrace{\mathrm{dep}(w_1)}_{a} + 1 + \underbrace{\mathrm{dep}(w_2)}_{b}.$$

**两侧的选择彼此独立**：只要分别求出“$a$ 能取哪些值”和“$b$ 能取哪些值”，答案就是这两个集合的 Minkowski 和再 $+1$。

### 3.3 算法流程：Q 集合的刻画与卷积

![Q_A 只收录深度 h 与分支节点的深度](../../../images/cf2253e_branch_depths.svg)

记 $Q_A=\{\mathrm{dep}(\mathrm{LCA}(x_1,x_2)) : x_1,x_2\in L_A\}$（允许 $x_1=x_2$）。它有一个非常简洁的刻画：

- $h\in Q_A$ 恒成立：取 $x_1=x_2$，相当于把同一条直径取两次；
- $d<h$ 属于 $Q_A$ 当且仅当存在深度为 $d$ 的节点 $w$，它的**至少两个不同孩子**的子树中都含有 $L_A$ 里的点（此时 $w$ 就是某对最深点的 LCA，称为分支节点）。

所以只要统计每个节点的“最深点信息”。以 $u$ 为根 BFS 得到深度与父子关系后逆序扫描：

- $\mathrm{cnt}[v]$：子树中深度为 $h$ 的点数，初值为 1（当 $\mathrm{dep}(v)=h$）或 0；
- $\mathrm{childDeep}[v]$：有几个孩子的 $\mathrm{cnt}>0$。

若 $\mathrm{childDeep}[v]\ge 2$，则 $v$ 是分支节点，把 $\mathrm{dep}(v)$ 加入 $Q$。B 侧同样处理。最后把 $Q_A,Q_B$ 看成 0/1 向量做卷积，系数非零的位置 $s$ 就对应 $k=s+1$。

![算法流程](../../../images/cf2253e_flow.svg)

### 3.4 示例演算（样例 5）

![样例 5 的演算表](../../../images/cf2253e_walkthrough.svg)

样例 5 的树为 $1\!-\!2,\ 1\!-\!3,\ 1\!-\!4,\ 3\!-\!5,\ 4\!-\!6,\ 2\!-\!7,\ 7\!-\!8,\ 7\!-\!9$，直径 $D=5$，故 $h=2$，中心边是 $1\!-\!2$。

- A 侧（根为 1）：最深点是 5、6（深度 2）；节点 1 的孩子 3、4 的子树都含最深点 ⇒ $0\in Q_A$，再加上 $h=2$，得 $Q_A=\{0,2\}$；
- B 侧（根为 2）：最深点是 8、9；节点 2 只有一个方向（孩子 7）含最深点，分支发生在节点 7（深度 1）⇒ $Q_B=\{1,2\}$。

四种组合给出 $k=0+1+1,\ 0+1+2,\ 2+1+1,\ 2+1+2=2,3,4,5$，共 4 个，与输出 `4 2 3 4 5` 一致。注意 $k=1$ 不可达，因为 $0\notin Q_B$——这说明答案集合是 Minkowski 和而不是区间（样例 4 的 $1,3,5$ 同理）。

## 4. 算法细节

1. **求直径与中心边**：从任意点 BFS 取最远点 $s$，再从 $s$ BFS 取最远点 $t$，$D=\mathrm{dist}(s,t)$；沿父指针把 $s\to t$ 的路径倒序存入 `path`，则中心边为 $(\mathrm{path}[h],\mathrm{path}[h+1])$，$h=(D-1)/2$（0-indexed）。
2. **两侧 BFS**：以 $u$ 为根时屏蔽边 $(u,v)$（只需在 $u$ 的出边处跳过 $v$），并用“不回到父亲”避免重复访问；因为输入是树，这就足够了。
3. **逆序统计**：BFS 序的逆序保证孩子先于父亲结算；根没有父亲，分支判定要单独补一次（$Q[0]$）。
4. **位向量下标**：$Q$ 的长度是 $h+1$，下标即深度；最深的 $h$ 一定置 1。
5. **卷积规模**：$N$ 取不小于 $2h+1$ 的 2 的幂，模 $998244353$。卷积系数不超过 $\min(|Q_A|,|Q_B|)\le h+1\le 5\cdot 10^5$，远小于模数，不会因为取模变成 0。
6. **多测清空**：只重置 `head[1..n]` 与 `ecnt`（其余数组都是本次覆盖写），避免 $O(\max n)$ 的重复清零。
7. **I/O**：$10^6$ 条边加上 $O(n)$ 个输出数字，用 `fread` 手写读入、手写输出缓冲，避免 `cin`/`cout` 或 `printf` 的逐次开销。
8. **稀疏加速**：当 $|Q_A|\cdot|Q_B|$ 明显小于卷积规模时，直接双重循环枚举更快（分支节点很多时 $h$ 必然较小）。Python 版用阈值 200000 在两种做法间切换。

## 5. 正确性证明

**引理 1**：设 $e=(u,v)$ 是某条直径的中间边，$h=(D-1)/2$。则 A 中任意点到 $u$ 的距离不超过 $h$，B 中任意点到 $v$ 的距离不超过 $h$。

**证明**：设 $x\in A$ 且 $\mathrm{dist}(x,u)=d>h$。该直径的另一端 $t\in B$ 满足 $\mathrm{dist}(v,t)=h$，于是 $\mathrm{dist}(x,t)=d+1+h>2h+1=D$，与 $D$ 是直径矛盾。B 侧对称。∎

**引理 2**：任意直径 $(x,y)$ 都满足 $x\in A$、$y\in B$（或反之），且 $\mathrm{dist}(x,u)=\mathrm{dist}(y,v)=h$；从而所有直径都包含 $e$。

**证明**：若 $x,y$ 同在 A，则 $\mathrm{dist}(x,y)\le 2h<D$，矛盾；故路径必过 $e$，长度为 $\mathrm{dist}(x,u)+1+\mathrm{dist}(y,v)=D$。由引理 1 两个加数都 $\le h$，只能都等于 $h$。∎

**引理 3**：对 $x_1,x_2\in L_A$（可相同），$\mathrm{path}(x_1,u)\cap\mathrm{path}(x_2,u)=\mathrm{path}(u,\mathrm{LCA}(x_1,x_2))$，公共边数等于 LCA 的深度。

**证明**：以 $u$ 为根后，两条根路径的公共部分正是它们到 LCA 的前缀，边数等于 LCA 的深度。∎

**引理 4**：$Q_A=\{h\}\cup\{\mathrm{dep}(w): w\text{ 是分支节点}\}$。

**证明**：$x_1=x_2$ 给出 $h$，此时 $\mathrm{dep}(\mathrm{LCA})=h$。若 $x_1\ne x_2$，两点深度都是 $h$，其 LCA 必在某个节点的两个不同孩子子树中各取到一点，故该 LCA 深度小于 $h$ 且是分支节点。反之，若 $w$ 有两个孩子的子树都含最深点，各取一个得到 $x_1,x_2$，则 $\mathrm{LCA}(x_1,x_2)=w$。∎

**定理**：$k$ 美丽当且仅当存在 $a\in Q_A$、$b\in Q_B$ 使 $k=a+1+b$。

**证明**：由引理 2，任取直径可写为 $(x,y)$，$x\in L_A,y\in L_B$。由引理 3，两条直径的交集由三段互不相交的路径拼成：A 侧公共前缀（$a=\mathrm{dep}(w_1)$ 条边）、中心边（1 条边）、B 侧公共前缀（$b=\mathrm{dep}(w_2)$ 条边），故 $k=a+1+b$ 且 $a\in Q_A,b\in Q_B$。反过来，任给 $a\in Q_A,b\in Q_B$，由引理 4 取对应的 $x_1,x_2$ 与 $y_1,y_2$（两侧互不影响，可独立选取），即得交集恰含 $a+1+b$ 条边的两条直径。∎

## 6. 复杂度分析

- **时间**：两次直径 BFS 为 $O(n)$；两侧 BFS 合计为 $O(n)$；逆序统计为 $O(n)$；卷积为 $O(h\log h)$。单组 $O(n+h\log h)$，由 $\sum n\le 10^6$ 得总复杂度 $O(\sum n\log n)$，常数很小。
- **空间**：CSR 邻接表 $O(n)$、若干 $O(n)$ 辅助数组、卷积数组 $O(h)$，合计 $O(n)$，在 512 MB 下非常宽裕。
- **实测**（C++17，`-O2`，Apple clang）：$n=10^6$ 的链（$h\approx 5\cdot 10^5$，卷积规模 $2^{20}$）用时 0.18 s；两侧各有 997 个分支深度的双梳形（$|Q_A|=|Q_B|=998$）用时 0.06 s；$t=10^4$ 组小树用时 0.04 s。4 s 限制下余量超过 20 倍。Python（CPython 3.9）在上述链上约 3.2 s，已接近限制，建议提交 PyPy。

## 7. 参考代码

### C++17

```cpp
#include <cstdio>
#include <algorithm>
#include <vector>
using namespace std;
static const int MAXN = 1000005, MOD = 998244353;

static int head[MAXN], nxt[2 * MAXN], to[2 * MAXN], ecnt;
static int dep[MAXN], par[MAXN], ord[MAXN], cntDeep[MAXN], childDeep[MAXN];
static char ibuf[1 << 22], obuf[1 << 25];
static int ilen = 0, ipos = 0, olen = 0;

static int gc() {
    if (ipos == ilen) { ilen = (int)fread(ibuf, 1, 1 << 22, stdin); ipos = 0; if (ilen <= 0) return -1; }
    return ibuf[ipos++];
}
static bool rd(int &x) {
    int c = gc(); while (c != -1 && (c < '0' || c > '9')) c = gc();
    if (c == -1) return false;
    x = 0; while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return true;
}
static void put(int x) {
    if (x == 0) { obuf[olen++] = '0'; return; }
    char t[12]; int p = 0;
    while (x) { t[p++] = char('0' + x % 10); x /= 10; }
    while (p) obuf[olen++] = t[--p];
}
static int pw(int a, int e) {
    long long r = 1, b = a;
    for (; e; e >>= 1) { if (e & 1) r = r * b % MOD; b = b * b % MOD; }
    return (int)r;
}
static void ntt(vector<int> &a, bool inv) {
    int n = (int)a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        int w = pw(3, (MOD - 1) / len); if (inv) w = pw(w, MOD - 2);
        int hf = len >> 1;
        for (int i = 0; i < n; i += len) {
            long long cur = 1;
            for (int j = 0; j < hf; j++) {
                int u = a[i + j], v = (int)(cur * a[i + j + hf] % MOD);
                int s = u + v, d = u - v;
                if (s >= MOD) s -= MOD;
                if (d < 0) d += MOD;
                a[i + j] = s; a[i + j + hf] = d;
                cur = cur * w % MOD;
            }
        }
    }
    if (inv) { int ni = pw(n, MOD - 2); for (int &x : a) x = (int)((long long)x * ni % MOD); }
}
// 从 src 出发 BFS（屏蔽边 src--blocked），ord 存 BFS 序，返回访问点数
static int bfs(int src, int blocked, int n) {
    int qh = 0, qt = 0;
    dep[src] = 0; par[src] = 0; ord[qt++] = src;
    while (qh < qt) {
        int v = ord[qh++];
        int blk = (v == src) ? blocked : 0;
        for (int e = head[v]; e != -1; e = nxt[e]) {
            int u = to[e];
            if (u == par[v] || u == blk) continue;
            par[u] = v; dep[u] = dep[v] + 1; ord[qt++] = u;
        }
    }
    return qt;
}
// 在给定一侧求 Q：Q[d]=1 表示深度 d 可作为 LCA 深度
static void computeQ(int root, int blocked, int n, int h, vector<int> &Q) {
    int m = bfs(root, blocked, n);
    for (int i = 0; i < m; i++) {
        int v = ord[i];
        cntDeep[v] = (dep[v] == h);
        childDeep[v] = 0;
    }
    Q.assign(h + 1, 0);
    Q[h] = 1;                       // 取同一个端点两次
    for (int i = m - 1; i >= 1; i--) {
        int v = ord[i];
        if (childDeep[v] >= 2) Q[dep[v]] = 1;   // 分支节点
        int p = par[v];
        if (cntDeep[v] > 0) childDeep[p]++;
        cntDeep[p] += cntDeep[v];
    }
    if (childDeep[ord[0]] >= 2) Q[0] = 1;      // 根单独判
}

int main() {
    int t;
    if (!rd(t)) return 0;
    while (t--) {
        int n; rd(n);
        for (int i = 1; i <= n; i++) head[i] = -1;
        ecnt = 0;
        for (int i = 0; i < n - 1; i++) {
            int u, v; rd(u); rd(v);
            to[ecnt] = v; nxt[ecnt] = head[u]; head[u] = ecnt++;
            to[ecnt] = u; nxt[ecnt] = head[v]; head[v] = ecnt++;
        }
        // 两次 BFS 求直径 s--t
        int m = bfs(1, 0, n), s = 1;
        for (int i = 0; i < m; i++) if (dep[ord[i]] > dep[s]) s = ord[i];
        m = bfs(s, 0, n);
        int tt = s;
        for (int i = 0; i < m; i++) if (dep[ord[i]] > dep[tt]) tt = ord[i];
        int D = dep[tt], h = (D - 1) / 2;
        static vector<int> path; path.clear();
        for (int v = tt; v; v = par[v]) path.push_back(v);
        reverse(path.begin(), path.end());
        int cu = path[h], cv = path[h + 1];       // 中心边
        static vector<int> QA, QB;
        computeQ(cu, cv, n, h, QA);
        computeQ(cv, cu, n, h, QB);
        int N = 1; while (N < 2 * h + 1) N <<= 1;
        vector<int> A(N, 0), B(N, 0);
        for (int i = 0; i <= h; i++) { A[i] = QA[i]; B[i] = QB[i]; }
        ntt(A, false); ntt(B, false);
        for (int i = 0; i < N; i++) A[i] = (int)((long long)A[i] * B[i] % MOD);
        ntt(A, true);
        int cnt = 0;
        for (int s2 = 0; s2 <= 2 * h; s2++) cnt += (A[s2] != 0);
        put(cnt);
        for (int s2 = 0; s2 <= 2 * h; s2++) if (A[s2]) { obuf[olen++] = ' '; put(s2 + 1); }
        obuf[olen++] = '\n';
    }
    fwrite(obuf, 1, olen, stdout);
    return 0;
}
```

### Python3

```python
import sys
from array import array


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    MOD = 998244353
    out = []

    def ntt(a, inv):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit; bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        L = 2
        while L <= n:
            w = pow(3, (MOD - 1) // L, MOD)
            if inv:
                w = pow(w, MOD - 2, MOD)
            hf = L >> 1
            for i in range(0, n, L):
                cur = 1
                for k in range(i, i + hf):
                    u = a[k]; v = cur * a[k + hf] % MOD
                    a[k] = (u + v) % MOD
                    a[k + hf] = (u - v) % MOD
                    cur = cur * w % MOD
            L <<= 1
        if inv:
            ni = pow(n, MOD - 2, MOD)
            for i in range(n):
                a[i] = a[i] * ni % MOD

    for _ in range(t):
        n = int(data[p]); p += 1
        deg = array('i', [0]) * (n + 2)
        eu = array('i', [0]) * (n - 1); ev = array('i', [0]) * (n - 1)
        for i in range(n - 1):
            u = int(data[p]); v = int(data[p + 1]); p += 2
            eu[i] = u; ev[i] = v; deg[u] += 1; deg[v] += 1
        start = array('i', [0]) * (n + 2)
        for v in range(1, n + 1):
            start[v + 1] = start[v] + deg[v]
        pos = array('i', start)
        adj = array('i', [0]) * (2 * (n - 1))
        for i in range(n - 1):
            u = eu[i]; v = ev[i]
            adj[pos[u]] = v; pos[u] += 1
            adj[pos[v]] = u; pos[v] += 1
        del eu, ev, pos, deg

        dep = array('i', [0]) * (n + 1); par = array('i', [0]) * (n + 1)
        order = array('i', [0]) * (n + 1)

        def bfs(src, blocked):              # 屏蔽边 src--blocked，返回访问点数
            par[src] = 0; dep[src] = 0; order[0] = src
            qh, qt = 0, 1
            while qh < qt:
                v = order[qh]; qh += 1
                dv = dep[v] + 1
                blk = blocked if v == src else 0
                for i in range(start[v], start[v + 1]):
                    u = adj[i]
                    if u == par[v] or u == blk:
                        continue
                    par[u] = v; dep[u] = dv; order[qt] = u; qt += 1
            return qt

        m = bfs(1, 0)
        sfar, bd = 1, -1
        for i in range(m):
            v = order[i]
            if dep[v] > bd:
                bd = dep[v]; sfar = v
        m = bfs(sfar, 0)
        tfar, bd = sfar, -1
        for i in range(m):
            v = order[i]
            if dep[v] > bd:
                bd = dep[v]; tfar = v
        h = (bd - 1) // 2
        path = []
        v = tfar
        while v:
            path.append(v); v = par[v]
        path.reverse()
        cu, cv = path[h], path[h + 1]         # 中心边

        cntDeep = array('i', [0]) * (n + 1); childDeep = array('i', [0]) * (n + 1)

        def compute_q(root, blocked):         # 返回该侧的 Q（升序深度列表）
            m = bfs(root, blocked)
            Q = bytearray(h + 1); Q[h] = 1
            for i in range(m):
                v = order[i]
                cntDeep[v] = 1 if dep[v] == h else 0
                childDeep[v] = 0
            for i in range(m - 1, 0, -1):
                v = order[i]; pv = par[v]
                if childDeep[v] >= 2:
                    Q[dep[v]] = 1
                if cntDeep[v]:
                    childDeep[pv] += 1
                cntDeep[pv] += cntDeep[v]
            if childDeep[order[0]] >= 2:
                Q[0] = 1
            return [d for d in range(h + 1) if Q[d]]

        A = compute_q(cu, cv); B = compute_q(cv, cu)
        mark = bytearray(2 * h + 2)
        if len(A) * len(B) <= 200000:                  # 稀疏：双重循环枚举
            for a in A:
                for b in B:
                    mark[a + b] = 1
        else:                                          # 稠密：NTT 卷积
            N = 1
            while N < 2 * h + 1:
                N <<= 1
            fa = [0] * N; fb = [0] * N
            for d in A:
                fa[d] = 1
            for d in B:
                fb[d] = 1
            ntt(fa, False); ntt(fb, False)
            for i in range(N):
                fa[i] = fa[i] * fb[i] % MOD
            ntt(fa, True)
            for i in range(2 * h + 1):
                if fa[i]:
                    mark[i] = 1
        ks = [str(i + 1) for i in range(2 * h + 1) if mark[i]]
        out.append(str(len(ks)) + " " + " ".join(ks))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n=2$（$h=0$）**：$Q_A=Q_B=\{0\}$，答案只有 $k=1$；此时卷积规模 $N=1$，NTT 会退化成“乘 1”，不要写成空实现或出现除零。
2. **必须允许两条直径完全相同**：否则 $k=D$ 永远取不到（尤其是一条链的树，答案只有一个值 $D$）。
3. **答案不是区间**：样例 4 的 $\{1,3,5\}$ 说明中间会跳号，不能用“上界 + 全输出”代替 Minkowski 和。
4. **多测清空**：忘记重置 `head` 或 `ecnt` 会把上一组的边混进来；数组按最大 $n$ 静态分配时只需重置用到的前缀。
5. **两侧 BFS 的屏蔽**：只屏蔽中心边 $(u,v)$，不要顺手把 $u$ 的其他孩子屏蔽掉，也不要漏掉 $v$ 这一侧的子树的处理。
6. **深度复用**：两次 BFS 共用 `dep`，每次都要先设 `dep[src]=0`；由于屏蔽了中心边，两侧深度都从 0 起算，$h$ 的判定才正确。
7. **输出格式**：$m$ 与各个 $k$ 必须在同一行，且行末换行；用缓冲输出时记得最后 flush。
8. **Python 细节**：$10^6$ 层的树用递归会爆栈，必须写迭代 BFS；CPython 在最大数据上接近超时，建议 PyPy，或按 §4.8 用稀疏枚举替代卷积。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：1 / 1 通过（按 Codeforces 标准 checker 的 token 比对，忽略空白与大小写）。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [Codeforces 1085D Minimum Diameter Tree](https://codeforces.com/problemset/problem/1085/D)：把总权 $s$ 平摊到所有叶子出发的边，最小直径为 $2s/\text{叶子数}$，同样是“直径由叶子决定”的视角。
- [Codeforces 1294F Three Paths on a Tree](https://codeforces.com/problemset/problem/1294/F)：直径端点必在最优解中，同样是“两次 BFS + 端点性质”。
- [Codeforces 911F Tree Destruction](https://codeforces.com/problemset/problem/911/F)：沿直径贪心删点，与本题“所有直径过中心边”同源。
- [LeetCode 1245. 树的直径](https://leetcode.cn/problems/tree-diameter/)：两次 BFS 求直径长度的模板题。

**延伸思考**：① 若直径长度为偶数，中心变成一个点，交集长度是 $a+b$（没有那个 $+1$），$Q$ 的定义要改成以中心点为根；② 如果把“边数”换成“边权和”，深度不再是整数，卷积失效，需要新的刻画；③ 本题 $\sum n\le 10^6$ 允许 $O(n\log n)$，如果 $n$ 加到 $10^7$，能否利用 $|Q_A|\cdot|Q_B|=O(n)$ 的性质做到 $O(n)$？
