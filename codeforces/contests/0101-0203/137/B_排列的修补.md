# Codeforces 137B Permutation 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/137/B
- **比赛来源**：Codeforces Beta Round 98 (Div. 2) · Problem B
- **难度**：1000
- **标签**：实现、贪心
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给 $n$ 个数（$1\le a_i\le5000$），每次可把任一元素改成任意整数。求最少改几个，使序列成为 $1..n$ 的排列（不能删/加元素）。

**约束**：

- $n\le5000$、$a_i\le5000$：桶计数即可。
- 排列要求每个 $1..n$ 恰好出现一次 ✓；$>n$ 的值必须改 ✓。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3
3 1 2

输出：
0
```

官方样例 2（输入 / 输出原样）：

```text
输入：
2
2 2

输出：
1
```

官方样例 3（输入 / 输出原样）：

```text
输入：
5
5 3 3 3 1

输出：
2
```

**样例 3 走查**：值集在 $1..5$ 内为 $\{5,3,1\}$，缺 $\{2,4\}$ → 需要改 2 个 ✓（把多余的两个 3 改成 2、4 ✓）。

**观察**：答案 = $1..n$ 中**没出现**的值的个数 = $n-$（$1..n$ 中出现的不同值个数）✓ —— 每缺一个值就要改一个"多余"的位置，且总能把多余的改成缺的 ✓。

![缺失值](../../../images/cf137b_missing.svg)

## 3. 解题思路

桶标记 $1..n$ 内出现过的值，统计缺失数 ✓。

![流程](../../../images/cf137b_flow.svg)

### 3.4 样例走查

见 2 节 ✓。

自造样例（标注"自造"）：

| 输入 | 输出 |
|------|------|
| `1` / `1` | `0` |
| `1` / `7` | `1` |
| `4` / `1 1 1 1` | `3` |

## 4. 正确性证明

**引理 1**：设 $S=\{a_i\le n\}$ 的不同值集合，则至少需改 $n-|S|$ 个。

**证明**：最终排列含全部 $1..n$；只保留 $|S|$ 个合法值不动 → 其余 $n-|S|$ 个位置必须改 ✓。∎

**引理 2**：$n-|S|$ 个改动足够。

**证明**：把多余元素（重复值或 $>n$）逐个改成缺失值即可 ✓。∎

**定理**：答案 = $n-|S|$。

**证明**：引理 1、2 ✓。∎

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
    vector<char> seen(n + 1, 0);
    for (int i = 0; i < n; ++i) { int x; cin >> x; if (x <= n) seen[x] = 1; }
    int missing = 0;
    for (int v = 1; v <= n; ++v) if (!seen[v]) ++missing;
    cout << missing << '\n';
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    seen = [False] * (n + 1)
    for i in range(n):
        x = int(data[1 + i])
        if x <= n:
            seen[x] = True
    print(sum(1 for v in range(1, n + 1) if not seen[v]))


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **$>n$ 的值**：不算"已出现"，必须改。
2. **重复值**：多余的要改。
3. **已恰好是排列**：0。
4. **$n=1$**：$a_1=1$ → 0。
5. **桶大小**：$n+1$ 即可（只看 $1..n$）。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：3 / 3 通过。
- **额外测试**：220 组随机数据与"缺失值计数"独立实现比对，**220 / 220 全部一致**。
- **图片校验**：两张 SVG（`cf137b_missing.svg`、`cf137b_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 137A Postcards and photos](https://codeforces.com/problemset/problem/137/A)：同场 A 题。
- [Codeforces 137C History](https://codeforces.com/problemset/problem/137/C)：同场 C 题。
- [LeetCode 448. 找到所有数组中消失的数字](https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array/)：缺失数字。
- [LeetCode 268. 丢失的数字](https://leetcode.cn/problems/missing-number/)：缺失数字。

**延伸思考**：

1. **如果允许删/加**：问题变成集合对齐。
2. **如果要求最小改动次数且可换顺序**：同上。
3. **如果值域更大**：用哈希或排序。
4. **如果要求输出方案**：把多余位置改成缺失值。
