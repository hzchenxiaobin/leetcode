# Codeforces 165A 超级中心点 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/165/A
- **比赛来源**：Codeforces Round 112 (Div. 2) · Problem A（UTC 2012-03-16）
- **难度**：1000
- **标签**：实现
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个互不相同的整点。若点 $(x,y)$ 在集合中存在同一水平线上的左邻（$x'<x$）与右邻（$x'>x$）、以及同一竖直线上的下邻（$y'<y$）与上邻（$y'>y$），称它"超级中心"。求超级中心的个数。

**约束**：$n\le200$：$O(n^2)$ 直接判。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
8
1 1
4 2
3 1
1 2
0 2
0 1
1 0
1 3
输出：
2
```

$(1,1)$ 左右有 $(0,1),(3,1)$，上下有 $(1,0),(1,2)$ ✓；$(1,2)$ 左右有 $(0,2),(4,2)$，上下有 $(1,1),(1,3)$ ✓ ⇒ 2

官方样例 2（输入 / 输出原样）：

```text
输入：
5
0 0
0 1
1 0
0 -1
-1 0
输出：
1
```

只有原点四个方向各有点 ✓

![四个方向各至少要有一个点](../../../images/cf165a_dirs.svg)

**观察**：只需对每个点扫一遍所有点，记录四个方向是否存在。

## 3. 解题思路

对每个点 $i$，遍历所有点 $j$：若 $y_j=y_i$ 且 $x_j<x_i$ 则 L；$x_j>x_i$ 则 R；若 $x_j=x_i$ 且 $y_j<y_i$ 则 D、$y_j>y_i$ 则 U。四者齐备则计数 +1。

![样例 1 的两个超级中心](../../../images/cf165a_sample.svg)

## 4. 正确性证明

**引理**：点 $i$ 是超级中心 ⟺ 存在 $j$ 满足 $y_j=y_i\wedge x_j<x_i$，存在 $j'$ 满足 $y_{j'}=y_i\wedge x_{j'}>x_i$，以及类似的上下两个。

**证明**：题面对四个"邻居"的定义正是"同行且在左/右、同列且在下/上"，逐一对应 ✓ ∎

**定理**：程序输出正确。

**证明**：程序对每个点精确检查引理中的四个存在量词，四者同时成立才计数 ⇒ 输出等于超级中心数 ✓ ∎

## 5. 复杂度分析

- **时间**：$O(n^2)\le4\times10^4$，可忽略（实测 2 ms）。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> x(n), y(n);
    for (int i = 0; i < n; i++) scanf("%d %d", &x[i], &y[i]);
    int ans = 0;
    for (int i = 0; i < n; i++) {
        bool L = false, R = false, U = false, D = false;
        for (int j = 0; j < n; j++) {
            if (x[j] == x[i]) {
                if (y[j] < y[i]) D = true;
                if (y[j] > y[i]) U = true;
            }
            if (y[j] == y[i]) {
                if (x[j] < x[i]) L = true;
                if (x[j] > x[i]) R = true;
            }
        }
        if (L && R && U && D) ans++;
    }
    printf("%d\n", ans);
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    pts = [(int(data[1 + 2 * i]), int(data[2 + 2 * i])) for i in range(n)]
    ans = 0
    for i, (x, y) in enumerate(pts):
        L = R = U = D = False
        for (a, b) in pts:
            if a == x:
                if b < y: D = True
                if b > y: U = True
            if b == y:
                if a < x: L = True
                if a > x: R = True
        if L and R and U and D:
            ans += 1
    print(ans)


main()
```

## 7. 边界情况与易错点

1. **同行/同列才算邻居**：斜方向不算。
2. **点互不相同**：无需去重（题面保证）。
3. **坐标可为负**：不要用数组下标代替比较。
4. **$n=1$**：答案 0。
5. **四个方向都要**：缺一不可。
6. **判断顺序**：注意"同行"判 L/R、"同列"判 D/U。
7. **输出**：单个整数。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/165/A_超级中心点.md`
- **官方样例**：$2/2$ 通过。
- **独立对拍**：另写"用集合查同行/同列极值"的独立实现，对 $200$ 组随机点集（$n\le10$、坐标 $[-2,2]$）比较，全部一致。
- **性能**：$n=200$ 单次约 2 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 165B Burning Midnight Oil](https://codeforces.com/problemset/problem/165/B)：同场 B 题。
- [Codeforces 165C Another Problem on Strings](https://codeforces.com/problemset/problem/165/C)：同场 C 题。
- [LeetCode 149. 直线上最多的点数](https://leetcode.cn/problems/max-points-on-a-line/)：点集几何。

**延伸思考**：

1. **若要求 8 个方向**：把斜方向也纳入。
2. **若要求最近邻**：需要排序/哈希。
3. **若 $n$ 到 $10^5$**：按 x、y 分组统计即可 $O(n\log n)$。
