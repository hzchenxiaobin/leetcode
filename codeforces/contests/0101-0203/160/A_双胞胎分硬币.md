# Codeforces 160A 双胞胎分硬币 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/160/A
- **比赛来源**：Codeforces Round 111 (Div. 2) · Problem A（UTC 2012-03-06）
- **难度**：900
- **标签**：贪心、排序
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 枚硬币，要拿走其中一部分，使得拿走的金额**严格大于**剩下的金额，并让拿走的硬币**枚数最少**。求最少枚数。

**约束**：$n\le100$，面值 $\le100$：排序后从大到小取即可。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
2
3 3

输出：
2
```

总额 6，需要 $>3$：拿一枚 3 只有 3（不严格大于 3），拿两枚得 6 ✓ ⇒ 2

官方样例 2（输入 / 输出原样）：

```text
输入：
3
2 1 2

输出：
2
```

总额 5，需要 $>2.5$：拿 2+2=4 ✓ ⇒ 2

![从大到小取，直到超过一半](../../../images/cf160a_half.svg)

**观察**：枚数最少 ⇒ 每枚尽量大 ⇒ 从大到小取；条件是 $\text{取走}>\text{剩余}$，即 $2\cdot\text{取走}>\text{总额}$。

## 3. 解题思路

1. 求总额 $S$，把硬币降序排序；
2. 依次累加，直到 `2*sum > S`，输出已取枚数。

![样例 1：拿 3+3 才严格过半](../../../images/cf160a_sample.svg)

## 4. 正确性证明

**引理 1（取 $k$ 枚的最大金额）**：取 $k$ 枚能取得的金额上限是"最大的 $k$ 枚之和"。

**证明**：任取 $k$ 枚，其和不超过排序后前 $k$ 大之和（可逐位交换论证）∎

**引理 2（单调性）**：若取 $k$ 枚能达到严格过半，则取 $k+1$ 枚也能（面值为正）。

**证明**：金额只增不减，$2\cdot\text{sum}>S$ 保持 ✓ ∎

**定理**：程序输出的枚数最小。

**证明**：由引理 1，若最少的可行枚数为 $k^\ast$，则前 $k^\ast$ 大之和必严格过半（否则任何 $k^\ast$ 枚都不行，矛盾）。程序按降序累加，第一次满足 `2*sum>S` 的下标就是 $k^\ast$；由引理 2 更小的 $k$ 都不可行 ⇒ 输出最小 ✓ ∎

## 5. 复杂度分析

- **时间**：排序 $O(n\log n)$ + 线性扫描，实测 < 2 ms。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    int total = 0;
    for (int i = 0; i < n; i++) { scanf("%d", &a[i]); total += a[i]; }
    sort(a.begin(), a.end(), greater<int>());
    int sum = 0, cnt = 0;
    for (int i = 0; i < n && sum * 2 <= total; i++) { sum += a[i]; cnt++; }
    printf("%d\n", cnt);
    return 0;
}
```

### Python3

```python
import sys
def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = sorted((int(x) for x in data[1:1+n]), reverse=True)
    total = sum(a)
    s = cnt = 0
    for x in a:
        if s * 2 > total:
            break
        s += x
        cnt += 1
    print(cnt)
main()
```

## 7. 边界情况与易错点

1. **严格大于**：$2\cdot\text{sum}>S$，不能写成 $\ge$（样例 1）。
2. **$n=1$**：拿 1 枚 ⇒ 1。
3. **全相等**：需要拿超过一半的枚数。
4. **面值为正**：保证"多拿不吃亏"。
5. **整数运算**：用 `2*sum` 避免浮点。
6. **排序方向**：降序，别升序。
7. **输出**：单个整数。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/160/A_双胞胎分硬币.md`
- **官方样例**：$2/2$ 通过（`2`、`2`），C++ 与 Python 一致。
- **独立对拍**：另写"枚举所有 $2^n$ 子集、取金额过半且枚数最少"的暴力，对 $200$ 组随机数据（$n\le10$）比较，全部一致。
- **性能**：$n=100$ 单次 < 2 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 160B Unlucky Ticket](https://codeforces.com/problemset/problem/160/B)：同场 B 题。
- [Codeforces 160C Find Pair](https://codeforces.com/problemset/problem/160/C)：同场 C 题。
- [LeetCode 561. 数组拆分](https://leetcode.cn/problems/array-partition/)：排序贪心。

**延伸思考**：

1. **若要求"拿走不超过一半枚数且金额最大"**：变成背包。
2. **若面值可为负**：贪心失效。
3. **若两人轮流拿**：变成博弈。
