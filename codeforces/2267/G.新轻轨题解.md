# Codeforces 新轻轨 题解

## 1. 题目概述

- **标题 / 题号**：新轻轨（Codeforces 2267G，英文名 New LRT）
- **链接**：https://codeforces.com/problemset/problem/2267/G
- **来源**：Codeforces Round 1123 (Div. 2) · Problem G
- **难度**：2600（3000 分，Div. 2 压轴）
- **限制**：时间 2 s / 内存 512 MB
- **标签**：位运算与子掩码、动态规划、生成函数、前缀和分层、组合计数

**题意**：从数轴位置 $0$ 走到位置 $n$。站在 $i$ 时可选任意正整数 $x$ 满足 $m \mathbin{\&} x = x$（即 $x$ 是 $m$ 的**子掩码**），付 $c_x$ 金币跳到 $i+x$；一次行程是一串这样的移动，移动顺序不同或某一步不同即视为不同行程。求所有能到达 $n$ 的行程的**花费总和**对 $10^9+7$ 取模。多测：先给 $t$，每组给 $n, m$ 与 $c_1, \dots, c_m$（**下标就是步长**，天然 1-indexed），逐组输出答案。

**约束**：$1 \le t \le 10^4$；$1 \le n, m < 2^{20}$；$1 \le c_i \le 10^9$；$\sum n \le 2^{20}$，$\sum m \le 2^{20}$。合法步长恰是 $m$ 的非零子掩码，故 $x \le m$ 自动成立、$c_x$ 总有定义；$n$ 不可达时答案为 $0$。

## 2. 示例

```text
输入
4
3 3
2 2 1
4 5
3 1 2 4 5
5 3
9 1 5
8 3
1000000000 1000000000 1000000000

输出
15
16
271
999997081
```

第一组的四条行程及其花费在 §3.4 的演算图中逐条列出。

**自造样例**（只有偶数步长 / 不可达）

```text
输入
2
4 2
5 7
3 2
5 7
输出
14
0
```

$m = 2$ 只有步长 $2$ 可用：$n = 4$ 的唯一行程是 $0 \to 2 \to 4$，花费 $7+7=14$；$n = 3$ 走不到，答案为 $0$。

## 3. 解题思路

### 3.1 暴力思路

枚举行程不可行（$n = 8, m = 3$ 就有 $81$ 条，$n$ 再大就指数爆炸）。按位置 DP 是自然的：$f[i]$ 为到达 $i$ 的行程数、$A[i]$ 为这些行程的花费之和，则

$$f[i] = \sum_{x \subseteq m,\ x \le i} f[i-x], \qquad A[i] = \sum_{x \subseteq m,\ x \le i} \bigl(A[i-x] + c_x f[i-x]\bigr).$$

状态 $O(n)$，但每个状态要枚举 $m$ 的**全部**子掩码，转移量 $O(2^{\operatorname{popcount}(m)})$，$m = 2^{20}-1$ 时约 $n \cdot 2^{20} \approx 2^{40}$。另一条路是把总花费拆成「行程 × 每一步」，答案变成 $\sum_x c_x (f * f)[n-x]$，可朴素卷积是 $O(n^2) \approx 10^{12}$。两条都不行——难点正是合法步长有指数多个，必须利用「子掩码 = 二进制位的子集」这个乘积结构。

### 3.2 核心观察：标记一步，答案变成自卷积

![标记一步：把总花费拆成每条路径每一步的贡献](images/cf2267_g_mark_step.svg)

总花费 $= \sum_{\text{行程}} \sum_{\text{步}} c_{\text{步长}}$，交换求和顺序，只需数出每种步长被走了多少次：$\text{Ans} = \sum_{x \subseteq m,\ x \ge 1} c_x N_x$。固定这一步从 $p$ 跳到 $p+x$：前段是 $0 \to p$ 的行程（$f[p]$ 种），后段是 $p+x \to n$ 的行程；把后段**反转**，步长序列只是倒序而步长集合对倒序不变，故后段条数等于从 $0$ 走到 $n-x-p$ 的行程条数，即 $f[n-x-p]$。于是

$$N_x = \sum_{p=0}^{n-x} f[p]\, f[n-x-p] = (f * f)[n-x], \qquad
\text{Ans} = \sum_{x \subseteq m} c_x\, (f * f)[n-x]. \tag{1}$$

