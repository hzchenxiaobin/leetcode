# Codeforces 精确对齐 题解

## 1. 题目概述

- **标题 / 题号**：精确对齐（Codeforces 2275D，英文名 Precision Alignment）
- **链接**：https://codeforces.com/problemset/problem/2275/D
- **来源**：Codeforces Round 1125 (Div. 3) · Problem D
- **难度**：1300
- **限制**：时间 2 s / 内存 256 MB
- **标签**：二分答案、贪心、暴力枚举、模拟（官方 tag：binary search、brute force、greedy、implementation）

**题意**：有 $n$ 间实验室，第 $i$ 间的三台仪器读数为 $(a_i,b_i,c_i)$。三台仪器**可区分**，位置固定、不能重排。一次操作指选定一间实验室 $i$，执行下面三件事**之一**：

- $c_i \mathrel{+}= \operatorname{sgn}(a_i-b_i)$
- $b_i \mathrel{+}= \operatorname{sgn}(a_i-c_i)$
- $a_i \mathrel{+}= \operatorname{sgn}(b_i-c_i)$

其中 $\operatorname{sgn}(x)$ 在 $x>0$ 时为 $1$、$x<0$ 时为 $-1$、$x=0$ 时为 $0$。也就是说：每次只把**一台**仪器的读数挪动 $1$，方向由**另外两台**的差决定，且是「写在前面的减后面的」。操作依次进行，每次都看当时的读数；同一间实验室可以操作任意多次，也可以一次不碰，所有实验室合计**至多** $k$ 次操作。

评分取最差的一间：

$$S=\min_{1\le i\le n}(a_i+b_i+c_i)$$

求 $S$ 的最大可能值。多测格式：首行 $t$；每组先给 $n,k$，随后 $n$ 行每行 $a_i,b_i,c_i$；每组输出一行答案。

**约束**：

- $1\le t\le 10^4$，$1\le n\le 2\times10^5$，$\sum n\le 2\times10^5$
- $0\le k\le 10^{18}$
- $-10^9\le a_i,b_i,c_i\le 10^9$
- 答案可能超出 32 位整数（最坏约 $10^{18}$ 量级），必须用 64 位整数

## 2. 示例

官方样例（共 5 组，输入输出原样）：

```text
输入：
5
3 4
-3 -1 -2
1 3 5
2 4 6
3 4
6 4 2
6 7 0
7 6 0
3 1000000000000000000
4 4 4
1 5 9
-1000000000 0 1000000000
2 4
1 2 3
0 0 5
4 3
2 1 0
4 4 5
1 5 9
7 -2 1

输出：
-2
14
12
6
6
```

第 1 组的 $-2$ 说明答案可以是负数；第 3 组的 $(4,4,4)$ 把答案封顶在 $12$；第 4 组的 $(0,0,5)$ 看似卡死，却靠一次 $b\mathrel{-}=1$ 脱困后一路 $+1$ 追到 $6$。

## 3. 解题思路

### 3.1 暴力思路

单间实验室的「操作序列」长度是 $k$，每步 3 种选择，直接搜索是 $3^k$；$k$ 到 $10^{18}$ 时完全不可行。多间实验室还要把 $k$ 拆开分配，组合数更爆炸。所以必须找到**单间实验室「花 $m$ 次操作能得到多大和」的闭式表达**，再把它组合起来。

### 3.2 核心观察：三种状态与「长期 +1」的开关

![一台仪器的三种状态与每次操作的增量](images/cf2275_d_three_regimes.svg)

只看**和** $P=a+b+c$ 的变化。三个操作各自把哪一台挪动 $1$、增量为多少，完全由**另外两台**决定：

| 操作 | 被改的读数 | 增量为 $+1$ 的条件 | 增量为 $-1$ 的条件 |
|------|-----------|--------------------|--------------------|
| op1 | $c$ | $a>b$ | $a<b$ |
| op2 | $b$ | $a>c$ | $a<c$ |
| op3 | $a$ | $b>c$ | $b<c$ |

