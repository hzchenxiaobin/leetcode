# Codeforces 158E 电话与最长睡眠 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/158/E
- **比赛来源**：VK Cup 2012 Qualification Round 1 · Problem E（UTC 2012-03-03）
- **难度**：1900
- **标签**：DP、排序
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：一天 $[1,86400]$ 秒，有 $n$ 个来电，第 $i$ 个在时刻 $t_i$（严格递增给出）打来、持续 $d_i$ 秒。Jackson 最多可以**忽略 $k$ 个**来电。若他在忙时来电，来电进入队列，他按"先来先服务"依次接听；空闲时来电必须立刻接。求他今天能拥有的**最长连续睡眠时长**（从 $[1,86400]$ 中任取一段，他在这段里不忙）。

**约束**：$n\le4000$，$k\le n$：$O(nk)$ DP。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3 2
30000 15000
40000 15000
50000 15000

输出：
49999
```

忽略前两个电话 $\Rightarrow$ 只在 50000 有一次通话（15000 秒）$\Rightarrow$ 可睡 $1..49999$ 共 49999 秒 ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
5 1
1 20000
10000 10000
20000 20000
25000 10000
80000 60000
输出：
39999
```

![dp[j] = 处理完前 i 个电话、忽略 j 个后的最早空闲时刻](../../../images/cf158e_dp.svg)

**观察 1（状态）**：由于电话按时间顺序到来、且是队列（FIFO），处理顺序就是输入顺序。定义

$$dp[j]=\text{处理完前 }i\text{ 个电话、共忽略 }j\text{ 个之后，Jackson 最早何时空闲}.$$

**观察 2（转移）**：
- 接第 $i$ 个：`start = max(dp[j], t_i)`，`finish = start + d_i`；
- 忽略第 $i$ 个：`dp[j+1] = min(dp[j+1], dp[j])`。

**观察 3（统计睡眠）**：处理完前 $i$ 个电话、空闲时刻为 $dp$ 时，到下个电话 $t_{i+1}$ 之前的空闲段长度为 $t_{i+1}-dp$（若已无电话，则到 86401 秒为止，长度 $86401-dp$）。

由于对同一 $(i,j)$，越早空闲越有利（支配关系），所以只需保留最小值。

## 3. 解题思路

1. `dp[j]` 初始化：`dp[0]=1`（第 1 秒开始空闲），其余 $+\infty$；
2. 对 $i=1..n$：用 `ndp` 转移（接/忽略），然后对每个 $j$ 用 $t_{i+1}-dp[j]$ 更新答案（$i=n$ 时用 86401）；
3. 输出最大答案。

![样例 1：忽略前两个](../../../images/cf158e_sample.svg)

## 4. 正确性证明

**引理 1（FIFO 即输入顺序）**：Jackson 接听电话的顺序与来电顺序一致。

**证明**：新来电都在队尾，他总取队首（最早来电）；而 $t_i$ 严格递增 ⇒ 输入顺序 = 队首顺序。∎

**引理 2（状态充分）**：给定 $(i,j)$，未来的最优只与"当前最早空闲时刻"有关，且越小越好。

**证明**：后续接听时刻为 $\max(\text{空闲}, t)$，关于"空闲"单调不减；睡眠段长度也是 $t'-\text{空闲}$，关于空闲单调不增。因此更小的空闲时刻在所有后续决策中都不劣（支配）。∎

**引理 3（转移完备）**：$dp$ 的转移覆盖且只覆盖"接/忽略第 $i$ 个电话"两种合法选择。

**证明**：每个电话只能被接或被忽略（且忽略总数 ≤ $k$），两种转移分别对应；接时开始时刻为 $\max(\text{空闲},t_i)$（若空闲更早则等到 $t_i$），结束加 $d_i$ ✓ ∎

**引理 4（睡眠统计正确）**：处理完前 $i$ 个、空闲时刻 $dp$ 之后到下个来电前的空闲长度为 $t_{i+1}-dp$（无来电时为 $86401-dp$）。

**证明**：从 $dp$ 到 $t_{i+1}-1$ 都不忙，共 $t_{i+1}-dp$ 秒 ✓；若没有后续来电，则到 86400 秒，共 $86400-dp+1=86401-dp$ ✓ ∎

**定理**：程序输出最长睡眠时长。

**证明**：任一"忽略集合"对应一条 DP 路径（引理 3），其睡眠段由引理 4 精确统计；由引理 2，对每个 $(i,j)$ 只需保留最早空闲时刻，不会漏掉更优解。故程序答案 ≥ 任意方案、且自身对应一个真实方案 ⇒ 等于最大值。∎

