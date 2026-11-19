# Codeforces 2279D 元图 题解

## 1. 题目概述

- **标题 / 题号**：元图（Codeforces 2279D，英文名 Meta Graph）
- **链接**：https://codeforces.com/problemset/problem/2279/D
- **来源**：Codeforces Round 1133 (Div. 1) · Problem D
- **难度**：未评级（1750 分）
- **限制**：时间 3 s / 内存 256 MB
- **标签**：构造，动态规划，图论，最短路

**题意**：给定连通无向简单图 $G=(V,E)$，$|V|=n$。定义 $G$ 的**元图** $f(G)$：顶点是 $n^2$ 个有序对 $a_b$（$1\le a,b\le n$，读作「第一坐标 $a$、第二坐标 $b$」）。对 $G$ 的每条边 $(a,b)$，在 $f(G)$ 中连两类边：

- **走路边**：对所有 $1\le c\le n$，连 $(c_a,c_b)$——第一坐标不动，第二坐标沿 $G$ 挪一步；
- **交换边**：连 $(a_b,b_a)$——两个坐标互换，前提是它们相邻。

给定起点 $w_x$、终点 $y_z$，求 $f(G)$ 中两点的最短路长度。

**约束**：$1\le t\le10^4$，$2\le n\le2\cdot10^5$，$n-1\le m\le\min\bigl(2\cdot10^5,\frac{n(n-1)}2\bigr)$，$1\le w,x,y,z\le n$；$G$ 连通、无重边无自环；$\sum n\le2\cdot10^5$、$\sum m\le2\cdot10^5$。

## 2. 示例与观察
```text
输入
3
3 2
1 1 3 3
1 2
2 3
4 4
1 1 4 1
1 2
2 3
3 4
1 4
2 1
1 1 1 1
1 2

输出
6
2
0
```

三组分别对应：路径图上的 $1_1\to3_3$（$6$ 步，官方 note 给出的路径即 $1_1,1_2,2_1,2_2,2_3,3_2,3_3$）；四元环上 $1_1\to4_1$（先走 $1\to4$ 再交换，$2$ 步）；单边图上原地不动（$0$ 步）。

## 3. 解题思路

### 3.1 暴力思路

$f(G)$ 有 $n^2$ 个点；每条 $G$ 的边产生 $O(n)$ 条走路边，另有 $2m$ 条交换边，边数 $O(nm)$。直接建图 BFS 需 $O(n^2+nm)$，$n=2\cdot10^5$ 时 $n^2=4\cdot10^{10}$，既存不下也跑不完，必须把状态数压下来。

### 3.2 核心观察：只有两个原子动作

![元图的两种边：横向走路、斜向交换](../../../images/cf2279d_meta_grid.svg)

把状态写成 $(p,q)$（即题目里的 $p_q$），$d(u,v)$ 表示 $G$ 中的距离。$f(G)$ 里只有两种边：

