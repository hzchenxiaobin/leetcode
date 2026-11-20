# Codeforces 86B 俄罗斯方块再临 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/86/B
- **比赛来源**：Yandex.Algorithm 2011: Round 2 · Problem B（UTC 2011-05-22）
- **难度**：2200
- **标签**：构造、图匹配、贪心、图着色
- **评测类型**：特殊评测（答案不唯一）
- **限制**：时间 1 s / 内存 256 MB

**题意**：给一个 $n\times m$ 的棋盘，有些格子已经填了（`#`），其余是空格（`.`）。你需要把所有空格划分成若干**连通**（按边相邻）的图形，每个图形恰好含 $2\sim5$ 个格子（任意形状，允许旋转与镜像，题面的「仪表盘」里有全部 $2\sim5$ 格的连通图形）。输出时每个图形用一种数字表示，同一个图形的格子写同一个数字，`#` 保持原样。要求：相邻（按边）的两个图形必须用不同数字。无解输出 `-1`。

**约束**：

- $n,m\le1000$：最多 $10^6$ 个格子，构造必须是 $O(nm)$ 或 $O(nm\log nm)$，不能对整盘做指数搜索。
- 图形大小限定 $2\sim5$：既不能出现「单个格子」，也不能把一大片并成一块。
- 可用的「数字」只有 $0\sim9$ 共 10 种，因此给「图形相邻图」着色时颜色数不能超过 10。
- 特殊评测：任意合法方案都算对，所以样例输出只是其中一种。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
2 3
...
#.#

输出：
000
#0#
```

```text
输入：
3 3
.#.
...
..#

输出：
5#1
511
55#
```

```text
输入：
3 3
...
.##
.#.

输出：
-1
```

```text
输入：
1 2
##

输出：
##
```

**样例 1**：`. . . / # . #`，5 个空格连成一块（上面一行三格 + 下面两格分别挂在左右两端），正好可以用**一个 5 格图形**全部盖住，所以输出全是 `0`。

**样例 2**：7 个空格被分成三块（3 + 2 + 2），见 3.4 的插图。

**样例 3**：右下角 $(3,3)$ 那个空格子上、左都是 `#`，右、下越界——它没有任何空格邻居，连 2 格图形都凑不出来，故无解。题面提示说的就是这个格子。

**样例 4**：没有空格，输出原样即可。

**观察**：

1. 判分把「数字相同且四连通」的极大格子集当作一个图形，所以**不需要**真的指定每个图形的位置，只要数字标得合适：每个同数字连通块的大小在 $[2,5]$ 之间。
2. 「相邻图形数字不同」是这条定义的自动推论：若相邻两格数字相同，它们就属于同一个连通块。所以要担心的只有「块的大小」。
3. 输入无解的**唯一**障碍是「孤立空格子」（上下左右都不是空格）。只要能构造出覆盖，就一定能标号。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

对 $10^6$ 个格子做搜索（枚举每个空格子归属哪个图形）是指数级的，不可行。必须找一个**确定性的局部构造**：从左到右、从上到下扫一遍就能定下来。

### 3.2 核心观察一：三步构造

![三步铺满：横向配对 → 纵向配对 → 剩余单格挂靠](../../../images/cf86b_pipeline.svg)

1. **无解判据**：若存在一个空格子，上下左右都不是空格（`#` 或越界），则无解，直接输出 `-1`。
2. **横向配对**：按行优先顺序扫，遇到一个「空格且还没配对、右边也是空格且还没配对」的格子，就把这两个格子配成一块（$1\times2$ 骨牌）。
3. **纵向配对**：再按同样的顺序扫一遍，遇到「空格且还没配对、下边也是空格且还没配对」，配成一块（$2\times1$ 骨牌）。
4. **剩余单格挂靠**：经过前两步，还没被配对的空格子一定是**互相不相邻**的（下面的引理 2），而且它至少有一个邻居在骨牌上（否则它就是孤立格，与第 1 步矛盾）。把每个剩余单格并到任意一个相邻骨牌所在的图形里。
5. **着色**：构造「图形相邻图」（两个图形有边相邻就连边），对它做一个正常着色，颜色数 $\le6\le10$，再用数字 `0..9` 表示。

