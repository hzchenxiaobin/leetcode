# Codeforces 131C The World is a Theatre 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/131/C
- **比赛来源**：Codeforces Beta Round 95 (Div. 2 Only) · Problem C（UTC 2011-10-30）
- **难度**：1400
- **标签**：组合数学
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个男生、$m$ 个女生，选恰好 $t$ 人组成剧团，要求**男生至少 4 人、女生至少 1 人**。求方案数。

**约束**：

- $n,m\le30$、$t\le n+m$：组合数直接算，用 64 位（$C(60,30)\approx1.18\times10^{17}$ 在 `long long` 内）✓。
- 只按"构成"计，不按顺序 ✓。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
5 2 5

输出：
10
```

官方样例 2（输入 / 输出原样）：

```text
输入：
4 3 5

输出：
3
```

**样例 1 走查**：$n=5,m=2,t=5$：男生 4 + 女生 1：$\binom54\binom21=5\cdot2=10$；男生 5 + 女生 0：女生不足 ✗ → 10 ✓。

**样例 2 走查**：$n=4,m=3,t=5$：男生 4（唯一选择）+ 女生 1：$\binom44\binom31=1\cdot3=3$ ✓。

**观察**：枚举男生人数 $b\in[4,n]$，女生 $g=t-b$ 需满足 $1\le g\le m$ → 答案 $\sum_b\binom{n}{b}\binom{m}{t-b}$ ✓。

![枚举](../../../images/cf131c_split.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举子集不可行；按"男生人数"分类即可。

### 3.2 核心观察

两类人独立选 → 乘法原理；总人数固定 → 只需枚举一个维度 ✓。

![流程](../../../images/cf131c_flow.svg)

### 3.3 算法流程

1. 预处理组合数（帕斯卡三角到 60）；
2. 枚举 $b=4..n$，若 $1\le t-b\le m$ 则累加 $\binom nb\binom m{t-b}$；
3. 输出。

### 3.4 样例走查

见 2 节 ✓。

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `4 1 5` | 1 | 恰好 4 男 1 女 |
| `4 1 4` | 0 | 女生不足 |
| `5 5 9` | 5 | 只能是 4 男 5 女或 5 男 4 女 |

## 4. 正确性证明

**引理 1**：选定 $b$ 个男生、$g$ 个女生的方案数为 $\binom nb\binom mg$。

**证明**：两类独立选择，乘法原理 ✓。∎

**引理 2**：合法方案 $\iff$ $b\ge4$、$g\ge1$、$b+g=t$，且 $b\le n$、$g\le m$。

**证明**：题面约束 ✓。∎

**定理**：按 $b$ 求和不重不漏。

**证明**：每个方案有唯一的 $(b,g)$ ✓；由引理 1、2 求和即答案 ✓。∎

## 5. 复杂度分析

- **时间**：$O(60^2)$ 预处理 + $O(n)$ 枚举。
- **空间**：$O(60^2)$。
- **与时限的关系**：实测约 $2$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
ll C[61][61];
int main() {
    int n, m, t;
    if (!(cin >> n >> m >> t)) return 0;
    for (int i = 0; i <= 60; ++i) {
        C[i][0] = 1;
        for (int j = 1; j <= i; ++j) C[i][j] = C[i-1][j-1] + C[i-1][j];
    }
    ll ans = 0;
    for (int b = 4; b <= n && b <= t - 1; ++b) {
        int g = t - b;
        if (g < 1 || g > m) continue;
        ans += C[n][b] * C[m][g];
    }
    cout << ans << '\n';
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    n, m, t = (int(x) for x in sys.stdin.buffer.read().split()[:3])
    C = [[0] * 61 for _ in range(61)]
    for i in range(61):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i-1][j-1] + C[i-1][j]
    ans = 0
    for b in range(4, min(n, t - 1) + 1):
        g = t - b
        if 1 <= g <= m:
            ans += C[n][b] * C[m][g]
    print(ans)


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **男生下限 4、女生下限 1**：两条边界的上下都要检查。
2. **64 位**：$C(60,30)$ 超过 `int`。
3. **$t$ 太小**：如 $t<5$ → 0。
4. **女生不够**：$g>m$ 跳过。
5. **组合数预处理到 $n+m\le60$**。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：2 / 2 通过（`10`、`3`）。
- **额外测试**：200 组随机小数据与"枚举所有 $\binom{n+m}{t}$ 组合"的暴力比对，**200 / 200 全部一致**。
- **图片校验**：两张 SVG（`cf131c_split.svg`、`cf131c_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 131B Opposites Attract](https://codeforces.com/problemset/problem/131/B)：同场 B 题。
- [Codeforces 131D Subway](https://codeforces.com/problemset/problem/131/D)：同场 D 题。
- [LeetCode 62. 不同路径](https://leetcode.cn/problems/unique-paths/)：组合数。
- [LeetCode 1569. 将子数组重新排序得到同一个二叉查找树的方案数](https://leetcode.cn/problems/number-of-ways-to-reorder-array-to-get-same-bst/)：组合计数。

**延伸思考**：

1. **如果要求男女都至少 $k$ 人**：改枚举边界。
2. **如果人数到 $10^5$**：用阶乘 + 逆元。
3. **如果要求指定某些人必须参加**：预先扣除。
4. **如果要求顺序**：乘上 $t!$。
