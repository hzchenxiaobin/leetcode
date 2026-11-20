# Codeforces 2283C 大异或 题解

## 1. 题目概述

- **标题 / 题号**：大异或（Codeforces 2283C，英文名 Big XOR）
- **链接**：https://codeforces.com/problemset/problem/2283/C
- **来源**：Educational Codeforces Round 196 (Rated for Div. 2) · Problem C（UTC 2026-11-04）
- **难度**：未评级（Div. 2 的 C 题，暂无公开 rating）
- **限制**：时间 2 s / 内存 512 MB
- **标签**：位运算、构造、异或、数学

**题意**：给定 $n$，初始数组 $a=[1,2,\dots,n]$。任选一个下标集合 $S$，把 $S$ 中每个元素乘 $2$（每个位置至多一次，$S$ 可空、也可取满），得到数组 $b$。记

$$k = a_1 \mid a_2 \mid \cdots \mid a_n,\qquad m = b_1 \oplus b_2 \oplus \cdots \oplus b_n .$$

要求构造 $S$ 使得 $m \ge 2k$，输出 $n$ 个 $0/1$：第 $i$ 位为 $1$ 表示翻倍 $a_i$。题目保证对一切合法 $n$ 都有解，不要求最小化 $|S|$，多解输出任意一组。多测。

**约束**：

- $1 \le t \le 10^4$，$1 \le n \le 2\times10^5$，且 $\sum n \le 2\times 10^5$
- $b_i \le 2n \le 4\times10^5 < 2^{19}$，所以 $m < 2^{19}$，值域很小；但掩码运算建议统一用 `long long`
- 输出总量是 $\sum n$ 个数，必须缓冲输出，不能逐组刷新

## 2. 示例与观察
官方样例（输入 / 输出原样）：

```text
输入：
5
3
6
9
5
11

输出：
1 0 1
0 1 1 0 0 1
0 1 1 1 0 1 0 0 1
0 1 1 1 0
0 0 1 0 1 1 0 1 1 0 1
```

> 💡 **本题是多解构造，样例输出只是其中一种解**。$n=3$ 官方给 `1 0 1`（$b=[2,2,6]$，$m=6$），本文代码给 `0 1 0`（只翻倍 $2$：$b=[1,4,3]$，$m=1\oplus4\oplus3=6=2k$），两者都合法。校验器是 special judge，**不要按样例输出逐字节对齐**。

## 3. 解题思路

### 3.1 暴力思路

枚举 $2^n$ 个集合 $S$，每个集合花 $O(n)$ 求 $m$，总复杂度 $O(n2^n)$；$n\le 2\times 10^5$ 时完全不可行（连 $n=30$ 都过不去）。

把「翻倍第 $i$ 项」看成一个开关也有一定启发：它给整体异或带来净改变 $\delta_i = i\oplus 2i$，于是 $m = X\oplus\bigoplus_{i\in S}\delta_i$，其中 $X=\bigoplus_{i=1}^n i$。可惜 $\delta_i$ 的位形是 $i$ 的「相邻位差分」，翻倍一个数会同时翻转多个位，逐元素贪心没有任何局部依据——这也是本题被标成 constructive 的原因。

### 3.2 核心观察：n 个开关其实只有一个自由度 Y

![关键压缩：m = X ⊕ Y ⊕ 2Y](../../../images/cf2283c_xor_compression.svg)

设 $X = 1\oplus 2\oplus\cdots\oplus n$，$S$ 为翻倍的下标集合。因为 $a_i=i$ 要么保留、要么变成 $2i$，所以

$$m = X \oplus \bigoplus_{i\in S}\bigl(i\oplus 2i\bigr) = X \oplus \biggl(\bigoplus_{i\in S} i\biggr)\oplus \biggl(\bigoplus_{i\in S} 2i\biggr).$$

异或满足交换律与结合律，而左移与异或可交换（$\bigoplus_{i\in S}2i = \bigl(\bigoplus_{i\in S}i\bigr)\ll 1$）。记 $Y=\bigoplus_{i\in S}i$，立刻得到**唯一的压缩恒等式**

$$m = X \oplus Y \oplus (Y\ll 1).$$

