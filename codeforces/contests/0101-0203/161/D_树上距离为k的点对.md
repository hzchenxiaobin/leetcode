# Codeforces 161D 树上距离为 k 的点对 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/161/D
- **比赛来源**：VK Cup 2012 Round 1 · Problem D（UTC 2012-03-11）
- **难度**：1800
- **标签**：树、DP、点分治
- **评测类型**：普通
- **限制**：时间 3 s / 内存 512 MB

**题意**：$n$ 个点的树，求距离恰为 $k$ 的无序点对数。

**约束**：$n\le50000$，$k\le500$：树形 DP，$O(nk)$。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
5 2
1 2
2 3
3 4
2 5

输出：
4
```

距离 2 的点对：$(1,3),(1,5),(3,5),(4,2)$ ✓（注意 $(2,4)$ 距离 2 也算——共 4 对）

官方样例 2（输入 / 输出原样）：

```text
输入：
5 3
1 2
2 3
3 4
4 5
输出：
2
```

![dp[u][d] 与子树的合并](../../../images/cf161d_dp.svg)

**观察**：设 $dp[u][d]$ = 以 $u$ 为根的子树中，与 $u$ 距离为 $d$ 的点数。合并孩子 $v$ 时：跨子树的点对距离 = $d_1+d_2$（$d_1$ 在已合并部分、$d_2$ 在 $v$ 的子树），故新增 $dp[u][d]\cdot dp[v][K-1-d]$ 之和；然后把 $dp[v][\cdot]$ 平移一位并入 $dp[u][\cdot]$。

## 3. 解题思路

1. 任选根（1），后序 DFS；
2. 每个点 $dp[u][0]=1$；对每个孩子 $v$：先累加 $\sum_{d}dp[v][d]\cdot dp[u][K-1-d]$，再对 $d$ 做 $dp[u][d+1]+=dp[v][d]$；
3. 输出累加值。

![样例 1：距离 2 的四对](../../../images/cf161d_sample.svg)

## 4. 正确性证明

**引理 1（$dp$ 语义）**：合并完若干孩子后，$dp[u][d]$ 等于"这些孩子子树 ∪ $\{u\}$"中与 $u$ 距离为 $d$ 的点数。

**证明**：归纳。初始 $dp[u][0]=1$ ✓；并入孩子 $v$ 时，$v$ 子树中与 $u$ 距离为 $d+1$ 的点恰是 $v$ 子树中与 $v$ 距离为 $d$ 的点（唯一路径经过边 $uv$）⇒ 平移一位并入 ✓ ∎

**引理 2（计数不重不漏）**：合并孩子 $v$ 时，新增的点对恰是"一个点在已合并部分、另一个在 $v$ 子树"且距离为 $K$ 的那些。

**证明**：设已合并部分中的点 $x$ 距 $u$ 为 $d$，$v$ 子树中的点 $y$ 距 $v$ 为 $d'$，则 $dist(x,y)=d+1+d'$（路径必须经过 $u,v$）⇒ 等于 $K$ ⟺ $d+d'=K-1$ ✓ 程序按 $dp[u][d]\cdot dp[v][K-1-d]$ 累加 ✓ 每对恰好在其 LCA 处被计一次（当 $v$ 是包含较后加入的那个点的孩子时）∎

**定理**：程序输出正确。

**证明**：由引理 2，所有点对在合并时被计数一次且仅一次（按 LCA 分类），距离条件由引理 2 的等式保证；由引理 1 的 $dp$ 正确性，累加结果准确 ✓ ∎

## 5. 复杂度分析

- **时间**：每个点对每个孩子做 $O(K)$ 转移 ⇒ $O(nK)\le2.5\times10^7$，实测约 62 ms。
- **空间**：$O(nK)$ 的 `long long` ≈ 200 MB（512 MB 内）——若需省内存可用 `int`+滚动，或按点开 `vector`。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXK = 505;
vector<int> g[50005];
ll dp[50005][MAXK];
ll ans = 0;
int n, K;
void dfs(int u, int par) {
    dp[u][0] = 1;
    for (int v : g[u]) {
        if (v == par) continue;
        dfs(v, u);
        for (int d = 0; d < K; d++)
            if (dp[v][d])
                ans += dp[v][d] * dp[u][K - 1 - d];
        for (int d = 0; d + 1 <= K; d++) dp[u][d + 1] += dp[v][d];
    }
}
int main() {
    if (scanf("%d %d", &n, &K) != 2) return 0;
    for (int i = 0; i < n - 1; i++) {
        int a, b; scanf("%d %d", &a, &b);
        g[a].push_back(b); g[b].push_back(a);
    }
    dfs(1, 0);
    printf("%lld\n", ans);
    return 0;
}
```

### Python3

```python
import sys
def main():
    data = sys.stdin.read().split()
    n, K = int(data[0]), int(data[1])
    g = [[] for _ in range(n + 1)]
    p = 2
    for _ in range(n - 1):
        a = int(data[p]); b = int(data[p + 1]); p += 2
        g[a].append(b); g[b].append(a)
    ans = 0
    sys.setrecursionlimit(300000)
    dp = [[0] * (K + 1) for _ in range(n + 1)]
    # 迭代后序 DFS
    order = []
    par = [0] * (n + 1)
    stack = [1]
    par[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if v != par[u]:
                par[v] = u
                stack.append(v)
    for u in reversed(order):
        dp[u][0] = 1
        for v in g[u]:
            if v == par[u]:
                continue
            for d in range(K):
                if dp[v][d]:
                    ans += dp[v][d] * dp[u][K - 1 - d]
            for d in range(K):
                dp[u][d + 1] += dp[v][d]
    print(ans)
main()
```

## 7. 边界情况与易错点

1. **$K-1-d$ 的下标**：必须 $0\le K-1-d<K$，即 $d\le K-1$。
2. **先统计后合并**：顺序反了会把同一子树内的点对算进来（会多数）。
3. **无序对**：每个点对只在 LCA 处计一次，不必再除以 2。
4. **$n=1$**：答案 0。
5. **链状树**：递归深度 $5\times10^4$，C++ 需注意栈，Python 用迭代后序。
6. **结果范围**：最多 $\binom{n}{2}\approx1.25\times10^9$，用 64 位更稳。
7. **内存**：$nK$ 个 `long long` 约 200 MB，注意 512 MB 限制。
8. **$K>n-1$**：答案为 0（DP 自然给出）。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/161/D_树上距离为k的点对.md`
- **官方样例**：$2/2$ 通过（`4`、`2`），C++ 与 Python 一致。
- **独立对拍**：另写"从每个点 BFS 求全源距离、统计距离恰为 $K$ 的无序对"的暴力，对 $200$ 组随机树（$n\le9$、$K\le4$）比较，全部一致。
- **性能**：$n=50000,K=500$ 随机树 62 ms、链 55 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 161C Abracadabra](https://codeforces.com/problemset/problem/161/C)：同场 C 题。
- [Codeforces 161E Polycarpus the Safecracker](https://codeforces.com/problemset/problem/161/E)：同场 E 题。
- [Luogu P3806 点分治模板](https://www.luogu.com.cn/problem/P3806)：距离为 $k$ 的点对（多组询问）。

**延伸思考**：

1. **若 $k$ 很大（如 $10^9$）**：$O(nk)$ 不可行，需要点分治 + 双指针（$O(n\log n)$）。
2. **若带边权**：DP 的"平移一位"变成"按边权平移"。
3. **若要求距离 ≤ k**：把等式换成前缀和。
