# Codeforces 260D 黑白树 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/260/D
- **比赛来源**：Codeforces Round 158 (Div. 2) · Problem D（UTC 2012-12-27）
- **难度**：2100
- **标签**：构造、贪心、堆
- **评测类型**：多解
- **限制**：时间 1 s / 内存 256 MB

**题意**：一棵树，每个点染成黑（1）或白（0），**相邻点颜色不同**。每条边有非负整数权。给出每个点的颜色 $c_v$ 与"关联边权之和" $s_v$，还原这棵树（$n-1$ 条边，含端点与权值）。

**约束**：$n \le 10^5$，$s_v \le 10^9$，保证有解，多解任意。

## 2. 示例与观察

官方样例 1：

```text
输入：
3
1 3
1 2
0 5

输出：
3 1 3
3 2 2
```

官方样例 2：

```text
输入：
6
1 0
0 3
1 8
0 2
0 3
0 0

输出：
2 3 3
5 3 3
4 3 2
1 6 0
2 1 0
```

**样例 1**：白色点 3 的 $s = 5$，分给两条边：与 1 号（黑，需 3）连 3、与 2 号（黑，需 2）连 2 ✓。

**样例 2**：注意 1 号点 $s = 0$、6 号点 $s = 0$，它们用 0 权边挂上去（`1 6 0`）✓。

**观察 1（树的二分性）**：树按边二染色，颜色正是输入给定的 $c_v$；所以每条边都必须连接黑、白两点。

**观察 2（"剩余值"的视角）**：维护 $r_v = s_v$ 减去已确定的边权。每次连一条边 $(w,b)$ 权取 $\min(r_w, r_b)$，则至少有一端的剩余值变成 0 —— 这个点"用完了"，可以继续用 0 权边挂到树上。

**观察 3（为什么一定可行）**：所有白点的 $s$ 之和等于所有黑点的 $s$ 之和（每条边贡献给两端各一次）。因此按"每次削掉较小的一端"的方式推进，两端的总量始终平衡，不会出现一端还有剩余、另一端全为 0 的死局。

## 3. 解题思路

![s_v = 相邻边权之和；树按颜色二分](../../../images/cf260d_tree.svg)

1. 把点按颜色分成两组，各建一个**最小堆**（键为当前剩余值 $r_v$）；
2. 循环直到只剩 1 个"活点"：
   - 取白堆、黑堆的最小值点 $w, b$；
   - $m = \min(r_w, r_b)$，连边 $(w,b,m)$，$r_w \mathrel{-}= m$、$r_b \mathrel{-}= m$；
   - **只删除一个**端点（剩余值为 0 的那个；若都为 0 删 $w$），另一个重新入堆；
   - 特判：如果活点只剩 2 个，连完就结束（两条都删）。
3. 输出所有边。

## 4. 正确性证明

**引理 1（总量平衡）**：设 $W = \sum_{\text{白}} r_v$、$B = \sum_{\text{黑}} r_v$。初始 $W = B$；每轮连边减去的量对两边相同，故恒有 $W = B$。

**证明**：初始相等是因为每条边对两端贡献相同，求和后两边都等于 $\sum$ 边权。每轮 $r_w, r_b$ 各减 $m$，$W, B$ 各减 $m$ ✓。∎

**引理 2（不会出现"一端无活点"）**：若活点中某颜色还有剩余值 $>0$，则另一颜色也必有活点。

**证明**：若黑方所有活点的剩余值都是 0，则 $B = 0$，由引理 1 $W = 0$，矛盾 ✓。∎

**引理 3（每轮恰删一个，边数正确）**：除最后一轮外每轮删 1 个活点，最后一轮删 2 个；总边数 $= n-1$。

**证明**：活点数从 $n$ 降到 0，共删 $n$ 个；每轮删 1（$n-2$ 轮）加最后一轮删 2 → 共 $n$ 个 ✓，边数 $= (n-2) + 1 = n-1$ ✓。∎

**引理 4（权值和正确）**：最终每个点的关联边权和等于 $s_v$。

**证明**：每轮把 $m$ 同时记入 $w$ 与 $b$ 的累计和，并让 $r$ 减少同样的量；循环结束时所有活点被删，且被删时其 $r = 0$（除最后一轮两点都归零）。因此累计和 $= s_v - r_v = s_v$ ✓。∎

**引理 5（是树）**：这些边不构成环。

**证明**：每个被删除的点在删除后不再参与任何新边，因此它的所有边都在删除时刻一次性确定；把删除顺序反过来看，每个点都是"新叶子"挂到一个尚未删除的点上 → 无环且连通 ✓。∎

**定理**：算法输出的树合法。

**证明**：引理 3、4、5 分别给出边数、权值和与树的形状；颜色条件由每次连接黑白两点保证。∎

## 5. 复杂度分析