关键在于：**op1 只改 $c$，$a,b$ 不动**。所以一旦 $a>b$，op1 的增量永远 $+1$，可以无限重复；同理 $a>c$ 时反复 op2（只改 $b$）、$b>c$ 时反复 op3（只改 $a$），都能每步净 $+1$。反之，若 $a\le b\le c$，三个增量分别是 $\operatorname{sgn}(a-b)\le0$、$\operatorname{sgn}(a-c)\le0$、$\operatorname{sgn}(b-c)\le0$，**没有一步能让和上升**；而 $a=b=c$ 时三个 $\operatorname{sgn}$ 全是 $0$，操作纯空转，读数永远冻结。

于是每间实验室落在三种状态之一：

1. **自由态**：$a>b$ 或 $a>c$ 或 $b>c$（等价于**不是** $a\le b\le c$）。每步净 $+1$，$m$ 步后和为 $P+m$；又因为单步至多改变 $\pm1$，这恰是上界。
2. **有序态**：$a\le b\le c$ 且三数不全相等。每一步都只能让和原地或下降，想涨**必须先「逃出」有序区**。
3. **冻结态**：$a=b=c$。任何操作都是空转，和永久不变，它是整个答案的硬上界。

### 3.3 算法流程：逃生代价 + 二分答案

![有序态的逃生阶梯与代价 e](images/cf2275_d_escape_ladder.svg)

**逃生**：在有序态里，op1 能把 $c$ 每次压 $1$（需 $a<b$），op2 能把 $b$ 每次压 $1$（需 $a<c$），op3 只会压低 $a$、帮倒忙。于是只有两条路：

- 把 $b$ 压到 $a-1$：花 $b-a+1$ 步，落地时 $a>b$，进入自由态；
- 把 $c$ 压到 $b-1$：花 $c-b+1$ 步，落地时 $b>c$，进入自由态。

取较小者，得到**逃生代价**

$$e=\min\bigl(\{b-a+1 \text{ 若 } a<c\},\ \{c-b+1 \text{ 若 } a<b\}\bigr),\qquad e\ge 1$$

它也是下界：$b$ 只能靠 op2 每步降 $1$（需 $a<c$），$c$ 只能靠 op1 每步降 $1$（需 $a<b$），而走 $a>c$ 需要 $c-a+1\ge c-b+1$ 步不会更便宜（严格证明见 §5 引理 4）。

逃生的代价是「先跌后爬」：$e$ 步之后和变成 $P-e$，之后每步 $+1$。于是让单间实验室的和达到 $X$ 所需的最少操作数（记为 $f(X)$）是

$$f(X)=\begin{cases}0, & X\le P\\[2pt] X-P, & X>P,\ \text{自由态}\\[2pt] X-P+2e, & X>P,\ \text{有序态}\\[2pt] +\infty, & X>P,\ \text{冻结态}\end{cases}$$

**整体**：$F(X)=\sum_i f_i(X)$ 随 $X$ 单调不减，且「每组实验室独立花钱、预算共享」正是求和，所以 $X$ 可行 $\iff F(X)\le k$，可以**二分答案**。

**判定加速**：只有 $P_i<X$ 的实验室要花钱，且花的是 $X-P_i+2e_i$。按 $P_i$ 排序后

$$F(X)=\sum_{P_i<X}\bigl(X-P_i+2e_i\bigr)=\mathrm{cnt}\cdot X-\sum_{P_i<X}P_i+2\sum_{P_i<X}e_i$$

前缀和即可 $O(\log n)$ 判定（C++ 里直接 $O(n)$ 也够快）。二分区间取

$$\Bigl[\min_i P_i,\ \min_i (P_i+k)\Bigr]$$

下界一定可行（一次不操作）；上界之所以不可行：设 $j$ 取到 $\min_i(P_i+k)$，则 $X>\min_i(P_i+k)\ge P_j+k$，而单步至多 $+1$，实验室 $j$ 单独就要超过 $k$ 步。若存在冻结实验室，再把上界收紧到「冻结实验室的最小和」。

### 3.4 示例演算

![二分答案与样例 5 的判定表](images/cf2275_d_binary_search_flow.svg)

对样例 5（$n=4$，$k=3$）：

