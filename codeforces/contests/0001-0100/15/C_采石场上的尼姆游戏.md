# Codeforces 15C 采石场上的尼姆游戏 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/15/C
- **比赛来源**：Codeforces Beta Round 15 · Problem C（UTC 2010-05-29）
- **难度**：2000
- **标签**：博弈论、数学（games, math）
- **评测类型**：普通
- **限制**：时间 2 s / 内存 64 MB

**题意**：有 $n$ 个采石场。第 $i$ 个采石场有 $m_i$ 辆自卸车，车里的石头数依次是

$$x_i,\ x_i + 1,\ x_i + 2,\ \dots,\ x_i + m_i - 1 .$$

两人玩标准 Nim 游戏：轮流选一辆车、取走任意正数块石头，取不了的人输。先手必胜输出 `tolik`，否则输出 `bolik`。

**约束**：

- $n \le 10^5$，$x_i, m_i \le 10^{16}$：单是"把每辆车都列出来"就有 $\sum m_i$ 可达 $10^{21}$ 个，绝无可能。
- $x_i + m_i - 1 \le 2 \times 10^{16}$：仍在 64 位整数范围内（$2^{63} \approx 9.2 \times 10^{18}$），但**必须**用 `long long`，`int` 完全不够，`double` 也不行。
- 每个采石场贡献的是一段**连续整数**，所以可以用"前缀异或"的 $O(1)$ 公式把整段一起算掉。
- 输出必须是小写的 `tolik` / `bolik`。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
2
2 1
3 2

输出：
tolik
```

**样例 1 演算**：第 1 个采石场只有一辆车，$2$ 块石头；第 2 个采石场有两辆车，分别是 $3$ 块与 $4$ 块。所有堆的大小是 $\{2, 3, 4\}$，异或和

$$2 \oplus 3 \oplus 4 = (2 \oplus 3) \oplus 4 = 1 \oplus 4 = 5 \ne 0 .$$

Nim 的异或和非零，先手必胜，输出 `tolik`。

官方样例 2（输入 / 输出原样）：

```text
输入：
4
1 1
1 1
1 1
1 1

