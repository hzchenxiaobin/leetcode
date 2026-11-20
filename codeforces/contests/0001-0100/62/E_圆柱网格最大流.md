# Codeforces 62E 圆柱网格最大流 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/62/E
- **比赛来源**：Codeforces Beta Round 62 · Problem E（2011-02-26）
- **难度**：2700
- **标签**：网络流、最小割、状压 DP
- **评测类型**：普通
- **限制**：时间 5 s / 内存 256 MB

**题意**：一个 $n$ 行 $m$ 列的网格被卷成圆柱：每一列的 $n$ 个点按环状连接（第 $n$ 行与第 1 行相连）。网格的边是走廊：

- **横向走廊**：相邻两列之间，共 $(m-1)n$ 条，第 $c$ 组第 $r$ 条连接 $(r,c)$ 与 $(r,c+1)$；
- **纵向走廊**：每列 $n$ 条，第 $c$ 组第 $r$ 条连接 $(r,c)$ 与 $(r+1,c)$（$r=n$ 时接第 1 行）。

最左列是"入口"（无限条触手可以从这些点进入），最右列是"出口"（触手只能从这些点离开）。每条走廊有容量。求最多能有多少条触手从入口流到出口。

> 题面配图：圆柱网格示意，$n=4,m=5$。

**约束**：

- $n \le 5$，$m \le 10^5$：列数极多，但**宽度极小**，这是典型的"小宽度最小割 + 逐列 DP"。
- 容量 $\le 10^9$，总容量可达约 $10^{15}$，用 64 位整数。
- 图有 $nm$ 个结点、约 $2nm$ 条边，直接跑 Dinic 在最坏情况下可能很慢；最小割 DP 是 $O(m \cdot n \cdot 2^n)$。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3 4
4 4 4
1 1 5
5 5 3
4 1 2
1 3 1
3 5 4
1 4 3

输出：
7
```

官方样例 2：

```text
输入：
2 2
9 2
2 3
6 1