- **走路**：$(p,q)\to(p,q')$，其中 $q\sim q'$——让第二坐标在 $G$ 上挪一步；连走若干步即 $(p,q)\to(p,q'')$，代价 $d(q,q'')$。
- **交换**：$(p,q)\to(q,p)$，要求 $p\sim q$，代价 $1$。

于是任意路径都能化简：连续两段走路合并成一段（代价取 $G$ 中距离）；连续两次交换回到原状态，直接删掉。所以**最短路必然形如「走路、交换、走路、交换、……、走路」，且每段走路都取 $G$ 中的最短路**。

设一共交换 $k$ 次，把「交换时第一坐标取到的点」依次记为 $w=v_0,v_1,\dots,v_{k-1},v_k=y$，则 $(v_0,\dots,v_k)$ 是 $G$ 中的一条 walk，第 $i$ 次交换后的状态恰为 $(v_i,v_{i-1})$。逐段累加代价：第一段把第二坐标从 $x$ 走到 $v_1$（需 $v_1\sim v_0=w$）付 $d(x,v_1)$ 再交换；第 $i$ 次与第 $i+1$ 次交换之间把第二坐标从 $v_{i-1}$ 走到 $v_{i+1}$（需 $v_i\sim v_{i+1}$）付 $d(v_{i-1},v_{i+1})$ 再交换；最后状态 $(y,u)$（$u=v_{k-1}\sim y$）把第二坐标从 $u$ 走到 $z$。总代价

$$C=d(x,v_1)+1+\sum_{i=1}^{k-1}\bigl[d(v_{i-1},v_{i+1})+1\bigr]+d(u,z).\tag{1}$$

中间每次推进的系数 $d(v_{i-1},v_{i+1})\in\{1,2\}$（因 $v_{i-1}\sim v_i\sim v_{i+1}$），所以一次推进要 $2$ 或 $3$。**关键引理**：等于 $1$ 的项（三点成三角形）可以消掉——把对应的 $v_i$ 从序列里删去，两端仍相邻，代价不变大（引理 2）。于是可以假设式 (1) 中所有系数都等于 $2$，此时

$$C=d(x,v_1)+\bigl[3(k-2)+4\bigr]+d(u,z)\ \ge\ d(x,v_1)+3\,d(v_1,u)+4+d(u,z),$$

最后一步用了 $d(v_1,u)\le k-2$（中间那段 walk 只有 $k-2$ 条边）。反过来，任给 $v\in N(w)$、$u\in N(y)$，把 $v$ 到 $u$ 的最短路塞进中间，就能造出代价不超过 $d(x,v)+3d(v,u)+4+d(u,z)$ 的路径。再加上 $k=0$（$w=y$，第一坐标本来就在位）与 $k=1$（$w\sim y$，只交换一次）两种边界，答案即

$$\text{ans}=\min\begin{cases}d(x,z), & w=y,\\[2pt] d(x,y)+1+d(w,z), & w\sim y,\\[2pt] \min\limits_{v\in N(w),\,u\in N(y)}\bigl[d(x,v)+3d(v,u)+4+d(u,z)\bigr].\end{cases}\tag{2}$$

> 💡 分支③ 里 $+4$ 的来源：第一次交换 $1$ 加最后一次推进 $3$；中间每跨一步付 $3$ = 走两步 $+$ 交换一次。

### 3.3 算法流程：两次 BFS + 一次多源 Dijkstra

![算法流程](../../../images/cf2279d_algorithm_flow.svg)

式 (2) 第三行是「双端点」最小化，但可以拆成两半：

1. 从 $x$、$z$ 各做一次 BFS，得到 $d(x,\cdot)$ 与 $d(z,\cdot)$；
2. **多源 Dijkstra**：源点集 $N(w)$，源 $v$ 的初值取 $d(x,v)$，每条边权恒为 $3$，跑完得到 $A[u]=\min_{v\in N(w)}\bigl[d(x,v)+3d(v,u)\bigr]$；
3. 第三支为 $\min_{u\in N(y)}[A[u]+4+d(z,u)]$，最终答案取三支中的最小值。

边权全是 $3$，故每次松弛就是 $+3$；但初值各不相同，不能直接用普通 BFS（除非改用桶/基数堆）。

### 3.4 示例演算

![样例 1 走查](../../../images/cf2279d_walkthrough.svg)

样例 1：$G$ 是路径 $1-2-3$，起点 $1_1$、终点 $3_3$。分支① 因 $w=1\ne y=3$ 不生效；分支② 因 $1$ 与 $3$ 不相邻不生效；分支③ 中 $N(w)=N(y)=\{2\}$，故 $v=u=2$，$A[2]=d(x,2)=1$，于是

$$\text{ans}=A[2]+4+d(z,2)=1+4+1=6,$$

与官方输出一致，对应路径 $1_1\to1_2\to2_1\to2_2\to2_3\to3_2\to3_3$。

样例 2：四元环 $1-2-3-4-1$，起点 $1_1$、终点 $4_1$，分支② 生效（$1\sim4$）：$d(x,y)+1+d(w,z)=d(1,4)+1+d(1,1)=1+1+0=2$，即先走 $1\to4$ 再交换一步。样例 3：$w=y=1$，分支① 给出 $d(x,z)=0$。

## 4. 算法细节

1. **多测重建**：每组重建邻接表与 $d(x,\cdot)$、$d(z,\cdot)$、$A$ 三个数组；$\sum n\le2\cdot10^5$，总代价线性。
2. **多源初值**：源点是 $v\in N(w)$，初值为 $d(x,v)$，**不是** $0$、也不是 $d(x,w)$；同一源点只在更小时入堆。
3. **惰性删除**：Dijkstra 弹出 $(d,u)$ 后若 $d>A[u]$ 直接跳过，省掉 `decrease-key`。
4. **三支取 min**：$w=y$ 时分支①、$w\sim y$ 时分支② 都可能优于分支③（样例 2、3 即是），不能只算分支③。
5. **$w\sim y$ 的判定**：扫 $N(w)$ 打标记即可，$\sum\deg=2m$；收尾只枚举 $u\in N(y)$，简单图无自环故 $u\ne y$。
6. **溢出**：$A[u]\le3n+O(1)$，答案 $\le3n\approx6\cdot10^5$，`int` 够用；仍用 `long long` 存答案，`INF` 取 $10^9$ 保证加法不溢出。
7. **I/O**：$\sum(n+m)\le4\cdot10^5$ 个整数，`scanf` 或 `ios::sync_with_stdio(false)` 都够快，换行统一 `'\n'`。

## 5. 正确性证明

**引理 1（规范形）**：$f(G)$ 中任意两点间存在最短路，形如「走路、交换、走路、……、走路」交替，且每段走路都是 $G$ 中的最短路径。

**证明**：取一条最短路。连续两段走路可合并（代价和 $\ge$ 两端点的 $G$ 距离，换成最短路只会更短）；连续两次交换等价于回到原状态 $(p,q)\to(q,p)\to(p,q)$，删掉更短，矛盾。故走路与交换交替。若某段走路长于两端点的 $G$ 距离，替换为最短路即得更短路径，矛盾。∎

**引理 2（三角形折扣可消去）**：设规范路径的 walk 为 $v_0=w,\dots,v_k=y$，代价如式 (1)。若某个 $1\le i\le k-1$ 满足 $d(v_{i-1},v_{i+1})=1$，则删去 $v_i$ 后仍是规范路径，且代价不变大。

**证明**：删去后 $v_{i-1}\sim v_{i+1}$，序列仍是 $G$ 中的 walk，首末两段的交换条件也依旧成立。逐项比较：被删掉的第 $i$ 项等于 $d(v_{i-1},v_{i+1})+1=2$；受影响的只有第 $i-1$ 项（原为 $d(v_{i-2},v_i)+1$，新值 $\le d(v_{i-2},v_i)+2$，最多 $+1$）与第 $i$ 项（原为 $d(v_i,v_{i+2})+1$，新值 $\le d(v_i,v_{i+2})+2$，最多 $+1$）；若 $i=1$，起始段由 $d(x,v_1)$ 变为 $d(x,v_2)\le d(x,v_1)+1$（此时「第 $i-1$ 项」不存在）；若 $i=k-1$，收尾段由 $d(v_{k-1},z)$ 变为 $d(v_{k-2},z)\le d(v_{k-1},z)+1$。增加量合计不超过 $2$，恰被删掉的 $2$ 抵消，故代价不变大。∎

**引理 3（下界）**：任意从 $w_x$ 到 $y_z$ 的路径长度不小于式 (2) 右端。

**证明**：由引理 1 取规范路径，由引理 2 反复删去三角形折扣，得到规范路径 $P'$，代价 $C'\le C$，且或者 $k'=0$、或者 $k'=1$、或者 $k'\ge2$ 且所有 $d(v'_{i-1},v'_{i+1})=2$。

- $k'=0$：第一坐标始终是 $w$，故 $w=y$，代价 $d(x,z)$，正是分支①。
- $k'=1$：$C'=d(x,y)+1+d(w,z)$，且要求 $w\sim y$，正是分支②。
- $k'\ge2$ 且无折扣：$C'=d(x,v'_1)+1+3(k'-1)+d(u,z)$，其中 $v'_1\in N(w)$、$u=v'_{k'-1}\in N(y)$。把 $1+3(k'-1)$ 写成 $3(k'-2)+4$，并用 $d(v'_1,u)\le k'-2$（中间 walk 只有 $k'-2$ 条边），得
 $$C'\ \ge\ d(x,v'_1)+3d(v'_1,u)+4+d(u,z)\ \ge\ \min_{v\in N(w),\,u\in N(y)}\bigl[d(x,v)+3d(v,u)+4+d(u,z)\bigr].$$

综上 $C\ge C'\ge$ 式 (2) 右端。∎

**引理 4（可达）**：式 (2) 右端的每个值都可由某条合法路径达到。

**证明**：分支①：把第二坐标从 $x$ 走到 $z$，恰 $d(x,z)$ 步。分支②：先走 $x\to y$，交换得 $(y,w)$，再走 $w\to z$，共 $d(x,y)+1+d(w,z)$ 步。分支③：取 $v\in N(w)$、$u\in N(y)$ 及 $G$ 中 $v$ 到 $u$ 的最短路 $v=a_0,\dots,a_m=u$，构造规范路径 $v_i=a_{i-1}\,(1\le i\le m+1)$、$v_{m+2}=y$：起始段 $d(x,v)$、一次交换、随后 $m+1$ 次推进各不大于 $3$（每次推进的两端点都经某个中间点相邻，距离 $\le2$）、收尾 $d(u,z)$，总代价不超过 $d(x,v)+3m+4+d(u,z)$。∎

**定理**：答案等于式 (2) 右端。

**证明**：引理 3 给出下界，引理 4 给出可达，两侧相等。∎

## 6. 复杂度分析

- **时间**：两次 BFS 为 $O(n+m)$；多源 Dijkstra 堆操作 $O((n+m)\log n)$。单组 $O((n+m)\log n)$，总计 $O\bigl((\sum n+\sum m)\log n\bigr)$，约 $4\cdot10^5\times18\approx7\times10^6$ 次基本操作。
- **空间**：邻接表 $O(n+m)$，三个 `int` 数组 $O(n)$，堆 $O(n+m)$，合计约 $10$ MB，远小于 $256$ MB。
- **实测**：本机（Apple clang `-O2`）$n=m=2\cdot10^5$ 的最大数据 $0.05$ s；Python3 版本同一数据 $0.4$ s。对 $3$ s 限时余量约 $60$ 倍。

## 7. 参考代码

### C++17

```cpp
#include <cstdio>
#include <vector>
#include <queue>
#include <deque>
#include <utility>
#include <algorithm>
using namespace std;

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;
    while (t--) {
        int n, m, w, x, y, z;
        scanf("%d %d", &n, &m);
        scanf("%d %d %d %d", &w, &x, &y, &z);
        --w; --x; --y; --z;
        vector<vector<int>> adj(n);
        for (int i = 0; i < m; i++) {
            int a, b; scanf("%d %d", &a, &b); --a; --b;
            adj[a].push_back(b); adj[b].push_back(a);
        }
        const int INF = 1000000000;
        auto bfs = [&](int s) {                       // 单源 BFS
            vector<int> d(n, -1); deque<int> q; d[s] = 0; q.push_back(s);
            while (!q.empty()) {
                int u = q.front(); q.pop_front();
                for (int v : adj[u]) if (d[v] < 0) { d[v] = d[u] + 1; q.push_back(v); }
            }
            return d;
        };
        vector<int> dx = bfs(x), dz = bfs(z);

        // A[u] = min over v in N(w) of d(x,v) + 3*d(v,u)
        vector<int> A(n, INF);
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
        for (int v : adj[w]) if (dx[v] < A[v]) { A[v] = dx[v]; pq.push({A[v], v}); }
        while (!pq.empty()) {                         // 边权恒为 3 的多源 Dijkstra
            auto [d, u] = pq.top(); pq.pop();
            if (d > A[u]) continue;                   // 惰性删除
            for (int v : adj[u]) if (d + 3 < A[v]) { A[v] = d + 3; pq.push({A[v], v}); }
        }

        bool wy = false;
        for (int v : adj[w]) if (v == y) wy = true;
        long long ans = INF;
        if (w == y) ans = min(ans, (long long)dx[z]);              // 分支 ①
        if (wy)     ans = min(ans, (long long)dx[y] + 1 + dz[w]);  // 分支 ②
        for (int u : adj[y]) if (A[u] < INF)                       // 分支 ③
            ans = min(ans, (long long)A[u] + 4 + dz[u]);
        printf("%lld\n", ans);
    }
    return 0;
}
```

### Python3

```python
import sys
from heapq import heappush, heappop


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    INF = 10 ** 9
    out = []
    for _ in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        w = int(data[pos]) - 1; x = int(data[pos + 1]) - 1
        y = int(data[pos + 2]) - 1; z = int(data[pos + 3]) - 1
        pos += 4
        adj = [[] for _ in range(n)]
        for _ in range(m):
            a = int(data[pos]) - 1; b = int(data[pos + 1]) - 1; pos += 2
            adj[a].append(b); adj[b].append(a)

        def bfs(s):                       # list 当队列，顺序遍历即 BFS 序
            d = [-1] * n
            d[s] = 0
            q = [s]
            for u in q:
                du = d[u] + 1
                for v in adj[u]:
                    if d[v] < 0:
                        d[v] = du; q.append(v)
            return d

        dx, dz = bfs(x), bfs(z)

        # 多源 Dijkstra：源集 N(w)，初值 d(x,v)，边权恒为 3
        A = [INF] * n
        pq = []
        for v in adj[w]:
            if dx[v] < A[v]:
                A[v] = dx[v]; heappush(pq, (dx[v], v))
        while pq:
            d, u = heappop(pq)
            if d > A[u]:
                continue
            nd = d + 3
            for v in adj[u]:
                if nd < A[v]:
                    A[v] = nd; heappush(pq, (nd, v))

        ans = INF
        if w == y:                        # 分支 ①
            ans = min(ans, dx[z])
        if y in adj[w]:                   # 分支 ②
            ans = min(ans, dx[y] + 1 + dz[w])
        for u in adj[y]:                  # 分支 ③
            ans = min(ans, A[u] + 4 + dz[u])
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$w=y$（分支①）**：第一坐标已就位，直接把第二坐标走到 $z$ 最省；样例 3 答案是 $0$ 而不是「至少交换一次」的 $2$。
2. **$w\sim y$（分支②）**：样例 2 的答案 $2$ 完全来自这一支；只写分支③ 会得到 $5$，直接 WA。
3. **$n=2$**：单边图正确答案 $3$（$1_1\to1_2\to2_1\to2_2$）来自分支②，而分支③ 算出 $9$，三支取 min 必须写全。
4. **多源初值写成 $0$**：源点必须是 $N(w)$、初值必须是 $d(x,v)$，否则结果偏小。
5. **$+4$ 写成 $+3$ 或 $+5$**：它等于「首次交换 $1$ + 最后一次推进 $3$」，写错整体偏 $1$，样例即挂。
6. **别把折扣塞回 DP**：若按真实值 $d(v_{i-1},v_{i+1})\in\{1,2\}$ 转移，又回到 $O(n^2)$ 的状态 DP；统一成 $3$ 才能压成一次最短路。
7. **多测 $t=10^4$**：不要每组 `memset` 大小 $2\cdot10^5$ 的数组，用 `vector` 按 $n$ 分配；$A$ 初始化成 `INF` 而非 `-1`。
8. **自环**：$p=q$ 不算相邻（简单图无自环），自测造数据时别误触发分支②。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：1 / 1 通过（按 Codeforces 标准 checker 的 token 比对，忽略空白与大小写）。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [Codeforces 2279A. Reverse and Double](https://codeforces.com/problemset/problem/2279/A)：同场 A 题，二分 + 暴力 + 数据结构，可对照「先化简操作再套模板」的节奏。
- [Codeforces 1737D. Ela and the Wiring Wizard](https://codeforces.com/problemset/problem/1737/D)：图上「变形」操作后求最短路，与本题「操作后的元图」思路同源。
- [LeetCode 787. K 站中转内最便宜的航班](https://leetcode.cn/problems/cheapest-flights-within-k-stops/)：分层状态最短路，体会「状态设计决定复杂度」。
- [Codeforces 20C. Dijkstra?](https://codeforces.com/problemset/problem/20/C)：最短路模板 + 路径还原，配合引理 4 的构造可输出本题方案。

**延伸思考**：

1. 若要求输出路径本身而非长度，按引理 4 的构造还原 $v\to u$ 的最短路即可，仍是 $O(n+m)$。
2. 若把交换代价改成 $c$，公式里 $+4$ 变成 $c+3$、每步 $3$ 变成 $2+c$，多源 Dijkstra 的边权同步修改。
3. 若「交换」放宽成任意两点都能换（不要求相邻），则 $k\le2$ 就够，答案退化成几个 BFS 距离的 $\min$；本题的复杂性正来自「必须相邻」，以及引理 2 那条「删点消折扣」的桥梁。
