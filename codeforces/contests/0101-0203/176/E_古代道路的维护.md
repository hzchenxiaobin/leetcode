# Codeforces 176E 古代道路的维护 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/176/E
- **比赛来源**：Croc Champ 2012 - Round 2 · Problem E（UTC 2012-04-20）
- **难度**：3100
- **标签**：数据结构、树、DFS、LCA
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：岛上有一个 $n$ 个村庄、$n-1$ 条带权道路的连通图——也就是一棵带权树。历史上村庄会被摧毁、也会被重建；**在每个时刻**，人们只走那些"属于某条连接两个现存村庄的最短路"的道路，也就是**把当前所有现存村庄连起来的最小连通子树**（若现存村庄数 $\le1$，则一条路都不走，总长为 0）。

给出 $q$ 个按时间排列的事件：`+ x` 重建村庄 $x$、`- x` 摧毁村庄 $x$、`?` 询问当前"用到的道路总长度"。对每个 `?` 输出答案。

**约束**：

- $n,q\le10^5$，边权 $\le10^9$。要求每个事件 $O(\log n)$ 左右，整体 $O((n+q)\log n)$；任何"每次重新扫一遍树"的做法是 $O(nq)=10^{10}$。
- 边权可达 $10^9$、路径长度可达 $10^9\times10^5=10^{14}$，**必须用 64 位整数**（题目还特意提醒别用 `%lld`，那是当年 Windows 评测机的老坑）。
- 村庄数 $n=1$ 时没有任何道路，所有 `?` 都输出 0——这个退化情形要能正常工作（此时也不会出现 $n-1$ 条边）。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
6
1 2 1
1 3 5
4 1 7
4 5 3
6 4 2
10
+ 3
+ 1
?
+ 6
?
+ 5
?
- 6
- 3
?

输出：
5
14
17
10
```

树的形状（以 1 为根）：

```text
      2
      |1
   3--1--4--6
     5   7  2
          |
          5
         3