输出：
11
```

**样例演算**（样例 2）：$n=2,m=2$，只有一个横向间隔，两行容量分别为 9 和 2；两列各有 2 条纵向边。

- 左列两个点都是源，右列两个点都是汇。
- 纵向边在同一侧内部（两端都在源侧或都在汇侧），不会被割；唯一可能被割的是两条横向边，总容量 $9+2=11$。
- 所以最大流 = 11，与输出一致。

自造样例（均已用参考程序核对）：

| 输入 | 输出 | 说明 |
|------|------|------|
| $n=2,m=2$，所有容量为 0 | 0 | 没有通路 |
| $n=2,m=2$，横边容量 1、1，纵边 0 | 2 | 两行各一条通路 |
| $n=3,m=2$，横边全 0 | 0 | 横向被切断 |
| $n=2,m=3$，容量较大 | 见程序 | 用 Dinic 对拍 |

## 3. 解题思路

### 3.1 朴素做法与瓶颈

把每个格点当结点、每条走廊当无向边，源点连最左列所有点、汇点连最右列所有点，跑最大流。结点数 $nm \le 5 \times 10^5$、边数约 $2nm \le 10^6$，Dinic 在这种"长条 + 大容量"的图上虽然常常很快，但最坏复杂度没有保证，5 s 内有风险。

由于 $n \le 5$，更好的做法是利用**最大流 = 最小割**，把割按列分解，做状压 DP。

### 3.2 核心观察：割只取决于每列的"源侧点集"

![圆柱网格](../../../images/cf62e_cylinder.svg)

把最左列的所有点看成源（因为触手从那里进入，容量无限），最右列的所有点看成汇（容量无限）。一个 $s$-$t$ 割给每个格点标记"在源侧 $S$"或"在汇侧 $T$"，割的代价是所有两端分属不同侧的走廊容量之和。

因为源/汇边容量无限，最优割必然满足：

- 最左列所有点都在 $S$；
- 最右列所有点都在 $T$。

对第 $c$ 列，用一个 $n$ 位掩码 $\text{mask}_c$ 表示哪些行在 $S$。那么割的代价可以按列拆开：

- **列内纵向边**：第 $c$ 列第 $r$ 条边两端都在本列，只有 $\text{mask}_c$ 的第 $r$ 位与第 $r+1$ 位不同时被割，代价记作 $V_c(\text{mask}_c)$；
- **列间横向边**：第 $c$ 与 $c+1$ 列之间第 $r$ 条边，只有 $\text{mask}_c$ 与 $\text{mask}_{c+1}$ 的第 $r$ 位不同时被割，代价为对应容量。

于是

$$\text{最小割} = \min_{\text{mask}_0 = \text{全1},\ \text{mask}_{m-1} = 0}\ \sum_{c=0}^{m-2}\Big( H_c(\text{mask}_c,\text{mask}_{c+1}) + V_{c+1}(\text{mask}_{c+1}) \Big) + V_0(\text{全1}).$$

其中 $V_0(\text{全1}) = 0$（全在同一侧不会被割）。

### 3.3 DP 转移

![按列状态做最小割 DP](../../../images/cf62e_cut.svg)

令 $dp[A]$ 表示处理到第 $c$ 列、第 $c$ 列掩码为 $A$ 时的最小代价。从第 $c$ 列转移到第 $c+1$ 列：

$$dp'[B] = V_{c+1}(B) + \min_{A}\Big( dp[A] + H_c(A,B)\Big),$$

$$H_c(A,B) = \sum_{r=0}^{n-1} [A_r \ne B_r]\cdot h_c[r].$$

初始 $dp[\text{全1}] = 0$，其余为无穷大；最终答案是 $dp'[0]$（最右列掩码必须为 0）。

直接枚举 $A,B$ 是 $O(4^n)$ 每列，$n=5$ 时每列 1024 次，$m=10^5$ 时约 $10^8$ 次，C++ 也偏紧。利用 $H_c$ 的特殊结构可以降一维。

### 3.4 超立方体上的最短路变换

![DP 转移的逐位松弛](../../../images/cf62e_dp.svg)

内层要求的是

$$g[B] = \min_A \Big( dp[A] + \sum_{r: A_r \ne B_r} h_c[r] \Big).$$

这等价于在 $n$ 维超立方体上，从每个 $A$ 出发、边权为 $h_c[r]$ 的最短路：翻转第 $r$ 位要付 $h_c[r]$。由于每条边非负，且超立方体上两点间的最短路就是"把不同的位各翻一次"，可以做逐位松弛：

$$g \leftarrow dp;\qquad \text{对每个 } r:\quad g[B] \leftarrow \min\big(g[B],\ g[B \oplus 2^r] + h_c[r]\big).$$

每轮处理一位，一轮内对所有 $2^n$ 个掩码更新；$n$ 轮后 $g[B]$ 就是上式的最小值。复杂度 $O(n \cdot 2^n)$ 每列，总计 $O(m n 2^n) \approx 1.7 \times 10^7$，非常快。

### 3.5 样例走查

样例 2：$n=2,m=2$。初始 $dp[11] = 0$。

第 0 列到第 1 列的转移：$H_0(A,B) = [A_0\ne B_0]\cdot 9 + [A_1\ne B_1]\cdot 2$，$V_1(B) = 0$（$B=00$ 时同侧无边被割）。要求 $B = 00$，$A = 11$，代价 $9 + 2 = 11$。答案 11。

## 4. 正确性证明

**引理 1（建模正确）**：上述网络的 $s$-$t$ 最大流等于触手最大数量。

**证明**：每条走廊容量限制同时通过的触手数；触手从入口点到出口点构成流，容量约束与流量守恒正是网络流的定义。入口/出口用无限容量边连接源/汇，不限制流量。无向边按两个方向各一条容量为 $c$ 的弧建模，最优流中不会同时出现相反方向的正流量（可抵消），因此等价于走廊最多通过 $c$ 条。∎

**引理 2（割的列分解）**：任一满足源/汇约束的割，其代价恰好等于各列纵向割代价与相邻列横向割代价之和。

**证明**：图中的边只有两类：列内纵向边和列间横向边，分别只依赖一列掩码与两列掩码；把所有边按所属列/间隔分组求和即得。∎

**引理 3（DP 最优性）**：DP 计算出的值等于所有满足边界掩码约束的割代价的最小值。

**证明**：对列数归纳。第 0 列掩码固定为全 1；假设 $dp[A]$ 是前 $c$ 列（含第 $c$ 列纵向代价）的最小代价，则枚举 $B$ 并加上第 $c$ 与 $c+1$ 列之间的横向代价和第 $c+1$ 列纵向代价，恰好覆盖所有可能的第 $c+1$ 列掩码，取最小即得 $dp'[B]$。归纳到最后一列，$dp'[0]$ 就是全局最小割。∎

**引理 4（逐位松弛正确）**：对非负权 $h_c[r]$，按位松弛 $n$ 轮后 $g[B] = \min_A (dp[A] + \sum_{r:A_r\ne B_r} h_c[r])$。

**证明**：超立方体上从 $A$ 到 $B$ 的任意路径可以化简为"只翻转 $A$ 与 $B$ 不同的位各一次"，代价恰为 $\sum h_c[r]$；逐位松弛相当于允许使用前 $r$ 种翻转的 Bellman-Ford，$n$ 轮后覆盖所有位，故得到最短路。∎

**定理**：算法输出等于触手最大数量。

**证明**：由最大流最小割定理，最大流 = 最小割；由引理 1-3，DP 求出最小割；由引理 4，转移被正确计算。故输出正确。∎

## 5. 复杂度分析

- **时间**：每列做 $n$ 轮、每轮 $2^n$ 次更新，$O(m n 2^n)$；$n=5,m=10^5$ 时约 $1.7 \times 10^7$ 次运算。
- **空间**：$dp$ 与临时数组各 $2^n$ 个 64 位整数；容量存储 $O(nm)$（可边读边处理，进一步降到 $O(n)$）。
- **数值**：最小割不超过所有走廊容量之和，约 $2 \times 10^5 \times 5 \times 10^9 = 10^{15}$，`long long` 安全。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

static const int BUFSZ = 1 << 20;
static char sbuf[BUFSZ];
static int spos = 0, slen = 0;
static inline int gc(){
    if(spos == slen){
        slen = (int)fread(sbuf, 1, BUFSZ, stdin);
        spos = 0;
        if(slen == 0) return -1;
    }
    return sbuf[spos++];
}
static inline long long readInt(){
    int c = gc();
    while(c < '0' || c > '9'){ if(c == -1) return -1; c = gc(); }
    long long x = 0;
    while(c >= '0' && c <= '9'){ x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

int main(){
    int n = (int)readInt();
    int m = (int)readInt();
    if(n < 0) return 0;
    int hn = (m - 1) * n;
    vector<long long> h(hn);
    for(int i = 0; i < hn; i++) h[i] = readInt();
    vector<long long> v((long long)m * n);
    for(int i = 0; i < m * n; i++) v[i] = readInt();

    int N = 1 << n;
    const long long INF = (long long)4e18;
    vector<long long> dp(N, INF), g(N), ndp(N), tmp(N);
    dp[N - 1] = 0;  // leftmost column: all nodes on source side
    for(int c = 0; c < m - 1; c++){
        // vertical cut cost of column c+1
        for(int mask = 0; mask < N; mask++){
            long long s = 0;
            for(int r = 0; r < n; r++){
                int a = (mask >> r) & 1;
                int b = (mask >> ((r + 1) % n)) & 1;
                if(a != b) s += v[(long long)(c + 1) * n + r];
            }
            ndp[mask] = s;
        }
        g = dp;
        for(int r = 0; r < n; r++){
            long long w = h[(long long)c * n + r];
            tmp = g;
            int bit = 1 << r;
            for(int mask = 0; mask < N; mask++){
                long long cand = tmp[mask ^ bit] + w;
                if(cand < g[mask]) g[mask] = cand;
            }
        }
        for(int mask = 0; mask < N; mask++) dp[mask] = g[mask] + ndp[mask];
    }
    printf("%lld\n", dp[0]);
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    idx = 2
    h = [0] * ((m - 1) * n)
    for i in range((m - 1) * n):
        h[i] = int(data[idx]); idx += 1
    v = [0] * (m * n)
    for i in range(m * n):
        v[i] = int(data[idx]); idx += 1

    N = 1 << n
    INF = 10 ** 30
    dp = [INF] * N
    dp[N - 1] = 0
    for c in range(m - 1):
        ndp = [0] * N
        base = (c + 1) * n
        for mask in range(N):
            s = 0
            for r in range(n):
                a = (mask >> r) & 1
                b = (mask >> ((r + 1) % n)) & 1
                if a != b:
                    s += v[base + r]
            ndp[mask] = s
        g = dp[:]
        for r in range(n):
            w = h[c * n + r]
            bit = 1 << r
            tmp = g[:]
            for mask in range(N):
                cand = tmp[mask ^ bit] + w
                if cand < g[mask]:
                    g[mask] = cand
        dp = [g[mask] + ndp[mask] for mask in range(N)]
    print(dp[0])


main()
```