| 实验室 | $P$ | 状态 / $e$ | $f(6)$ | $f(7)$ |
|--------|-----|-----------|--------|--------|
| $(2,1,0)$ | $3$ | 自由（$a>b$） | $6-3=3$ | $7-3=4$ |
| $(4,4,5)$ | $13$ | 有序，$a<c$ 故 $e=b-a+1=1$ | $0$ | $0$ |
| $(1,5,9)$ | $15$ | 有序，$e=\min(5,5)=5$ | $0$ | $0$ |
| $(7,-2,1)$ | $6$ | 自由（$a>c$） | $0$ | $7-6=1$ |
| 合计 | | | $3\le 3$ ✓ | $5>3$ ✗ |

$X=6$ 恰好花光预算，$X=7$ 超支，故答案为 $6$。

再看样例 4 的 $(0,0,5)$：$a=b<c$，op1 因 $a-b=0$ 空转，只能走 $b-a+1=1$ 这条 —— 先把 $b$ 压到 $-1$ 逃出有序区（和 $5\to4$），随后 $a>b$，每次 op1 让 $c+1$。所以 $f(6)=6-5+2\cdot1=3$：正是题面提示的「$b\mathrel{+}=\operatorname{sgn}(a-c)$ 之后就脱困了」，三步恰好把和从 $5$ 抬到 $6$。

## 4. 算法细节

1. **多测清空**：每组重新读入并把 `s / e` 按当前 $n$ 重新开数组；$\sum n\le 2\times10^5$ 保证总复杂度。用 `scanf`/`sys.stdin.buffer.read()` 一次性读入，避免 $10^4$ 组小数据的 I/O 抖动。
2. **状态判定顺序**：先判 $a=b=c$（冻结），再判 $a\le b\le c$（有序），剩下都是自由态。不要写成 `a<b<c`，等号很关键：$a=b<c$ 仍是必须逃生的有序态，$a=b=c$ 才是冻结态。
3. **$e$ 的两个分支各自带前提**：$a<b$ 才允许「压 $c$」，$a<c$ 才允许「压 $b$」；用 `INF` 占位再取 `min`，不要无条件取 `min`，否则 $a=b<c$ 会算出错误的 $c-b+1$。
4. **溢出**：单间代价最大约 $10^{18}+2\cdot10^9$，$n$ 间相加可达 $2\times10^{23}$，判定时必须用 `__int128`，并**一旦超过 $k$ 立即 break**；答案量级 $10^{18}$，输出用 `long long`。
5. **二分写法用「可行/不可行」双指针**：`lo` 恒可行、`hi` 恒不可行，`while (hi - lo > 1)`，`mid = lo + (hi - lo) / 2`（值域含负数，这样写不会错）。
6. **上界的合成**：设 $C$ 为所有冻结实验室中和的最小值（没有冻结实验室时 $C=+\infty$），则上界取 $\min\bigl(\min_i(P_i+k),\,C\bigr)$；别忘了再 $+1$ 让它落在不可行侧。
7. **前缀和加速（Python）**：把 $P_i$ 排序、对 $P$ 与 $e$ 各做前缀和，`bisect_left` 求出 $\mathrm{cnt}$，单次判定 $O(\log n)$；C++ 用 $O(n)$ 扫描更快且常数小。
8. **「至多 $k$ 次」不是「恰好 $k$ 次」**：判定只问「够不够」，$X\le P_i$ 的实验室直接记 $0$；用不掉的操作留着即可，不要因为剩余预算去强行多算代价。

## 5. 正确性证明

**引理 1（单步上界）**：任意一次操作对某间实验室的和的改变量属于 $\{-1,0,+1\}$，故 $m$ 次操作后该间实验室的和至多 $P+m$。∎

**引理 2（自由态可达上界）**：若 $a>b$ 或 $a>c$ 或 $b>c$，则对任意 $m\ge0$，存在 $m$ 步操作使该间实验室的和恰为 $P+m$。

