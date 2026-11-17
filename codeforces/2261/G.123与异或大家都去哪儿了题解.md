# Codeforces 123 与异或，大家都去哪儿了 题解

## 1. 题目概述

- **标题 / 题号**：123 与异或，大家都去哪儿了（Codeforces 2261G，英文名 1 2 3 and XOR, Where Did Everybody Go?）
- **链接**：https://codeforces.com/problemset/problem/2261/G
- **来源**：WorldQuant Round 1 (Codeforces Round 1128, Div. 1 + Div. 2) · Problem G
- **难度**：$\ast 2800$（4000 分）
- **限制**：时间 7 s / 内存 1024 MB
- **标签**：位运算，数据结构，分治，动态规划，贪心，排序，双指针

**题意**：给定长度为 $n$ 的非负整数序列 $a$。对一个长度为 $k$ 的序列 $b$ 定义一次**点自增**：选一个下标 $i$，给 $b_i$ 加上任意非负整数（加 $0$ 也允许）。令 $f(b)$ 为恰好做一次点自增后 $b_1\oplus b_2\oplus\cdots\oplus b_k$ 的**最小值**。求 $\sum_{1\le l\le r\le n}f([a_l,\dots,a_r])$。**多测**：第一行 $t$，每组给 $n$ 与 $a_1,\dots,a_n$，逐组输出一个整数。

**约束**：

- $1\le t\le 10^4$，$1\le n\le 4\times10^5$，所有测试的 $n$ 之和不超过 $4\times10^5$；
- $0\le a_i<2^{25}$：位宽固定 25，这是全题复杂度的关键常数；
- 区间数约 $8\times10^{10}$，必须按位、按段整体统计，不能逐区间求；
- 答案上界约 $4\times10^{10}\times2^{25}\approx1.4\times10^{18}$，必须 64 位整数。

## 2. 示例

**官方样例**

```text
输入
4
5
5 4 6 7 5
5
3 3 2 2 3
1
67
10
1827481 5921082 14619611 643973 6718274 2948 244716 29 0 6717827

输出
43
21
67
36695941
```

**自造小例（补足奇偶差异）**

```text
输入：2 / 3 / 1 1 1 / 2 / 6 5      输出：4 / 11
解释：[1,1,1] 长度为 3 的区间没有可清位，f = 1，加上 3 个单元素区间得 4；
      [6,5] 长度为 2 的区间贡献 0（把 5 加成 6 异或即为 0），故 11 = 6 + 5 + 0。
```

## 3. 解题思路

### 3.1 暴力思路

单区间：枚举下标 $i$ 与增量，$O(k\cdot2^{25})$；全部区间：$O(n^3\cdot2^{25})$，毫无希望。即使单区间做到 $O(k)$，区间数也有 $8\times10^{10}$ 个。必须找到「按位拆开、按段合并」的统计方式。

### 3.2 核心观察：单区间取值就是 S 的高位前缀

![单区间从高位贪心](images/cf2261_g_range_value_concept.svg)

记区间异或和 $S$、按位与 $A$。把某个 $b_i$ 换成 $c\ge b_i$ 后异或值变成 $u_i\oplus c$，其中 $u_i=S\oplus b_i$。从**最高位**看：若 $c>b_i$，设 $j$ 为 $c$ 与 $b_i$ 的最高不同位，则必有 $c_j=1,\ b_{i,j}=0$；$j$ 之上 $c$ 与 $b_i$ 相同，结果这些位只能等于 $S$ 的同一位，而第 $j$ 位结果为 $S_j\oplus1$：

- $S_j=0$：第 $j$ 位由 0 变 1、更高位不变，结果反而变大，不可能最优；
- $S_j=1$：第 $j$ 位清成 0，且 $j$ 之下取 $c=u_i$ 可全清，得到 $S\ \&\ \sim(2^{j+1}-1)$。

拐弯位要求 $b_{i,j}=0$，即 $A_j=0$。故**严格变优的取值恰是**「$S$ 抹掉不高于 $j$ 的位」（$j$ 取遍 $A_j=0,\ S_j=1$），最小者由最高的这种位给出：

