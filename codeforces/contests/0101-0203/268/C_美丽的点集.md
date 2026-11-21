# Codeforces 268C 美丽的点集 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/268/C
- **比赛来源**：Codeforces Round 164 (Div. 2) · Problem C（UTC 2013-01-28）
- **难度**：1500
- **标签**：构造
- **评测类型**：多解（任意最优解）
- **限制**：时间 1 s / 内存 256 MB

**题意**：在 $0 \le x \le n$、$0 \le y \le m$、$x + y > 0$ 的整点中选一个尽量大的子集，使**任意两点距离都不是整数**。输出方案。

**约束**：$n, m \le 100$。

## 2. 示例与观察

官方样例 1：

```text
输入：
2 2

输出：
3
0 1
1 2
2 0
```

官方样例 2：

```text
输入：
4 3

输出：
4
0 3
2 1
3 0
4 2
```

**观察 1（选一条反对角线）**：取 $x + y = c$，任意两点的距离为 $|dx|\sqrt 2$；因为 $\sqrt 2$ 是无理数，只有 $dx = 0$（同一个点）时才是整数 → 所以这条线上的整点两两距离都非整数 ✓。

**观察 2（点数最大）**：$x+y=c$ 上满足 $0\le x\le n$、$0\le y \le m$ 的整点数为 $\min(n,c) - \max(0, c-m) + 1$，在 $c = \min(n,m)$ 时取到 $\min(n,m)+1$。

**观察 3（上界）**：同一列（或同一行）里任意两点距离是整数（垂直/水平相差整数），所以每行每列最多取 1 个点 → 总数 $\le \min(n, m) + 1$ ✓ 与构造吻合。

## 3. 解题思路

![全部点放在一条反对角线上](../../../images/cf268c_line.svg)

1. $c = \min(n, m)$；
2. 输出所有 $(x, c-x)$，$x$ 从 $\max(0, c-m)$ 到 $\min(n, c)$。

## 4. 正确性证明

**引理 1（合法性）**：同一条反对角线上的不同整点距离不是整数。

**证明**：设两点 $(x_1, c-x_1)$、$(x_2, c-x_2)$，$d = |x_1-x_2|\sqrt 2$；$\sqrt2$ 无理，$d$ 为整数 ⇔ $|x_1-x_2| = 0$ ⇔ 同一点 ✓。∎

**引理 2（点数）**：构造输出的点数恰为 $\min(n,m)+1$。

**证明**：$c = \min(n,m)$ 时 $y = c - x \ge 0$ 且 $x \le c \le n$、$y \le c \le m$，所以全部 $x \in [0, c]$ 都合法，共 $c+1$ 个 ✓；且 $(0,0)$ 不在其中（$x+y = c \ge 1$）✓。∎

**引理 3（上界）**：任一合法点集大小 $\le \min(n,m)+1$。

**证明**：同一列两点距离为 $|dy|$（整数）→ 每列至多 1 个；共 $n+1$ 列 → $\le n+1$；同理每行至多 1 个 → $\le m+1$；取小得 $\le \min(n,m)+1$ ✓。∎

**定理**：构造最优。

**证明**：引理 1、2 给出合法解且达到引理 3 的上界 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n+m)$（输出量）。
- **空间**：$O(1)$。
- **与时限的关系**：时限 1 s，实测端到端 2.8 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    // 取同一条反对角线 x+y=c 上的所有整点，c = min(n,m)
    int c = min(n, m);
    vector<pair<int,int>> pts;
    for (int x = max(0, c - m); x <= min(n, c); x++) pts.push_back({x, c - x});
    printf("%d\n", (int)pts.size());
    for (auto &p : pts) printf("%d %d\n", p.first, p.second);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    c = min(n, m)
    pts = [(x, c - x) for x in range(max(0, c - m), min(n, c) + 1)]
    out = [str(len(pts))]
    for x, y in pts:
        out.append("%d %d" % (x, y))
    sys.stdout.write("\n".join(out) + "\n")
main()
```

## 7. 边界情况与易错点

1. **不能包含 $(0,0)$**：题面要求 $x+y>0$；$c \ge 1$ 保证 ✓。
2. **$n \ne m$**：取 $c = \min$ 时仍在矩形内 ✓。
3. **输出点数必须等于实际点数**。
4. **多解**：与官方不同的点集也算对（本题 special judge）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（由 checker 判定合法），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf268c.py`（检查范围、去重、任意两点距离平方是否为完全平方数）。
- **独立暴力对拍**：随机 $n, m \le 5$，250 组，两个实现都通过 checker，且点数都等于 $\min(n,m)+1$（与理论上界一致），**250 / 250 通过**。
- **最大约束性能**：$n = m = 100$，实测端到端 2.8 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 268B Buttons](https://codeforces.com/problemset/problem/268/B)：同场 B 题。
- [Codeforces 268E Playlist](https://codeforces.com/problemset/problem/268/E)：同场 E 题。

**延伸思考**：

1. **如果允许取任意多边形区域**：构造要改，但"每行每列至多一个"的上界仍在。
2. **如果距离要求是"有理数"**：条件会强很多。

