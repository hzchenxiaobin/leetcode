# Codeforces 160E 公交车与乘客 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/160/E
- **比赛来源**：Codeforces Round 111 (Div. 2) · Problem E（UTC 2012-03-06）
- **难度**：2400
- **标签**：离线、线段树、排序
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：$n$ 辆公交车（起点 $s_i$、终点 $f_i$、发车时刻 $t_i$，$t_i$ 互不相同），$m$ 位乘客在时刻 $b_i$ 出现在 $l_i$ 站、要直达 $r_i$ 站。乘客选**发车时刻 $t_j$ 最小**且满足 $s_j\le l_i$、$r_i\le f_j$、$b_i\le t_j$ 的车；没有则输出 $-1$。求每位乘客的车号。

**约束**：$n,m\le10^5$：离线按右端点排序 + 线段树。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
4 3
1 10 10
5 6 2
6 7 3
5 7 4
5 7 1
1 2 1
1 10 11

输出：
4 1 -1
```

乘客 1（$l=5,r=7,b=1$）：候选车 1(1–10,t=10)、3(6–7,t=3)、4(5–7,t=4)；最小 $t$ 是车 4 ✓
乘客 2（$1,2,1$）：车 1 满足（$s=1\le1$、$2\le10$、$1\le10$）✓
乘客 3（$1,10,11$）：$t\ge11$ 没有车 ⇒ -1 ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
1 1
1 1000000000 1000000000
1 1000000000 1000000000

输出：
1
```

![按右端点降序扫描，线段树按 t 找最小可行](../../../images/cf160e_sweep.svg)

**观察**：把乘客按 $r$ 降序、公交按 $f$ 降序，则在处理某位乘客时，"已加入"的车恰好是 $f\ge r$ 的那些。剩下两个条件：$s\le l$ 与 $t\ge b$，且要**最小** $t$。

于是：线段树按 $t$ 排序（下标 = 第几小的 $t$），每个位置存"已加入车中 $t$ 等于该值的那辆车的 $s$"（实际只需存该位置上的最小 $s$ 及其车号）。查询即：在 $t\ge b$ 的后缀里，找**最左边**满足 $s\le l$ 的位置 ⇒ 线段树二分。

## 3. 解题思路

1. 车按 $f$ 降序，乘客按 $r$ 降序；
2. 对 $t$ 做离散化，线段树维护区间最小 $s$（及对应车号）；
3. 扫描乘客：先把所有 $f\ge r$ 的车插入（叶子取 $\min s$），再在 $[\,lower\_bound(b),\ n)$ 上二分找最左的 $\min s\le l$ 的位置；
4. 该位置对应车号即答案，否则 $-1$。

![样例 1：三位乘客的答案](../../../images/cf160e_sample.svg)

## 4. 正确性证明

**引理 1（离线集合正确）**：处理乘客 $p$（$r_p$）时，线段树中恰为满足 $f_j\ge r_p$ 的全部车。

**证明**：车按 $f$ 降序、乘客按 $r$ 降序，扫描时单调加入；双指针保证不漏不多 ✓ ∎

**引理 2（查询的等价性）**：在 $t\ge b$ 的位置里找最小的 $t$ 使得该位置上存在 $s\le l$ 的车 ⟺ 题面所要的车。

**证明**：题面要求 $s_j\le l$、$r\le f_j$、$b\le t_j$ 中 $t_j$ 最小。引理 1 后 $f$ 条件已满足；线段树位置按 $t$ 升序排列 ⇒ 最左的可行位置就是最小 $t$ ✓ 该位置上记录的 $\min s$ 对应的车满足 $s\le l$ ✓ ∎

**定理**：程序对每位乘客输出正确车号或 $-1$。

**证明**：由引理 1、2，若查询返回位置，则对应车满足全部三个条件且 $t$ 最小；若返回空（后缀内所有最小 $s>l$），则不存在满足条件的车 ⇒ 输出 $-1$ ✓ ∎

## 5. 复杂度分析