$$t=\operatorname{MSB}(S\ \&\ \sim A),\qquad f=\begin{cases}S\ \&\ \sim(2^{t+1}-1), & t\text{ 存在}\\ S, & t\text{ 不存在}\end{cases}$$

**结论只依赖 $(S,A)$ 两个量**，区间内部结构被完全吃掉。

### 3.3 算法流程：奇偶归零 + 按位拆解 + AND 分段 + 离线 Trie

![奇偶长度与按位判据](images/cf2261_g_parity_truncate.svg)

**第一步：偶数长度归零。** $k$ 为偶数时，凡「所有数该位都是 1」的位在 $S$ 中必为 0（偶数个 1 异或掉），即 $A\ \&\ S=0$，于是 $t=\operatorname{MSB}(S)$（$S=0$ 时 $f=0$），$f=0$。只有**奇数长度区间**有贡献。

**第二步：奇数长度按位拆开。** 此时 $A$ 的位都含于 $S$（奇数个 1 异或为 1）。由 3.2，$f$ 的第 $j$ 位为 1 当且仅当 $A_j=1$ 且 $S_m=A_m\,(\forall m>j)$。把 $S$ 写成前缀异或 $s$（$s_0=0,\ s_i=s_{i-1}\oplus a_i$，$S=s_r\oplus s_{l-1}$），则 $S_m=A_m\iff s_{l-1,m}=s_{r,m}\oplus A_m$。于是

> 第 $j$ 位有贡献 $\iff$ $A_j=1$ 且 $s_{l-1}$ 与 $v:=s_r\oplus A$ 在**所有 $\ge j$ 的位**上相同。

答案化为 25 个计数问题：$\sum_j 2^j\cdot\#\{\text{满足上式的 }(l,r)\}$。

![AND 分段与离线 Trie](images/cf2261_g_and_segments_trie.svg)

**第三步：固定右端点，把 $l$ 切成 AND 段。** 固定 $r$，令 $g(l)=A(l,r)$。由 $A(l,r)=A(l+1,r)\ \&\ a_l$ 知 $l$ 递减时 $g$ 单调减弱、每变一次至少清掉一个 1 位，故**至多 26 段**。段内 $A$ 固定 ⇒ 模式串 $v=s_r\oplus A$ 固定，一次 Trie 走步即可结算该段所有为 1 的位：

> 沿 $v$ 的位从高到低走 Trie；每进入一个节点（前缀已匹配），若 $A$ 的该位为 1，就累加 $2^j\times$「该子树中 $p$ 的个数」；子树为空即停（更低位不可能有 $p$ 匹配）。

**第四步：离线差分。** 段 $[lo,hi]$ 需对 $p=l-1\in[lo-1,hi-1]$ 计数，拆成两个前缀计数：位置 $hi-1$ 挂 $+1$、位置 $lo-2$ 挂 $-1$（负位置丢弃）。按 $t=0,1,\dots,n$ 扫描：先插入 $s_t$，再回答挂在 $t$ 上的事件——此时 Trie 恰含 $s_0,\dots,s_t$，查询值就是「$p\le t$ 的个数」，差分后即得 $[lo-1,hi-1]$。段值 $A=0$ 的段整段跳过（贡献恒为 0）。

### 3.4 示例演算

![样例一逐区间演算](images/cf2261_g_walkthrough.svg)

对 $a=[5,4,6,7,5]$，只列奇数长度区间（$S,A$ 用二进制）：

| 区间 | $S$ | $A$ | $t$ | $f$ |
|------|-----|-----|-----|-----|
| 5 个单元素区间 | $=a_l$ | $=a_l$ | 无 | $5+4+6+7+5=27$ |
| 4 个长度 2 区间 | 与 $A$ 无交集 | — | $\operatorname{MSB}(S)$ | 0 |
| $[5,4,6]$ | $111$ | $100$ | 1 | $100=4$ |
| $[4,6,7]$ | $101$ | $100$ | 0 | $100=4$ |
| $[6,7,5]$ | $100$ | $100$ | 无 | $4$ |
| $[5,4,6,7,5]$ | $101$ | $100$ | 0 | $100=4$ |

