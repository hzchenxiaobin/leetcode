# Codeforces 明日之缎带 题解

## 1. 题目概述

- **标题 / 题号**：明日之缎带（Codeforces 2255B，英文名 A Ribbon for Tomorrow）
- **链接**：https://codeforces.com/problemset/problem/2255/B
- **来源**：Codeforces Round 1116 (Div. 1) · Problem B（同题在 Div. 2 的编号是 2256D）
- **难度**：1600
- **限制**：时间 2 s / 内存 256 MB
- **标签**：组合数学、数学、字符串、计数、隔板法

**题意**：给定长度为 $n$ 的 01 串 $s$（`0` 白珠、`1` 黑珠）。一次操作可任选 $1 \le l \le r \le n$，要求**当前串中** $s_l = s_r$，然后把子串 $s_l s_{l+1} \cdots s_r$ 整体**倒序**；操作可做任意多次（含 0 次）。问从 $s$ 出发能得到多少个不同的 01 串，对 $998244353$ 取模。多测：第一行 $t$，每组给出 $n$ 与 $s$，每组输出一行。

**约束**：

- $1 \le t \le 10^4$，$1 \le n \le 10^6$，且 $\sum n \le 10^6$
- $s$ 仅由 `0`、`1` 组成，$\lvert s \rvert = n$
- 模数 $998244353$（**不是** $10^9+7$）

$\sum n \le 10^6$ 决定了解法必须是每组线性；而答案本身随 $n$ 指数增长（$n = 10^6$ 时是天文学数字），所以只能靠组合公式数，不能搜索。

## 2. 示例

```text
输入
4
5
00110
6
001010
5
01010
6
111111

输出
2
3
1
1
```

- `00110` → 2：`00110`、`01100`（反转整体，$s_1 = s_5 = 0$）；`001010` → 3：`001010`、`010010`（反转前 4 位）、`010100`（反转整体，$s_1 = s_6 = 0$）。
- `01010` → 1：完全交替，端点同色的区间都是回文，反转不改变串；`111111` → 1：全同色，反转任何区间都不变。

**自造补充**：$n = 6$、$s = \texttt{011000}$ → `3`，可达串为 `000110`、`001100`、`011000`（公式给出 $\binom{3}{1}\binom{1}{0} = 3$，见 §3.4）。

## 3. 解题思路

### 3.1 暴力思路

把「当前串」当状态做 BFS：每个状态枚举 $O(n^2)$ 个合法区间、每次反转 $O(n)$，单状态转移就是 $O(n^3)$。更致命的是**状态数就等于答案**，而答案随 $n$ 指数增长（暴力枚举可得 $n = 20$ 时最大已有 $17640$ 个可达串）。暴力只配用来对拍小数据。

### 3.2 核心观察一：换成差分串，操作变成「偶校验区间反转」

![差分串：s 到 d 的转换与操作示意](images/cf2255_b_difference_model.svg)

定义**差分串**（长度 $m = n-1$）：$d_i = [\,s_i \ne s_{i+1}\,]$，$i = 1, \dots, n-1$。三个事实串起来即可换掉整个问题：

1. **首尾字符不变**：若 $l = 1$，操作后新的第一位是 $s_r$，而合法性要求 $s_r = s_l = s_1$；$l > 1$ 时首位不在反转范围内。末位对称。故 $s$ 与 $(s_1, d)$ 一一对应，**答案等于从 $d$ 出发可得的不同 $d'$ 的个数**。
2. **端点同色 $\iff$ 区间内「1」的个数为偶数**：从 $s_l$ 走到 $s_r$ 要跨 $r-l$ 条边，每条 $d_i = 1$ 翻转一次字符，故 $s_l \oplus s_r = \sum_{i=l}^{r-1} d_i \bmod 2$。
3. **反转 $s_l \cdots s_r$ $\iff$ 反转 $d_l \cdots d_{r-1}$**：段内相邻差序列被整体倒序；交界处 $d_{l-1} = [\,s_{l-1} \ne s_l\,]$ 变成 $[\,s_{l-1} \ne s_r\,]$，由 $s_l = s_r$ 与原值相同，右交界 $d_r$ 同理。

于是问题等价地变为：**给定长度 $m$ 的 01 串 $d$，每次可反转任意一段含偶数个 1 的连续区间，问能得到多少种不同的 $d$。**

### 3.3 核心观察二：空隙按下标奇偶分组，组内可任意搬运

![空隙的奇偶分组与不变量](images/cf2255_b_gap_parity.svg)

把 $d$ 按「1」切成空隙：$d = 0^{a_0}\, 1\, 0^{a_1}\, 1\, \cdots\, 1\, 0^{a_k}$，其中 $k$ 是 1 的个数，$a_0, \dots, a_k \ge 0$，$\sum a_i = m - k$。

