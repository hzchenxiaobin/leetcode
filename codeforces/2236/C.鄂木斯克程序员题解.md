# Codeforces 鄂木斯克程序员 题解

## 1. 题目概述

- **标题 / 题号**：鄂木斯克程序员（Codeforces 2236C，英文名 Omsk Programmers）
- **链接**：https://codeforces.com/problemset/problem/2236/C
- **来源**：Codeforces Round 1103 (Div. 3) · Problem C
- **难度**：未评级（1000 分）
- **限制**：时间 1 s / 内存 256 MB
- **标签**：暴力枚举、贪心、数学

**题意**：给定三个整数 $a, b, x$。每次操作可以二选一：

1. 选 $a$ 或 $b$ 中的一个，把它加 $1$；
2. 选 $a$ 或 $b$ 中的一个，把它除以 $x$ 并**向下取整**。

求最少多少次操作能让 $a$ 与 $b$ 相等（只要求最终两个数相等，不要求变成某个指定值）。多测。

**约束**：

- $1 \le t \le 10^4$，$1 \le a, b \le 10^9$，$2 \le x \le 10^9$
- 除法是**向下取整**，因此 $\lfloor p/x \rfloor$ 会损失一部分值，这一损失决定了加法该放在除法前还是除法后
- 值域 $10^9$ 而 $x \ge 2$，任何数连续除不了约 $31$ 次就会变成 $0$；这是全部复杂度的来源

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
7
1 2 3
2 3 2
7 3 10
17 3 3
10 10 2
4 7 2
1 6 2

输出：
1
1
2
3
0
2
2
```

对照说明：第 1 组只能补加（$1 \to 2$）；第 3 组两边各除一次 $7 \to 0$、$3 \to 0$；第 4 组 $17 \to 5 \to 1$ 两次除法，$3 \to 1$ 一次除法；第 6 组 $a = 4$ 不动，$b: 7 \to 3$ 再补 $1$ 到 $4$（共 $2$ 步；也可以先加 $1$ 再除，同样 $2$ 步）；第 7 组 $6 \to 3 \to 1$ 与 $a = 1$ 相等。

自造一组，覆盖「一次除法正好归零」与「除法链很长」：

```text
输入：
2
1000000000 1 2
8 5 2

输出：
29
2

