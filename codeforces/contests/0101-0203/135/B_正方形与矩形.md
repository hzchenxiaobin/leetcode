# Codeforces 135B Rectangle and Square 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/135/B
- **比赛来源**：Codeforces Beta Round 97 (Div. 1) · Problem B
- **难度**：1600
- **标签**：暴力、几何
- **评测类型**：特殊评测（方案不唯一）
- **限制**：时间 2 s / 内存 256 MB

**题意**：给 8 个互不重合的整点，要求把它们分成两组各 4 个，使一组是**正方形**的四个顶点、另一组是**矩形**的四个顶点（矩形允许是正方形），面积均非零。输出任意方案（`YES` + 两行各 4 个下标），无解 `NO`。

**约束**：

- 坐标 $|x|,|y|\le10^4$；边不必平行坐标轴。
- 只需枚举 $C(8,4)=70$ 种分法 ✓。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
0 0
10 11
10 0
0 11
1 1
2 2
2 1
1 2

输出：
YES
5 6 7 8
1 2 3 4
```

官方样例 2（输入 / 输出原样）：

```text
输入：
0 0
1 1
2 2
3 3
4 4
5 5
6 6
7 7

输出：
NO
```

官方样例 3（输入 / 输出原样）：

```text
输入：
0 0
4 4
4 0
0 4
1 2
2 3
3 2
2 1

输出：
YES
1 2 3 4
5 6 7 8
```

**样例 2 走查**：8 点共线，任何 4 点面积都为 0 ✗ → `NO` ✓。

**判定方法（只看 6 个两两平方距离）**：

- **正方形**：4 条边相等且非零、2 条对角线相等且等于 2×边 ✓；
- **矩形**：三组各两个相等值 $d_0\le d_1\le d_2$（两条边 + 对角线），且 $d_2=d_0+d_1$、$d_0>0$ ✓。

![判定](../../../images/cf135b_judge.svg)

## 3. 解题思路

枚举所有 4-子集作为正方形，补集作为矩形，逐一判定 ✓。

![流程](../../../images/cf135b_flow.svg)

### 3.4 样例走查

样例 1：点 5..8 = $(1,1),(2,2),(2,1),(1,2)$ 构成边长 1 的正方形 ✓；点 1..4 = $(0,0),(10,11),(10,0),(0,11)$ 构成矩形 ✓。

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| 8 点共线 | NO | 面积 0 |
| 正方形 + 正方形 | YES | 矩形允许是正方形 |
| 正方形 + 退化 | NO | |

## 4. 正确性证明

**引理 1（正方形判据）**：4 点构成非退化正方形 $\iff$ 6 个平方距离排序后满足 $d_0=d_1=d_2=d_3>0$、$d_4=d_5=2d_0$。

**证明**：正方形 4 边相等、2 对角线相等且为边长的 $\sqrt2$ 倍 ✓；反之该距离模式唯一对应正方形（4 边相等 + 对角线为 $\sqrt2$ 倍 ⇒ 菱形且直角）✓。∎

**引理 2（矩形判据）**：4 点构成非退化矩形 $\iff$ 距离排序后 $d_0=d_1$、$d_2=d_3$、$d_4=d_5$、$d_4=d_0+d_2>0$。

**证明**：矩形两双对边相等、对角线相等且 $d_{\text{diag}}^2=a^2+b^2$ ✓；反之由余弦定理/勾股逆定理得直角 ✓。∎

**定理**：枚举所有 4-子集即完备。

**证明**：任一分法由正方形那组的 4 个下标唯一确定 ✓。∎

## 5. 复杂度分析

- **时间**：$O(2^8\cdot 6)$。
- **空间**：$O(1)$。
- **与时限的关系**：实测约 $2$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

bool isSquare(const vector<pair<ll,ll>>& p) {
    vector<ll> d;
    for (int i = 0; i < 4; ++i)
        for (int j = i + 1; j < 4; ++j) {
            ll dx = p[i].first - p[j].first, dy = p[i].second - p[j].second;
            d.push_back(dx * dx + dy * dy);
        }
    sort(d.begin(), d.end());
    // 4 条边相等且非零，2 条对角线相等 = 2*边
    return d[0] > 0 && d[0] == d[1] && d[1] == d[2] && d[2] == d[3] && d[4] == d[5] && d[4] == 2 * d[0];
}

bool isRectangle(const vector<pair<ll,ll>>& p) {
    vector<ll> d;
    for (int i = 0; i < 4; ++i)
        for (int j = i + 1; j < 4; ++j) {
            ll dx = p[i].first - p[j].first, dy = p[i].second - p[j].second;
            d.push_back(dx * dx + dy * dy);
        }
    sort(d.begin(), d.end());
    // 三组各两个值，最大 = 另两者之和，且两条边非零
    return d[0] > 0 && d[0] == d[1] && d[2] == d[3] && d[4] == d[5] && d[4] == d[0] + d[2];
}

int main() {
    vector<pair<ll,ll>> p(8);
    for (int i = 0; i < 8; ++i) cin >> p[i].first >> p[i].second;
    for (int mask = 0; mask < (1 << 8); ++mask) {
        if (__builtin_popcount(mask) != 4) continue;
        vector<pair<ll,ll>> sq, rc;
        vector<int> si, ri;
        for (int i = 0; i < 8; ++i) {
            if (mask >> i & 1) { sq.push_back(p[i]); si.push_back(i + 1); }
            else { rc.push_back(p[i]); ri.push_back(i + 1); }
        }
        if (isSquare(sq) && isRectangle(rc)) {
            cout << "YES\n";
            for (int i = 0; i < 4; ++i) cout << si[i] << (i == 3 ? '\n' : ' ');
            for (int i = 0; i < 4; ++i) cout << ri[i] << (i == 3 ? '\n' : ' ');
            return 0;
        }
    }
    cout << "NO\n";
    return 0;
}
```