输出：
bolik
```

**样例 2 演算**：四辆车，每辆都是 $1$ 块石头，异或和 $1 \oplus 1 \oplus 1 \oplus 1 = 0$，先手必败，输出 `bolik`。

**观察**：

1. Nim 的胜负只取决于所有堆大小的**异或和**，所以问题变成"快速求出 $\bigoplus_{i=1}^n \bigoplus_{t=x_i}^{x_i+m_i-1} t$"。
2. 每段是连续整数，而"$1$ 到 $k$ 的异或和"有非常简单的封闭形式（只与 $k \bmod 4$ 有关），于是每一段可以用**两个前缀异或**相减（异或意义下就是再异或一次）得到。

自造样例（标注"自造"，`⏎` 表示换行；均已用参考程序与逐堆暴力核对）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `2 ⏎ 2 1 ⏎ 3 2` | `tolik` | 官方样例 1，异或和 $5$ |
| `4 ⏎ 1 1 ⏎ 1 1 ⏎ 1 1 ⏎ 1 1` | `bolik` | 官方样例 2，异或和 $0$ |
| `1 ⏎ 5 3` | `tolik` | $5 \oplus 6 \oplus 7 = 4 \ne 0$ |
| `1 ⏎ 1 4` | `tolik` | $1 \oplus 2 \oplus 3 \oplus 4 = 4 \ne 0$ |
| `1 ⏎ 1 3` | `bolik` | $1 \oplus 2 \oplus 3 = 0$，先手必败 |
| `2 ⏎ 10000000000000000 1 ⏎ 10000000000000000 2` | `tolik` | 两段分别为 $\{10^{16}\}$ 与 $\{10^{16}, 10^{16}+1\}$，异或剩 $10^{16}+1$ |

第 5 组是"前缀长度为 $4$ 的倍数时异或为 $0$"的典型：$1 \oplus 2 \oplus 3 = (1 \oplus 2) \oplus 3 = 3 \oplus 3 = 0$。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

把每个采石场的每辆车都展开，逐堆异或。$\sum m_i$ 可达 $10^5 \times 10^{16} = 10^{21}$，$2$ s 内绝无可能——连读入都做不到。

但注意：堆的大小是**连续整数**。如果能 $O(1)$ 求出一段连续整数的异或和，整个问题就变成 $O(n)$。

### 3.2 核心观察：$1 \oplus 2 \oplus \dots \oplus k$ 的封闭形式

![前缀异或的四种情况](../../../images/cf15c_prefix.svg)

记 $g(k) = 1 \oplus 2 \oplus \dots \oplus k$（并规定 $g(0) = 0$）。按 $k \bmod 4$ 分类，可以直接验证（归纳证明见第 4 节）：

$$g(k) = \begin{cases} k, & k \bmod 4 = 0,\\ 1, & k \bmod 4 = 1,\\ k+1, & k \bmod 4 = 2,\\ 0, & k \bmod 4 = 3.\end{cases}$$

于是任意区间 $[l, r]$ 的异或和是

$$\bigoplus_{t=l}^{r} t = g(r) \oplus g(l-1).$$

![Nim 的异或和与区间拆分](../../../images/cf15c_nim.svg)

对第 $i$ 个采石场，贡献为 $g(x_i + m_i - 1) \oplus g(x_i - 1)$；把所有贡献再异或起来，得到总异或和 $S$。由 Nim 定理：$S \ne 0$ 先手必胜（`tolik`），$S = 0$ 先手必败（`bolik`）。

整个算法只有 $O(n)$ 次 $O(1)$ 的前缀异或，完全不需要展开任何一辆车。

### 3.3 算法流程

1. 读入 $n$；
2. 令 `total = 0`；
3. 对每个采石场 $(x, m)$：
   1. `r = x + m - 1`，`l = x`；
   2. `total ^= g(r) ^ g(l - 1)`；
4. 输出 `total ? "tolik" : "bolik"`。

其中 `g(k)` 用 `switch (k & 3)` 或查表实现，注意 `g(0) = 0` 与 `k = 0` 时返回 $0$（本题 $x \ge 1$，`l - 1` 可能为 $0$，必须处理）。

### 3.4 样例走查：样例 1

![样例 1 的区间拆分](../../../images/cf15c_walkthrough.svg)

| 采石场 | 区间 | $g(r)$ | $g(l-1)$ | 段异或 | 累计 `total` |
|--------|------|--------|----------|--------|--------------|
| 1 | $[2, 2]$ | $g(2) = 3$ | $g(1) = 1$ | $3 \oplus 1 = 2$ | $2$ |
| 2 | $[3, 4]$ | $g(4) = 4$ | $g(2) = 3$ | $4 \oplus 3 = 7$ | $2 \oplus 7 = 5$ |

最终 `total = 5 ≠ 0`，输出 `tolik`。可以对照手算：$\{2\}$ 与 $\{3,4\}$ 合并即 $\{2,3,4\}$，$2 \oplus 3 \oplus 4 = 5$ ✓

## 4. 正确性证明

**引理 1（Nim 定理）**：标准 Nim 游戏（每步从一堆中取任意正数个）中，先手必胜当且仅当所有堆大小的异或和非零。

**证明**：设异或和为 $S$。

若 $S = 0$：任意一步把某堆从 $a$ 改成 $a' < a$，则新的异或和 $S' = S \oplus a \oplus a' = a \oplus a' \ne 0$（因为 $a' \ne a$）。也就是说，$S = 0$ 的局面只能走到 $S \ne 0$ 的局面。

若 $S \ne 0$：设 $S$ 的最高二进制位是第 $b$ 位，则必存在某堆 $a$ 的第 $b$ 位为 $1$。取 $a' = a \oplus S$，则 $a' < a$（最高位被消掉），且新异或和 $S \oplus a \oplus a' = S \oplus a \oplus (a \oplus S) = 0$。所以 $S \ne 0$ 时总能走到 $S = 0$。

终局（全 $0$）的异或和是 $0$，且它是必败态。由上面两条，$S \ne 0$ 是必胜态、$S = 0$ 是必败态（对堆数归纳）。∎

**引理 2（前缀异或公式）**：对任意 $k \ge 0$，$g(k) = 1 \oplus \dots \oplus k$ 满足
$g(k) = k$（$k \equiv 0$）、$1$（$k \equiv 1$）、$k+1$（$k \equiv 2$）、$0$（$k \equiv 3$），模 $4$。

**证明**：对 $k$ 归纳，每四个一组。先验证 $k = 0,1,2,3$：$g(0) = 0$、$g(1) = 1$、$g(2) = 3 = 2+1$、$g(3) = 0$，与公式一致。

设对某个 $k$ 成立，考虑 $k+4$：

$$g(k+4) = g(k) \oplus (k+1) \oplus (k+2) \oplus (k+3) \oplus (k+4).$$

连续的四个整数 $k+1, k+2, k+3, k+4$ 中，$k+1$ 与 $k+2$ 只差最低位，$k+3$ 与 $k+4$ 也只差最低位，而更高位相同。直接计算：$(k+1)\oplus(k+2) = 1$、$(k+3)\oplus(k+4) = 1$（因为每对只差最低位），故这四个数的异或为 $1 \oplus 1 = 0$。于是 $g(k+4) = g(k)$，即 $g$ 以 $4$ 为周期，公式对一切 $k$ 成立。∎

**引理 3（区间异或的分解）**：$\bigoplus_{t=l}^{r} t = g(r) \oplus g(l-1)$。

**证明**：$g(r) = g(l-1) \oplus \bigl(\bigoplus_{t=l}^{r} t\bigr)$，两边同异或 $g(l-1)$ 即得（异或满足结合律、交换律，且 $x \oplus x = 0$）。∎

**定理**：算法输出的胜利判断与双方最优策略下的真实结果一致。

**证明**：由引理 3，算法对每个采石场算出的正是该段所有车的异或和 $g(x+m-1) \oplus g(x-1)$；把这些段异或起来，得到全部车的异或和 $S$（把所有车按采石场分组不影响异或结果）。由引理 1，$S \ne 0$ 时先手必胜、$S = 0$ 时先手必败，算法正是按 $S$ 是否为零输出两个字符串。∎

## 5. 复杂度分析

- **时间**：$O(n)$。每个采石场只做两次前缀异或求值（每次几次位运算）和一次异或合并，$n \le 10^5$ 时约 $3 \times 10^5$ 次基本操作。
- **空间**：$O(1)$（不算读入缓冲），只存累计异或和。
- **数值范围**：$x + m - 1 \le 2 \times 10^{16} < 2^{63}-1$，`long long` 足够；`int` 会在 $x$ 处就溢出。Python 的整数无上限，天然安全。
- **与时限的关系**：时限 2 s，$n = 10^5$、$x, m$ 取 $10^{16}$ 的最坏数据实测 C++ 端到端约 $0.40$ s（其中大部分是读入 $10^5$ 行 16 位十进制数）、峰值内存 $1.7$ MB；Python 约 $0.08$ s。余量在 5 倍以上。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

// [1, k] 内所有整数异或和：k mod 4 决定
static inline long long xorUpto(long long k) {
    if (k < 0) return 0;
    switch (k & 3LL) {
        case 0: return k;
        case 1: return 1;
        case 2: return k + 1;
        default: return 0;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    long long total = 0;
    for (int i = 0; i < n; ++i) {
        long long x, m;
        cin >> x >> m;
        total ^= xorUpto(x + m - 1) ^ xorUpto(x - 1);   // 区间 [x, x+m-1] 的异或
    }
    cout << (total ? "tolik" : "bolik") << '\n';
    return 0;
}
```

