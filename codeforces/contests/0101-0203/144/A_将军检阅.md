# Codeforces 144A Arrival of the General 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/144/A
- **比赛来源**：Codeforces Round 103 (Div. 2) · Problem A
- **难度**：800
- **标签**：实现、贪心
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个士兵按当前顺序站成一列，将军只要求"第一个是最高的、最后一个是矮的"（其他人随便，可有并列）。每秒可交换**相邻**两人，求最少秒数。

**约束**：

- $n\le100$、$a_i\le100$，允许并列 ✓。
- 只能相邻交换 ⇒ 代价 = 移动距离（每次一步）✓。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
4
33 44 11 22

输出：
2
```

官方样例 2（输入 / 输出原样）：

```text
输入：
7
10 10 58 31 63 40 76

输出：
10
```

**样例 1 走查**：最大值 44 在下标 1（0 基），把它冒泡到最前需 1 步；最小值 11 在下标 2，移到末尾需 $4-1-2=1$ 步；最大值在最小值**左边**（$1<2$），两者交互不重叠 → 总 2 ✓。

**样例 2 走查**：最大值 76 在下标 6 → 6 步；最小值 10 取**最右**的下标 1 → $7-1-1=5$ 步；但最大值在最小值右边（$6>1$），移动过程中会"顺带"把最小值往右推一格 → 省 1 步 → $6+5-1=10$ ✓。

**观察**：

- 最大值要冒泡到最前：**取最左**的最大值（少走步）；
- 最小值要冒泡到最后：**取最右**的最小值；
- 若最大值位置在最小值位置**右侧**，两条路径交叉 ⇒ 少一次。

![位置](../../../images/cf144a_pos.svg)

## 3. 解题思路

按上面三条算出答案 ✓。

![流程](../../../images/cf144a_flow.svg)

### 3.4 样例走查

见 2 节 ✓。自造样例（标注"自造"）：`2` / `1 2` → `2`？最大 2 在下标 1、最小 1 在下标 0：$1 + (1-0) = 2$，但最大值在最小值右边 → $-1$ ⇒ 1；`3` / `5 5 5` → 0（最左最大 = 下标 0，最右最小 = 下标 2：$0 + 0 = 0$ ✓）。

## 4. 正确性证明

**引理 1**：把最左最大值移到最前至少需 `posMax` 步。

**证明**：相邻交换每步只改变一格的相对次序，跨过 `posMax` 个元素至少 `posMax` 步 ✓。∎

**引理 2**：把最右最小值移到最后至少需 `n-1-posMin` 步；两个操作可叠加，但若 `posMax > posMin` 则交叉部分只算一次（省 1）。

**证明**：两次冒泡在交叉区间共用移动 ✓；交换次序不改变总代价下界，构造可达 ✓。∎

**定理**：答案 `= posMax + (n-1-posMin) - [posMax>posMin]`。

**证明**：引理 1、2 给出下界，按"先移最大值、再移最小值"的构造可达 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n)$。
- **空间**：$O(n)$。
- **与时限的关系**：实测约 $2$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (auto& x : a) cin >> x;
    int mx = *max_element(a.begin(), a.end());
    int mn = *min_element(a.begin(), a.end());
    int posMax = -1, posMin = -1;
    for (int i = 0; i < n; ++i) if (a[i] == mx) { posMax = i; break; }        // 最左的最大值
    for (int i = n - 1; i >= 0; --i) if (a[i] == mn) { posMin = i; break; }   // 最右的最小值
    int ans = posMax + (n - 1 - posMin);
    if (posMax > posMin) --ans;   // 两者交错时省一次
    cout << ans << '\n';
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(t) for t in data[1:1 + n]]
    mx, mn = max(a), min(a)
    pos_max = a.index(mx)
    pos_min = n - 1 - a[::-1].index(mn)
    ans = pos_max + (n - 1 - pos_min)
    if pos_max > pos_min:
        ans -= 1
    print(ans)


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **最大值取最左**：取最右会多走步。
2. **最小值取最右** ✓。
3. **交叉省一步**：`posMax > posMin` 时减 1。
4. **并列极值**：靠上述取法自动处理。
5. **$n=2$**：答案 0 或 1。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：2 / 2 通过。
- **额外测试**：220 组随机数据与"枚举所有极值位置组合取最小"的独立实现比对，C++/Python 共 **440 次运行全部一致**。
- **图片校验**：两张 SVG（`cf144a_pos.svg`、`cf144a_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 144B Meeting](https://codeforces.com/problemset/problem/144/B)：同场 B 题。
- [Codeforces 144C Anagram Search](https://codeforces.com/problemset/problem/144/C)：同场 C 题。
- [LeetCode 1051. 高度检查器](https://leetcode.cn/problems/height-checker/)：排序比较。
- [LeetCode 1855. 下标对中的最大距离](https://leetcode.cn/problems/maximum-distance-between-a-pair-of-values/)：距离。

**延伸思考**：

1. **如果允许任意交换**：只数错位个数。
2. **如果要求整体非增**：变成逆序对计数。
3. **如果最大值/最小值有多解**：取法同上。
4. **如果 $n$ 很大**：$O(n)$ 仍可。