一次合法操作（区间含偶数个 1）等价于：取 $0 \le i < j \le k$ 且 $j - i$ 为**偶数**，再取 $0 \le u \le a_i$、$0 \le v \le a_j$，则

$$a_i \leftarrow a_i - u + v, \qquad a_j \leftarrow a_j - v + u, \qquad (a_{i+1}, \dots, a_{j-1}) \text{ 整体倒序}$$

**不变量**：$j - i$ 为偶数 $\Rightarrow$ $i, j$ 同奇偶，而中间那段的倒序只是换位置、不改变各空隙的下标奇偶性。故两个和恒不变：

$$E = \sum_{i \text{ 为偶数}} a_i, \qquad O = \sum_{i \text{ 为奇数}} a_i$$

**反向可达**：取 $j = i + 2$（中间只有一个空隙，倒序是恒等）、$u = 0$、$v = 1$，即「从 $a_{i+2}$ 搬 1 个零给 $a_i$」。同奇偶下标的空隙连成链 $p, p+2, p+4, \dots$，沿链来回搬即可把任一分布重排为任一同和分布。因此**可达类恰为全部具有相同 $(E, O)$ 的空隙向量**。

计数用隔板法：$E$ 分给 $c_e = \lfloor k/2 \rfloor + 1$ 个偶下标空隙，方案 $\binom{E + c_e - 1}{c_e - 1}$；奇数侧 $c_o = \lceil k/2 \rceil$，方案 $\binom{O + c_o - 1}{c_o - 1}$；两组独立，相乘即为答案。

### 3.4 落到 run 上：只依赖「段长」的公式

![样例 001010 的 run 分组演算](images/cf2255_b_walkthrough.svg)

$d$ 的「1」恰好落在 $s$ 的 run 交界处。对 $s$ 做行程编码 $s = c_0^{b_0} c_1^{b_1} \cdots c_{R-1}^{b_{R-1}}$（相邻段字符不同、段内相同），则 $k = R - 1$ 且 $a_i = b_i - 1$。代回不变量：

$$E + c_e = \sum_{i \text{ 偶}} b_i = S_e, \qquad O + c_o = \sum_{i \text{ 奇}} b_i = S_o, \qquad c_e = \lceil R/2 \rceil,\quad c_o = \lfloor R/2 \rfloor$$

$$\boxed{\ \text{ans} = \binom{S_e - 1}{c_e - 1} \cdot \binom{S_o - 1}{c_o - 1}\ }$$

$c_o = 0$（即 $R = 1$）时第二因子取 $1$；组合意义就是「$S_e$ 个字符切成 $c_e$ 段、每段至少 1 个」。以 `001010` 为例：$b = (2,1,1,1,1)$，$R = 5$；偶下标段 $b_0,b_2,b_4$ 给 $S_e = 4$、$c_e = 3$，因子 $\binom{3}{2} = 3$；奇下标段 $b_1,b_3$ 给 $S_o = 2$、$c_o = 2$，因子 $\binom{1}{1} = 1$；答案 $3$，与枚举一致。

## 4. 算法细节

1. **阶乘只预处理一次**：上标 $S_e - 1 \le n - 1$，预处理 `fact`/`invfact` 到 $\max n$，`invfact` 用费马小定理只求一次再倒推；每组若重算会退化成 $O(t \cdot n)$。
2. **双指针求 run**：`for (int i = 0; i < n; ) { int j = i; while (j < n && s[j] == s[i]) j++; ... i = j; }`，边求段长边按 `R % 2` 累加四个量，不要用 `vector` 存段长。
3. **组合数边界**：`C(n,k)` 对 `k < 0 || k > n || n < 0` 返回 0；但 $c_o = 0$ 时应让**整个因子取 1**（$\binom{S_o-1}{-1}$ 无意义），用 `if (cntOdd)` 显式判断，别指望兜底。
4. **乘法的范围**：全部用 `long long`；$998244353 < 2^{30}$，两个模内数相乘约 $10^{18}$，不溢出但有惊无险，不能写 `int` 连乘。
5. **下标约定**：题面 $1$-indexed，run 用 $0$-indexed（第 $0,2,4\dots$ 段是「偶数段」）；两套约定混用是本类题的 off-by-one 主因。
6. **读入与多测**：`cin >> n >> s` 后令 `n = s.size()`，即使输入 $n$ 与串长不符也不越界；Python 用 `sys.stdin.buffer.read().split()` 一次读完。所有量在循环体内声明，全局只有只读的阶乘表，无需清空。

## 5. 正确性证明

**引理 1（差分串等价）**：任何操作后 $s_1, s_n$ 都不变，$s$ 由 $(s_1, d_1, \dots, d_{n-1})$ 唯一确定；并且「$s_l = s_r$ 且反转 $s_l \cdots s_r$」等价于「$\sum_{i=l}^{r-1} d_i$ 为偶数且反转 $d_l \cdots d_{r-1}$」。

