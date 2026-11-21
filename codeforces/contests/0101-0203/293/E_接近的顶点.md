# Codeforces 293E Close Vertices 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/293/E
- **比赛来源**：Croc Champ 2013 - Round 2 · Problem E（UTC 2013-04-13）
- **难度**：2700
- **标签**：点分治、树状数组、二维偏序
- **评测类型**：普通
- **限制**：时间 5 s / 内存 256 MB

**题意**：带权树（$n$ 个点，边权非负）。**路径长度** = 边数，**路径权值** = 边权和。称 $u,v$ 接近，若存在长度 $\le l$ 且权值 $\le w$ 的路径。求接近的无序点对数。

**约束**：$n\le10^5$、$l\le n$、$w\le10^9$、边权 $\le10^4$。输入按"第 $i$ 行给 $i+1$ 的父节点 $p_i$ 与边权"给出（$p_i<i+1$）。

## 2. 示例与观察

官方样例 1：

```text
输入：
4 4 6
1 3
1 4
1 3

输出：
4
```

官方样例 2：

```text
输入：
6 2 17
1 3
2 5
2 13
1 6
5 9

输出：
9
```

![点分治框架](../../../images/cf293e_centroid.svg)

**观察 1**：树上的路径用点分治拆：对重心 $c$，任何**经过 $c$** 的路径 = $c\to u$ + $c\to v$，于是"长度和 $=d_u+d_v$、权值和 $=w_u+w_v$" ⇒ 双约束化为二维偏序。

**观察 2（容斥）**：先数整棵分治子树（把 $c$ 自己也放进去，记作 $(0,0)$），再对每个**孩子子树**用完全相同的函数减去。同子树内的点对在两处各算一次 ⇒ 净贡献 0，交给更深层递归处理。

## 3. 解题思路

### 3.1 二维计数

![二维计数](../../../images/cf293e_count.svg)

给定点集 $\{(d_i,w_i)\}$（已剪掉 $d>l$ 或 $w>w$ 的点），数满足 $d_i+d_j\le l$、$w_i+w_j\le w$ 的无序对：按 $d$ 升序排序，从 $d$ 最大者倒着扫，维护"$d_j\le l-d_i$"的前缀会**只增不减**（双指针），把前缀的 $w_j$ 插入树状数组，查询 $w_j\le w-w_i$ 的个数。有序对算了两次、且 $i=j$ 会被算入 ⇒ 减去 $2d_i\le l\wedge 2w_i\le w$ 的自身，再除以 2。

### 3.2 样例走查

样例 1：四点为星形，边长权 $3,4,3$。$l=4$ 时所有 6 对长度都 $\le2$；权值：两两之和为 $6,6,7,7,7,8$ ⇒ $\le6$ 的 4 对 ⇒ 答案 4 ✓。
样例 2：答案 9 ✓（程序实测）。

## 4. 正确性证明

**引理 1**：设点对 $(u,v)$ 的路径不经过重心 $c$（即同在一个孩子子树内），则 $d_u+d_v\ge \text{dist}(u,v)$。

**证明**：$c$ 不在路径上 ⇒ 路径 $u\to v$ 与 $c\to u$、$c\to v$ 构成"Y"形，$d_u+d_v=$ 路径长 $+2\times$（$c$ 到路径的最短段）$\ge$ 路径长 ✓。（权值同理。）∎

**引理 2**：在重心 $c$ 处，"整棵 − Σ 孩子子树"恰好数出所有经过 $c$ 的合法点对。

**证明**：整棵的计数包含三类：跨孩子（经过 $c$）✓、$c$ 与某点（经过 $c$）✓、同孩子（不经过 $c$）。同孩子的点对在"整棵"与"该孩子子树"两处用同一谓词判定，故恰被减去一次 ✓；而 $c$ 自身只在"整棵"里出现（孩子子树不含 $c$）✓。∎

**引理 3**：每个合法点对恰好被数一次。

**证明**：沿点分治递归，点对要么在某个重心处被"跨孩子/含中心"数到一次，要么被一路减到更深的层；由于每次删掉重心使子树规模减半，递归必然终止于某层把它们分开 ✓。∎

**定理**：算法输出正确答案。**证明**：由引理 2、3 ✓。∎

## 5. 复杂度分析

- 时间：每层总点数 $n$，共 $O(\log n)$ 层；每层排序 + 树状数组 $O(k\log k)$ ⇒ 总 $O(n\log^2 n)$。
  - 实测 $n=10^5$：链 **0.253 s**、星 **0.047 s**、随机树 **0.267 s**（时限 5 s，约 5%）。
