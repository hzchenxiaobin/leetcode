# Codeforces 最小极差之和 题解

## 1. 题目概述

- **标题 / 题号**：最小极差之和（Codeforces 2241G，英文名 Summmon）
- **链接**：https://codeforces.com/problemset/problem/2241/G
- **来源**：Codeforces Round 1107 (Div. 3) · Problem G
- **难度**：2400（$\ast 2400$）
- **限制**：时间 4 s / 内存 256 MB
- **标签**：二分、数据结构、贪心、实现、数学、数论（官方标签：binary search, data structures, greedy, implementation, math, number theory）

**题意**：对长度为 $m$ 的数组 $b$，可以反复执行以下操作：选一个 $1 \le i < m$，把 $b_{i+1}$ 改成 $b_{i+1}+b_i$ **或** $b_{i+1}-b_i$（$b_i$ 取**当前**值，且可以操作任意多次）。记 $f(b)$ 为所有可达数组里 $\max(b)-\min(b)$ 的最小值。给定数组 $a$，求

$$\sum_{1 \le l \le r \le n} f([a_l, a_{l+1}, \dots, a_r]).$$

**约束**：

- $1 \le t \le 10^4$，$1 \le n \le 2\cdot 10^5$，$\sum n \le 2\cdot 10^5$
- $1 \le a_i \le 10^9$
- **答案可能超出 int64**，官方明确建议使用 `__int128`（Python 无需处理）
- 4 s 的时限相对宽松，$O(n\log n)$ 绰绰有余，$O(n^2)$ 一定超时