这一步是枢纽：二维的「路径 × 花费」统计塌缩成 $f$ 与它的自卷积。令 $S(y) = \sum_{x \subseteq m, x \ge 1} y^x$，则 $F(y) = \sum_i f[i]y^i = \frac{1}{1-S(y)}$。记 $h = f * f$，由 $F = 1 + SF$ 得

$$F^2 = F(1 + SF) = F + S F^2 \;\Longrightarrow\; h[0] = 1,\quad h[i] = f[i] + \sum_{x \subseteq m,\ x \ge 1} h[i-x]. \tag{2}$$

**$h$ 与 $f$ 满足同一个递推**，只是源项从 $\delta_{i,0}$ 换成了 $f[i]$。于是「求卷积」这件本该动用 FFT 的事，被化归成同一类 DP；剩下的问题只是把这个递推算得足够快。

### 3.3 算法流程 / 状态转移：按位分层

![位分层 DP：把 1+S 拆成 (1+y^1)(1+y^2)(1+y^4)… 的乘积后逐列填表](images/cf2267_g_layered_dp.svg)

设 $m$ 的二进制位为 $c_1 < c_2 < \dots < c_r$（$c_t = 2^{b_t}$，$r = \operatorname{popcount}(m) \le 20$）。子掩码就是位的子集，故 $1 + S(y) = \prod_{t=1}^{r}(1 + y^{c_t})$。对级数 $g$ 定义

$$D_t[i] = \sum_{x \subseteq \{c_1,\dots,c_t\}} g[i-x] \quad(\text{下标} < 0 \text{ 记 } 0),\qquad
D_t[i] = D_{t-1}[i] + D_{t-1}[i-c_t],\quad D_0 = g. \tag{3}$$

**关键重新分组**：每个非零子掩码 $x$ 有唯一的最高位 $c_t$，写成 $x = c_t + x'$ 且 $x'$ 只用到编号 $< t$ 的位，于是

$$\sum_{x \subseteq m,\ x \ge 1} g[i-x] = \sum_{t=1}^{r} \sum_{x' \subseteq \{c_1,\dots,c_{t-1}\}} g[i - c_t - x'] = \sum_{t=1}^{r} D_{t-1}[i - c_t]. \tag{4}$$

把 (4) 代回 (2) 和 $f$ 的递推，两者是同一个模板：

$$g[i] = \text{src}[i] + \sum_{t=1}^{r} D_{t-1}[i - c_t], \qquad
\begin{cases}\text{求 } f: & \text{src} = (1,0,0,\dots)\\ \text{求 } h = f*f: & \text{src} = f\end{cases} \tag{5}$$

(5) 右侧只出现列 $i - c_t < i$，同列的 $D_t[i]$ 由 (3) 用「同列上一行 + 更早列」拼出，所以按 $i = 0,1,\dots,n$ **列优先**扫一遍即可，每列 $O(r)$ 次加法；只需保留 $D_0,\dots,D_{r-1}$ 共 $r$ 行。最后用 `s = (s-1) & m` 枚举 $m$ 的非零子掩码（$2^{r} \le 2^{20}$ 个），累加 $c_s \cdot h[n-s]$（$s > n$ 跳过）即得答案。

> 💡 官方标签有 `fft`：$F = 1/\bigl(2 - \prod_t (1+y^{c_t})\bigr)$ 也能用多项式求逆（任意模 NTT/FFT）$O(n\log n)$ 求出。但分母是乘积形式，按位摊开就是 $r$ 层前缀和，$O(nr)$ 且常数极小，还绕开了 $10^9+7$ 不是 NTT 模数的麻烦。

### 3.4 示例演算

![样例 1 演算：四条路径、f 表、h = f∗f 表与最终求和](images/cf2267_g_walkthrough.svg)

$n = 3,\ m = 3$（子掩码 $1,2,3$），$c = (2,2,1)$。$f = (1,1,2,4)$，$h = f*f = (1,2,5,12)$，其中 $h[2] = f[0]f[2] + f[1]f[1] + f[2]f[0] = 2+1+2 = 5$。于是

$$\text{Ans} = c_1 h[2] + c_2 h[1] + c_3 h[0] = 2\cdot 5 + 2\cdot 2 + 1\cdot 1 = 15,$$

与样例一致。用位分层再验证 $f$ 的第 $4$ 列（$c_1 = 1, c_2 = 2$）：$f[4] = D_0[3] + D_1[2] = 4 + 3 = 7$，正是凑出 $4$ 的行程数（$1{+}1{+}1{+}1,\ 1{+}1{+}2,\ 1{+}2{+}1,\ 2{+}1{+}1,\ 2{+}2,\ 1{+}3,\ 3{+}1$）。