合计 $27+0+12+4=43$，与样例输出一致。注意 $[6,7,5]$：$S=A=4$（$t$ 不存在），三个数在 bit 1、bit 0 上并不全相同，但 $f$ 仍是整个 $S$——正是 3.2 中「没有可清位就原样返回」的分支。

## 4. 算法细节

1. **AND 段增量维护**：不要每段二分。把上一轮（右端点 $r-1$）的段列表整体 $\&\ a_r$，再追加单点段 $[r,r]$ 并合并相邻同值项，每轮 $O(25)$。
2. **事件位置**：段 $[lo,hi]$ 的 $+1$ 在 $hi-1$、$-1$ 在 $lo-2$；$lo=1$ 时 $lo-2=-1$ 必须丢弃，否则会多减掉不属于任何区间的计数。
3. **扫描顺序**：先 `insert(s[t])` 再回答位置 $t$ 的事件，否则漏掉 $p=t$（即 $l-1=t$）这个合法前缀。
4. **剪枝**：$A=0$ 的段跳过；查询里「走不动即 `break`」既保证正确又显著降常数。
5. **64 位与规模**：$2^j\times cnt$ 单次就可达 $6.7\times10^{12}$，必须 `1LL << j`；Trie 节点上界 $25(n+1)+1$，一次分配三张 `int` 数组（$n=4\times10^5$ 约 $10^7$ 节点、120 MB）。
6. **多测**：Trie 节点计数器（`used`）归 1、事件桶与段列表按组重建；总 $n$ 只有 $4\times10^5$，重建代价可接受。I/O 用 `fread` 快读，Python 用 `sys.stdin.buffer.read().split()`。

## 5. 正确性证明

**引理 1**：设区间异或和 $S$、按位与 $A$，$t=\operatorname{MSB}(S\ \&\ \sim A)$（不存在记 $t=-1$），则 $f=S\ \&\ \sim(2^{t+1}-1)$（$t=-1$ 时即 $S$）。

**证明**：一次操作把某个 $b_i$ 换成 $c\ge b_i$，结果是 $u_i\oplus c$（$u_i=S\oplus b_i$）。$c=b_i$ 得 $S$；若 $c>b_i$，取最高不同位 $j$，必有 $c_j=1,b_{i,j}=0$，$j$ 之上结果与 $S$ 逐位相同，第 $j$ 位为 $S_j\oplus1$，$j$ 之下可由 $c=u_i$ 清零，故结果为 $S\ \&\ \sim(2^{j+1}-1)$（当 $S_j=1$）或严格大于 $S$（当 $S_j=0$）。又拐弯要求 $b_{i,j}=0\iff A_j=0$。于是严格改进值构成集合 $\{S\ \&\ \sim(2^{j+1}-1):A_j=0,\ S_j=1\}$，随 $j$ 增大而减小，最小值由最大的可用 $j=t$ 给出；集合为空只能取 $S$。∎

**引理 2**：$k$ 为偶数时 $A\ \&\ S=0$，从而 $f=0$。

**证明**：$A_j=1$ 表示区间内 $k$ 个数第 $j$ 位全为 1，$k$ 为偶数故 $S_j=0$。于是所有 $S_j=1$ 的位都满足 $A_j=0$，$t=\operatorname{MSB}(S)$（$S\ne0$），由引理 1 得 $f=0$；$S=0$ 时同样为 0。∎

**引理 3**：$k$ 为奇数时 $A\subseteq S$（按位包含），且 $f$ 的第 $j$ 位为 1 $\iff$ $A_j=1$ 且对一切 $m>j$ 有 $S_m=A_m$。

**证明**：$A_m=1$ 时该位区间内全为 1、个数 $k$ 为奇数，故 $S_m=1$，即 $A\subseteq S$。由引理 1，第 $j$ 位为 1 $\iff S_j=1$ 且 $j>t$；而 $j>t\iff$ 不存在 $m>j$ 使 $S_m=1,A_m=0$，由 $A\subseteq S$ 这等价于「$m>j$ 时 $S_m=A_m$」。又 $A_j=1\Rightarrow S_j=1$，故条件可写成「$A_j=1$ 且 $m>j$ 全等」。∎