![骨牌 + 挂在它上面的单格：最多 5 格](../../../images/cf86b_size.svg)

为什么每个图形不超过 5 格：以一块横骨牌 $(i,j),(i,j+1)$ 为例，它的 6 个邻居是 $(i,j-1)$、$(i,j+2)$、$(i-1,j)$、$(i-1,j+1)$、$(i+1,j)$、$(i+1,j+1)$。其中

- $(i,j-1)$ **不可能**是剩余单格（第 2 步扫到它时 $(i,j)$ 还没被配走，它俩会被直接配对）；
- 同一侧的两个邻居（如 $(i-1,j)$ 与 $(i-1,j+1)$）彼此相邻，而剩余单格两两不相邻，所以同一侧至多挂一个。

于是最多挂 $1+1+1=3$ 个单格，图形大小 $\le 2+3=5$ ✓。竖骨牌同理。

### 3.3 核心观察二：着色

把每个图形收缩成一个点，得到的「图形相邻图」是网格图（平面图）的收缩，所以它**也是平面图**。平面图一定存在度数 $\le5$ 的顶点（平均度 $<6$），于是可以用「退化序」贪心染色：

1. 反复找一个当前度数 $\le5$ 的顶点，把它从图里删掉并压栈；
2. 按出栈（逆序）给顶点染色，每个顶点取「邻居里没用过的最小颜色」。

每个顶点染色时，它已染色的邻居就是「删除顺序在它之前」的那些，个数 $\le5$，所以最多用 6 种颜色 ✓。颜色数 $6\le10$，用数字 `0..5` 即可。

（题解里还给了另一种更巧的做法：把整个平面按 $(i,j)\mapsto 3(i\bmod 3)+(j\bmod 3)$ 染成 9 色，每个图形取它「骨牌黑格」的网格颜色。因为相邻格子的网格颜色一定不同，相邻图形的颜色也一定不同。见「延伸思考」。）

### 3.4 样例 2 走查

![样例 2 走查：3×3 里的 7 个空格被分成 3+2+2](../../../images/cf86b_sample2.svg)

输入 3×3，空格在 $(1,1),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2)$（1-indexed）。

1. 横向配对：$(2,1)$-$(2,2)$ 成对；$(3,1)$-$(3,2)$ 成对（$(2,3)$ 右边越界，配不上）。
2. 纵向配对：$(1,3)$-$(2,3)$ 成对（$(1,1)$ 下方 $(2,1)$ 已被配走）。
3. 剩余单格：$(1,1)$，它的邻居 $(2,1)$ 在骨牌上 → 挂到该块，这块变成 3 格。
4. 图形：$\{(1,1),(2,1),(2,2)\}$ 大小 3；$\{(1,3),(2,3)\}$ 大小 2；$\{(3,1),(3,2)\}$ 大小 2。
5. 相邻关系：第 1 块与第 3 块相邻（$(2,1)$-$(3,1)$），第 1 块与第 2 块相邻（$(2,2)$-$(2,3)$），第 2、3 块不相邻。
6. 着色：第 1 块取 1，第 2、3 块都可以取 0（它们不相邻），得到

```text
1#0
110
00#
```

这正是样例 2 的另一种合法输出（样例给的是 `5#1 / 511 / 55#`）。

## 4. 正确性证明

**引理 1（无解判据）**：若存在一个空格子，其上下左右四个位置都不是空格（`#` 或越界），则问题无解。

**证明**：任何图形都是连通的、且大小 $\ge2$，所以该格子所属的图形必须还含有另一个与它边相邻的空格，矛盾。∎

**引理 2（剩余单格两两不相邻）**：在引理 1 成立的前提下，执行完横向配对与纵向配对后，剩余未配对的空格子两两不相邻。

**证明**：设 $u,v$ 是相邻的两个空格。若它们左右相邻（同一行、列 $j$ 与 $j+1$），按行优先顺序扫到 $u$ 时 $v$ 尚未被配对（$v$ 在 $u$ 之后），于是 $u$ 会与 $v$ 配对，$v$ 不会成为剩余单格，矛盾。若它们上下相邻（同一列、行 $i$ 与 $i+1$），在纵向配对阶段扫到 $u$ 时：若 $v$ 尚未配对，则 $u$ 与 $v$ 配对；若 $v$ 已被配对（横向阶段配走了），则 $v$ 不是剩余单格。两种情形都说明二者不可能同时是剩余单格。∎

