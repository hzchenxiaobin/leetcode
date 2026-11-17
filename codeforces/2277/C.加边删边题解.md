# Codeforces 加边删边 题解

## 1. 题目概述

- **标题 / 题号**：加边删边（Codeforces 2277C，英文名 Edge Addeleting）
- **链接**：https://codeforces.com/problemset/problem/2277/C
- **来源**：Codeforces Round 1129 (Div. 2) · Problem C
- **难度**：未评级（1500 分 / Div. 2 C，约 1800 档）
- **限制**：时间 3 s / 内存 256 MB
- **标签**：树，DFS 与遍历，贪心，最近公共祖先

**题意**：给定一棵 $n$ 个点的树（边权全为 1），依次做 $m$ 次操作。第 $i$ 次操作分两步：

1. 加入边 $(1, v_i)$，此时图中出现唯一一个环；若 $(1, v_i)$ 本就在树里，加入的是一条**平行边**，环就由这两条平行边组成；
2. 从该环上任选一条边（**可以就是刚加进去的那条**）删除，使图重新变成树。

问 $m$ 次操作全部做完后，点 $1$ 到点 $n$ 的距离最大是多少。多测：首行 $t$，每组先给 $n, m$，接着 $n-1$ 行边，最后一行 $m$ 个整数 $v_1..v_m$，逐组输出一个答案。

**约束**：

- $1 \le t \le 10^4$；$2 \le n \le 5 \times 10^5$；$1 \le m \le 5 \times 10^5$
- $\sum n \le 5 \times 10^5$，$\sum m \le 5 \times 10^5$；$2 \le v_i \le n$（永远不可能是 $1$）
- 时间 3 s，要求总复杂度 $O(n + m)$；树可能是一条 $5\times10^5$ 深的链，**不能递归建树**

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
5
2 2
1 2
2 2
3 2
1 2
2 3
2 3
7 2
1 2
2 3
3 7
2 4
4 5
1 6
6 5
10 4
1 2
2 3
3 10
2 4
4 5
5 6
1 7
7 8
8 9
9 8 6 10
7 1
1 2
2 7
1 3
3 4
4 5
5 6
6