于是「$2^n$ 种选择」塌缩成「挑一个整数 $Y$」：**只有被翻倍下标的异或影响 $m$**，具体是哪些下标、翻倍几个，全都不重要。$Y$ 的可达范围恰好是整个 $[0,2^B)$（$B$ 为 $n$ 的二进制位数，$2^{B-1}\le n<2^B$）：因为 $1,2,4,\dots,2^{B-1}$ 全在数组里，按 $Y$ 的二进制位挑这些元素，它们的下标异或正等于 $Y$。

再看目标。$k = 1\mid 2\mid\cdots\mid n = 2^B-1$（$n\ge 2^{B-1}$ 保证 $0..B-1$ 位都被覆盖），所以 $2k = 2^{B+1}-2$；又每项 $b_i\le 2n<2^{B+1}$，故 $m<2^{B+1}$。**于是 $m\ge 2k$ 只剩两种可能**

$$m = 2^{B+1}-2 \quad\text{或}\quad m = 2^{B+1}-1,$$

等价于「$m$ 的第 $1..B$ 位全是 $1$」，第 $0$ 位随便。

### 3.3 算法流程：位梯子逐位钉死 y_b

![位梯子：逐位定 y，再用取反修正](../../../images/cf2283c_bit_ladder.svg)

记 $x_b,y_b,m_b$ 分别是 $X,Y,m$ 的第 $b$ 位。由 $m=X\oplus Y\oplus(Y\ll1)$ 拆位得

$$m_b = x_b \oplus y_b \oplus y_{b-1}\qquad (y_{-1}=0).$$

要求 $m_b=1$（$1\le b\le B$）就逼出一条**从低位到高位的递推（位梯子）**：

$$y_b = 1 \oplus x_b \oplus y_{b-1},\qquad b=1,2,\dots,B.$$

关键的三点是：

1. **$y_0$ 完全自由**，因为 $m_0$ 不受约束（$m_0 = x_0\oplus y_0$，取到什么都合法）。
2. **$Y<2^B$ 强制 $y_B=0$**。而梯子在第 $B$ 层给出 $y_B = 1\oplus x_B\oplus y_{B-1} = 1\oplus y_{B-1}$（$x_B=0$），所以 $y_B=0 \iff y_{B-1}=1 \iff m_B=1$，两个条件自动吻合。
3. **$y_0$ 取反 = 所有 $y_b$ 一起取反**（归纳：$y_{b-1}$ 翻转则 $y_b=1\oplus x_b\oplus y_{b-1}$ 也翻转）。所以两种 $y_0$ 恰好一种让 $y_B=0$；并且取反不改变 $y_b\oplus y_{b-1}$，$b<B$ 的等式全部保持。

于是算法只有三步：先令 $y_0=0$ 一路推到 $y_B$；若 $y_B=1$ 就把 $y_0..y_B$ 整体取反（再丢掉第 $B$ 位），让 $y_B$ 归零；最后令 $Y=\sum_{b<B}y_b2^b$，输出「对每个 $y_b=1$ 翻倍元素 $2^b$」。

### 3.4 示例演算

![n = 11 的走查表](../../../images/cf2283c_walkthrough_n11.svg)

以 $n=11$ 为例：$B=4$，$k=15$，$2k=30$，而 $n\bmod 4=3$ 给出 $X=0$。

| 位 $b$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $x_b$ | 0 | 0 | 0 | 0 | 0 |
| $y_b$ | 0 | 1 | 0 | 1 | 0 |
| $m_b$ | 随意 | 1 | 1 | 1 | 1 |

梯子逐步：$y_1=1\oplus0\oplus0=1$，$y_2=1\oplus0\oplus1=0$，$y_3=1\oplus0\oplus0=1$，$y_4=1\oplus0\oplus1=0$。末位已是 $0$，无需取反，$Y=(1010)_2=10$：翻倍 $2^1=2$ 与 $2^3=8$，得 $b=[1,4,3,4,5,6,7,16,9,10,11]$，$m=0\oplus10\oplus20=30=2k$ ✓。

再核两组：$n=6$（$B=3$，$X=7$）推出 $y_3=1$ → 取反得 $y=(1,1,1)$、$Y=7$，翻倍 $1,2,4$ 得 $m=7\oplus7\oplus14=14=2k$ ✓；$n=9$（$B=4$，$X=1$）推出 $y=(0,1,0,1,0)$、$Y=10$，翻倍 $2,8$ 得 $m=1\oplus10\oplus20=31\ge30$ ✓。

## 4. 算法细节