**引理 3（每个图形大小在 $2\sim5$ 之间）**：上述构造产出的每个图形都是连通的，且大小 $\ge2$、$\le5$。

**证明**：连通性：图形要么是骨牌本身（2 格相连），要么是骨牌加上若干个与骨牌某格边相邻的单格，显然连通。下界 2：骨牌本身就有 2 格。上界 5：由 3.2 的讨论，一块骨牌最多挂 3 个剩余单格（左/上/下/右四个方向中，与骨牌同一行左侧的那个方向不可能有单格，同一侧的两个位置不可能同时是单格），故 $\le 2+3=5$。∎

**引理 4（着色合法）**：图形相邻图是平面图，存在正常着色使用不超过 6 种颜色；贪心（退化序）算法能在线性时间内找到它。

**证明**：图形相邻图由网格图（平面图）收缩每个图形的格子集得到，收缩保持平面性。平面图至少有 3 个顶点时必有度数 $\le5$ 的顶点（否则边数 $>3V-6$，与平面图边数上界矛盾），故算法每步都能找到可删的点；逆序染色时每个点至多 5 个已染色邻居，用 6 色必有一种可选。∎

**定理**：程序要么输出 `-1`（当且仅当无解），要么输出一个合法标号。

**证明**：无解时由引理 1 程序输出 `-1`；有解时引理 1 不成立，于是每个空格都有空格邻居，构造进行到最后一步，由引理 2、3 得到一组大小合法的连通图形；由引理 4 着色后，任意两个边相邻的格子若属于不同图形则颜色不同（否则它们会被并成同一个同色连通块，可能破坏大小约束）——这正是题面要求的「相邻图形数字不同」。因此输出合法。∎

## 5. 复杂度分析

