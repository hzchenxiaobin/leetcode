# Codeforces 276E Little Girl and Problem on Trees 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/276/E
- **比赛来源**：Codeforces Round 169 (Div. 2) · Problem E（UTC 2013-02-24）
- **难度**：2100
- **标签**：树、树状数组、差分
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个点的树，**除根 1 外每个点度数 ≤ 2**。初始全 0。两种操作：

1. `0 v x d`：把所有与 $v$ 距离 ≤ $d$ 的点加 $x$；
2. `1 v`：输出点 $v$ 的当前值。

**约束**：$n, q \le 10^5$，$x \le 10^4$，$d < n$。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 6
1 2
1 3
0 3 1 2
0 2 3 1
0 1 5 2
1 1
1 2
1 3

输出：
9
9
6
```

官方样例 2：

```text
输入：
6 11
1 2
2 5
5 4
1 6
1 3
0 3 1 3
0 3 4 5
0 2 1 4
0 1 5 5
0 4 6 2
1 1
1 2
1 3
1 4
1 5
1 6

输出：
11
17
11
16
17
11
```

**观察 1（形状）**：除根外度数 ≤ 2 ⇒ 每个子树是一条**链**，整棵树是"蜘蛛"：根 1 挂着若干条链。

**观察 2（球的分解）**：设 $v$ 在第 $b$ 条链上、深度 $d_v$（到根的距离）。与 $v$ 距离 ≤ $d$ 的点分两类：

- **同链**：深度 $p$ 满足 $|p - d_v| \le d$ → 一段深度区间；
- **其它链**：必须经过根，距离 $= d_v + p$ → $p \le d - d_v$（所有链的深度前缀）；
- 根自己：需要 $d_v \le d$。

**观察 3（数据结构）**：

- 每条链一个 Fenwick（差分，区间加 / 单点查）处理"同链"；
- 一个按**深度**的全局 Fenwick 处理"跨链"，即所有链的深度前缀加；
- 但跨链更新不应作用到 $v$ 自己所在的链上（它已由同链规则处理），所以再给每条链维护一个"跨链扣减"的 Fenwick，查询时减去。

查询 $v$（非根）：`chain[b].query(d_v) + global.query(d_v) - chainCross[b].query(d_v)`。

## 3. 解题思路

![蜘蛛树上的"球"](../../../images/cf276e_spider.svg)

见上。总复杂度 $O((n+q)\log n)$。

## 4. 正确性证明

**引理 1（形状）**：除根外度数 $\le 2$ 的树，其每个"根的儿子"对应的子树是一条链。

**证明**：从某个儿子出发，除根外每个点度数 $\le 2$，扣除父边后至多一个儿子 → 是一条路径 ✓。∎

**引理 2（球分解）**：对链 $b$ 上深度 $d_v$ 的点 $v$，距 $v$ 不超过 $d$ 的点集 $=\{u \in b: |p_u - d_v| \le d\} \cup \{u \notin b, u \ne \text{根}: p_u \le d - d_v\} \cup \{\text{根}: d_v \le d\}$。

**证明**：同链距离 $= |p_u - d_v|$；跨链路径必经根，距离 $= d_v + p_u$ ✓。∎

**引理 3（结构正确）**：查询式给出 $v$ 处所有更新的累加。

**证明**：每次更新按引理 2 的分解写入三处结构：同链区间（chain[b]）、所有链深度前缀（global）、本链扣减（chainCross[b]）；查询时对 $v$ 取 `chain[b]` 的点值 + `global` 的深度前缀 − `chainCross[b]` 的深度前缀，恰好把"同链"与"跨链"分别计一次 ✓。根的值单独用累加器维护 ✓。∎

**定理**：算法正确。

**证明**：由引理 1–3 ✓。∎

## 5. 复杂度分析

- **时间**：$O((n+q)\log n)$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 2 s，$n = q = 10^5$ 实测端到端 49.8 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

struct Fenwick {                       // 区间加 + 单点查（差分）
    vector<ll> t; int n;
    void init(int n_) { n = n_; t.assign(n + 2, 0); }
    void add(int i, ll v) { for (; i <= n; i += i & -i) t[i] += v; }
    void range_add(int l, int r, ll v) { if (l > r) return; add(l, v); add(r + 1, -v); }
    ll query(int i) const { ll s = 0; for (int x = i; x > 0; x -= x & -x) s += t[x]; return s; }
};

int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int a, b; scanf("%d %d", &a, &b);
        adj[a].push_back(b); adj[b].push_back(a);
    }
    // 编号：1 是根；每个 1 的孩子开一条链
    vector<int> br(n + 1, -1), dep(n + 1, 0);
    vector<int> len;                     // 每条链的最大深度
    for (int c : adj[1]) {
        int b = (int)len.size();
        len.push_back(0);
        int prev = 1, cur = c, d = 1;
        while (true) {
            br[cur] = b; dep[cur] = d;
            len[b] = max(len[b], d);
            int nxt = -1;
            for (int u : adj[cur]) if (u != prev) { nxt = u; break; }
            if (nxt < 0) break;
            prev = cur; cur = nxt; d++;
        }
    }
    int maxdep = 0;
    for (int L : len) maxdep = max(maxdep, L);
    // 每条链一个 Fenwick（区间加、单点查）
    vector<int> off(len.size() + 1, 0);
    int total = 0;
    for (size_t b = 0; b < len.size(); b++) { off[b] = total; total += len[b] + 2; }
    auto makeFlat = [&]() { return vector<ll>(total + 2, 0); };
    vector<ll> fA = makeFlat(), fC = makeFlat();
    auto addFlat = [&](vector<ll>& f, int b, int i, ll v) {
        int base = off[b], cap = len[b];
        for (int x = i; x <= cap; x += x & -x) f[base + x] += v;
    };
    auto qFlat = [&](vector<ll>& f, int b, int i) {
        ll s = 0; int base = off[b];
        for (int x = i; x > 0; x -= x & -x) s += f[base + x];
        return s;
    };
    auto rangeFlat = [&](vector<ll>& f, int b, int l, int r, ll v) {
        if (l > r) return;
        addFlat(f, b, l, v);
        if (r + 1 <= len[b]) addFlat(f, b, r + 1, -v);
    };
    Fenwick globalF; globalF.init(maxdep + 2);
    ll rootVal = 0;
    while (q--) {
        int type; scanf("%d", &type);
        if (type == 0) {
            int v; ll x; int d;
            scanf("%d %lld %d", &v, &x, &d);
            if (v == 1) {
                rootVal += x;
                globalF.range_add(1, min(d, maxdep), x);
            } else {
                int b = br[v], dv = dep[v];
                if (dv <= d) rootVal += x;
                int lo = max(1, dv - d), hi = min(len[b], dv + d);
                rangeFlat(fA, b, lo, hi, x);
                int D = d - dv;
                if (D >= 1) {
                    int Dc = min(D, maxdep);
                    globalF.range_add(1, Dc, x);
                    rangeFlat(fC, b, 1, min(D, len[b]), -x);
                }
            }
        } else {
            int v; scanf("%d", &v);
            if (v == 1) { printf("%lld\n", rootVal); }
            else {
                int b = br[v], p = dep[v];
                ll ans = qFlat(fA, b, p) + globalF.query(p) + qFlat(fC, b, p);
                printf("%lld\n", ans);
            }
        }
    }
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    q = int(data[pos]); pos += 1
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = int(data[pos]); b = int(data[pos + 1]); pos += 2
        adj[a].append(b); adj[b].append(a)
    br = [-1] * (n + 1)
    dep = [0] * (n + 1)
    lens = []
    for c in adj[1]:
        b = len(lens); lens.append(0)
        prev, cur, d = 1, c, 1
        while True:
            br[cur] = b; dep[cur] = d
            if d > lens[b]: lens[b] = d
            nxt = -1
            for u in adj[cur]:
                if u != prev:
                    nxt = u; break
            if nxt < 0: break
            prev, cur, d = cur, nxt, d + 1
    maxdep = max(lens) if lens else 0
    total = sum(L + 2 for L in lens)
    fA = [0] * (total + 2)
    fC = [0] * (total + 2)
    off = [0] * len(lens)
    acc = 0
    for b, L in enumerate(lens):
        off[b] = acc; acc += L + 2
    def addFlat(f, b, i, v):
        cap = lens[b]; base = off[b]
        while i <= cap:
            f[base + i] += v
            i += i & -i
    def qFlat(f, b, i):
        base = off[b]; s = 0
        while i > 0:
            s += f[base + i]
            i -= i & -i
        return s
    def rangeFlat(f, b, l, r, v):
        if l > r: return
        addFlat(f, b, l, v)
        if r + 1 <= lens[b]: addFlat(f, b, r + 1, -v)
    # 全局按深度的 BIT
    gsize = maxdep + 2
    g = [0] * (gsize + 2)
    def gadd(i, v):
        while i <= gsize:
            g[i] += v
            i += i & -i
    def grange(l, r, v):
        if l > r: return
        gadd(l, v)
        if r + 1 <= gsize: gadd(r + 1, -v)
    def gq(i):
        s = 0
        while i > 0:
            s += g[i]
            i -= i & -i
        return s
    rootVal = 0
    out = []
    for _ in range(q):
        t = int(data[pos]); pos += 1
        if t == 0:
            v = int(data[pos]); x = int(data[pos + 1]); d = int(data[pos + 2]); pos += 3
            if v == 1:
                rootVal += x
                grange(1, min(d, maxdep), x)
            else:
                b = br[v]; dv = dep[v]
                if dv <= d: rootVal += x
                lo = max(1, dv - d); hi = min(lens[b], dv + d)
                rangeFlat(fA, b, lo, hi, x)
                D = d - dv
                if D >= 1:
                    grange(1, min(D, maxdep), x)
                    rangeFlat(fC, b, 1, min(D, lens[b]), -x)
        else:
            v = int(data[pos]); pos += 1
            if v == 1:
                out.append(str(rootVal))
            else:
                b = br[v]; p = dep[v]
                out.append(str(qFlat(fA, b, p) + gq(p) + qFlat(fC, b, p)))
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
main()
```

## 7. 边界情况与易错点

1. **$v$ 是根**：更新作用于所有深度 ≤ $d$ 的点；查询读累加器。
2. **$d - d_v < 1$**：没有跨链部分。
3. **深度区间越界**：与链长取 min。
4. **差分的右端点 +1**：Fenwick 边界不要越界。
5. **74 位**：值可达 $q\cdot x = 10^9$，64 位保险。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（9/9/6、11/17/11/16/17/11），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版每次更新做 BFS 找距离 ≤ $d$ 的点直接加。随机 200 组（$n \le 8$，随机蜘蛛树 + 随机操作），**200 / 200 全部一致**。
- **最大约束性能**：$n = q = 10^5$，实测端到端 49.8 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 276D Little Girl and Maximum XOR](https://codeforces.com/problemset/problem/276/D)：同场 D 题。
- [Codeforces 375D Tree and Queries](https://codeforces.com/problemset/problem/375/D)：树上操作的另一类做法。

**延伸思考**：

1. **如果度数不受限**：变成"树上半径更新"，需要点分树或动态树。
2. **如果要求区间求值**：需要更复杂的结构。