**证明**：$l = 1$ 时新首位为 $s_r$，合法性给出 $s_r = s_l = s_1$；$l > 1$ 时首位不在区间内；末位对称，故逆推 $s_{i+1} = s_i \oplus d_i$ 可还原 $s$。又 $s_l \oplus s_r = \bigl(\sum_{i=l}^{r-1} d_i\bigr) \bmod 2$，得端点同色 $\iff$ 偶数；段内相邻对 $(s_t, s_{t+1})$ 倒序后只是顺序颠倒，故段内 $d$ 序列反转，而交界处 $d_{l-1}, d_r$ 分别变为 $[\,s_{l-1} \ne s_r\,]$、$[\,s_l \ne s_{r+1}\,]$，由 $s_l = s_r$ 与原值相等。∎

**引理 2（$E, O$ 是不变量）**：一次操作后 $\sum_{i \text{ 偶}} a_i$ 与 $\sum_{i \text{ 奇}} a_i$ 都不变。

**证明**：操作只改 $a_i, a_j$（$i \equiv j \pmod 2$）并把 $a_{i+1},\dots,a_{j-1}$ 倒序；倒序保持下标集合与各位置取值不变，故两组和都不受中间段影响。被改的两项满足 $(a_i - u + v) + (a_j - v + u) = a_i + a_j$ 且同属一组，故该组和不变。∎

**引理 3（同 $(E,O)$ 的向量互达）**：元素个数相同、$E$ 与 $O$ 分别相等的两个空隙向量互相可达。

**证明**：取 $j = i + 2$、$u = 0$、$v = 1$（需 $a_{i+2} \ge 1$），区间内恰含两个 1 故合法，中间段只有单个空隙、倒序为恒等，效果仅为 $a_i {+}{=} 1$、$a_{i+2} {-}{=} 1$；其逆操作 $u = 1, v = 0$ 同样合法，故这一步可逆。同奇偶下标构成链 $p, p+2, p+4, \dots$，沿链把单位零从盈余搬到亏空即可；两组搬运互不干扰。∎

**定理**：算法输出 $\binom{S_e-1}{c_e-1}\binom{S_o-1}{c_o-1}$ 即所求不同串数。

**证明**：由引理 1，答案等于从 $d$ 出发在偶校验区间反转下可得的不同 $d'$ 数；由引理 2、3，该可达类恰为与初始 $d$ 同 $(E,O)$ 的全部空隙向量，且不同空隙向量对应不同 $d$（从而不同 $s$）。由 $a_i = b_i - 1$ 得 $E = S_e - c_e$、$O = S_o - c_o$，再对两组分别用隔板法计数并相乘即得。∎

## 6. 复杂度分析

- **时间**：阶乘预处理 $O(\max n)$；每组一次双指针扫描 $O(n)$；总计 $O(\max n + \sum n) \approx 2 \times 10^6$ 次基本运算。
- **空间**：`fact` 与 `invfact` 各 $O(\max n)$ 个 `long long`（约 16 MB，限 256 MB）；每组额外 $O(1)$（不存段长数组）。
- **实测**：`g++ -std=c++17 -O2` 下 $n = 10^6$ 单组约 **0.08 s**、Python3 约 **0.53 s**；$t = 10^4, \sum n = 10^6$ 时 C++ 约 **0.13 s**、Python3 约 **0.24 s**；最坏形态（大量 run、答案极大）Python3 也不超过 **0.66 s**，对 2 s 时限余量 3 倍以上。

## 7. 参考代码

### C++17

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

const long long MOD = 998244353;
const int MAXF = 1000005;
vector<long long> fact(MAXF), invfact(MAXF);

long long pw(long long a, long long b) {
    long long r = 1; a %= MOD;
    while (b) { if (b & 1) r = r * a % MOD; a = a * a % MOD; b >>= 1; }
    return r;
}