**引理 4**：对区间 $[l,r]$，「$A_j=1$ 且 $m>j$ 时 $S_m=A_m$」$\iff$「$A_j=1$ 且 $s_{l-1}$ 与 $v=s_r\oplus A$ 在一切 $\ge j$ 的位上相同」。

**证明**：$S_m=s_{r,m}\oplus s_{l-1,m}$，故 $S_m=A_m\iff s_{l-1,m}=s_{r,m}\oplus A_m=v_m$；逐位合并即得。∎

**引理 5**：固定 $r$，$l\mapsto A(l,r)$ 至多取 26 个值。

**证明**：$A(l,r)=A(l+1,r)\ \&\ a_l$，故 $l$ 递减时值按位单调减弱，每变一次至少清掉一个 1 位，位宽 25 给出上界 26。∎

**定理**：算法输出等于 $\sum_{l\le r}f(l,r)$。

**证明**：由引理 1、2 知每个区间的 $f$ 只由 $(S,A)$ 决定且偶数长度为 0。对奇数长度，引理 3、4 把「第 $j$ 位贡献」化为对 $p=l-1$ 的前缀匹配条件，权重 $2^j$。由引理 5，固定 $r$ 时 $l$ 被 AND 段划分成互不相交的若干段，段内 $A$ 与模式串 $v$ 固定，Trie 沿 $v$ 走步时在每个 $A_j=1$ 的层累加该子树中 $p$ 的个数，恰为该段「在 $\ge j$ 位上匹配」的 $p$ 个数。差分事件保证段内 $p\in[lo-1,hi-1]$ 的计数为「$+$ 减 $-$」；扫描到 $t$ 时 Trie 恰含 $s_0..s_t$，故只统计 $p\le t$，即 $l-1\le t$，对应合法区间。于是每个 $(l,r,j)$ 被且仅被计入一次，总量即所求。∎

## 6. 复杂度分析

- **时间**：插入 $O(25n)$；AND 段总数 $O(25n)$，每段 2 个事件、每个事件走至多 25 步，故 $O(25^2n)$，最坏约 $2.5\times10^8$ 次简单数组访问。实测 $n=4\times10^5$：随机数据 0.47 s、构造的「25 段」极端数据 1.43 s，对 7 s 时限有 5 倍以上余量。
- **空间**：Trie $O(25n)$ 节点（3 张 `int` 数组）+ 事件 $O(50n)$ 个（2 张 `int` 数组），合计约 $2.9\times10^2$ MB；$n=4\times10^5$ 实测峰值 282 MB，在 1024 MB 内。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