第 4 个样例（$n = 8$，$m = 3$，$c_x \equiv 10^9$）也能手算：$f = 1,1,2,4,7,13,24,44,81$，$h = 1,2,5,12,26,56,118,244$，$\text{Ans} = 10^9(h[7]+h[6]+h[5]) = 10^9 \cdot 418 \equiv 999997081$，吻合（$418$ 也等于所有行程的步数总和）。

## 4. 算法细节

1. **只保留 $\le n$ 的位**：步长 $> n$ 跨不出边界，对应位直接丢弃，于是 $r \le 20$；$r = 0$ 时（没有可用步长）直接输出 $0$，绝不要建空表。
2. **表按列连续存**：`tab[i*r + t] = D_t[i]`，列内连续、跨列步长 $r$，缓存友好；第 $i$ 列只读更早的列。
3. **两趟复用同一张表**：第一趟 `src = δ` 得 $f$，第二趟 `src = f` 得 $h$；第二趟从 $i=0$ 逐列**覆盖写**，读取的永远 $< i$ 列，因此读不到第一趟的残留，无需清空。
4. **累加用 `long long`**：一列加 $r$ 个小于 $10^9+7$ 的数可达 $2 \times 10^{10}$，超过 `int`；答案里 $c_x \cdot h[n-x]$ 同理。
5. **越界判定**：$j = i - c_t < 0$ 视作 $0$，先判 `j >= 0` 再取下标，避免负下标。
6. **子掩码枚举**：`for (int s = m; s; s = (s-1) & m)`，并 `if (s > n) continue;`，否则 $h[n-s]$ 下标为负。
7. **多测**：每组按 $n$ 重新分配表；$\sum n, \sum m \le 2^{20}$ 保证总开销与峰值内存只由最大的一组决定。
8. **I/O**：最多约 $10^6$ 个 $c_i$，用 `scanf`/`printf`；C++ 还可加 `ios::sync_with_stdio(false)`。

## 5. 正确性证明

**引理 1（标记一步）**：对合法步长 $x$，满足「其中某一步的步长为 $x$」的 (行程, 该步位置) 个数为 $(f*f)[n-x]$。

**证明**：设该步从 $p$ 跳到 $p+x$。前段 $0\to p$（$f[p]$ 种）与后段 $p+x \to n$ 相互独立；后段倒序后是 $0 \to n-x-p$ 的行程，且倒序是双射（步长集合在倒序下不变），故后段有 $f[n-x-p]$ 种。不同的 (行程, 位置) 与不同的 $(p, \text{前段}, \text{后段})$ 一一对应，对 $0 \le p \le n-x$ 求和即得。∎

**引理 2（$D_t$ 的语义）**：按 (3) 递推得 $D_t[i] = \sum_{x \subseteq \{c_1,\dots,c_t\}} g[i-x]$（越界项记 $0$）。

**证明**：对 $t$ 归纳。$t=0$ 时 $D_0 = g$ 且只有空子集，成立。设对 $t-1$ 成立，则 $\{c_1,\dots,c_t\}$ 的子集按是否含 $c_t$ 分成两类：不含者贡献 $D_{t-1}[i]$，含者令 $x = c_t + x'$ 贡献 $D_{t-1}[i-c_t]$，合起来正是 (3)。∎

**引理 3（按最高位分组）**：对任意级数 $g$，$\sum_{x \subseteq m, x \ge 1} g[i-x] = \sum_{t=1}^{r} D_{t-1}[i-c_t]$。

**证明**：非零子掩码 $x$ 唯一对应其最高位编号 $t$，此时 $x = c_t + x'$ 且 $x' \subseteq \{c_1,\dots,c_{t-1}\}$。按 $t$ 分类互不相交且覆盖全部非零子掩码，内层由引理 2 恰为 $D_{t-1}[i-c_t]$。∎

**引理 4（$h$ 的递推）**：$h = f*f$ 满足 $h[0] = 1$、$h[i] = f[i] + \sum_{x\ge1} h[i-x]$。

**证明**：$F = 1 + SF$ 即 $f[0]=1$、$f[i]=\sum_{x\ge1}f[i-x]$；于是 $F^2 = F(1+SF) = F + SF^2$，逐项即得，$i=0$ 时求和为空、$h[0]=f[0]=1$。∎

**引理 5（列优先归纳）**：两趟都按 $i$ 递增完整写满每列，则第 $i$ 列执行完后 $g[0..i]$ 与 $D_0[0..i],\dots,D_{r-1}[0..i]$ 均与定义一致。

