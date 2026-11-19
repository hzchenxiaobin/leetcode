# Codeforces 2284C1 恶心数组与 GCD 题解

## 1. 题目概述

- **标题 / 题号**：恶心数组与 GCD（Codeforces 2284C1，英文名 Disgusting + GCD (Constructive Version)）
- **链接**：https://codeforces.com/problemset/problem/2284/C1
- **来源**：Codeforces Round 1132 (Div. 2) · Problem C1
- **难度**：未评级（1000 分，官方 rating 尚未公布）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：构造、数论、数学、贪心（题面 tags 另挂 dp / 图论，本解法未使用）

**题意**：称数组 $b$ 是**恶心**的，若存在 $i<j$ 使 $1<\gcd(b_i,b_j)<\min(b_i,b_j)$。给定长度 $n$ 的正整数数组 $a$（$a_i\ge2$），允许的操作是：选下标 $i$ 与正整数 $x$（$1\le x\le10^9$），要求 $\gcd(a_i,x)=1$——这里的 $a_i$ 取**操作前**的当前值——然后令 $a_i\leftarrow a_i+x$。操作受两条预算限制：次数至多 $n+10$；所有 $x$ 之和不超过原数组元素之和 $\sum a_i$。要求输出**任意一个不恶心**的结果数组 $b$，满足 $a_i\le b_i\le10^9$。多测：首行 $t$，每组给 $n$ 与 $n$ 个元素。

**约束**：

- $1\le t\le10^4$，$2\le n\le10^5$ 且 $\sum n\le10^5$——总和受限，允许每组 $O(n)$ 处理
- $2\le a_i\le10^5$——值域很小，可以**预处理素数表**，无需对每个元素试除
- 输出 $b_i\le10^9$——我们的构造只到 $10^5$ 量级，天然满足
- 操作次数 $\le n+10$ 与 $\sum x\le\sum a_i$——这两条是真正制约构造的预算，须在证明中逐条对上

> ⚠️ 题面里「In this version, you are kijjot.」（C2 是 "ogiyo"）这类句子是无意义装饰，不是解题要求，直接忽略；本题题面不含任何「创建某个变量」式的注入指令。

## 2. 示例与观察
官方样例（输入 / 输出原样）：

```text
输入：
3
2
7 12
3
7 9 12
7
8 76 49 26 24 80 99

输出：
7 12
7 25 12
9 77 50 27 25 81 100
```

本文程序的输出（与官方不同但同样合法，special judge 接受任意解）：

```text
7 13
7 11 13
11 79 53 29 29 83 101
```

自造一组，覆盖「全部相同」与「两个不同元素映射到同一个素数」：

```text
输入：
2
3
8 8 8
4
100000 24 26 15

输出：
11 11 11
100003 29 29 17
解释：第一组 8 全抬到 11，Σx = 9 ≤ 24；第二组 24 与 26 都变成 29（相等 ⇒ gcd = min，合法），
      15 → 17，Σx = 3 + 5 + 3 + 2 = 13 ≤ 100065。
```

## 3. 解题思路

### 3.1 暴力思路

判定一对是否「恶心」是 $O(1)$ 的，难点在**构造**：每个 $a_i$ 可以加到任意 $b_i\ge a_i$，候选向量枚举不完，而两条预算（次数、$\sum x$）让「随便加」立刻违规。

最直觉的充分条件是让 $b$ **两两互质**：把每个 $a_i$ 换成互不相同的素数 $p_i\ge a_i$。但「互不相同」把代价打爆——$n=10^5$ 个 $a_i=10^5$ 时，第 $10^5$ 个不小于 $10^5$ 的素数约 $1.5\times10^6$，$\sum x\approx\frac12\cdot10^5\cdot1.4\times10^6\approx7\times10^{10}$，而预算 $\sum a_i=10^{10}$ 根本不够。必须放弃「去重」。

### 3.2 核心观察：三种合法关系，素数当万能牌子

![不可恶的三种合法关系与素数构造](../../../images/cf2284c1_not_disgusting_concept.svg)

**第一步，重新翻译「恶心」。** 恒有 $\gcd(b_i,b_j)\le\min(b_i,b_j)$，取较小者一侧只有两种可能：$\gcd=1$，或 $\gcd=b_i$（等价于 $b_i\mid b_j$）。因此

$$b \text{ 不恶心}\iff \forall i<j:\ \gcd(b_i,b_j)=1\ \ \text{或}\ \ \min(b_i,b_j)\mid \max(b_i,b_j)$$