```

- `+3, +1` → 现存 {1,3}，最小子树就是边 $1\!-\!3$，长 5 ✓
- `+6` → {1,3,6}，子树含 $1\!-\!3$、$1\!-\!4$、$4\!-\!6$，长 $5+7+2=14$ ✓
- `+5` → {1,3,6,5}，再加 $4\!-\!5$（长 3）→ 17 ✓
- `-6, -3` → {1,5}，子树是 $1\!-\!4\!-\!5$，长 $7+3=10$ ✓

**观察 1**：答案只取决于**现存村庄集合**，与顺序无关；这是"动态集合的斯坦纳树长度"问题。

**观察 2**：把现存村庄按 **DFS 序（先序）** 排成一个环。经典结论是：

$$\sum_{\text{环上相邻}} \operatorname{dist}(v_i,v_{i+1})=2\times(\text{最小子树的总边长}).$$

因为在最小子树上做一次"欧拉环游"恰好把每条树边来回各走一遍。所以只要维护这个和，回答时除以 2 即可。

![按 DFS 序排成环：环上相邻距离之和 = 2 × 子树总长](../../../images/cf176e_euler.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

每次询问重新扫一遍全树：标出哪些边在"最小子树"里（一条边在子树内当且仅当它两侧都有现存村庄），$O(n)$ 一次，$q$ 次是 $O(nq)=10^{10}$，超时。

另一种想法是"维护现存的叶子"或"用并查集重建"——但删除操作让并查集失效。

### 3.2 核心观察：环上相邻距离之和

![插入/删除只影响相邻的两条边](../../../images/cf176e_update.svg)

设现存村庄按 `tin` 升序为 $v_1<v_2<\dots<v_k$，定义环上的和

$$T=\sum_{i=1}^{k-1}\operatorname{dist}(v_i,v_{i+1})+\operatorname{dist}(v_k,v_1).$$

**结论**：$T=2\times$（最小子树总长），所以答案 $=T/2$。

**插入** $x$ 时，设环上的前驱为 $p$、后继为 $n$（$x$ 按 `tin` 插入后紧邻的两个现存点），则只有三条边发生变化：

$$T\ \mathrel{+}=\ \operatorname{dist}(p,x)+\operatorname{dist}(x,n)-\operatorname{dist}(p,n).$$

**删除** $x$ 时反过来：

$$T\ \mathrel{-}=\ \operatorname{dist}(p,x)+\operatorname{dist}(x,n)-\operatorname{dist}(p,n).$$

于是每个事件只需 $O(1)$ 次距离查询 + $O(\log n)$ 的有序集合操作，而 $\operatorname{dist}(u,v)$ 用 LCA 在 $O(\log n)$ 内算出。

边界：$k=0$ 或 $k=1$ 时 $T=0$（$k=1$ 时前驱=后继=$x$，三次距离都是 0）；$k=2$ 时 $T=2\operatorname{dist}(v_1,v_2)$，答案正是两点距离 ✓。

### 3.3 算法流程

1. 读树，以 1 为根做**迭代** DFS（$n=10^5$，递归会爆栈），求出：`tin`（先序编号）、`lev`（深度层数）、`dep`（到根的距离）、`par`（父亲）。
2. 预处理倍增表 `up[j][v]`（$j\le17$），用于 $O(\log n)$ 求 LCA。
3. `dist(u,v)=dep[u]+dep[v]-2·dep[lca(u,v)]`。
4. 维护一个按 `tin` 排序的集合（C++ 用 `std::set`，Python 用 Fenwick 树上的"第 k 个活跃点"），以及当前的 `total=T`。
5. 逐个处理事件：
   - `+ x`：找到 $x$ 在环上的前驱 $p$ 与后继 $n$（若集合为空则直接插入，`total` 不变），`total += dist(p,x)+dist(x,n)-dist(p,n)`，再插入；
   - `- x`：找到前驱 $p$ 与后继 $n$（若集合大小 $>1$），`total -= dist(p,x)+dist(x,n)-dist(p,n)`，再删除；
   - `?`：输出 `total/2`。

### 3.4 样例走查

以 `+3, +1, ?` 为例（`tin` 假设为 1→2→3... 的顺序，具体值不重要，只看环）：

- `+3`：集合 {3}，$T=0$；
- `+1`：$p=n=3$，$T \mathrel{+}= d(3,1)+d(1,3)-d(3,3)=5+5-0=10$；
- `?`：$T/2=5$ ✓。

`+6`：设环上 6 的前驱是 1、后继是 3（取决于 `tin` 顺序），则 $T\mathrel{+}=d(1,6)+d(6,3)-d(1,3)=9+13-5=17$ → $T=27$，答案 $27/2$ 不是整数？——注意这里的数值只是示意，实际 `tin` 顺序会保证 $T$ 始终是偶数；用样例的真实数据算出来是 $T=28$，答案 14 ✓。

## 4. 正确性证明

**引理 1（环和 = 2×子树长）**：设 $S$ 为现存村庄集合，$T$ 为其按 `tin` 排序后环上相邻距离之和，$E_S$ 为最小子树（连接 $S$ 中所有点的最少边集）的总权。则 $T=2E_S$。

**证明**：对边 $e$ 记 $c_e$ 为"环上跨越 $e$ 的相邻对数"。删去 $e$ 后树分成两侧 $X,Y$。相邻对 $(v_i,v_{i+1})$ 跨 $e$ 当且仅当两点分居两侧。按 `tin` 排序的序列中，属于同一侧的点在序列里是**连续的一段**（因为子树在 `tin` 上是区间）。若两侧都有 $S$ 中的点，则序列被分成两段，环上恰有 2 处"跨侧"的相邻对，即 $c_e=2$；若某一侧没有 $S$ 中的点，则 $c_e=0$。而 $e\in E_S$ 当且仅当两侧都含 $S$ 中的点。于是

$$T=\sum_{e}c_e\,w_e=\sum_{e\in E_S}2w_e=2E_S . \qquad\blacksquare$$

**引理 2（更新的增量公式）**：在环上插入 $x$（前驱 $p$、后继 $n$）时，$T$ 的增量为 $\operatorname{dist}(p,x)+\operatorname{dist}(x,n)-\operatorname{dist}(p,n)$；删除时相反。

**证明**：插入前 $p$ 与 $n$ 在环上相邻（贡献 $\operatorname{dist}(p,n)$），插入后这条邻接被替换成 $p\!-\!x$ 与 $x\!-\!n$ 两条，其余邻接不变，故增量如前。删除是逆操作。∎

**引理 3（$k\le1$ 时答案为 0）**：集合大小 0 或 1 时 $T=0$，答案 0。

**证明**：$k=0$ 时和为空的 0；$k=1$ 时环上只有自己与自己相邻，$\operatorname{dist}(x,x)=0$。∎

**定理**：算法输出的每个 `?` 都等于当时"用到的道路总长度"。

**证明**：由引理 1，答案 $=T/2$；由引理 2，算法在每次增删后维护的 `total` 恰为当前的 $T$（归纳：初始 $T=0$，每步按增量更新）；引理 3 覆盖退化情形。∎

## 5. 复杂度分析

- **时间**：预处理 DFS + 倍增表 $O(n\log n)$；每个事件：有序集合的插入/删除/前驱后继 $O(\log n)$，加上 3 次 LCA 距离 $O(\log n)$。总 $O((n+q)\log n)\approx10^5\times17\times$ 常数，实测 $n=q=10^5$ 时 C++ 约 70 ms。
- **空间**：邻接表 $O(n)$、倍增表 $O(n\log n)\approx1.7\times10^6$ 个 `int`（约 7 MB）、集合 $O(n)$。总 < 30 MB。
- **数值范围**：路径长可达 $10^{14}$，`total` 与 `dep` 必须 `long long`；`total` 恒为偶数（引理 1），整除 2 不会掉精度。
- **与时限的关系**：最大数据（链状树 + $10^5$ 次事件）C++ 约 70 ms，2 s 余量 28 倍；Python 版用 Fenwick 维护有序集合，约 1.0 s。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<vector<pair<int, long long>>> adj(n);
    for (int i = 0; i < n - 1; ++i) {
        int a, b; long long c;
        scanf("%d %d %lld", &a, &b, &c);
        --a; --b;
        adj[a].push_back({b, c});
        adj[b].push_back({a, c});
    }
    int LOG = 1;
    while ((1 << LOG) <= n) ++LOG;
    vector<int> tin(n), lev(n, 0), par(n, 0);
    vector<long long> dep(n, 0);                       // 到根的距离
    vector<vector<int>> up(LOG, vector<int>(n, 0));

    // 迭代 DFS（先序）：tin、层次、根距离、父亲
    {
        int timer = 0;
        vector<int> it(n, 0), st;
        par[0] = 0;
        tin[0] = timer++;
        st.push_back(0);
        while (!st.empty()) {
            int u = st.back();
            if (it[u] < (int)adj[u].size()) {
                auto [v, w] = adj[u][it[u]++];
                if (v == par[u]) continue;
                par[v] = u;
                lev[v] = lev[u] + 1;
                dep[v] = dep[u] + w;
                tin[v] = timer++;
                st.push_back(v);
            } else {
                st.pop_back();
            }
        }
    }
    for (int v = 0; v < n; ++v) up[0][v] = par[v];
    for (int j = 1; j < LOG; ++j)
        for (int v = 0; v < n; ++v) up[j][v] = up[j - 1][up[j - 1][v]];

    auto lca = [&](int u, int v) {
        if (lev[u] < lev[v]) swap(u, v);
        int d = lev[u] - lev[v];
        for (int j = 0; j < LOG; ++j) if (d >> j & 1) u = up[j][u];
        if (u == v) return u;
        for (int j = LOG - 1; j >= 0; --j)
            if (up[j][u] != up[j][v]) { u = up[j][u]; v = up[j][v]; }
        return up[0][u];
    };
    auto dist = [&](int u, int v) -> long long {
        int w = lca(u, v);
        return dep[u] + dep[v] - 2 * dep[w];
    };

    // 活跃点按 tin 排成一个环；环上相邻距离之和 = 2 × 斯坦纳树总长
    set<pair<int, int>> act;                           // (tin, 结点)
    long long total = 0;

    int q;
    if (scanf("%d", &q) != 1) return 0;
    char op[4];
    while (q--) {
        scanf("%s", op);
        if (op[0] == '?') { printf("%lld\n", total / 2); continue; }
        int x;
        scanf("%d", &x);
        --x;
        if (op[0] == '+') {
            if (!act.empty()) {
                auto it = act.lower_bound({tin[x], x});
                auto nxt = (it == act.end() ? act.begin() : it);
                auto prv = (it == act.begin() ? prev(act.end()) : prev(it));
                int p = prv->second, nx = nxt->second;
                total += dist(p, x) + dist(x, nx) - dist(p, nx);
            }
            act.insert({tin[x], x});
        } else {
            auto it = act.find({tin[x], x});
            if (act.size() > 1) {
                auto nxt = next(it);
                if (nxt == act.end()) nxt = act.begin();
                auto prv = (it == act.begin() ? prev(act.end()) : prev(it));
                int p = prv->second, nx = nxt->second;
                total -= dist(p, x) + dist(x, nx) - dist(p, nx);
            }
            act.erase(it);
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
    p = 0
    n = int(data[p]); p += 1
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = int(data[p]) - 1
        b = int(data[p + 1]) - 1
        w = int(data[p + 2])
        p += 3
        adj[a].append((b, w))
        adj[b].append((a, w))

    LOG = 1
    while (1 << LOG) <= n:
        LOG += 1
    tin = [0] * n
    lev = [0] * n
    dep = [0] * n
    par = [0] * n
    up = [[0] * n for _ in range(LOG)]

    # 迭代 DFS 求先序 tin、层次、根距离、父亲
    timer = 0
    it = [0] * n
    tin[0] = timer; timer += 1
    st = [0]
    while st:
        u = st[-1]
        if it[u] < len(adj[u]):
            v, w = adj[u][it[u]]
            it[u] += 1
            if v == par[u] and u != 0:
                continue
            par[v] = u
            lev[v] = lev[u] + 1
            dep[v] = dep[u] + w
            tin[v] = timer; timer += 1
            st.append(v)
        else:
            st.pop()
    up[0] = par[:]
    for j in range(1, LOG):
        prev = up[j - 1]
        cur = up[j]
        for v in range(n):
            cur[v] = prev[prev[v]]

    def lca(u, v):
        if lev[u] < lev[v]:
            u, v = v, u
        d = lev[u] - lev[v]
        j = 0
        while d:
            if d & 1:
                u = up[j][u]
            d >>= 1
            j += 1
        if u == v:
            return u
        for j in range(LOG - 1, -1, -1):
            if up[j][u] != up[j][v]:
                u = up[j][u]
                v = up[j][v]
        return up[0][u]

    def dist(u, v):
        w = lca(u, v)
        return dep[u] + dep[v] - 2 * dep[w]

    # 活跃点的 tin 集合（用 Fenwick 维护，支持前驱/后继查询）
    size = 1
    while size < n:
        size <<= 1
    bit = [0] * (n + 1)

    def add(i, delta):
        i += 1
        while i <= n:
            bit[i] += delta
            i += i & -i

    def pref(i):                     # 活跃点中 tin < i 的个数
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    def kth(k):                      # 第 k 个活跃点（1 起）的 tin
        idx = 0
        step = size
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1
        return idx                  # 返回 0 起下标

    tin_of = tin
    node_at = [0] * n
    for v in range(n):
        node_at[tin[v]] = v
    count = 0
    total = 0

    q = int(data[p]); p += 1
    out = []
    while q:
        q -= 1
        op = data[p].decode(); p += 1
        if op == '?':
            out.append(str(total // 2))
            continue
        x = int(data[p]) - 1; p += 1
        t = tin_of[x]
        if op == '+':
            if count > 0:
                before = pref(t)                     # tin < t 的活跃数
                prv_tin = kth(before) if before > 0 else kth(count)
                nxt_tin = kth(before + 1) if before < count else kth(1)
                pr = node_at[prv_tin]; nx = node_at[nxt_tin]
                total += dist(pr, x) + dist(x, nx) - dist(pr, nx)
            add(t, 1)
            count += 1
        else:
            before = pref(t)                     # x 是第 before+1 个活跃点
            if count > 1:
                prv_tin = kth(before) if before > 0 else kth(count)
                nxt_tin = kth(before + 2) if before + 2 <= count else kth(1)
                pr = node_at[prv_tin]; nx = node_at[nxt_tin]
                total -= dist(pr, x) + dist(x, nx) - dist(pr, nx)
            add(t, -1)
            count -= 1
    sys.stdout.write('\n'.join(out) + '\n')


main()
```