- **时间**：两遍扫描 $O(nm)$；建边与排序去重 $O(E\log E)$（$E\le2\cdot10^6$）；退化序染色 $O(V+E)$。总体 $O(nm\log(nm))$，$10^6$ 个格子实测 C++ 端到端 41 ms。
- **空间**：`fig` 表 $O(nm)$、边表 $O(nm)$、颜色与度数 $O(V)$。$10^6$ 格时约 20 MB，远低于 256 MB。
- **与时限的关系**：1 s 时限下 C++ 有 20 倍以上余量；Python 在 $10^6$ 格时需要约 2.7 s，建议用 PyPy3 或直接交 C++。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<string> g(n);
    for (int i = 0; i < n; ++i) {
        static char buf[1005];
        if (scanf("%1004s", buf) != 1) return 0;
        g[i] = buf;
    }
    static const int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};

    // 1) 有孤立的空格子就无法覆盖
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            if (g[i][j] != '.') continue;
            bool ok = false;
            for (int d = 0; d < 4; ++d) {
                int ni = i + dr[d], nj = j + dc[d];
                if (ni >= 0 && ni < n && nj >= 0 && nj < m && g[ni][nj] == '.') ok = true;
            }
            if (!ok) { puts("-1"); return 0; }
        }

    // 2) 先横放配对，再竖放配对
    vector<vector<int>> fig(n, vector<int>(m, -1));
    vector<int> figSize;
    auto newFig = [&]() { figSize.push_back(0); return (int)figSize.size() - 1; };
    for (int i = 0; i < n; ++i)
        for (int j = 0; j + 1 < m; ++j)
            if (g[i][j] == '.' && g[i][j + 1] == '.' && fig[i][j] < 0 && fig[i][j + 1] < 0) {
                int id = newFig();
                fig[i][j] = fig[i][j + 1] = id;
                figSize[id] = 2;
            }
    for (int i = 0; i + 1 < n; ++i)
        for (int j = 0; j < m; ++j)
            if (g[i][j] == '.' && g[i + 1][j] == '.' && fig[i][j] < 0 && fig[i + 1][j] < 0) {
                int id = newFig();
                fig[i][j] = fig[i + 1][j] = id;
                figSize[id] = 2;
            }

    // 3) 剩下的单格一定四邻都是骨牌格，挂到任一相邻骨牌上（每块最多长到 5 格）
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j) {
            if (g[i][j] != '.' || fig[i][j] >= 0) continue;
            for (int d = 0; d < 4; ++d) {
                int ni = i + dr[d], nj = j + dc[d];
                if (ni < 0 || ni >= n || nj < 0 || nj >= m) continue;
                if (fig[ni][nj] >= 0) { fig[i][j] = fig[ni][nj]; ++figSize[fig[ni][nj]]; break; }
            }
        }

    // 4) 给“图形相邻图”做正常着色：它由网格图的收缩得到，一定是平面图，
    //    故存在度数 <= 5 的顶点，按退化序贪心用不到 6 种颜色。
    int F = (int)figSize.size();
    vector<int> head(F, -1), nxtE, to;
    {
        vector<pair<int, int>> es;
        es.reserve((size_t)n * m * 2);
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j) {
                if (fig[i][j] < 0) continue;
                int a = fig[i][j];
                if (j + 1 < m && fig[i][j + 1] >= 0 && fig[i][j + 1] != a) {
                    int b = fig[i][j + 1];
                    es.push_back({min(a, b), max(a, b)});
                }
                if (i + 1 < n && fig[i + 1][j] >= 0 && fig[i + 1][j] != a) {
                    int b = fig[i + 1][j];
                    es.push_back({min(a, b), max(a, b)});
                }
            }
        sort(es.begin(), es.end());
        es.erase(unique(es.begin(), es.end()), es.end());
        nxtE.assign(es.size() * 2, -1);
        to.assign(es.size() * 2, 0);
        for (size_t k = 0; k < es.size(); ++k) {
            int a = es[k].first, b = es[k].second;
            to[2 * k] = b; nxtE[2 * k] = head[a]; head[a] = 2 * k;
            to[2 * k + 1] = a; nxtE[2 * k + 1] = head[b]; head[b] = 2 * k + 1;
        }
    }
    vector<int> deg(F, 0), alive(F, 1), removedOrder;
    removedOrder.reserve(F);
    for (int v = 0; v < F; ++v)
        for (int e = head[v]; e != -1; e = nxtE[e]) ++deg[v];
    {
        deque<int> q;
        for (int v = 0; v < F; ++v) if (deg[v] <= 5) q.push_back(v);
        while ((int)removedOrder.size() < F) {
            if (q.empty()) {                       // 理论上不会发生（平面图）
                for (int v = 0; v < F; ++v) if (alive[v]) { q.push_back(v); break; }
            }
            int v = q.front();
            q.pop_front();
            if (!alive[v]) continue;
            alive[v] = 0;
            removedOrder.push_back(v);
            for (int e = head[v]; e != -1; e = nxtE[e]) {
                int u = to[e];
                if (!alive[u]) continue;
                if (--deg[u] == 5) q.push_back(u);
            }
        }
    }
    vector<int> col(F, -1);
    for (int idx = F - 1; idx >= 0; --idx) {
        int v = removedOrder[idx];
        bool used[10] = {};
        for (int e = head[v]; e != -1; e = nxtE[e]) {
            int u = to[e];
            if (col[u] >= 0 && col[u] < 10) used[col[u]] = true;
        }
        int c = 0;
        while (c < 10 && used[c]) ++c;
        col[v] = c;                                // 平面图保证 c <= 5
    }

    string line(m, '#');
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (g[i][j] == '#') line[j] = '#';
            else line[j] = char('0' + col[fig[i][j]]);
        }
        puts(line.c_str());
    }
    return 0;
}
```

### Python3

```python
import sys
from collections import deque


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    g = [data[2 + i].decode() for i in range(n)]
    DR = (1, -1, 0, 0)
    DC = (0, 0, 1, -1)

    # 1) 孤立空格子 => 无解
    for i in range(n):
        for j in range(m):
            if g[i][j] != '.':
                continue
            ok = False
            for d in range(4):
                ni, nj = i + DR[d], j + DC[d]
                if 0 <= ni < n and 0 <= nj < m and g[ni][nj] == '.':
                    ok = True
            if not ok:
                sys.stdout.write("-1\n")
                return

    # 2) 横放配对，再竖放配对
    fig = [[-1] * m for _ in range(n)]
    size = []
    for i in range(n):
        for j in range(m - 1):
            if g[i][j] == '.' and g[i][j + 1] == '.' and fig[i][j] < 0 and fig[i][j + 1] < 0:
                fid = len(size)
                size.append(2)
                fig[i][j] = fig[i][j + 1] = fid
    for i in range(n - 1):
        for j in range(m):
            if g[i][j] == '.' and g[i + 1][j] == '.' and fig[i][j] < 0 and fig[i + 1][j] < 0:
                fid = len(size)
                size.append(2)
                fig[i][j] = fig[i + 1][j] = fid

    # 3) 剩下的单格挂到相邻骨牌上
    for i in range(n):
        for j in range(m):
            if g[i][j] != '.' or fig[i][j] >= 0:
                continue
            for d in range(4):
                ni, nj = i + DR[d], j + DC[d]
                if 0 <= ni < n and 0 <= nj < m and fig[ni][nj] >= 0:
                    fig[i][j] = fig[ni][nj]
                    size[fig[ni][nj]] += 1
                    break

    # 4) 图形相邻图的正常着色（平面图 => 退化度 <= 5 => 6 种颜色够）
    F = len(size)
    adj = [set() for _ in range(F)]
    for i in range(n):
        for j in range(m):
            if fig[i][j] < 0:
                continue
            a = fig[i][j]
            if j + 1 < m and fig[i][j + 1] >= 0 and fig[i][j + 1] != a:
                adj[a].add(fig[i][j + 1]); adj[fig[i][j + 1]].add(a)
            if i + 1 < n and fig[i + 1][j] >= 0 and fig[i + 1][j] != a:
                adj[a].add(fig[i + 1][j]); adj[fig[i + 1][j]].add(a)

    deg = [len(adj[v]) for v in range(F)]
    alive = [True] * F
    order = []
    q = deque(v for v in range(F) if deg[v] <= 5)
    while len(order) < F:
        if not q:
            for v in range(F):
                if alive[v]:
                    q.append(v)
                    break
        v = q.popleft()
        if not alive[v]:
            continue
        alive[v] = False
        order.append(v)
        for u in adj[v]:
            if alive[u]:
                deg[u] -= 1
                if deg[u] == 5:
                    q.append(u)

    col = [-1] * F
    for idx in range(F - 1, -1, -1):
        v = order[idx]
        used = {col[u] for u in adj[v] if col[u] >= 0}
        c = 0
        while c in used:
            c += 1
        col[v] = c

    out = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append('#' if g[i][j] == '#' else str(col[fig[i][j]]))
        out.append(''.join(row))
    sys.stdout.write('\n'.join(out) + '\n')


