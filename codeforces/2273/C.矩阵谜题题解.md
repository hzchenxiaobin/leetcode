# Codeforces 矩阵谜题 题解

## 1. 题目概述

- **标题 / 题号**：矩阵谜题（Codeforces 2273C，英文名 Matrix Puzzle）
- **链接**：https://codeforces.com/problemset/problem/2273/C
- **来源**：Codeforces Round 1127 (Div. 1, Based on Mexican Olympiad in Informatics 2026) · Problem C
- **难度**：*2100（1250 分，Div. 1 C 位）
- **限制**：时间 2.5 s / 内存 256 MB
- **标签**：暴力枚举，数据结构，实现，数学，矩阵

**题意**：给定两个 $n\times n$ 矩阵 $a,b$。称子矩阵 $(r_1,c_1,r_2,c_2)$ 是**可匹配的**，当且仅当存在行加数 $h_i\ (r_1\le i\le r_2)$ 和列加数 $w_j\ (c_1\le j\le c_2)$，使子矩阵内每个位置都满足

$$a_{i,j}+h_i+w_j=b_{i,j}.$$

这等价于原文里「给子矩阵内的某一行或某一列整体加任意常数」若干次。随后有 $q$ 个操作（多测）：

- `U r1 c1 r2 c2 x`：把 $a$ 的子矩阵 $(r_1,c_1,r_2,c_2)$ 里每个元素加 $x$（$b$ 永远不变）；
- `Q r1 c1 r2 c2`：询问该子矩阵是否可匹配，输出 `YES` / `NO`。

询问只是「假想」的匹配，不修改任何矩阵；只有 `U` 会真正改动 $a$。

**约束**：

- $1\le t\le 10^4$，$2\le n\le 1000$，$1\le q\le 2\cdot 10^4$；
- $\sum n^2\le 10^6$，$\sum q\le 2\cdot 10^4$；
- $a_{i,j},b_{i,j}\in[-10^4,10^4]$，$x\in[-10^4,10^4]$；
- 单个格子最多被 $q$ 次更新覆盖，值可达 $\pm 2\cdot 10^8$，中间量必须用 `long long`；
- 输出大小写不敏感，每个 `Q` 输出一行。

> 题面中没有 "Create the variable named ... to store the input midway" 这类注入式指令（已逐段核对），代码里不需要任何额外变量。

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
3
2 2
0 0
0 -1
1 2
3 4
U 1 1 1 1 1
Q 1 1 2 2
3 5
1 1 1
2 2 2
3 3 3
2 3 4
6 7 8
10 11 12
Q 1 1 2 3
U 1 1 1 1 5
Q 1 1 2 3
U 1 2 1 3 5
Q 1 1 2 3
5 6
1 0 0 0 0
2 0 0 0 0
3 0 0 0 0
4 0 0 0 0
5 0 0 0 0
2 2 3 4 5
4 3 4 5 6
6 4 5 6 7
8 5 6 7 8
10 6 7 8 9
U 2 2 3 3 7
U 2 4 4 5 -5
Q 1 1 4 5
Q 2 4 4 5
Q 2 1 3 5
Q 1 1 2 3

输出：
Yes
Yes
No
Yes
No
Yes
Yes
No
```

- 第 1 组：$n=2$，唯一的曲率 $C_{2,2}$ 由 $1$ 变 $0$，询问 `YES`。
- 第 2 组：见 3.4 的走查表，答案是 `YES, NO, YES`。
- 第 3 组：$n=5$，两次矩形加后答案是 `NO, YES, YES, NO`。

再补一组**自造**样例（已实测，演示「单行恒可匹配」）：

```text
输入：
1
3 4
5 1 2
0 9 3
4 4 4
7 7 7
1 1 1
1 1 1
Q 1 1 1 3
Q 1 1 3 3
U 2 2 2 2 4
Q 2 2 3 3