### Python3

```python
import sys


def xor_upto(k: int) -> int:
    """[1, k] 的整数异或和"""
    if k < 0:
        return 0
    r = k & 3
    if r == 0:
        return k
    if r == 1:
        return 1
    if r == 2:
        return k + 1
    return 0


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    p = 1
    total = 0
    for _ in range(n):
        x, m = int(data[p]), int(data[p + 1])
        p += 2
        total ^= xor_upto(x + m - 1) ^ xor_upto(x - 1)
    sys.stdout.write(("tolik" if total else "bolik") + "\n")


main()
```

## 7. 边界情况与易错点

1. **`int` 溢出**：$x, m \le 10^{16}$，`int` 只能存到 $2 \times 10^9$ 左右。所有涉及 $x, m$ 的运算都要 `long long`。
2. **`x + m - 1` 的范围**：最大 $2 \times 10^{16}$，`long long` 安全；但若题目把上限改成 $10^{18}$，就要注意 $x + m - 1$ 可能逼近 $2^{63}$，仍需 64 位（Python 无碍）。
3. **`g(0)`**：当 $x = 1$ 时 $l - 1 = 0$，必须让 `g(0) = 0`，否则会把区间算错。代码里显式写了 `k < 0 → 0`，且 `k = 0` 走 `k & 3 == 0` 分支返回 $0$。
4. **`k mod 4` 的四条分支**：$k \equiv 0 \to k$、$1 \to 1$、$2 \to k+1$、$3 \to 0$，别记错顺序（尤其是 $k \equiv 2$ 是 $k+1$ 而不是 $k$）。
5. **先手/后手的字符串**：先手必胜是 `tolik`，必败是 `bolik`；大小写与拼写都要与题面完全一致（全小写）。
6. **段内异或用异或合并，不是相加**：$g(r) \oplus g(l-1)$，不是 $g(r) - g(l-1)$。写成减法是最常见的错误。
7. **多组的读入**：$n$ 行两个数，用 `cin >>` 或一次 `split` 均可；`n = 10^5` 时注意关闭同步。
8. **`m = 1` 的退化**：此时区间只有一个数 $x$，公式给出 $g(x) \oplus g(x-1) = x$，正确。
9. **空堆**：题目保证 $x_i, m_i \ge 1$，不会出现 $0$ 块石头的堆，因此不需要考虑"空堆不影响异或和"之外的退化。

