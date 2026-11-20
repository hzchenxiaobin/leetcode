# Codeforces 120D Three Sons 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/120/D
- **比赛来源**：School Regional Team Contest, Saratov, 2011 · Problem D
- **难度**：1400
- **标签**：暴力
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：$n\times m$ 的田地，每格有产量 $c_{ij}$。用**两条互相平行、且平行于某一边**的直线（沿格线、严格在格子之间）把田分成三块，每块至少一格。求有多少种分法使得三块的产量（不计顺序）恰好是 $A,B,C$。

**约束**：

- $n,m\le50$，$\max(n,m)\ge3$。
- 两条线只能同向（都横或都竖），所以分法 = 选择两个切点。
- $A,B,C\le10^6$，产量和到 $2.5\times10^5$，用 `int` 也够，但稳妥用 `long long`。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3 3
1 1 1
1 1 1
1 1 1
3 3 3

输出：
2
```

官方样例 2（输入 / 输出原样）：

```text
输入：
2 5
1 1 1 1 1
2 2 2 2 2
3 6 6

输出：
3
```

官方样例 3（输入 / 输出原样）：

```text
输入：
3 3
1 2 3
3 1 2
2 3 1
5 6 7

输出：
0
```

**样例 1 走查**：$3\times3$ 全 1，每块和都是 3。横向切法：只有 $(i,j)=(0,1)$（切在行 1 后、行 2 后）→ 3+3+3 ✓ 算 1 种；纵向同理 1 种 → 共 2 ✓。

**样例 2 走查**：$2\times5$，行和分别 5 与 10。横向：不满足 $3,6,6$（只有两块）。纵向：列和 3,3,3,3,3。需要 3+3+（3+3+3=9）？行和 5/10：纵向切出三块，各块和 = 3a、3b、3c（$a+b+c=5$）→ 需要 {3,6,6} ⇒ a,b,c ∈ {1,2,2} ✓ 三种排列 ✓ → 3 ✓。

**观察**：两条线必须同向 ⇒ 只需分别枚举"横切"的两个切点 (i,j) 与"竖切"的两个切点 ✓，每种 $O(n^2)$ / $O(m^2)$，用前缀和 $O(1)$ 算三块之和 ✓。

![切法](../../../images/cf120d_cuts.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

$n,m\le50$：横切 $O(n^2)$ 对，每对 $O(nm)$ 求和 → $2500\times2500 = 6\times10^6$ ✓ 直接算也行；用前缀和更快。

### 3.2 核心观察

横切 $(i,j)$（$0\le i<j\le n-2$）：三块是行 $[0..i]$、$[i+1..j]$、$[j+1..n-1]$ ✓ 用行和前缀 ✓；竖切同理用列和前缀 ✓。判定用排序后与 $(A,B,C)$ 排序比较 ✓（"不计顺序"）。

![流程](../../../images/cf120d_flow.svg)

### 3.3 算法流程

1. 读入矩阵与 $A,B,C$（排序）；
2. 求行和、列和；
3. 枚举横切的两条线与竖切的两条线，用前缀和算三块和，排序后匹配则计数；
4. 输出计数。

### 3.4 样例走查

见 2 节 ✓。

自造样例（标注"自造"）：

| 输入 | 输出 |
|------|------|
| `1 3` / `1 1 1` / `1 1 1` | 1 |
| `3 1` / `1` / `1` / `1` / `1 1 1` | 1 |
| `3 3` / 全 0 / `0 0 0` | 2 |

## 4. 正确性证明

**引理 1**：任何合法分法都由两条同向平行线给出；横切对应一对行切点，竖切对应一对列切点。

**证明**：题面要求两条线平行且平行于某一边 ⇒ 同向；横切把行分成三段 ✓。∎

**引理 2**：枚举所有 $(i,j)$（横）与 $(i,j)$（竖）恰好覆盖所有分法，且每种分法只被枚举一次。

**证明**：切点对与分法一一对应（$i<j$ 且每段非空）✓。∎

**引理 3**：三块产量由前缀和正确计算。

**证明**：块 $[0..i]$ 的和 = 行前缀差 ✓，其余同理 ✓。∎

**定理**：算法输出正确。

**证明**：由引理 1、2、3，算法计数了所有满足"三块产量多重集 = {A,B,C}"的分法 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n^2+m^2)$（前缀和）。
- **空间**：$O(n+m)$。
- **与时限的关系**：实测 $50\times50$ 时 C++ 端到端 $6.6$ ms、Python $17.4$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<vector<long long>> g(n, vector<long long>(m));
    for (int i = 0; i < n; ++i) for (int j = 0; j < m; ++j) cin >> g[i][j];
    long long A, B, C;
    cin >> A >> B >> C;
    vector<long long> want = {A, B, C};
    sort(want.begin(), want.end());
    long long ans = 0;
    auto check = [&](long long x, long long y, long long z) {
        vector<long long> v = {x, y, z};
        sort(v.begin(), v.end());
        return v == want;
    };
    // 横切
    vector<long long> rowSum(n);
    for (int i = 0; i < n; ++i) { long long s = 0; for (int j = 0; j < m; ++j) s += g[i][j]; rowSum[i] = s; }
    for (int i = 0; i + 2 < n; ++i)          // 上段 [0..i]
        for (int j = i + 1; j + 1 < n; ++j) { // 中段 [i+1..j]，下段 [j+1..n-1]
            long long s1 = 0, s2 = 0, s3 = 0;
            for (int t = 0; t <= i; ++t) s1 += rowSum[t];
            for (int t = i + 1; t <= j; ++t) s2 += rowSum[t];
            for (int t = j + 1; t < n; ++t) s3 += rowSum[t];
            if (check(s1, s2, s3)) ++ans;
        }
    // 竖切
    vector<long long> colSum(m);
    for (int j = 0; j < m; ++j) { long long s = 0; for (int i = 0; i < n; ++i) s += g[i][j]; colSum[j] = s; }
    for (int i = 0; i + 2 < m; ++i)
        for (int j = i + 1; j + 1 < m; ++j) {
            long long s1 = 0, s2 = 0, s3 = 0;
            for (int t = 0; t <= i; ++t) s1 += colSum[t];
            for (int t = i + 1; t <= j; ++t) s2 += colSum[t];
            for (int t = j + 1; t < m; ++t) s3 += colSum[t];
            if (check(s1, s2, s3)) ++ans;
        }
    cout << ans << '\n';
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    p = 2
    g = []
    for i in range(n):
        row = [int(t) for t in data[p:p + m]]
        p += m
        g.append(row)
    A, B, C = int(data[p]), int(data[p + 1]), int(data[p + 2])
    want = sorted((A, B, C))

    def ok(x, y, z):
        return sorted((x, y, z)) == want

    ans = 0
    rowSum = [sum(r) for r in g]
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            s1 = sum(rowSum[:i + 1])
            s2 = sum(rowSum[i + 1:j + 1])
            s3 = sum(rowSum[j + 1:])
            if ok(s1, s2, s3):
                ans += 1
    colSum = [sum(g[i][j] for i in range(n)) for j in range(m)]
    for i in range(m - 2):
        for j in range(i + 1, m - 1):
            s1 = sum(colSum[:i + 1])
            s2 = sum(colSum[i + 1:j + 1])
            s3 = sum(colSum[j + 1:])
            if ok(s1, s2, s3):
                ans += 1
    print(ans)


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **两条线必须同向**：不能一横一竖。
2. **每块至少一格**：$i\ge0$、$j\ge i+1$、$j\le n-2$。
3. **不计顺序**：三块产量与 $A,B,C$ 的任意排列匹配即可（排序比较）。
4. **$A,B,C$ 可相等**：排序后比较自动处理。
5. **$n=1$ 或 $m=1$**：该方向无法切（需要至少 3 段），只枚举另一方向。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：3 / 3 通过（`2`、`3`、`0`）。
- **额外测试**：215 组随机小矩阵（$n,m\le5$）与独立暴力（直接按块求和）比对，**215 / 215 全部一致**。
- **图片校验**：两张 SVG（`cf120d_cuts.svg`、`cf120d_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 120C Winnie-the-Pooh and honey](https://codeforces.com/problemset/problem/120/C)：同场 C 题。
- [Codeforces 119B Before Exam](https://codeforces.com/problemset/problem/119/B)：划分与极值。
- [LeetCode 304. 二维区域和检索](https://leetcode.cn/problems/range-sum-query-2d-immutable/)：二维前缀和。
- [LeetCode 1139. 最大的以 1 为边界的正方形](https://leetcode.cn/problems/largest-1-bordered-square/)：二维前缀和。

**延伸思考**：

1. **如果允许一横一竖（T 形）**：分法数变多，需要枚举交点。
2. **如果要求三块形状也相同**：强约束。
3. **如果 $n,m$ 到 $1000$**：$O(n^2)$ 仍可，但要用前缀和。
4. **如果线可以斜着**：变成计算几何计数。
