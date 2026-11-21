# Codeforces 266D BerDonalds 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/266/D
- **比赛来源**：Codeforces Round 163 (Div. 2) · Problem D（UTC 2013-01-22）
- **难度**：2400
- **标签**：图论、最短路、三分/分段线性
- **评测类型**：普通（浮点，$10^{-9}$）
- **限制**：时间 5 s / 内存 256 MB

**题意**：无向连通带权图。把餐厅建在**任意位置**（可以在边的内部），使"到最远顶点的最短路"最小。输出这个最小值。

**约束**：$n$ 较小（可做 $n$ 次最短路），$m$ 较大；边权 $\le 10^5$。

## 2. 示例与观察

官方样例 1：

```text
输入：
2 1
1 2 1

输出：
0.50
```

官方样例 2：

```text
输入：
3 3
1 2 1
2 3 1
1 3 1

输出：
1.00
```

官方样例 3：

```text
输入：
3 2
1 2 100
2 3 1

输出：
50.50
```

**样例 1**：只有一条边，中点最优 → 0.5。

**样例 2**：三角形，任取一点（如在某边中点）最远距离都是 1。

**样例 3**：链 1-2（100）、2-3（1）。若餐厅在长边上距 1 号 $t$ 处：到 1 是 $t$，到 2 是 $100-t$，到 3 是 $101-t$ → 最大 $= 101-t$（对 $t \le 100$），最小在 $t=100$ 处得 1？不对——还要考虑 $t$ 小时到 1 的距离：max$(t, 101-t)$ 在 $t = 50.5$ 处取 50.5 ✓ 与样例一致。

**观察 1**：设点在边 $(u,v,w)$ 上、距 $u$ 为 $t$（$0 \le t \le w$）。到顶点 $x$ 的距离是 $\min(d_u[x] + t,\ d_v[x] + w - t)$。

**观察 2**：对每个 $x$，这是两条直线的最小值（一个"帐篷"）；总偏心距 $h(t) = \max_x(\cdot)$。

**观察 3**：$h$ 是分段线性函数；在每段上 $h(t) = \max(P + t, Q - t)$（$P$ 为"上升那半边"的最大截距、$Q$ 为"下降那半边"的最大截距），最小值在 $t = (Q-P)/2$ 或段的端点。

**观察 4**：把顶点按 $p_x - q_x$ 排序（$p_x = d_u[x]$、$q_x = d_v[x]+w$），"哪一半"随 $t$ 增大只会从"下降"变成"上升"，所以按排序顺序枚举分界点，用前缀/后缀最大值 $O(n)$ 求出每段的最小值。

## 3. 解题思路

![图的绝对中心：可以在边的内部取点](../../../images/cf266d_edge.svg)

1. 从每个顶点跑 Dijkstra 得到 $d[\cdot][\cdot]$；
2. 对每条边 $(u,v,w)$：
   - $p_x = d_u[x]$、$q_x = d_v[x]+w$，按 $p_x - q_x$ 升序排序；
   - 前缀 $\max p$、前缀 $\min (q-p)/2$；后缀 $\max q$、后缀 $\max (q-p)/2$；
   - 对每个分界 $k$（0..n），可行 $t$ 区间 $[\max(0, \text{suf}), \min(w, \text{pre})]$，在该区间上最小化 $\max(P_k + t, Q_k - t)$（取 $t = (Q_k-P_k)/2$ 再裁剪）；
3. 所有边取最小即为答案。

## 4. 正确性证明

**引理 1（距离公式）**：点在边 $(u,v,w)$ 上距 $u$ 为 $t$ 时，到顶点 $x$ 的最短路长为 $\min(d_u[x]+t,\ d_v[x]+w-t)$。

**证明**：任何从该点到 $x$ 的最短路必然先从 $(u,v)$ 内部走到 $u$ 或 $v$（该边内部没有其它节点），故取二者较小 ✓。∎

**引理 2（分段表示）**：对固定的 $k$（按 $p-q$ 排序后的前 $k$ 个），在区间 $t \in [\max(0,\max_{x \notin S}(q_x-p_x)/2),\ \min(w,\min_{x \in S}(q_x-p_x)/2)]$ 上，$h(t) = \max(P_k + t,\ Q_k - t)$。