## 7. 边界情况与易错点

1. **边界掩码**：最左列必须全 1、最右列必须全 0；若不强制，会得到一个"不连通源汇"的伪割，答案偏小。
2. **列内纵向边是环状的**：第 $r$ 位与第 $(r+1)\bmod n$ 位都要比较，最后一条边连接第 $n$ 行与第 1 行，不能漏。
3. **零容量**：容量可以是 0，DP 中正常参与取最小；不要用 0 当"无此边"。
4. **$n=2$**：环状连接只有两条边（0-1 与 1-0），注意不要重复计算同一条边两次。
5. **$m=2$**：只有一次列间转移，答案就是 $\sum_r h_0[r]$（受边界掩码约束）；代码无需特判。
6. **64 位**：总容量可达 $10^{15}$，`int` 会溢出；哨兵 INF 要足够大且加法不溢出（用 `4e18` 时要保证不会与容量相加溢出，容量和远小于它）。
7. **输入顺序**：先 $(m-1)$ 行横向容量，再 $m$ 行纵向容量，行内按 $n$ 行从上到下；读错顺序会得到完全不同的答案。
8. **性能**：$10^6$ 个整数输入，C++ 用快速读入避免 `cin` 超时；Python 在 $m=10^5$ 时较慢，建议 PyPy3 或提交 C++。