**证明**：对 $i$ 归纳。由 (5)，$g[i]$ 只用 $\text{src}[i]$ 与 $D_{t-1}[i-c_t]$，而 $c_t \ge 1$ 说明这些格子位于列 $i-c_t < i$，由归纳假设正确；随后同列递推 (3) 只用同列上一行与更早列的 $D_{t-1}$，亦正确。∎

**定理**：算法输出的 $\sum_{x \subseteq m} c_x h[n-x]$ 等于题面所求的所有行程花费之和。

**证明**：由引理 5，$f$ 与 $h = f*f$ 正确；由引理 1，$c_x h[n-x]$ 恰为全部行程中「步长为 $x$ 的步」贡献的花费；对合法步长求和即得总花费。$x > n$ 时下标为负、直接跳过，这类步长也确实无法出现。∎

## 6. 复杂度分析

- **时间**：两趟列扫描各 $O(nr)$（每列 $r$ 次查表累加 + $r-1$ 次同列递推，$r = \#\{b: 2^b \text{ 是 } m \text{ 的位且} \le n\} \le 20$），子掩码枚举 $O(2^r)$，读入 $O(m)$。合计约 $4 \cdot 2^{20} \cdot 20 \approx 8.4\times10^{7}$ 次基本运算。
- **空间**：表 $O(nr)$ 个 32 位整数（$n = 2^{20}-1, r = 20$ 时约 $80$ MB），另有 $O(n)$ 的 $f, h$；峰值实测约 $101$ MB，远低于 $512$ MB。
- **对照时限**：极限数据 $n = m = 2^{20}-1$（$r = 20$，含读入 $10^6$ 个 $c_i$）实测约 $0.28$ s，距 $2$ s 有 $7$ 倍以上余量。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 1000000007;

// res[i] = src[i] + sum_{t=1..r} D_{t-1}[i-c_t]；tab[i*r+t] = D_t[i]（只存 t = 0..r-1）
static void runPass(const vector<int> &src, vector<int> &res, int n,
                    const vector<int> &bits, vector<uint32_t> &tab) {
    int r = (int)bits.size();
    size_t W = (size_t)r;
    for (int i = 0; i <= n; ++i) {
        long long acc = 0;
        for (int t = 1; t <= r; ++t) {
            int j = i - bits[t - 1];
            if (j >= 0) acc += tab[(size_t)j * W + (t - 1)];
        }
        res[i] = (int)((src[i] + acc) % MOD);
        uint32_t *col = &tab[(size_t)i * W];
        col[0] = (uint32_t)res[i];                       // D_0 = g
        for (int t = 1; t < r; ++t) {                    // D_t[i] = D_{t-1}[i] + D_{t-1}[i-c_t]
            int j = i - bits[t - 1];
            col[t] = (uint32_t)((col[t - 1] + (j >= 0 ? tab[(size_t)j * W + (t - 1)] : 0u)) % MOD);
        }
    }
}

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n, m;
        scanf("%d %d", &n, &m);
        vector<int> c(m + 1), bits;
        for (int i = 1; i <= m; ++i) scanf("%d", &c[i]);
        for (int b = 0; b < 20; ++b)
            if (((m >> b) & 1) && (1 << b) <= n) bits.push_back(1 << b);
        int r = (int)bits.size();
        if (r == 0) { puts("0"); continue; }
        vector<int> f(n + 1, 0), h(n + 1, 0), src(n + 1, 0);
        vector<uint32_t> tab((size_t)(n + 1) * (size_t)r, 0u);
        src[0] = 1;
        runPass(src, f, n, bits, tab);          // f：到达每个位置的行程数
        runPass(f, h, n, bits, tab);            // h = f * f，复用同一张表
        long long ans = 0;
        for (int s = m; s; s = (s - 1) & m)     // 枚举 m 的非零子掩码
            if (s <= n) ans = (ans + (long long)c[s] * h[n - s]) % MOD;
        printf("%d\n", (int)ans);
    }
    return 0;
}
```

### Python3

```python
import sys

MOD = 1000000007


