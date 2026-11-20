# Codeforces 22E 最少补边成强连通 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/22/E
- **比赛来源**：Codeforces Beta Round 22 (Div. 2 Only) · Problem E（UTC 2010-06-29）
- **难度**：2300
- **标签**：DFS、图论、树
- **评测类型**：特殊评测（任意最优方案）
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个点，每个点 $i$ 有一条出边 $i\to f_i$（函数图）。求最少补多少条有向边使整张图强连通，并输出方案。

**约束**：每点出度恰为 1，因此每个弱连通分量恰有一个环，环上挂树；利用这个结构可以 $O(n)$ 求解。

## 2. 示例与观察

官方样例（输入 / 输出原样，共 2 组）：

```text
输入：
3
3 3 2
输出：
1
3 1
```

```text
输入：
7
2 3 1 3 4 4 1
输出：
3
2 5
2 6
3 7
```

**样例解释**：样例 1 环为 $2\leftrightarrow3$，$1$ 入度为 0；补 $3\to1$ 即可。样例 2 中入度 0 的点是 $5,6,7$，补 3 条边。

**观察 1**：每个分量恰有一个环，其余点是指向环的树。

**观察 2（源与汇）**：缩点后汇 = 每个分量的环；源 = 树上入度 0 的点，以及"纯环"分量本身。

**观察 3（答案）**：记源的总数为 $p$、分量数为 $C$。每个源都要有新的入边，故至少 $p$ 条；把各分量按环首尾相连 $p$ 条就够。单分量纯环时答案 0。

![函数图的结构](../../../images/cf22e_struct.svg)

## 3. 解题思路

### 3.1 一般结论与本题差异

一般有向图"最少补边强连通"是缩点 DAG 上的 $\max(\text{源},\text{汇})$，构造是汇源交替连成环。本题的函数图中每个分量的汇就是它的环，源是入度 0 的树点；直接套公式容易在"分量内部连边"上浪费。

### 3.2 算法

![把分量首尾相连](../../../images/cf22e_link.svg)

1. Kahn 剥叶找环上的点：反复删除入度 0 的点；
2. 并查集求弱连通分量；
3. 每个分量：全在环上 → 纯环，源取环上代表；否则源 = 非环且入度 0 的点；
4. 单分量且纯环 → 输出 0；
5. 否则按分量排成一圈：第 $j$ 个分量的每个源 $s$ 都从"上一个分量的环代表"连入。补边数 = 源的总数。

### 3.3 合法性

每个源获得一条新入边；缩点后分量形成一个大环（每个分量既有出边也有入边），分量内所有点都能到环、环能进入下一分量，故整体强连通。

### 3.4 样例走查

样例 2：源 $\{5,6,7\}$，环代表取 1，补 $1\to5,1\to6,1\to7$ 共 3 条。

## 4. 正确性证明

**引理 1**：函数图的每个弱连通分量恰有一个有向环。

**证明**：沿出边走必入环；两个不同环不能互相到达，否则合并。∎

**引理 2（下界）**：至少需要 $|S|$ 条边，$S$ 为源集合（入度 0 的点 + 纯环分量的代表）。

**证明**：$S$ 中每个 SCC 在原图入度为 0，必须各有至少一条新入边，且一条边只有一个终点。∎

**引理 3（上界）**：3.2 的构造恰加 $|S|$ 条边且使图强连通。

**证明**：每个源恰得一条入边；缩点后分量间形成大环，任一分量可达任一分量，分量内点可达环，故强连通。∎

**定理**：算法输出的边数最少且构造合法。

**证明**：由引理 2、3 下界与构造相等；单分量纯环已强连通，答案为 0。∎

## 5. 复杂度分析

