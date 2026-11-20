# Codeforces 98B Help King 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/98/B
- **比赛来源**：Codeforces Beta Round 78 (Div. 1 Only) · Problem B（UTC 2011-07-22）
- **难度**：2200
- **标签**：实现、概率、树
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：国王要用一枚公平硬币（正反面各概率 $1/2$）从 $n$ 个骑士中选出**恰好一个**，要求每个骑士被选中的概率都等于 $1/n$。抛硬币的策略可以任意设计（包括"抛到某一步发现结果落在多余的分支上就重抛或继续利用"），但每一步都必须只依赖之前抛出的结果。求**最优策略下**抛掷次数的期望值，输出既约分数 `a/b`。

**约束**：

- $1 \le n \le 10000$：策略空间巨大，必须推公式；但 $n$ 不大，可以 $O(n \log n)$ 地预处理。
- 答案必须是**既约分数**，且分母可能非常长（见 3.4 节，$n=9941$ 时分子分母各有约 1500 位十进制数字）——必须用大整数。
- $n$ 是 2 的幂时答案恰为 $\log_2 n$（整数），例如 $n=4 \Rightarrow 2/1$、$n=2 \Rightarrow 1/1$。
- $n=1$ 时不需要抛硬币，期望为 $0$，输出 `0/1`。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
2

输出：
1/1
```

官方样例 2（输入 / 输出原样）：

```text
输入：
3

输出：
8/3
```

官方样例 3（输入 / 输出原样）：

```text
输入：
4