1. **求 $B$**：$B=\lfloor\log_2 n\rfloor+1$，代码 `while ((1LL << B) <= n) ++B`；注意 $n=1$ 时 $B=1$，别用会返回 $0$ 的写法。
2. **求 $X$**：$\bigoplus_{i=1}^{n}i$ 有周期闭式——$n\bmod 4 = 0,1,2,3$ 时分别为 $n,1,n+1,0$，$O(1)$ 搞定，不必循环 $n$ 项。
3. **递推方向**：必须从 $b=1$ 推到 $b=B$（$y_b$ 依赖 $y_{b-1}$），用变量 `prev` 存上一位，边推边把为 $1$ 的位写进 `Y`。
4. **$y_B$ 修正**：若推出 $y_B=1$，用掩码 `(1LL << (B + 1)) - 1` 把 $0..B$ 位整体取反，再 `& ((1LL << B) - 1)` 丢掉第 $B$ 位。少翻第 $0$ 位会破坏 $b=1$ 的等式，多翻一位会破坏 $y_B=0$。
5. **下标映射**：$y_b$ 对应元素值 $2^b$，它在数组里的**位置是下标 $2^b$**，所以写 `d[1 << b] = 1` 而不是 `d[b] = 1`。这是本题最容易错的一步：写成 `d[b]` 时 $n=3$ 会输出 `1 0 0`，$m=3<6$。
6. **输出**：$\sum n\le 2\times10^5$ 个数，用 `string` 拼好一次性写出（或用 `'\n'` 而不用 `endl`），避免每组刷新缓冲区。
7. **多测**：`Y`、`prev`、`B`、`X` 每组重算，无全局数组，天然没有跨测污染。

## 5. 正确性证明

**引理 1（$k$ 与 $m$ 的上界）**：$k=2^B-1$，$2k=2^{B+1}-2$，且 $m<2^{B+1}$。

**证明**：由 $2^{B-1}\le n<2^B$，对每个 $0\le b<B$ 有 $2^b\le 2^{B-1}\le n$，即 $2^b$ 是数组元素，故 $k$ 的第 $b$ 位为 $1$，$k\ge 2^B-1$；又所有元素 $<2^B$，没有更高的位，故 $k=2^B-1$。每项 $b_i\le 2n\le 2^{B+1}-2<2^{B+1}$，异或结果的每一位都来自这些数，故 $m<2^{B+1}$。∎

**引理 2（压缩恒等式）**：设 $Y=\bigoplus_{i\in S}i$，则 $m=X\oplus Y\oplus(Y\ll1)$。

**证明**：$b_i$ 等于 $i$（$i\notin S$）或 $2i$（$i\in S$），故 $m=\bigoplus_{i=1}^{n}i\oplus\bigoplus_{i\in S}(i\oplus 2i)=X\oplus\bigl(\bigoplus_{i\in S}i\bigr)\oplus\bigl(\bigoplus_{i\in S}2i\bigr)$。异或满足交换律、结合律，且 $2i=i\ll1$ 与异或可交换，故 $\bigoplus_{i\in S}2i=Y\ll1$，代入即得结论。∎

**引理 3（$Y$ 的可达性）**：任意 $Y\in[0,2^B)$ 都能被某个 $S\subseteq[1,n]$ 实现，且可取 $S\subseteq\{1,2,4,\dots,2^{B-1}\}$。

**证明**：把 $Y$ 写成二进制 $Y=\sum_{b=0}^{B-1}y_b2^b$，取 $S=\{2^b:y_b=1\}$。由 $2^b\le 2^{B-1}\le n$ 知 $S\subseteq[1,n]$；$S$ 中元素是互不相同的 $2$ 的幂，异或就是各幂之和，等于 $Y$。∎

**引理 4（位梯子充分）**：若 $y_0,\dots,y_B$ 满足 $y_b=1\oplus x_b\oplus y_{b-1}$（$1\le b\le B$）且 $y_B=0$，则 $m_b=1$ 对一切 $b=1..B$ 成立，从而 $m\ge 2k$。

**证明**：递推式本身就是 $m_b=x_b\oplus y_b\oplus y_{b-1}$ 的移项，故每个 $m_b=1$。最后一层 $b=B$ 需要单独看：$x_B=0$，递推式化为 $y_B=1\oplus y_{B-1}$，于是 $y_B=0\iff y_{B-1}=1$，此时 $m_B=x_B\oplus y_B\oplus y_{B-1}=0\oplus0\oplus1=1$，同样成立。于是 $m$ 的 $1..B$ 位全为 $1$，$m\ge2^{B+1}-2=2k$（引理 1）。∎