## 5. 复杂度分析

- **时间**：$O(nk)\le1.6\times10^7$，实测 $n=k=4000$ 时 C++ 约 0.025 s。
- **空间**：$O(k)$（滚动数组）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    vector<long long> t(n + 1), d(n + 1);
    for (int i = 1; i <= n; i++) scanf("%lld %lld", &t[i], &d[i]);
    const long long DAY = 86401;                 // 一天的"结束哨兵"（第 86401 秒开始不可睡）
    const long long INF = LLONG_MAX / 4;
    // dp[j] = 处理完前 i 个电话、忽略了 j 个后，最早空闲时刻
    vector<long long> dp(k + 1, INF), ndp(k + 1, INF);
    dp[0] = 1;
    long long ans = 0;
    for (int i = 1; i <= n; i++) {
        fill(ndp.begin(), ndp.end(), INF);
        for (int j = 0; j <= k && j <= i; j++) {
            if (dp[j] >= INF) continue;
            // 接这个电话
            long long start = max(dp[j], t[i]);
            long long finish = start + d[i];
            if (finish < ndp[j]) ndp[j] = finish;
            // 忽略这个电话
            if (j + 1 <= k && dp[j] < ndp[j + 1]) ndp[j + 1] = dp[j];
        }
        dp.swap(ndp);
        // 用"下一个电话到来之前"的空闲段更新答案
        long long nextT = (i < n) ? t[i + 1] : DAY;
        for (int j = 0; j <= k; j++)
            if (dp[j] < INF) ans = max(ans, nextT - dp[j]);
    }
    printf("%lld\n", ans);
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    t = [0] * (n + 1)
    d = [0] * (n + 1)
    p = 2
    for i in range(1, n + 1):
        t[i] = int(data[p]); d[i] = int(data[p + 1]); p += 2
    DAY = 86401
    INF = float("inf")
    dp = [INF] * (k + 1)
    dp[0] = 1
    ans = 0
    for i in range(1, n + 1):
        ndp = [INF] * (k + 1)
        for j in range(0, min(k, i) + 1):
            if dp[j] == INF:
                continue
            start = max(dp[j], t[i])
            finish = start + d[i]
            if finish < ndp[j]:
                ndp[j] = finish
            if j + 1 <= k and dp[j] < ndp[j + 1]:
                ndp[j + 1] = dp[j]
        dp = ndp
        nxt = t[i + 1] if i < n else DAY
        for j in range(0, k + 1):
            if dp[j] < INF:
                ans = max(ans, nxt - dp[j])
    print(ans)


main()
```

## 7. 边界情况与易错点

1. **初始空闲时刻是 1**（第 1 秒），不是 0。
2. **无来电**：$n=0$ 时答案 86400（代码里 $n=0$ 不会进入循环，需要特判——本题 $n\ge1$，但为稳妥可加）。
3. **忽略次数可以少于 $k$**：DP 允许"用不完"。
4. **同一时刻多通电话**：$t_i$ 严格递增，不会出现。
5. **电话超出一天**：$t_i+d_i$ 可以超过 86400，答案截断在 86401 之前（用 $86401-dp$）。
6. **`INF` 不要参与加法**：先判 `dp[j]>=INF`。
7. **队列语义**：接听顺序 = 输入顺序（引理 1），不要按 $t_i+d_i$ 排序。
8. **答案范围**：$0..86400$。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/158/E_电话与最长睡眠.md`
- **官方样例**：$2/2$ 通过（`49999`、`39999`），C++ 与 Python 一致。
- **独立对拍**：另写"枚举所有不超过 $k$ 的忽略集合、按 FIFO 模拟求最长空闲段"的暴力（$n\le6$），对 $200$ 组随机数据（时间在 $[1,200)$ 内互异、时长 $\le30$）比较，全部一致。
- **性能**：$n=k=4000$ 单次约 0.025 s（C++）、3.7 s（Python，建议 PyPy3/C++）。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 158C Cd and pwd commands](https://codeforces.com/problemset/problem/158/C)：同场 C 题。
- [Codeforces 158D Ice Sculptures](https://codeforces.com/problemset/problem/158/D)：同场 D 题。
- [LeetCode 1235. 规划兼职工作](https://leetcode.cn/problems/maximum-profit-in-job-scheduling/)：调度类 DP。

**延伸思考**：

1. **若允许"中途挂断"**：需要另一套状态（当前通话已进行的时长）。
2. **若 $k$ 很大（=n）**：可以忽略全部电话，答案 86400（需特判 $n$ 个电话全忽略后仍无来电）。
3. **若要求"必须睡满某段"**：变成判断可行性（同样 DP）。