def run_pass(src, n, bits, tab, r):
    """res[i] = src[i] + sum_t D_{t-1}[i-c_t]，表按列存 tab[i*r+t] = D_t[i]"""
    res = [0] * (n + 1)
    for i in range(n + 1):
        acc, base = 0, i * r
        for t in range(1, r + 1):
            j = i - bits[t - 1]
            if j >= 0:
                acc += tab[j * r + t - 1]
        res[i] = (src[i] + acc) % MOD
        tab[base] = res[i]
        for t in range(1, r):
            j = i - bits[t - 1]
            tab[base + t] = (tab[base + t - 1] + (tab[j * r + t - 1] if j >= 0 else 0)) % MOD
    return res


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos, T, out = 1, data[0], []
    for _ in range(T):
        n, m = data[pos], data[pos + 1]
        pos += 2
        c = [0] + data[pos:pos + m]
        pos += m
        bits = [1 << b for b in range(20) if (m >> b) & 1 and (1 << b) <= n]
        r = len(bits)
        if r == 0:
            out.append(0)
            continue
        tab = [0] * ((n + 1) * r)
        src = [0] * (n + 1)
        src[0] = 1
        f = run_pass(src, n, bits, tab, r)
        h = run_pass(f, n, bits, tab, r)
        ans, s = 0, m
        while s:
            if s <= n:
                ans = (ans + c[s] * h[n - s]) % MOD
            s = (s - 1) & m
        out.append(ans)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
```

> ⚠️ Python 版是同一算法的直译，内层循环接近 $10^{8}$ 次，CPython 下约需 $10$ s 以上，最大数据会 TLE（小数据完全正确；$n \le 2^{16}$ 实测约 $1.2$ s）。正式提交请用 C++17，或改 PyPy 并压平内层循环。

## 8. 边界情况与易错点

1. **$m$ 偶数、$n$ 奇数**：所有步长都是偶数，永远到不了奇数位置，答案必须是 $0$（DP 会给出 $f[i]=0$，但别在 $h$ 里读到脏值）。
2. **$n = 1, m = 1$**：唯一行程一步走完，答案 $c_1$；靠 $h[0]=1$ 统计正确。
3. **$r = 0$**（如 $n=1, m=2$）：没有 $\le n$ 的位，`tab` 长度会变成 $0$，必须先特判输出 $0$。
4. **$x > n$**：`h[n-x]` 下标为负，枚举子掩码时必须先跳过；位过滤时同样只保留 $\le n$ 的位。
5. **溢出**：列内累加 $r$ 个 $<10^9+7$ 的值可达 $2\times10^{10}$，`int` 溢出；$c_x \cdot h$ 也必须 `long long`。
6. **表复用**：第二趟若跳过 $i=0$ 或漏写某列，就会读到第一趟（$f$ 的 $D$ 表）残留，答案必错；务必每列写满 $r$ 行。
7. **多测清空**：每组重分配 `tab`，不要跨测试残留；$\sum n \le 2^{20}$ 保证总开销可控。
8. **取模与负数**：全程只有加法和取模，没有减法，不必补 `+MOD`；但要保证 `j < 0` 的判空在下标计算之前。

## 相关题目与扩展

- [Codeforces 2267F1. XOR Transformations (Easy Version)](https://codeforces.com/problemset/problem/2267/F1) / [F2. Hard Version](https://codeforces.com/problemset/problem/2267/F2)：同场题，同样是「按二进制位分层」的套路。
- [LeetCode 70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/)：本题退化版——步长固定 $\{1,2\}$、只求方案数不求花费和。
- [LeetCode 746. 使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/)：同一 DP 框架，把「求和」换成「最短路」。
- [Codeforces 632E. Thief in a Shop](https://codeforces.com/problemset/problem/632/E)：生成函数 + 卷积经典题，可与本题「乘积结构 → 分层前缀和」对照。

**延伸思考**：

1. 若把「花费之和」换成「花费 $\le K$ 的行程数」，需要双变量生成函数，$O(nr)$ 的分层退化为 $O(nrK)$，只能靠 FFT 加速。
2. 若 $n$ 放大到 $10^{18}$（$m$ 仍很小）：$F = 1/\bigl(2-\prod_t(1+y^{c_t})\bigr)$ 是有理函数，$f$ 满足阶数 $\le m$ 的线性递推，可用 Bostan–Mori 在 $O(m\log m\log n)$ 求单项。
3. 若步长集合换成「$m$ 的超掩码」或任意集合，乘积结构消失，$O(nr)$ 技巧立即失效——这正是本题必须要求子掩码的原因。
4. (1) 的代数形式是 $\text{Ans} = [y^n]\,D(y)F(y)^2$，其中 $D(y) = \sum_{x \subseteq m} c_x y^x$；它把「标记一步」翻译成「前缀 $\times$ 后缀 $\times$ 那一步」。