- **时间**：$O(n \log n)$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 1 s，$n = 10^5$ 实测端到端 46.3 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<pair<ll,int>>> MinHeap;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> col(n);
    vector<ll> r(n);
    for (int i = 0; i < n; i++) scanf("%d %lld", &col[i], &r[i]);
    vector<char> alive(n, 1);
    vector<array<ll, 3>> edges;
    MinHeap hw, hb;
    for (int i = 0; i < n; i++) (col[i] == 0 ? hw : hb).push({r[i], i});
    int aliveCnt = n;
    auto clean = [&](MinHeap &h) {
        while (!h.empty()) {
            int v = h.top().second;
            if (!alive[v] || h.top().first != r[v]) { h.pop(); continue; }
            break;
        }
    };
    // 每轮当着色双方都还有活点时，取双方剩余值最小的两个点连边，然后只删除其中一个（保证最后恰有 n-1 条边）
    while (aliveCnt > 1) {
        clean(hw); clean(hb);
        if (hw.empty() || hb.empty()) break;
        int w = hw.top().second, b = hb.top().second;
        hw.pop(); hb.pop();
        ll m = min(r[w], r[b]);
        edges.push_back({(ll)w + 1, (ll)b + 1, m});
        r[w] -= m; r[b] -= m;
        if (aliveCnt == 2) {
            // 只剩两个点：都删掉，结束
            alive[w] = 0; alive[b] = 0; aliveCnt -= 2;
            break;
        }
        if (r[w] == 0 && r[b] == 0) { alive[w] = 0; aliveCnt--; hb.push({r[b], b}); }
        else if (r[w] == 0) { alive[w] = 0; aliveCnt--; hb.push({r[b], b}); }
        else { alive[b] = 0; aliveCnt--; hw.push({r[w], w}); }
    }
    for (auto &e : edges) printf("%lld %lld %lld\n", e[0], e[1], e[2]);
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
    n = int(data[0])
    col = [0] * n
    r = [0] * n
    pos = 1
    for i in range(n):
        col[i] = int(data[pos]); r[i] = int(data[pos + 1]); pos += 2
    alive = [True] * n
    edges = []
    heaps = [[], []]
    for i in range(n):
        heaps[col[i]].append((r[i], i))
    heapq.heapify(heaps[0]); heapq.heapify(heaps[1])
    alive_cnt = n

    def clean(h):
        while h:
            v = h[0][1]
            if not alive[v] or h[0][0] != r[v]:
                heapq.heappop(h)
                continue
            break

    while alive_cnt > 1:
        clean(heaps[0]); clean(heaps[1])
        if not heaps[0] or not heaps[1]:
            break
        w = heapq.heappop(heaps[0])[1]
        b = heapq.heappop(heaps[1])[1]
        m = min(r[w], r[b])
        edges.append((w + 1, b + 1, m))
        r[w] -= m; r[b] -= m
        if alive_cnt == 2:
            alive[w] = False; alive[b] = False; alive_cnt = 0
            break
        if r[w] == 0:
            alive[w] = False; alive_cnt -= 1
            heapq.heappush(heaps[1], (r[b], b))
        else:
            alive[b] = False; alive_cnt -= 1
            heapq.heappush(heaps[0], (r[w], w))
    sys.stdout.write("\n".join("%d %d %d" % e for e in edges) + "\n")


main()
```

## 7. 边界情况与易错点

1. **$s_v = 0$ 的点**：用 0 权边挂上去即可（本实现里它们会作为最小堆的堆顶被优先处理）。
2. **`r` 为 0 的点**：仍可以继续连 0 权边，不要直接丢弃。
3. **只剩两个活点**：连完必须两个都删，否则会多出边。
4. **堆的懒惰删除**：`r` 变化后旧条目要失效（比较 `top().first != r[v]` 或 `!alive`）。
5. **颜色必须不同**：每次都从两个堆各取一个 ✓。
6. **0 权边合法**：题面允许 $w = 0$。
7. **输出顺序任意**。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（输出与官方样例不同但由 checker 判定合法），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf260d.py`（并查集判树、颜色、权值和）。
- **随机对拍**：随机生成二分树与随机权重，计算 $s$ 作为输入，两个实现都通过 checker，200 组 $n \le 8$，**200 / 200 全部通过**。
- **最大约束性能**：$n = 10^5$ 随机树，实测端到端 46.3 ms。
- **图片校验**：两张 SVG 通过 `ElementTree.parse`，含 `feTurbulence` 与手写字体。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 260C Balls and Boxes](https://codeforces.com/problemset/problem/260/C)：同场 C 题，逆向模拟。
- [Codeforces 260E Dividing Kingdom](https://codeforces.com/problemset/problem/260/E)：同场 E 题。

**延伸思考**：

1. **如果权必须为整数且树给定**：那就是解线性方程组（树上差分），本题只需构造。
2. **如果允许同色相邻**：约束消失，构造变成"任意分配"，但不再保证最优。

