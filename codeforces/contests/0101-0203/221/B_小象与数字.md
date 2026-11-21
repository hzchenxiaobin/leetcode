# Codeforces 221B 小象与数字（Little Elephant and Numbers） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/221/B
- **比赛来源**：Codeforces Round 136 (Div. 2) · Problem B（UTC 2012-08-31）
- **难度**：1300
- **标签**：枚举、数位
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给定 $x$，数出 $x$ 的约数 $d$ 中，$d$ 与 $x$ 的十进制表示至少有一个公共数字的个数。

**约束**：$1\le x\le10^9$。

## 2. 示例与观察

官方样例一：

```text
输入：
1

输出：
1
```

官方样例二：

```text
输入：
10

输出：
2
```

**观察**：$x\le10^9$ ⇒ 约数只有千余个；枚举到 $\sqrt x$ 即可，同时得到 $d$ 与 $x/d$。

![枚举约数并查公共数字](../../../images/cf221b_div.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举 $1..x$ 是 $10^9$ 太慢。

### 3.2 核心观察

把 $x$ 的数字放进集合，逐个约数检查是否有数字命中；$d^2=x$ 时只算一次。

### 3.3 算法流程

1. 记录 $x$ 的十进制数字集合。
2. 枚举 $d=1..\lfloor\sqrt x\rfloor$，若整除则检查 $d$ 与 $x/d$。
3. 输出计数。

![样例](../../../images/cf221b_walk.svg)

### 3.4 样例走查

$x=1$：约数 1 ⇒ 1；$x=10$：约数 1、2、5、10，含 1 或 0 的是 1 与 10 ⇒ 2。

## 4. 正确性证明

**引理 1**：每个约数都能由 $d\le\sqrt x$ 的枚举得到。

**证明**：约数成对出现 $d\cdot (x/d)=x$，较小者 $\le\sqrt x$。∎

**引理 2**：检查数字公共性正确。

**证明**：十进制表示逐位判断，集合交集非空即存在公共数字。∎

**定理**：计数正确。

**证明**：由引理 1、2，枚举覆盖全部约数且判定正确。∎

## 5. 复杂度分析

- **时间**：$O(\sqrt x\log x)$。\n- **空间**：$O(1)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    long long x;
    if (scanf("%lld", &x) != 1) return 0;
    string sx = to_string(x);
    bool has[10] = {false};
    for (char c : sx) has[c - '0'] = true;
    auto share = [&](long long d) {
        string sd = to_string(d);
        for (char c : sd) if (has[c - '0']) return true;
        return false;
    };
    int cnt = 0;
    for (long long d = 1; d * d <= x; ++d) {
        if (x % d) continue;
        if (share(d)) ++cnt;
        long long e = x / d;
        if (e != d && share(e)) ++cnt;
    }
    printf("%d\n", cnt);
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    x = int(sys.stdin.read().split()[0])
    hs = set(str(x))
    cnt = 0
    d = 1
    while d * d <= x:
        if x % d == 0:
            if hs & set(str(d)):
                cnt += 1
            e = x // d
            if e != d and hs & set(str(e)):
                cnt += 1
        d += 1
    print(cnt)


main()
```

## 7. 边界情况与易错点

1. **$x$ 是完全平方**：$d=x/d$ 不要重复计数。
2. **$x=1$**：答案是 1。
3. **约数为 1 位数**：也要比较。
4. **$x$ 含 0**：数字集合包含 0。
5. **约数不含任何公共数字**：不计数。

## 8. 验证记录

- **编译环境与命令**：`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/221/B_小象与数字.md`。
- **官方样例**：2 / 2 通过。
- **随机对拍**：与枚举 $1..x$ 全部约数（$x\le2\times10^4$）**250 组**一致。
- **性能**：$x=$ 大素数时 < 1 ms。
- **图片校验**：`cf221b_div.svg`、`cf221b_walk.svg` 通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 221A 小象与函数](https://codeforces.com/problemset/problem/221/A)：同场题目。
- [LeetCode 507 完美数](https://leetcode.cn/problems/perfect-number/)：约数枚举。

**延伸思考**：

1. 若要求公共数字个数 ≥k，统计改一改。
2. 若 $x$ 到 $10^{18}$，需要 Pollard-Rho。
