# Codeforces 115B Lawnmower 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/115/B
- **比赛来源**：Codeforces Beta Round 87 (Div. 1 Only) · Problem B（UTC 2011-09-15）
- **难度**：1500
- **标签**：贪心、排序
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n\times m$ 的花园，每格是草 `G` 或杂草 `W`。除草机从 $(1,1)$ 出发、初始朝右。每步可以：

1. 沿当前朝向水平移动一格；
2. 向下一格（行 $+1$），**同时把朝向翻转**。

不能离开花园。求割掉所有杂草的最少步数（杂草被"经过"即割掉）。

**约束**：

- $n,m\le150$：$O(nm)$ 或 $O(nm^2)$ 都行。
- 向左只能在朝左时移动、向右只能在朝右时移动 —— **一行之内不能回头**。
- 每下移一行，朝向翻转，所以在第 $i$ 行（1 基）时朝向一定是"奇数行朝右、偶数行朝左"✓。
- 初始格一定是草。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
4 5
GWGGW
GGWGG
GWGGG
WGGGG

输出：
11
```

官方样例 2（输入 / 输出原样）：

```text
输入：
3 3
GWW
WWW
WWG

输出：
7
```

官方样例 3（输入 / 输出原样）：

```text
输入：
1 1
G

输出：
0
```

**样例 1 走查**：杂草分布在行 1 的列 2、5，行 2 的列 3，行 3 的列 2，行 4 的列 1。

- 第 1 行朝右：从列 1 走到列 5（4 步，顺带割掉列 2 的草）→ 还必须下移前把列 3 的草留到行 2？行 2 朝左，从列 5 往左扫，能扫到列 3 ✓，但行 1 下移后列 5 的入口要满足行 2 的右端 = 3 ✓
- 下移（1 步）朝左，从列 5 走到列 2（3 步，割行 2 列 3、行 3 列 2 的入口？）

按"每行出口列 = max(本行右端, 下一行右端)"（朝右）或 min(本行左端, 下一行左端)（朝左）的贪心算：4 + 1 + 3 + 1 + 0 + 1 + 1 = 11 ✓（与程序输出一致）。

**样例 2 走查**：3×3，杂草在行 1 的列 2、3，行 2 全部，行 3 的列 1、2。朝右第 1 行要走到列 3（2 步）；下移（1）朝左，行 2 朝左从列 3 扫到列 1（2 步）；下移（1）朝右，行 3 从列 1 扫到列 2（1 步）→ 2+1+2+1+1 = 7 ✓。

**观察 1**：第 $i$ 行的朝向完全由行号决定（奇数朝右、偶数朝左），所以**只需决定每行的"出口列"**。

**观察 2**：朝右时，除草机在该行只能向右走，所以它经过的列区间是 $[入口, 出口]$；要割掉本行杂草，必须 $入口 \le$ 本行最左杂草、$出口 \ge$ 本行最右杂草。又因为下一行朝左，下一行的入口 $=$ 本行的出口，而下一行要能扫到它最右的杂草，需要 $出口 \ge$ 下一行最右杂草。

![朝向与出口](../../../images/cf115b_rows.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

可以 DP：`dp[i][c]` = 处理完前 $i$ 行、位于第 $i$ 行入口列 $c$ 的最小水平步数，转移 $O(m^2)$，总 $O(nm^2)=3.4\times10^6$ ✓ 可行。

但更有洞见的是**贪心**：每行的出口列可以直接定出来。

### 3.2 核心观察：每行出口 = 本行与下一行极值的合并

记第 $i$ 行为：

- $L_i$ = 本行最左杂草列（无杂草则无约束）；
- $R_i$ = 本行最右杂草列。

设处理第 $i$ 行时除草机在列 $c$。

- **朝右**（$i$ 为奇数）：出口 $e=\max\bigl(c,\ R_i,\ R_{i+1}\bigr)$，其中不存在的项忽略；步数 $e-c$。
- **朝左**（$i$ 为偶数）：出口 $e=\min\bigl(c,\ L_i,\ L_{i+1}\bigr)$，步数 $c-e$。

为什么"合并下一行"是对的：下一行朝向相反，从同一列出发扫向另一侧，所以本行的出口必须已经越过下一行最远的那一侧；同时出口不能比当前位置更"往回"（朝右不能变小）✓。

最后一行只合并本行的极值。总步数 = 水平步数之和 + 下移次数（= 最后一个有杂草的行号 $-1$）。

![流程](../../../images/cf115b_flow.svg)

### 3.3 算法流程

1. 预处理每行的 $L_i,R_i$，找最后一个有杂草的行 $last$；
2. 若没有杂草 → 0；
3. `cur=0`（列，0 基）、`right=true`、`ans=0`；
4. 对 $i=1..last$：
   - 朝右：`need = max(cur, R_i, R_{i+1})`（越界项略），`ans += need-cur`，`cur=need`；
   - 朝左：`need = min(cur, L_i, L_{i+1})`，`ans += cur-need`，`cur=need`；
   - 若 $i<last$：`ans += 1`（下移），`right = !right`；
5. 输出 `ans`。

### 3.4 样例走查

样例 1（列 0 基）：$L=[1,2,1,0]$，$R=[4,2,1,0]$，$last=3$。

| 行 | 朝向 | 入口 | 计算 | 出口 | 累计 |
|----|------|------|------|------|------|
| 0 | 右 | 0 | max(0,4,2)=4 | 4 | 4 |
| 1 | 左 | 4 | min(4,1,1)=1 | 1 | 4+1+3=8 |
| 2 | 右 | 1 | max(1,1,0)=1 | 1 | 8+1+0=9 |
| 3 | 左 | 1 | min(1,0)=0 | 0 | 9+1+1=11 |

输出 11 ✓。

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `1 1` / `G` | 0 | 无杂草 |
| `2 2` / `GG` / `GW` | 2 | 行 1 朝右走到列 2（1 步），下移 1 步，行 2 朝左已覆盖杂草 |
| `3 3` / `GGG` / `GGG` / `GGW` | 4 | 行 1 走到列 3（2 步）+ 下移 2 步 |

## 4. 正确性证明

**引理 1（朝向确定）**：处理第 $i$ 行时朝向恒为"奇数行朝右、偶数行朝左"。

**证明**：初始朝右且每下移一次翻转，归纳即得。∎

**引理 2（出口必须满足的下界/上界）**：朝右处理第 $i$ 行时，出口 $e\ge \max(R_i,R_{i+1})$（不存在的项忽略），且 $e\ge c$；朝左时 $e\le\min(L_i,L_{i+1})$ 且 $e\le c$。

**证明**：朝右时经过区间 $[c,e]$ 必须覆盖本行杂草 $[L_i,R_i]$，故 $e\ge R_i$；下一行朝左、入口为 $e$、需覆盖其杂草 $[L_{i+1},R_{i+1}]$，扫左需入口 $\ge R_{i+1}$，故 $e\ge R_{i+1}$；$e\ge c$ 是因为只能向右。朝左对称。∎

**引理 3（贪心取等号最优）**：每行的步数只与 $|e-c|$ 有关，且 $c$ 由上一行决定；取引理 2 中最小可行的 $e$ 即为最优。

**证明**：第 $i$ 行的代价是 $|e-c|$，$e$ 的取值范围是 $[\,\max(c,R_i,R_{i+1}),\,m-1]$（朝右），代价随 $e$ 单调增，取最小值 $e=\max(c,R_i,R_{i+1})$ 最优；而且更小的 $e$ 不会让后续行更优（后续行的入口与 $e$ 的关系是：朝右行希望入口尽量小、朝左行希望入口尽量大，取我们的 $e$ 恰好同时满足下一行的最远需求，再大只会增加本行与后续行的距离）✓。∎

**定理**：算法输出最少步数。

**证明**：下移次数固定为 $last$（必须下移到最后一个有杂草的行，且每次下移都是必需的）；水平步数由引理 2、3 逐行取到下界并达到 ✓。∎

## 5. 复杂度分析

- **时间**：$O(nm)$。
- **空间**：$O(nm)$（存网格）或 $O(n)$。
- **与时限的关系**：实测 $150\times150$ 时 C++ 端到端 $6.0$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<string> g(n);
    for (int i = 0; i < n; ++i) cin >> g[i];
    vector<int> L(n, INT_MAX), R(n, -1);
    int last = -1;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            if (g[i][j] == 'W') {
                L[i] = min(L[i], j);
                R[i] = max(R[i], j);
                last = i;
            }
    if (last < 0) { cout << 0 << '\n'; return 0; }
    long long ans = 0;
    int cur = 0;          // 当前列（0 基）
    bool right = true;    // 朝向
    for (int i = 0; i <= last; ++i) {
        int need = -1;
        if (right) {
            need = cur;                      // 可以原地不动
            if (R[i] >= 0) need = max(need, R[i]);
            if (i + 1 <= last && R[i + 1] >= 0) need = max(need, R[i + 1]);
            ans += need - cur; cur = need;
        } else {
            need = cur;
            if (L[i] < INT_MAX) need = min(need, L[i]);
            if (i + 1 <= last && L[i + 1] < INT_MAX) need = min(need, L[i + 1]);
            ans += cur - need; cur = need;
        }
        if (i < last) { ++ans; right = !right; }   // 向下移动并转向
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
    g = [data[2 + i].decode() for i in range(n)]
    L = [m] * n
    R = [-1] * n
    last = -1
    for i in range(n):
        for j in range(m):
            if g[i][j] == 'W':
                if j < L[i]:
                    L[i] = j
                if j > R[i]:
                    R[i] = j
                last = i
    if last < 0:
        sys.stdout.write("0\n")
        return
    ans = 0
    cur = 0
    right = True
    for i in range(last + 1):
        if right:
            need = cur
            if R[i] >= 0:
                need = max(need, R[i])
            if i + 1 <= last and R[i + 1] >= 0:
                need = max(need, R[i + 1])
            ans += need - cur
            cur = need
        else:
            need = cur
            if L[i] < m:
                need = min(need, L[i])
            if i + 1 <= last and L[i + 1] < m:
                need = min(need, L[i + 1])
            ans += cur - need
            cur = need
        if i < last:
            ans += 1
            right = not right
    sys.stdout.write(str(ans) + "\n")


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **出口要 clamp 到入口列**：朝左时若"下一行的左端"在入口右侧，不能强行往右走（第一版本就漏了这个 clamp，被对拍抓出）。
2. **没有杂草**：输出 0（不要输出 $n-1$ 的下移步数）。
3. **下移次数**：固定为"最后一个有杂草的行号 $-1$"，而不是 $n-1$。
4. **最后一行**：只合并自己的极值，没有"下一行"。
5. **行内不回头**：不要写成"可以先左后右"。
6. **入口列 = 上一行出口列**：下移不改变列。
7. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：3 / 3 通过（`11`、`7`、`0`）。
- **额外测试（逐行 DP 暴力对拍）**：另写一份**按行 DP** 的暴力——`dp[i][c]` = 到达第 $i$ 行入口列 $c$ 的最小水平步数，枚举行内所有可行出口列 $c'$ 且检查经过区间是否覆盖本行杂草；对 300 组随机小网格（$n,m\le6$，杂草概率 0.35）与 C++、Python 三方比对，**300 / 300 全部一致**（该对拍抓出了第一版贪心漏 clamp 的 bug）。
- **最大约束性能**：$150\times150$ 时 C++ 端到端 5 次平均 $6.0$ ms、Python $16.8$ ms。
- **图片校验**：两张 SVG（`cf115b_rows.svg`、`cf115b_flow.svg`）通过 `xml.etree.ElementTree.parse`，文本块估算未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError: true`）渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 115A Party](https://codeforces.com/problemset/problem/115/A)：同场 A 题。
- [Codeforces 115C Plumber](https://codeforces.com/problemset/problem/115/C)：同场 C 题。
- [Codeforces 1155C Alarm Clocks Everywhere](https://codeforces.com/problemset/problem/1155/C)：贪心。
- [LeetCode 1011. 在 D 天内送达包裹的能力](https://leetcode.cn/problems/capacity-to-ship-packages-within-d-days/)：区间贪心。
- [LeetCode 253. 会议室 II](https://leetcode.cn/problems/meeting-rooms-ii/)：扫描。

**延伸思考**：

1. **如果允许在行内掉头**：每行最优就变成"覆盖区间的最短路"，答案更小。
2. **如果下移不转向**：贪心会更简单（每行都能只朝一个方向累积）。
3. **如果要求输出路径**：把每行的起止列记下来即可。
4. **如果花园很大（$1500^2$）**：$O(nm)$ 仍然够。