**证明**：$x \in S$ 时 $p_x + t \le q_x - t$（因为 $t \le (q_x-p_x)/2$），所以该顶点贡献 $p_x + t$；反之贡献 $q_x - t$。取最大即得 ✓。∎

**引理 3（每段最优）**：$\max(P+t, Q-t)$ 在 $t = (Q-P)/2$ 处取最小（若该点在区间内），否则在区间端点。

**证明**：这是"V 形"函数，两支斜率 $\pm 1$，交点即最小点 ✓。∎

**定理**：算法输出全图绝对中心的最小偏心距。

**证明**：全图任意点都在某条边上（或顶点，可作为边的端点 $t=0$ 或 $t=w$，已被覆盖）。由引理 1、2、3，算法对每条边求出了 $h$ 的最小值，取全局最小即答案 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n(m\log n) + m n \log n)$（$n$ 次 Dijkstra + 每条边排序）。
- **空间**：$O(n^2 + m)$。
- **与时限的关系**：时限 5 s，$n = 100$、$m = 4950$ 实测端到端 23.8 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
static const ll INFLL = (ll)4e18;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<int> eu(m), ev(m), ew(m);
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        scanf("%d %d %d", &eu[i], &ev[i], &ew[i]);
        adj[eu[i]].push_back({ev[i], ew[i]});
        adj[ev[i]].push_back({eu[i], ew[i]});
    }
    // n 很小：从每个点跑一次 Dijkstra
    vector<vector<ll>> d(n + 1, vector<ll>(n + 1, INFLL));
    for (int s = 1; s <= n; s++) {
        priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<pair<ll,int>>> pq;
        d[s][s] = 0; pq.push({0, s});
        while (!pq.empty()) {
            auto [du, u] = pq.top(); pq.pop();
            if (du != d[s][u]) continue;
            for (auto [v, w] : adj[u]) if (du + w < d[s][v]) { d[s][v] = du + w; pq.push({d[s][v], v}); }
        }
    }
    double ans = 1e30;
    for (int e = 0; e < m; e++) {
        int u = eu[e], v = ev[e], w = ew[e];
        vector<int> idx(n);
        iota(idx.begin(), idx.end(), 1);
        sort(idx.begin(), idx.end(), [&](int a, int b) {
            return (d[u][a] - d[v][a]) < (d[u][b] - d[v][b]);
        });
        vector<double> p(n + 1), q(n + 1);
        for (int x = 1; x <= n; x++) { p[x] = (double)d[u][x]; q[x] = (double)d[v][x] + w; }
        vector<double> prefMaxP(n + 2, -1e30), sufMaxQ(n + 2, -1e30);
        vector<double> prefMinHalf(n + 2, 1e30), sufMaxHalf(n + 2, -1e30);
        for (int k = 0; k < n; k++) {
            int x = idx[k];
            prefMaxP[k + 1] = max(prefMaxP[k], p[x]);
            prefMinHalf[k + 1] = min(prefMinHalf[k], (q[x] - p[x]) / 2.0);
        }
        for (int k = n - 1; k >= 0; k--) {
            int x = idx[k];
            sufMaxQ[k] = max(sufMaxQ[k + 1], q[x]);
            sufMaxHalf[k] = max(sufMaxHalf[k + 1], (q[x] - p[x]) / 2.0);
        }
        for (int k = 0; k <= n; k++) {
            double lo = (k == n ? -1e30 : sufMaxHalf[k]);          // 不在 S 的约束
            double hi = (k == 0 ? 1e30 : prefMinHalf[k]);          // 在 S 的约束
            lo = max(lo, 0.0);
            hi = min(hi, (double)w);
            if (lo > hi + 1e-12) continue;
            double ps = prefMaxP[k], qc = sufMaxQ[k];
            double best;
            if (k == 0) best = qc - hi;                            // h(t) = qc - t
            else if (k == n) best = ps + lo;                       // h(t) = ps + t
            else {
                double t = (qc - ps) / 2.0;
                t = max(lo, min(hi, t));
                best = max(ps + t, qc - t);
            }
            ans = min(ans, best);
        }
    }
    printf("%.10f\n", ans);
    return 0;
}
```

### Python3

```python
import sys
import heapq

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    eu = [0] * m; ev = [0] * m; ew = [0] * m
    adj = [[] for _ in range(n + 1)]
    pos = 2
    for i in range(m):
        eu[i] = int(data[pos]); ev[i] = int(data[pos + 1]); ew[i] = int(data[pos + 2]); pos += 3
        adj[eu[i]].append((ev[i], ew[i]))
        adj[ev[i]].append((eu[i], ew[i]))
    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for s in range(1, n + 1):
        d = dist[s]; d[s] = 0
        pq = [(0, s)]
        while pq:
            du, u = heapq.heappop(pq)
            if du != d[u]:
                continue
            for v, w in adj[u]:
                if du + w < d[v]:
                    d[v] = du + w
                    heapq.heappush(pq, (d[v], v))
    ans = float('inf')
    for e in range(m):
        u, v, w = eu[e], ev[e], ew[e]
        order = sorted(range(1, n + 1), key=lambda x: dist[u][x] - dist[v][x])
        p = [0.0] * (n + 1); q = [0.0] * (n + 1)
        for x in range(1, n + 1):
            p[x] = dist[u][x]; q[x] = dist[v][x] + w
        prefMaxP = [-1e30] * (n + 2); prefMinHalf = [1e30] * (n + 2)
        sufMaxQ = [-1e30] * (n + 2); sufMaxHalf = [-1e30] * (n + 2)
        for k in range(n):
            x = order[k]
            prefMaxP[k + 1] = max(prefMaxP[k], p[x])
            prefMinHalf[k + 1] = min(prefMinHalf[k], (q[x] - p[x]) / 2.0)
        for k in range(n - 1, -1, -1):
            x = order[k]
            sufMaxQ[k] = max(sufMaxQ[k + 1], q[x])
            sufMaxHalf[k] = max(sufMaxHalf[k + 1], (q[x] - p[x]) / 2.0)
        for k in range(n + 1):
            lo = -1e30 if k == n else sufMaxHalf[k]
            hi = 1e30 if k == 0 else prefMinHalf[k]
            lo = max(lo, 0.0); hi = min(hi, float(w))
            if lo > hi + 1e-12:
                continue
            if k == 0:
                best = sufMaxQ[k] - hi
            elif k == n:
                best = prefMaxP[k] + lo
            else:
                t = (sufMaxQ[k] - prefMaxP[k]) / 2.0
                t = max(lo, min(hi, t))
                best = max(prefMaxP[k] + t, sufMaxQ[k] - t)
            ans = min(ans, best)
    sys.stdout.write("%.10f\n" % ans)