## 8. 验证记录

- **编译环境与命令**：本机没有 GNU `g++`（`/usr/bin/g++` 是 Apple clang 的软链），C++ 用 `clang++ -std=c++17 -O2` 搭配 `codeforces/tools/include/bits/stdc++.h` 兼容头编译，代码只用标准库，可原样提交 GNU C++17；Python 为 `Python 3.9.6`。文档结构 / 编译 / 样例由 `python3 codeforces/tools/verify_solution.py codeforces/contests/0001-0100/15/C_采石场上的尼姆游戏.md` 一条命令复核。
- **官方样例**：2 / 2 通过（`samples 2`、`C++ 编译 OK, 样例 2/2`、`Python 语法 OK, 样例 2/2`）。
- **独立暴力对拍**：暴力程序把每辆车的大小逐堆异或起来（完全不用前缀公式），生成 **250 组**随机小数据（$n \le 6$；两种模式：$x \le 40, m \le 12$ 与 $x \le 6, m \le 4$，后者专门覆盖 $k \bmod 4 = 0$ 的边界），C++ 与 Python 各跑一遍，合计 **500 次**比对，**0 处不符**。
- **最大约束性能**：$n = 10^5$、$x, m$ 取 $10^{16}$ 量级的随机数据，C++ 端到端约 $0.40$ s、峰值内存 $1.7$ MB；Python 约 $0.08$ s，相对 2 s / 64 MB 余量充足。
- **图片校验**：三张 SVG（`cf15c_prefix.svg`、`cf15c_nim.svg`、`cf15c_walkthrough.svg`）均通过 `xml.etree.ElementTree.parse`，并用无头浏览器读取每个 `text` 的 `getBBox` 复核：无越出 `viewBox`、无文字互相重叠、无文字溢出所在方框。
- **公式校验**：正文公式经 `node codeforces/tools/katex_check.cjs`（`throwOnError`）渲染无报错。
- **复核状态**：verified（样例、500 次对拍、性能、图片、公式五项均实跑通过；环境差异仅在于本机无 GNU g++，已用 clang++ 等价验证）。

## 相关题目与扩展

- [Codeforces 15A Cottage Village](https://codeforces.com/problemset/problem/15/A)、[Codeforces 15B Laser](https://codeforces.com/problemset/problem/15/B)：同场 A、B 题，分别是"离散候选枚举"与"矩形容斥"。
- [LeetCode 1486. 数组异或操作](https://leetcode.cn/problems/xor-operation-in-an-array/)：区间异或的入门版。
- [LeetCode 810. 黑板异或游戏](https://leetcode.cn/problems/chalkboard-xor-game/)：另一道用异或和判断胜负的博弈题。
- [Codeforces 10C Digital Root](https://codeforces.com/problemset/problem/10/C)：同样是"用数论公式把 $O(n^2)$ 压到 $O(1)$"的计数题。

**延伸思考**：

1. **如果采石场的车数不是连续整数**：前缀异或的封闭形式失效，需要用更一般的"按位计数"：对每一位统计有多少个数在该位上是 $1$，复杂度 $O(n \log \max)$，对任意给出的数列都适用。
2. **如果要求输出第一步的走法**：Nim 定理的构造性证明给出了方法——找到异或和最高位对应的一堆，把它改成 $a \oplus S$，这样第一步就能走到异或和为 $0$ 的局面。
3. **为什么 $g$ 的周期是 $4$**：四个连续整数中，前两个只差最低位、后两个也只差最低位，配对异或各得 $1$，再异或得 $0$；这个结构性原因是公式简洁的根源。
4. **如果石头数的范围到 $10^{18}$ 且要求模某个数**：异或没有模运算，只能按位处理；但"异或和"本身依然在 64 位内，只有区间端点需要小心溢出。
5. **Nim 的变体**：如果每步最多取 $k$ 个（受限 Nim），先手胜负由"每堆模 $k+1$ 后的异或和"决定；本篇的 $g$ 公式仍然能派上用场，只是每个数要先取模。