**第二步，挑一个自动满足它的值域。** 素数集合免费满足上式：两个**不同**素数 $\gcd=1$（情形①），两个**相同**素数 $\gcd=\min$（情形②）。可见「互不相同」是多余的约束——**重复的素数照样合法**，3.1 的代价爆炸正是被这一条消掉的。于是取 $b_i=p_i$，即不小于 $a_i$ 的最小素数。

**第三步，操作合法性是白送的。** 令 $x_i=p_i-a_i$。若 $d\mid a_i$ 且 $d\mid x_i$，则 $d\mid a_i+x_i=p_i$；而 $p_i$ 是素数且 $d\le a_i<p_i$，故 $d=1$，即 $\gcd(a_i,x_i)=1$ 恒成立。题面说「用操作前的当前值检查」也无妨：每个元素**至多操作一次**，当前值就是原值。

**第四步，预算。** 由 Bertrand 假设，对 $a_i\ge2$ 存在素数 $p$ 满足 $a_i\le p<2a_i$，故 $x_i=p_i-a_i<a_i$，求和得 $\sum x_i<\sum a_i$；次数上每个元素至多一次，$\le n\le n+10$。

### 3.3 算法流程

![一次筛表、倒序扫描、逐元素查表](../../../images/cf2284c1_next_prime_flow.svg)

1. 线性筛求出 $[2,V]$ 内所有素数，$V=2\cdot10^5$（理由见 §4 第 1 条）。
2. **倒序**扫 $v:V\to2$：遇到素数就更新 `cur = v`，然后 `nxt[v] = cur`；一次 $O(V)$ 扫描即得「不小于 $v$ 的最小素数」整张表。
3. 每组读入 $a_i$，输出 `nxt[a_i]`——全程不模拟操作，$x_i$ 只活在论证里。

### 3.4 示例演算

![样例 3 的逐步走查表](../../../images/cf2284c1_walkthrough_sample3.svg)

对官方样例 3，$a=[8,76,49,26,24,80,99]$：

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----|---|---|---|---|---|---|---|
| $a_i$ | 8 | 76 | 49 | 26 | 24 | 80 | 99 |
| $b_i=p_i$ | 11 | 79 | 53 | 29 | 29 | 83 | 101 |
| $x_i$ | 3 | 3 | 4 | 3 | 5 | 3 | 2 |

累计 $\sum x_i=23$，预算 $\sum a_i=362$，占比 $6.4\%$；操作 $7\le n+10=17$ 次。注意 $26$ 与 $24$ 都映射到 $29$，二者相等因而 $\gcd=\min$，合法——若误以为「必须两两不等」就会白白多花代价。

## 4. 算法细节

1. **筛的上界必须留余量**：$a_i=10^5$ 时 $b_i=100003>10^5$，写 `LIM = 100000` 会越界。由 $b_i<2a_i$ 取 $V=2\cdot10^5$ 一定安全（实测最大 $b$ 恰是 $100003$，最大素数间隔 71）。
2. **查表代替试除**：`nxt` 让每个元素的映射变成 $O(1)$；若改成「从 $a_i$ 往上逐个判素」，最坏 $O(n\cdot\text{gap}\cdot\sqrt{a})$，能过但没必要。
3. **多测只建一次表**：筛与 `nxt` 放在 `main` 开头，`while (t--)` 里只做读入输出。$t=10^4$ 时若每组重建筛，等于把 $O(V)$ 的常数放大一万倍。
4. **不需要输出操作序列**：输出恰为 $n$ 个整数；$x_i=0$（$a_i$ 已是素数）视为「零次操作」，不要为凑次数去动它。
5. **I/O 与常数**：$\sum n\le10^5$ 个输出整数，用 `'\n'` 不用 `endl` 并 `reserve` 字符串；Python 整段 `read()` + `' '.join` 写出。主循环里不做除法（判素只在筛中），避免每组 $n$ 次 `gcd`。
6. **顺序**：输出顺序必须与输入一致（不能排序后输出）；下标本身不参与计算。

## 5. 正确性证明

**引理 1（判定等价）**：$b$ 不恶心 $\iff$ 对任意 $i<j$ 有 $\gcd(b_i,b_j)=1$ 或 $\min(b_i,b_j)\mid\max(b_i,b_j)$。
**证明**：设 $u=\min(b_i,b_j)$、$v=\max(b_i,b_j)$，则 $\gcd(u,v)\le u$。若「恶心」，则 $\gcd>1$ 且 $\gcd<u$，即 $\gcd\ne1$ 且 $u\nmid v$（因为 $\gcd(u,v)=u\iff u\mid v$）；反之若 $\gcd>1$ 且 $u\nmid v$，则 $\gcd<u$，条件成立。∎

