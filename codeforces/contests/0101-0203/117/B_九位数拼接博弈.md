# Codeforces 117B 九位数拼接博弈 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/117/B
- **比赛来源**：Codeforces Beta Round 88 · Problem B（UTC 2011-09-23）
- **难度**：1800
- **标签**：博弈、数论、同余
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：先手写一个 9 位数字串 $s_1$（数值 $\le a$，允许前导零），后手看到后写 $s_2$（数值 $\le b$，允许前导零）。若拼接出的 18 位数 $s_1\cdot10^9+s_2$ 被 $mod$ 整除则后手胜，否则先手胜。双方最优，问胜负；若先手胜，输出字典序最小的获胜 $s_1$。

**约束**：

- $a,b\le10^9$，$mod\le10^7$：可以枚举 $s_1$ 的 $mod$ 个余类。
- 定长 9 位 → 字典序即数值序。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
1 10 7
输出：
2
```

官方样例二：

```text
输入：
4 0 9
输出：
1 000000001
```

**样例一走查**：$s_1=0$：需要 $s_2\equiv0\pmod7$，$s_2=0\le10$ 即可 → 后手胜；$s_1=1$：$10^9\equiv6$，需要 $s_2\equiv1$，$1\le10$ → 后手胜。两种都挡不住 → `2` ✓。

**样例二走查**：$a=4,b=0$：后手只能写 $s_2=0$，需 $s_1\cdot10^9\equiv0\pmod9$，即 $s_1\equiv0\pmod9$。$s_1=0$ 会让后手赢，$s_1=1$ 时 $r=8>0$ → 先手胜，输出 `000000001` ✓。

![同余模型](../../../images/cf117b_model.svg)

**观察**：给定 $s_1$，后手能选的 $s_2\in[0,b]$ 中与目标同余的最小非负解是 $r=(-s_1\cdot10^9)\bmod mod$；所以

$$\text{后手胜}\iff r\le b,\qquad \text{先手胜}\iff r>b .$$

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举 $s_1\in[0,a]$ 与 $s_2\in[0,b]$：$10^{18}$ 对，不可能。但注意 $r$ 只依赖 $s_1\bmod mod$，所以只需枚举 $s_1$ 的余类代表，最多 $mod\le10^7$ 个。

### 3.2 核心观察：只需前 $mod$ 个数

![样例对照](../../../images/cf117b_sample.svg)

$r(s_1)$ 随 $s_1$ 以 $mod$ 为周期。若存在可行 $s_1\le a$，则最小的可行 $s_1$ 一定 $<mod$（否则减去 $mod$ 后同样可行且更小）。于是从小到大枚举 $s_1=0,1,\dots,\min(a,mod-1)$，第一个满足 $r>b$ 的就是字典序最小答案（定长 9 位，数值序 = 字典序）。

### 3.3 算法流程

1. 计算 $p=10^9\bmod mod$；
2. 对 $s_1=0..\min(a,mod-1)$：$r=(-(s_1\bmod mod)\cdot p)\bmod mod$；若 $r>b$ 输出 `1` 与 9 位补零的 $s_1$；
3. 全都不行输出 `2`。

### 3.4 样例走查

| $a,b,mod$ | 枚举 | 结论 |
|---|---|---|
| $1,10,7$ | $s_1=0\to r=0$；$s_1=1\to r=1$ | 都 $\le10$ → `2` |
| $4,0,9$ | $s_1=0\to r=0$；$s_1=1\to r=8>0$ | `1 000000001` |

## 4. 正确性证明

**引理 1**：给定 $s_1$，后手存在合法 $s_2$ 当且仅当 $r=(-s_1\cdot10^9)\bmod mod\le b$。

**证明**：需要 $s_2\equiv -s_1\cdot10^9\pmod{mod}$；$[0,b]$ 中最小的非负同余解是 $r$，若 $r\le b$ 取 $s_2=r$；否则所有解都 $\ge r>mod-1$？不一定——解是 $r+k\cdot mod$，最小正的是 $r$，若 $r>b$ 则更大的也 $>b$ ✓。∎

**引理 2**：若存在可行 $s_1\le a$，则最小的可行 $s_1$ 小于 $mod$。

**证明**：$r$ 以 $mod$ 为周期；若 $s_1\ge mod$ 可行，则 $s_1-mod$ 也可行且更小，与最小性矛盾 ✓。∎

**引理 3**：在定长 9 位表示下，字典序最小等于数值最小。

**证明**：等长字符串的字典序比较与对应整数的大小比较一致 ✓。∎

**定理**：算法输出的胜负与（先手胜时）$s_1$ 都正确。

**证明**：由引理 1，先手胜 $\iff$ 存在 $s_1\le a$ 使 $r>b$；由引理 2，只需检查前 $mod$ 个数，算法从小到大枚举并取第一个可行值 ✓，再由引理 3 它就是字典序最小的获胜串 ✓。∎

## 5. 复杂度分析

- **时间**：$O(\min(a,mod))$，最坏 $10^7$。
- **空间**：$O(1)$。
- **数值范围**：$s_1\cdot10^9$ 会超过 64 位，必须先取模；用 `long long` 且先 `% mod`。
- **与时限的关系**：2 s 下实测 $10^7$ 次循环约 $21$ ms（C++）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    ll a, b, mod;
    if (scanf("%lld %lld %lld", &a, &b, &mod) != 3) return 0;
    ll pw = 1;
    for (int i = 0; i < 9; ++i) pw = (pw * 10) % mod;   // 10^9 mod mod
    ll lim = min(a, (ll)mod - 1);
    for (ll s1 = 0; s1 <= lim; ++s1) {
        ll r = (mod - (s1 % mod) * pw % mod) % mod;
        if (r > b) {
            printf("1 %09lld\n", s1);
            return 0;
        }
    }
    printf("2\n");
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
    a = int(data[0]); b = int(data[1]); mod = int(data[2])
    pw = pow(10, 9, mod)
    lim = min(a, mod - 1)
    for s1 in range(lim + 1):
        r = (-(s1 % mod) * pw) % mod
        if r > b:
            sys.stdout.write("1 %09d\n" % s1)
            return
    sys.stdout.write("2\n")


main()
```