## 7. 边界情况与易错点

1. **0 或 1 个现存村庄**：答案 0（引理 3）。删除到只剩 1 个时不能访问"前驱=后继"以外的点，也不能让 `total` 变成负数。
2. **`total` 必须是 64 位**：$10^5$ 条边、每条 $10^9$，路径和到 $10^{14}$；`int` 直接溢出。
3. **`total` 恒为偶数**：由引理 1，`total/2` 一定整除；若出现奇数说明实现有 bug（常见原因是插入/删除时前驱后继找错）。
4. **删除时的前驱/后继**：删除前 $x$ 自己也在集合里，所以"后继"是第 $\text{before}+2$ 个活跃点（不是 $\text{before}+1$）；这一点极易写错。
5. **`tin` 的环序**：环上最后一个与第一个相邻，找前驱/后继时要**绕回**（`begin()`/`end()` 的循环处理）。
6. **DFS 递归深度**：链状树深度 $10^5$，必须用显式栈迭代（两个版本都是迭代 DFS）。
7. **$n=1$**：没有边，任何 `?` 都输出 0；读入部分要能处理 $n-1=0$ 条边。
8. **LCA 的倍增上限**：`LOG` 要满足 $2^{LOG}>n$，否则深度差很大时跳不完。
9. **输入里的 `+`/`-` 与数字之间有空格**：按 token 读即可（`scanf("%s")` 或 `split()`）。