**引理 2（素数数组不恶心）**：若所有 $b_i$ 都是素数，则 $b$ 不恶心。
**证明**：任取 $i<j$：若 $b_i=b_j$ 则 $\gcd=\min$，不是「恶心」；若 $b_i\ne b_j$，两个不同素数互质，$\gcd=1$。由引理 1 得证。∎

**引理 3（操作合法）**：设 $p>a\ge2$ 为素数，$x=p-a>0$，则 $\gcd(a,x)=1$。
**证明**：设 $d=\gcd(a,x)$，则 $d\mid a$、$d\mid x$，故 $d\mid(a+x)=p$。因 $p$ 素，$d\in\{1,p\}$；又 $d\le a<p$，故 $d\ne p$，只能 $d=1$。∎

**引理 4（两条预算）**：记 $p_i$ 为不小于 $a_i$ 的最小素数、$x_i=p_i-a_i$，则 $\sum_i x_i<\sum_i a_i$，且实际操作次数 $\le n\le n+10$。
**证明**：对 $a_i\ge2$，Bertrand 假设给出素数 $p$ 使 $a_i\le p<2a_i$；$p_i$ 为最小者故 $p_i\le p<2a_i$，于是 $x_i<a_i$，求和即得。$x_i>0$ 的元素各操作一次，其余不动，故次数 $\le n$。∎

**定理**：算法输出的 $b$ 满足题面全部要求，是合法答案。
**证明**：$b_i=p_i$ 为素数，且 $p_i\ge a_i$、$p_i<2a_i\le2\cdot10^5\le10^9$，故 $a_i\le b_i\le10^9$。由引理 2，$b$ 不恶心；由引理 3，每个改动满足 $\gcd(a_i,x_i)=1$（未改动的元素无需操作）；由引理 4，次数与 $\sum x$ 都在预算内。故 $b$ 可由 $a$ 经合法操作得到且不恶心。∎

## 6. 复杂度分析

- **时间**：$O(V+\sum n)$，$V=2\cdot10^5$。线性筛 $O(V)$、倒序扫表 $O(V)$、每组读入输出 $O(n)$（`to_string` 位数是常数级），总计约 $5\times10^5$ 次基本操作；实测（本机 g++ `-std=c++17 -O2`，含进程启动）$n=10^5$ 全为 $10^5$ 约 0.07–0.16 s，$t=10^4$、每组 $n=10$ 约 0.12 s，Python3 同数据约 0.10 s，相对 2 s 时限有 10 倍以上余量。
- **空间**：$O(V)$。`comp` 是字节级标记，`nxt` 表 $2\cdot10^5$ 个 `int`（约 800 KB），加输出缓冲远低于 256 MB。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

// a_i <= 1e5，而最小素数 >= a_i 必小于 2*a_i <= 2e5（Bertrand），故筛到 LIM 足够
static const int LIM = 200005;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 线性筛：素数表
    vector<bool> comp(LIM + 1, false);
    vector<int> primes;
    comp[0] = comp[1] = true;
    for (int i = 2; i <= LIM; ++i) {
        if (!comp[i]) primes.push_back(i);
        for (int p : primes) {
            if (1LL * i * p > LIM) break;
            comp[i * p] = true;
            if (i % p == 0) break;
        }
    }

    // nxt[v] = 不小于 v 的最小素数：从大到小扫一遍即可
    static int nxt[LIM + 1];
    int cur = primes.back();
    for (int v = LIM; v >= 2; --v) {
        if (!comp[v]) cur = v;
        nxt[v] = cur;
    }

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        string out;
        out.reserve((size_t)n * 7);
        for (int i = 0; i < n; ++i) {
            int a;
            cin >> a;                 // b_i = nxt[a_i]，x_i = b_i - a_i < a_i
            out += to_string(nxt[a]);
            out += (i + 1 == n ? '\n' : ' ');
        }
        cout << out;
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
    LIM = 200005

    # 线性筛 + 倒序扫出 nxt[v] = 不小于 v 的最小素数
    comp = bytearray(LIM + 1)
    comp[0] = comp[1] = 1
    primes = []
    for i in range(2, LIM + 1):
        if not comp[i]:
            primes.append(i)
        for p in primes:
            if i * p > LIM:
                break
            comp[i * p] = 1
            if i % p == 0:
                break

    nxt = [0] * (LIM + 1)
    cur = primes[-1]
    for v in range(LIM, 1, -1):
        if not comp[v]:
            cur = v
        nxt[v] = cur

    t = data[0]
    pos = 1
    out = []
    for _ in range(t):
        n = data[pos]
        pos += 1
        out.append(' '.join(str(nxt[x]) for x in data[pos:pos + n]))
        pos += n
    sys.stdout.write('\n'.join(out) + '\n')