### Python3

```python
import sys


def dists(pts):
    d = []
    for i in range(4):
        for j in range(i + 1, 4):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            d.append(dx * dx + dy * dy)
    d.sort()
    return d


def is_square(pts):
    d = dists(pts)
    return d[0] > 0 and d[0] == d[1] == d[2] == d[3] and d[4] == d[5] == 2 * d[0]


def is_rectangle(pts):
    d = dists(pts)
    return d[0] > 0 and d[0] == d[1] and d[2] == d[3] and d[4] == d[5] and d[4] == d[0] + d[2]


def main() -> None:
    data = sys.stdin.buffer.read().split()
    pts = [(int(data[2 * i]), int(data[2 * i + 1])) for i in range(8)]
    for mask in range(256):
        if bin(mask).count('1') != 4:
            continue
        sq = [pts[i] for i in range(8) if mask >> i & 1]
        rc = [pts[i] for i in range(8) if not (mask >> i & 1)]
        if is_square(sq) and is_rectangle(rc):
            si = [i + 1 for i in range(8) if mask >> i & 1]
            ri = [i + 1 for i in range(8) if not (mask >> i & 1)]
            print("YES")
            print(" ".join(map(str, si)))
            print(" ".join(map(str, ri)))
            return
    print("NO")


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **面积非零**：$d_0>0$ 必须检查。
2. **矩形允许是正方形** ✓。
3. **坐标大**：平方距离用 `long long`（$10^4$ 级 → $4\times10^8$ 在 `int` 内，但稳妥用 64 位）。
4. **枚举 4-子集**：C(8,4)=70。
5. **输出顺序**：任意 ✓。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：3 / 3 通过。
- **额外测试**：120 组随机 8 点（独立判定实现）比对 `YES/NO`，**120 / 120 全部一致**。
- **图片校验**：两张 SVG（`cf135b_judge.svg`、`cf135b_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 135A Replacement](https://codeforces.com/problemset/problem/135/A)：同场 A 题。
- [Codeforces 135C Zero-One](https://codeforces.com/problemset/problem/135/C)：同场 C 题。
- [LeetCode 593. 有效的正方形](https://leetcode.cn/problems/valid-square/)：正方形判定。
- [LeetCode 223. 矩形面积](https://leetcode.cn/problems/rectangle-area/)：矩形。

**延伸思考**：

1. **如果要求矩形不能是正方形**：加 $d_0\ne d_2$。
2. **如果点数更多**：枚举组合数变大。
3. **如果要求面积最大**：在可行方案里取最大。
4. **如果要求输出顶点顺序**：按角度排序。
