# Codeforces 272E Dima and Horses 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/272/E
- **比赛来源**：Codeforces Round 167 (Div. 2) · Problem E（UTC 2013-02-13）
- **难度**：2200
- **标签**：构造、局部搜索
- **评测类型**：多解
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 匹马，仇恨关系是对称的，**每匹马最多 3 个敌人**。把它们分成两组，使每匹马在**自己组内**的敌人数不超过 1。输出分组或 `-1`。

**约束**：$n \le 10^5$（度数 ≤ 3）。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 3
1 2
3 2
3 1

输出：
100
```

官方样例 2：

```text
输入：
2 1
2 1

输出：
00
```

官方样例 3：

```text
输入：
10 6
1 2
1 3
1 4
2 3
2 4
3 4

输出：
0110000000
```

**观察 1（关键）**：度数 ≤ 3。若某匹马 $v$ 在自己组内有 $\ge 2$ 个敌人，那么它的**组外**敌人数 $\le 3 - 2 = 1$ → 把它换到另一组后，它的组内敌人数 $\le 1$ ✓。

**观察 2（势函数）**：每次换组，$v$ 的组内边数变化为 $(b - a) \le -1$（$a \ge 2$ 为组内敌人数、$b \le 1$ 为组外敌人数）→ **组内边总数严格减少** → 过程必然终止（最多 $m$ 步）。

**观察 3**：终止时所有马的组内敌人数 $\le 1$ ✓。

## 3. 解题思路

![局部搜索：党内敌人 > 1 就换党](../../../images/cf272e_flip.svg)

1. 初始全部放进组 0，`cnt[v] = deg(v)`；
2. 队列维护 `cnt[v] >= 2` 的马；
3. 取出 $v$：换组，重算 `cnt[v]`，并更新邻居的 `cnt`（同组 +1、异组 -1），把变坏的邻居入队；
4. 队列空 → 输出。

## 4. 正确性证明

**引理 1（可行性）**：若 $v$ 的组内敌人数 $\ge 2$，则换组后它的组内敌人数 $\le 1$。

**证明**：度数 $\le 3$，组内 $\ge 2$ ⇒ 组外 $\le 1$；换组后原来的组外敌人变成组内，故新的组内敌人数 $\le 1$ ✓。∎

**引理 2（终止性）**：设 $E$ 为"两端同组"的边数，每次换组后 $E$ 严格减小。

**证明**：$v$ 的组内边 $a \ge 2$ 条变成组外边，组外边 $b \le 1$ 条变成组内边 → $\Delta E = b - a \le -1$ ✓。∎

**定理**：算法输出的分组合法。

**证明**：由引理 2 算法终止；终止时队列为空，即所有马 `cnt[v] <= 1`；由引理 1 的更新逻辑，`cnt` 始终等于组内敌人数 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + m)$（每条边引起的更新与换组次数相关，换组 ≤ $m$ 次）。
- **空间**：$O(n + m)$。
- **与时限的关系**：时限 2 s，$n = 10^5, m=136562$ 实测端到端 46.6 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n, m;
    if(scanf("%d %d",&n,&m)!=2) return 0;
    vector<vector<int>> adj(n+1);
    for(int i=0;i<m;i++){int a,b;scanf("%d %d",&a,&b);adj[a].push_back(b);adj[b].push_back(a);}
    vector<int> party(n+1,0), cnt(n+1,0);
    deque<int> q;
    for(int v=1;v<=n;v++){ cnt[v]=(int)adj[v].size(); if(cnt[v]>1) q.push_back(v); }
    while(!q.empty()){
        int v=q.front(); q.pop_front();
        if(cnt[v]<=1) continue;
        party[v]^=1;
        cnt[v]=0;
        for(int u:adj[v]){
            if(party[u]==party[v]){ cnt[u]++; cnt[v]++; }
            else { cnt[u]--; }
            if(cnt[u]>1) q.push_back(u);
        }
        if(cnt[v]>1) q.push_back(v);
    }
    for(int v=1;v<=n;v++) printf("%d",party[v]);
    printf("\n");
    return 0;
}
```

### Python3

```python
import sys
from collections import deque
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    pos = 2
    for _ in range(m):
        a, b = int(data[pos]), int(data[pos + 1]); pos += 2
        adj[a].append(b); adj[b].append(a)
    party = [0] * (n + 1)
    cnt = [len(adj[v]) for v in range(n + 1)]
    q = deque(v for v in range(1, n + 1) if cnt[v] > 1)
    while q:
        v = q.popleft()
        if cnt[v] <= 1:
            continue
        party[v] ^= 1
        cnt[v] = 0
        for u in adj[v]:
            if party[u] == party[v]:
                cnt[u] += 1; cnt[v] += 1
            else:
                cnt[u] -= 1
            if cnt[u] > 1:
                q.append(u)
        if cnt[v] > 1:
            q.append(v)
    sys.stdout.write("".join(str(party[v]) for v in range(1, n + 1)) + "\n")
main()
```

## 7. 边界情况与易错点

1. **度数为 0**：任意分组 ✓。
2. **初始全同组**：$E = m$，逐步修复。
3. **`cnt` 的更新**：换组后 `cnt[v]` 要重算，邻居只需 ±1。
4. **队列里可能有过期条目**：取出后检查 `cnt[v] > 1`。
5. **多解**：任何合法分组都行。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（`100`、`00`、`0110000000`；第三组本实现给 `1100000000` 同样合法），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf272e.py`（检查每匹马组内敌人数 ≤ 1）。
- **随机对拍**：250 组随机图（度数 ≤ 3），两个实现都通过 checker，**250 / 250 通过**（修复了早期版本 `cnt[v]` 未重算的 bug）。
- **最大约束性能**：$n = 10^5$、$m = 136562$，实测端到端 46.6 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 272D Dima and Two Sequences](https://codeforces.com/problemset/problem/272/D)：同场 D 题。
- [Codeforces 687A NP-Hard Problem](https://codeforces.com/problemset/problem/687/A)：二部图划分的同类构造。

**延伸思考**：

1. **如果度数上限是 4**：换组后可能仍 > 1，局部搜索不再保证终止。
2. **如果要求"两组非空"**：需要额外处理。