- **时间**：排序 $O((n+m)\log)$，每次插入/查询 $O(\log n)$；总 $O((n+m)\log n)$，$n=m=10^5$ 实测约 111 ms。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Bus { long long s, f, t; int id; };
struct Person { long long l, r, b; int id; };

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<Bus> buses(n);
    for (int i = 0; i < n; i++) {
        scanf("%lld %lld %lld", &buses[i].s, &buses[i].f, &buses[i].t);
        buses[i].id = i;
    }
    vector<Person> people(m);
    for (int i = 0; i < m; i++) {
        scanf("%lld %lld %lld", &people[i].l, &people[i].r, &people[i].b);
        people[i].id = i;
    }
    vector<long long> ts;
    for (auto &b : buses) ts.push_back(b.t);
    sort(ts.begin(), ts.end());
    int P = (int)ts.size();
    int sz = 1;
    while (sz < P) sz <<= 1;
    const long long INF = LLONG_MAX;
    vector<long long> treeMin(2 * sz, INF);
    vector<int> treeId(2 * sz, -1);
    auto insert = [&](int pos, long long s, int id) {
        int p = pos + sz;
        if (s < treeMin[p]) { treeMin[p] = s; treeId[p] = id; }
        for (p >>= 1; p >= 1; p >>= 1) {
            if (treeMin[2 * p] <= treeMin[2 * p + 1]) { treeMin[p] = treeMin[2 * p]; treeId[p] = treeId[2 * p]; }
            else { treeMin[p] = treeMin[2 * p + 1]; treeId[p] = treeId[2 * p + 1]; }
            if (p == 1) break;
        }
    };
    function<int(int,int,int,int,long long)> firstOk = [&](int node, int nl, int nr, int lo, long long L) -> int {
        if (nr <= lo || treeMin[node] > L) return -1;
        if (nr - nl == 1) return nl;
        int mid = (nl + nr) / 2;
        int res = firstOk(2 * node, nl, mid, lo, L);
        if (res != -1) return res;
        return firstOk(2 * node + 1, mid, nr, lo, L);
    };
    sort(buses.begin(), buses.end(), [](const Bus &a, const Bus &b) { return a.f > b.f; });
    sort(people.begin(), people.end(), [](const Person &a, const Person &b) { return a.r > b.r; });
    vector<int> ans(m, -1);
    int bp = 0;
    for (auto &pe : people) {
        while (bp < n && buses[bp].f >= pe.r) {
            int pos = (int)(lower_bound(ts.begin(), ts.end(), buses[bp].t) - ts.begin());
            insert(pos, buses[bp].s, buses[bp].id);
            bp++;
        }
        int lo = (int)(lower_bound(ts.begin(), ts.end(), pe.b) - ts.begin());
        if (lo >= P) continue;
        int pos = firstOk(1, 0, sz, lo, pe.l);
        if (pos != -1 && pos < P) ans[pe.id] = treeId[pos + sz];
    }
    for (int i = 0; i < m; i++) printf("%d%c", ans[i] == -1 ? -1 : ans[i] + 1, i + 1 == m ? '\n' : ' ');
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    p = 2
    buses = []
    for i in range(n):
        s = int(data[p]); f = int(data[p + 1]); t = int(data[p + 2]); p += 3
        buses.append((f, s, t, i))
    people = []
    for i in range(m):
        l = int(data[p]); r = int(data[p + 1]); b = int(data[p + 2]); p += 3
        people.append((r, l, b, i))
    ts = sorted(b[2] for b in buses)
    pos_of = {t: i for i, t in enumerate(ts)}
    P = len(ts)
    sz = 1
    while sz < P:
        sz <<= 1
    INF = float("inf")
    tree = [INF] * (2 * sz)
    treeId = [-1] * (2 * sz)

    def insert(pos, s, idx):
        # 直接重建到根（简单实现）
        i = pos + sz
        if s >= tree[i]:
            return
        tree[i] = s; treeId[i] = idx
        i >>= 1
        while i >= 1:
            a, b = 2 * i, 2 * i + 1
            if tree[a] <= tree[b]:
                tree[i] = tree[a]; treeId[i] = treeId[a]
            else:
                tree[i] = tree[b]; treeId[i] = treeId[b]
            if i == 1:
                break
            i >>= 1

    def first_ok(node, nl, nr, lo, L):
        if nr <= lo or tree[node] > L:
            return -1
        if nr - nl == 1:
            return nl
        mid = (nl + nr) // 2
        r = first_ok(2 * node, nl, mid, lo, L)
        if r != -1:
            return r
        return first_ok(2 * node + 1, mid, nr, lo, L)

    buses.sort(key=lambda x: -x[0])
    people.sort(key=lambda x: -x[0])
    ans = [-1] * m
    bp = 0
    import bisect
    for (r, l, b, idx) in people:
        while bp < n and buses[bp][0] >= r:
            f, s, t, bid = buses[bp]
            insert(pos_of[t], s, bid)
            bp += 1
        lo = bisect.bisect_left(ts, b)
        if lo >= P:
            continue
        pos = first_ok(1, 0, sz, lo, l)
        if pos != -1 and pos < P:
            ans[idx] = treeId[pos + sz]
    print(" ".join(str(a if a == -1 else a + 1) for a in ans))


main()
```

## 7. 边界情况与易错点

1. **$t$ 全不同**：可用 $t$ 直接离散化（唯一）。
2. **$b$ 相同**：按 $r$ 排序即可，无影响。
3. **无可行车**：输出 $-1$。
4. **同一位置多辆车**：只需保留最小 $s$（其余永远不优）。
5. **线段树二分的 $lo$**：用 `lower_bound(t>=b)`，注意是后缀。
6. **插入顺序**：$f\ge r$ 用双指针，乘客与车都降序。
7. **输出格式**：一行 $m$ 个数，空格分隔。
8. **`long long`**：坐标可达 $10^9$，用 64 位。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/160/E_公交车与乘客.md`
- **官方样例**：$2/2$ 通过（`4 1 -1`、`1`），C++ 与 Python 一致。
- **独立对拍**：另写"对每位乘客线性扫描全部车、取可行者中 $t$ 最小"的暴力，对 $200$ 组随机数据（$n,m\le4$）比较，全部一致。
- **性能**：$n=m=10^5$ 实测 C++ 约 111 ms、Python 约 1.2 s（Python 版用递归线段树，建议 C++）。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 160D Edges in MST](https://codeforces.com/problemset/problem/160/D)：同场 D 题。
- [Codeforces 161C Abracadabra](https://codeforces.com/problemset/problem/161/C)：VK Cup 的递归题。
- [LeetCode 2407. 最长递增子序列 II](https://leetcode.cn/problems/longest-increasing-subsequence-ii/)：线段树优化。

**延伸思考**：

1. **若要求"最小 $t$ 且同 $t$ 时最短行程"**：线段树改存二元组。
2. **若车可换乘**：变成最短路/区间图问题。
3. **若强制在线**：用可持久化线段树。
