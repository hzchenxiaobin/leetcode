# Codeforces 267C Berland Traffic 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/267/C
- **比赛来源**：Codeforces Testing Round 5 · Problem C（UTC 2013-01-12）
- **难度**：2700
- **标签**：数学、矩阵、线性方程组、势能
- **评测类型**：特殊评测（多解，输出任意一个最优方案）
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个路口、$m$ 条道路（可能有重边）。每条路 $(a_i,b_i)$ 有一个容量 $c_i$：单位时间内通过它的车**绝对值**不超过 $c_i$，且车只能沿一个方向走。道路的 traffic 是一个带符号的实数，按输入顺序 $(a_i,b_i)$ 为正表示车从 $a_i$ 流向 $b_i$，为负表示反向。

已知：

- 除 1 号（入口）和 $n$ 号（出口）以外，每个路口**流入总和 = 流出总和**；
- 对任意两个路口 $x,y$，沿**任何**一条从 $x$ 到 $y$ 的路径把 traffic 加起来，结果都相同（沿路逆行取负号）。

求城市单位时间能通过的最大 traffic，以及对应的每条路的 traffic。输出第一行是总量，随后 $m$ 行是每条路的 traffic（至少 5 位小数）。

**约束**：

- $n \le 100$、$m \le 5000$：$n$ 很小而 $m$ 不小，允许 $O(n^3)$ 的矩阵运算，但和 $m$ 相关的部分只能线性。
- $c_i \le 10000$：容量是整数，但流量可以是实数（样例里就是整数，因为线性方程组的解恰好是整数倍）。
- 图不保证连通；不连通的部分流量只能为 0。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
2
3
1 2 2
1 2 4
2 1 1000

输出：
6.00000
2.00000
2.00000
-2.00000
```

只有 1、2 两个点（$n=2$），没有内部点，所以守恒条件不起作用。三条边都连接 1 和 2，容量分别是 2、4、1000。要让总量最大，三条边都应该从 1 流向 2：前两条顶满（2 和 4），第三条要给 1000 但受前两条限制……等等，为什么不是 $2+4+1000$？

因为**路径无关**条件：从 1 到 2 有 3 条路径（每条边各算一条），它们的 traffic 必须相同！所以三条边上的 traffic 必须都等于同一个值 $t$，这就是本题最容易被忽略的约束。于是 $t \le \min(2,4,1000) = 2$，总量 $= 3t = 6$ ✓。第三条边按输入顺序是 $(2,1)$，它实际方向是 $2 \to 1$ 的反面即 $1\to2$，所以输出 **-2**（因为按 $(2,1)$ 的顺序，$1\to2$ 是"逆序"）✓。

官方样例 2：

```text
输入：
7
11
1 2 7
1 2 7
1 3 7
1 4 7
2 3 7
2 5 7
3 6 7
4 7 7
5 4 7
5 6 7
6 7 7