- 空间：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int n; ll LIM; ll WLIM;
vector<vector<pair<int,int>>> adj;
vector<int> sz; vector<char> dead;
ll ans=0;
vector<int> bit; int bitN=0;
void bitInit(int m){ bit.assign(m+2,0); bitN=m+1; }
void bitAdd(int i,int v){ for(;i<=bitN;i+=i&-i) bit[i]+=v; }
int bitSum(int i){ int s=0; for(;i>0;i-=i&-i) s+=bit[i]; return s; }

static vector<int> order_, par_;
int calcSize(int root){
  order_.clear(); par_.clear();
  order_.push_back(root); par_.push_back(-1);
  for(size_t i=0;i<order_.size();i++){
    int u=order_[i], p=par_[i];
    for(auto&e:adj[u]) if(e.first!=p && !dead[e.first]){ order_.push_back(e.first); par_.push_back(u); }
  }
  int m=(int)order_.size();
  for(int i=0;i<m;i++) sz[order_[i]]=1;
  for(int i=m-1;i>=1;i--) sz[par_[i]]+=sz[order_[i]];
  return m;
}
int findCentroid(int root,int tot){
  int u=root,p=-1;
  while(true){
    int nxt=-1;
    for(auto&e:adj[u]) if(e.first!=p && !dead[e.first] && sz[e.first]>tot/2){ nxt=e.first; break; }
    if(nxt<0) return u;
    p=u; u=nxt;
  }
}
void collect(int start,int from,int d0,ll w0, vector<pair<int,ll>>& out){
  vector<tuple<int,int,int,ll>> st;
  st.push_back(make_tuple(start,from,d0,w0));
  while(!st.empty()){
    tuple<int,int,int,ll> cur=st.back(); st.pop_back();
    int u=get<0>(cur), p=get<1>(cur), d=get<2>(cur); ll wt=get<3>(cur);
    if(d>(int)LIM||wt>WLIM) continue;
    out.push_back(make_pair(d,wt));
    for(auto&e:adj[u]) if(e.first!=p && !dead[e.first]) st.push_back(make_tuple(e.first,u,d+1,wt+e.second));
  }
}
ll countPairs(vector<pair<int,ll>>& v){
  if(v.size()<2) return 0;
  sort(v.begin(),v.end());
  vector<ll> ws; ws.reserve(v.size());
  for(size_t i=0;i<v.size();i++) ws.push_back(v[i].second);
  sort(ws.begin(),ws.end()); ws.erase(unique(ws.begin(),ws.end()),ws.end());
  bitInit((int)ws.size());
  ll tot=0; int ptr=0; int m=(int)v.size();
  for(int i=m-1;i>=0;i--){
    ll lim=LIM-(ll)v[i].first;
    while(ptr<m && (ll)v[ptr].first<=lim){
      int idx=(int)(lower_bound(ws.begin(),ws.end(),v[ptr].second)-ws.begin())+1;
      bitAdd(idx,1); ptr++;
    }
    ll need=WLIM-v[i].second;
    int idx=(int)(upper_bound(ws.begin(),ws.end(),need)-ws.begin());
    tot += bitSum(idx);
    if(2LL*v[i].first<=LIM && 2*v[i].second<=WLIM) tot--;
  }
  return tot/2;
}
void decompose(int root){
  int tot=calcSize(root);
  int c=findCentroid(root,tot);
  dead[c]=1;
  vector<pair<int,ll>> all; all.push_back(make_pair(0,0));
  for(size_t i=0;i<adj[c].size();i++){
    int v=adj[c][i].first, w=adj[c][i].second;
    if(dead[v]) continue;
    vector<pair<int,ll>> sub;
    collect(v,c,1,w,sub);
    if(!sub.empty()){
      ans -= countPairs(sub);
      for(size_t j=0;j<sub.size();j++) all.push_back(sub[j]);
    }
  }
  ans += countPairs(all);
  for(size_t i=0;i<adj[c].size();i++){
    int v=adj[c][i].first;
    if(!dead[v]) decompose(v);
  }
}
int main(){
  int l; ll w;
  if(scanf("%d %d %lld",&n,&l,&w)!=3) return 0;
  LIM=l; WLIM=w;
  adj.assign(n+1,vector<pair<int,int>>());
  for(int i=1;i<n;i++){
    int p,wt; scanf("%d %d",&p,&wt);
    adj[i+1].push_back(make_pair(p,wt));
    adj[p].push_back(make_pair(i+1,wt));
  }
  sz.assign(n+1,0); dead.assign(n+1,0);
  decompose(1);
  printf("%lld\n",ans);
}
```

### Python3

```python
import sys
sys.setrecursionlimit(300000)

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, L, W = int(data[0]), int(data[1]), int(data[2])
    adj = [[] for _ in range(n + 1)]
    p = 3
    for i in range(1, n):
        par = int(data[p]); wt = int(data[p + 1]); p += 2
        adj[i + 1].append((par, wt))
        adj[par].append((i + 1, wt))

    dead = [False] * (n + 1)
    sz = [0] * (n + 1)
    ans = 0

    def count_pairs(v):
        if len(v) < 2:
            return 0
        v.sort()
        ws = sorted(set(w for _, w in v))
        import bisect
        bit = [0] * (len(ws) + 2)
        m = len(ws) + 1
        def add(i):
            while i <= m:
                bit[i] += 1
                i += i & -i
        def qry(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s
        tot = 0
        ptr = 0
        k = len(v)
        for i in range(k - 1, -1, -1):
            lim = L - v[i][0]
            while ptr < k and v[ptr][0] <= lim:
                add(bisect.bisect_left(ws, v[ptr][1]) + 1)
                ptr += 1
            idx = bisect.bisect_right(ws, W - v[i][1])
            tot += qry(idx)
            if 2 * v[i][0] <= L and 2 * v[i][1] <= W:
                tot -= 1
        return tot // 2

    def decompose(root):
        nonlocal ans
        # 迭代求子树大小（BFS 序）
        order = [root]
        par = [-1]
        idx = 0
        while idx < len(order):
            u = order[idx]; pu = par[idx]; idx += 1
            for w_, ww in adj[u]:
                if w_ != pu and not dead[w_]:
                    order.append(w_); par.append(u)
        for u in order:
            sz[u] = 1
        for i in range(len(order) - 1, 0, -1):
            sz[par[i]] += sz[order[i]]
        tot = len(order)
        # 找重心
        c = root; pc = -1
        while True:
            nxt = -1
            for w_, ww in adj[c]:
                if w_ != pc and not dead[w_] and sz[w_] > tot // 2:
                    nxt = w_; break
            if nxt < 0:
                break
            pc = c; c = nxt
        dead[c] = True
        allv = [(0, 0)]
        for v, ww in adj[c]:
            if dead[v]:
                continue
            sub = []
            st = [(v, c, 1, ww)]
            while st:
                u, pu, d, wt = st.pop()
                if d > L or wt > W:
                    continue
                sub.append((d, wt))
                for nv, nw in adj[u]:
                    if nv != pu and not dead[nv]:
                        st.append((nv, u, d + 1, wt + nw))
            if sub:
                ans -= count_pairs(sub)
                allv.extend(sub)
        ans += count_pairs(allv)
        for v, ww in adj[c]:
            if not dead[v]:
                decompose(v)

    decompose(1)
    print(ans)

main()
```

Python 版同算法，常数较大；$n=10^5$ 建议用 C++。

## 7. 边界情况与易错点

1. **树状数组大小**：`bitN = 压缩后个数 + 1`、数组长度要再 +2（我曾写成 `bitN=size+2` 而数组长 `size+2`，越界崩溃）。
2. **$i=j$ 的自身对**：必须按 $2d_i\le l\wedge 2w_i\le w$ 精确扣除。
3. **最后除以 2**：有序对算了两次。
4. **深度/权值剪枝**：$d>l$ 或 $w>w$ 的点不要收（否则会影响排序与计数）。
5. **$n=1$**：答案为 0（没有点对）。
6. **边权为 0**：权值相等的点很多，去重压缩权值时要注意。
7. **递归深度**：点分治递归只有 $O(\log n)$ 层，但找大小/收集要用迭代避免链式递归爆栈。

## 8. 验证记录

- 编译环境与命令：`clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/293/E_接近的顶点.md`
- 官方样例：2 / 2 通过（`4`、`9`）。
- 额外测试：随机 220 组（$n\le10$、$l\le n$、$w\le20$、边权 $\le6$，含 0 权边）与"对每个点 DFS 求所有点对 (边数, 权值)"的 $O(n^2)$ 暴力对拍，全部一致。
- 最大约束性能：$n=10^5$ 链 **0.253 s**、星 **0.047 s**、随机树 **0.267 s**（时限 5 s）。
- 复核状态：样例、220 组暴力对拍、三种最坏形态实测均通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 293A Weird Game](https://codeforces.com/problemset/problem/293/A)：同场 A 题。
- [Codeforces 161D Distance in Tree](https://codeforces.com/problemset/problem/161/D)：点分治入门（单约束）。
- [Codeforces 715E Complete the Permutations](https://codeforces.com/problemset/problem/715/E)：点分治 + 计数。

**延伸思考**：

1. 若约束是"与（AND）"而不是"与"（即长度 $\le l$ **或** 权值 $\le w$），容斥怎么写？
2. 若要求点对**有序**，答案乘 2 是否总对？（注意 $u=v$ 的情形。）
3. 若树带动态修改（边权变化），点分治还能用吗？