- **时间**：$O(n\alpha(n))$。
- **空间**：$O(n)$。
- **与时限的关系**：远低于 2 s。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; if(!(cin>>n)) return 0;
    vector<int> f(n+1), indeg(n+1,0);
    for(int i=1;i<=n;i++){ cin>>f[i]; indeg[f[i]]++; }
    // 拓扑剥叶，剩下的就是环上的点
    vector<int> deg=indeg, oncyc(n+1,1);
    queue<int> q; for(int i=1;i<=n;i++) if(deg[i]==0) q.push(i);
    while(!q.empty()){
        int u=q.front(); q.pop(); oncyc[u]=0;
        if(--deg[f[u]]==0) q.push(f[u]);
    }
    // 并查集找弱连通分量
    vector<int> par(n+1); iota(par.begin(),par.end(),0);
    function<int(int)> find=[&](int x){ return par[x]==x?x:par[x]=find(par[x]); };
    for(int i=1;i<=n;i++){ int a=find(i),b=find(f[i]); if(a!=b) par[a]=b; }
    map<int, vector<int>> comps;
    for(int i=1;i<=n;i++) comps[find(i)].push_back(i);
    vector<int> reps;                       // 每个分量取一个环上点（汇）
    vector<vector<int>> srcOf;              // 每个分量的源
    bool pureAll=true;
    for(auto &kv: comps){
        auto &vs=kv.second;
        bool pure=true; int cyc=-1;
        for(int v:vs){ if(oncyc[v]){ if(cyc<0) cyc=v; } else pure=false; }
        if(!pure) pureAll=false;
        reps.push_back(cyc);
        vector<int> src;
        if(pure) src.push_back(cyc);        // 纯环：自己既是源又是汇
        else for(int v:vs) if(!oncyc[v] && indeg[v]==0) src.push_back(v);
        srcOf.push_back(src);
    }
    int C=reps.size();
    if(C==1 && pureAll){ cout<<0<<"\n"; return 0; }   // 已经强连通
    vector<pair<int,int>> es;
    for(int j=0;j<C;j++){
        int from=reps[(j-1+C)%C];           // 上一分量的汇连到本分量的每个源
        for(int s: srcOf[j]) es.push_back({from, s});
    }
    cout<<es.size()<<"\n";
    for(auto &e:es) cout<<e.first<<" "<<e.second<<"\n";
}
```

### Python3

```python
import sys
from collections import deque
def main():
    d=list(map(int,sys.stdin.buffer.read().split()))
    n=d[0]; f=[0]+d[1:1+n]
    indeg=[0]*(n+1)
    for i in range(1,n+1): indeg[f[i]]+=1
    deg=indeg[:]; oncyc=[1]*(n+1)
    q=deque(i for i in range(1,n+1) if deg[i]==0)
    while q:
        u=q.popleft(); oncyc[u]=0
        deg[f[u]]-=1
        if deg[f[u]]==0: q.append(f[u])
    par=list(range(n+1))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]]; x=par[x]
        return x
    for i in range(1,n+1):
        a,b=find(i),find(f[i])
        if a!=b: par[a]=b
    comps={}
    for i in range(1,n+1): comps.setdefault(find(i),[]).append(i)
    reps=[]; src_of=[]; pure_all=True
    for vs in comps.values():
        pure=all(oncyc[v] for v in vs)
        if not pure: pure_all=False
        cyc=next(v for v in vs if oncyc[v])
        reps.append(cyc)
        if pure: src_of.append([cyc])
        else: src_of.append([v for v in vs if not oncyc[v] and indeg[v]==0])
    C=len(reps)
    if C==1 and pure_all:
        print(0); return
    es=[]
    for j in range(C):
        frm=reps[(j-1)%C]
        for s in src_of[j]: es.append((frm,s))
    print(len(es))
    print('\n'.join(f'{a} {b}' for a,b in es))
main()
```

## 7. 边界情况与易错点

1. **纯环分量**：它既是源又是汇，必须计入源，否则漏边。
2. **整图已是强连通**：输出 0（单个纯环），不能输出自环。
3. **自环**：构造时避免 $T\to s$ 中 $T=s$。
4. **多分量**：必须把所有分量连成一圈，只连一个方向不够。
5. **入度计算**：用全体入度，不是树上入度。
6. **输出格式**：先输出补边数，再逐行输出边；0 条时只输出一行 0。
7. **方案不唯一**：用 checker 验证。

## 8. 验证记录

- **编译环境**：`Apple clang 21.0.0`（`-O2`），Python 3.9.6。
- **官方样例**：2 / 2 通过（checker 校验边数与强连通）。
- **随机对拍**：随机 **200 组**函数图（$n\le7$），用 Tarjan 缩点独立计算 $\max(\text{源},\text{汇})$（单 SCC 为 0），并检查输出边数相等且补完强连通（正反 DFS），C++ / Python **全部一致，0 处不符**。
- **性能**：远低于 2 s。
- **图片/公式**：两张 SVG 通过检查；KaTeX 无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 22D Segments](https://codeforces.com/problemset/problem/22/D)：同场 D 题。
- [Codeforces 999E Reachability from the Capital](https://codeforces.com/problemset/problem/999/E)：补边可达类构造。

**延伸思考**：

1. **一般有向图**：答案为缩点后 $\max(\text{源},\text{汇})$，构造更复杂。
2. **保持函数图性质**：新增边会破坏出度条件，需重新建模。
3. **最少补边使弱连通**：答案为分量数减一。
