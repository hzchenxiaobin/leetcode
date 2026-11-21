# Codeforces 243B 寻找九头蛇子图 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/243/B
- **比赛来源**：Codeforces Round 150 (Div. 1) · Problem B（UTC 2012-11-16）
- **难度**：2000
- **标签**：图论、暴力、构造
- **评测类型**：多解（任一 hydra 即可，需 checker）
- **限制**：时间 2 s / 内存 256 MB

**题意**：无向简单图 $G$（$n,m\le10^5$），给定 $h,t\le100$。求一个「hydra」：两个相邻点 $u,v$，$u$ 另外连 $h$ 个点（头），$v$ 另外连 $t$ 个点（尾），且这 $h+t+2$ 个点两两不同。输出 `YES` 与方案，或 `NO`。

**约束**：$n,m\le10^5$，$h,t\le100$。暴力枚举所有 $(u,v)$ 再求交集是 $O(nm)$，会超时；必须利用 $h,t$ 很小这一点做剪枝。

## 2. 示例与观察

```text
输入：
9 12 2 3
1 2
2 3
1 3
1 4
2 5
4 5
4 6
6 5
6 7
7 5
8 7
9 1

输出：
YES
4 1
5 6
9 3 2
```

```text
输入：
7 10 3 3
1 2
2 3
1 3
1 4
2 5
4 5
4 6
6 5
6 7
7 5
输出：
NO```


**样例一**：$u=4,v=1$，头 $\{5,6\}$（都在 $N(4)$ 里，$4$ 的邻居是 $1,5,6$），尾 $\{9,3,2\}$（都在 $N(1)$ 里，$1$ 的邻居是 $2,3,4,9$），共 $2+3+2=7$ 个点互不相同 ✓。

![hydra 结构](../../../images/cf243b_hydra.svg)

**观察一**：记 $A=N(u)\setminus\{v\}$、$B=N(v)\setminus\{u\}$。存在方案 $\iff$

$$|A|\ge h,\quad |B|\ge t,\quad |A\cup B|\ge h+t .$$

（这就是「从 $A$ 取 $h$ 个、从 $B$ 取 $t$ 个且不重复」的充要条件。）

**观察二**：$u$ 必须满足 $\deg(u)\ge h+1$，$v$ 必须满足 $\deg(v)\ge t+1$；这一条就滤掉了绝大多数边（例如星形图的叶子）。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

对每条边求 $|A\cup B|$ 需要 $O(\deg u+\deg v)$，最坏（星形图中心 + 度数 2 的叶子）是 $10^{10}$。

### 3.2 核心观察：三种情形分别处理

![判定与构造](../../../images/cf243b_cond.svg)

对候选边 $(u,v)$（两端度数足够）：

1. **$|A|\ge h+t$**：先取 $A$ 的前 $h$ 个当头（标记），再从 $B$ 里挑不在标记中的 $t$ 个当尾。若 $B$ 里不够，说明 $B$ 大部分被头占了，取其中若 $t-q$ 个「与头重合」的点补进尾，然后把头重选（避开这些尾）——因为 $|A|\ge h+t$，重选一定够。全程只扫 $O(h+t)$ 个元素。
2. **$|B|\ge h+t$**：对称地先定尾、再补头。
3. **两侧都 $<h+t$**：此时 $|A|,|B|<200$，直接标记 $A$、扫 $B$ 算出 $|A\cup B|$ 精确判定；构造时「头优先取 $A\setminus B$」，即可保证 $B$ 里还剩 $t$ 个。

关键点：情形 3 里如果「头随便取」，可能把头全取在 $B$ 上，导致尾不够；所以必须优先取 $A\setminus B$ 的元素。

### 3.3 样例走查

样例一：$u=2,v=5$：$A=N(2)\setminus\{5\}=\{1,3\}$，$B=N(5)\setminus\{2\}=\{4,6,7\}$，$|A|=2=h,|B|=3=t$，并集 5 = $h+t$ ✓ → 输出头 $\{1,3\}$、尾 $\{4,6,7\}$。

样例二：$h=t=3$，图中度数 $\ge4$ 的点很少且互相之间并集不够 6 → `NO`（由 checker 的独立判定确认）。