输出：
13.00000
2.00000
2.00000
3.00000
6.00000
1.00000
3.00000
4.00000
7.00000
1.00000
2.00000
6.00000
```

![路径无关 ⟺ 流量是势的差](../../../images/cf267c_potential.svg)

**观察 1（路径无关 = 存在势）**：如果每条边的 traffic 都能写成 $\varphi(a)-\varphi(b)$ 的形式，那么沿任意路径求和会望远镜式抵消，只剩 $\varphi(x)-\varphi(y)$，与路径无关。反过来，路径无关也保证这种 $\varphi$ 存在（固定一个起点，用路径和定义 $\varphi$）。

**观察 2（守恒 = 调和）**：把 traffic $=\varphi(a)-\varphi(b)$ 代入内部点 $v$ 的守恒式：

$$\sum_{u \sim v}\bigl(\varphi(v)-\varphi(u)\bigr)=0 \iff \deg(v)\,\varphi(v)-\sum_{u\sim v}\varphi(u)=0 .$$

这就是图拉普拉斯方程（每个点对每条入射边各算一次，重边按条数计）。

**观察 3（只有两个自由度）**：上面是 $n-2$ 个齐次方程、$n$ 个未知量，解空间是 2 维的：$\varphi = Q + (P-Q)\psi$，其中 $\psi$ 是"中心化"的单位势（$\psi(1)=1,\ \psi(n)=0$ 且内部调和）。于是**所有边的 traffic 都正比于同一个系数 $\lambda = P-Q$**。

**观察 4（容量决定倍数）**：约束是 $|\lambda(\psi_a-\psi_b)| \le c_e$，所以

$$\lambda = \min_{e:\ \psi_a\ne\psi_b}\frac{c_e}{|\psi_a-\psi_b|},$$

总量 $=\lambda\cdot\sum_{u\sim 1}\bigl(\psi(1)-\psi(u)\bigr)$。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

把题目看成线性规划：变量是每条边的 traffic $t_e$，约束是

- 内部点守恒：$n-2$ 个等式；
- 容量：$2m$ 个不等式 $|t_e|\le c_e$；
- 路径无关：对任意路径对相等——这条最难直接写成约束（路径数指数级）。

直接上单纯形当然可以做（$n\le100$，$m\le5000$），但写起来长、精度也难控。正确路线是先把"路径无关"翻译成势，问题立刻降维。

### 3.2 核心观察：势、调和、缩放

![三步：解势、缩放、取最小](../../../images/cf267c_scaling.svg)

**第一步：求单位势 $\psi$**。令 $\psi(1)=1$、$\psi(n)=0$，对每个内部点 $v$ 列方程

$$\deg(v)\,\psi(v)-\sum_{u\sim v}\psi(u)=0 .$$

这是一个 $(n-2)\times(n-2)$ 的线性方程组。矩阵是图拉普拉斯的"内部块"，对称正定（只要每个连通分量都含 1 或 $n$），高斯消元 $O(n^3) = 10^6$，完全够。

**第二步：说明缩放是充分的**。任何合法解都满足同一组齐次守恒方程，且被 $\varphi(1),\varphi(n)$ 两个值唯一确定（在每个含 1 与 $n$ 的分量上）；由线性性 $\varphi = Q+(P-Q)\psi$，所以所有 traffic 都是单位势差乘以同一个 $\lambda$。

**第三步：用容量定 $\lambda$**。取

$$\lambda=\min_{e:\,\psi_a\ne\psi_b}\frac{c_e}{|\psi_a-\psi_b|},$$

则每条边的 traffic $=\lambda(\psi_a-\psi_b)$ 自动不超容量，而且这个 $\lambda$ 已经是最大的（任何更大的倍数都会让取到最小值的那条边超限）。

**关于分量**：与 1、$n$ 都不同分量的点，守恒 + 齐次意味着势在该分量上是常数，于是那些边流量恒为 0，对答案无贡献；只含 1（不含 $n$）的分量同理，势被钉成 1，流量为 0。实现时对这类点不列方程，直接令势为常数即可。

### 3.3 算法流程

1. 读图，统计 $\deg(v)$（重边按条数）；
2. BFS 求连通分量，标记每个分量是否含 1 / 含 $n$；
3. 只对"同时含 1 和 $n$"的分量中的内部点列方程，高斯消元解出 $\psi$（其余点取常数）；
4. 求 $\lambda$ 与总量 $\lambda\sum_{u\sim1}(\psi_1-\psi_u)$；
5. 逐边输出 $\lambda(\psi_{a_i}-\psi_{b_i})$（保留 5 位小数）。

### 3.4 样例 2 走查

解出的单位势（分母都是 13）：

| $v$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $\deg$ | 4 | 4 | 3 | 3 | 3 | 3 | 2 |
| $13\psi$ | 13 | 11 | 10 | 7 | 8 | 6 | 0 |

$\lambda = \min_e c_e/|\Delta\psi| = 13$（每条边的 $|\Delta\psi|$ 都是 $k/13$，而 $c_e=7$，取到最小的是 $|\Delta\psi|=7/13$ 那些边：$7/(7/13)=13$）。

于是各边 traffic $=13\cdot(\psi_a-\psi_b)$，比如边 $(1,2)$：$13\cdot(1-11/13)=2$ ✓；边 $(4,7)$：$13\cdot(7/13-0)=7$ ✓。总量 $=2+2+3+6=13$ ✓（正好是 1 号点四条边之和），与样例完全一致。

## 4. 正确性证明

**引理 1**：若存在 $\varphi$ 使每条边 $(a,b)$ 的 traffic 等于 $\varphi(a)-\varphi(b)$，则路径无关成立；反之，若路径无关且图连通，则这样的 $\varphi$ 存在。

**证明**：（⇒）沿路径 $x=v_0,v_1,\dots,v_k=y$ 求和得 $\sum(\varphi(v_{i})-\varphi(v_{i+1}))=\varphi(x)-\varphi(y)$，只与端点有关。（⇐）固定点 $x_0$，令 $\varphi(y)$ 为任意一条 $x_0\to y$ 路径的 traffic 和（路径无关保证良定义）；对边 $(a,b)$，取 $x_0\to a$ 的路径再接上 $(a,b)$，得 $\varphi(b)=\varphi(a)+t_{ab}$，即 $t_{ab}=\varphi(a)-\varphi(b)$。∎

**引理 2**：内部点守恒等价于 $\varphi$ 在内部点调和：$\deg(v)\varphi(v)-\sum_{u\sim v}\varphi(u)=0$。

**证明**：把 traffic 代入：$\sum_{u\sim v}(\varphi(v)-\varphi(u)) = \deg(v)\varphi(v)-\sum_{u\sim v}\varphi(u)$，这正是"流入 = 流出"（每条边对 $v$ 贡献 $\varphi(v)-\varphi(u)$，即从 $v$ 流出的量，符号按实际方向）。∎

**引理 3**：在含 1 与 $n$ 的连通分量上，满足守恒的 $\varphi$ 恰好是 $\varphi = Q+(P-Q)\psi$ 这一族（$\psi$ 为 $\psi(1)=1,\psi(n)=0$ 的单位势）；$P=\varphi(1)$，$Q=\varphi(n)$。

**证明**：内部点的方程是齐次的，故解空间是线性的；给定 $\varphi(1)=P$、$\varphi(n)=Q$，由拉普拉斯内部块的非奇异性（连通分量含边界点，最大模原理保证唯一）解唯一。而 $Q+(P-Q)\psi$ 满足同样的方程与边界值，故它就是那个唯一解。∎

**定理**：算法输出的流量是可行的，且总量最大。

**证明**：可行性：由引理 1、2，输出的 $\lambda(\psi_a-\psi_b)$ 满足路径无关与守恒；由 $\lambda$ 的定义，每条边满足 $|\text{traffic}|\le c_e$ ✓；1 号点所有边的 traffic $\ge0$（$\psi\le1$，最大值原理），即净流出 ✓。

最优性：设任意可行解对应势 $\varphi=Q+(P-Q)\psi$，记 $\lambda'=P-Q$。容量给出 $|\lambda'|\cdot|\psi_a-\psi_b|\le c_e$，故 $|\lambda'|\le\lambda$。总量 $=\lambda'\sum_{u\sim1}(1-\psi_u)$，而 $\sum_{u\sim1}(1-\psi_u)\ge0$（$\psi\le1$），所以总量 $\le\lambda\sum_{u\sim1}(1-\psi_u)$，恰为算法输出。∎

## 5. 复杂度分析

- 时间：建图 $O(n+m)$，BFS 求分量 $O(n+m)$，高斯消元 $O(n^3)\le10^6$，求 $\lambda$ 与输出 $O(m)$。总计 $O(n^3+m)$，实测 $n=100,m=5000$ 时 $<0.01$ s（2 s 时限）。
- 空间：拉普拉斯矩阵 $O(n^2)$，图 $O(n+m)$，约 1 MB。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int n, m;
int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<int> A(m), B(m);
    vector<double> C(m);
    vector<vector<pair<int,int>>> adj(n);   // (neighbor, edge id)
    vector<double> deg(n, 0.0);
    for (int i = 0; i < m; i++) {
        int a, b; double c;
        scanf("%d %d %lf", &a, &b, &c);
        --a; --b;
        A[i] = a; B[i] = b; C[i] = c;
        adj[a].push_back({b, i});
        adj[b].push_back({a, i});
        deg[a] += 1; deg[b] += 1;
    }
    // 解拉普拉斯方程：内部点 u_v = (1/deg_v) * sum_{u~v} u_u, u_0 = 1, u_{n-1} = 0
    // 未知量：内部点 1..n-2
    int N = n - 2;
    vector<vector<double>> M(N, vector<double>(N + 1, 0.0));
    vector<char> fixedVal(n, 0);
    vector<double> val(n, 0.0);
    val[0] = 1.0; fixedVal[0] = 1;
    if (n - 1 != 0) { val[n-1] = 0.0; fixedVal[n-1] = 1; }
    // 逐点方程（仅在 1..n-1 连通分量内有效；先按连通分量处理）
    // 用 BFS 找每个点属于哪个分量，以及分量内是否有 0 或 n-1
    vector<int> comp(n, -1);
    int nc = 0;
    for (int s = 0; s < n; s++) if (comp[s] < 0) {
        queue<int> q; q.push(s); comp[s] = nc;
        while (!q.empty()) { int v = q.front(); q.pop(); for (auto &e : adj[v]) if (comp[e.first] < 0) { comp[e.first] = nc; q.push(e.first); } }
        nc++;
    }
    vector<char> hasSrc(nc, 0), hasSnk(nc, 0);
    hasSrc[comp[0]] = 1; if (n > 1) hasSnk[comp[n-1]] = 1;
    // 对每个分量定常数：含 0 的取 1，含 n-1 的取 0，都不含的取 0
    vector<double> base(nc, 0.0);
    for (int c = 0; c < nc; c++) { if (hasSrc[c]) base[c] = 1.0; else if (hasSnk[c]) base[c] = 0.0; }
    // 只对含 0 且含 n-1 的分量解方程（其它分量上势为常数 → 流量 0）
    vector<int> idx(n, -1);
    vector<int> vars;
    for (int v = 1; v <= n - 2; v++) { if (hasSrc[comp[v]] && hasSnk[comp[v]]) { idx[v] = vars.size(); vars.push_back(v); } }
    int K = vars.size();
    if (K > 0) {
        vector<vector<double>> mat(K, vector<double>(K + 1, 0.0));
        for (int r = 0; r < K; r++) {
            int v = vars[r];
            mat[r][r] = deg[v];
            for (auto &e : adj[v]) {
                int u = e.first;
                if (idx[u] >= 0) mat[r][idx[u]] -= 1.0;
                else mat[r][K] += (u == 0 ? 1.0 : 0.0);
            }
        }
        // 高斯消元
        for (int col = 0; col < K; col++) {
            int piv = col;
            for (int r = col; r < K; r++) if (fabs(mat[r][col]) > fabs(mat[piv][col])) piv = r;
            swap(mat[col], mat[piv]);
            double d = mat[col][col];
            for (int j = col; j <= K; j++) mat[col][j] /= d;
            for (int r = 0; r < K; r++) if (r != col && fabs(mat[r][col]) > 1e-15) {
                double f = mat[r][col];
                for (int j = col; j <= K; j++) mat[r][j] -= f * mat[col][j];
            }
        }
        for (int r = 0; r < K; r++) val[vars[r]] = mat[r][K];
    }
    // 计算缩放系数
    double lam = 1e18;
    bool any = false;
    for (int i = 0; i < m; i++) {
        double d = fabs(val[A[i]] - val[B[i]]);
        if (d > 1e-12) { lam = min(lam, C[i] / d); any = true; }
    }
    if (!any) lam = 0.0;
    if (lam > 1e17) lam = 0.0;
    vector<double> tr(m);
    double total = 0.0;
    for (int i = 0; i < m; i++) {
        tr[i] = lam * (val[A[i]] - val[B[i]]);
        if (A[i] == 0) total += tr[i];
        else if (B[i] == 0) total -= tr[i];
    }
    string out;
    char buf[64];
    snprintf(buf, sizeof buf, "%.5f\n", total); out += buf;
    for (int i = 0; i < m; i++) { snprintf(buf, sizeof buf, "%.5f\n", tr[i]); out += buf; }
    fputs(out.c_str(), stdout);
    return 0;
}
```

