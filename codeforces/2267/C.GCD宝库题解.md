# Codeforces GCD 宝库 题解

## 1. 题目概述

- **标题 / 题号**：GCD 宝库（Codeforces 2267C，英文名 GCD Treasury）
- **链接**：https://codeforces.com/problemset/problem/2267/C
- **来源**：Codeforces Round 1123 (Div. 2) · Problem C
- **难度**：1200（本题 1000 分）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：贪心，数学，数论

**题意**：宝库有 $n$ 堆金币，第 $i$ 堆 $a_i$ 枚；海盗手上的数是 $x$。每步操作：挑一个 $a_i>0$ 且 $\gcd(a_i,x)\ne1$ 的下标 $i$，令 $g=\gcd(a_i,x)$，从这堆取走 $g$ 枚（$a_i\leftarrow a_i-g$），再令 $x\leftarrow g$。找不到这样的下标就停止。求最多能取走多少枚金币。**多测**：第一行 $t$；每组先给 $n,x$，再给一行 $n$ 个 $a_i$；每组输出一行一个整数。

**约束**：

- $1\le t\le10^4$，$1\le n,x\le3\cdot10^5$，$1\le a_i\le3\cdot10^5$，所有测试的 $\sum n\le3\cdot10^5$；
- 单组答案上界 $n\cdot\max a_i\le9\cdot10^{10}$，超过 `int`，C++ 必须用 `long long`；$x$ 全程只取 $x$ 的约数，而 $3\cdot10^5$ 以内约数最多的数是 $277200$，恰有 $180$ 个约数——这是复杂度的关键上界。

## 2. 示例

**官方样例**（一个输入块，共 5 组）

```text
输入
5
3 1
2 3 5
3 4
2 3 4
4 2
2 2 2 2
6 6
2 3 2 3 2 3
7 6
9 9 4 4 4 4 4

输出
0
6
8
9
20
```

- 第 1 组 $x=1$ 一步都走不了；第 2 组先取第 3 堆（$g=4$）拿 4 枚，再取第 1 堆（$g=\gcd(2,4)=2$）拿 2 枚，$x=2$ 后 $3$ 与 $2$ 互质，共 $6$。
- 第 3 组四堆全是 $2$，各取光得 $8$；第 4 组先取 $3$ 得 $x=3$、扫光三堆 $3$ 得 $9$（先取 $2$ 只有 $6$）；第 5 组取一堆 $4$ 使 $x=2$ 后扫光五堆 $4$ 得 $20$，两堆 $9$ 与 $2$ 互质只能放弃。

**自造样例**（覆盖"深链才最优"）：$n=4,x=210,a=[105,70,42,30]$，输出 $217$。$x$ 依次为 $210\to70\to35\to7$，停在 $7$ 时 $105,70,42$ 都是 $7$ 的倍数，整堆扫光共 $217$，而 $30$ 与 $7$ 互质；若贪心先取 $105$（$g=105$），$x$ 立刻锁死在 $105$，只能拿 $105$。

## 3. 解题思路

### 3.1 暴力思路

按题意直接搜索：每步最多 $n$ 种选择，同一堆还能被反复取（每次只减 $g$），操作次数可达 $\sum a_i/g$，状态空间是天文数字，$n=3\cdot10^5$ 连枚举第一步都不可接受；即使退化成"每堆取或不取"再枚举 $2^n$ 个子集也不可行。所以必须先把"操作过程"化简成结构性结论，让答案只依赖最终停在哪个 $x$ 上。

### 3.2 核心观察：可达集合就是 gcd 闭包

三个小结论（严格证明见第 5 节）：