> 💡 一句话本质：$b_1$ 是**永远动不了**的锚点，$b_2$ 只能落在 $b_2+b_1\mathbb Z$ 上；但 $j\ge 3$ 的步长会不断变小，于是「只要遇到第一个不是 $a_l$ 倍数的位置 $j^*$」，答案就被 $j^*$ 钉死为 $d=\min(r, a_l-r)$，后面再多的元素都能塞进这段区间。

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
5
3
6 4 8
4
1 2 3 4
9
9 9 8 2 4 4 3 5 3
6
18 12 24 9 6 36
6
36 24 18 12 9 6
输出：
4
3
39
72
111
```

官方第 1 组解释：单元素贡献 $0$；$[6,4]$ 最优不动，极差 $2$；$[4,8]$ 用 $b_2:=b_2-b_1$ 得 $[4,4]$，极差 $0$；$[6,4,8]$ 只把 $8$ 改成 $4$，得 $[6,4,4]$，极差 $2$，合计 $4$。

官方第 2 组解释：$[2,3]$、$[3,4]$、$[2,3,4]$ 各贡献 $1$，其余全为 $0$，合计 $3$。

自造示例（标注：**非官方**）：$a=[18,36,26]$，答案是 $18$。$l=1$ 时 $18\mid 36$ 但 $18\nmid 26$，$j^*=3$，$r=8$，$d=8$，权重 $1$；$l=2$ 时 $36\nmid 26$，$r=26$，$d=\min(26,10)=10$，权重 $1$；合计 $8+10=18$。

## 3. 解题思路

### 3.1 暴力思路

先算单个 $f(b)$：状态是整组 $b$，边是「把某个 $b_{i+1}$ 加减 $b_i$」，值是可达性。但可达状态**无穷多**（$b_2$ 可以取 $a_2+k a_1$），只能人为截断数值范围做 BFS，正确性没有保证。再对 $O(n^2)$ 个子数组各跑一遍，完全不可行。

所以必须先把 $f(b)$ 的解析形式推出来。

### 3.2 核心观察：可达集只有「一段格点」，答案被首个非倍数位置钉死

**(1) 每个位置能独立取哪些值。** 关键不变量：**任意时刻 $\gcd(b_1,\dots,b_j)$ 保持不变**（$\gcd(x\pm y, y)=\gcd(x,y)$），$b_1$ 更是常量。由此可以刻画出每个位置的可达集。

![b2 落在 b2+b1Z 上，bj 的步长更细且整除 d，于是能塞进长度 d 的区间](images/cf2241_g_mod_class.svg)

**结论**：在子数组 $b=[a_l,\dots,a_r]$ 中，对每个 $j\ge 2$，$b_j$ 可以取到**且只能取到**

$$b_j \in a_j + g_{j-1}\mathbb Z,\qquad g_{j-1}=\gcd(a_l,\dots,a_{j-1}),$$

并且各位置**互相独立**（可以同时达成）。必要性来自 gcd 不变（$b_j$ 永远是 $a_j$ 加整系数线性组合）；充分性用归纳：把 $b_{j-1}$ 挪到 $a_{j-1}+k g_{j-2}$ 再整体加到 $b_j$ 上，可用的加数生成的子群正是 $\gcd(g_{j-2},a_{j-1})\mathbb Z=g_{j-1}\mathbb Z$，最后从大到小把各位置固定下来即可。

特别地，$g_1=a_l$，所以 $b_2$ 的步长是**锚点自己** $a_l$；而 $g_{j-1}$ 随 $j$ 单调**只减不增**且始终整除 $a_l$——「越靠后越灵活」是本题的命门。

**(2) 答案只由「第一个不是 $a_l$ 倍数的位置」决定。**

记 $j^*$ 为最小的 $j>l$ 满足 $a_l\nmid a_j$（不存在则记 $j^*=\infty$）。

![a_l 整除的这段区间内前缀 gcd 恒为 a_l，第一次不整除时 gcd 才真正下降](images/cf2241_g_first_drop.svg)

- **$j<j^*$ 时没有代价**：$a_l$ 整除 $a_l,\dots,a_{j-1}$，故 $g_{j-1}=a_l$，而 $a_j\equiv 0\pmod{a_l}$，取 $b_j=a_l$ 即可，贡献 $0$。
- **$j^*$ 处必须付钱**：此时 $g_{j^*-1}=a_l$，于是 $b_1=a_l$、$b_{j^*}\equiv a_{j^*}\pmod{a_l}$，两者模 $a_l$ 的距离至少是 $d=\min(r,a_l-r)$，其中 $r=a_{j^*}\bmod a_l$。
- **$j>j^*$ 不用再加钱**：可以验证 $g_{j-1}\mid g_{j^*}=\gcd(a_l,a_{j^*})\mid d$，而长度恰为 $d$ 的区间「步长为 $g_{j-1}$ 的格子」必然包含每个剩余类的代表元，所以每个位置都能挤进 $[a_l-d,a_l]$ 或 $[a_l,a_l+d]$。

于是

$$f([a_l,\dots,a_R])=\begin{cases}0, & R<j^*\\ d, & R\ge j^*\end{cases}\qquad(R\ \text{为右端点})$$

——**一旦区间盖住 $j^*$，后面再加多少元素都改不了答案**。这是把 $O(n^2)$ 压成 $O(n\log n)$ 的关键：以 $l$ 开头的子数组里，有 $n-j^*+1$ 个（1-based）贡献 $d$，其余为 $0$。

### 3.3 算法流程

![每个左端点只做一次二分，判定用区间 gcd](images/cf2241_g_flow.svg)

```
for each test case:
    读入 n, a[0..n-1]，n == 1 直接输出 0
    建稀疏表求区间 gcd，预处理好 lg[]
    ans = 0
    for l = 0 .. n-2:
        v = a[l]
        if gcd(a[l+1..n-1]) % v == 0:      # 后缀全是 v 的倍数
            continue                        # 这个 l 没有任何贡献
        # 二分第一个 j：gcd(a[l+1..j]) 不是 v 的倍数
        lo = l, hi = n-1                    # P(lo) 恒真，P(hi) 已知为假
        while hi - lo > 1:
            mid = (lo + hi) / 2
            if gcd(a[l+1..mid]) % v == 0: lo = mid
            else:                         hi = mid
        r = a[hi] % v
        d = min(r, v - r)
        ans += d * (n - hi)                 # 共 n-hi 个右端点
    输出 ans（__int128）