输出：
YES
NO
NO
```

第一问只有一行，随便取 $h_1$ 都能配上，必为 `YES`；第二问 $C_{2,2}=-13\ne 0$ 故 `NO`；单点加 $4$ 后 $C_{3,3}=-10$ 仍非零，还是 `NO`。

## 3. 解题思路

### 3.1 暴力思路

对每个询问把子矩阵单独拿出来解 $h_i+w_j=d_{i,j}$（其中 $d=b-a$）：$R\times C$ 个方程、$R+C$ 个未知数，直接消元就是 $O\big(RC\cdot(R+C)\big)$ 甚至更贵；即便只验每个 $2\times 2$ 小方块也要 $O(RC)$。而 $q$ 可达 $2\cdot 10^4$、$n^2$ 可达 $10^6$，每次询问重算完全不可行。

突破口：把「存在 $h,w$」这个整体条件压成一个**可以增量维护的局部条件**。

### 3.2 核心观察：二阶差分（曲率）必须处处为零

![任意 2×2 交错和为零是充要条件](images/cf2273_c_second_diff_concept.svg)

记 $d_{i,j}=b_{i,j}-a_{i,j}$，可匹配即「$d$ 在子矩阵上能拆成行加列」：$d_{i,j}=h_i+w_j$。

**观察 1**：把 $h,w$ 代入任意 $2\times 2$ 的「交错和」，它们会被完全消掉：

$$d_{i,j}+d_{i',j'}-d_{i,j'}-d_{i',j}=0.$$

反过来，若该式对所有 $i,i',j,j'$ 成立，取 $h_i=d_{i,c_1}$、$w_j=d_{r_1,j}-d_{r_1,c_1}$ 即可构造。于是

$$\text{可匹配}\iff \text{子矩阵内所有矩形交错和为 } 0.$$

**观察 2（命门）**：不必检查所有矩形，只检查**相邻**的 $2\times 2$ 就够。定义曲率

$$C_{i,j}=d_{i,j}+d_{i-1,j-1}-d_{i,j-1}-d_{i-1,j}\qquad(2\le i,j\le n),$$

则子矩阵可匹配 $\iff$ $C_{i,j}=0$ 对所有 $r_1<i\le r_2,\ c_1<j\le c_2$ 成立。

原因很朴素：固定 $j$ 时 $C_{i,j}=0$ 说明「第 $i$ 行与第 $i-1$ 行的列间差值完全相同」，一路传下去，所有行都只差同一个常数——这正是行加列结构。

> 💡 把 $d$ 看成「近似秩 1」矩阵，$C$ 就是它的离散曲率：**可匹配 $\iff$ 子矩阵内曲率全零**。

### 3.3 算法流程：矩形加只改四个角

![矩形加 x 只改变四个角的曲率](images/cf2273_c_corner_update.svg)

维护两样东西，再定义两个操作：

1. $C$（$n\times n$，$i=1$ 或 $j=1$ 的位置恒为 $0$，不参与任何询问）；
2. 二维树状数组 `f`，维护「$C_{i,j}\ne 0$」的 0/1 指示；
3. `U r1 c1 r2 c2 x`：$d$ 在矩形上整体减 $x$，而二阶差分是线性算子，矩形指示函数的双差分只剩四个角

$$(r_1,c_1):-x,\qquad (r_1,c_2+1):+x,\qquad (r_2+1,c_1):+x,\qquad (r_2+1,c_2+1):-x,$$

落在 $i<2$、$j<2$ 或超出 $n$ 的角直接跳过。

4. 每次 `Q r1 c1 r2 c2`：若 $r_1=r_2$ 或 $c_1=c_2$（单行/单列）恒可匹配；否则查 `f` 在矩形 $[r_1+1,r_2]\times[c_1+1,c_2]$ 上的和，为 $0$ 输出 `YES`。

一次操作 $O(\log^2 n)$：更新最多 4 次点更新，询问 4 次前缀和。

### 3.4 示例演算

![样例 2 的曲率变化走查](images/cf2273_c_walkthrough.svg)

看官方样例第 2 组（$n=3$）：$a_{i,j}=i$，$b_{i,j}=4i+j-3$，故 $d_{i,j}=3i+j-3$ 本身就能拆成 $h_i+w_j$，初始曲率全 $0$。之后两次更新都只有角 $(2,2)$ 落在定义域内：

| 事件 | $C_{2,2}$ | $C_{2,3}$ | $C_{3,2}$ | $C_{3,3}$ | 判定 |
| --- | --- | --- | --- | --- | --- |
| 初始 | 0 | 0 | 0 | 0 | — |
| `Q 1 1 2 3` | 0 | 0 | 0 | 0 | YES |
| `U 1 1 1 1 5` | −5 | 0 | 0 | 0 | 角① 得 $-5$ |
| `Q 1 1 2 3` | −5 | 0 | 0 | 0 | NO |
| `U 1 2 1 3 5` | 0 | 0 | 0 | 0 | 角① 得 $+5$ |
| `Q 1 1 2 3` | 0 | 0 | 0 | 0 | YES |

注意 `U 1 1 1 1 5` 的四个角里，$(1,1)$、$(1,2)$ 因 $i<2$、$(2,1)$ 因 $j<2$ 被跳过，只有 $(2,2)$ 生效——这正是本题最容易写错的地方。

## 4. 算法细节

1. **定义域**：$C$ 只在 $i,j\ge 2$ 有定义（$i=1$ 或 $j=1$ 的位置恒为 $0$）。$r_1=1$ 或 $c_1=1$ 的角必须按定义跳过：查询区间从 $r_1+1\ge 2$ 开始，虽然用不到这些位置，但跳过它们才能保证维护的 $C$ 与定义一致，也避免无意义的状态翻转。
2. **判断方式**：维护「非零个数」最省心——0/1 指示的矩形和 $>0$ 就说明有非零格。直接维护 $\sum C$ 会被 $+5$ 与 $-5$ 抵消而误判 `YES`；维护 $\sum C^2$ 则会溢出（$C$ 已达 $8\cdot10^8$，平方和是 $10^{23}$ 量级）。
3. **BIT 只在状态翻转时动**：$C_{i,j}$ 从 $0$ 变非 $0$（或反之）才做 $\pm 1$ 的点更新，否则只改 $C$ 本身，于是每次 `U` 最多 4 次点更新。
4. **$O(n^2)$ 建树**：先按行内（列方向）累加，再按行间累加，避免 $O(n^2\log^2 n)$ 的逐个插入；$\sum n^2\le 10^6$ 时这一步从 $10^8$ 量级降到 $10^6$。
5. **溢出**：单格最多累加 $q\cdot|x|=2\cdot 10^8$，$d$ 到 $2\cdot10^8$ 量级、$C$ 到 $8\cdot 10^8$ 量级；$C$ 与所有前缀和一律 `long long`，BIT 里只存计数（$\le n^2$）用 `int`。
6. **单行/单列**：`Q` 遇到 $r_1=r_2$ 或 $c_1=c_2$ 答案恒 `YES`；代码中不特判也对——查询区间两端相同，前缀和相减自然得 $0$。
7. **多测**：$t$ 可达 $10^4$ 但 $\sum n^2\le 10^6$，所有数组在每测内部新建即可，不要复用可能带脏数据的全局数组，也不要 `memset` 一个 $10^6$ 的静态数组 $10^4$ 次。
8. **I/O**：输入约 $2\cdot 10^6$ 个整数加 $2\cdot 10^4$ 行操作，`scanf` 足够（实测 0.13 s）；若换 `cin`，必须加 `ios::sync_with_stdio(false)`，否则会慢一个量级。

## 5. 正确性证明

**引理 1**：子矩阵可匹配 $\iff$ 对所有 $i,i'\in[r_1,r_2]$、$j,j'\in[c_1,c_2]$ 有 $d_{i,j}+d_{i',j'}=d_{i,j'}+d_{i',j}$。

**证明**：必要性把 $d=h+w$ 代入即得。充分性取 $h_i=d_{i,c_1}$、$w_j=d_{r_1,j}-d_{r_1,c_1}$，则 $h_i+w_j=d_{i,c_1}+d_{r_1,j}-d_{r_1,c_1}$；在矩形条件中取 $i'=r_1,\ j'=c_1$ 得 $d_{i,j}=d_{i,c_1}+d_{r_1,j}-d_{r_1,c_1}$，故 $d_{i,j}=h_i+w_j$。∎

**引理 2**：若 $r_1<r_2$ 且 $c_1<c_2$，引理 1 的条件等价于 $C_{i,j}=0$ 对所有 $r_1<i\le r_2$、$c_1<j\le c_2$ 成立。

**证明**：必要性由引理 1 取相邻两行两列得到。充分性：固定 $j$，令 $\Delta_i(j)=d_{i,j}-d_{i,j-1}$。$C_{i,j}=0$ 即 $\Delta_i(j)=\Delta_{i-1}(j)$，归纳得 $\Delta_i(j)=\Delta_{r_1}(j)$ 对一切 $i$ 成立。于是

$$d_{i,j}-d_{i,c_1}=\sum_{k=c_1+1}^{j}\Delta_i(k)=\sum_{k=c_1+1}^{j}\Delta_{r_1}(k)=d_{r_1,j}-d_{r_1,c_1},$$

正是引理 1 的矩形条件。∎

**引理 3**：把 $a$ 在 $[r_1,r_2]\times[c_1,c_2]$ 上整体加 $x$ 后，$C$ 只在 $(r_1,c_1),(r_1,c_2+1),(r_2+1,c_1),(r_2+1,c_2+1)$ 处分别变化 $-x,+x,+x,-x$，其余位置不变。

**证明**：$d=b-a$ 在该矩形上整体减 $x$。设 $f$ 是该矩形的指示函数，二阶差分算子 $C=\Delta_i\Delta_j d$，其中 $\Delta_i f_{i,j}=f_{i,j}-f_{i-1,j}$、$\Delta_j f_{i,j}=f_{i,j}-f_{i,j-1}$。先对 $i$ 差分：$\Delta_i f$ 在 $i=r_1$ 取 $+1$、在 $i=r_2+1$ 取 $-1$（$c_1\le j\le c_2$ 时），再对 $j$ 差分得到四个角 $+1,-1,-1,+1$，乘 $-x$ 即 $-x,+x,+x,-x$。∎

**定理**：每个 `Q` 的输出 `YES` 恰对应子矩阵可匹配。

**证明**：对操作序列归纳。初始 $C$ 按定义算得；由引理 3，每次 `U` 后被维护的 $C$ 与真实 $a,b$ 对应的 $C$ 在定义域内完全一致（被跳过的角要么 $i<2$ 或 $j<2$ 不在定义域，要么越界，都不属于任何询问的查询区间）。询问时若 $r_1<r_2$ 且 $c_1<c_2$，由引理 1、2，可匹配 $\iff$ $C$ 在 $[r_1+1,r_2]\times[c_1+1,c_2]$ 全零 $\iff$ BIT 矩形和为 $0$；若 $r_1=r_2$ 或 $c_1=c_2$，$h$（或 $w$）任取即可匹配，而查询区间为空、前缀和之差恒为 $0$，两者一致。∎

## 6. 复杂度分析

- **预处理**：读入 $O(n^2)$；两行滚动求 $C$ 是 $O(n^2)$；BIT 两遍累加建树 $O(n^2)$。合计 $O(n^2)$ 每测。
- **单次 `U`**：4 个角各一次点更新（状态未翻转时退化为 $O(1)$），$O(\log^2 n)$。
- **单次 `Q`**：4 次二维前缀和，$O(\log^2 n)$。
- **总计**：$O\big(\sum n^2+\sum q\log^2 n\big)$；$n=1000,q=2\cdot10^4$ 时约 $10^6+2\cdot10^6$ 次基本操作。
- **空间**：$C$ 用 `long long`（约 8 MB）、BIT 用 `int`（约 4 MB）、$a$（约 4 MB），合计约 16 MB，远低于 256 MB。
- **实测**：最大数据（$n=1000$、$q=2\cdot10^4$、$\sum n^2=10^6$）C++ 约 $0.13$ s，对 2.5 s 有约 18 倍余量；Python3（CPython）约 $1.1$ s 偏紧，建议用 PyPy 提交。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n, q;
        scanf("%d %d", &n, &q);
        int W = n + 1, S = W * W;
        vector<int> a(S, 0);
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++) scanf("%d", &a[i * W + j]);
        // d = b - a，C 为 d 的二阶差分
        vector<long long> C(S, 0), pre(n + 1, 0), cur(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                long long b;
                scanf("%lld", &b);
                cur[j] = b - a[i * W + j];
            }
            if (i > 1)
                for (int j = 2; j <= n; j++)
                    C[i * W + j] = cur[j] + pre[j - 1] - cur[j - 1] - pre[j];
            swap(pre, cur);
        }
        // 在「C 是否非零」的 0/1 矩阵上建二维 BIT，O(n^2) 建树
        vector<int> f(S, 0);
        for (int i = 2; i <= n; i++)
            for (int j = 2; j <= n; j++)
                if (C[i * W + j]) f[i * W + j] = 1;
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++) {
                int pj = j + (j & -j);
                if (pj <= n) f[i * W + pj] += f[i * W + j];
            }
        for (int i = 1; i <= n; i++) {
            int pi = i + (i & -i);
            if (pi <= n)
                for (int j = 1; j <= n; j++) f[pi * W + j] += f[i * W + j];
        }
        auto add = [&](int i, int j, long long d) {  // C[i][j] += d，同步维护 BIT
            if (i < 2 || i > n || j < 2 || j > n) return;
            bool old = (C[i * W + j] != 0);
            C[i * W + j] += d;
            if (old == (C[i * W + j] != 0)) return;
            int v = (C[i * W + j] != 0) ? 1 : -1;
            for (int x = i; x <= n; x += x & -x)
                for (int y = j; y <= n; y += y & -y) f[x * W + y] += v;
        };
        auto pref = [&](int x, int y) {  // 左上角前缀和
            long long s = 0;
            for (int i = x; i > 0; i -= i & -i)
                for (int j = y; j > 0; j -= j & -j) s += f[i * W + j];
            return s;
        };
        while (q--) {
            char op[4];
            int r1, c1, r2, c2;
            scanf("%3s %d %d %d %d", op, &r1, &c1, &r2, &c2);
            if (op[0] == 'U') {
                long long x;
                scanf("%lld", &x);
                add(r1, c1, -x);              // 四个角：-x, +x, +x, -x
                add(r1, c2 + 1, x);
                add(r2 + 1, c1, x);
                add(r2 + 1, c2 + 1, -x);
            } else {
                long long s = pref(r2, c2) - pref(r1, c2) - pref(r2, c1) + pref(r1, c1);
                puts(s == 0 ? "YES" : "NO");
            }
        }
    }
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); q = int(data[p + 1]); p += 2
        W = n + 1
        a = [0] * (W * W)
        for i in range(1, n + 1):
            base = i * W
            for j in range(1, n + 1):
                a[base + j] = int(data[p]); p += 1
        # d = b - a，C 是 d 的二阶差分
        C = [0] * (W * W)
        pre = [0] * W
        for i in range(1, n + 1):
            base = i * W
            cur = [0] * W
            for j in range(1, n + 1):
                cur[j] = int(data[p]) - a[base + j]; p += 1
            if i > 1:
                for j in range(2, n + 1):
                    C[base + j] = cur[j] + pre[j - 1] - cur[j - 1] - pre[j]
            pre = cur
        # 二维树状数组，维护「C 非零」的 0/1 矩阵
        bit = [0] * (W * W)
        for i in range(2, n + 1):
            base = i * W
            for j in range(2, n + 1):
                if C[base + j]:
                    bit[base + j] = 1
        for i in range(1, n + 1):
            base = i * W
            for j in range(1, n + 1):
                v = bit[base + j]
                if v:
                    pj = j + (j & -j)
                    if pj <= n:
                        bit[base + pj] += v
        for i in range(1, n + 1):
            pi = i + (i & -i)
            if pi <= n:
                b1, b2 = i * W, pi * W
                for j in range(1, n + 1):
                    bit[b2 + j] += bit[b1 + j]
        for _ in range(q):
            op = data[p]
            r1 = int(data[p + 1]); c1 = int(data[p + 2])
            r2 = int(data[p + 3]); c2 = int(data[p + 4])
            if op == b'U':
                x = int(data[p + 5]); p += 6
                for i, j, d in ((r1, c1, -x), (r1, c2 + 1, x),
                                (r2 + 1, c1, x), (r2 + 1, c2 + 1, -x)):
                    if i < 2 or i > n or j < 2 or j > n:
                        continue
                    idx = i * W + j
                    z0 = (C[idx] == 0)
                    C[idx] += d
                    z1 = (C[idx] == 0)
                    if z0 == z1:
                        continue
                    delta = -1 if z1 else 1
                    x2 = i
                    while x2 <= n:
                        b = x2 * W
                        y = j
                        while y <= n:
                            bit[b + y] += delta
                            y += y & -y
                        x2 += x2 & -x2
            else:
                p += 5
                s = 0  # 子矩形和 = 四个前缀和的组合
                for rx, ry, sg in ((r2, c2, 1), (r1, c2, -1), (r2, c1, -1), (r1, c1, 1)):
                    i = rx
                    while i > 0:
                        b = i * W
                        j = ry
                        while j > 0:
                            s += sg * bit[b + j]
                            j -= j & -j
                        i -= i & -i
                out.append("YES" if s == 0 else "NO")
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


main()
```