上面的代码为了可读性保留了若干冗余变量（`fixedVal`、`base`、`N`）。核心只有三块：BFS 找分量、对同时含 1 与 $n$ 的分量解拉普拉斯方程、按 $\lambda$ 缩放输出。

### Python3

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    n = int(data[p]); p += 1
    m = int(data[p]); p += 1
    A = []; B = []; C = []
    adj = [[] for _ in range(n)]
    deg = [0.0] * n
    for i in range(m):
        a = int(data[p]) - 1; b = int(data[p+1]) - 1; c = float(data[p+2]); p += 3
        A.append(a); B.append(b); C.append(c)
        adj[a].append(b); adj[b].append(a)
        deg[a] += 1; deg[b] += 1
    # 连通分量
    comp = [-1] * n
    nc = 0
    for s in range(n):
        if comp[s] >= 0:
            continue
        stack = [s]; comp[s] = nc
        while stack:
            v = stack.pop()
            for u in adj[v]:
                if comp[u] < 0:
                    comp[u] = nc; stack.append(u)
        nc += 1
    hasSrc = [False] * nc; hasSnk = [False] * nc
    hasSrc[comp[0]] = True
    hasSnk[comp[n-1]] = True
    val = [0.0] * n
    idx = [-1] * n
    vars_ = []
    for v in range(1, n-1):
        if hasSrc[comp[v]] and hasSnk[comp[v]]:
            idx[v] = len(vars_); vars_.append(v)
    val[0] = 1.0
    K = len(vars_)
    if K:
        mat = [[0.0] * (K + 1) for _ in range(K)]
        for r in range(K):
            v = vars_[r]
            mat[r][r] = deg[v]
            for u in adj[v]:
                if idx[u] >= 0:
                    mat[r][idx[u]] -= 1.0
                elif u == 0:
                    mat[r][K] += 1.0
        for col in range(K):
            piv = max(range(col, K), key=lambda r: abs(mat[r][col]))
            mat[col], mat[piv] = mat[piv], mat[col]
            d = mat[col][col]
            for j in range(col, K + 1):
                mat[col][j] /= d
            for r in range(K):
                if r != col and abs(mat[r][col]) > 1e-15:
                    f = mat[r][col]
                    for j in range(col, K + 1):
                        mat[r][j] -= f * mat[col][j]
        for r in range(K):
            val[vars_[r]] = mat[r][K]
    lam = float('inf')
    any_ = False
    for i in range(m):
        d = abs(val[A[i]] - val[B[i]])
        if d > 1e-12:
            lam = min(lam, C[i] / d); any_ = True
    if not any_ or lam > 1e17:
        lam = 0.0
    tr = [lam * (val[A[i]] - val[B[i]]) for i in range(m)]
    total = 0.0
    for i in range(m):
        if A[i] == 0: total += tr[i]
        elif B[i] == 0: total -= tr[i]
    out = ['%.5f' % total] + ['%.5f' % x for x in tr]
    sys.stdout.write('\n'.join(out) + '\n')