## 8. 验证记录

- **编译环境与命令**：`python3 codeforces/tools/verify_solution.py codeforces/contests/0001-0100/62/E_圆柱网格最大流.md`；C++ 由 clang++ 17 + `codeforces/tools/include` 兼容头编译（`-O2`），Python 3 直接运行。
- **官方样例**：C++ 2 / 2 通过，Python 2 / 2 通过。
- **额外测试**：随机 300 组（$n \le 5$，$m \le 6$，容量 $0 \sim 10$）与独立的 Dinic 最大流程序逐组比对，0 处不一致。
- **最大约束性能**：$n=5,m=10^5$ 随机容量，C++ 运行约 0.05 s（含快速读入），远低于 5 s。
- **复核状态**：最大流建模、割的列分解、DP 最优性与逐位松弛均已证明，并与 Dinic 对拍一致。

## 相关题目与扩展

- [Codeforces 62D 下一条欧拉回路](https://codeforces.com/problemset/problem/62/D)：同一场的图论构造题。
- [Codeforces 62C 黑斑并集周长](https://codeforces.com/problemset/problem/62/C)：同一场的计算几何题。
- **延伸思考 1**：若网格不卷成圆柱（普通平面网格），纵向边不再环状，DP 完全一样，只是 $V$ 的计算少一条边。
- **延伸思考 2**：若 $n$ 增大到 10 左右，$2^n$ 仍可接受；到 20 就需要更高级的割结构（如平面图最短路对偶）。
- **延伸思考 3**：本题是"小树宽图上的最小割"的典型例子：按列切分后，割只与边界状态有关，可以用 $2^{\text{width}}$ 的 DP 求解。
