# Codeforces 301B Yaroslav and Time 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/301/B
- **比赛来源**：Codeforces Round 182 (Div. 1) · Problem B（UTC 2013-05-04）
- **难度**：2100
- **标签**：二分、图论
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个站点（坐标为整点），从 1 出发要到 $n$。移动耗时 $d \times \text{曼哈顿距离}$；**首次**到达站点 $i$（$2 \le i \le n-1$）时计时器加上 $a_i$。计时器任何时刻不能为负（到 0 即失败）。求初始计时器的最小值。

**约束**：$n \le 100$，$d \le 10^5$，坐标 $|x|,|y| \le 100$。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 1000
1000
0 0
0 1
0 3

输出：
2000
```

官方样例 2：

```text
输入：
3 1000
1000
1 0
1 1
1 2

输出：
1000
```

**观察 1（单调性）**：初始时间 $T$ 越大越容易成功 → 可**二分** $T$。

**观察 2（给定 $T$ 的可行性）**：维护 `best[v]` = 到达 $v$ 时的最大剩余时间。转移：

$$\text{best}[v] \leftarrow \max\bigl(\text{best}[u] - d\cdot\text{dist}(u,v) + a_v\bigr),\quad \text{要求 } \text{best}[u] - d\cdot\text{dist}(u,v) \ge 0.$$

只要 `best[n]` 可达即可行；每次取当前剩余时间最大的未访问点松弛（$n$ 很小，$O(n^2)$ 即可）。

**样例 1 验证**：$T=2000$：$1\to2$ 花 1000 剩 1000，加 $a_2=1000$ → 2000；$2\to3$ 花 2000 剩 0 ✓ 可达 → 2000 ✓。

## 3. 解题思路

![二分 + 最大化剩余时间](../../../images/cf301b_binary.svg)

二分答案 + $O(n^2)$ 松弛判定。

## 4. 正确性证明

**引理 1**：固定 $T$ 时，若存在可行路径则上述松弛过程会把 `best[·]` 更新到"该点可达且剩余时间最大"。

**证明**：每条边上的剩余时间单调（先减后加，且加在到达时），故到达某点时"剩余时间越大越好"；按下界（非负）过滤后做最长路松弛即可 ✓（边长非正、点权非负，$O(n^2)$ 松弛足够）。∎

**引理 2**：答案关于 $T$ 单调，二分正确。

**证明**：$T$ 增大时所有 $T$ 下的可行路径仍可行 ✓。∎

**定理**：输出为最小初始时间。

**证明**：二分找到最小可行 $T$；由引理 1 判定正确 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n^2 \log(\text{范围}))$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 2 s，$n = 100$ 实测端到端 3.0 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int n; ll d;
vector<ll> a, xs, ys;
bool can(ll T){
    // 从 1 出发，dist[v] = 到达 v 时的最大剩余时间
    vector<ll> best(n+1, LLONG_MIN);
    vector<char> done(n+1, 0);
    best[1] = T;
    for(int it=0; it<n; it++){
        int u=-1;
        for(int v=1;v<=n;v++) if(!done[v] && best[v]!=LLONG_MIN && (u<0 || best[v]>best[u])) u=v;
        if(u<0) break;
        done[u]=1;
        for(int v=1;v<=n;v++){
            if(done[v] || v==u) continue;
            ll cost = d * (llabs(xs[u]-xs[v]) + llabs(ys[u]-ys[v]));
            if(best[u] - cost < 0) continue;             // 途中必须 >= 0
            ll arr = best[u] - cost + (v==n ? 0 : a[v]);
            if(arr > best[v]) best[v] = arr;
        }
    }
    return done[n] || best[n] != LLONG_MIN;
}
int main(){
    if(scanf("%d %lld",&n,&d)!=2) return 0;
    a.assign(n+1,0); xs.assign(n+1,0); ys.assign(n+1,0);
    for(int i=2;i<=n-1;i++) scanf("%lld",&a[i]);
    for(int i=1;i<=n;i++) scanf("%lld %lld",&xs[i],&ys[i]);
    ll lo=0, hi=(ll)1e15;
    while(lo<hi){
        ll mid=(lo+hi)/2;
        if(can(mid)) hi=mid; else lo=mid+1;
    }
    printf("%lld\n", lo);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, d = int(data[0]), int(data[1])
    a = [0]*(n+1)
    for i in range(2, n):
        a[i] = int(data[2 + (i-2)])
    base = 2 + (n-2)
    xs = [0]*(n+1); ys = [0]*(n+1)
    for i in range(1, n+1):
        xs[i] = int(data[base + 2*(i-1)]); ys[i] = int(data[base + 2*(i-1) + 1])
    def can(T):
        best = [None]*(n+1)
        done = [False]*(n+1)
        best[1] = T
        for _ in range(n):
            u = -1
            for v in range(1, n+1):
                if not done[v] and best[v] is not None and (u < 0 or best[v] > best[u]):
                    u = v
            if u < 0: break
            done[u] = True
            for v in range(1, n+1):
                if done[v] or v == u: continue
                cost = d * (abs(xs[u]-xs[v]) + abs(ys[u]-ys[v]))
                if best[u] - cost < 0: continue
                arr = best[u] - cost + (0 if v == n else a[v])
                if best[v] is None or arr > best[v]: best[v] = arr
        return done[n]
    lo, hi = 0, 10**15
    while lo < hi:
        mid = (lo + hi)//2
        if can(mid): hi = mid
        else: lo = mid + 1
    print(lo)
main()
```

## 7. 边界情况与易错点

1. **必须允许"跳过中间站"直接到 $n$**。
2. **到达 $n$ 不再加 $a_n$**（题面只给 $a_2..a_{n-1}$）。
3. **剩余时间为 0 时仍可继续**（≥0 即可）。
4. **二分上界**：足够大（如 $10^{15}$）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（2000、1000），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版枚举**所有简单路径**（任意子集与顺序）计算所需初始时间。随机 200 组 $n \le 5$，**200 / 200 全部一致**（我最初写的暴力只枚举"访问全部中间站"的路径，被程序反杀后修正为枚举所有子集）。
- **最大约束性能**：$n = 100$，实测端到端 3.0 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 301A Yaroslav and Sequence](https://codeforces.com/problemset/problem/301/A)：同场 A 题。
- [LeetCode 1928. 规定时间内到达终点的最小花费](https://leetcode.cn/problems/minimum-cost-to-reach-destination-in-time/)：时间/代价双约束的同类题。

**延伸思考**：

1. **如果同一站可以反复加时间**：问题变成正环检测。
2. **如果要求恰好经过 k 站**：加一维状态。