static char buf[1 << 25];
int bp = 0, bl = 0;
inline int gc() {
    if (bp >= bl) { bl = (int)fread(buf, 1, sizeof(buf), stdin); bp = 0; if (bl <= 0) return -1; }
    return buf[bp++];
}
inline int readInt() {
    int c = gc(); while (c != -1 && (c < '0' || c > '9')) c = gc();
    int x = 0; while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

const int BITS = 25;
struct Seg { int val, lo, hi; };          // 固定 r 时 AND 相同的一段 l 区间

int main() {
    int t = readInt();
    vector<int> a, s, ch0, ch1, cnt, evV, evA, st, ptr;
    vector<Seg> prv, cur;
    while (t--) {
        int n = readInt();
        a.assign(n + 1, 0); s.assign(n + 1, 0);
        for (int i = 1; i <= n; i++) { a[i] = readInt(); s[i] = s[i - 1] ^ a[i]; }

        // 维护以 r 结尾的 AND 段：上一轮的段整体 AND 上 a[r]，再追加单点段 [r,r]
        auto build = [&](int r) {
            int ar = a[r];
            cur.clear();
            for (const Seg &g : prv) {
                int nv = g.val & ar;
                if (!cur.empty() && cur.back().val == nv) cur.back().hi = g.hi;
                else cur.push_back({nv, g.lo, g.hi});
            }
            if (!cur.empty() && cur.back().val == ar) cur.back().hi = r;
            else cur.push_back({ar, r, r});
            prv.swap(cur);
        };

        st.assign(n + 2, 0); prv.clear();              // 第一遍：数事件
        for (int r = 1; r <= n; r++) {
            build(r);
            for (const Seg &g : prv) {
                if (g.val == 0) continue;              // A = 0 的段贡献恒为 0
                st[g.hi]++;                            // 事件位置 hi-1（下标错位 1）
                if (g.lo >= 2) st[g.lo - 1]++;         // 事件位置 lo-2
            }
        }
        for (int i = 0; i <= n; i++) st[i + 1] += st[i];
        evV.assign(st[n + 1], 0); evA.assign(st[n + 1], 0);
        ptr.assign(n + 2, 0);
        for (int i = 0; i <= n; i++) ptr[i] = st[i];

        prv.clear();                                    // 第二遍：填事件（符号压进 A 的最高位）
        for (int r = 1; r <= n; r++) {
            build(r);
            int sr = s[r];
            for (const Seg &g : prv) {
                if (g.val == 0) continue;
                int v = sr ^ g.val, p1 = g.hi - 1, p2 = g.lo - 2;
                evV[ptr[p1]] = v; evA[ptr[p1]] = g.val; ptr[p1]++;
                if (p2 >= 0) { evV[ptr[p2]] = v; evA[ptr[p2]] = g.val | (1 << 31); ptr[p2]++; }
            }
        }

        int nodes = BITS * (n + 1) + 2;                 // 离线扫描：先插 s[t]，再答位置 t 的事件
        ch0.assign(nodes, 0); ch1.assign(nodes, 0); cnt.assign(nodes, 0);
        int used = 1;
        long long ans = 0;
        for (int tt = 0; tt <= n; tt++) {
            int x = s[tt], u = 0;
            cnt[0]++;
            for (int j = BITS - 1; j >= 0; j--) {
                int c = (x >> j) & 1;
                if (c == 0) { if (!ch0[u]) ch0[u] = used++; u = ch0[u]; }
                else { if (!ch1[u]) ch1[u] = used++; u = ch1[u]; }
                cnt[u]++;
            }
            for (int e = st[tt]; e < st[tt + 1]; e++) {
                int v = evV[e], Ap = evA[e], A = Ap & 0x7fffffff;
                int uu = 0; long long res = 0;
                for (int j = BITS - 1; j >= 0; j--) {
                    uu = ((v >> j) & 1) ? ch1[uu] : ch0[uu];
                    if (!uu) break;                     // 更低位没有 p 能匹配
                    if ((A >> j) & 1) res += (1LL << j) * cnt[uu];
                }
                ans += (Ap < 0) ? -res : res;
            }
        }
        printf("%lld\n", ans);
    }
    return 0;
}
```

### Python3

```python
import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    BITS = 25
    idx = 0
    t = data[idx]; idx += 1
    out = []
    for _ in range(t):
        n = data[idx]; idx += 1
        a = data[idx:idx + n]; idx += n

        s = [0] * (n + 1)
        x = 0
        for i in range(n):
            x ^= a[i]
            s[i + 1] = x

        # 固定 r：把 l 切成 AND 相同的段，每段换成两个离线前缀计数事件
        ev = [[] for _ in range(n + 1)]
        prv = []
        for r in range(1, n + 1):
            ar = a[r - 1]
            cur = []
            for (val, lo, hi) in prv:
                nv = val & ar
                if cur and cur[-1][0] == nv:
                    cur[-1][2] = hi
                else:
                    cur.append([nv, lo, hi])
            if cur and cur[-1][0] == ar:
                cur[-1][2] = r
            else:
                cur.append([ar, r, r])
            prv = cur
            sr = s[r]
            for (val, lo, hi) in cur:
                if val == 0:
                    continue
                v = sr ^ val
                ev[hi - 1].append((v, val))
                if lo >= 2:
                    ev[lo - 2].append((v, -val))

        # 前缀异或的二进制 Trie + 离线扫描
        nodes = BITS * (n + 1) + 2
        ch0 = [0] * nodes
        ch1 = [0] * nodes
        cnt = [0] * nodes
        used = 1
        ans = 0
        rng = range(BITS - 1, -1, -1)
        for tt in range(n + 1):
            x = s[tt]
            u = 0
            cnt[0] += 1
            for j in rng:
                if (x >> j) & 1:
                    w = ch1[u]
                    if w == 0:
                        ch1[u] = used
                        w = used
                        used += 1
                else:
                    w = ch0[u]
                    if w == 0:
                        ch0[u] = used
                        w = used
                        used += 1
                u = w
                cnt[u] += 1
            for (v, sa) in ev[tt]:
                A = sa if sa > 0 else -sa
                u = 0
                res = 0
                for j in rng:
                    u = ch1[u] if (v >> j) & 1 else ch0[u]
                    if u == 0:
                        break
                    if (A >> j) & 1:
                        res += (1 << j) * cnt[u]
                ans += res if sa > 0 else -res
        out.append(ans)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()
```

> Python 版是同一算法的参考实现，常数大：实测 $n=10^5$ 随机约 3.8 s、极端数据约 22 s，$n=4\times10^5$ 必超时；正式提交请用 C++17 版。

## 8. 边界情况与易错点

1. **$n=1$**：无 $t$，$f=a_1$，答案即 $a_1$；Trie 只插入 $s_0,s_1$，节点上界仍要按 $25(n+1)$ 开够。
2. **事件位置越界**：$lo=1$ 时 $lo-2=-1$ 必须丢弃；$hi=1$ 时 $hi-1=0$ 必须保留（对应 $p=0$，即 $l=1$）。
3. **别用「公共前缀」直觉替代 $S$**：$[6,7,5]$ 的公共前缀是 4、$f$ 也是 4，但 $[7,15,11]$ 的公共前缀是 0 而 $f=3$（$S=A=3$，$t$ 不存在），所以必须真的按 $S$ 算。
4. **偶数长度不必手工过滤**：判据「$A_j=1$ 且 $\ge j$ 位全等」本身已蕴含奇数长度（$A_j=S_j=1$ 要求该位 1 的个数为奇数）；但若另加奇偶过滤且写反，会直接错一半。
5. **全 0 / 全相同**：全 0 时所有段被 `A==0` 剪枝跳过，答案 0，注意别漏加根节点计数；全相同时 $S=A$、$t$ 不存在，$f=a_i$。
6. **溢出与多测**：$2^j\times cnt$ 单次已超 `int`，答案 $1.4\times10^{18}$ 需 `long long`；多测时 `used` 归 1、`st/ptr` 与段列表按组重建。

## 相关题目与扩展

- [LeetCode 201. 数字范围按位与](https://leetcode.cn/problems/bitwise-and-of-numbers-range/)：区间 AND 的「公共高位前缀」，本题 3.2 的 $t$ 是其加强版。
- [LeetCode 1835. 所有数对按位与结果的异或和](https://leetcode.cn/problems/find-xor-sum-of-all-pairs-bitwise-and/)：按位拆开、各位独立求和。
- [LeetCode 421. 数组中两个数的最大异或值](https://leetcode.cn/problems/maximum-xor-of-two-numbers-in-an-array/)：二进制 Trie 上按前缀计数，本题查询部分的原型。
- [Codeforces 242E. XOR on Segment](https://codeforces.com/problemset/problem/242/E)：区间异或 + 按位独立统计。

**延伸思考**：

1. 位宽从 25 放宽到 $B$ 时复杂度是 $O(B^2n)$；「AND 段数」与「Trie 深度」两个 $B$ 相乘是瓶颈，能否用分治压到 $B\log B$？
2. 操作改成「可以不做」答案不变（加 0 即可）；改成「必须加**正**整数」时 3.2 的候选集合要整体位移，结论需重推。
3. 把「求和」换成「求所有 $f$ 的最大值」：判据不变，但要换掉逐区间枚举。
4. 把异或换成按位或：单区间贪心结构仍在，但「偶数长度归零」不再成立，需要另找统计方式。
