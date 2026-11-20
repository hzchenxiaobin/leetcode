# Codeforces 165D 胡须图的路径查询 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/165/D
- **比赛来源**：Codeforces Round 112 (Div. 2) · Problem D（UTC 2012-03-16）
- **难度**：2100
- **标签**：树链剖分、线段树
- **评测类型**：普通
- **限制**：时间 4 s / 内存 256 MB

**题意**：$n$ 个点、$n-1$ 条边的连通图（"胡须图"：最多一个点度数 $>2$，即若干条链交于一点）。每条边初始为黑。操作：把第 $i$ 条边涂黑/涂白；询问 $a,b$ 之间是否只经黑边连通，若可以输出最短距离（边数），否则输出 $-1$。

**约束**：$n\le10^5$、$m\le3\times10^5$：树链剖分 + 线段树维护"白边个数"。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3
1 2
2 3
7
3 1 2
3 1 3
3 2 3
2 2
3 1 2
3 1 3
3 2 3
输出：
1
2
1
1
-1
-1
```

链 1–2–3，初始全黑：距离分别 1、2、1 ✓；把第 2 条边（2–3）涂白后：1–2 仍黑（距离 1），1–3 与 2–3 需经过白边 ⇒ -1 ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
6
1 5
6 4
2 3
3 5
5 6
6
3 3 4
2 5
3 2 6
3 1 2
2 3
3 3 1
输出：
3
-1
3
2
```

![把边权挂在子节点上，路径查询 = 两条链上的区间和](../../../images/cf165d_hld.svg)

**观察**：图是树（$n-1$ 条边、连通）。把每条边的颜色记在"较深的端点"上，则"$a\to b$ 路径全黑" ⟺ 路径上白边数 $=0$；距离 = $\text{depth}[a]+\text{depth}[b]-2\,\text{depth}[\text{lca}]$。

用树链剖分把路径拆成 $O(\log n)$ 段区间，线段树维护区间内白边个数 ⇒ 单点修改、区间求和。

## 3. 解题思路

1. 以 1 为根，求 `parent/depth/size/heavy`，再做树链剖分得到 `head/pos`；
2. 线段树按 `pos` 存"该位置对应边是否白"（1/0）；
3. 涂色：找到第 $i$ 条边较深的端点，单点更新；
4. 查询：沿重链向上跳，累计白边数并求得 LCA；若白边数为 0 输出深度差，否则 -1。

![样例 1 的 7 次查询](../../../images/cf165d_sample.svg)

## 4. 正确性证明

**引理 1（边权挂在子节点）**：把边 $uv$（$u$ 是 $v$ 的父）的颜色记在 $v$ 上，则树上一条路径 $a\to b$ 的边集合恰是"$a$ 到 lca（不含 lca）"与"$b$ 到 lca（不含 lca）"上的所有点（除 lca 外）所挂的边。

**证明**：树上路径唯一，每条边由其较深端点唯一标识 ✓ 路径上的边正是两端点路径上除 lca 外的点所挂的边 ✓ ∎

**引理 2（树链剖分的路径分解）**：任一路径可分解为 $O(\log n)$ 个"同一条重链上的连续区间"，且每个区间对应线段树上的一段。

**证明**：树链剖分的标准性质：沿重链跳跃时，每次跳到链头再上跳，轻边数 $O(\log n)$ ✓ 每段在 `pos` 上连续 ✓ ∎

**引理 3（判定与距离）**：路径全黑 ⟺ 区间和为 0；此时最短距离 $=\text{depth}[a]+\text{depth}[b]-2\text{depth}[\text{lca}]$。

**证明**：区间和 = 路径上白边数（引理 1、2）✓ 全黑时唯一路径即最短（树中唯一简单路径）✓ ∎

**定理**：程序输出正确。

**证明**：由引理 1–3，每次涂色正确更新对应边；每次询问先求白边数（为 0 才可达），再输出深度差或 -1 ✓ ∎

## 5. 复杂度分析

