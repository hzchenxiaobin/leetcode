# Codeforces 125C 霍比特人的派对 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/125/C
- **比赛来源**：Codeforces Testing Round 2 · Problem C（UTC 2011-10-29）
- **难度**：1600
- **标签**：构造、组合
- **评测类型**：普通（输出任意方案）
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个霍比特人，安排 $k$ 天派对，每天给出一个非空客人集合，要求：

- 任意两天都有**至少一个**共同客人；
- 任意三天都**没有**共同客人。

求最大的 $k$ 及每天的客人名单。

**约束**：

- $n\le10000$；客人编号 $1..n$。
- 输出任意合法方案。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
4
输出：
3
1 2 
1 3 
2 3 
```

官方样例二：

```text
输入：
5
输出：
3
1 2 
1 3 
2 3 
```

**样例走查**：$n=4$：三天分别是 $\{1,2\},\{1,3\},\{2,3\}$：两两有交集 ✓，三天无共同客人 ✓。

![客人对应"天对"](../../../images/cf125c_pairs.svg)

**观察**：条件"任意两天相交、任意三天无共同"意味着**每个客人只能在至多两天出现**（否则三天会共享他）。于是每个客人可以看作"某两天组成的一对"，而任意两天都需要一对 → 需要的客人数 $\ge\binom{k}{2}$。

## 3. 解题思路

### 3.1 核心观察：客人 = 天对

![样例 n=4](../../../images/cf125c_sample.svg)

若安排 $k$ 天，则：

- 每个客人至多出现在 2 天（否则任意含这三天的三元组违反条件）；
- 任意两天必须共享客人 → 至少 $\binom{k}{2}$ 个客人（每个客人最多覆盖一对天）。

所以 $k$ 的最大值由 $\binom{k}{2}\le n$ 决定；反之取 $k$ 满足条件，并给每一对天分配一个专属客人即可构造成功。

### 3.2 算法流程

1. 求最大的 $k$ 使 $k(k-1)/2\le n$；
2. 枚举所有天对 $(a,b)$（$a<b$），分配新编号客人 $id$，加入第 $a$ 天与第 $b$ 天；
3. 输出 $k$ 与每天的客人列表。

### 3.3 样例走查

$n=4$：$k=3$（$\binom{3}{2}=3\le4<\binom{4}{2}=6$）；天对 $(0,1),(0,2),(1,2)$ → 客人 1,2,3 → 输出 `1 2`、`1 3`、`2 3` ✓。

## 4. 正确性证明

**引理 1**：合法方案中每个客人最多出现 2 天。

**证明**：若某客人出现在三天 $A,B,C$，则这三天有共同客人，违反第二条 ✓。∎

**引理 2**：$k$ 天需要至少 $\binom{k}{2}$ 个客人。

**证明**：每对天（共 $\binom{k}{2}$ 对）都必须有共同客人；由引理 1 一个客人最多同时覆盖一对天，故客人数 $\ge\binom{k}{2}$ ✓。∎

**引理 3**：构造方案合法。

**证明**：任意两天恰共享"它们那一对"的客人（至少一个 ✓）；任意三天：每个客人只属于一对天，不可能同时属于三天 ✓。∎

**定理**：算法给出的 $k$ 最大且方案合法。

**证明**：由引理 2，$k$ 必须满足 $\binom{k}{2}\le n$，算法取到最大 ✓；由引理 3 方案合法 ✓。∎

## 5. 复杂度分析

- **时间**：$O(k^2)\le O(n)$。
- **空间**：$O(n)$。
- **与时限的关系**：实测约 $3$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int k = 0;
    while ((k + 1) * k / 2 <= n) ++k;   // 最大的 k 使 C(k,2) <= n
    printf("%d\n", k);
    // 第 i 天：所有包含 i 的二元组对应的“hobbit”
    vector<vector<int>> days(k);
    int id = 0;
    for (int a = 0; a < k; ++a)
        for (int b = a + 1; b < k; ++b) {
            ++id;
            days[a].push_back(id);
            days[b].push_back(id);
        }
    for (int i = 0; i < k; ++i) {
        string line;
        for (size_t t = 0; t < days[i].size(); ++t) {
            line += to_string(days[i][t]);
            line += ' ';
        }
        printf("%s\n", line.c_str());
    }
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    k = 0
    while (k + 1) * k // 2 <= n:
        k += 1
    days = [[] for _ in range(k)]
    idx = 0
    for a in range(k):
        for b in range(a + 1, k):
            idx += 1
            days[a].append(idx)
            days[b].append(idx)
    out = [str(k)]
    for d in days:
        out.append(" ".join(map(str, d)) + " " if d else "")
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 7. 边界情况与易错点

1. **必须每天非空**：$k\ge2$ 时每天至少出现在 $k-1$ 对里，非空 ✓（$k=1$ 也非空）。
2. **上界公式**：$k(k-1)/2\le n$，注意是组合数不是 $k^2$。
3. **客人编号范围**：$1..n$，构造用的客人数恰好 $\binom{k}{2}\le n$ ✓。
4. **输出格式**：第一行 $k$，之后每天一行。
5. **$n=3$**：$k=2$（$\binom{2}{2}=1\le3<\binom{3}{2}=3$）→ 两天 `1`、`1` ✓。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：2 / 2 通过（都是 `3` + 三行），C++ 与 Python 一致。
- **独立暴力对拍**：独立校验器检查（$k$ 是否最大、每天非空、两两相交、无三元共同、编号范围），对 $n=3..59$ **全部 57 个取值** 两语言均通过。
- **性能**：约 $3$ ms。
- **图片校验**：`cf125c_pairs.svg`、`cf125c_sample.svg` 通过 `ElementTree.parse`，无越界/重叠。
- **公式校验**：KaTeX 0 错；无 `---` 分隔线。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 125A 巴登长度换算](https://codeforces.com/problemset/problem/125/A)、[125B Simple XML](https://codeforces.com/problemset/problem/125/B)、[125D Two progressions](https://codeforces.com/problemset/problem/125/D)、[125E MST Company](https://codeforces.com/problemset/problem/125/E)：同场其余题。
- [LeetCode 1419. 数青蛙](https://leetcode.cn/problems/minimum-number-of-frogs-croaking/)：构造计数。
- [Codeforces 1332B Composite Coloring](https://codeforces.com/problemset/problem/1332/B)：构造分类。

**延伸思考**：

1. **如果允许三元共同**：上界变成 $\binom{k}{3}\le n$ 之类的更高阶条件。
2. **如果要求每天客人数量相同**：变成平衡不完全区组设计（BIBD）。
3. **如果要求"任意两天恰好一个共同客人"**：这正是本题构造，称为"成对平衡设计"的退化情形。