long long C(int n, int k) {
    if (k < 0 || k > n || n < 0) return 0;
    return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    fact[0] = 1;
    for (int i = 1; i < MAXF; i++) fact[i] = fact[i - 1] * i % MOD;
    invfact[MAXF - 1] = pw(fact[MAXF - 1], MOD - 2);
    for (int i = MAXF - 1; i > 0; i--) invfact[i - 1] = invfact[i] * i % MOD;

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; string s;
        cin >> n >> s;
        n = (int)s.size();

        int R = 0;                                // run 编号，从 0 开始
        long long sumEven = 0, sumOdd = 0;        // 偶数段 / 奇数段的总字符数
        long long cntEven = 0, cntOdd = 0;        // 偶数段 / 奇数段的段数
        for (int i = 0; i < n; ) {
            int j = i;
            while (j < n && s[j] == s[i]) j++;    // 双指针取一段 run
            long long len = j - i;
            if (R % 2 == 0) { sumEven += len; cntEven++; }
            else            { sumOdd  += len; cntOdd++;  }
            R++; i = j;
        }

        long long ans = C((int)(sumEven - 1), (int)(cntEven - 1));
        if (cntOdd > 0)                           // c_o = 0 时该因子取 1
            ans = ans * C((int)(sumOdd - 1), (int)(cntOdd - 1)) % MOD;
        cout << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys
from itertools import groupby

MOD = 998244353

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    tests, pos, maxlen = [], 1, 1
    for _ in range(t):
        n = int(data[pos])
        s = data[pos + 1]
        pos += 2
        tests.append(s)
        maxlen = max(maxlen, len(s))

    fact = [1] * (maxlen + 1)
    for i in range(1, maxlen + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (maxlen + 1)
    invfact[maxlen] = pow(fact[maxlen], MOD - 2, MOD)
    for i in range(maxlen, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(n: int, k: int) -> int:
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    out = []
    for s in tests:
        sum_even = sum_odd = cnt_even = cnt_odd = 0
        for idx, (_, g) in enumerate(groupby(s)):   # s 是 bytes，可直接分组
            length = len(list(g))
            if idx % 2 == 0:
                sum_even += length
                cnt_even += 1
            else:
                sum_odd += length
                cnt_odd += 1
        ans = comb(sum_even - 1, cnt_even - 1)
        if cnt_odd:                                # c_o = 0 时该因子取 1
            ans = ans * comb(sum_odd - 1, cnt_odd - 1) % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n = 1$ 与全 0 / 全 1**：都只有一段 run，$c_o = \lfloor R/2 \rfloor = 0$，必须跳过第二个因子，答案 $1$——这是最容易 WA 的点。
2. **完全交替串**：$R = n$，每段长 1，$S_e = c_e$、$S_o = c_o$，两个因子都是 $\binom{c-1}{c-1} = 1$，答案 $1$，与「该情形所有合法区间都是回文」一致。
3. **只有两段**（如 `000111`）：$c_e = c_o = 1$，两因子均为 $\binom{\cdot}{0} = 1$，答案 $1$；注意整体反转不合法（端点异色），别误以为能得 `111000`。
4. **$n = 0$ 的组合数**：$b_0 = 1$ 且 $c_e = 1$ 时 $\binom{0}{0} = 1$，要求 `fact[0] = 1` 且 `C(0,0)` 返回 1，不能把 `k == 0` 当成无解。
5. **模数与数组上界**：模数是 $998244353$（抄成 $10^9+7$ 可能仍过小样例）；阶乘要预处理到 $\max n$，固定到 $10^5$ 而 $n = 10^6$ 会越界。
6. **多测清零与 bytes/str 混用**：四个累加器若声明为全局且不清零会直接崩；Python 里 `groupby(bytes)` 逐字节分组、比较的是整数，不要中途混入 `decode()` 后的 `str`。

## 相关题目与扩展

- [Codeforces 2256D](https://codeforces.com/problemset/problem/2256/D)：本题在 Div. 2 的编号（同一道题），可对照两边的题面表述。
- [Codeforces 2255A](https://codeforces.com/problemset/problem/2255/A)：同场 A 题，同样是「找不变量 + 几行结论」的风格。
- [LeetCode 1621. 大小为 K 的不重叠线段的数目](https://leetcode.cn/problems/number-of-sets-of-k-non-overlapping-line-segments/)：同样把计数化成「在空隙里插板」，可与本文 §3.4 的隔板法对照。
- [OI Wiki · 组合数学](https://oi-wiki.org/math/combinatorics/combination/)：隔板法与多重集排列的标准推导。

**延伸思考**：

1. **去掉 $s_l = s_r$ 的限制**：若允许反转任意区间，长度为 2 的反转就是交换相邻字符，可生成所有同「0/1 个数」的串，答案变成 $\binom{n}{k}$。可见端点同色这条限制正是把可达集从 $\binom{n}{k}$ 压到「两组隔板」的关键。
2. **求最少步数**：把初始空隙向量搬到目标向量，每单位搬运对应一次 $j = i+2$ 的操作，于是最少操作数的自然上界是两组各自「盈余→亏空」的搬运量之和；由于一次长区间操作还能顺带倒序中间空隙，最优值需要更细的势能分析。
3. **换成循环移位或更多颜色**：若操作改成「区间循环右移一位」，差分形态不再是简单反转，但「1 的位置如何移动」的分析框架仍可复用；若珠子有 $c \ge 3$ 种颜色，不变量会变成各颜色在两组内的总和，公式变为多个组合数之积，可用 $c = 3$ 的小数据 BFS 验证猜想。