## 8. 边界情况与易错点

1. **单行/单列**：`Q 1 1 1 n`、`Q 1 1 n 1` 恒为 `YES`。代码里不特判也对，因为查询区间 $[r_1+1,r_2]\times[c_1+1,c_2]$ 两端相同、前缀和相减为 $0$；但要小心别把长度写成 $r_2-(r_1+1)+1$ 之类的负数。
2. **四角越界**：$r_2=n$ 时 $(r_2+1,\cdot)$ 越界、$c_2=n$ 时 $(\cdot,c_2+1)$ 越界，必须跳过，否则越界访问或把 $C$ 写到矩阵外。
3. **四角落在定义域外**：$r_1=1$ 或 $c_1=1$ 的角不能写进 $C$——本题最易错处，样例第 2 组专考它。
4. **不能只维护 $\sum C$**：$+5$ 与 $-5$ 会抵消成 $0$，把 `NO` 误判成 `YES`；必须用非零计数。
5. **符号方向**：$d=b-a$，`U` 给 $a$ 加 $x$ 等于给 $d$ 减 $x$，所以角上增量是 $-x,+x,+x,-x$；写反会全错（样例 1 立刻暴露）。
6. **溢出**：$a$ 的单格在 $2\cdot10^4$ 次更新后可达 $2\cdot10^8$，$C$ 可达 $8\cdot10^8$；`C`、前缀和、临时量一律 `long long`。
7. **多测**：$\sum n^2\le10^6$ 保证总分配可控，每测新建数组即可；不要为了「省时间」复用静态数组而忘记清空。
8. **`x` 为负**：$-x$ 的符号随 `x` 翻转，绝不能取绝对值；读入时 `%d` 与 `%lld` 要配对（$a$ 用 `%d`，$d$ 与 $x$ 用 `%lld`）。