输出：
2/1
```

**样例 1 走查**：$n=2$ 抛一次即可，期望 $1$，写作 `1/1`。

**样例 2 走查**：$n=3$。抛 2 次得到 4 个等概率结果：把其中 3 个分别判给 3 个骑士，剩下 1 个结果"作废"；但作废的那 1 个分支本身仍是 $1/4$ 的概率质量，可以和后续抛掷继续组合，而不是白白重来。按 3.2 的公式逐项算：

$$\frac{2^0\bmod 3}{2^0}+\frac{2^1\bmod 3}{2^1}+\frac{2^2\bmod 3}{2^2}+\cdots = 1+1+\frac14+\frac14+\frac1{16}+\frac1{16}+\cdots = 2+\frac{2\cdot\frac14}{1-\frac14} = 2+\frac23 = \frac83.$$

（另一种等价看法：$1/3 = 0.010101\ldots_2$，每个骑士的叶子深度是 $2,4,6,\dots$，期望 $3\sum_{j\ge1}2j\,2^{-2j} = \frac83$。）

**样例 3 走查**：$n=4$ 抛 2 次得到 4 个等概率结果，一一对应，期望 $2$。

**观察 1**：任何策略都是一棵**二叉树**：每个内部结点是一次抛掷，左右儿子是两种结果；叶子标注"选中的骑士"。叶子深度为 $d$ 时其概率为 $2^{-d}$。策略合法 $\iff$ 每个骑士的所有叶子的概率和恰好是 $1/n$。

**观察 2**：把"选骑士"看成对均匀随机比特流做**无偏抽取**。每次抛掷产生 1 个公平比特，问题变成：用最少（期望）的比特数从 $n$ 个等概率结果中取一个。

**观察 3**：$n = 2^a m$（$m$ 为奇数）时可以先抛 $a$ 次把范围缩到 $m$，所以 $E(2^a m) = a + E(m)$。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

直觉做法是"抛 $k = \lceil \log_2 n\rceil$ 次，落在 $[0,n)$ 内就接受，否则重来"，期望 $k\cdot \frac{2^k}{n}$。对 $n=3$ 它给出 $2\cdot\frac43 = \frac83$ ✓，但对 $n=5$ 它给出 $3\cdot\frac85 = 4.8$，而最优是 $3.6$。原因是被拒的那部分**概率质量并没有浪费**，可以留到下一轮继续用（"带进位的拒绝采样"）。

真正的瓶颈是：如何刻画"最优"。答案是 **Knuth–Yao 的 DDG 树**（discrete distribution generating tree）：每一步都尽可能多地"结算"叶子，剩下的未定分支继续参与后面的抛掷。

### 3.2 核心观察：未定分支数 = $2^k \bmod n$

![抛硬币的决策树](../../../images/cf98b_tree.svg)

设树在第 $k$ 层有 $2^k$ 个结点。**贪心构造**：在第 $k$ 层，尽量把"能凑齐一整组 $n$ 个结果"的结点判成叶子；因为每次凑齐一组就要用掉 $n$ 个结点，所以第 $k$ 层结算完后，仍未定的结点数恰好是

$$I_k = 2^k \bmod n .$$

（$I_0 = 1$；每往下一层结点翻倍，能结算的叶子数就是"凑够 $n$ 的组数"，余数正是 $\bmod n$ 的余数。）

于是抛掷次数 $T$ 满足 $P(T > k) = I_k / 2^k$，从而

$$E[T] = \sum_{k\ge 0} P(T>k) = \sum_{k\ge 0}\frac{2^k \bmod n}{2^k}.$$

### 3.3 算法流程：把无穷和化成既约分数

![化为分数](../../../images/cf98b_fraction.svg)

1. 写 $n = 2^a m$，$m$ 为奇数。由 3.2 的公式，前 $a$ 项都是 $1$（因为 $2^k < 2^a \le n$ 时 $2^k \bmod n = 2^k$），而 $k \ge a$ 之后 $\dfrac{2^k\bmod n}{2^k} = \dfrac{2^{k-a}\bmod m}{2^{k-a}}$，所以
   $$E(n) = a + \sum_{j\ge0}\frac{2^j\bmod m}{2^j} = a + E(m).$$
2. $m=1$ 时 $E = a$，答案 $\frac{a}{1}$。
3. $m>1$ 时，$c_j = 2^j \bmod m$ 是周期数列，周期 $t = \operatorname{ord}_m(2)$（$2$ 模 $m$ 的阶，$m$ 奇所以 $2$ 与 $m$ 互素）。于是
   $$\sum_{j\ge0}\frac{c_j}{2^j} = \frac{\sum_{j=0}^{t-1} c_j\,2^{\,t-j}}{2^t-1}.$$
   分子用 Horner 法 $O(t)$ 次"乘 2 加常数"算，分母是 $2^t-1$。
4. 加上整数部分 $a$：$\;E = \dfrac{a\,(2^t-1) + \sum_j c_j 2^{t-j}}{2^t-1}$，再用最大公约数约分。

### 3.4 规模与精度

$t = \operatorname{ord}_m(2) \le \varphi(m) \le 10000$，所以分母 $2^t-1$ 最多约 $10^4$ 个二进位（约 3000 位十进制）。实测 $n \le 10000$ 中分母最长的是 $n = 9967$：分母约 $4983$ 个二进位；$n = 9941$ 时分子分母都接近 $5000$ 个二进位。因此：

- Python 直接用内置大整数；
- C++ 必须手写大整数（加、减、乘小整数、移位、二进制 gcd、长除法），本文字节给出完整实现。

### 3.5 样例走查

| $n$ | $a$ | $m$ | $t$ | 化简前 | 答案 |
|-----|-----|-----|-----|--------|------|
| 2 | 1 | 1 | — | $1/1$ | `1/1` |
| 3 | 0 | 3 | 2 | $(1\cdot4+2\cdot2)/(4-1)=8/3$ | `8/3` |
| 4 | 2 | 1 | — | $2/1$ | `2/1` |
| 5 | 0 | 5 | 4 | $54/15 = 18/5$ | `18/5` |
| 6 | 1 | 3 | 2 | $1+8/3 = 11/3$ | `11/3` |
| 1 | 0 | 1 | — | $0/1$ | `0/1` |

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `1` | `0/1` | 不用抛 |
| `5` | `18/5` | 带进位的拒绝采样 |
| `7` | `24/7` | $1/7 = 0.001001\ldots_2$ |
| `8` | `3/1` | 2 的幂 |
| `10000` | （约 3000 位的大分数） | 必须大整数 |

## 4. 正确性证明

**引理 1（策略 ↔ 二叉树）**：任何合法策略对应一棵二叉树，叶子深度 $d$ 的概率为 $2^{-d}$；策略使每个骑士概率恰为 $1/n$ 当且仅当对每个骑士 $i$，其叶子集合满足 $\sum_{d\in L_i}2^{-d} = 1/n$。

**证明**：策略的每一步只依赖已抛出的结果，故可展开成二叉树；深度 $d$ 的结点对应一条长为 $d$ 的抛掷序列，概率 $2^{-d}$。叶子对应"策略在此停止并宣布结果"。"每个骑士被选中概率 $1/n$"即其叶子的概率和。∎

**引理 2（未定分支数）**：按"每层尽量结算"的贪心构造，第 $k$ 层结算后未定的结点数为 $2^k\bmod n$。

**证明**：对 $k$ 归纳。$k=0$：$1$ 个结点，$1\bmod n=1$。设第 $k$ 层未定 $I_k$ 个，则第 $k+1$ 层有 $2I_k$ 个结点；其中每 $n$ 个结点可以结算出"每个骑士各一个叶子"，故结算后剩 $2I_k \bmod n$ 个。由 $I_k = 2^k\bmod n$ 得 $2I_k\bmod n = 2^{k+1}\bmod n$。∎

**引理 3（期望公式）**：贪心策略的期望抛掷次数 $E=\sum_{k\ge0}\dfrac{2^k\bmod n}{2^k}$，并且任何合法策略的期望都不小于它。

**证明**：期望的尾和公式 $E[T]=\sum_{k\ge0}P(T>k)$；"策略在第 $k$ 层仍未停止"当且仅当走到该层的结点未定，概率为 $I_k/2^k$，代入引理 2 得公式。最优性：若某策略在第 $k$ 层没有把可结算的结点全部结算，则必有一个本可在第 $k$ 层结算的结果被推迟到更深的层，交换论证可把它提前而严格减小 $E$；贪心逐层结算，故最优。∎

**引理 4（闭式化简）**：$E = a + \dfrac{\sum_{j<t}c_j2^{t-j}}{2^t-1}$，其中 $n=2^am$、$t=\operatorname{ord}_m(2)$、$c_j=2^j\bmod m$。

**证明**：由引理 3，$E(n)=\sum_k (2^k\bmod n)/2^k$。对 $k<a$，$2^k<n$ 故 $2^k\bmod n=2^k$，贡献 $a$ 个 $1$；对 $k\ge a$，$2^k\bmod n = 2^a(2^{k-a}\bmod m)$（因为 $n=2^am$），该项等于 $(2^{k-a}\bmod m)/2^{k-a}$。故 $E(n)=a+\sum_{j\ge0}c_j2^{-j}$。又 $c$ 以 $t$ 为周期，$\sum_{j\ge0}c_j2^{-j}=\sum_{j<t}c_j2^{-j}\cdot\frac{1}{1-2^{-t}}=\frac{\sum_{j<t}c_j2^{t-j}}{2^t-1}$。∎

**定理**：算法输出的既约分数等于最优期望值。

**证明**：由引理 3、4，期望值为 $(a(2^t-1)+\sum_jc_j2^{t-j})/(2^t-1)$；算法用 Horner 法正确算出分子（$y\leftarrow2y+c_j$ 累加后再乘 2）、分母 $2^t-1$，加上整数部分并用 gcd 约分，得到既约分数，故输出正确。∎

## 5. 复杂度分析

- **时间**：求阶 $O(t)$ 次模乘；Horner $O(t)$ 次大整数乘 2；gcd 用二进制算法 $O(t\cdot t/64)$ 级别；$t\le 10000$。实测 $n=9941$（分母约 5000 位）C++ 端到端 $35.8$ ms，Python $30.2$ ms。
- **空间**：$O(t)$ 个机器字（约 $t/32$ 个 32 位字）。
- **与时限的关系**：2 s 时限下余量在 50 倍以上。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

// 简化大整数：base 1e9，小端存储
struct Big {
    vector<uint32_t> d;          // 若为空表示 0
    static const uint32_t BASE = 1000000000u;

    Big() {}
    explicit Big(long long v) { while (v > 0) { d.push_back((uint32_t)(v % BASE)); v /= BASE; } }
    bool zero() const { return d.empty(); }
    void trim() { while (!d.empty() && d.back() == 0) d.pop_back(); }

    int cmp(const Big& o) const {
        if (d.size() != o.d.size()) return d.size() < o.d.size() ? -1 : 1;
        for (int i = (int)d.size() - 1; i >= 0; --i)
            if (d[i] != o.d[i]) return d[i] < o.d[i] ? -1 : 1;
        return 0;
    }
    Big add(const Big& o) const {
        Big r; size_t n = max(d.size(), o.d.size());
        r.d.assign(n, 0); unsigned long long carry = 0;
        for (size_t i = 0; i < n; ++i) {
            unsigned long long s = carry + (i < d.size() ? d[i] : 0) + (i < o.d.size() ? o.d[i] : 0);
            r.d[i] = (uint32_t)(s % BASE); carry = s / BASE;
        }
        if (carry) r.d.push_back((uint32_t)carry);
        return r;
    }
    Big sub(const Big& o) const {   // 要求 *this >= o
        Big r; r.d.assign(d.size(), 0); long long borrow = 0;
        for (size_t i = 0; i < d.size(); ++i) {
            long long cur = (long long)d[i] - borrow - (i < o.d.size() ? o.d[i] : 0);
            if (cur < 0) { cur += BASE; borrow = 1; } else borrow = 0;
            r.d[i] = (uint32_t)cur;
        }
        r.trim(); return r;
    }
    Big mulSmall(uint32_t k) const {
        Big r; if (k == 0 || zero()) return r;
        r.d.assign(d.size(), 0); unsigned long long carry = 0;
        for (size_t i = 0; i < d.size(); ++i) {
            unsigned long long cur = (unsigned long long)d[i] * k + carry;
            r.d[i] = (uint32_t)(cur % BASE); carry = cur / BASE;
        }
        while (carry) { r.d.push_back((uint32_t)(carry % BASE)); carry /= BASE; }
        return r;
    }
    Big shl1() const { return mulSmall(2); }
    Big shr1() const {
        Big r; r.d.assign(d.size(), 0); unsigned long long carry = 0;
        for (int i = (int)d.size() - 1; i >= 0; --i) {
            unsigned long long cur = (unsigned long long)d[i] + carry * BASE;
            r.d[i] = (uint32_t)(cur / 2); carry = cur % 2;
        }
        r.trim(); return r;
    }
    bool even() const { return d.empty() || (d[0] % 2 == 0); }
    string str() const {
        if (zero()) return "0";
        vector<uint32_t> chunks;
        Big cur = *this;
        while (!cur.zero()) {
            vector<uint32_t> q(cur.d.size(), 0);
            unsigned long long rem = 0;
            for (int i = (int)cur.d.size() - 1; i >= 0; --i) {
                unsigned long long v = rem * BASE + cur.d[i];
                q[i] = (uint32_t)(v / BASE);
                rem = v % BASE;
            }
            Big nq; nq.d = q; nq.trim();
            chunks.push_back((uint32_t)rem);
            cur = nq;
        }
        string s = to_string(chunks.back());
        char buf[16];
        for (int i = (int)chunks.size() - 2; i >= 0; --i) {
            snprintf(buf, sizeof(buf), "%09u", chunks[i]);
            s += buf;
        }
        return s;
    }
};

Big gcdBig(Big a, Big b) {
    if (a.zero()) return b;
    if (b.zero()) return a;
    int shift = 0;
    while (a.even() && b.even()) { a = a.shr1(); b = b.shr1(); ++shift; }
    while (a.even()) a = a.shr1();
    while (true) {
        while (b.even()) b = b.shr1();
        if (a.cmp(b) > 0) swap(a, b);
        b = b.sub(a);
        if (b.zero()) break;
    }
    for (int i = 0; i < shift; ++i) a = a.shl1();
    return a;
}

pair<Big, Big> divmodBig(const Big& A, const Big& B) {
    Big q, r;
    if (A.cmp(B) < 0) return {Big(), A};
    q.d.assign(A.d.size(), 0);
    for (int i = (int)A.d.size() - 1; i >= 0; --i) {
        r = r.mulSmall(Big::BASE);
        if (A.d[i]) r = r.add(Big((long long)A.d[i]));
        long long lo = 0, hi = (long long)Big::BASE - 1;
        Big best;
        while (lo <= hi) {
            long long mid = (lo + hi) / 2;
            Big cand = B.mulSmall((uint32_t)mid);
            if (cand.cmp(r) <= 0) { best = cand; q.d[i] = (uint32_t)mid; lo = mid + 1; }
            else hi = mid - 1;
        }
        r = r.sub(best);
    }
    q.trim();
    return {q, r};
}

int main() {
    long long n;
    if (!(cin >> n)) return 0;
    int a = 0;
    long long m = n;
    while (m % 2 == 0) { m /= 2; ++a; }
    Big num, den;
    if (m == 1) {
        num = Big(a); den = Big(1);
    } else {
        int t = 1;
        long long x = 2 % m;
        while (x != 1) { x = (x * 2) % m; ++t; }
        Big y((long long)(1 % m));
        long long c = 1 % m;
        for (int j = 1; j < t; ++j) {
            c = (c * 2) % m;
            y = y.shl1().add(Big(c));
        }
        num = y.shl1();
        Big one(1);
        Big p = one;
        for (int i = 0; i < t; ++i) p = p.shl1();
        den = p.sub(one);
        num = den.mulSmall((uint32_t)a).add(num);
    }
    Big g = gcdBig(num, den);
    Big qn = num, qd = den;
    if (g.cmp(Big(1)) > 0) {
        qn = divmodBig(num, g).first;
        qd = divmodBig(den, g).first;
    }
    cout << qn.str() << '/' << qd.str() << '\n';
    return 0;
}
```