```

二分的依据是把「$a_l$ 整除区间里每个数」换成「$a_l$ 整除区间的 gcd」：$v$ 整除集合中每个元素 $\iff v$ 整除它们的 gcd。这个谓词关于右端点单调（gcd 只会变小），所以可以二分；单次判定 $O(1)$，每个 $l$ 只花 $O(\log n)$。

### 3.4 示例演算

![样例 4 的逐 l 演算表](images/cf2241_g_walkthrough.svg)

以样例 4（$n=6$，$a=[18,12,24,9,6,36]$）为例：

| $l$ | $a_l$ | $j^*$ | $r=a_{j^*}\bmod a_l$ | $d$ | 权重 $n-j^*+1$ | 贡献 |
|---|---|---|---|---|---|---|
| 1 | 18 | 2 | 12 | 6 | 5 | 30 |
| 2 | 12 | 4 | 9 | 3 | 3 | 9 |
| 3 | 24 | 4 | 9 | 9 | 3 | 27 |
| 4 | 9 | 5 | 6 | 3 | 2 | 6 |
| 5 | 6 | 无 | — | 0 | — | 0 |
| 6 | 36 | 无 | — | 0 | — | 0 |
| **合计** | | | | | | $\mathbf{72}$ |

注意 $l=5$ 时 $a_5=6$ 而后面只有 $36$，$6\mid 36$，永远等不到降点，所以 $f$ 恒为 $0$——「有降点」不是必然的。

## 4. 算法细节

1. **不必真的模拟操作**：$f$ 的解析式（3.2）已经把「模拟 → 判定」变成「算两个数 $j^*,d$」，代码里一个操作都不用做。
2. **判定用区间 gcd，不是区间最小值**：$a_l$ 要整除区间内**所有**元素，等价于整除它们的 gcd；只有 gcd 才有这种「全体性」。写成 `min` 或 `lcm` 都不对（$v\mid \mathrm{lcm}$ 不蕴含 $v\mid$ 每个元素）。
3. **二分方向别写反**：谓词 $P(j)=\big(v \mid \gcd(a_{l+1},\dots,a_j)\big)$ 是「先真后假」，找的是**第一个假**位置。用 `lo=l`（$P$ 恒真）、`hi=n-1`（已判为假），循环条件 `hi-lo>1`，最后答案就是 `hi`。
4. **可以先用一次整体判定剪枝**：先查 $v \mid \gcd(a_{l+1..n-1})$，为真就整段跳过，省掉一次二分；对「后缀全是倍数」的数据这一步把每个 $l$ 压到 $O(1)$。
5. **稀疏表的下标**：$k=\lfloor\log_2(\text{len})\rfloor$，区间 gcd 为 $\gcd(sp[k][L], sp[k][R-2^k+1])$，右边那个 `+1` 极易漏；`lg` 表递推 `lg[i]=lg[i/2]+1` 从 $i=2$ 开始。
6. **权重用 0-based 下标**：左端点 $l$、降点下标 `hi` 都是 0-based 时，右端点取 `hi..n-1` 共 `n-hi` 个；若混用 1-based 的 $n-j^*+1$ 会整体偏移 1。
7. **答案必须 128 位**：每个 $l$ 的贡献 $\le \frac{a_l}{2}\cdot n \le 5\times10^{8}\cdot 2\cdot10^{5}=10^{14}$，$n$ 个 $l$ 之和可达 $2\times10^{19}$，`long long` 会溢出（实测 $n=2\cdot10^5$、$a$ 交替取 $10^9$ 与 $5\cdot10^8+1$ 时答案 $5.0\times10^{18}$，仅差一个量级就撞墙）。C++ 手写 `__int128` 输出。
8. **多测均摊**：$t$ 可达 $10^4$ 但 $\sum n\le 2\cdot10^5$，所以每组建 $O(n\log n)$ 的稀疏表总代价仍是 $O(\sum n\log n)$；别写成每组 $O(V)$ 清空 $10^9$ 大小的数组。
9. **常数优化**：C++ 用 `std::gcd`（C++17，别依赖 GNU 的 `__gcd`）；Python 把查询内联进循环、避免函数调用，实测从 $1.66$ s 降到 $1.22$ s。
10. **读入**：$\sum n$ 个整数 + 组数，`scanf` 足够（实测含读入 $0.10$ s）；Python 用 `sys.stdin.buffer.read().split()`。

## 5. 正确性证明

**引理 1（可达集）**：设子数组 $b_1,\dots,b_m$ 对应 $a_l,\dots,a_r$，$g_{j-1}=\gcd(a_l,\dots,a_{j-1})$。则对每个 $j\ge2$，$b_j$ 的可达值集合恰为 $a_j+g_{j-1}\mathbb Z$，且各位置的取值可以同时达成。

**证明**：每个操作都是整数线性组合，故任意可达配置满足 $b_j\equiv a_j\pmod{g_{j-1}}$，必要性得证。充分性对 $j$ 归纳并用「从大到小固定」的顺序：先只动 $b_m$（用 $b_{m-1}$ 的当前值加减，可加任意 $b_{m-1}$ 的倍数），再固定 $b_{m-1}$（用 $b_{m-2}$），……最后固定 $b_2$（用 $b_1$）；固定 $b_k$ 之后的操作（下标 $\le k-1$）不会碰到 $b_{k+1},\dots,b_m$，所以已固定的位置不被破坏。而把 $b_{j-1}$ 挪到 $a_{j-1}+k g_{j-2}$ 后能加到 $b_j$ 上的所有加数生成的子群为 $\gcd\big(g_{j-2},\,a_{j-1}\big)\mathbb Z=g_{j-1}\mathbb Z$，故 $a_j+g_{j-1}\mathbb Z$ 中每个值都能取到。∎

**引理 2（降点前无代价）**：若 $j<j^*$，则 $g_{j-1}=a_l$；若还有 $a_l\mid a_j$，则 $b_j$ 可取 $a_l$。

**证明**：由 $j^*$ 的定义，$j<j^*$ 时 $a_l$ 整除 $a_l,\dots,a_{j-1}$，gcd 只能等于 $a_l$；再由 $a_j\equiv0\pmod{a_l}$ 与引理 1 取 $b_j=a_l\in a_j+a_l\mathbb Z$。∎

**引理 3（下界）**：若 $j^*$ 存在，则任何可达配置的极差 $\ge d=\min(r,a_l-r)$，其中 $r=a_{j^*}\bmod a_l$。

**证明**：$b_1=a_l$，而由引理 1 有 $b_{j^*}\equiv a_{j^*}\pmod{a_l}$（注意 $g_{j^*-1}=a_l$），故 $b_{j^*}-b_1\equiv r\pmod{a_l}$，其绝对值 $\ge\min(r,a_l-r)=d$，极差自然 $\ge d$。∎

**引理 4（上界）**：若 $j^*$ 存在，则存在可达配置使极差恰为 $d$。

**证明**：取 $b_1=a_l$、$b_{j^*}=a_l-d$（或 $a_l+d$，落在 $a_{j^*}+a_l\mathbb Z$ 中，见引理 1）；对 $j<j^*$ 取 $b_j=a_l$（引理 2）。对 $j>j^*$，由 $g_{j^*}=\gcd(a_l,a_{j^*})$ 与引理 1 的整除关系得 $g_{j-1}\mid g_{j^*}\mid r$ 且 $g_{j^*}\mid a_l$，故 $g_{j-1}\mid d$；于是长度 $d$、含 $b_1$ 与 $b_{j^*}$ 的闭区间里含有每个模 $g_{j-1}$ 剩余类的代表元（区间长度 $\ge$ 步长），让每个 $b_j$ 取该代表元即可，所有值都落在同一个长度 $d$ 的区间内。∎

**定理**：$\displaystyle\sum_{1\le l\le R\le n}f([a_l,\dots,a_R])=\sum_{l:\,j^*_l\text{ 存在}} d_l\cdot(n-j^*_l+1)$。

**证明**：固定 $l$。若 $R<j^*$，则区间内所有 $a_j$ 都满足 $j<j^*$ 且被 $a_l$ 整除，由引理 2 可取全部 $=a_l$，极差 $0$；若 $R\ge j^*$，由引理 3、4 极差恰为 $d$（引理 4 的构造只用前 $j^*$ 个位置的性质，与 $R$ 无关）。因此以 $l$ 开头的子数组里恰有 $n-j^*+1$ 个（1-based）贡献 $d$，其余 $0$，对 $l$ 求和即得。∎

## 6. 复杂度分析

- **时间**：每组建 $O(n\log n)$ 的 gcd 稀疏表与 `lg` 表；主体对每个 $l$ 做一次 $O(\log n)$ 的二分，每次判定 $O(1)$，共 $O(n\log n)$。总计 $O\big(\sum n\log n\big)$，$n=2\cdot10^5$ 时约 $3.6\times10^6$ 次 gcd。
- **空间**：稀疏表 $O(n\log n)$ 个 64 位整数，$n=2\cdot10^5$ 时约 $18\times2\cdot 10^5\times8\text{ B}\approx 29$ MB，加其余数组远低于 256 MB。
- **对照时限**：4 s 非常宽松。本机（Apple clang 21 `-O2`，含读入，`/usr/bin/time -p` 取 real）实测 $n=2\cdot10^5$：随机值 $0.10$ s、$[2,2,\dots,2,3]$ $0.05$ s、全 $1$ $0.02$ s、$t=10^4$ 组小数据 $0.03$ s、答案接近 int64 上限的构造 $0.08$ s，余量约 40 倍。
- **Python**：CPython 3.9 同一批数据 $0.32\sim1.33$ s（建议提交 PyPy3，更快更稳）；内联查询后 CPython 也在 4 s 内。
- **验证**：官方 5 组样例全部吻合；与「按定义 BFS 枚举所有可达状态（数值截断验证两档边界一致）」的暴力对比了 $4139$ 组小数组（$m\le5$，含 $m\le4$ 的全枚举）$0$ 处不一致，另有 $80$ 组端到端对拍（每个子数组都跑 BFS 求 $f$ 再求和）；与独立 $O(n^2)$ 实现（逐 $l$ 扫描维护前缀 gcd）对拍 $9330+400+12$ 组（$n\le5$ 全枚举、随机 $n\le60$、$n=1000$）$0$ 处不一致；C++ 与 Python 在所有大测上输出完全一致。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef __int128 lll;

static void print128(lll x) {                 // 答案可能超 int64，手写输出
    if (x == 0) { puts("0"); return; }
    string s;
    while (x > 0) { s.push_back(char('0' + (int)(x % 10))); x /= 10; }
    reverse(s.begin(), s.end());
    puts(s.c_str());
}

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;       // 空输入防护
    while (t--) {
        int n;
        scanf("%d", &n);
        vector<ll> a(n);
        for (int i = 0; i < n; ++i) scanf("%lld", &a[i]);

        if (n == 1) { puts("0"); continue; }  // 只有单元素子数组，贡献 0

        // ---- 稀疏表：O(1) 求区间 gcd ----
        int K = 1;
        while ((1 << K) <= n) ++K;
        vector<int> lg(n + 1, 0);
        for (int i = 2; i <= n; ++i) lg[i] = lg[i >> 1] + 1;
        vector<vector<ll>> sp(K, vector<ll>(n, 0));
        for (int i = 0; i < n; ++i) sp[0][i] = a[i];
        for (int k = 1; k < K; ++k) {
            int half = 1 << (k - 1);
            for (int i = 0; i + (1 << k) <= n; ++i)
                sp[k][i] = std::gcd(sp[k - 1][i], sp[k - 1][i + half]);
        }
        auto query = [&](int l, int r) -> ll {           // gcd(a[l..r])，闭区间
            int k = lg[r - l + 1];
            return std::gcd(sp[k][l], sp[k][r - (1 << k) + 1]);
        };

        lll ans = 0;
        for (int l = 0; l + 1 < n; ++l) {
            const ll v = a[l];
            // 整个后缀都是 v 的倍数 => 以 l 开头的子数组极差全为 0
            if (query(l + 1, n - 1) % v == 0) continue;
            // 二分第一个 j：gcd(a[l+1..j]) 不是 v 的倍数（即 v 不整除 a[j]）
            int lo = l, hi = n - 1;                      // P(lo) 恒真，P(hi) 已为假
            while (hi - lo > 1) {
                int mid = lo + (hi - lo) / 2;
                if (query(l + 1, mid) % v == 0) lo = mid;
                else                            hi = mid;
            }
            const ll r = a[hi] % v;
            const ll d = min(r, v - r);
            ans += (lll)d * (n - hi);                    // 右端点取 hi..n-1 共 n-hi 个
        }
        print128(ans);
    }
    return 0;
}
```

