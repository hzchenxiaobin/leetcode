# Codeforces 225D 蛇（Snake） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/225/D
- **比赛来源**：Codeforces Round 139 (Div. 2) · Problem D（UTC 2012-09-21）
- **难度**：2200
- **标签**：BFS、状态压缩
- **评测类型**：普通
- **限制**：时间 4 s / 内存 256 MB

**题意**：$n\times m$ 网格上有长度 $k$ 的蛇（头为 1，依次到尾），身体不能重叠、不能穿墙。每步头移到相邻格，其余节跟随。求头到达苹果的最少步数，不可达输出 −1。

**约束**：$n,m\le15$，蛇身长度由输入给出。

## 2. 示例与观察

官方样例一：

```text
输入：
4 5
##...
..1#@
432#.
...#.

输出：
4
```

官方样例二：

```text
输入：
4 4
#78#
.612
.543
..@.

输出：
6
```

官方样例三：

```text
输入：
3 2
3@
2#
1#

输出：
-1
```

**观察**：身体形态完全由“头和每节相对前一节的方向”决定；每节 2 bit，长度 $k-1$ ⇒ 状态可编码成“头位置 + 方向串”。

![状态 = 头 + 方向串](../../../images/cf225d_bfs.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

直接存整条蛇坐标也可，但状态编码更省。

### 3.2 核心观察

BFS：新头 = 头 + 方向；不撞身体（尾同时移开）；方向串左移并压入“新头指向旧头”的方向。

### 3.3 算法流程

1. 解析初始蛇身与苹果。
2. BFS 状态 (头位置, 方向串)。
3. 到达苹果输出步数；队列空输出 −1。

![样例](../../../images/cf225d_walk.svg)

### 3.4 样例走查

样例一 4 步、样例二 6 步、样例三 −1 ✓。

## 4. 正确性证明

**引理 1（状态完备）**：头位置 + 方向串唯一确定整条蛇。

**证明**：从头开始按方向串逐节递推坐标。∎

**引理 2（转移正确）**：按上述转移得到的正是规则允许的移动。

**证明**：头移入相邻格、其余节跟随、尾格空出；碰撞检查排除非法。∎

**定理**：BFS 得到最短步数。

**证明**：由引理 1、2，状态图与游戏一一对应，BFS 求无权最短路。∎

## 5. 复杂度分析

- **时间**：$O(\text{状态数}\times4)$。\n- **空间**：$O(\text{状态数})$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int n, m, k;
static char g[20][20];
static int dx4[4] = {-1, 1, 0, 0}, dy4[4] = {0, 0, -1, 1};
int id(int x, int y) { return x * m + y; }
int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 0; i < n; ++i) scanf("%s", g[i]);
    vector<pair<int,int>> seg(300);
    int maxSeg = 0;
    pair<int,int> apple{-1,-1};
    for (int i = 0; i < n; ++i) for (int j = 0; j < m; ++j) {
        char c = g[i][j];
        if (c >= '1' && c <= '9') { int v = c - '0'; seg[v] = {i, j}; maxSeg = max(maxSeg, v); }
        else if (c == '@') apple = {i, j};
    }
    k = maxSeg;
    auto passable = [&](int x, int y) { return x >= 0 && x < n && y >= 0 && y < m && g[x][y] != '#'; };
    // 编码：d[i] = body[i] -> body[i+1] 的方向（i=0..k-2），每 2 bit
    unsigned long long init = 0;
    for (int i = 1; i <= k - 1; ++i) {
        int x0 = seg[i].first, y0 = seg[i].second, x1 = seg[i+1].first, y1 = seg[i+1].second;
        int d;
        if (x1 == x0 - 1) d = 0; else if (x1 == x0 + 1) d = 1; else if (y1 == y0 - 1) d = 2; else d = 3;
        init |= (unsigned long long)d << (2 * (i - 1));
    }
    unsigned long long mask = (k >= 2) ? ((1ULL << (2 * (k - 1))) - 1) : 0ULL;
    map<pair<int, unsigned long long>, int> dist;
    queue<pair<int, unsigned long long>> q;
    pair<int, unsigned long long> start = {id(seg[1].first, seg[1].second), init};
    dist[start] = 0; q.push(start);
    vector<pair<int,int>> body;
    while (!q.empty()) {
        auto cur = q.front(); q.pop();
        int headId = cur.first; unsigned long long dirs = cur.second;
        int d0 = dist[cur];
        int hx = headId / m, hy = headId % m;
        if (make_pair(hx, hy) == apple) { printf("%d\n", d0); return 0; }
        // 还原身体
        body.clear();
        body.push_back({hx, hy});
        int x = hx, y = hy;
        for (int i = 0; i < k - 1; ++i) {
            int d = (dirs >> (2 * i)) & 3;
            x += dx4[d]; y += dy4[d];
            body.push_back({x, y});
        }
        for (int d = 0; d < 4; ++d) {
            int nx = hx + dx4[d], ny = hy + dy4[d];
            if (!passable(nx, ny)) continue;
            bool bad = false;
            for (int i = 0; i + 1 < k; ++i) if (body[i].first == nx && body[i].second == ny) { bad = true; break; }
            if (bad) continue;
            int back = (d == 1) ? 0 : (d == 0) ? 1 : (d == 3) ? 2 : 3;   // 旧头在新头的哪个方向
            unsigned long long nd = (dirs << 2) & mask;
            nd |= (unsigned long long)back;
            pair<int, unsigned long long> st = {id(nx, ny), nd};
            if (!dist.count(st)) { dist[st] = d0 + 1; q.push(st); }
        }
    }
    printf("-1\n");
    return 0;
}
```

### Python3

```python
import sys
from collections import deque


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    g = [data[2 + i].decode() for i in range(n)]
    seg = {}
    apple = None
    for i in range(n):
        for j in range(m):
            c = g[i][j]
            if c.isdigit():
                seg[int(c)] = (i, j)
            elif c == '@':
                apple = (i, j)
    k = max(seg)
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def passable(p):
        return 0 <= p[0] < n and 0 <= p[1] < m and g[p[0]][p[1]] != '#'

    body = tuple(seg[i] for i in range(1, k + 1))
    seen = {body}
    q = deque([(body, 0)])
    while q:
        b, d = q.popleft()
        head = b[0]
        if head == apple:
            print(d); return
        for dx, dy in dirs4:
            nh = (head[0] + dx, head[1] + dy)
            if not passable(nh):
                continue
            if nh in b[:-1]:
                continue
            nb = (nh,) + b[:-1]
            if nb not in seen:
                seen.add(nb); q.append((nb, d + 1))
    print(-1)


main()
```

## 7. 边界情况与易错点

1. **长度 1**：只看头。
2. **尾格可进入**：尾巴同时移开。
3. **数字字符**：蛇身用 1..9 表示顺序。
4. **不可达**：输出 −1。
5. **苹果位置**：只判头是否到达。

## 8. 验证记录

- **编译环境与命令**：`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/225/D_蛇.md`。
- **官方样例**：3 / 3 通过（4、6、−1）。
- **随机对拍**：与独立实现（直接存整条蛇坐标的 BFS）**120 组**（C++）与 **53 组**（Python）随机地图一致。
- **性能**：15×15 最大网格 < 0.1 s。
- **图片校验**：`cf225d_bfs.svg`、`cf225d_walk.svg` 通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 225C 条形码](https://codeforces.com/problemset/problem/225/C)：同场 DP。
- [LeetCode 909 蛇梯棋](https://leetcode.cn/problems/snakes-and-ladders/)：BFS。

**延伸思考**：

1. 若蛇会变长，状态需加长度。
2. 若要求吃完所有苹果，变成 TSP 型搜索。