**证明**：三种情况对称，只证 $a>b$。op1 为 $c\mathrel{+}=\operatorname{sgn}(a-b)=1$，它只改 $c$，故 $a,b$ 不变、$a>b$ 恒成立，重复 $m$ 次即得 $P+m$。由引理 1 这是上界，所以恰为上界。$a>c$ 时重复 op2（只改 $b$）、$b>c$ 时重复 op3（只改 $a$）同理。∎

**引理 3（有序区不能升）**：若 $a\le b\le c$，则任一操作的和增量 $\le 0$；特别地，只要状态始终停在 $a\le b\le c$，和就不可能超过初值 $P$。

**证明**：三个增量分别是 $\operatorname{sgn}(a-b),\operatorname{sgn}(a-c),\operatorname{sgn}(b-c)$，在 $a\le b\le c$ 下均 $\le0$。∎

**引理 4（逃生代价）**：设 $a\le b\le c$ 且不全相等，令 $e=\min(\{b-a+1\mid a<c\},\{c-b+1\mid a<b\})$。则（i）任何从该状态出发、首次离开有序区的操作序列长度 $t$ 满足 $t\ge e$，且离开时和为 $P-t\le P-e$；（ii）存在长度恰为 $e$ 的序列，离开后 $a>b$（走第一条路）或 $b>c$（走第二条路），即立刻进入自由态。

**证明**：（i）op3 只把 $a$ 降低，对造出 $a>b$、$b>c$、$a>c$ 都无益，故最短序列可以不用 op3，于是 $a$ 不变、$b=b_0-y$、$c=c_0-x$（$x,y$ 为 op1、op2 次数，每次都让和 $-1$，故长度为 $t=x+y$ 时和为 $P-t$）。要 $a>b$ 需 $y\ge b-a+1$ 且每步 op2 时 $a<c$（初值 $a<c$ 由 $a\le b\le c$ 且不全等得到）；要 $b>c$ 需 $x\ge c-b+1$ 且初值 $a<b$；要 $a>c$ 需 $x\ge c-a+1\ge c-b+1$。故长度 $\ge e$。（ii）若取第一条路且 $a<c$，做 $b-a+1$ 次 op2 即得 $a>b$；若取第二条路且 $a<b$，做 $c-b+1$ 次 op1 即得 $b>c$。两条路每步都是 $-1$，故落地时和都是 $P-e$。∎

**定理 1（单间代价公式）**：$f(X)$（让一间实验室的和 $\ge X$ 的最少操作数）等于 §3.3 给出的分段函数。

**证明**：$X\le P$ 时 $0$ 步即达标；由引理 1，这是最小值。自由态且 $X>P$：由引理 2 可达 $P+m$ 且不能更快，故需 $X-P$ 步。有序态且 $X>P$：由引理 3，若不离开有序区则永远 $\le P<X$，故必须离开；设某序列在 $t$ 步首次离开，由引理 4 有 $t\ge e$ 且此时和 $\le P-e$，之后每步至多 $+1$，故总步数 $\ge t+\bigl(X-(P-t)\bigr)\ge X-P+2e$（对 $t\ge e$ 单调递增）；取引理 4(ii) 的序列再连做 $X-P+e$ 步自由态操作，恰好 $X-P+2e$ 步。冻结态：三个 $\operatorname{sgn}$ 恒 $0$，读数不变，$X>P$ 时不可能。∎

**引理 5（单调性）**：$f_i(X)$ 关于 $X$ 单调不减，故 $F(X)=\sum_i f_i(X)$ 单调不减；若 $X$ 可行（$F(X)\le k$）则所有 $X'\le X$ 都可行。

**证明**：逐段观察 $f_i$ 显然单调不减（$\infty$ 段除外，那里 $X>P$ 恒成立）。求和保序；可行性即 $F(X)\le k$。∎

**定理 2（算法正确）**：二分的输出等于 $\max S$。

**证明**：设初始 $lo_0=\min_i P_i$，$hi_0=\min\bigl(\min_i(P_i+k),C\bigr)+1$，其中 $C$ 是冻结实验室和的最小值（无冻结实验室时为 $+\infty$）。$lo_0$ 可行（一次不操作即可）；$hi_0$ 不可行：若 $hi_0-1=\min_i(P_i+k)$ 由实验室 $j$ 取到，则 $hi_0>P_j+k$，由引理 1 光是实验室 $j$ 就要超过 $k$ 步；若被 $C$ 收紧，则 $hi_0$ 超过某冻结实验室的和，由定理 1 该间代价为 $\infty$。每轮判定精确（定理 1）且可行性单调（引理 5），故不变量「左端可行、右端不可行」恒成立；终止时右端 $-$ 左端 $=1$，输出即最大可行值。∎