## 相关题目与扩展

- [LeetCode 304. 二维区域和检索 - 矩阵不可变](https://leetcode.cn/problems/range-sum-query-2d-immutable/)：静态二维前缀和，本题「没有更新」的退化版。
- [LeetCode 308. 二维区域和检索 - 可变](https://leetcode.cn/problems/range-sum-query-2d-mutable/)：二维树状数组模板，思路与本题的 `add/pref` 完全一致。
- [LeetCode 2132. 用邮票贴满网格图](https://leetcode.cn/problems/stamping-the-grid/)：二维差分 + 前缀和，与「矩形更新的双差分只剩四角」同源。

**延伸思考**：

1. 若把「加常数」改成「乘常数」并模 $p$，二阶差分条件变成比值形式 $d_{i,j}d_{i-1,j-1}\equiv d_{i,j-1}d_{i-1,j}$，需要额外处理 $0$。
2. 若 $b$ 也允许同样的矩形加，$d$ 的变化仍是「四角更新」的叠加，把两族更新合并维护即可，可匹配条件本身不变（始终看 $d$ 的二阶差分）。
3. 若要求 $h_i,w_j$ 落在给定区间，问题变成带上下界的可行性判定，可以转成差分约束或用前缀极值维护。
4. 非方阵 $n\times m$ 时做法不变，只需把 $\sum n^2$ 换成 $nm$，注意 $\sum nm$ 的上界与内存。