**引理 5（取反修正命中唯一合法序列）**：设 $y^{(0)}$ 是从 $y_0=0$ 推出的序列，$y^{(1)}$ 为它逐位取反。则恰有一个满足 $y_B=0$，且算法输出的那个满足引理 4 的全部条件。

**证明**：取反使每个 $y_b$ 翻转（对 $b$ 归纳），故 $y_B^{(1)}=1-y_B^{(0)}$，二进制下恰有一个为 $0$。取反不改变 $y_b\oplus y_{b-1}$，所以 $1\le b<B$ 的等式对两者都成立；修正后 $y_B=0$ 的那个由引理 4 也满足 $b=B$ 的等式。算法正是保留它，故输出的序列满足引理 4。∎

**定理**：程序输出的 $d_1..d_n$ 对应的数组 $b$ 满足 $m\ge2k$。

**证明**：由引理 5，程序得到的 $y$ 序列满足引理 4，令 $Y=\sum_{b<B}y_b2^b$（第 $B$ 位为 $0$，故 $Y<2^B$）。由引理 3，$S=\{2^b:y_b=1\}\subseteq[1,n]$ 实现了这个 $Y$，而程序输出的正是 $S$ 的指示向量；于是引理 2 给出 $m=X\oplus Y\oplus(Y\ll1)$，引理 4 给出 $m\ge2k$。∎

## 6. 复杂度分析

- **时间**：每组 $O(n+\log n)$——梯子 $O(B)=O(\log n)$，$X$ 用闭式 $O(1)$，输出 $O(n)$。全场合计 $O(\sum n+t\log n)$，最坏约 $2\times10^5+1.8\times10^5$ 次基本运算。
- **空间**：算法本身 $O(1)$（几个整数）；输出缓冲 $O(n)$，也可以逐个数输出做到 $O(1)$ 额外空间。
- **可行性**：实测 C++（`-O2`，含进程启动）在 $n=2\times10^5$ 单组上约 $6$ ms，在 $t=10^4$、$\sum n=2\times10^5$ 上约 $15$ ms；Python3 同样两组约 $38$ ms 与 $58$ ms。对 2 s 时限有百倍余量，瓶颈只是 I/O。

## 7. 参考代码