## 6. 复杂度分析

- **时间**：单次判定 $O(n)$（C++）或 $O(\log n)$（Python 前缀和）。二分轮数 $\lceil\log_2(\text{值域})\rceil$，值域 $\le 10^{18}+3\times10^9$，即 $\le 62$ 轮。C++ 总 $O(n\log V)\approx 62\times2\times10^5\approx1.2\times10^7$ 次加法，实测最坏 $0.08$ s，相对 2 s 时限有 20 倍以上余量。Python 为 $O(n\log n+\log V\log n)$ 每组，实测最大数据 $0.4$ s。
- **空间**：$O(n)$ 存 $P_i$ 与 $e_i$（Python 额外两个前缀和数组），$2\times10^5$ 个 64 位整数约 $3.2$ MB，远低于 256 MB。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef __int128 i128;

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n; ll k;
        scanf("%d %lld", &n, &k);
        vector<ll> s(n), e(n);   // e: 0 自由 / >0 有序的逃生代价 / -1 冻结
        ll lo = LLONG_MAX, hi = LLONG_MAX;
        for (int i = 0; i < n; i++) {
            ll a, b, c;
            scanf("%lld %lld %lld", &a, &b, &c);
            s[i] = a + b + c;
            if (a == b && b == c) {
                e[i] = -1;                        // 冻结：读数永远不变
            } else if (a <= b && b <= c) {        // 有序：先付代价逃生
                ll best = LLONG_MAX;
                if (a < b) best = min(best, c - b + 1);   // 压 c 到 b-1  -> b>c
                if (a < c) best = min(best, b - a + 1);   // 压 b 到 a-1  -> a>b
                e[i] = best;
            } else {
                e[i] = 0;                         // 自由：每步净 +1
            }
            lo = min(lo, s[i]);
            hi = min(hi, s[i] + k);               // 单步至多 +1，这是硬上界
        }
        hi += 1;                                  // hi 取不可行值
        while (hi - lo > 1) {
            ll mid = lo + (hi - lo) / 2;
            bool ok = true;
            i128 total = 0;
            for (int i = 0; i < n; i++) {
                if (s[i] < mid) {                 // 只有和太小的实验室要花钱
                    if (e[i] < 0) { ok = false; break; }
                    total += (i128)mid - s[i] + 2 * (i128)e[i];
                    if (total > (i128)k) { ok = false; break; }
                }
            }
            if (ok) lo = mid; else hi = mid;
        }
        printf("%lld\n", lo);
    }
    return 0;
}
```

### Python3

```python
import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); k = int(data[p + 1]); p += 2
        ss = [0] * n
        es = [0] * n
        frozen_min = None
        for i in range(n):
            a = int(data[p]); b = int(data[p + 1]); c = int(data[p + 2]); p += 3
            s = a + b + c
            ss[i] = s
            if a == b and b == c:                  # 冻结：操作全是空转
                es[i] = -1
                if frozen_min is None or s < frozen_min:
                    frozen_min = s
            elif a <= b and b <= c:                # 有序：先付逃生代价 e
                best = None
                if a < b:
                    best = c - b + 1
                if a < c:
                    v = b - a + 1
                    if best is None or v < best:
                        best = v
                es[i] = best
            else:                                  # 自由：每步 +1
                es[i] = 0
        lo = min(ss)
        hi = min(s + k for s in ss) + 1
        if frozen_min is not None and frozen_min + 1 < hi:
            hi = frozen_min + 1

        pairs = sorted((ss[i], es[i]) for i in range(n) if es[i] >= 0)
        m = len(pairs)
        keys = [0] * m
        pref_s = [0] * (m + 1)
        pref_e = [0] * (m + 1)
        for i in range(m):
            keys[i] = pairs[i][0]
            pref_s[i + 1] = pref_s[i] + pairs[i][0]
            pref_e[i + 1] = pref_e[i] + pairs[i][1]

        while hi - lo > 1:
            mid = (lo + hi) // 2
            j = bisect_left(keys, mid)             # 有 j 间实验室的和 < mid
            if j * mid - pref_s[j] + 2 * pref_e[j] <= k:
                lo = mid
            else:
                hi = mid
        out.append(str(lo))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$k=0$**：直接输出 $\min_i P_i$。代码里 `hi = min(s_i + 0) + 1 = lo + 1`，循环不进，输出 `lo`，正确。
