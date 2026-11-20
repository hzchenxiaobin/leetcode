# Codeforces 159B 笔帽配对最优 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/159/B
- **比赛来源**：VK Cup 2012 Qualification Round 2 · Problem B（UTC 2012-03-09）
- **难度**：1100
- **标签**：贪心、排序
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：$n$ 支笔（颜色 $x_i$、直径 $y_i$）、$m$ 个笔帽（颜色 $a_j$、直径 $b_j$）。笔帽只能盖在同直径的笔上；若颜色也相同则称"完美配对"。要求先最大化**配对数**，再在配对数最多的前提下最大化**完美配对数**。输出这两个数。

**约束**：$n,m\le10^5$，颜色与直径 $\le1000$：用二维计数即可。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3 4
1 2
3 4
2 4
5 4
2 4
1 1
1 2

输出：
3 2
```

笔：(1,2)、(3,4)、(2,4)；帽：(5,4)、(2,4)、(1,1)、(1,2)。
按直径 4：笔 2 支（颜色 3、2），帽 2 个（颜色 5、2）⇒ 可配 2 对（受 min(2,2) 限制），其中颜色相同的只有 (2,4) 一支笔对应一个 (2,4) 帽 ⇒ 1 对完美；按直径 2：笔 1 支（1,2），帽 1 个（1,2）⇒ 1 对且完美；直径 1：帽 1 个但无笔 ⇒ 0。
总计配对 $2+1=3$，完美 $1+1=2$ ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
2 2
1 2
2 1
3 4
5 1

输出：
1 0
```

直径 2 的笔 1 支、帽 0 个；直径 1 的笔 1 支、帽 1 个（颜色 5 vs 2，不匹配）⇒ 配对 1、完美 0 ✓

![按直径分组，再按 (颜色,直径) 分组](../../../images/cf159b_match.svg)

**观察**：配对只受直径约束 ⇒ 每个直径独立；完美配对只受 (颜色,直径) 约束 ⇒ 每个 (颜色,直径) 也独立。于是

