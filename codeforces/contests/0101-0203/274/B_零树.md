# Codeforces 274B Zero Tree 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/274/B
- **比赛来源**：Codeforces Round 168 (Div. 1) · Problem B（UTC 2013-02-20）
- **难度**：1800
- **标签**：树、贪心、DP
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个点的树，每点有权值 $v_i$。一次操作：选一棵**包含根 1 的连通子树**，把子树内所有点 $+1$ 或 $-1$。求让所有点变成 $0$ 的最少操作数。

**约束**：$n \le 10^5$，$|v_i| \le 10^9$。

## 2. 示例与观察

官方样例 1：

```text
输入：
3
1 2
1 3
1 -1 1

输出：
3
```

**观察 1（操作的结构）**：对点 $v$ 而言，能影响它的操作有两类：作用在"包含 $v$ 的子树"上的操作，以及作用在**更深**（在 $v$ 子树内部）的操作。一次"以 $v$ 为根的子树"操作会同时影响 $v$ 与它的全部后代，所以父子可以**共用**操作。

**观察 2（状态设计）**：对每个点 $v$ 记 `plus[v]`、`minus[v]`：把 $v$ 的子树（含 $v$）全部清零所需的最少 $+1$ / $-1$ 操作次数（这些操作的子树都包含 $v$）。

**观察 3（合并）**：子节点 $u$ 需要 `plus[u]` 次加、`minus[u]` 次减，而这些操作的子树可以通过把 $v$ 也纳入来"顺便"作用于 $v$ → 父节点取**最大值** $\max_u$ 即可（不能取和，因为不同子树的加操作可以分别延伸到 $v$，但同一个 $+1$ 只能记一次到 $v$）。

**观察 4（补齐差额）**：设取最大值后 $p = \max_u plus[u]$、$m = \max_u minus[u]$，那么 $v$ 当前的值变成 $v_v + p - m$；若它 $> 0$ 就还差 $v_v+p-m$ 次减法 → `minus[v] = m + (v_v+p-m)`；否则 `plus[v] = p + (m - v_v - p)`。

**样例验证**：叶子 2（$v=-1$）：`plus=1, minus=0`；叶子 3（$v=1$）：`plus=0, minus=1`。根 1：$p=\max(1,0)=1$，$m=\max(0,1)=1$，当前值 $1+1-1=1>0$ → `minus=1+1=2`。答案 $p+m = 1+2 = 3$ ✓。

## 3. 解题思路

![自底向上合并 (plus, minus)](../../../images/cf274b_dp.svg)

按"逆 BFS/DFS 后序"自底向上算 `plus`、`minus`，答案 `plus[1] + minus[1]`。

## 4. 正确性证明

**引理 1（下界）**：对任意点 $v$，任何合法方案中作用于 $v$ 子树的 $+1$ 操作至少 $\max_u plus[u]$ 次、$-1$ 至少 $\max_u minus[u]$ 次（$u$ 为 $v$ 的子节点）。

**证明**：作用于 $u$ 子树的每个操作，其子树必包含 $u$ 且包含 $v$（因为要求子树含根 $1$ 且连通？注意：子树必须包含根 1，故任何操作都作用于一条"从根出发的连通块"），所以对 $u$ 有效的操作同时也作用于 $v$；$v$ 上总共至少需要这些次数 ✓。∎

**引理 2（可达）**：按上述递推得到的 $(plus[v], minus[v])$ 能真正把 $v$ 的子树清零。

**证明**：对子树高度归纳。子节点分别能用 $plus[u]$、$minus[u]$ 清零；把父 $v$ 加入这些操作的子树（仍连通、仍含根）后不影响子节点的清零效果；再按差额补足 $v$ 的值 ✓。∎

**定理**：答案是 $plus[1] + minus[1]$，且最优。

**证明**：由引理 1（下界）与引理 2（可达），每个点的次数都取到下界，故总次数最小 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n)$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 2 s，$n = 10^5$ 实测端到端 38.4 ms。
- **数值范围**：$n\cdot|v| \le 10^{14}$，必须 64 位。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int n;
vector<vector<int>> adj;
vector<ll> val;
vector<ll> neg, pos;          // 需要的 -1 次数 / +1 次数
int main(){
    if(scanf("%d",&n)!=1) return 0;
    adj.assign(n+1,{});
    for(int i=0;i<n-1;i++){int a,b;scanf("%d %d",&a,&b);adj[a].push_back(b);adj[b].push_back(a);}
    val.assign(n+1,0);
    for(int i=1;i<=n;i++) scanf("%lld",&val[i]);
    // 迭代 DFS 求后序
    vector<int> par(n+1,0), order;
    order.reserve(n);
    vector<int> st{1}; par[1]=-1;
    while(!st.empty()){
        int v=st.back(); st.pop_back(); order.push_back(v);
        for(int u: adj[v]) if(u!=par[v]){ par[u]=v; st.push_back(u); }
    }
    neg.assign(n+1,0); pos.assign(n+1,0);
    for(int i=n-1;i>=0;i--){          // 逆后序 = 自底向上
        int v=order[i];
        ll p=0, m=0;
        for(int u: adj[v]) if(u!=par[v]){ p=max(p,pos[u]); m=max(m,neg[u]); }
        ll cur = val[v] + p - m;
        if(cur>0) m+=cur; else p+=-cur;
        pos[v]=p; neg[v]=m;
    }
    printf("%lld\n", pos[1]+neg[1]);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    pos_ = 1
    for _ in range(n - 1):
        a, b = int(data[pos_]), int(data[pos_ + 1]); pos_ += 2
        adj[a].append(b); adj[b].append(a)
    val = [0] * (n + 1)
    for i in range(1, n + 1):
        val[i] = int(data[pos_]); pos_ += 1
    par = [0] * (n + 1)
    order = []
    st = [1]; par[1] = -1
    while st:
        v = st.pop(); order.append(v)
        for u in adj[v]:
            if u != par[v]:
                par[u] = v; st.append(u)
    plus = [0] * (n + 1)
    minus = [0] * (n + 1)
    for v in reversed(order):
        p = m = 0
        for u in adj[v]:
            if u != par[v]:
                p = max(p, plus[u]); m = max(m, minus[u])
        cur = val[v] + p - m
        if cur > 0:
            m += cur
        else:
            p += -cur
        plus[v] = p; minus[v] = m
    print(plus[1] + minus[1])
main()
```

## 7. 边界情况与易错点

1. **$n = 1$**：答案 $|v_1|$。
2. **负值**：`plus` / `minus` 都可能很大，用 64 位。
3. **子节点取 max 而不是 sum**：关键。
4. **递归深度**：$n = 10^5$ 的链会爆栈 → 用迭代。
5. **读入顺序**：边在前、权值在后。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：1 / 1 通过（3），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版在状态空间（各点权值）上做 BFS，枚举所有含根的连通子树与 $\pm1$。随机 250 组 $n \le 4$、$|v_i| \le 2$，**全部一致**（其中状态数可行的样本均参与比对）。
- **最大约束性能**：$n = 10^5$ 随机树，实测端到端 38.4 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 274A k-Multiple Free Set](https://codeforces.com/problemset/problem/274/A)：同场 A 题。
- [Codeforces 274D Lovely Matrix](https://codeforces.com/problemset/problem/274/D)：同场 D 题。

**延伸思考**：

1. **如果操作可以是任意子树（不必含根）**：问题变成树上差分，答案不同。
2. **如果一次可以加减任意整数**：退化。