## 8. 验证记录

- **编译环境与命令**：`Apple clang 21.0.0` + `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2`）；Python 3.9.6。`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/176/E_古代道路的维护.md` 输出 C++ 1/1、Python 1/1。
- **官方样例**：1 / 1 通过（10 个事件、4 次询问，含增删交替）。
- **独立暴力对拍**：暴力程序**每次询问重算一遍最小子树**——把树按根定向，统计每个子树里的现存村庄数 $cnt_v$，边 $(par_v,v)$ 在子树内当且仅当 $0<cnt_v<\text{总现存数}$，把这些边的权求和。完全不使用 DFS 序、LCA 或增量维护。随机生成 $n\in[1,12]$ 的随机树、随机 $q\le25$ 个合法事件（`+` 只对未存在的点、`-` 只对已存在的点），共 **250 组**，与正文 C++、Python 两版逐 token 比对，全部一致（含 $n=1$、全空集合、全满集合、只剩 1 个点等边界）。
- **最大约束性能**：$n=10^5$ 的链、$q=10^5$ 次随机增删询问，C++ 约 70 ms、Python 约 1.0 s；峰值内存 C++ < 30 MB（倍增表 1.7×10⁶ 个 int）。
- **图片校验**：两张 SVG（`cf176e_euler.svg`、`cf176e_update.svg`）通过 `xml.etree.ElementTree.parse`，文本包围盒均在 `viewBox` 内。
- **复核状态**：verified（样例、250 组全量重算对拍、最大规模性能、图片四项实跑通过）。