main()
```

**说明**：本题是特殊评测，样例输出只是众多合法解之一，本文代码的输出与样例 2 不同但同样合法（见 3.4）。验证时使用 `codeforces/tools/checkers/cf86b.py`。

## 7. 边界情况与易错点

1. **全 `#` 的棋盘**：没有空格，直接输出原样（不能输出 `-1`，也不能输出空文件）。
2. **孤立空格**：判据是「上下左右都不在棋盘内或不是空格」。注意越界也算「不是空格」，边界格子要正确处理。
3. **图形大小必须 $\ge2$**：如果某块只有 1 格，判分会拒绝；把剩余单格挂到骨牌上正是为了避免它。
4. **图形大小必须 $\le5$**：如果对「剩余单格」的处理不当（例如把两个相邻单格并成一块再反复合并），可能出现 6 格以上的块。必须严格按「单格挂到相邻骨牌」的方式做。
5. **数字只有 10 个**：着色若用 $\Delta+1$ 的简单贪心，最坏可能超过 10；必须用「平面图 6 色」的退化序贪心（或用题解的 9 色网格法）。
6. **相邻图形不能同色**：判分把同色连通块当作一个图形，所以两图形相邻却同色会被合并成超大的块，直接 WA。
7. **$n=1$ 或 $m=1$**：退化情形；横/纵配对之一不可用，剩余单格的挂靠逻辑必须仍然成立（引理 2、3 对一维同样适用）。
8. **输出格式**：恰好 $n$ 行、每行 $m$ 个字符；`#` 的位置必须与输入一致。
9. **大输入 I/O**：$10^6$ 个字符，C++ 用 `scanf("%s")`/关同步，Python 用 `read().split()`。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `clang++ -std=c++17 -O2` 配 `codeforces/tools/include/bits/stdc++.h` 兼容头编译（可原样提交 GNU C++17）；Python 为系统 `python3`。
- **checker**：构造题输出不唯一，仓库提供 `codeforces/tools/checkers/cf86b.py`。它读入输入与实际输出，校验：① 输出 `-1` 时要求确实存在孤立空格；② 否则行数、列数、`#` 位置必须与输入一致，空格处必须是数字；③ 按「同数字四连通」划分图形，每个图形大小必须在 $2\sim5$。运行方式：`python3 codeforces/tools/verify_solution.py <doc> --checker codeforces/tools/checkers/cf86b.py`。
- **官方样例**：4 / 4 通过（用 checker 判定；样例 1、3、4 的输出与题面**逐字相同**，样例 2 是另一种合法解）。
- **文档与样例一致性**：`check_samples.py --only 0001-0100/86` 0 问题；`check.py codeforces/contests/0001-0100/86` 0 失败。
- **穷举验证（884 个棋盘）**：对 $1\times2$、$1\times5$、$2\times2$、$2\times3$、$2\times4$、$3\times3$ 的**全部** `#`/`.` 组合共 **884 个棋盘**，先用独立暴力（对空格集做「划分成连通 2..5 块」的精确搜索，判定是否有解）确认有解性，再用 checker 校验参考程序的输出：**全部一致且全部通过**。
- **随机验证（220 组）**：$n,m\le5$、密度随机的棋盘，同样「暴力判有解性 + checker 验输出」双管齐下，**全部通过**；Python 版本另抽 60 组做同样验证，也全部通过。
- **最大约束性能**：$n=m=1000$、全空格的极限输入，C++ 端到端约 41 ms、Python 约 2.7 s（Python 建议 PyPy3），相对 1 s 时限 C++ 余量 20 倍以上。
- **图片校验**：三张 SVG（`cf86b_pipeline.svg`、`cf86b_size.svg`、`cf86b_sample2.svg`）通过 `xml.etree.ElementTree.parse`，文字包围盒均在 `viewBox` 内。
- **公式校验**：正文公式经 KaTeX（`throwOnError: true`）渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 86C Genetic engineering](https://codeforces.com/problemset/problem/86/C)：同场 C 题，AC 自动机 + DP。
- [Codeforces 86E Long sequence](https://codeforces.com/problemset/problem/86/E)：同场 E 题，本原多项式构造。
- [Codeforces 1157E Minimum Array](https://codeforces.com/problemset/problem/1157/E)：同为构造题，强调「任意合法解即可」。
- [Codeforces 1114D Flood Fill](https://codeforces.com/problemset/problem/1114/D)：区间着色类问题，可与本题的「相邻块异色」对照。
- [LeetCode 785. 判断二分图](https://leetcode.cn/problems/is-graph-bipartite/)：图着色入门，本题的退化序 6 染色是它的进阶版。

**延伸思考**：

1. **题解的 9 色网格法**：把平面按 $(i,j)\mapsto 3(i\bmod3)+(j\bmod3)$ 染成 9 色（这是网格图的正常染色），每个图形取它「骨牌的黑格」的网格颜色。因为相邻格子的网格颜色不同，而图形的颜色取自骨牌黑格，可以证明相邻图形颜色必不同（见官方题解）。这比退化序着色更好写，也值得作为对照实现。
2. **如果图形大小放宽到 $2\sim6$**：构造完全不变（骨牌最多挂 3 个单格），$2+3=5<6$，仍然每块 $\le5$；但上界证明要重新算「最多挂几个单格」。
3. **如果只允许 $1\times2$ 骨牌（大小恰为 2）**：那就变成「完美匹配」问题，网格图不总存在完美匹配（如 3 格的 L 形），必须解一般图匹配（带花树），难度陡增。
4. **如果要求图形形状必须来自给定的有限集合**：这就成了精确覆盖/平铺问题，一般情形是 NP 难的，本题「任意连通 2..5 格」的宽松条件才是可构造的关键。
5. **如果数字只有 2 种**：等价于要求图形相邻图二分；一般平面图不二分，所以会无解——本题给 10 种数字足够宽裕。