### Python3

```python
import sys
from math import gcd


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:                                   # 空输入防护
        return
    t = data[0]
    pos = 1
    out = []
    for _ in range(t):
        n = data[pos]; pos += 1
        a = data[pos:pos + n]; pos += n
        if n == 1:
            out.append("0")
            continue

        # 稀疏表：区间 gcd
        lg = [0] * (n + 1)
        for i in range(2, n + 1):
            lg[i] = lg[i >> 1] + 1
        sp = [a]
        j = 1
        while (1 << j) <= n:
            prev = sp[-1]
            half = 1 << (j - 1)
            sp.append([gcd(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)])
            j += 1

        ans = 0
        for l in range(n - 1):
            v = a[l]
            # 后缀整体判定：gcd(a[l+1..n-1]) 是 v 的倍数 => 该 l 贡献 0
            ln = n - 1 - l
            k = lg[ln]
            if gcd(sp[k][l + 1], sp[k][n - (1 << k)]) % v == 0:
                continue
            lo, hi = l, n - 1
            while hi - lo > 1:
                mid = (lo + hi) >> 1
                ln = mid - l
                k = lg[ln]
                if gcd(sp[k][l + 1], sp[k][mid - (1 << k) + 1]) % v == 0:
                    lo = mid
                else:
                    hi = mid
            r = a[hi] % v
            ans += (r if r < v - r else v - r) * (n - hi)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **答案溢出**：每个 $l$ 的贡献可达 $10^{14}$，总和可达 $2\times10^{19}$；`long long` 会在 $n$ 大且 $a_l$ 大的数据上溢出，必须 `__int128`（输出也要手写，`cout` 不支持）。
2. **$n=1$**：没有 $j$，答案 $0$；循环写成 `l < n-1` 就自然跳过，但 `query(l+1,n-1)` 在 $l=n-1$ 时会区间为空，必须保证不进循环。
3. **$j^*$ 可能不存在**：例如 $a=[4,8]$、$a=[6,36]$ 或全 $1$ 的数组，所有后缀都是 $a_l$ 的倍数，贡献 $0$；漏掉这个分支会在二分时越界或给出错误 $d$。
4. **二分端点语义**：`lo=l` 只是「保证为真」的哨兵（下标 $l+1>l$，空区间不会被真正查询），`hi=n-1` 则必须已确认为假，所以要先做整体判定；`mid` 由 `(lo+hi)/2` 得出时总有 $mid\ge l+1$，区间非空。
5. **整除方向**：判定要写 `g % v == 0`（即 $v\mid g$），不能写 `v % g == 0`；写反后小数据仍可能碰巧正确，但 $g\ge v$ 时会立刻出错。
6. **稀疏表 `+1`**：右半段下标是 $R-2^k+1$，漏掉 `+1` 会把答案算小；`K` 的循环条件用 `(1<<K) <= n`，`lg` 表从 $i=2$ 递推。
7. **权重偏移**：0-based 下权重是 `n-hi`；写成 `n-hi+1` 会把每个 $l$ 多算一个子数组，样例 1 就会从 $4$ 变成 $6$。
8. **多测重建**：$\sum n$ 有上界，但每组都要重建稀疏表与 `lg`；不要用 $10^9$ 大小的全局数组，也不要忘记 `ans` 归零。
9. **Python 性能**：CPython 需把查询内联（省掉闭包调用），否则 $2\cdot 10^5$ 会到 $1.7$ s 以上；提交建议 PyPy3。

## 相关题目与扩展

- [Codeforces 475D CGCDSSQ](https://codeforces.com/problemset/problem/475/D)：统计「区间 gcd 等于给定值」的区间数，核心同样是「前缀 gcd 只有 $O(\log A)$ 种取值」。
- [Codeforces 1101D GCD Counting](https://codeforces.com/problemset/problem/1101/D)：树上路径 gcd 与因子统计，可与本题的「gcd 链」思想对照。
- [LeetCode 2447. 最大公因数等于 K 的子数组数目](https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/)：区间 gcd 分组的入门题，本题二分判定用的正是同一类工具。
- [Codeforces 1548B Integers Have Friends](https://codeforces.com/problemset/problem/1548/B)：把「同余」转成「差分数组的 gcd」，与本题「用 gcd 描述整除约束」的手法相近。

**延伸思考**：

1. **若允许任意两个位置互相加减**：本题限制「只能用 $b_i$ 更新 $b_{i+1}$」，可达集才呈现「逐步变细」的层次；若任意 $b_i,b_j$ 都能互加减，可达集退化成「gcd 相同的所有数组」，$f$ 直接恒为 $0$（全部调成同一个数 $g$），题目就没难度了。
2. **求 $\sum f^2$ 或加权重**：解析式不变，只把 $d$ 换成 $d^2$（需 `__int128` 甚至高精度），复杂度完全相同。
3. **单点修改 + 询问**：$j^*$ 由「$a_l$ 整除的一段后缀」决定，可用线段树上二分（判定仍是区间 gcd）支持 $O(\log^2 n)$ 的修改与查询，思路与静态版一致。
4. **$a_i$ 放宽到 $10^{18}$**：稀疏表与二分都不依赖值域，只把 `long long` 换成 `__int128`，答案则可能要写高精度。
5. **反过来问最大值**：若求 $\max_{l\le R} f(l,R)$，注意 $f(l,R)$ 关于 $R$ 是「先 $0$ 后恒定」，所以只需对每个 $l$ 看是否存在 $j^*$，取 $d$ 的最大值即可，$O(n\log n)$ 一样成立。