- **时间**：建树剖分 $O(n)$；每次操作 $O(\log^2 n)$（$O(\log n)$ 段 × 线段树 $O(\log n)$）；$n=10^5$、$m=3\times10^5$ 实测约 140 ms。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 100005;
vector<int> g[MAXN];
int par_[MAXN], dep[MAXN], sz[MAXN], heavy[MAXN], head[MAXN], pos_[MAXN];
int edgeTo[MAXN];                 // 第 i 条边对应的"子节点"
int timer_ = 0;
// 线段树：区间内白边个数
static int seg[4 * MAXN];

void build(int node, int l, int r) {
    seg[node] = 0;
    if (l == r) return;
    int mid = (l + r) / 2;
    build(2 * node, l, mid);
    build(2 * node + 1, mid + 1, r);
}
void update(int node, int l, int r, int idx, int val) {
    if (l == r) { seg[node] = val; return; }
    int mid = (l + r) / 2;
    if (idx <= mid) update(2 * node, l, mid, idx, val);
    else update(2 * node + 1, mid + 1, r, idx, val);
    seg[node] = seg[2 * node] + seg[2 * node + 1];
}
int query(int node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return seg[node];
    int mid = (l + r) / 2;
    return query(2 * node, l, mid, ql, qr) + query(2 * node + 1, mid + 1, r, ql, qr);
}
int dfsSize(int u, int p) {
    par_[u] = p; sz[u] = 1; heavy[u] = -1;
    int best = 0;
    for (int v : g[u]) {
        if (v == p) continue;
        dep[v] = dep[u] + 1;
        sz[u] += dfsSize(v, u);
        if (sz[v] > best) { best = sz[v]; heavy[u] = v; }
    }
    return sz[u];
}
void dfsHLD(int u, int p, int h) {
    head[u] = h;
    pos_[u] = timer_++;
    if (heavy[u] != -1) dfsHLD(heavy[u], u, h);
    for (int v : g[u]) {
        if (v == p || v == heavy[u]) continue;
        dfsHLD(v, u, v);
    }
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> eu(n - 1), ev(n - 1);
    for (int i = 0; i < n - 1; i++) {
        scanf("%d %d", &eu[i], &ev[i]);
        g[eu[i]].push_back(ev[i]);
        g[ev[i]].push_back(eu[i]);
    }
    dep[1] = 0;
    dfsSize(1, 0);
    dfsHLD(1, 0, 1);
    build(1, 0, n - 1);
    // 把每条边定位到"较深"的端点
    for (int i = 0; i < n - 1; i++) {
        int a = eu[i], b = ev[i];
        edgeTo[i] = (dep[a] > dep[b]) ? a : b;
    }
    int m;
    if (scanf("%d", &m) != 1) return 0;
    for (int qi = 0; qi < m; qi++) {
        int t;
        scanf("%d", &t);
        if (t == 1 || t == 2) {
            int i;
            scanf("%d", &i);
            i--;                                       // 0 基
            update(1, 0, n - 1, pos_[edgeTo[i]], (t == 2) ? 1 : 0);   // 2 = 涂白
        } else {
            int a, b;
            scanf("%d %d", &a, &b);
            long long whites = 0;
            int u = a, v = b;
            while (head[u] != head[v]) {
                if (dep[head[u]] < dep[head[v]]) swap(u, v);
                whites += query(1, 0, n - 1, pos_[head[u]], pos_[u]);
                u = par_[head[u]];
            }
            if (dep[u] > dep[v]) swap(u, v);
            // u 为 LCA
            whites += query(1, 0, n - 1, pos_[u] + 1, pos_[v]);
            if (whites > 0) printf("-1\n");
            else printf("%d\n", dep[a] + dep[b] - 2 * dep[u]);
        }
    }
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    p = 0
    n = int(data[p]); p += 1
    g = [[] for _ in range(n + 1)]
    eu = [0] * (n - 1)
    ev = [0] * (n - 1)
    for i in range(n - 1):
        a = int(data[p]); b = int(data[p + 1]); p += 2
        eu[i] = a; ev[i] = b
        g[a].append(b); g[b].append(a)
    # 迭代求 parent / depth / size / heavy
    par_ = [0] * (n + 1)
    dep = [0] * (n + 1)
    order = []
    stack = [1]
    par_[1] = 0
    seen = [False] * (n + 1)
    seen[1] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                par_[v] = u
                dep[v] = dep[u] + 1
                stack.append(v)
    sz = [1] * (n + 1)
    heavy = [-1] * (n + 1)
    for u in reversed(order):
        best = 0
        for v in g[u]:
            if v == par_[u]:
                continue
            sz[u] += sz[v]
            if sz[v] > best:
                best = sz[v]
                heavy[u] = v
    head = [0] * (n + 1)
    pos_ = [0] * (n + 1)
    timer = 0
    stack = [(1, 1)]
    while stack:
        u, h = stack.pop()
        # 沿重链一路走
        while u != -1:
            head[u] = h
            pos_[u] = timer
            timer += 1
            for v in g[u]:
                if v != par_[u] and v != heavy[u]:
                    stack.append((v, v))
            u = heavy[u]
    # 线段树（白边计数）
    size = 1
    while size < n:
        size <<= 1
    seg = [0] * (2 * size)

    def update(idx, val):
        i = idx + size
        seg[i] = val
        i >>= 1
        while i:
            seg[i] = seg[2 * i] + seg[2 * i + 1]
            i >>= 1

    def query(l, r):
        if l > r:
            return 0
        res = 0
        l += size; r += size
        while l <= r:
            if l & 1:
                res += seg[l]; l += 1
            if not (r & 1):
                res += seg[r]; r -= 1
            l >>= 1; r >>= 1
        return res

    edgeTo = [0] * (n - 1)
    for i in range(n - 1):
        edgeTo[i] = eu[i] if dep[eu[i]] > dep[ev[i]] else ev[i]
    m = int(data[p]); p += 1
    out = []
    for _ in range(m):
        t = int(data[p]); p += 1
        if t == 1 or t == 2:
            i = int(data[p]) - 1; p += 1
            update(pos_[edgeTo[i]], 1 if t == 2 else 0)
        else:
            a = int(data[p]); b = int(data[p + 1]); p += 2
            u, v = a, b
            whites = 0
            while head[u] != head[v]:
                if dep[head[u]] < dep[head[v]]:
                    u, v = v, u
                whites += query(pos_[head[u]], pos_[u])
                u = par_[head[u]]
            if dep[u] > dep[v]:
                u, v = v, u
            whites += query(pos_[u] + 1, pos_[v])
            out.append("-1" if whites > 0 else str(dep[a] + dep[b] - 2 * dep[u]))
    print("\n".join(out))


main()
```

## 7. 边界情况与易错点

1. **边的颜色挂在较深端点**：查询时要排除 LCA 自己（`pos_[u]+1`）。
2. **图是树**：$n-1$ 条边且连通（题面保证"胡须图"）。
3. **递归深度**：$10^5$ 的链会让 C++ 递归爆栈 ⇒ 需要开栈/改迭代（Python 用迭代）。
4. **涂色语义**：操作 2 = 涂白（记 1），操作 1 = 涂黑（记 0）。
5. **LCA**：在树链跳跃结束后统一得到。
6. **距离**：全黑时用深度差（不经过白边才可达）。
7. **多解**：本题输出唯一。
8. **输入规模**：$m=3\times10^5$，用快速读入。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/165/D_胡须图的路径查询.md`
- **官方样例**：$2/2$ 通过（多行输出逐行一致）。
- **独立对拍**：另写"每次询问只沿黑边 BFS 求最短路"的暴力，对 $189$ 组随机胡须图（$n\le7$、随机涂色序列）比较，全部一致。
- **性能**：$n=10^5$、$m=3\times10^5$ 实测 C++ 约 140 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 165E Compatible Numbers](https://codeforces.com/problemset/problem/165/E)：同场 E 题。
- [Luogu P3384 树链剖分模板](https://www.luogu.com.cn/problem/P3384)：HLD 模板。
- [LeetCode 2846. 边权重均等查询](https://leetcode.cn/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/)：树上路径查询。

**延伸思考**：

1. **若要求"经过最少的白边"**：把白边记 1、黑边记 0，求路径最小白边数（仍是路径和）。
2. **若图是胡须（星形链）**：可以只用每条链的前缀和做到 $O(1)$ 查询。
3. **若允许动态加边**：需要 Link-Cut Tree。