## 4. 正确性证明

**引理 1（充要条件）**：能从 $A$ 选 $h$ 个、$B$ 选 $t$ 个且互不相同 $\iff |A|\ge h,\ |B|\ge t,\ |A\cup B|\ge h+t$。

**证明**：必要性显然。充分性：取 $A'\subseteq A$ 为 $h$ 个元素，优先取 $A\setminus B$（若 $|A\setminus B|\ge h$ 则 $A'\subseteq A\setminus B$，此时 $B\setminus A'=B$，$|B|\ge t$ ✓；否则 $A'$ 含 $h-|A\setminus B|$ 个 $A\cap B$ 的元素，$|B\setminus A'|=|B|-h+|A\setminus B|=|A\cup B|-h\ge t$ ✓），再从 $B\setminus A'$ 取 $t$ 个。∎

**引理 2（三种情形都构造成功）**：只要引理 1 的条件成立，上述三种情形的构造都能给出合法方案。

**证明**：情形 1：头 $X$ 取 $A$ 的 $h$ 个；尾优先取 $B\setminus X$。若 $|B\setminus X|\ge t$ 直接完成；否则把 $B\cap X$ 中补 $t-|B\setminus X|$ 个进尾，再把头重选为 $A$ 中避开「全部尾」的 $h$ 个——因为 $|A|\ge h+t$ 且尾只有 $t$ 个，故 $|A|-t\ge h$，够。情形 2 对称。情形 3：由引理 1 的构造（头优先取 $A\setminus B$）δ 直接成立，此时判定已用精确的 $|A\cup B|$。∎

**定理**：算法输出 `YES` 时方案合法；若存在方案，算法一定能输出 `YES`。

**证明**：合法性由引理 2；完备性：若存在方案，则对应边 $(u,v)$ 满足引理 1 的条件，且度数检查通过，算法在处理该边时按引理 2 构造成功。∎

## 5. 复杂度分析

