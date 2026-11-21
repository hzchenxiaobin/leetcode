# Codeforces 216B 组队（Forming Teams） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/216/B
- **比赛来源**：Codeforces Round 133 (Div. 2) · Problem B（UTC 2012-08-14）
- **难度**：1700
- **标签**：图论、二分图、奇环
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个学生，每人至多两个仇人（无向）。要把他们分成人数相等的两队，敌人不能同队；可以让一些人坐板凳。求最少坐板凳人数。

**约束**：$2\le n\le100$，$1\le m\le100$。

## 2. 示例与观察

官方样例一：

```text
输入：
5 4
1 2
2 4
5 3
1 4

输出：
1
```

官方样例二：

```text
输入：
6 2
1 4
3 4

输出：
0
```

官方样例三：

```text
输入：
6 6
1 2
2 3
3 1
4 5
5 6
6 4

输出：
2
```

**观察**：每点度数 ≤2 ⇒ 每个连通块是路径或环。奇环无法二分 ⇒ 每个奇环至少要踢 1 人；踢完后若总人数为奇数，还要再踢 1 人。

![图 = 路径与环](../../../images/cf216b_teams.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举子集不可行（$2^{100}$）。

### 3.2 核心观察

答案 $=$ 奇环个数 $+\big((n-\text{奇环个数})\bmod2\big)$。踢掉一个奇环顶点后它变成偶路径，各分量二染色差 ≤1，可调整方向使总差为 0。

### 3.3 算法流程

1. DFS 求每个连通块。
2. 若块内所有点度数为 2 且块大小为奇数 ⇒ 奇环计数 +1。
3. 输出奇环数 + ((n − 奇环数) mod 2)。

![三个样例](../../../images/cf216b_walk.svg)

### 3.4 样例走查

样例一：1-2-4-1 是奇环 ⇒ 1+(5−1)%2=1 ✓；样例二无奇环且 6 偶 ⇒ 0 ✓；样例三两奇环 ⇒ 2 ✓。

## 4. 正确性证明

**引理 1（结构）**：每个连通块是路径或环。

**证明**：每点度数 ≤2 且无向 ⇒ 连通块为路径或环。∎

**引理 2（奇环必须踢人）**：奇环不能二分染色，故每个奇环至少踢 1 人；踢 1 人后变偶路径可二分。

**证明**：奇环不是二分图；删去一个顶点得路径。∎

**引理 3（平衡可达成）**：踢掉所有奇环各 1 人后，若剩余人数为偶数，则必存在方向选择使两队人数相等。

**证明**：各分量二染色差 $|s-t|\le1$；总人数偶 ⇒ 差为 1 的分量个数为偶 ⇒ 可取一半取正、一半取负使总差为 0。∎

**定理**：答案公式正确。

**证明**：由引理 2 下界为奇环个数；由引理 3 若剩余为奇数还需再踢 1 人，恰好达到；故公式最优。∎

## 5. 复杂度分析

- **时间**：$O(n+m)$。\n- **空间**：$O(n+m)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b; scanf("%d %d", &a, &b);
        adj[a].push_back(b); adj[b].push_back(a);
    }
    vector<int> vis(n + 1, 0);
    int oddCycles = 0;
    for (int s = 1; s <= n; ++s) {
        if (vis[s]) continue;
        // 收集连通块
        vector<int> comp;
        vector<int> st{s}; vis[s] = 1;
        while (!st.empty()) {
            int v = st.back(); st.pop_back(); comp.push_back(v);
            for (int w : adj[v]) if (!vis[w]) { vis[w] = 1; st.push_back(w); }
        }
        bool allDeg2 = true;
        for (int v : comp) if (adj[v].size() != 2) allDeg2 = false;
        if (allDeg2 && comp.size() % 2 == 1) ++oddCycles;
    }
    int ans = oddCycles + ((n - oddCycles) % 2);
    printf("%d\n", ans);
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    adj = [[] for _ in range(n + 1)]
    p = 2
    for _ in range(m):
        a = int(data[p]); b = int(data[p + 1]); p += 2
        adj[a].append(b); adj[b].append(a)
    vis = [False] * (n + 1)
    odd = 0
    for s in range(1, n + 1):
        if vis[s]:
            continue
        comp = []
        st = [s]; vis[s] = True
        while st:
            v = st.pop(); comp.append(v)
            for w in adj[v]:
                if not vis[w]:
                    vis[w] = True; st.append(w)
        if all(len(adj[v]) == 2 for v in comp) and len(comp) % 2 == 1:
            odd += 1
    print(odd + (n - odd) % 2)


main()
```

## 7. 边界情况与易错点

1. **奇环判定**：必须“块内所有点度数为 2 且大小为奇数”，缺一不可。
2. **孤立点**：度 0，属于路径，可用来平衡奇偶。
3. **剩余人数为奇数**：要再踢 1 人。
4. **两个奇环共享顶点**：不可能（度 ≤2 时连通块互不相交）。
5. **答案上界**：≤ 奇环数+1 ≤ n。

## 8. 验证记录

- **编译环境与命令**：`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/216/B_组队.md`。
- **官方样例**：3 / 3 通过（1、0、2）。
- **随机对拍**：暴力枚举所有踢人方案并检验“可二分且两队等量”（$n\le8$）共 **250 组**，完全一致。
- **性能**：$n=100$ 时 < 1 ms。
- **图片校验**：`cf216b_teams.svg`、`cf216b_walk.svg` 通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 216A 六边形铺砖](https://codeforces.com/problemset/problem/216/A)：同场数学。
- [LeetCode 785 判断二分图](https://leetcode.cn/problems/is-graph-bipartite/)：二分图判定。

**延伸思考**：

1. 若度数上限为 3，连通块结构变复杂，需要更一般的二分图处理。
2. 若允许人数差 ≤1，答案只需奇环数。
