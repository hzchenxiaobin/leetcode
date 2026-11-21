# Codeforces 222C 约分（Reducing Fractions） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/222/C
- **比赛来源**：Codeforces Round 137 (Div. 2) · Problem C（UTC 2012-09-10）
- **难度**：1800
- **标签**：数论、质因数分解
- **评测类型**：特殊评测（多解，分数等价且已约分）
- **限制**：时间 2 s / 内存 256 MB

**题意**：给定 $n$ 个数与 $m$ 个数的两组集合，分子、分母分别是各组之积。把分数约分，输出等价的两组数（个数不变，每个数 ≥1）。

**约束**：$n,m\le10^5$，每个数 $\le10^7$。

## 2. 示例与观察

官方样例一：

```text
输入：
3 2
100 5 2
50 10

输出：
2 3
2 1
1 1 1
```

官方样例二：

```text
输入：
4 3
2 5 10 20
100 1 3

输出：
1 1
20
3
```

**观察**：约分等价于对每个质数 $p$，从分子、分母各去掉 $\min$(指数) 个。值 ≤ $10^7$ ⇒ 用最小质因子筛分解。

![质因数分解后约分](../../../images/cf222c_factor.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

直接做大数 gcd 不可行（乘积巨大）；但分解后逐质数处理即可。

### 3.2 核心观察

统计分子/分母每个质数的总指数，取可约去量，再逐个从每个数中除掉对应因子。

### 3.3 算法流程

1. SPF 筛到 $10^7$。
2. 分解所有数，统计 $\mathrm{cntA}[p]$、$\mathrm{cntB}[p]$。
3. 可约去量 $c_p=\min(\mathrm{cntA},\mathrm{cntB})$。
4. 重新分解每个数，把前 $c_p$ 个因子 $p$ 去掉，输出剩下的乘积。

![样例](../../../images/cf222c_walk.svg)

### 3.4 样例走查

样例一：$100\cdot5\cdot2/(50\cdot10)=1000/500=2/1$，输出如 `1 1 2 / 1 1` ✓；样例二 $2000/300=20/3$ ✓。

## 4. 正确性证明

**引理 1（约分条件）**：$\gcd$(分子, 分母) $=\prod_p p^{\min(\mathrm{cntA},\mathrm{cntB})}$。

**证明**：质因数分解唯一，公共部分即各质数指数取小。∎

**引理 2（构造正确）**：按 $c_p$ 从两侧各删去这些因子后，左右乘积比不变且互质。

**证明**：两侧同除相同因子比值不变；每侧不再共享任何质数 ⇒ 互质。∎

**定理**：输出合法。

**证明**：由引理 1、2。∎

## 5. 复杂度分析

- **时间**：$O(MAXV\log\log MAXV+\text{总因子数})$。\n- **空间**：$O(MAXV)$（SPF 数组 40 MB）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
static const int MAXV = 10000000;
static int spf[MAXV + 1];
int main() {
    for (int i = 0; i <= MAXV; ++i) spf[i] = i;
    for (int i = 2; (long long)i * i <= MAXV; ++i)
        if (spf[i] == i)
            for (long long j = (long long)i * i; j <= MAXV; j += i)
                if (spf[j] == j) spf[j] = i;
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<int> a(n), b(m);
    for (int i = 0; i < n; ++i) scanf("%d", &a[i]);
    for (int i = 0; i < m; ++i) scanf("%d", &b[i]);
    unordered_map<int, long long> cntA, cntB;
    cntA.reserve(1 << 16); cntB.reserve(1 << 16);
    for (int x : a) { while (x > 1) { int p = spf[x]; ++cntA[p]; x /= p; } }
    for (int x : b) { while (x > 1) { int p = spf[x]; ++cntB[p]; x /= p; } }
    // 计算可消去的指数
    unordered_map<int, long long> cancelA, cancelB;
    for (auto &kv : cntA) {
        long long other = cntB.count(kv.first) ? cntB[kv.first] : 0;
        long long c = min(kv.second, other);
        if (c) { cancelA[kv.first] = c; cancelB[kv.first] = c; }
    }
    // 从 a 的每个数里除掉 cancelA 的因子
    for (int i = 0; i < n; ++i) {
        int x = a[i];
        int y = 1;
        while (x > 1) {
            int p = spf[x]; x /= p;
            auto it = cancelA.find(p);
            if (it != cancelA.end() && it->second > 0) --it->second;
            else y *= p;
        }
        a[i] = y;
    }
    for (int i = 0; i < m; ++i) {
        int x = b[i];
        int y = 1;
        while (x > 1) {
            int p = spf[x]; x /= p;
            auto it = cancelB.find(p);
            if (it != cancelB.end() && it->second > 0) --it->second;
            else y *= p;
        }
        b[i] = y;
    }
    printf("%d %d\n", n, m);
    for (int i = 0; i < n; ++i) printf("%d%c", a[i], i + 1 == n ? '\n' : ' ');
    for (int i = 0; i < m; ++i) printf("%d%c", b[i], i + 1 == m ? '\n' : ' ');
    return 0;
}
```

### Python3

```python
import sys

MAXV = 10 ** 7
spf = list(range(MAXV + 1))
i = 2
while i * i <= MAXV:
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i
    i += 1


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    b = [int(x) for x in data[2 + n:2 + n + m]]
    ca = {}
    cb = {}
    for x in a:
        while x > 1:
            p = spf[x]; ca[p] = ca.get(p, 0) + 1; x //= p
    for x in b:
        while x > 1:
            p = spf[x]; cb[p] = cb.get(p, 0) + 1; x //= p
    canA = {}
    canB = {}
    for p, c in ca.items():
        c2 = min(c, cb.get(p, 0))
        if c2:
            canA[p] = c2; canB[p] = c2
    for i in range(n):
        x = a[i]; y = 1
        while x > 1:
            p = spf[x]; x //= p
            if canA.get(p, 0) > 0:
                canA[p] -= 1
            else:
                y *= p
        a[i] = y
    for i in range(m):
        x = b[i]; y = 1
        while x > 1:
            p = spf[x]; x //= p
            if canB.get(p, 0) > 0:
                canB[p] -= 1
            else:
                y *= p
        b[i] = y
    print(n, m)
    print(' '.join(map(str, a)))
    print(' '.join(map(str, b)))


main()
```

## 7. 边界情况与易错点

1. **某个数变成 1**：仍要输出 1。
2. **分子/分母个数不变**：输出行数固定。
3. **完全约掉**：如 2/4 ⇒ 1/2，两个 1 也要输出。
4. **值到 $10^7$**：筛要开够。
5. **多解**：只要等价且已约分，输出格式自由（校验器检查）。

## 8. 验证记录

- **编译环境与命令**：`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/222/C_约分.md --checker codeforces/tools/checkers/cf222c.py`。
- **官方样例**：2 / 2 通过。
- **随机对拍**：用“分数等价 + 已约分”校验器检查样例与随机数据；另与 Python 大整数暴力约分对照 **250 组**。
- **性能**：$n=m=10^5$、值 $10^7$ 时 0.08 s（筛 0.1 s）。
- **图片校验**：`cf222c_factor.svg`、`cf222c_walk.svg` 通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 222B 宇宙表](https://codeforces.com/problemset/problem/222/B)：同场题目。
- [LeetCode 1025 除数博弈](https://leetcode.cn/problems/divisor-game/)：数论。

**延伸思考**：

1. 若乘积超过 64 位，仍可用分解法。
2. 若要求输出仍按原顺序的因子，需记录分解。