- 情形 1、2 每条候选边只花 $O(h+t)$；情形 3 每条边 $O(|A|+|B|)\le O(h+t)$。总 $O(m(h+t))\le2\times10^7$。
- 空间 $O(n+m)$。
- 实测：$h=t=100$、团 + 巨型星形（10 万条边，答案 `NO`）约 $22$ ms；$h=t=1$、5 万点 7.5 万边（有解）约 $12$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m, h, t;
    if (scanf("%d %d %d %d", &n, &m, &h, &t) != 4) return 0;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        scanf("%d %d", &a, &b);
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    // 时间戳数组：xMark 标记「已选为头/尾的禁止集合」，bMark 标记 B 以便判断 A\B
    vector<int> xMark(n + 1, 0), bMark(n + 1, 0);
    int xStamp = 0, bStamp = 0;
    vector<int> heads, tails;

    for (int u = 1; u <= n; ++u) {
        int nA = (int)adj[u].size() - 1;      // |N(u)\{v}| 的上界（v 是某个邻居）
        if ((int)adj[u].size() < h + 1) continue;
        for (int v : adj[u]) {
            if ((int)adj[v].size() < t + 1) continue;
            int nB = (int)adj[v].size() - 1;
            if (nA < h || nB < t) continue;
            heads.clear(); tails.clear();
            if (nA >= h + t) {
                // A 足够大：先取 h 个做头，再从 B\heads 里取尾
                for (int z : adj[u]) { if (z == v) continue; heads.push_back(z); if ((int)heads.size() == h) break; }
                ++xStamp;
                for (int z : heads) xMark[z] = xStamp;
                vector<int> inX;
                for (int z : adj[v]) {
                    if (z == u) continue;
                    if (xMark[z] == xStamp) { if ((int)inX.size() < t) inX.push_back(z); }
                    else { tails.push_back(z); if ((int)tails.size() == t) break; }
                }
                if ((int)tails.size() < t) {
                    int need = t - (int)tails.size();
                    if ((int)inX.size() < need) continue;
                    vector<int> Y(inX.begin(), inX.begin() + need);
                    for (int z : Y) tails.push_back(z);
                    // 头要同时避开「已定下的尾」和 Y
                    ++xStamp;
                    for (int z : tails) xMark[z] = xStamp;
                    vector<int> nh;
                    for (int z : adj[u]) { if (z == v) continue; if (xMark[z] == xStamp) continue; nh.push_back(z); if ((int)nh.size() == h) break; }
                    if ((int)nh.size() < h) continue;
                    heads = nh;
                }
            } else if (nB >= h + t) {
                // B 足够大：先取 t 个做尾，再从 A\tails 里取头
                for (int z : adj[v]) { if (z == u) continue; tails.push_back(z); if ((int)tails.size() == t) break; }
                ++xStamp;
                for (int z : tails) xMark[z] = xStamp;
                vector<int> inY;
                for (int z : adj[u]) {
                    if (z == v) continue;
                    if (xMark[z] == xStamp) { if ((int)inY.size() < h) inY.push_back(z); }
                    else { heads.push_back(z); if ((int)heads.size() == h) break; }
                }
                if ((int)heads.size() < h) {
                    int need = h - (int)heads.size();
                    if ((int)inY.size() < need) continue;
                    vector<int> Z(inY.begin(), inY.begin() + need);
                    for (int z : Z) heads.push_back(z);
                    ++xStamp;
                    for (int z : heads) xMark[z] = xStamp;
                    vector<int> nt;
                    for (int z : adj[v]) { if (z == u) continue; if (xMark[z] == xStamp) continue; nt.push_back(z); if ((int)nt.size() == t) break; }
                    if ((int)nt.size() < t) continue;
                    tails = nt;
                }
            } else {
                // 两侧都 < h+t（≤200）：精确判定 |A ∪ B| ≥ h+t，并构造
                ++bStamp;
                for (int z : adj[v]) if (z != u) bMark[z] = bStamp;
                int inter = 0;
                for (int z : adj[u]) if (z != v && bMark[z] == bStamp) ++inter;
                if (nA + nB - inter < h + t) continue;
                // 头优先取 A\B
                ++xStamp;
                for (int z : adj[u]) {
                    if (z == v || bMark[z] == bStamp) continue;
                    heads.push_back(z); xMark[z] = xStamp;
                    if ((int)heads.size() == h) break;
                }
                if ((int)heads.size() < h) {
                    for (int z : adj[u]) {
                        if (z == v || bMark[z] != bStamp) continue;
                        if (xMark[z] == xStamp) continue;
                        heads.push_back(z); xMark[z] = xStamp;
                        if ((int)heads.size() == h) break;
                    }
                }
                if ((int)heads.size() < h) continue;
                for (int z : adj[v]) {
                    if (z == u || xMark[z] == xStamp) continue;
                    tails.push_back(z);
                    if ((int)tails.size() == t) break;
                }
                if ((int)tails.size() < t) continue;
            }
            printf("YES\n%d %d\n", u, v);
            for (int i = 0; i < (int)heads.size(); ++i) printf("%d%c", heads[i], i + 1 == (int)heads.size() ? '\n' : ' ');
            for (int i = 0; i < (int)tails.size(); ++i) printf("%d%c", tails[i], i + 1 == (int)tails.size() ? '\n' : ' ');
            return 0;
        }
    }
    printf("NO\n");
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m, h, t = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    adj = [[] for _ in range(n + 1)]
    p = 4
    for _ in range(m):
        a, b = int(data[p]), int(data[p + 1])
        p += 2
        adj[a].append(b)
        adj[b].append(a)

    for u in range(1, n + 1):
        if len(adj[u]) < h + 1:
            continue
        for v in adj[u]:
            if len(adj[v]) < t + 1:
                continue
            A = [z for z in adj[u] if z != v]
            B = [z for z in adj[v] if z != u]
            if len(A) < h or len(B) < t:
                continue
            if len(A) >= h + t or len(B) >= h + t:
                if len(A) >= h + t:
                    heads = A[:h]
                    hs = set(heads)
                    tails = [z for z in B if z not in hs][:t]
                    if len(tails) < t:
                        inX = [z for z in B if z in hs]
                        need = t - len(tails)
                        if len(inX) < need:
                            continue
                        tails = tails + inX[:need]
                        ts = set(tails)
                        heads = [z for z in A if z not in ts][:h]
                        if len(heads) < h:
                            continue
                    out = (heads, tails)
                else:
                    tails = B[:t]
                    ts = set(tails)
                    heads = [z for z in A if z not in ts][:h]
                    if len(heads) < h:
                        inY = [z for z in A if z in ts]
                        need = h - len(heads)
                        if len(inY) < need:
                            continue
                        heads = heads + inY[:need]
                        hs = set(heads)
                        tails = [z for z in B if z not in hs][:t]
                        if len(tails) < t:
                            continue
                    out = (heads, tails)
            else:
                setB = set(B)
                inter = sum(1 for z in A if z in setB)
                if len(A) + len(B) - inter < h + t:
                    continue
                heads = [z for z in A if z not in setB][:h]
                if len(heads) < h:
                    hs0 = set(heads)
                    heads += [z for z in A if z in setB and z not in hs0][:h - len(heads)]
                if len(heads) < h:
                    continue
                hs = set(heads)
                tails = [z for z in B if z not in hs][:t]
                if len(tails) < t:
                    continue
                out = (heads, tails)
            heads, tails = out
            lines = ["YES", "%d %d" % (u, v),
                     ' '.join(map(str, heads)), ' '.join(map(str, tails))]
            sys.stdout.write('\n'.join(lines) + '\n')
            return
    sys.stdout.write("NO\n")


