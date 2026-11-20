# Codeforces 157B 同心圆红区面积 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/157/B
- **比赛来源**：Codeforces Round 110 (Div. 2) · Problem B（UTC 2012-02-29）
- **难度**：1000
- **标签**：几何、排序
- **评测类型**：浮点（误差 $\le10^{-4}$）
- **限制**：时间 2 s / 内存 256 MB

**题意**：平面上一组同心圆，把平面分成若干环带；相邻环带颜色交替（红/蓝），且**最外层（所有圆之外）是蓝色**。给定各圆半径（互不相同），求红色部分总面积。

**约束**：$n\le100$，$r_i\le1000$：排序后从外向内交替累加即可。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
1
1

输出：
3.1415926536
```

只有半径 1 的圆：外部蓝、内部（半径 1 以内）红 ⇒ $\pi$ ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
3
1 4 2

输出：
40.8407044967
```

排序 $1,2,4$：外部蓝；(2,4] 红：$\pi(16-4)=12\pi$；(1,2] 蓝；(0,1] 红：$\pi\cdot1$。合计 $13\pi=40.8407$ ✓

![从最外层向内交替上色](../../../images/cf157b_rings.svg)

**观察**：颜色只由"从外数第几层"的奇偶决定。把半径升序排列 $r_1<\cdots<r_n$，则环带 $(r_{i-1},r_i]$ 的颜色为红 ⟺ 从外数它是第 $n-i+1$ 层，即 $(n-i)$ 为偶数。面积 $\pi(r_i^2-r_{i-1}^2)$。

## 3. 解题思路

1. 半径升序排序；
2. 从 $i=n$ 到 $1$：若 $(n-i)$ 为偶数（即从外数奇数层），累加 $\pi(r_i^2-r_{i-1}^2)$（$r_0=0$）；
3. 输出（保留 10 位小数）。

为避免精度损失，先在整数上累加"平方差之和"，最后再乘 $\pi$。

![样例 2：13π](../../../images/cf157b_sample.svg)

## 4. 正确性证明

**引理 1（环带划分）**：按半径升序，平面被分成 $n+1$ 个区域：$(r_n,\infty)$ 与 $(r_{i-1},r_i]$（$i=1..n$，$r_0=0$），颜色相邻交替。

**证明**：同心圆两两不交，半径把平面按到圆心的距离分层 ⇒ 每个区域恰是一个环带（或外部）。题面规定相邻环带异色且最外层为蓝 ⇒ 由外向内交替确定唯一颜色。∎

**引理 2（颜色公式）**：环带 $(r_{i-1},r_i]$ 为红 ⟺ $n-i$ 为偶数。

**证明**：从外数，$(r_n,\infty)$ 是第 1 层（蓝），$(r_{n-1},r_n]$ 是第 2 层（红），……，$(r_{i-1},r_i]$ 是第 $n-i+2$ 层。红 ⟺ 层号偶数 ⟺ $n-i+2$ 偶 ⟺ $n-i$ 偶。∎

**引理 3（面积）**：环带 $(r_{i-1},r_i]$ 的面积为 $\pi(r_i^2-r_{i-1}^2)$。

**证明**：圆环面积 = 外圆面积 − 内圆面积 ✓ ∎

**定理**：程序输出红色部分总面积。

**证明**：由引理 1–3，红色总面积 $=\sum_{i:\ n-i\ \text{偶}}\pi(r_i^2-r_{i-1}^2)$，程序正是按此累加（先整数求和再乘 $\pi$，不引入额外误差）。∎

## 5. 复杂度分析

- **时间**：排序 $O(n\log n)$ + 线性累加；实测 < 3 ms。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> r(n);
    for (int i = 0; i < n; i++) scanf("%d", &r[i]);
    sort(r.begin(), r.end());
    long long area = 0;                      // 用和表示，最后乘 π
    for (int i = n - 1; i >= 0; i--) {
        long long outer = 1LL * r[i] * r[i];
        long long inner = (i > 0) ? 1LL * r[i - 1] * r[i - 1] : 0;
        // 最外层圆环 (r[n-2], r[n-1]] 是红色，向内交替
        if ((n - 1 - i) % 2 == 0) area += outer - inner;
    }
    printf("%.10f\n", (double)area * acos(-1.0));
    return 0;
}
```

### Python3

```python
import sys
import math


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    r = sorted(int(x) for x in data[1:1 + n])
    area = 0
    for i in range(n - 1, -1, -1):
        outer = r[i] * r[i]
        inner = r[i - 1] * r[i - 1] if i > 0 else 0
        if (n - 1 - i) % 2 == 0:
            area += outer - inner
    print("%.10f" % (area * math.pi))


main()
```

## 7. 边界情况与易错点

1. **最外层是蓝**：所以最大的环带 $(r_{n-1},r_n]$ 是红色，别搞反。
2. **$n=1$**：整个圆盘是红色 ⇒ $\pi r^2$。
3. **排序**：输入半径无序，必须先排序。
4. **精度**：先整数累加再乘 $\pi$；输出 10 位小数足够。
5. **半径互不相同**：题面保证，无需去重。
6. **$\pi$ 的取值**：用 `acos(-1.0)` / `math.pi`。
7. **奇偶判断**：用 $(n-1-i)\%2$（从外数第几层）而不是 $i$。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/157/B_同心圆红区面积.md`
- **官方样例**：$2/2$ 通过（`3.1415926536`、`40.8407044967`），C++ 与 Python 一致。
- **独立对拍**：另写"降序排列后从外层 idx=0 开始、偶数 idx 为红"的独立实现，对 $200$ 组随机半径（$n\le8$）比较，误差 $<10^{-6}$，全部一致。
- **性能**：$n=100$ 单次 < 3 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 157A Game Outcome](https://codeforces.com/problemset/problem/157/A)：同场 A 题。
- [LeetCode 836. 矩形重叠](https://leetcode.cn/problems/rectangle-overlap/)：几何基础。
- [Codeforces 158D Ice Sculptures](https://codeforces.com/problemset/problem/158/D)：同一时段的几何/枚举题。

**延伸思考**：

1. **若最外层是红色**：整体奇偶反转。
2. **若给的是直径**：半径取一半再套公式。
3. **若圆不同心**：面积变成圆交/并问题，难度陡增。