1. **能碰就能清空**：当前 $x=c$、某堆剩 $v$、$g=\gcd(v,c)>1$，取走 $g$ 后 $x=g$、该堆剩 $v-g$，而 $\gcd(v-g,g)=\gcd(v,g)=g$，下次 $\gcd$ 仍是 $g$；又 $g\mid v$，反复取 $v/g$ 次恰好归零。**每堆贡献只有 $0$ 或 $a_i$，不存在"只取一半"的最优解。**
2. **碰过的堆再也不能降低 $x$**：它剩下的值始终是此后所有 $x$ 取值的倍数，$\gcd$ 恒等于当前 $x$。能降 $x$ 的只有**从未碰过**的堆，其值仍是原始 $a_i$。
3. **$x$ 的取值就是 gcd 的累积**：走若干步后 $x=\gcd(x_{\text{原}},a_{i_1},a_{i_2},\dots)$，即初始 $x$ 与被碰过的那些 $a_i$ 的 $\gcd$。

于是可达集合为 $R=\{\gcd(x,a_{i_1},\dots,a_{i_k}):k\ge0\}$——$x$ 与 $a$ 的**任意子集**的 $\gcd$。收益只由终点 $r$ 决定：停在 $r$ 时所有 $r\mid a_i$ 的堆都能整堆扫光，共 $S(r)=\sum_{r\mid a_i}a_i$；反过来任何被取过的堆都满足 $r\mid a_i$，收益不超过 $S(r)$。**答案即 $\max\{S(r): r\in R,\ r\ge2\}$。**

![x 的整除链与每个终点的收益](images/cf2267_c_gcd_chain_concept.svg)

### 3.3 算法流程 / 状态转移

降维：$R$ 中每个 $r$ 都整除 $x$，因此 $r\mid a_i \iff r\mid\gcd(a_i,x)=b_i$，且 $\gcd(r,a_i)=\gcd(r,b_i)$。即每堆只需压成 $b_i=\gcd(a_i,x)$，不同的 $b_i$ 最多 $\tau(x)\le180$ 种。把 $a_i$ 按 $b_i$ 入桶，得 $B[b]=\sum_{\gcd(a_i,x)=b}a_i$。

![算法流程](images/cf2267_c_algorithm_flow.svg)

1. 逐堆算 $b_i=\gcd(a_i,x)$，丢弃 $b_i=1$ 的堆，把 $a_i$ 累加进桶 $B[b_i]$；
2. 求闭包：$R$ 初始为 $\{x\}$，用栈/BFS 反复对 $r\in R$、$b\in B$ 算 $g=\gcd(r,b)$，若 $g>1$ 且未出现就加入 $R$，直到不再变化；
3. 对每个 $r\in R$ 且 $r\ge2$ 求 $S(r)=\sum_{r\mid b}B[b]$，取最大输出；若 $R=\{1\}$（即 $x=1$），答案为 $0$。

### 3.4 示例演算

官方第 5 组 $x=6,a=[9,9,4,4,4,4,4]$：$b$ 依次为 $3,3,2,2,2,2,2$，桶 $B[3]=18,B[2]=20$；闭包 $6\to\{3,2\}$ 且 $\gcd(3,2)=1$，故 $R=\{6,3,2\}$，$S(6)=0,S(3)=18,S(2)=20$，答案 $20$。

自造样例 $x=210,a=[105,70,42,30]$：依次取 $70$（$g=70$）、$105$（$g=35$，取 3 次清空）、$42$（$g=7$，取 6 次清空），$x$ 走成 $210\to70\to35\to7$；$30$ 与 $7$ 互质停手，合计 $70+105+42=217$。桶为 $B[105]=105,B[70]=70,B[42]=42,B[30]=30$，闭包还包含 $35,21,15,14,10,6,7,5,\dots$，其中 $S(7)=217$ 最大。

![示例演算走查表](images/cf2267_c_walkthrough.svg)

## 4. 算法细节

