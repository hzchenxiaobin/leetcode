# Codeforces 119A Epic Game 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/119/A
- **比赛来源**：Codeforces Beta Round 90 · Problem A（UTC 2011-09-22）
- **难度**：800
- **标签**：实现
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：Simon 和 Antisimon 各有固定正整数 $a,b$，石堆初始有 $n$ 块。Simon 先手，轮到谁就从石堆取走 $\gcd(\text{自己的数},\ \text{当前剩余石子数})$ 块。取不够（剩余严格小于需要取的数）的人输。问 Simon 赢输出 `0`，否则输出 `1`。

**约束**：

- $1\le a,b,n\le100$：直接模拟。
- $\gcd(x,0)=x$：**剩余石子为 0 时**轮到的人要取 $\gcd(\cdot,0)=\cdot>0$ 块，必然取不到 → 输 ✓（所以不会死循环）。
- 每次至少取 1 块（$\gcd\ge1$），所以总回合数 $\le n+1$。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3 5 9

输出：
0
```

官方样例 2（输入 / 输出原样）：

```text
输入：
1 1 100

输出：
1
```

**样例 1 走查**：$a=3,b=5,n=9$。

| 回合 | 玩家 | 剩余 | 取 $\gcd$ | 取后 |
|------|------|------|-----------|------|
| 1 | Simon | 9 | $\gcd(3,9)=3$ | 6 |
| 2 | Antisimon | 6 | $\gcd(5,6)=1$ | 5 |
| 3 | Simon | 5 | $\gcd(3,5)=1$ | 4 |
| 4 | Antisimon | 4 | $\gcd(5,4)=1$ | 3 |
| 5 | Simon | 3 | $\gcd(3,3)=3$ | 0 |
| 6 | Antisimon | 0 | $\gcd(5,0)=5>0$ | 取不到 → Antisimon 输 |

Simon 赢 → 输出 `0` ✓。

**样例 2 走查**：两人都是 1，每次取 $\gcd(1,n)=1$ → 100 次后石堆为 0，轮到 Simon（第 101 回合）取 $\gcd(1,0)=1>0$ → Simon 输 → `1` ✓。

**观察**：胜负完全由"谁先面对取不够的局面"决定，直接按规则模拟即可；每回合至少取 1，最多 $n+1$ 回合。

![流程](../../../images/cf119a_game.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

无瓶颈：$O(n\log\max(a,b))$。

### 3.2 核心观察：终止条件

轮到的玩家需要的数量是 $g=\gcd(\text{自己的数}, n_{\text{剩余}})$；若 $g>n_{\text{剩余}}$ 则该玩家输 ✓。因为 $g\ge1$ 且每次至少取 1，模拟一定在 $n+1$ 步内结束 ✓。

![回合](../../../images/cf119a_turns.svg)

### 3.3 算法流程

1. 读入 $a,b,n$，`turn = Simon`；
2. 循环：算 $g=\gcd(\text{当前玩家的数}, n)$；若 $g>n$ → 当前玩家输 → 输出（Simon 输则 `1`，否则 `0`）；
3. 否则 $n\mathrel{-}=g$，换手。

### 3.4 样例走查

见 2 节表格 ✓。

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `1 1 1` | 0 | Simon 取 1 → 剩余 0 → Antisimon 取 $\gcd(1,0)=1>0$ 失败 |
| `2 2 2` | 0 | $\gcd(2,2)=2$ → Simon 取光，Antisimon 面对 0 输 |
| `6 4 2` | 0 | $\gcd(6,2)=2$ → Simon 取光 |

## 4. 正确性证明

**引理 1（模拟合法）**：每回合取走的数量 $g=\gcd(\cdot,n)\ge1$ 且当 $g\le n$ 时取走后剩余非负。

**证明**：$\gcd\ge1$；$g\le n$ 时 $n-g\ge0$ ✓。∎

**引理 2（终止）**：模拟在至多 $n+1$ 回合内到达"某人取不够"的局面。

**证明**：每回合剩余至少减少 1，最多 $n$ 回合后剩余为 0，此时轮到的人 $g\ge1>0$ → 输 ✓。∎

**定理**：算法输出正确。

**证明**：算法逐回合按题面规则更新，并在 $g>n$ 时判定当前玩家输（题面定义）✓；由引理 2 必然终止 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n\log \max(a,b))\le O(100\cdot7)$。
- **空间**：$O(1)$。
- **与时限的关系**：实测 C++ 端到端约 $2$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int a, b, n;
    if (!(cin >> a >> b >> n)) return 0;
    // Simon 先手：轮流取 gcd(自己的数, 剩余石子数)
    bool simon = true;
    while (true) {
        int take = std::gcd(simon ? a : b, n);
        if (take > n) { cout << (simon ? 1 : 0) << '\n'; return 0; }
        n -= take;
        simon = !simon;
    }
}
```

### Python3

```python
import math
import sys


def main() -> None:
    a, b, n = (int(t) for t in sys.stdin.buffer.read().split()[:3])
    simon = True
    while True:
        take = math.gcd(a if simon else b, n)
        if take > n:
            sys.stdout.write(("1" if simon else "0") + "\n")
            return
        n -= take
        simon = not simon


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **输出含义反直觉**：Simon 赢输出 `0`，输输出 `1`（题面如此）。
2. **$\gcd(x,0)=x$**：剩余为 0 时不是"平局"，而是轮到的人输。
3. **先手是 Simon**：第一回合用 $a$。
4. **取不够的定义**：严格小于（$g>n$）才输；$g=n$ 时正好取光 ✓。
5. **至少取 1**：$g\ge1$，循环一定终止。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：2 / 2 通过（`0`、`1`）。
- **额外测试**：250 组随机 $(a,b,n)\le(30,30,40)$ 与独立递归模拟比对，**250 / 250 全部一致**。
- **最大约束性能**：$a=b=1,\ n=100$ 时 C++ 端到端 15 次平均约 $2$ ms。
- **图片校验**：两张 SVG（`cf119a_game.svg`、`cf119a_turns.svg`）通过 `xml.etree.ElementTree.parse`，文本块估算未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError: true`）渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 119B Before Exam](https://codeforces.com/problemset/problem/119/B)：同场 B 题。
- [Codeforces 120A Elevator](https://codeforces.com/problemset/problem/120/A)：同一场次的 Div.2 A 题。
- [Codeforces 1104A Splitting into digits](https://codeforces.com/problemset/problem/1104/A)：构造。
- [LeetCode 292. Nim 游戏](https://leetcode.cn/problems/nim-game/)：博弈。
- [LeetCode 1025. 除数博弈](https://leetcode.cn/problems/divisor-game/)：博弈。

**延伸思考**：

1. **如果取 $\gcd$ 换成取固定值**：变成取石子游戏的周期分析。
2. **如果两人可以自选取多少**：变成 Nim 类博弈。
3. **如果要求输出总回合数**：模拟中计数即可。
4. **如果 $n$ 到 $10^{18}$**：需要找 $\gcd$ 序列的周期。