## 7. 边界情况与易错点

1. **$mod=1$**：$r\equiv0$ 恒成立；$b\ge0$ 时后手必胜 → 输出 `2`。
2. **$b=0$**：只有 $r=0$ 时后手能赢；先手要避开 $s_1\equiv0\pmod{mod}$。
3. **$a=0$**：先手只能写 $0$，直接判断。
4. **$10^9$ 溢出**：必须先把 $10^9$ 对 $mod$ 取模再乘。
5. **枚举上界**：`min(a, mod-1)`，不要用 `min(a, mod)` 或直接枚举到 $a$。
6. **补零**：输出必须恰好 9 位（`%09lld`）。
7. **字典序**：定长时与数值序一致，所以从小到大枚举即可。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：2 / 2 通过（`2`、`1 000000001`），C++ 与 Python 输出一致。
- **独立暴力对拍**：暴力枚举所有 $(s_1,s_2)$ 对（$a,b\le40$、$mod\le40$）判断后手是否有招，再取最小获胜 $s_1$（与同余推导不同）。**260 组**随机数据全部一致。
- **最大约束性能**：$a=b=10^9$、$mod=10^7$ 时 C++ 约 $21$ ms。
- **图片校验**：`cf117b_model.svg`、`cf117b_sample.svg` 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写体字体族，文本包围盒未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError`）渲染无报错；无 `---` 分隔线。
- **复核状态**：verified（样例、对拍、性能、图片、公式均实跑通过）。

## 相关题目与扩展

- [Codeforces 117A 电梯往返时间](https://codeforces.com/problemset/problem/117/A)、[117C Cycle](https://codeforces.com/problemset/problem/117/C)、[117D Not Quick Transformation](https://codeforces.com/problemset/problem/117/D)：同场其余题。
- [Codeforces 1104C Grid game](https://codeforces.com/problemset/problem/1104/C)：博弈 + 构造。
- [Codeforces 1382B Sequential Nim](https://codeforces.com/problemset/problem/1382/B)：简单博弈。
- [LeetCode 877. 石子游戏](https://leetcode.cn/problems/stone-game/)：最优策略推理。

**延伸思考**：

1. **如果 $s_1,s_2$ 长度可变**：字典序与数值序不再一致，需要按长度分层。
2. **如果要求后手输出字典序最小**：需要再解一次同余下界问题。
3. **如果拼接的是 $s_2$ 在前**：只需交换 $a,b$ 与乘数。
4. **如果 $mod$ 到 $10^9$**：枚举 $mod$ 个余类不可行，需要更强的数论（如解线性同余 + 区间判定）。

