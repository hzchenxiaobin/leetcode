# Codeforces 299B Ksusha the Squirrel 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/299/B
- **比赛来源**：Croc Champ 2013 - Round 2 (Div. 2 Edition) · Problem B（UTC 2013-04-19）
- **难度**：900
- **标签**：贪心、实现
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：$n$ 个格子排成一行，某些格子上有石头（`#`），松鼠从第 1 格出发，每步可以跳到 $i+1..i+k$ 中的任意一格，但不能落在石头上。问能否到达第 $n$ 格（保证首尾都是 `.`）。

**约束**：$n\le3\times10^5$，$k\le3\times10^5$ ⇒ $O(n)$。

## 2. 示例与观察

官方样例 1：

```text
输入：
2 1
..

输出：
YES
```

官方样例 2：

```text
输入：
5 2
.#.#.

输出：
YES
```

官方样例 3：

```text
输入：
7 3
.#.###.

输出：
NO
```

![关键判据](../../../images/cf299b_gap.svg)

**观察（唯一障碍是最长连续石头段）**：要跨过一段长 $L$ 的连续石头，必须从石头前那一格直接跳到石头后那一格，跳跃距离是 $L+1$ ⇒ 必须 $L+1\le k$。只要所有石头段都满足，就能逐段跳过。

所以判据：**存在长度 $\ge k$ 的连续 `#` 段 ⇒ NO，否则 YES**。

## 3. 解题思路

### 3.1 正解

![为什么不用 BFS](../../../images/cf299b_flow.svg)

一次扫描，维护当前连续 `#` 的长度 `run`：`run` 一旦达到 $k$ 就输出 `NO`；扫完没触发则 `YES`（遇到 `.` 把 `run` 清 0）。

### 3.2 样例走查

样例 2：`.#.#.`，$k=2$：石头段长 1，$1+1=2\le2$ ✓ ⇒ YES。
样例 3：`.#.###.`，$k=3$：中间一段长 3，$3+1=4>3$ ✗ ⇒ NO。

## 4. 正确性证明

**引理 1**：若存在长 $L\ge k$ 的连续石头段，则无法通过。

**证明**：该段前后最近的落脚点之间距离 $L+1\ge k+1>k$，超出单次跳跃上限；而跳跃只能向前、且不能落在段内 ⇒ 无法越过 ✓。∎

**引理 2**：若所有石头段长 $L$ 都满足 $L+1\le k$，则可以到达终点。

**证明**：构造性策略：从当前位置一直往前跳，遇到石头段时从段前那一格跳到段后那一格（距离 $L+1\le k$ ✓）。段内不含石头，段与段之间全是 `.`，所以每一步都合法，能一路走到 $n$ ✓。∎

**定理**：判据正确。**证明**：由引理 1、2 ✓。∎

## 5. 复杂度分析

- 时间：$O(n)$，$n=3\times10^5$ 实测 $<1$ ms。
- 空间：$O(n)$（存路串），额外 $O(1)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){int n,k;scanf("%d %d",&n,&k);static char s[300005];scanf("%s",s);
 int run=0;
 for(int i=0;i<n;i++){
   if(s[i]=='#'){run++; if(run>=k){puts("NO");return 0;}}
   else run=0;
 }
 puts("YES");}
```

### Python3

```python
n, k = map(int, input().split())
s = input().strip()
run = 0
for c in s:
    if c == '#':
        run += 1
        if run >= k:
            print("NO")
            break
    else:
        run = 0
else:
    print("YES")
```

## 7. 边界情况与易错点

1. **判据是"最长连续段 ≥ k"**，不是"石头总数 ≥ k"。
2. **$k=1$**：任何石头（长度 1 ≥ 1）都过不去 ⇒ 只要有 `#` 就 NO。
3. **首尾是 `.`**（题面保证）⇒ 起点/终点不会被石头占。
4. **段长为 $k-1$ 时可以过**（跳跃距离恰好 $k$）。
5. **$n=2$**：直接判两格是否都为空。
6. **别写 BFS**：$O(n)$ 扫描足够，BFS 也能过但没必要。

## 8. 验证记录

- 编译环境与命令：`clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/299/B_松鼠克苏莎.md`
- 官方样例：3 / 3 通过（`YES`、`YES`、`NO`）。
- 额外测试：随机 250 组（$n\le10$、$k\le5$、随机石头布局、首尾强制为 `.`）与"按可达点集合逐格 DP"的暴力对拍，全部一致。
- 最大约束性能：$n=3\times10^5$ 实测 $<1$ ms。
- 复核状态：样例、250 组 DP 对拍、性能均实测通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 299A Ksusha and Array](https://codeforces.com/problemset/problem/299/A)：同场 A 题。
- [Codeforces 298B Sail](https://codeforces.com/problemset/problem/298/B)：同批 298 场。
- [Codeforces 339B Xenia and Ringroad](https://codeforces.com/problemset/problem/339/B)：另一类"能不能走到"的判定。

**延伸思考**：

1. 若允许**向后跳**，判据会怎么变？
2. 若每段石头的"代价"不同（例如踩到会扣分），就变成最短路问题——怎么建模？
3. 若 $k$ 随位置变化（第 $i$ 格能跳 $k_i$），还能 $O(n)$ 判定吗？