main()
```

## 7. 边界情况与易错点

1. **头尾不能重复**：最容易错的地方——重选头时必须把「已确定的尾」全部标记，否则会输出重复点（本解法在初版就踩过这个坑，已修复）。
2. **$h$ 或 $t$ 大于可用邻居**：度数检查要写成 $\deg\ge h+1$（要排除 $v$ 本身）。
3. **同色/自环/重边**：题面保证没有，但仍要保证 $u\ne v$。
4. **星形图性能**：必须走情形 1/2 的「$O(h+t)$」路径，否则会退化成 $O(\deg^2)$。
5. **`NO` 的判定**：只有在所有候选边都失败后才输出，不能提前退出。
6. **多测**：单组数据。

## 8. 验证记录

- **编译环境与命令**：`verify_solution.py` 自动回退到 `clang++ -std=c++17 -O2 -I codeforces/tools/include`；Python 3.9.6。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/243/B_寻找九头蛇子图.md --checker codeforces/tools/checkers/cf243b.py` → `CF243B: samples 2 / C++ 编译 OK, 样例 2/2 / Python 语法 OK, 样例 2/2`
- **checker 的校验条件**（`codeforces/tools/checkers/cf243b.py`）：`YES` 时校验 $u\sim v$、头都与 $u$ 相邻、尾都与 $v$ 相邻、$h+t+2$ 个点两两不同；`NO` 时用「枚举每条边检查 $|A|\ge h,|B|\ge t,|A\cup B|\ge h+t$」独立判定（$n\le400$），防止把有解判成无解。
- **官方样例**：2 / 2 通过。
- **随机对拍**：**240 组**随机图（$n\le10$，$m\le18$，$h,t\in[1,3]$），判定与独立暴力一致，`YES` 输出全部通过 checker，0 组不合法。
- **最大约束性能**：见第 5 节（22 ms / 12 ms，限时 2 s）。
- **图片校验**：`cf243b_hydra.svg`、`cf243b_cond.svg` 通过 XML 解析。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 243A The Brand New Function](https://codeforces.com/problemset/problem/243/A)、[243C Colorado Potato Beetle](https://codeforces.com/problemset/problem/243/C)：同场题。

**延伸思考**：

1. **若 hydra 要求是「导出子图」恰好为树**（不允许多余边）：需要额外检查所选点之间没有别的边，复杂度上升。
2. **若 $h,t$ 很大（$10^5$）**：$O(m(h+t))$ 不可行，需要按度数分块或随机采样。
3. **若要求找「最大的 hydra」**：变成最优化问题，可以枚举 $u,v$ 后用 $|A\cup B|$ 排序。