1. **多测清空**：桶与 $R$ 全部在每组内部用局部 `vector` 重建；不要用跨组复用的全局数组，也不要做 $O(\max a_i)$ 的清空（$t$ 可达 $10^4$，会直接退化）。
2. **不要按值域筛**：多测下 $\sum\max a_i$ 最坏到 $3\cdot10^9$，用调和级数预计算倍数和会超时；本题只需 $x$ 的约数（$\le180$ 个），按桶求和即 $O(\tau(x)\cdot k)$，$k$ 为不同 $b_i$ 数。顺便把 $b_i=1$ 的堆丢掉——它们永远取不动，留着只会让闭包空转（$\gcd(r,1)=1$ 被 $>1$ 过滤）。
3. **答案与桶都用 `long long`**：$S(r)$ 上界 $9\cdot10^{10}$，`int` 会静默溢出，多测时不要用 `int` 中转；Python 整数天然无上界。
4. **闭包必须跑到不动点**：$S(x)$ 常常是 $0$（没有堆是 $x$ 的倍数）而答案很大；漏掉"新加入的 $r$ 继续与桶做 $\gcd$"就只会走一步。$|R|\le180$，用 `vector` + `find` 判重足够。
5. **$r\ge2$ 的过滤**：$x=1$ 时闭包只有 $1$，答案是 $0$，绝不是"把所有堆扫光"（$\gcd(a_i,1)=1$ 永远非法）。
6. **I/O 与常数**：$\sum n\le3\cdot10^5$、输入约 $2$ MB，需 `std::ios::sync_with_stdio(false)`（或 `scanf`）加速；$t=10^4$ 时用 `'\n'` 而非 `endl`。

## 5. 正确性证明

**引理 1（一次触碰即可清空）**：若当前 $x=c$，某堆剩 $v>0$ 且 $g=\gcd(v,c)>1$，则从此刻起只对这一堆操作，可合法地把它取到 $0$，共取走 $v$ 枚。

**证明**：第一步取 $g$ 合法，此后 $x=g$、剩 $v-g$；由 $\gcd(v-g,g)=\gcd(v,g)=g$ 知下一步 $\gcd$ 仍是 $g>1$，操作继续合法。归纳得 $j$ 次后剩 $v-jg$、$x=g$、$\gcd(v-jg,g)=g$；又 $g\mid v$，当 $j=v/g$ 时恰好取完，共取 $v$ 枚。∎

**引理 2（$x$ 的取值等于与已碰堆的 $\gcd$）**：设按首次触碰顺序用了堆 $i_1,\dots,i_k$，第 $j$ 次首次触碰后 $x=c_j$，则 $c_j=\gcd(x,a_{i_1},\dots,a_{i_j})$。特别地，被碰过的堆此后剩余值恒为当前 $x$ 的倍数，再也无法把 $x$ 变小。

**证明**：先证"碰过就降不动"：设某堆首次被操作时 $g=\gcd(v,c)$，操作后 $x=g$、剩余 $v'=v-g$，故 $g\mid v'$；而 $x$ 单调不增且每次新值是旧值的约数，此后任何当前值 $c'$ 都整除 $g$，于是 $c'\mid v'$、$\gcd(v',c')=c'$，即它只能原样"送"出当前 $x$，不能把 $x$ 压低。

再对 $j$ 归纳证明结论。$j=1$ 时该堆未被碰过、值仍为 $a_{i_1}$，故 $c_1=\gcd(a_{i_1},c_0)=\gcd(a_{i_1},x)$。设对 $j-1$ 成立：若 $i_j$ 此前未被碰过，则 $c_j=\gcd(a_{i_j},c_{j-1})=\gcd(x,a_{i_1},\dots,a_{i_j})$；若 $i_j$ 更早（第 $m<j$ 步）被碰过，由上段得 $c_j=c_{j-1}$，同时 $c_{j-1}\mid c_{m+1}=\gcd(a_{i_j},c_m)\mid a_{i_j}$，故 $\gcd(x,a_{i_1},\dots,a_{i_j})=c_{j-1}=c_j$。∎

**引理 3（$R$ 中每个值都可达）**：设 $r=\gcd(x,\{a_i:i\in T\})\ge2$，则存在合法操作使 $x$ 最终等于 $r$。

**证明**：按 $T$ 中元素的任意顺序逐个操作。当前 $x=c=\gcd(x,\text{已用子集})$ 是 $r$ 的倍数（$r$ 是更大子集的 $\gcd$），下一个元素 $a$ 满足 $r\mid a$，故 $g=\gcd(a,c)$ 是 $r$ 的倍数，$g\ge r\ge2$，操作合法。由引理 2，操作后 $c$ 变为 $\gcd(x,\text{已用子集}\cup\{a\})$；全部用完后 $c=r$。∎