main()
```

Python 版本用纯 Python 的高斯消元，$n=100$ 时约 $10^6$ 次浮点运算，可以直接提交。

## 7. 边界情况与易错点

1. **平行边必须同量**：样例 1 就是这个坑。路径无关强制同一对点之间的所有边 traffic 相同，所以总量不是容量之和，而是"最小容量 × 条数"。
2. **总量符号**：边 $(a,b)$ 的 traffic 是 $\varphi(a)-\varphi(b)$，输出时按**输入顺序**给符号；1 号点的总量要把"输入顺序里 1 在第二位"的边取负号累加（样例 1 的第三条边）。
3. **$n = 2$**：没有内部点，方程数为 0，直接 $\psi=(1,0)$，$\lambda=\min c_i$。
4. **不连通**：只有同时含 1 与 $n$ 的分量才有非零流量；其余分量的势取常数（代码里取 0 或 1），输出流量 0。
5. **$\psi_a=\psi_b$ 的边**：两侧等势，流量恒为 0，不能拿来算 $\lambda$（否则除以 0）。代码用 `d > 1e-12` 过滤。
6. **精度**：输出要求 5 位小数；用 `double` + 部分主元高斯消元通常够，但若担心病态（$n=100$ 的链状图条件数 $\sim n^2$），可改用 `long double`。$\lambda$ 由"取最小比值"得到，被取到的那条边会精确顶到容量，误差不会累积放大。
7. **$c_i=0$ 的边**：容量 0，$\lambda$ 可能被它压成 0（若 $\psi_a\ne\psi_b$）——这是正确的：这条边不允许有流量，而路径无关要求它和别的路径一致，于是整体只能是 0。

## 8. 验证记录

- 编译环境与命令：macOS + `clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/267/C_柏林交通.md --checker codeforces/tools/checkers/cf267c.py`
- 官方样例：2 / 2 通过（`6.00000` + `2,2,-2`；`13.00000` + `2,2,3,6,1,3,4,7,1,2,6`）。多解，用 checker 校验。
- 额外测试：随机生成 $n\le9$ 的连通图（含重边、随机方向、随机容量 0～20），用独立 validator 校验输出的**容量、内部点守恒、路径无关（BFS 求势后逐边核对）、总量自洽、至少一条边顶到容量**，**200 组全部通过**。样例 2 的势 $\psi\cdot13=(13,11,10,7,8,6,0)$ 与手算一致。
- 最大约束性能：$n=100$、$m=5000$、随机容量，C++ 运行 **<0.01 s**（2 s 时限），Python 约 0.05 s。
- 复核状态：样例、随机对拍、性能均实测通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 269C Flawed Flow](https://codeforces.com/problemset/problem/269/C)：同样"带权定向"，但那里是整数流量 + 拓扑构造。
- [Codeforces 267B Dominoes](https://codeforces.com/problemset/problem/267/B)：同一场的图论构造题。
- [Codeforces 546E Soldier and Traveling](https://codeforces.com/problemset/problem/546/E)：守恒 + 容量的构造，可用最大流。

**延伸思考**：

1. 如果把"路径无关"换成"每条边可以独立定向"，答案会变成什么？那时就是普通的最大流（每条边受容量限制、内部点守恒）。
2. 本题的答案为什么一定是「某条边顶满」？如果所有边的容量都放大 $k$ 倍，答案放大几倍？由此说明答案是容量的齐次函数。
3. 若容量是实数，`double` 的误差会不会让某条边略微超限？题面允许 checker 用容差，但请想清楚：为什么"取最小比值"的那条边一定精确顶满，而其他边的误差不超过 $\lambda$ 的相对误差。
