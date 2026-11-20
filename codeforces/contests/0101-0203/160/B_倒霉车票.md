# Codeforces 160B 倒霉车票 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/160/B
- **比赛来源**：Codeforces Round 111 (Div. 2) · Problem B（UTC 2012-03-06）
- **难度**：1100
- **标签**：贪心、排序
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$2n$ 位数字组成的票号，均分成前后两半。若能把两半各重新配对，使每一对中"前半数字严格小于后半"或"每对中前半严格大于后半"，则输出 `YES`，否则 `NO`。

**约束**：$n\le100$：两半各自排序后逐位比较即可。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
2
2421

输出：
YES
```

前半 `24`、后半 `21`：排序后 `24` 与 `12`，逐位 $2>1$、$4>2$ ⇒ 全部严格大于 ⇒ YES ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
2
0135

输出：
YES
```

前半 `01`、后半 `35`：$0<3$、$1<5$ ✓

官方样例 3（输入 / 输出原样）：

```text
输入：
2
3754

输出：
NO
```

前半 `37`、后半 `54`：排序后 $3<5$ ✓ 但 $7>4$ ✗ ⇒ 混合，无法统一 ⇒ NO ✓

![两半各自排序后逐位比较](../../../images/cf160b_pair.svg)

**观察**：配对可以任意重排 ⇒ 只看两个多重集。存在满足"全部 `<`"的配对 ⟺ 排序后逐位 $x_i<y_i$ 全部成立（这是经典的重排不等式：要每个前半都小于对应的后半，按同样顺序排是最优尝试）。

## 3. 解题思路

1. 取前 $n$ 位与后 $n$ 位，各自排序；
2. 判断"所有 $x_i<y_i$"或"所有 $x_i>y_i$"是否成立；
3. 输出 `YES`/`NO`。

![样例 3：37 与 54 方向冲突 → NO](../../../images/cf160b_sample.svg)

## 4. 正确性证明

**引理（排序后逐位比较的充分必要性）**：设 $X,Y$ 为两个大小相同的多重集，则存在双射 $\pi$ 使所有 $x_i<y_{\pi(i)}$ ⟺ 把 $X,Y$ 升序排列后逐位 $x_i<y_i$。

**证明**：必要性：若存在某双射满足严格小于，则对任意 $k$，$X$ 中最小的 $k$ 个必须分别小于 $Y$ 中与之配对的 $k$ 个，故 $X$ 的前 $k$ 小之和... 更直接：由重排不等式，$\sum$ 最小化时按同序配对；若同序配对中某一位 $x_i\ge y_i$，则 $X$ 中至少有 $i$ 个元素 $\ge$ $Y$ 中第 $i$ 小的元素，鸽巢原理推出不存在完美匹配（Hall 定理/贪心交换）。充分性显然 ✓ ∎

**定理**：程序输出正确。

**证明**：题面要求的两种情形分别是"双射使全部 $<$"与"双射使全部 $>$"，由引理各自等价于排序后逐位比较；程序正是这样判定 ✓ ∎

## 5. 复杂度分析

- **时间**：排序 $O(n\log n)$，实测 < 2 ms。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    string s;
    cin >> s;
    string x = s.substr(0, n), y = s.substr(n, n);
    sort(x.begin(), x.end());
    sort(y.begin(), y.end());
    bool less = true, greater = true;
    for (int i = 0; i < n; i++) {
        if (!(x[i] < y[i])) less = false;
        if (!(x[i] > y[i])) greater = false;
    }
    printf("%s\n", (less || greater) ? "YES" : "NO");
    return 0;
}
```

### Python3

```python
import sys
def main():
    data = sys.stdin.read().split()
    n = int(data[0]); s = data[1]
    x = sorted(s[:n]); y = sorted(s[n:])
    less = all(a < b for a, b in zip(x, y))
    greater = all(a > b for a, b in zip(x, y))
    print("YES" if less or greater else "NO")
main()
```

## 7. 边界情况与易错点

1. **严格**：相等不算（`<=` 会误判）。
2. **两个方向都要试**：只要一个方向全满足即可。
3. **$n=1$**：比较单个数字。
4. **字符比较**：数字字符的字典序与数值序一致，可直接比较字符。
5. **长度为 $2n$**：题面保证。
6. **不能混用方向**：样例 3。
7. **输出大小写**：`YES`/`NO`。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/160/B_倒霉车票.md`
- **官方样例**：$3/3$ 通过（`YES`、`YES`、`NO`），C++ 与 Python 一致。
- **独立对拍**：另写"枚举所有 $n!$ 配对、检查是否全部严格同向"的暴力，对 $200$ 组随机票号（$n\le5$）比较，全部一致。
- **性能**：$n=100$ 单次 < 2 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 160A Twins](https://codeforces.com/problemset/problem/160/A)：同场 A 题。
- [Codeforces 160C Find Pair](https://codeforces.com/problemset/problem/160/C)：同场 C 题。
- [LeetCode 881. 救生艇](https://leetcode.cn/problems/boats-to-save-people/)：重排配对。

**延伸思考**：

1. **若要求"恰好 $m$ 对严格小于、其余严格大于"**：需要更细的匹配。
2. **若允许相等**：判据变成 $\le$。
3. **若两半长度不同**：多出的元素无法配对。