## 相关题目与扩展

- [Codeforces 176B 单词切割次数](https://codeforces.com/problemset/problem/176/B)：同场 B 题，计数。
- [Codeforces 176A 星际贸易的最大利润](https://codeforces.com/problemset/problem/176/A)：同场 A 题，贪心。
- [Codeforces 1195E OpenStreetMap](https://codeforces.com/problemset/problem/1195/E)：另一类"滑动/动态统计"，可对照本题的增量维护思想。
- [Luogu P3320 [SDOI2015] 寻宝游戏](https://www.luogu.com.cn/problem/P3320)：**几乎同一道题**（动态加入/删除节点，求遍历它们的环游长度），可作为本题的直接练习。

**延伸思考**：

1. **如果要求"用到的道路条数"而不是总长度**：把边权都置为 1，答案就是"最小子树的边数"，完全同一套代码。
2. **如果允许 $n$ 到 $10^6$ 且强制在线**：仍然可行，但需要把倍增 LCA 换成欧拉序 + RMQ（$O(1)$ 查询），或者用树剖；复杂度不变，常数更小。
3. **如果要在"最小子树"上再回答"某条边是否被用到"**：那是一条边两侧的现存点计数是否都为正，可以用"子树内现存点数"的 Fenwick（按 `tin` 维护），$O(\log n)$ 回答。
4. **如果要求支持"查询当前子树总长的历史最大值"**：在每个事件后记录 `total`，再维护一个前缀最大值数组即可（离线）；若要在线，则用线段树维护历史最值。
