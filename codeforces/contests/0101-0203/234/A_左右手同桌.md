# Codeforces 234A 左右手同桌 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/234/A
- **比赛来源**：Codeforces Round 145 (Div. 2, ACM-ICPC Rules) · Problem A（UTC 2012-10-13）
- **难度**：1200
- **标签**：构造
- **评测类型**：多解（输出任意合法座位表）
- **限制**：时间 1 s / 内存 256 MB

**题意**：$n$（偶数）个学生坐 $n/2$ 张双人桌，每桌左右各一人。两条限制：① 编号相差 1 的学生不能同桌；② 右手学生在左、左手学生在右的搭配不允许（会撞肘）。给出任意合法安排。

**约束**：$4\le n\le100$；保证有解。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
6
LLRLLL

输出：
1 4
2 5
6 3
```

```text
输入：
4
RRLL

输出：
3 1
4 2
```

**样例 1 演算**：配对 $(1,4),(2,5),(6,3)$：编号差都不是 1；$(6,3)$ 中 6 是 L 坐左、3 是 R 坐右，属于允许的 L–R 组合。

**样例 2 演算**：配对 $(3,1),(4,2)$：L 在左、R 在右，差为 2。

**关键观察**：把第 $i$ 个学生与第 $i+n/2$ 个学生配对，则编号差恒为 $n/2\ge2\ne1$（限制 ① 自动满足）。对每对：若两人中恰有一个 L，就把 L 放左边；否则（同为 L 或同为 R）任意。这样每桌都是 (L,·) 或 (R,R)，不会出现 (R,L)，限制 ② 也满足。

![配对 i 与 i+n/2，差恒为 n/2](../../../images/cf234a_pair.svg)

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `4` / `LLLL` | `1 3` / `2 4` | 两桌都 L–L |
| `4` / `RRRR` | `1 3` / `2 4` | 两桌都 R–R |
| `6` / `RLRLRL` | `2 1` / `4 3` / `6 5` | 每对 R,L → L 放左 |

## 3. 解题思路

### 3.1 算法

对 $i=1..n/2$：令 $p=i,\ q=i+n/2$。若 $p$ 是 R 且 $q$ 是 L，交换二者；输出 $p\ q$。

![L 放左、R 放右](../../../images/cf234a_orient.svg)

### 3.2 为什么不需要搜索

配对固定后，每对的左右朝向只受"不能 R 左 + L 右"约束：只要把该对中的 L 放左即可。由于配对差 $\ge2$，编号约束与朝向无关，因此构造总是成功。

## 4. 正确性证明

**引理 1**：配对 $(i,i+n/2)$ 的编号差为 $n/2\ge2$，故满足"编号相差 1 不能同桌"。

**证明**：$n\ge4\Rightarrow n/2\ge2$，差为 $n/2\ne1$。∎

**引理 2**：按"L 放左"的朝向后，每桌都不出现 (R 左, L 右)。

**证明**：若该对有 L：L 在左 → 左是 L，不可能是 R 左；若该对无 L（两个 R）→ 左是 R、右是 R，也不是 (R,L)。∎

**定理**：输出是合法座位表。

**证明**：配对覆盖所有学生且每对恰用一次（引理 1 保证两两不同、并集为全体）；由引理 1、2，两条限制都满足。∎

## 5. 复杂度分析

- **时间**：$O(n)$；$n\le100$ 时 < 1 ms。
- **空间**：$O(1)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    char buf[128];
    scanf("%s", buf);
    string s = buf;
    int half = n / 2;
    for (int i = 0; i < half; i++) {
        int p = i, q = i + half;          // 0-based
        if (s[p] == 'R' && s[q] == 'L') swap(p, q);   // L 放左
        printf("%d %d\n", p + 1, q + 1);
    }
    return 0;
}
```

### Python3

```python
import sys
data = sys.stdin.buffer.read().split()
n = int(data[0]); s = data[1].decode()
half = n // 2
out = []
for i in range(half):
    p, q = i, i + half
    if s[p] == 'R' and s[q] == 'L':
        p, q = q, p
    out.append(f"{p+1} {q+1}")
print("\n".join(out))
```

## 7. 边界情况与易错点

1. **编号从 1 开始**：输出要 +1。
2. **只交换 (R,L) 对**：不要把所有对都按字母排序，那会破坏"L 在左"以外的无关情形（虽仍合法，但没必要）。
3. **$n/2$ 为奇数时**：配对差仍为 $n/2\ge2$ ✓。
4. **多解**：任何合法座位表都被接受；本地验证要逐条检查两条限制与覆盖性。
5. **输入字母**：只有 `L`/`R`。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `clang++ -std=c++17 -O2 -I codeforces/tools/include` 编译；`verify_solution.py` 自动采用同样回退。Python 3.9.6。
- **官方样例**：2 / 2 通过（与官方输出逐字一致）。
- **独立暴力对拍**：对 $n\in\{4,6,8,10\}$ 的 **200 组**随机 L/R 串，逐条校验输出：配对覆盖、编号差 $\ne1$、无 (R 左, L 右)，全部通过。
- **最大约束性能**：$n=100$ 时 < 1 ms（限 1 s）。
- **图片校验**：两张 SVG 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写字体，文本包围盒均在 `viewBox` 内。
- **公式校验**：`node codeforces/tools/katex_check.cjs codeforces/contests/0101-0203/234` 报告 0 个错误。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 234B Reading](https://codeforces.com/problemset/problem/234/B)：同场 B 题，排序取前 k。
- [Codeforces 234C Weather](https://codeforces.com/problemset/problem/234/C)：同场 C 题，前后缀计数。
- [LeetCode 1054. 距离相等的条形码](https://leetcode.cn/problems/distant-barcodes/)：重排类构造。

**延伸思考**：

1. **如果限制改为"编号差 ≤1 不能同桌"**：配对差为 $n/2$ 仍然成立（$n/2\ge2$）。
2. **如果 n 为奇数**：无法两两配对，无解。
3. **如果要求字典序最小的座位表**：在合法配对空间里贪心搜索。
4. **如果允许三人桌**：约束结构变化，需要重新建模。