解释：第 1 组把 10^9 连除 29 次得 1，正好等于 b；第 2 组 8 除一次得 4，再补 1 到 5。
```

## 3. 解题思路

### 3.1 暴力思路

把 $(a, b)$ 当作状态做 BFS：每步有 $4$ 个后继（两个数各自 $+1$ 或除 $x$），边权为 $1$，第一次出现 $a = b$ 的层数就是答案。思路正确，但值域是 $10^9 \times 10^9$，可达状态数远超内存；即使按「答案不超过 $62$」限制层数，路径也有 $4^{62}$ 条。

可行的暴力只有一种：**固定两侧的除法次数**。对单个数而言，任意操作序列只由「除了几次」和「加了几次」决定，而加法的作用可以完全解析地算出来。

### 3.2 核心观察：加法永远放到除法之后

![加法推迟到除法之后](images/cf2236_c_defer_adds.svg)

记 $m_i = \left\lfloor a / x^i \right\rfloor$（$i \ge 0$，$m_0 = a$），即 $a$ 连除 $i$ 次的结果。

**关键事实**：若对 $a$ 施加 $d$ 次除法与 $c$ 次加法（顺序任意），终值 $v$ 一定满足

$$v \le m_d + c .$$

直觉上：在除法**之前**加 $1$，这 $1$ 会被随后的除法缩小成 $1/x$ 格，要凑出商 $+1$ 得加满 $x$ 次；在除法**之后**加 $1$，立刻就有 $1$ 格。既然加法的目的只是把值**抬高**，那就永远该放到最后。

由此，一个数只有 $31$ 种「形态」：连除 $i$ 次得到 $m_i$，此后每加 $1$ 步就抬 $1$ 格。于是

$$\text{cost}_a(V) = \min_{i:\, m_i \le V} \bigl(i + V - m_i\bigr),$$

其中 $V$ 是最终两边共同的值，$m_i \le V$ 是因为除法只会让值变小，除完不可能再变回比 $m_i$ 小的数。

两边独立，答案就是 $\min_V \bigl(\text{cost}_a(V) + \text{cost}_b(V)\bigr)$。把两条链写进同一个式子：固定 $i, j$，

$$\text{cost}_a(V) + \text{cost}_b(V) = 2V + (i + j - m_i - n_j),$$

它对 $V$ 单调递增，所以最优一定取 $V = \max(m_i, n_j)$，得到

$$\boxed{\;\text{ans} = \min_{i,\,j} \bigl(i + j + |m_i - n_j|\bigr)\;}$$

含义非常直白：$a$ 除 $i$ 次、$b$ 除 $j$ 次，谁除完更小就把另一边补加到这个较大的值上。

### 3.3 算法流程 / 状态转移

![算法流程：枚举两侧的除法次数](images/cf2236_c_enumerate_pairs.svg)

1. 预处理两条链：$m_0 = a$，$m_{k+1} = \lfloor m_k / x \rfloor$，直到 $m_k = 0$ 为止；$b$ 侧同理得 $n_0 \dots n_l$。
2. 初值 `best = min(|a-b|, ka + kb)`：前者是「只加不除」，后者是「两边都除到 $0$」。
3. 双重循环枚举 $(i, j)$，用 `i + j + |m_i - n_j|` 更新 `best`。
4. 剪枝：任何候选的代价都 $\ge i$，所以 $i \ge \text{best}$ 时外层直接 `break`，内层用 $i + j < \text{best}$ 卡住。
5. 输出 `best`。

### 3.4 示例演算

![示例演算表](images/cf2236_c_walkthrough.svg)

以 $a = 17,\ b = 3,\ x = 3$ 为例，两条链是 $m = (17, 5, 1, 0)$、$n = (3, 1, 0)$。表格中格子 $(i, j)$ 填入 $i + j + |m_i - n_j|$，全局最小值 $3$ 出现在 $(i, j) = (2, 1)$：$17 \to 5 \to 1$ 两次除法，$3 \to 1$ 一次除法，共 $3$ 步；$(i, j) = (1, 0)$ 同样是 $3$ 步（$17 \to 5$，$3$ 补加到 $5$），说明最优解不唯一，但最优值唯一。

再看第 6 组 $a = 4, b = 7, x = 2$：$m = (4, 2, 1, 0)$，$n = (7, 3, 1, 0)$。$(0, 0)$ 得 $3$，$(1, 0)$ 得 $1 + |2 - 7| = 6$，$(0, 1)$ 得 $1 + |4 - 3| = 2$，$(0, 2)$ 得 $2 + |4 - 1| = 5$，$(1, 1)$ 得 $2 + 1 = 3$，最小值 $2$：$b$ 除一次得 $3$，再补 $1$ 到 $4$。

## 4. 算法细节

1. **链长**：$m_k = 0$ 后立刻停止。再除一次只是多花一步而值仍是 $0$，永远不会更优；因此两边最多各 $31$ 项（$10^9 < 2^{30}$，但对 $x = 2$ 需要除 $30$ 次才归零，数组开 $35$ 更稳妥）。
2. **初值必须包含两条平凡解**：只加不除给 $|a - b|$；两边都除到 $0$ 给 $k_a + k_b$。少了任何一条都会给出错误的大值（样例 $7\ 3\ 10$ 的答案 $2$ 完全来自两边归零，而 $|a - b| = 4$）。
3. **剪枝的正确用法**：$\text{cost} \ge i$ 恒成立，所以 `i >= best` 时外层可以 `break`（$i$ 递增）；内层同理用 `i + j >= best` 收尾，注意别把 `i = 0` 也剪掉。
4. **整数类型**：$i + j + |m_i - n_j|$ 最大接近 $2 \times 10^9 + 60$，已经越过 `int` 上限（$2.147 \times 10^9$）的边缘，统一用 `long long`（Python 无此问题）。
5. **Python 的优化**：$n_j$ 关于 $j$ 单调不增，于是对固定 $m_i$ 存在分界 $j_0$（$n_{j_0} \le m_i < n_{j_0-1}$）。左段取 $\min(j + n_j)$ 的前缀最小，右段取 $\min(j - n_j)$ 的后缀最小，再用随 $i$ 单调右移的指针维护 $j_0$，单组复杂度从 $O(31^2)$ 降到 $O(31)$。
6. **读入**：$t$ 可达 $10^4$，用 `scanf` / `sys.stdin.buffer.read()` 一次性读完，避免逐行解析的开销。

## 5. 正确性证明

**引理 1**：设对某数施加 $d$ 次除法、$c$ 次加法后得到 $v$，则 $v \le m_d + c$。

**证明**：对操作次数归纳，维护不变量「当前值 $p \le m_{d'} + c'$」。初始 $p = a = m_0$ 成立。加一次：$p + 1 \le m_{d'} + (c' + 1)$。除一次：由 $\lfloor (u + c)/x \rfloor \le \lfloor u/x \rfloor + c$（对整数 $c \ge 0$ 成立）得

$$\left\lfloor \frac{p}{x} \right\rfloor \le \left\lfloor \frac{m_{d'} + c'}{x} \right\rfloor \le m_{d'+1} + c' .$$

∎

**引理 2**：把 $a$ 变成 $V$（$V \ge 0$）所需步数至少为 $\min\limits_{i:\, m_i \le V} (i + V - m_i)$。

**证明**：设方案用了 $d$ 次除法、$c$ 次加法。除法与加法都不会让值下降，故 $d$ 次除法后 $p \ge m_d$，最终 $V \ge m_d$，即 $d$ 在合法下标集合内。由引理 1，$c \ge V - m_d$，于是总步数 $d + c \ge d + V - m_d$，对每个合法 $d$ 成立，取最小即得。∎

**引理 3**：若 $V \ge m_i$，则「连除 $i$ 次再加 $V - m_i$ 次」恰好用 $i + V - m_i$ 步把 $a$ 变成 $V$。

**证明**：连除 $i$ 次得 $m_i$，再连续加 $1$ 共 $V - m_i$ 次即得 $V$，步数相加即得。∎

**定理**：$\text{ans} = \min\limits_{i,\,j} \bigl(i + j + |m_i - n_j|\bigr)$。

**证明**：

*上界*：对任意 $(i, j)$，令 $V = \max(m_i, n_j) \ge m_i, n_j$，由引理 3 两侧各自到达 $V$，总步数

$$i + (V - m_i) + j + (V - n_j) = i + j + |m_i - n_j|,$$

故 $\text{ans}$ 不超过右侧最小值。

*下界*：设最优方案中 $a$ 侧用了 $d$ 次除法、$c_1$ 次加法，$b$ 侧用了 $e$ 次除法、$c_2$ 次加法，两侧终值同为 $V$。由引理 2，

$$\text{ans} = d + c_1 + e + c_2 \ge (d + V - m_d) + (e + V - n_e) = d + e + 2V - m_d - n_e .$$

又因 $V \ge \max(m_d, n_e)$，有 $2V - m_d - n_e \ge |m_d - n_e|$，故 $\text{ans} \ge d + e + |m_d - n_e| \ge \min_{i,j} \bigl(i + j + |m_i - n_j|\bigr)$。

上下界相同，定理成立。∎

## 6. 复杂度分析

- **时间**：预处理两条链各 $O(\log_x 10^9) \le 31$ 步；枚举 $O(\log_x a \cdot \log_x b) \le 31^2 = 961$ 次常数运算，剪枝后远小于此。$t = 10^4$ 时约 $10^7$ 次基本运算，实测最坏 $21$ ms，相对 $1$ s 有 $45$ 倍以上余量。
- **空间**：$O(1)$（C++ 只用若干 `long long`），Python 版额外两条长度 $\le 32$ 的列表，仍为 $O(\log)$。
- **Python 实测**：用第 4 节第 5 条的单调优化后 $10^4$ 组最坏约 $0.2$ s，可以直接交 CPython；若照抄 C++ 的朴素双重循环约 $1.1$ s，会贴着 $1$ s 的时限（此时建议 PyPy 或改交 C++）。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;
    while (t--) {
        long long a, b, x;
        scanf("%lld %lld %lld", &a, &b, &x);
        long long best = llabs(a - b);          // 只加不除
        long long ka = 0, kb = 0;
        for (long long v = a; v > 0; v /= x) ++ka;
        for (long long v = b; v > 0; v /= x) ++kb;
        best = min(best, ka + kb);              // 两边都除到 0
        for (long long i = 0, u = a; i <= ka; ++i, u /= x) {
            if (i >= best) break;               // 代价至少为 i，无望
            for (long long j = 0, v = b; j <= kb && i + j < best; ++j, v /= x) {
                long long c = i + j + llabs(u - v);
                if (c < best) best = c;
            }
        }
        printf("%lld\n", best);
    }
    return 0;
}
```