### C++17

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    string out;
    out.reserve(4000000);
    while (t--) {
        int n;
        cin >> n;

        int B = 0;                                    // B = n 的二进制位数
        while ((1LL << B) <= n) ++B;
        long long X = (n % 4 == 0) ? (long long)n
                    : (n % 4 == 1) ? 1LL
                    : (n % 4 == 2) ? (long long)n + 1
                                   : 0LL;         // X = 1 ^ 2 ^ ... ^ n
        long long Y = 0, prev = 0;                    // Y = 被翻倍下标的异或
        for (int b = 1; b <= B; ++b) {                // 位梯子，y_0 = 0
            int cur = 1 ^ (int)((X >> b) & 1) ^ (int)prev;
            if (cur) Y |= (1LL << b);
            prev = cur;
        }
        if (prev) Y ^= (1LL << (B + 1)) - 1;          // y_B 必须为 0 -> 整体取反
        Y &= (1LL << B) - 1;                          // 丢掉第 B 位

        vector<char> d(n + 1, '0');
        for (int b = 0; b < B; ++b)
            if ((Y >> b) & 1) d[1 << b] = '1';        // 翻倍元素 2^b（下标也是 2^b）
        for (int i = 1; i <= n; ++i) {
            out += d[i];
            out += (i == n) ? '\n' : ' ';
        }
    }
    cout << out;
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    pos = 1
    res = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        B = n.bit_length()                       # 二进制位数
        X = (n, 1, n + 1, 0)[n % 4]              # X = 1 ^ 2 ^ ... ^ n
        Y = 0
        prev = 0                                 # 第 0 位先取 0
        for b in range(1, B + 1):                # 位梯子
            cur = 1 ^ ((X >> b) & 1) ^ prev
            if cur:
                Y |= 1 << b
            prev = cur
        if prev:                                 # y_B 必须为 0 -> 整体取反
            Y ^= (1 << (B + 1)) - 1
        Y &= (1 << B) - 1
        row = ['0'] * n
        for b in range(B):
            if (Y >> b) & 1:
                row[(1 << b) - 1] = '1'          # 翻倍元素 2^b
        res.append(' '.join(row))
    sys.stdout.write('\n'.join(res) + '\n')


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：$B=1$，$X=1$；梯子给 $y_1=1\oplus0\oplus0=1$，取反后 $y_0=1,y_1=0$，$Y=1$，翻倍元素 $1$，$m=2=2k$ ✓。若把 $B$ 算成 $0$（例如误用 `__builtin_clz(0)`）会输出 `0`，$m=1<2$。
2. **下标 vs 元素值**：$y_b$ 对应元素 $2^b$，位置是下标 $2^b$。写成 `d[b]=1` 时 $n=3$ 输出 `1 0 0`（$m=3$），是本构造最典型的 WA。
3. **取反掩码的位数**：要翻的是 $y_0..y_B$ 共 $B+1$ 位，掩码 $2^{B+1}-1$；漏掉 $y_0$ 会破坏 $b=1$ 的等式，多翻一位则破坏 $y_B=0$，之后 `Y &= (1<<B)-1` 已来不及补救。
4. **第 $0$ 位无要求**：$m\ge2k$ 只约束第 $1..B$ 位。硬凑「$m$ 全 1（含 bit 0）」会让梯子无解；反过来，本构造下 $m$ 的奇偶性被 $n$ 唯一钉死（见延伸思考）。
5. **移位宽度**：$B\le18$，$2^{B+1}\le2^{19}$ 用 `int` 其实不溢出，但统一写 `1LL << B` 更稳妥，避免日后扩大值域踩坑。
6. **输出格式与多解**：每组恰好 $n$ 个 $0/1$、空格分隔（行末不要多余空格），$\sum n\le2\times10^5$ 时不要用 `endl`；并且任何合法解都可通过，输出不必与样例相同。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：0 / 1 通过 token 比对；本题输出不唯一（构造 / 多解 / 特殊评测），剩余差异属预期，样例含义已在第 2 节逐组解释。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [Codeforces 1847C Vampiric Powers, anyone?](https://codeforces.com/problemset/problem/1847/C) 与 [Codeforces 1554C Mikasa](https://codeforces.com/problemset/problem/1554/C)：前者反复把「当前后缀异或」追加进数组求最大值，后者要求 $\operatorname{mex}\{n\oplus0,\dots,n\oplus m\}$，都是「异或的可加结构 + 逐位分析」的同款套路。
- [LeetCode 1486. 数组异或操作](https://leetcode.cn/problems/xor-operation-in-an-array/)：$\bigoplus_{i=1}^{n}i$ 的周期闭式，正是本文 $X$ 的 $O(1)$ 求法。
- [LeetCode 1738. 找出第 K 大的异或坐标值](https://leetcode.cn/problems/find-kth-largest-xor-coordinate-value/)：二维前缀异或 + 第 $k$ 大，练「异或的线性结构」。

**延伸思考**：

1. **最少翻倍几次**：本文构造只用 $\operatorname{popcount}(Y)$ 个元素（都是 $2$ 的幂）。但引理 2 说明 $m$ 只依赖 $Y$，任何异或等于 $Y$ 的集合都可行——若 $Y\le n$，直接翻倍单个元素 $Y$ 就够（如 $n=11$ 时 $Y=10\le11$，$|S|=1$）；一般情形下答案变成「用 $[1,n]$ 中互不相同的数异或出 $Y$ 的最少个数」。
2. **能否恰好取到 $m=2k$**：$m_0=x_0\oplus y_0$，而 $y_0$ 被 $y_B=0$ 唯一确定，所以每个 $n$ 只能取到 $2k$ 与 $2k+1$ 中的一个，奇偶性由 $n$ 决定。
3. **换成「任意位操作」**：若允许把 $a_i$ 换成 $a_i\oplus c_i$（$c_i$ 给定），则 $m=X\oplus\bigoplus_{i\in S}c_i$，问题变成子集异或方程，可用线性基 / 高斯消元在 $O(n\log A)$ 内判定与构造。
4. **字典序最小的解**：固定 $Y$ 后，把所有满足异或为 $Y$ 的集合按指示向量字典序排序，可贪心地从大到小把 $Y$ 拆成互不相同的元素。