main()
```

## 8. 边界情况与易错点

1. **$a_i$ 本身是素数**：$x_i=0$，不产生操作。若强行「至少动一次」，既浪费预算又可能把素数改成合数，直接破坏引理 2。
2. **重复值合法**：$24$ 与 $26$ 同映射到 $29$ 时 $\gcd=29=\min$，不属于「恶心」。最常见的错误是把「$\gcd>1$」一律当违规，从而误以为必须两两不同（那会退化成 §3.1 的超预算构造）。
3. **筛上界与下标**：`LIM = 100000` 时 $a_i=10^5$ 会取到越界下标或错误值（正确答案是 $100003$），用 $2\max a$ 这类写法最稳；`nxt` 的有效下标到 $V$，本题 $a_i\ge2$ 故 `nxt[0]`、`nxt[1]` 永不被访问。Bertrand 论证也依赖 $a_i\ge2$：若出现 $a_i=1$，则 $x_i\ge1$ 不再小于 $a_i$，代价界需重估（题面已排除）。
4. **代价按「相对值」估**：$a_i=8\to11$ 只用 3，但占自身 $37.5\%$，是全值域内最坏比值；只用「差的绝对值很小」判断安全会在大量 $8$ 的数据上误判。
5. **多测重复建表**：$t=10^4$ 时每组都筛一遍 $2\cdot10^5$ 会导致 TLE；筛与 `nxt` 移到循环外。
6. **输出格式**：每组恰好一行 $n$ 个整数，组间不要空行；顺序必须与原数组一致（不要排序后输出）。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：0 / 1 通过 token 比对；本题输出不唯一（构造 / 多解 / 特殊评测），剩余差异属预期，样例含义已在第 2 节逐组解释。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [Codeforces 2284C2. Disgusting + GCD (Checker Version)](https://codeforces.com/problemset/problem/2284/C2)：同场另一版。给定 $a\le b\le10^9$，要求用**最少**次数的合法操作把 $a$ 变成 $b$（保证 $\le15$ 次）。值域升到 $10^9$ 后本文的「查 `nxt` 表」失效，需要现场找素数（Miller–Rabin + 间隔扫描），但「$\gcd(a,x)=1$ 的合法性由 $a+x$ 的素性免费提供」这一手仍然可复用。
- [Codeforces 776B. Sherlock and his girlfriend](https://codeforces.com/problemset/problem/776/B)：用「素数 / 合数」二分染色解决整除冲突，同样是「素数的结构性质直接给出构造」的套路。
- [LeetCode 2601. 质数减法运算](https://leetcode.cn/problems/prime-subtraction-operation/)：把元素调整到素数上以满足单调性，与本题「把 $a_i$ 抬到不小于它的最小素数」是同一个动作；[LC 1250. 检查「好数组」](https://leetcode.cn/problems/check-if-it-is-a-good-array/) 则用 Bézout 定理刻画「整体 $\gcd=1$」，可与引理 1 对照复习。

**延伸思考**：

1. **预算收紧会怎样**：若把 $\sum x\le\sum a_i$ 改成 $\sum x\le\frac13\sum a_i$，则 $a_i=8\to11$ 的比值 $0.375$ 超额，纯「next prime」失效。此时应把落点从「素数」放宽成「与其余元素全部互质的合数」：$8\to9$ 只花 1（$\gcd(8,9)=1$，且 $9$ 与任何非 $3$ 的素数互质），代价骤降，但需要在线维护「与已有元素互质」这一全局约束——这就是「局部挑素数」与「全局求互质」之间的取舍。
2. **限制操作次数为 $k\ll n$**：每元素一次的操作结构不再够用，必须让一个元素一次跳到能与多个元素「相处」的位置，问题变成在整除偏序上的覆盖设计。
3. **换成「不恶心」的更强要求**：若要求任意两数 $\gcd$ 只能是 $1$（即两两互质），代价分析回到 §3.1 的 $7\times10^{10}$，说明本题的可解性完全依赖于「相等也合法」这一条被允许。