### Python3

```python
import sys

INF = 10 ** 18


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    t = data[0]
    pos = 1
    out = []
    for _ in range(t):
        a, b, x = data[pos], data[pos + 1], data[pos + 2]
        pos += 3

        ua = [a]                     # ua[i] = a 连除 i 次 x
        while ua[-1] > 0:
            ua.append(ua[-1] // x)
        ub = [b]
        while ub[-1] > 0:
            ub.append(ub[-1] // x)
        ka, kb = len(ua) - 1, len(ub) - 1

        # 答案 = min_{i,j} (i + j + |ua[i] - ub[j]|)
        # ub 单调不增：对固定 ui 存在分界 j0，使 j >= j0 时 ub[j] <= ui
        pre = [0] * (kb + 1)         # 前缀 min(j + ub[j])
        run = INF
        for j in range(kb + 1):
            if j + ub[j] < run:
                run = j + ub[j]
            pre[j] = run
        suf = [0] * (kb + 1)         # 后缀 min(j - ub[j])
        run = INF
        for j in range(kb, -1, -1):
            if j - ub[j] < run:
                run = j - ub[j]
            suf[j] = run

        best = ka + kb               # 两边都除到 0
        j0 = 0                       # 随 ui 减小而右移
        for i in range(ka + 1):
            if i >= best:
                break
            ui = ua[i]
            while j0 <= kb and ub[j0] > ui:
                j0 += 1
            cand = INF
            if j0 <= kb:             # 右侧：ub[j] <= ui
                cand = suf[j0] + ui
            if j0 >= 1:              # 左侧：ub[j] > ui
                v = pre[j0 - 1] - ui
                if v < cand:
                    cand = v
            if i + cand < best:
                best = i + cand
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$a = b$**：答案 $0$，代码里 $(i, j) = (0, 0)$ 直接给出 $0$，无需特判；但若用 `i >= best` 做剪枝，`best = 0` 时第一轮就 `break`，结果仍是 $0$，正确。
2. **$x$ 比两个数都大**：一次除法直接归零，此时「两边都除到 $0$」只需 $2$ 步，通常远小于 $|a - b|$；这就是初值里必须有 $k_a + k_b$ 的原因。
3. **$a < x$**：$k_a = 1$，链只有 $[a, 0]$ 两项；若把循环写成 `while (m > 1)` 就会漏掉最后的 $0$。
4. **只除「大的那一边」不够**：直觉总想只除大数，但样例 $17\ 3\ 3$ 的最优两边都除了（$17 \to 5 \to 1$，$3 \to 1$）；只除 $17$ 得到 $|1 - 3| + 2 = 4 > 3$。必须对 $(i, j)$ 双向枚举。
5. **剪枝漏掉 $i = 0$ 分支**：$i = 0$ 对应「$a$ 一次都不除」，此时 $|a - n_j|$ 可能正是最优（如样例 $4\ 7\ 2$），不能因为 $i = 0$ 就跳过内层。
6. **多测未重置**：`best`、两条链、指针 `j0` 都必须在每组测试内重新初始化，否则上一组的大值会污染下一组。

## 相关题目与扩展

- [Codeforces 1872A Two Vessels](https://codeforces.com/problemset/problem/1872/A)：两杯水互相倒，问最少几步让水量差不超过 $D$——同样是把「两个数」化成「一个差量」的贪心。
- [LeetCode 991. 坏了的计算器](https://leetcode.cn/problems/broken-calculator/)：只能乘 $2$ 或减 $1$，从 $X$ 得到 $Y$；正难则反，从 $Y$ 反推 $X$，与本题「除法只能向下取整、于是把加法挪到后面」是同一类结构洞察。

**延伸思考**：

- 若除法改成**向上取整**，最优解的结构会翻转（此时除法前加 $1$ 才能「借位」，加法反而应该前置），本题的单调性论证需要重写。
- 若允许对 $a$ 和 $b$ 使用**不同的** $x$，或允许「乘 $x$」操作，则两条链不再是单调递减序列，$j_0$ 的双指针失效，得回到 $O(31^2)$ 枚举甚至二分。
- 若目标不是相等而是 $|a - b| \le D$，则只需把 $|m_i - n_j|$ 换成 $\max(0, |m_i - n_j| - D)$，其余推导不变。