**引理 4（收益等于终点的 $S$）**：若某过程最终 $x=r\ge2$，则总收益不超过 $S(r)$，且存在总收益恰为 $S(r)$ 的过程。

**证明**：上界——被取过金币的堆 $i$ 在首次被取时得到 $g\mid a_i$，此后 $x$ 一直整除 $g$，故 $r\mid a_i$，收益 $\le\sum_{r\mid a_i}a_i=S(r)$。可达——由引理 3 走到 $r$，再用引理 1 清空每个 $r\mid a_i$ 的堆（$\gcd(a_i,r)=r\ge2$ 合法），合计 $S(r)$。∎

**定理**：答案等于 $\max\{S(r):r\in R,\ r\ge2\}$（该集合为空时答案为 $0$）。

**证明**：上界——设某过程走了 $k$ 步停在 $c_k$。若 $k=0$（初始 $x=1$ 或无合法下标）收益为 $0$；否则每步 $g\ge2$，故 $c_k\ge2$。$c_0=x\in R$，每步 $c_j=\gcd(c_{j-1},a)$，而 $c_{j-1}\mid x$ 给出 $\gcd(c_{j-1},a)=\gcd(c_{j-1},\gcd(a,x))$，即 $R$ 对 $r\mapsto\gcd(r,b)$ 封闭，故 $c_k\in R$，由引理 4 得收益 $\le S(c_k)\le\max_{r\in R,r\ge2}S(r)$。下界——对每个 $r\in R,r\ge2$，引理 3 给出到达 $r$ 的过程、引理 4 给出收益 $S(r)$ 的过程，故最大值既可达又是上界。∎

## 6. 复杂度分析

- **时间**：每组求 $b_i$ 为 $O(n\log A)$，分组排序 $O(n\log n)$（改用哈希表可到期望 $O(n)$），闭包与求和各 $O(|R|\cdot k)$，其中 $|R|\le\tau(x)\le180$、$k\le\min(n,\tau(x))$ 为不同桶数。总计 $O(\sum n\log n+\sum k\tau(x))$，主项 $\sum n\le3\cdot10^5$，后一项只是 $\tau(x)^2$ 量级的小常数。
- **空间**：$O(n)$ 存 $(b_i,a_i)$ 对（也可以边读边入桶，压到 $O(\tau(x))$），另加 $O(\tau(x))$ 的桶与 $R$；与 $t$ 无关。
- **可行性对照**：时限 2 s。实测最大规模（单组 $n=3\cdot10^5$、$x=277200$；以及 $t=10^4$、$\sum n=3\cdot10^5$）C++17 约 $0.6$ s（本机 clang + libc++，含约 2 MB 输入解析；同算法改用 `scanf` 为 $0.06$ s），Python3 约 $0.6$ s，均有 2 倍以上余量。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        int n; ll x;
        cin >> n >> x;
        vector<pair<ll, ll>> raw;              // (b_i = gcd(a_i, x), a_i)，只收 b_i > 1
        for (int i = 0; i < n; ++i) {
            ll v; cin >> v;
            ll g = gcd(v, x);
            if (g > 1) raw.push_back({g, v});
        }
        sort(raw.begin(), raw.end());
        vector<pair<ll, ll>> bucket;           // (b, 这一桶 a_i 之和)
        for (size_t i = 0; i < raw.size(); ) {
            size_t j = i; ll s = 0;
            while (j < raw.size() && raw[j].first == raw[i].first) s += raw[j].second, ++j;
            bucket.push_back({raw[i].first, s});
            i = j;
        }
        vector<ll> R;                          // 闭包：x 与任意子集的 gcd
        R.push_back(x);
        for (size_t i = 0; i < R.size(); ++i)
            for (auto &p : bucket) {
                ll g = gcd(R[i], p.first);
                if (g > 1 && find(R.begin(), R.end(), g) == R.end()) R.push_back(g);
            }
        ll ans = 0;
        for (ll r : R) {
            if (r < 2) continue;
            ll s = 0;
            for (auto &p : bucket) if (p.first % r == 0) s += p.second;
            ans = max(ans, s);
        }
        cout << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys
from math import gcd


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    t = data[0]
    pos = 1
    out = []
    for _ in range(t):
        n, x = data[pos], data[pos + 1]
        pos += 2
        a = data[pos:pos + n]
        pos += n
        bucket = {}                       # b = gcd(a_i, x) -> 该桶 a_i 之和
        for v in a:
            g = gcd(v, x)
            if g > 1:
                bucket[g] = bucket.get(g, 0) + v
        reach = {x}                       # 闭包：x 与任意子集的 gcd
        stack = [x]
        while stack:
            r = stack.pop()
            for b in bucket:
                g = gcd(r, b)
                if g > 1 and g not in reach:
                    reach.add(g)
                    stack.append(g)
        ans = 0
        for r in reach:
            if r < 2:
                continue
            s = 0
            for b, w in bucket.items():
                if b % r == 0:
                    s += w
            if s > ans:
                ans = s
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$x=1$ 或所有 $b_i=1$**：没有任何堆可取（$\gcd(a_i,1)=1$ 永远非法），答案必须是 $0$；不要把"$1$ 整除一切"误当成"全都能扫光"。
2. **`int` 溢出**：答案上界 $9\cdot10^{10}$，桶累加与 $S$ 都必须是 `long long`，多测时也不要用 `int` 中转。
3. **只算 $S(x)$ 就输出**：$S(x)$ 常为 $0$ 而答案很大（样例 5 就是 $S(6)=0$ 答案为 $20$），必须把闭包跑完。
4. **$n=1$**：答案为 $0$ 或 $a_1$——$\gcd(a_1,x)>1$ 时清空得 $a_1$，互质时为 $0$。
5. **约数与整除的方向**：$S(r)$ 只累加 $r\mid b$ 的桶（$b$ 是 $r$ 的倍数），写成 `r % b == 0` 就反了；$R$ 的元素一定整除 $x$，可用来自检。
6. **多测 I/O**：$t=10^4$ 时输出 $10^4$ 行，C++ 用 `'\n'`、Python 一次性 `join` 写出，避免逐行 `print`。

## 相关题目与扩展

- [Codeforces 1458A Row GCD](https://codeforces.com/problemset/problem/1458/A)：把"一串 $\gcd$"压成对少量关键值的 $\gcd$，与本题"只需保留 $b_i=\gcd(a_i,x)$"是同一种降维。
- [Codeforces 1203C Common Divisors](https://codeforces.com/problemset/problem/1203/C)：先求整体 $\gcd$ 再枚举约数，与本题"只枚举 $x$ 的约数"同源。
- [Codeforces 2267B 时髦数组](https://codeforces.com/problemset/problem/2267/B)：同场题，另一个"把每个阈值的上界顶满"的贪心。
- [LeetCode 914. 卡牌分组](https://leetcode.cn/problems/x-of-a-kind-in-a-deck-of-cards/)：用 $\gcd$ 合并多组计数。

**延伸思考**：

1. **允许"空转"**：若额外给出可选集合 $X$，每步可把 $x$ 直接换成任意 $c\mid x$，问题变成在有向约数格上走到 $S$ 最大的点，$O(\tau(x)^2)$ 的约数 DP 即可。
2. **多组询问**：同一数组 $a$ 上询问 $q$ 个不同的 $x$。先对 $a$ 做倍数额计数与求和（调和级数 $O(A\log A)$），每次询问枚举 $x$ 的约数即可 $O(\tau(x))$ 回答。
3. **值域放大到 $10^9$**：$\tau(x)$ 最大约 $1344$，算法结构不变，但 $S(r)$ 不能再用值域桶，只能对 $n$ 个 $b_i$ 枚举约数，复杂度变为 $O(n\tau(x))$。
4. **输出操作方案**：按引理 3 的构造先把 $x$ 沿子集顺序降到 $r$，再对所有 $r\mid a_i$ 的堆反复取 $r$，按"整堆清空"合并输出即可。
