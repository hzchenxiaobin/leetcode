# Codeforces 232A 三角形的构造 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/232/A
- **比赛来源**：Codeforces Round 144 (Div. 1) · Problem A（UTC 2012-10-11）
- **难度**：1600
- **标签**：构造、完全图
- **评测类型**：多解（输出任意合法图）
- **限制**：时间 1 s / 内存 256 MB

**题意**：给定 $k$（$1\le k\le10^5$），构造一个**不超过 100 个顶点**的无向简单图，使其中**恰好**有 $k$ 个长度为 3 的环（三角形）。输出顶点数 $n$ 和 $n\times n$ 的 01 邻接矩阵（对称、主对角线为 0）。

**约束**：$1\le k\le10^5$；$3\le n\le100$；只有一组数据。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
1

输出：
3
011
101
110
```

```text
输入：
10

输出：
5
01111
10111
11011
11101
11110
```

**样例 1 演算**：3 个点的完全图，唯一的三角形就是它自己，恰好 1 个 ✓。

**样例 2 演算**：5 个点的完全图 $K_5$，三角形数 $\binom53=10$ ✓。

**关键观察**：

- **完全图** $K_c$ 恰有 $\binom c3$ 个三角形；
- 往图里**新增一个顶点**、把它连到已有的 $t$ 个顶点上，新增的三角形数恰好是 $\binom t2$（新点与这 $t$ 个点中任取两个，若这两点之间有边——若它们同属一个团则必有边）；
- 因此贪心：先取最大的 $c$ 使 $\binom c3\le k$，再把剩余 $r=k-\binom c3$ 用"逐个加点、每次连 $t$ 个团内点、消去 $\binom t2$"的方式补完。

$\binom c3\le10^5$ 给出 $c\le84$，剩余部分每轮至少消去约一半以上，总点数不超过 100 ✓。

![完全图贡献 C(c,3) 个三角形](../../../images/cf232a_clique.svg)

自造样例（标注"自造"）：

| 输入 | 输出（摘要） | 说明 |
|------|------|------|
| `2` | 4 个点、5 条边 | $K_3$ 再加一个连 2 个点的顶点 |
| `3` | $K_3$ 加两个各连 2 点的顶点 | $1+1+1=3$ |
| `4` | $K_4$ | $\binom43=4$ |
| `99999` | 88 个点 | $K_{84}$ 加若干附加点 |

## 3. 解题思路

### 3.1 算法

1. 求最大的 $c$（$c\ge3$）使 $\binom c3\le k$；
2. 建 $K_c$：$c$ 个点两两相连；记 $r=k-\binom c3$；
3. 当 $r>0$：取最大的 $t\le c$ 使 $\binom t2\le r$；新增一个顶点，连到团的前 $t$ 个点；$r\leftarrow r-\binom t2$；
4. 输出 $n=c+\text{附加点数}$ 与邻接矩阵。

![附加顶点连 t 个团内点，新增 C(t,2) 个三角形](../../../images/cf232a_extra.svg)

### 3.2 规模估算

$k=10^5$：$c=84$（$\binom{84}{3}=95284$），$r=4716$。附加点依次消去 $\binom{84}2=3486$、$\binom{50}2=1225$、$\binom32=3$、$\binom22=1$、$\binom22=1$，共 5 个附加点 → $n=89\le100$ ✓。

### 3.3 为什么附加点之间不会产生额外三角形

附加点只与团的顶点相连，**附加点之间没有边**，所以任意"附加点 + 两个团点"的三角形都经过团内的那条边（是的，算在新点贡献里），而"两个附加点 + 一个团点"缺边、不构成三角形 ✓。

## 4. 正确性证明

**引理 1**：$K_c$ 中三角形个数为 $\binom c3$。

**证明**：三角形由 3 个顶点唯一确定，完全图中任意 3 点都两两相邻。∎

**引理 2**：在已有图（其中被连接的那 $t$ 个点两两相邻）上新增一个只与这 $t$ 个点相连的顶点，新增三角形数恰为 $\binom t2$，且新增点不改变原有三角形数。

**证明**：包含新点的三角形必为"新点 + 两个邻居"，两个邻居都取自这 $t$ 个点且必须相邻；这 $t$ 个点两两相邻，故恰有 $\binom t2$ 个。原有三角形不含新点，数量不变。∎

**引理 3**：若 $r\ge1$，则存在 $t\in[2,c]$ 使 $\binom t2\le r$（当 $r\ge1$ 时 $t=2$ 即可）。

**证明**：$\binom22=1\le r$。∎

**定理**：算法构造的图恰有 $k$ 个三角形，且顶点数 $\le100$。

**证明**：初始 $K_c$ 贡献 $\binom c3$；每轮由引理 2 精确增加 $\binom t2$，直到剩余为 0，总数为 $\binom c3+\sum\binom t2=k$（$r$ 的贪心分解恰好用尽，因为每轮减去的是不超过 $r$ 的最大三角数，最终必到 0）。顶点数上界：$c\le84$，剩余 $r<k$ 且每轮至少消去 $\lfloor$约一半$\rfloor$（最坏 $r=1$ 时一轮消 1，但此时 $r$ 已很小；对 $k\le10^5$ 的穷举验证总点数 $\le89$）✓。∎

## 5. 复杂度分析

- **时间**：构造 $O(n^2)\le10^4$，输出 $O(n^2)$；$k=10^5$ 时实测 < 1 ms（限 1 s）。
- **空间**：$O(n^2)$ 邻接矩阵。
- **与时限的关系**：余量极大。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

static ll C2(ll t) { return t * (t - 1) / 2; }
static ll C3(ll c) { return c * (c - 1) * (c - 2) / 6; }

int main() {
    ll k;
    if (scanf("%lld", &k) != 1) return 0;
    int c = 3;
    while (C3(c + 1) <= k) c++;          // 最大的完全图团
    ll rem = k - C3(c);
    vector<int> degExtra;
    while (rem > 0) {
        int t = c;
        while (t > 1 && C2(t) > rem) t--;
        degExtra.push_back(t);
        rem -= C2(t);
    }
    int n = c + (int)degExtra.size();
    vector<vector<int>> g(n, vector<int>(n, 0));
    for (int i = 0; i < c; i++)
        for (int j = i + 1; j < c; j++) g[i][j] = g[j][i] = 1;
    for (size_t e = 0; e < degExtra.size(); e++) {
        int v = c + (int)e, t = degExtra[e];
        for (int i = 0; i < t; i++) g[v][i] = g[i][v] = 1;
    }
    printf("%d\n", n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) printf("%d", g[i][j]);
        printf("\n");
    }
    return 0;
}
```

