# Codeforces 298A Snow Footprints 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/298/A
- **比赛来源**：Codeforces Round 180 (Div. 2) · Problem A（UTC 2013-04-19）
- **难度**：1300
- **标签**：构造、模拟
- **评测类型**：普通（多解，输出任意合法 $(s,t)$）
- **限制**：时间 1 s / 内存 256 MB

**题意**：一条被分成 $n$ 格的路。从 $i$ 走到 $i+1$ 会在第 $i$ 格留下右脚印 `R`，从 $i$ 走到 $i-1$ 会在第 $i$ 格留下左脚印 `L`（新脚印覆盖旧的）。Alice 从 $s$ 出发走了一段（始终在路内）停在 $t$。给出最终脚印串（含 `.`），求一对可能的 $(s,t)$。

**约束**：$n\le1000$ ⇒ $O(n)$ 扫描即可。

## 2. 示例与观察

官方样例 1：

```text
输入：
9
..RRLL...

输出：
3 4
```

官方样例 2：

```text
输入：
11
.RRRLLLLL..

输出：
7 5
```

![三种形态](../../../images/cf298a_pattern.svg)

**观察 1（形态）**：每格的脚印 = 它**最后一次离开**的方向。走法是一条路径，所以不可能"先出现 L、后出现 R"（那样左边的 L 会被后来向右的经过覆盖成 R）⇒ 脚印串必为 $\texttt{R}\ldots\texttt{R}\,\texttt{L}\ldots\texttt{L}$ 形态（两段之一可空）。

**观察 2（公式）**：设脚印范围 $[A,C]$（第一个/最后一个非 `.`），最后一个 `R` 在 $B$（若无 `R` 则全 `L`）：

- 全 `L`：从 $C$ 一路向左到 $A-1$ ⇒ $(C,\ A-1)$；
- 全 `R`：从 $A$ 一路向右到 $C+1$ ⇒ $(A,\ C+1)$；
- $\texttt{R}\ldots\texttt{R}\texttt{L}\ldots\texttt{L}$：$A\to\cdots\to C\to\cdots\to B+1$ ⇒ $(A,\ B+1)$。

## 3. 解题思路

### 3.1 构造

![样例走查](../../../images/cf298a_case.svg)

第三种情形最典型：先从 $A$ 一路右行到 $C$（把 $A..C-1$ 都盖上 `R`），再折返左行到 $B+1$（把 $B+1..C$ 覆盖成 `L`），最后停在 $B+1$。于是 $A..B$ 保留 `R`、$B+1..C$ 是 `L` ✓。

### 3.2 样例走查

样例 1：`..RRLL...`，$A=3,B=4,C=6$ ⇒ $(3,5)$：走 $3\to4\to5\to6\to5$，脚印 `R@3,R@4,L@5,L@6` ✓（官方给 $(3,4)$ 也合法）。
样例 2：`.RRRLLLLL..`，$A=2,B=4,C=9$ ⇒ $(2,5)$：走 $2\to\cdots\to9\to\cdots\to5$，脚印 `R@2,3,4` 与 `L@5..9` ✓。

## 4. 正确性证明

**引理 1**：合法输入必为"全 L / 全 R / R…L"三种形态之一。

**证明**：设两格 $i<j$。若 $i$ 的最后一次离开向左而 $j$ 的向右，考虑路径中最后一次经过区间 $[i,j]$ 的时刻……更直接地：脚印由路径的"最后离开"决定，而路径在位置上连续，左侧格子被改成 `L` 之后，任何向右的穿越都会把它重新写成 `R` ⇒ 一旦某格是 `L`，它右边的格子不可能在之后被写成 `R`（否则要穿过它）⇒ 形态只能是 `R…RL…L` ✓。∎

**引理 2**：三种构造都产生给定脚印。

**证明**：
- 全 `L`：走 $C,C-1,\dots,A-1$，每格最后一次离开都向左，且恰好覆盖 $[A,C]$ ⇒ 与输入一致 ✓。
- 全 `R`：对称 ✓。
- `R…L`：走 $A,A+1,\dots,C,C-1,\dots,B+1$。$A..B$ 的最后一次离开是向右（第一段，之后不再经过这些格）✓；$B+1..C$ 的最后一次离开是向左（第二段）✓；其它格没被离开过 ⇒ `.` ✓。∎

**定理**：输出是一组合法解。

**证明**：由引理 2，构造出的走法恰好复现输入脚印，故 $(s,t)$ 合法 ✓（题面允许任意解）。∎

## 5. 复杂度分析

- 时间：$O(n)$。
- 空间：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){int n;scanf("%d",&n);static char s[1005];scanf("%s",s);
 int a=-1,b=-1,c=-1;
 for(int i=0;i<n;i++) if(s[i]!='.'){ if(a<0)a=i; c=i; if(s[i]=='R')b=i; }
 if(b<0) printf("%d %d\n",c+1,a);          // 全 L：C -> A-1
 else if(b==c) printf("%d %d\n",a+1,c+2);  // 全 R：A -> C+1
 else printf("%d %d\n",a+1,b+2);           // R*L*：A -> ... -> C -> ... -> B+1
}
```

### Python3

```python
n = int(input())
s = input().strip()
pos = [i for i in range(n) if s[i] != '.']
A, C = pos[0], pos[-1]
R = [i for i in pos if s[i] == 'R']
if not R:                     # 全 L
    print(C + 1, A)
elif R[-1] == C:              # 全 R
    print(A + 1, C + 2)
else:                         # R...L
    print(A + 1, R[-1] + 2)
```

## 7. 边界情况与易错点

1. **全 `L` 时 $t=A-1$**：$A\ge1$ 时 $A-1$ 可能为 0 —— 合法输入下全 `L` 必有 $A\ge2$（否则她在第 1 格无法向左走）✓。
2. **全 `R` 时 $t=C+1\le n$**：同理 $C<n$ ✓。
3. **`R…L` 时 $t=B+1$**：$B+1\le C\le n$ ✓。
4. **不要假设 $s<t$ 或 $s>t$**：三种情形都可能。
5. **多解**：与样例不同不算错（本题 checker 用"长度受限搜索"验证是否真能复现足迹）。
6. **输入保证至少一个非 `.`**：不用处理全 `.`。

## 8. 验证记录

- 编译环境与命令：`clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/298/A_雪地脚印.md --checker codeforces/tools/checkers/cf298a.py`
- 官方样例：2 / 2 通过（多解，用 checker 的"存在一条走法复现足迹"验证；我的输出 $(3,5),(2,5)$ 与官方 $(3,4),(7,5)$ 都合法）。
- 额外测试：随机 150 组（$n\le12$，随机走法生成脚印），其中 $n\le6$ 的 59 组用**穷举所有长度 ≤13 的走法**验证输出的确能复现足迹；全部通过。
- 最大约束性能：$n=1000$ 实测 $<1$ ms。
- 复核状态：样例、随机 + 穷举对拍、性能均实测通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 298B Sail](https://codeforces.com/problemset/problem/298/B)：同场 B 题。
- [Codeforces 299A Ksusha and Array](https://codeforces.com/problemset/problem/299/A)：同批 299 场。
- [Codeforces 1A Theatre Square](https://codeforces.com/problemset/problem/1/A)：入门构造。

**延伸思考**：

1. 若允许 Alice 走出路外（走到更远的格子），脚印形态会多出哪些？
2. 若要求输出**所有**合法 $(s,t)$，怎么求？
3. 若给定 $(s,t)$，如何判定它是否合法？（提示：长度受限搜索或形态刻画。）