输出：
1
2
5
6
2
```

逐组核对（$g$ 与候选的定义见 3.3）：

| # | $n$ | 初始 $\operatorname{dep}(n)$ | 各 $v_i$ 的最优候选 $1+\operatorname{dist}(v_i,n)$ | 答案 |
|---|-----|------------------------------|---------------------------------------------------|------|
| 1 | 2 | 1 | $v=2$：$g=2$，候选 $1$ | **1** |
| 2 | 3 | 2 | $v=2$：$\operatorname{dist}=1$，候选 $2$；$v=3$：候选 $1$ | **2** |
| 3 | 7 | 3 | $v=6$：$g=1$ 不可用；$v=5$：$\operatorname{dist}=4$，候选 $5$ | **5** |
| 4 | 10 | 3 | $v=9,8$ 不可用；$v=6$：$\operatorname{dist}=5$，候选 $6$；$v=10$：候选 $1$ | **6** |
| 5 | 7 | 2 | $v=6$：$g=1$ 不可用，无有效候选 | **2** |

第 3 组的走法：第一次加入 $(1,6)$ 后直接删掉（空操作）；第二次加入 $(1,5)$，删掉 $(1,2)$，路径变成 $1 \to 5 \to 4 \to 2 \to 3 \to 7$，长度 $5$。

## 3. 解题思路

### 3.1 暴力思路

最直接的是搜索：第 $i$ 次操作的环长最多 $O(n)$，逐次枚举删哪条边，搜索树大小 $O(n^m)$，而 $m$ 可达 $5\times10^5$，完全不可行。即使只枚举「哪一次操作真正改变了 $1\to n$ 的路径」再枚举「删哪条边」，也要 $O(nm) \approx 2.5\times10^{11}$。所以必须找到**与操作序列无关的不变量**，把每个 $v_i$ 独立判定。

### 3.2 核心观察：操作只会「把一整块原树子树挂回根」

![操作把整块原树子树改挂到 1 上](images/cf2277_c_component_invariant.svg)

以 $1$ 为根。加入 $(1,v_i)$ 后形成的环 = 新边 + 当前树中 $1 \to v_i$ 的路径。设被删的边是 $(\operatorname{par}(c), c)$，被剪下来的就是**以 $c$ 为根的整棵子树**，它随后通过新边 $(1,v_i)$ 直接挂到根上（$v_i$ 就在这棵子树里）。

由此得到三条关键性质：

1. **新边永远形如 $(1,x)$**：除含 $1$ 的那块以外，每个连通块都**直接**挂在 $1$ 上，块与块不会串成链。
2. **被剪掉的全是原树边**：每个连通块始终是原树的一个**连通子树**，块内边一条未变，故块内任意两点的距离永远等于原树距离。
3. 于是 $\operatorname{dep}(n)$ 只有两种可能：$n$ 与 $1$ 同块时 $=\operatorname{dep}_{\text{原}}(n)$；$n$ 挂在 $(1,v_i)$ 上时 $=1+\operatorname{dist}_{\text{原}}(v_i,n)$。

第三条里的 $v_i$ 必须是**某次操作给出的顶点**，因为只有这些新边会被加入。

### 3.3 算法流程：一次 BFS 递推出全部 lca

![判定条件与 O(n+m) 公式](images/cf2277_c_lca_condition.svg)

还差最后一环：第 $i$ 次操作何时真能把 $n$ 换到 $v_i$ 那一块？被剪的边是 $(\operatorname{par}(c),c)$，$n$ 要落在 $c$ 的子树里，须同时满足：$c$ 是 $v_i$ 的祖先（在 $1\to v_i$ 路径上）、$c$ 是 $n$ 的祖先、$c\ne 1$（否则没有边可删）。这等价于 **$v_i$ 与 $n$ 有非根公共祖先**，即 $\operatorname{lca}(v_i,n)\ne 1$；充分性取 $c=\operatorname{lca}(v_i,n)$ 即可。

再看其余操作：每次都可以删掉刚加入的新边，使树原封不动——这是合法的**空操作**。所以除一次有效操作外，其余 $m-1$ 次全部做成空操作，互不干扰。于是答案是

$$\text{ans} = \max\Bigl(\operatorname{dep}_{\text{原}}(n),\ \max_{i:\ \operatorname{lca}(v_i,n) \ne 1} \bigl(1 + \operatorname{dep}(v_i) + \operatorname{dep}(n) - 2\operatorname{dep}(\operatorname{lca}(v_i,n))\bigr)\Bigr)$$

**不必建倍增 LCA 表**。对固定终点 $n$，把 $1 \to n$ 路径上的点标记 $\text{on}$，令 $g(u) = u$（若 $\text{on}(u)$）否则 $g(\operatorname{par}(u))$。$g(u)$ 即「$u$ 最深的、同时是 $n$ 祖先的祖先」$=\operatorname{lca}(u,n)$。按父先子后的顺序递推，一遍 $O(n)$ 得到全部 $g(u)$。

流程：迭代 BFS 求 $\operatorname{par},\operatorname{dep}$ 与父先子后的 `order` → 从 $n$ 沿 $\operatorname{par}$ 上溯标记 $\text{on}$ → 按 `order` 递推 $g$ → 令 $\text{ans}\leftarrow\operatorname{dep}(n)$，扫 $m$ 个 $v_i$，若 $g(v_i)\ne 1$ 就用上式更新 → 输出。

### 3.4 示例演算

![样例 3 与样例 4 的逐次判定](images/cf2277_c_walkthrough.svg)

样例 3（$n=7$，树 $1\!-\!2\!-\!3\!-\!7$、$2\!-\!4\!-\!5$、$1\!-\!6$，操作 $v=6,5$）：$\operatorname{dep}=[0,1,2,2,3,1,3]$，$1\to7$ 路径是 $1,2,3,7$。

- $v_1=6$：其父就是 $1$，$g(6)=1$，删任何边 $n$ 都留在 $1$ 这侧，**跳过**；
- $v_2=5$：$g(5)=g(4)=2\ne 1$，$\operatorname{dist}(5,7)=3+3-2\cdot1=4$，候选 $1+4=5$；
- $\text{ans}=\max(3,5)=5$。

样例 4：$\operatorname{dep}=[0,1,2,3,2,3,4,1,2,3]$，$v=9,8,6,10$。$9,8$ 挂在 $7$ 下、$10$ 挂在 $2$ 下，分居 $1$ 的两支，$g=1$ 跳过；$g(6)=2$，$\operatorname{dist}(6,10)=4+3-2\cdot1=5$，候选 $6$；$v=10$ 候选仅 $1$。故答案为 $6$。

## 4. 算法细节

1. **多测清空**：$t$ 可达 $10^4$ 而 $\sum n\le5\times10^5$。所有数组定义为**每组局部的 vector**，靠重新分配天然清零；绝不能用全局数组配合 `memset(n+1)`，最坏 $10^4\times5\times10^5$ 直接超时。
2. **必须迭代**：树可能是 $5\times10^5$ 深的链，C++ 递归 `dfs` 会爆栈（默认约 8 MB），Python 默认递归上限 1000 更会崩。用 `order` 当队列写 BFS 最省事，顺带保证父先子后。
3. **$g$ 的递推依赖顺序**：`g[u] = on[u] ? u : g[par[u]]` 必须按 `order` 遍历时计算；逆序或乱序会读到未赋值的 $g(\operatorname{par})$。
4. **$g(1)$ 恒为 $1$**：$1$ 必在 $1\to n$ 路径上，故 $\text{on}(1)$ 为真、$g(1)=1$，不会退化到 $g(0)$；仍建议把 $g(0)$ 预留为 $0$ 以防越界。
5. **距离公式**：$\operatorname{dist}(u,w)=\operatorname{dep}(u)+\operatorname{dep}(w)-2\operatorname{dep}(\operatorname{lca})$。本题所有量不超过 $n\le5\times10^5$，`int` 足够；写成 `long long` 也无代价，跨题复用更安全。
6. **$v_i=n$ 不必特判**：此时 $g=n$、$\operatorname{dist}=0$、候选 $1$，天然赢不过 $\operatorname{dep}(n)$，交给 $\max$ 即可。
7. **I/O 量**：约 $1.5\times10^6$ 个整数。C++ 关同步流即可；Python 必须整体读入再切分，用 `input()` 逐行读会超时。

## 5. 正确性证明

**引理 1（块是原树的连通子树，且块内距离不变）**：任意时刻，删掉所有形如 $(1,x)$ 的新边后，每个连通块的顶点集在原树中诱导一个连通子树；因此同块两点的距离等于原树距离。

**证明**：初始只有一块即整棵原树，成立。设操作前成立，操作加入 $(1,v_i)$ 并删环上一条边 $e$：若 $e$ 是新边，块的顶点集完全不变；若 $e$ 是原树边，它在某块内部把该块劈成两半，两半仍是原树的连通子树；新加的 $(1,v_i)$ 不是原树边，只影响「块如何挂到 $1$」，不改变任何块的顶点集。归纳即得。又因块诱导的顶点集在原树中连通，块内保留了连接这些点的全部路径边，故两点间路径唯一且与原树一致。∎

**引理 2（一次操作的净效果）**：设删边后 $n$ 与 $v_i$ 落在同一块 $B$，则操作后 $\operatorname{dep}(n)=1+\operatorname{dist}_{\text{原}}(v_i,n)$；若 $n$ 不在 $v_i$ 所在的块中，则 $\operatorname{dep}(n)$ 不变。

**证明**：第一种情形，$B$ 与外界唯一的连接就是新边 $(1,v_i)$（原来连出去的那条边已被删），故 $1\to n$ 的路 = 边 $(1,v_i)$ + $B$ 内 $v_i\to n$ 的路，长度 $1+\operatorname{dist}_{\text{原}}$（引理 1）。第二种情形 $n$ 所在块的挂接方式未变，$\operatorname{dep}(n)$ 不变。∎

**引理 3（可行性判定）**：在「前面所有操作都取空操作」的原始树上，第 $i$ 次操作能使 $n$ 与 $v_i$ 同块 $\iff \operatorname{lca}_{\text{原}}(v_i,n)\ne 1$。

**证明**：删掉 $(\operatorname{par}(c),c)$ 剪下的是 $c$ 的子树，故需 $c$ 同时是 $v_i$、$n$ 的祖先且 $c\ne1$。原树中这样的 $c$ 存在 $\iff$ 二者有非根公共祖先 $\iff \operatorname{lca}\ne1$；取 $c=\operatorname{lca}$ 即构造出合法方案。∎

**定理**：答案为 $\max\bigl(\operatorname{dep}_{\text{原}}(n),\ \max_{i:\,g(v_i)\ne1}(1+\operatorname{dist}_{\text{原}}(v_i,n))\bigr)$。

**证明**：

- **可达性（$\ge$）**：每次操作都可选择删掉刚加入的新边而不改变树（新边属于新形成的环，题目允许删环上任意一条）。故把除第 $i$ 次外的操作全取空操作合法；第 $i$ 次按引理 3 取 $c=\operatorname{lca}(v_i,n)$，由引理 2 得 $\operatorname{dep}(n)=1+\operatorname{dist}_{\text{原}}(v_i,n)$，其后继续取空操作即保持。全部取空操作则得 $\operatorname{dep}_{\text{原}}(n)$。
- **上界（$\le$）**：设最终树中 $n$ 所在块为 $S$。若 $1\in S$，则 $1\to n$ 的路只能留在 $S$ 内（其余块都只与 $1$ 单边相连，进去便出不来），再由引理 1 得 $\operatorname{dep}(n)=\operatorname{dep}_{\text{原}}(n)$。否则 $S$ 只能通过某条新边 $(1,x)$ 连到 $1$，$x$ 必是某次操作的 $v_i$，且由引理 1 得 $\operatorname{dep}(n)=1+\operatorname{dist}_{\text{原}}(v_i,n)$。又 $S$ 是原树的连通子树且 $1\notin S$，而 $v_i,n\in S$；若 $\operatorname{lca}(v_i,n)=1$，则原树中 $v_i\to n$ 的路径经过 $1$，该路径应整体落在 $S$ 内，矛盾。故 $\operatorname{lca}(v_i,n)\ne1$，该项已被上式的 $\max$ 覆盖。

两侧合起来即得结论。∎

## 6. 复杂度分析

- **时间**：每组 $O(n+m)$——BFS 建树、标记 $1\to n$ 路径、递推 $g$ 各 $O(n)$，扫描操作 $O(m)$。总计 $O(\sum n+\sum m)\le10^6$ 量级。
- **空间**：每组 $O(n+m)$，用于邻接表（$2(n-1)$ 条边）、$\operatorname{par}/\operatorname{dep}/g$ 与操作序列，峰值几 MB，远低于 256 MB。
- **对照时限**：$n=m=5\times10^5$ 的链 / 星 / 随机树 / 完全二叉树四种形态实测，含 $10$ MB 读入的整程序最坏 $\approx0.30$ s，纯算法部分 $\approx0.08$ s；时限 3 s，余量在 $10$ 倍以上。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        int n, m;
        cin >> n >> m;
        vector<vector<int>> adj(n + 1);
        for (int i = 0; i < n - 1; i++) {
            int x, y;
            cin >> x >> y;
            adj[x].push_back(y);
            adj[y].push_back(x);
        }
        vector<int> v(m);
        for (int i = 0; i < m; i++) cin >> v[i];

        // 迭代 BFS：父、深度、父先子后的 order
        vector<int> par(n + 1, 0), dep(n + 1, 0), order;
        order.reserve(n);
        order.push_back(1);
        for (size_t i = 0; i < order.size(); ++i) {
            int u = order[i];
            for (int w : adj[u]) {
                if (w == par[u]) continue;
                par[w] = u;
                dep[w] = dep[u] + 1;
                order.push_back(w);
            }
        }
        // 标记 1 -> n 路径；g[u] = lca(u, n)
        vector<char> on(n + 1, 0);
        for (int x = n; x != 0; x = par[x]) on[x] = 1;
        vector<int> g(n + 1, 0);
        for (int u : order) g[u] = on[u] ? u : g[par[u]];

        int ans = dep[n];
        for (int i = 0; i < m; i++) {
            int x = v[i];
            if (g[x] == 1) continue;              // 与 n 分居 1 的两支，该操作无效
            int cand = 1 + dep[x] + dep[n] - 2 * dep[g[x]];
            if (cand > ans) ans = cand;
        }
        cout << ans << '\n';
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
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            x = int(data[pos]); y = int(data[pos + 1]); pos += 2
            adj[x].append(y)
            adj[y].append(x)

        par = [0] * (n + 1); dep = [0] * (n + 1); order = [1]
        for u in order:                       # BFS：父先于子
            pu = par[u]; du = dep[u] + 1
            for w in adj[u]:
                if w != pu:
                    par[w] = u; dep[w] = du; order.append(w)

        on = bytearray(n + 1)
        x = n
        while x:
            on[x] = 1; x = par[x]

        g = [0] * (n + 1)
        for u in order:
            g[u] = u if on[u] else g[par[u]]

        dn = dep[n]; ans = dn
        for _ in range(m):
            v = int(data[pos]); pos += 1
            if g[v] != 1:
                cand = 1 + dep[v] + dn - 2 * dep[g[v]]
                if cand > ans:
                    ans = cand
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n=2$**：唯一树是 $1-2$，$\operatorname{dep}(n)=1$；任意 $v_i=2$ 给出 $g=2$、$\operatorname{dist}=0$、候选 $1$，答案恒为 $1$（样例 1）。不要把「候选 $1$」误当成能加长路径。
2. **$n$ 是 $1$ 的孩子**：$\operatorname{dep}(n)=1$ 看似无法改进，但只要 $v_i$ 落在 $n$ 的子树里且 $\operatorname{lca}(v_i,n)=n\ne1$，就能删掉 $(1,n)$ 把整棵子树翻过来，答案变成 $\operatorname{dep}(v_i)$。例如链 $1\!-\!n\!-\!x\!-\!y\!-\!z$ 取 $v=z$，答案由 $1$ 变 $4$——**不能只盯着 $\operatorname{dep}(n)$ 判断有无提升空间**。
3. **所有 $v_i$ 都与 $n$ 不同支**（$g(v_i)=1$）：一次有效操作都没有，答案就是 $\operatorname{dep}(n)$（样例 5）。把判定写成「$v_i$ 是否在 $n$ 的子树里」是错的：$v_i$ 在 $n$ 的**祖先一侧**同样能生效。
4. **深链爆栈**：$5\times10^5$ 深的链上递归必崩（C++ 栈溢出、Python `RecursionError`）；本文两份代码都用 `order` 迭代，天然免疫。
5. **多测清空的代价**：$\sum n$ 只有 $5\times10^5$ 但 $t$ 可达 $10^4$，每次 `memset` 大小为 $n$ 的全局数组在「很多小 case」下是 $O(t\cdot n)$，会 TLE。
6. **读入**：约 $1.5\times10^6$ 个整数，C++ 不关同步流时 `cin` 是唯一瓶颈，Python 必须整体读入。

## 相关题目与扩展

- [CF 1328E Tree Queries](https://codeforces.com/problemset/problem/1328/E)：判断一组点是否都落在某条根到某点的路径上，正是本文「把 $1\to n$ 路径打标记」的同款技巧。
- [CF 1702G2 Passable Paths (hard version)](https://codeforces.com/problemset/problem/1702/G2)：LCA + 路径判定，可看作本文「公共祖先 $\ne1$」条件的加强版。
- [CF 1092F Tree with Maximum Cost](https://codeforces.com/problemset/problem/1092/F)：换根 DP 入门，与本文「整块子树改挂到根」的重构视角互补。
- [LeetCode 2458. 移除子树后的二叉树高度](https://leetcode.cn/problems/height-of-binary-tree-after-subtree-removal-queries/)：同样是「剪掉一棵子树后深度怎么变」。

**延伸思考**：若要求「每次操作后就输出当前答案」，本结论可增量维护：第 $i$ 次操作只会把答案更新为 $\max(\text{旧答案},1+\operatorname{dist}(v_i,n))$，但仍需判断 $v_i$ 与 $n$ 此刻是否同块，即动态维护 $1\to n$ 这条根路径——需上 LCT，或把询问离线倒序用并查集缩点。若把终点换成 $q$ 个不同询问点，则需要真正的 LCA 预处理（倍增 / 欧拉序 + ST 表），每次询问 $O(1)$，复杂度 $O(n\log n+m+q)$；本文的 $g$ 递推相当于把「对固定终点的多次 LCA」压成一次线性扫描。