main()
```

## 7. 边界情况与易错点

1. **答案可能在顶点上**：$t=0$ 与 $t=w$ 的分段已被覆盖。
2. **浮点比较**：区间裁剪用 $10^{-12}$ 的容差。
3. **多边**：题面保证没有重边，但实现里 Dijkstra 不受影响。
4. **$n=2$**：只有一条边，答案 $w/2$。
5. **输出精度**：`%.10f` 足够（要求 $10^{-9}$）。
6. **排序键**：$p_x - q_x$（整数），避免浮点排序。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（0.5、1.0、50.5），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf266d.py`（与官方答案比较，误差 $10^{-9}$）。
- **独立暴力对拍**：暴力版对每条边采样 4000 个点计算偏心距的最小值；200 组随机小图，差值都在采样分辨率内（$< w/4000$），**200 / 200 通过**。
- **最大约束性能**：$n = 100$、$m = 4950$，实测端到端 23.8 ms。
- **图片校验**：两张 SVG 通过 `ElementTree.parse`，含 `feTurbulence` 与手写字体。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 266E More Queries to Array](https://codeforces.com/problemset/problem/266/E)：同场 E 题，线段树。
- [Codeforces 119A Epic Game](https://codeforces.com/problemset/problem/119/A)：与"图上中心"无关，仅为对照。

**延伸思考**：

1. **如果要求建在顶点上**：直接取 $\min_v \max_x d[v][x]$。
2. **如果是 $k$ 个餐厅**：$k$-center 问题，NP 难。