$$u=\sum_{d}\min\big(\#\text{笔}(d),\#\text{帽}(d)\big),\qquad v=\sum_{c,d}\min\big(\#\text{笔}(c,d),\#\text{帽}(c,d)\big).$$

## 3. 解题思路

1. 统计 `mk[c][d]`、`cp[c][d]`（二维计数），以及按直径的合计 `mkTot[d]`、`cpTot[d]`；
2. $u=\sum_d \min(mkTot[d], cpTot[d])$；
3. $v=\sum_{c,d}\min(mk[c][d],cp[c][d])$。

![样例 1：直径 4 配 2 对（其中 1 对完美），直径 2 配 1 对完美](../../../images/cf159b_sample.svg)

## 4. 正确性证明

**引理 1（配对上限与可达）**：直径 $d$ 上最多能配 $\min(\#\text{笔}(d),\#\text{帽}(d))$ 对，且可达到。

**证明**：每次配对消耗一支笔和一个帽且必须在同直径，故上限显然；按任意顺序把同直径的笔帽配上即可达到（颜色无关）✓ ∎

**引理 2（完美配对上限与可达）**：给定颜色-直径组合 $(c,d)$，其中完美配对最多 $\min(mk[c][d],cp[c][d])$ 对；把所有组合的完美配对加起来是可达的。

**证明**：每个完美配对消耗同 $(c,d)$ 的一笔一帽，故每组上限成立；各组之间互不共享笔帽 ⇒ 同时取到全部上限仍可行（总用量不超过各直径的笔帽总数）✓ ∎

**引理 3（不冲突）**：同时取到引理 1 与引理 2 的上界是可行的，即完美配对不减少总配对数。

**证明**：完美配对本身也是配对；对每个直径，用掉 $\sum_c\min(\cdot)$ 支笔与同样数目的帽，均不超过该直径的笔/帽总数，剩余按任意方式补齐到 $\min$ ⇒ 总数仍为 $\min$ ✓ ∎

**定理**：程序输出的 $u,v$ 是最优的（先最大配对、再最大完美）。

**证明**：由引理 1 得配对数的最大值；由引理 3，达到该最大值时完美配对可以取到引理 2 的上界，而引理 2 是完美配对的绝对上限 ⇒ 该值就是"配对数最大前提下的最大完美数"✓ ∎

## 5. 复杂度分析

- **时间**：统计 $O(n+m)$，二维求和 $O(1000^2)=10^6$，实测 < 10 ms。
- **空间**：$O(1000^2)$ 的计数表 ≈ 4 MB。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    const int MAXC = 1001;
    // mk[c][d]、cp[c][d]
    vector<vector<int>> mk(MAXC, vector<int>(MAXC, 0)), cp(MAXC, vector<int>(MAXC, 0));
    vector<int> mkTot(MAXC, 0), cpTot(MAXC, 0);
    for (int i = 0; i < n; i++) {
        int x, y; scanf("%d %d", &x, &y);
        mk[x][y]++; mkTot[y]++;
    }
    for (int j = 0; j < m; j++) {
        int a, b; scanf("%d %d", &a, &b);
        cp[a][b]++; cpTot[b]++;
    }
    long long u = 0, v = 0;
    for (int d = 1; d < MAXC; d++) u += min(mkTot[d], cpTot[d]);
    for (int c = 1; c < MAXC; c++)
        for (int d = 1; d < MAXC; d++) v += min(mk[c][d], cp[c][d]);
    printf("%lld %lld\n", u, v);
    return 0;
}
```

### Python3

```python
import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    p = 2
    mk = Counter()
    mk_tot = Counter()
    for _ in range(n):
        x = int(data[p]); y = int(data[p + 1]); p += 2
        mk[(x, y)] += 1
        mk_tot[y] += 1
    cp = Counter()
    cp_tot = Counter()
    for _ in range(m):
        a = int(data[p]); b = int(data[p + 1]); p += 2
        cp[(a, b)] += 1
        cp_tot[b] += 1
    u = sum(min(mk_tot[d], cp_tot[d]) for d in mk_tot.keys() | cp_tot.keys())
    v = sum(min(mk[k], cp[k]) for k in mk.keys() | cp.keys())
    print(u, v)


main()
```

## 7. 边界情况与易错点

1. **先最大化配对数**：不能只顾完美配对而少配对（引理 3 保证两者不冲突，但实现顺序要正确）。
2. **直径必须相等**：颜色相同但直径不同不能配。
3. **计数用 `long long`**：结果 ≤ $10^5$，`int` 也够，但求和用 `long long` 更稳。
4. **颜色/直径范围**：$1..1000$，二维表大小 $1001^2$。
5. **重复元素**：用计数而非集合，重复的笔/帽各算一次。
6. **$n$ 或 $m$ 为 0**：题面 $n,m\ge1$，代码也能处理。
7. **输出格式**：两个数空格分隔。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/159/B_笔帽配对最优.md`
- **官方样例**：$2/2$ 通过（`3 2`、`1 0`），C++ 与 Python 一致。
- **独立对拍**：另写"按直径、按 (颜色,直径) 分别取 min 求和"的独立实现（不同数据结构），对 $200$ 组随机数据（颜色/直径 $\le3$、$n,m\le6$）比较，全部一致。
- **性能**：$n=m=10^5$ 单次 < 10 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 159A Friends or Not](https://codeforces.com/problemset/problem/159/A)：同场 A 题。
- [Codeforces 159C String Manipulation 1.0](https://codeforces.com/problemset/problem/159/C)：同场 C 题。
- [LeetCode 455. 分发饼干](https://leetcode.cn/problems/assign-cookies/)：匹配类贪心。

**延伸思考**：

1. **若要求"完美配对优先"**（先最大完美）：两个量会互换角色。
2. **若一个笔帽能配多支笔**：变成流量问题。
3. **若值域到 $10^9$**：改用哈希表计数。