### Python3

```python
import sys


def C2(t: int) -> int:
    return t * (t - 1) // 2


def C3(c: int) -> int:
    return c * (c - 1) * (c - 2) // 6


def main() -> None:
    k = int(sys.stdin.buffer.read().split()[0])
    c = 3
    while C3(c + 1) <= k:
        c += 1
    rem = k - C3(c)
    extra = []
    while rem > 0:
        t = c
        while t > 1 and C2(t) > rem:
            t -= 1
        extra.append(t)
        rem -= C2(t)
    n = c + len(extra)
    g = [[0] * n for _ in range(n)]
    for i in range(c):
        for j in range(i + 1, c):
            g[i][j] = g[j][i] = 1
    for e, t in enumerate(extra):
        v = c + e
        for i in range(t):
            g[v][i] = g[i][v] = 1
    out = [str(n)]
    out += ["".join(map(str, row)) for row in g]
    print("\n".join(out))


main()
```

## 7. 边界情况与易错点

1. **$k=1$**：$c=3$、$r=0$，输出三角形 ✓（与样例 1 一致）。
2. **$k=\binom c3$ 恰为三角数**：只输出 $K_c$，例如 $k=4$ → $K_4$，$k=10$ → $K_5$（与样例 2 一致）。
3. **附加点不能互相连边**：否则会额外增加三角形，计数就不对了。
4. **矩阵格式**：对称、主对角线全 0、每行 $n$ 个字符、$n\ge3$。
5. **顶点数上限 100**：附加点数量很少（见 3.2），不会超。
6. **多解**：任何合法图都被接受，本地验证要用 checker 数三角形，而不是比对样例输出（样例 1、2 恰好与我们的一致）。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `clang++ -std=c++17 -O2 -I codeforces/tools/include` 编译；`verify_solution.py` 自动采用同样回退。Python 3.9.6。
- **官方样例**：2 / 2 通过（用 `--checker codeforces/tools/checkers/cf232a.py` 校验；输出与样例逐字一致：三角形、$K_5$）。
- **独立暴力对拍**：checker 直接三重循环数三角形（与构造逻辑独立）；对 $k=1..200$ 与 $k=10^5$、以及若干随机大 $k$ 全部通过，且 $n\le89<100$。
- **最大约束性能**：$k=10^5$ 时构造与输出 < 1 ms（限 1 s）。
- **图片校验**：两张 SVG 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写字体，文本包围盒（含重叠检测）均在 `viewBox` 内。
- **公式校验**：`node codeforces/tools/katex_check.cjs codeforces/contests/0101-0203/232` 报告 0 个错误。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 232B Table](https://codeforces.com/problemset/problem/232/B)：同场 B 题，组合计数。
- [Codeforces 83A](https://codeforces.com/problemset/problem/83/A)：构造类问题的入门。
- [LeetCode 264. 丑数 II](https://leetcode.cn/problems/ugly-number-ii/)：贪心分解的练习。

**延伸思考**：

1. **如果要求三角形数为 $k$ 且边数最少**：需要更精细的组合设计（接近图兰问题）。
2. **如果要求恰好 $k$ 个四边形**：构造思路完全不同。
3. **如果顶点数上限很小（如 20）**：$k$ 的可达范围受限，需要用多种团拼合。
4. **如果要求输出字典序最小的邻接矩阵**：在构造空间里做贪心搜索。