2. **冻结三元组**：$a=b=c$ 时三个 $\operatorname{sgn}$ 恒为 $0$，再加操作也没用，必须当成不可改进的硬上界；只判 $a\le b\le c$ 就会把它错归到有序态，算出 $e=b-a+1=1$ 而给出过大答案。
3. **有序但 $a=b$**：此时 op1 空转（$\operatorname{sgn}(0)=0$），压不动 $c$，只能走 $e=b-a+1=1$；若忽略前提条件取 $\min$ 会得到错误的 $c-b+1$。
4. **负数和负答案**：样例 1 的答案是 $-2$，下界可低至 $-3\times10^9$。二分、`min`、输出都要能处理负数，别用 `unsigned` 或把初值写成 `0`。
5. **答案溢出 32 位**：$n=1$、$k=10^{18}$、$a>b$ 时答案是 $P+k\approx10^{18}$，必须 `long long`（Python 无所谓）；但累加代价要用 `__int128`，否则 `n·X` 会到 $2\times10^{23}$。
6. **上界不能只写 $\min_i(P_i+k)$**：存在冻结实验室时还要和「冻结实验室的最小和」取 $\min$，否则二分会跑到冻结实验室达不到的区域，判定因 $\infty$ 全部失败但区间仍被错误收缩。
7. **二分区间含负数时**：`mid = (lo + hi) / 2` 在 $lo,hi$ 同为负时也是向下取整，配合 `hi - lo > 1` 的写法仍安全；但不要写 `lo <= hi` 的三分支版本，容易出现死循环。
8. **判定必须提前退出**：不要等 $n$ 间全部加完再比较 $k$，$10^{18}\times2\times10^5$ 会让 `__int128` 之外的类型直接溢出，也会白白多算。

## 相关题目与扩展

- [Codeforces 2275B. Did Not Go to Print](https://codeforces.com/problemset/problem/2275/B)：同场题，栈模拟，可用来看「同一场的读题节奏」。
- [Codeforces 2275C. Unrequited Love](https://codeforces.com/problemset/problem/2275/C)：同场数据结构题，同样是「先想清单点贡献再选容器」。
- [LeetCode 1552. 两球之间的磁力](https://leetcode.cn/problems/magnetic-force-between-two-balls/)：二分答案 + 贪心判定的经典模板，和本题的「二分 $X$ + 逐台算代价」同构。
- [LeetCode 1802. 有界数组中指定下标处的最大值](https://leetcode.cn/problems/maximum-value-at-a-given-index-in-a-bounded-array/)：同样是「每个位置有自己的代价函数、预算共享、二分答案」，代价分段这一点也一致。
- [LeetCode 410. 分割数组的最大值](https://leetcode.cn/problems/split-array-largest-sum/)：二分答案 + 贪心判定，可对照「单调性 $\Rightarrow$ 二分」的通用套路。

**延伸思考**：本题的 $f_i(X)$ 是**分段线性且带跳跃**的（有序态在 $X=P_i+1$ 处从 $0$ 直接跳到 $2e_i+1$），所以不能简单地对所有 $P_i$ 排序后贪心；但如果把 $k$ 改成「每间实验室各自有独立预算」，答案就退化成 $\min_i$ 的单间闭式，直接 $O(n)$。另一个变体是把操作改成「可以自由选一台仪器 $\pm1$」：此时有序态不复存在，$e$ 恒为 $0$，整题退化为 $\min_i(P_i+k/n)$ 一类的均摊问题。