### Python3

```python
import sys
from math import gcd


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = 0
    m = n
    while m % 2 == 0:
        m //= 2
        a += 1
    if m == 1:
        num, den = a, 1
    else:
        t = 1
        x = 2 % m
        while x != 1:
            x = (x * 2) % m
            t += 1
        y = 1 % m
        c = 1 % m
        for _ in range(1, t):
            c = (c * 2) % m
            y = 2 * y + c
        num = 2 * y
        den = (1 << t) - 1
        num += a * den
    g = gcd(num, den)
    sys.stdout.write(f"{num // g}/{den // g}\n")


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **$n=1$**：不需要抛硬币，输出 `0/1`（不是 `1/1`，也不是 `0/0`）。
2. **$n$ 是 2 的幂**：$m=1$，答案是整数 $a$，要写成 `a/1`。
3. **`0/1` 的约分**：$\gcd(0,1)=1$，别把 0 当特殊情况写错（`gcd(0,0)` 才无意义）。
4. **不要用简单拒绝采样的 $k\cdot2^k/n$**：$n=5$ 时它给 4.8，正确答案 3.6；两者的区别正是"被拒概率质量是否复用"。
5. **大整数必须真的大**：$n=9941$ 的答案分子分母各有约 5000 个二进位，用 `long long` 会溢出；题面没有保证答案很小。
6. **求阶循环的终止**：$m$ 为奇数时 $2$ 与 $m$ 互素，必然存在 $t$ 使 $2^t\equiv1$，循环会终止；但要注意 $m=1$ 时 $2\bmod1=0$，必须先把 $m=1$ 单独处理。
7. **`1 % m`**：$m=1$ 时 `1 % m = 0`，代码里用 `1 % m` 保持安全（虽然 $m=1$ 已提前返回）。
8. **输出格式**：`a/b`，没有前导零，中间是斜杠，末尾换行。
9. **性能**：大整数除法用逐位二分，虽然慢但只有两次；不要每次 gcd 迭代都做除法（用二进制 gcd）。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：3 / 3 通过（`1/1`、`8/3`、`2/1`）。
- **交叉验证**：对 $n = 1 \dots 3000$ 共 **3000 组**，C++（手写大整数）与 Python（内置大整数）输出逐字一致；另抽查 $n = 8191, 8192, 9941, 9973, 9999, 10000$ 等边界，两者也完全一致。
- **独立数值验证**：对 76 个 $n$（含 1..60、各种 2 的幂附近、大素数），用高精度十进制直接截断求和 $\sum_{k=0}^{200}\frac{2^k\bmod n}{2^k}$（截断误差 $<2^{-200}$），与程序输出的分数值比较，相对误差全部 $<10^{-25}$，**76 / 76 一致**；同时验证了大 $n$ 输出的分子分母互素。
- **最大约束性能**：$n=9941$（分母约 5000 个二进位）C++ 端到端 10 次平均 $35.8$ ms、Python $30.2$ ms。
- **图片校验**：两张 SVG（`cf98b_tree.svg`、`cf98b_fraction.svg`）通过 `xml.etree.ElementTree.parse`，文本块估算未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError: true`）渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 98A Help Victoria the Wise](https://codeforces.com/problemset/problem/98/A)：同场 A 题，Burnside 计数。
- [Codeforces 98E Help Shrek and Donkey](https://codeforces.com/problemset/problem/98/E)：同场 E 题，博弈 + 概率。
- [Codeforces 24D Broken robot](https://codeforces.com/problemset/problem/24/D)：期望的线性递推。
- [LeetCode 808. 分汤](https://leetcode.cn/problems/soup-servings/)：概率 DP 的入门。
- [LeetCode 837. 新 21 点](https://leetcode.cn/problems/new-21-game/)：概率递推。

**延伸思考**：

1. **如果硬币不均匀**（正面概率 $p$）：最优期望变成 $\sum_k \frac{?}{}$，需要按"可分辨的二进制串"重新推导，一般没有闭式。
2. **如果要求一次抛掷能选多个骑士**（批量出货）：问题变成"变长编码的期望长度"，可用 Huffman 类算法。
3. **如果要求最坏情况抛掷次数最小**：答案是"存在 $k$ 使 $n\mid 2^k$"，否则无解——与期望最优完全不同。
4. **如果 $n$ 很大**（如 $10^{18}$）：阶的计算需要分解 $m$ 并用 $\varphi$ 的因子检验，本文的 $O(t)$ 直接循环不再可行。
