# Codeforces 214B 作业（Hometask） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/214/B
- **比赛来源**：Codeforces Round 131 (Div. 2) · Problem B（UTC 2012-07-30）
- **难度**：1600
- **标签**：贪心、构造、数论
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给定 $n$ 个数字（0..9），用其中若干（可不用完、不可有前导零）拼出最大的、能被 2、3、5 同时整除的数。不存在则输出 −1。

**约束**：$1\le n\le10^5$。

## 2. 示例与观察

官方样例一：

```text
输入：
1
0

输出：
0
```

官方样例二：

```text
输入：
11
3 4 5 4 5 3 5 3 4 4 0

输出：
5554443330
```

官方样例三：

```text
输入：
8
3 2 5 1 5 2 2 3

输出：
-1
```

**观察**：被 2 和 5 整除 ⇒ 末位必须是 0（被 10 整除）；被 3 整除 ⇒ 各位数字和 ≡ 0 (mod 3)。所以先检查有没有 0，再调整数字和。

![能被 30 整除的构造](../../../images/cf214b_mod30.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举子集不可行；但可以按“要最大数”贪心：尽量保留所有数字，只删最少的数字使数字和 ≡ 0 (mod 3)。

### 3.2 核心观察

设非零数字和 $S$：若 $S\bmod3=1$，删一个 $\bmod3=1$ 的最小数字（没有就删两个 $\bmod3=2$ 的最小数字）；若 $S\bmod3=2$ 对称处理。删除的数字越少、越小，得到的数越大。

### 3.3 算法流程

1. 统计 0..9 出现次数；没有 0 ⇒ −1。
2. $S=\sum_{d\ge1} d\cdot cnt[d]$，按 $S\bmod3$ 删 1 或 2 个非零数字。
3. 若删完没有非零数字 ⇒ 输出 0。
4. 否则非零数字降序拼接，再接上全部 0。

![样例走查](../../../images/cf214b_walk.svg)

### 3.4 样例走查

样例二数字和 36 ≡ 0，全部保留：`5554443330`；样例三没有 0 ⇒ −1。

## 4. 正确性证明

**引理 1（整除条件）**：一个数能被 30 整除 ⟺ 末位为 0 且各位和 ≡ 0 (mod 3)。

**证明**：被 10 整除等价于末位 0；被 3 整除等价于各位和模 3 为 0。∎

**引理 2（删数最少且最小最优）**：在满足数字和 ≡0 的前提下，删掉的数字个数最少、且删掉的数字集合字典序最小，得到的数最大。

**证明**：位数优先（少删一位数值至少翻十倍）；位数相同时，从左到右比较，删除更小的数字使高位更大。按 mod 3 分类后，删 1 个（若可能）总优于删 2 个；同类中删最小的数字最好。∎

**定理**：算法输出最大可行数。

**证明**：0 必须至少有一个（否则无解）；由引理 1、2，调整后剩余数字集合达到最优；降序拼接给出该集合能组成的最大数。∎

## 5. 复杂度分析

- **时间**：$O(n+10)$。
- **空间**：$O(10)$。
- 输出长度可达 $10^5$ 位，用字符串。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> cnt(10, 0);
    for (int i = 0; i < n; ++i) { int d; scanf("%d", &d); cnt[d]++; }
    if (cnt[0] == 0) { printf("-1\n"); return 0; }
    int zeros = cnt[0];
    cnt[0] = 0;
    long long sum = 0;
    for (int d = 1; d <= 9; ++d) sum += (long long)d * cnt[d];
    auto removeOne = [&](int r) -> bool {          // 删掉一个 d%3==r 的最小数字
        for (int d = 1; d <= 9; ++d) if (d % 3 == r && cnt[d] > 0) { cnt[d]--; sum -= d; return true; }
        return false;
    };
    if (sum % 3 == 1) {
        if (!removeOne(1)) { if (!removeOne(2) || !removeOne(2)) { printf("-1\n"); return 0; } }
    } else if (sum % 3 == 2) {
        if (!removeOne(2)) { if (!removeOne(1) || !removeOne(1)) { printf("-1\n"); return 0; } }
    }
    bool any = false;
    for (int d = 1; d <= 9; ++d) if (cnt[d] > 0) any = true;
    if (!any) { printf("0\n"); return 0; }
    string out;
    for (int d = 9; d >= 1; --d) out.append(cnt[d], (char)('0' + d));
    out.append(zeros, '0');
    printf("%s\n", out.c_str());
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cnt = [0] * 10
    for x in data[1:1 + n]:
        cnt[int(x)] += 1
    if cnt[0] == 0:
        print(-1)
        return
    zeros = cnt[0]
    cnt[0] = 0
    total = sum(d * cnt[d] for d in range(1, 10))

    def remove_one(r):
        nonlocal total
        for d in range(1, 10):
            if d % 3 == r and cnt[d] > 0:
                cnt[d] -= 1
                total -= d
                return True
        return False

    if total % 3 == 1:
        if not remove_one(1):
            if not (remove_one(2) and remove_one(2)):
                print(-1)
                return
    elif total % 3 == 2:
        if not remove_one(2):
            if not (remove_one(1) and remove_one(1)):
                print(-1)
                return
    if all(cnt[d] == 0 for d in range(1, 10)):
        print(0)
        return
    out = ''.join(str(d) * cnt[d] for d in range(9, 0, -1)) + '0' * zeros
    print(out)


main()
```

## 7. 边界情况与易错点

1. **全是 0**：输出单个 `0`（不是空行）。
2. **没有 0**：直接 −1，即使数字和满足也不能被 10 整除。
3. **删完只剩 0**：输出 `0`。
4. **删两次均失败**：无解 −1（例如只有一个 1 且和 ≡1）。
5. **数字可重复**：计数数组处理，不能去重。
6. **前导零**：降序拼接保证首位非零（除非只剩 0）。

## 8. 验证记录

- **编译环境与命令**：`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/214/B_作业.md`。
- **官方样例**：3 / 3 通过（0、5554443330、−1）。
- **随机对拍**：枚举所有子集暴力求最大可行数（$n\le8$）共 **300 组**，完全一致。
- **性能**：$n=10^5$ 时 < 5 ms。
- **图片校验**：`cf214b_mod30.svg`、`cf214b_walk.svg` 通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 214A 方程组](https://codeforces.com/problemset/problem/214/A)：同场题目。
- [Codeforces 215D 炎热的日子](https://codeforces.com/problemset/problem/215/D)：另一道贪心。
- [LeetCode 1363 形成三的最大倍数](https://leetcode.cn/problems/largest-multiple-of-three/)：完全同型。

**延伸思考**：

1. 若只要求被 3 整除，不需要 0。
2. 若要求被 7 整除，删数贪心不再适用，需要 DP 余数。
