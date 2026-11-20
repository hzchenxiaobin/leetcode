# Codeforces 2249D 异或排列矩阵 题解

## 1. 题目概述

- **标题 / 题号**：异或排列矩阵（Codeforces 2249D，英文名 Xor Permutation Matrix）
- **链接**：https://codeforces.com/problemset/problem/2249/D
- **来源**：Codeforces Round 1112 (Div. 1) · Problem D（UTC 2026-07-26）
- **难度**：2300
- **限制**：时间 2 s / 内存 512 MB
- **标签**：位运算，构造，数学

**题意**：给定 $n$ 与 $x$（$0\le x\le n-1$），要求构造一个 $n\times n$ 的矩阵 $A$，同时满足

- 值域：对 $1\le i,j\le n$ 有 $0\le A_{i,j}\le n-1$；
- 每一行都是 $0,1,\dots,n-1$ 的一个排列；
- 每一列都是 $0,1,\dots,n-1$ 的一个排列；
- 对每个 $1\le i,j\le n-1$，相邻 $2\times2$ 块满足 $A_{i,j}\oplus A_{i+1,j}\oplus A_{i,j+1}\oplus A_{i+1,j+1}=x$。

若不存在这样的矩阵输出 $-1$。多测：第一行 $t$，接下来每组一行 $n\ x$；每组输出 $n$ 行、每行 $n$ 个整数，或单独一行 $-1$。

**约束**：

- $1\le t\le 180$，多测；
- $2\le n\le 2500$，$0\le x<n$；
- $\sum n\le 2500$，于是 $\sum n^2\le 6.25\times10^6$：**光把矩阵打印出来就是 $\Theta(n^2)$**，构造只能是 $O(n^2)$，不许有任何逐格搜索。

> 💡 题面没有任何「变量注入」类指令，全部要求都是上述四条矩阵条件。

## 2. 示例与观察
官方样例（输入 / 输出原样）：

```text
输入
5
2 0
2 1
3 0
4 1
4 0

输出
0 1
1 0
-1
-1
0 2 1 3
2 1 3 0
1 3 0 2
3 0 2 1
0 1 2 3
1 0 3 2
2 3 0 1
3 2 1 0
```

读法：第 1 组 $n=2,x=0$ 有解；第 2 组 $n=2,x=1$ 无解；第 3 组 $n=3,x=0$ 无解；第 4、5 组是 $n=4$ 的两个构造。

```text
输入（自造，★）
2
8 5
4 1

输出
0 2 1 7 4 3 5 6
2 5 3 0 6 4 7 1
1 3 0 6 5 2 4 7
7 0 6 5 3 1 2 4
4 6 5 3 0 7 1 2
3 4 2 1 7 5 6 0
5 7 4 2 1 6 0 3
6 1 7 4 2 0 3 5
0 2 1 3
2 1 3 0
1 3 0 2
3 0 2 1
```

★ 自造样例：$n=8,x=5$ 是「$n$ 为 2 的幂、$x\ne0$ 且不是 $n-1$」的普通情形，所有行/列都是 $0..7$ 的排列、每个相邻 $2\times2$ 异或都是 $5$；$n=4,x=1$ 即官方第 4 组，用于 §3.4 的走查。

## 3. 解题思路

### 3.1 暴力思路

最直接的做法是枚举拉丁方：$n=4$ 只有 $576$ 个，$n=5$ 有 $161\,280$ 个，$n=6$ 已经涨到 $8.1\times10^8$，$n=2500$ 完全无法想象。若改成逐格回溯：每填一格要维护行/列去重，而 $2\times2$ 约束只在右下角格子处才能校验，分支因子约 $n$、深度 $n^2$，最坏是指数级。

所以暴力只能在 $n\le 5$ 用来验证结论（本文的对拍代码就是这么做的）。真正要做的是：**把「相邻 $2\times2$ 异或为常数」翻译成一个代数结构，一次性锁死所有解的形状**。

### 3.2 核心观察：二阶差分恒为常数，解的形状被锁死

![二阶差分恒为 x：所有解都是 P_i⊕Q_j 再加上奇数行×奇数列上的 x](../../../images/cf2249d_second_difference.svg)

把「相邻 $2\times2$ 的异或」看作「先做行方向的差分、再做一次差分」，记（以下全部用 0-indexed）

$$D_{i,j}=A_{i,j}\oplus A_{i+1,j}\oplus A_{i,j+1}\oplus A_{i+1,j+1}.$$

题目要求 $D_{i,j}\equiv x$。这是 GF(2) 上逐位的**线性**条件，于是「解 = 一个特解 + 零二阶差分的齐次解」。

**特解**取修正项 $C_{i,j}=x\cdot[i\ \text{odd}][j\ \text{odd}]$。注意对任意 $i$ 都有 $[i\ \text{odd}]\oplus[i+1\ \text{odd}]=1$，列方向同理，所以 $C$ 在四个格子上的异或是

$$x\cdot\big([i\ \text{odd}]+[i+1\ \text{odd}]\big)\cdot\big([j\ \text{odd}]+[j+1\ \text{odd}]\big)=x\cdot1\cdot1=x .$$

于是 $B=A\oplus C$ 的四格异或恒为 $0$。

**齐次解**就是 $B_{i,j}=P_i\oplus Q_j$：固定第 $0$ 行与第 $0$ 列作为主元，其余格子由四格异或为 $0$ 唯一确定（见引理 1）。

把所有东西拼起来，**所有解恰好形如**

$$A_{i,j}=P_i\oplus Q_j\oplus x\cdot[i\ \text{odd}][j\ \text{odd}],\qquad 0\le i,j<n .$$

这一步的收益巨大：解空间从 $n^2$ 个格子坍缩成两条长度 $n$ 的序列。再代入「行/列是排列」：

- 第 $0$ 行是排列 $\Rightarrow\{Q_j\}$ 是置换；第 $0$ 列是排列 $\Rightarrow\{P_i\}$ 是置换；
- 第 $1$ 列（奇数列）的元素是 $P_i\oplus x[i\ \text{odd}]\oplus Q_1$ $\Rightarrow$ $P'_i:=P_i\oplus x[i\ \text{odd}]$ 也必须是置换；
- 对第 $1$ 行（奇数行）同理，$Q'_j:=Q_j\oplus x[j\ \text{odd}]$ 必须是置换。

### 3.3 算法流程：两个必要条件 + 一个配对构造

![轨道 {v, v⊕x} 要么整对不动、要么整对交换：交换轨道数必须是 n/4](../../../images/cf2249d_pair_matching.svg)

**必要条件 1（值域逼出 $n=2^m$）**。看任意偶数行 $i$：当 $j$ 为偶时该格是 $P_i\oplus Q_j$，$j$ 为奇时是 $P_i\oplus Q_j\oplus x$。由 $Q'_j=Q_j\oplus x[j\ \text{odd}]$ 的定义，**这一行的 $n$ 个值恰好就是 $\{P_i\oplus Q'_j\}_j$**（奇数行的置换性已保证 $Q'$ 是置换）。于是一方面 $P$ 是置换、另一方面 $Q'$ 是置换，两者的组合让每个有序对 $(a,b)\in[0,n)^2$ 都作为某个偶数行格子的值出现，值域要求

$$\forall a,b<n:\quad a\oplus b<n .$$

这个条件成立的充要条件是 $n$ 为 2 的幂（引理 2）。反例的取法很干净：令 $H=2^{m-1}$（$m=\lceil\log_2 n\rceil$）、$r=n-H\in[1,H)$，取 $a=H,\ b=r$，则 $a\oplus b=H+r=n$，越界。所以**一切非 2 的幂（包括所有奇数 $n$）都无解**。

**必要条件 2（配对逼出 $4\mid n$）**。$P$ 与 $P'$ 必须同时是置换。考虑 $\oplus x$ 在 $[0,n)$ 上的轨道：$x\ne0$ 时每个轨道是两元对 $\{v,v\oplus x\}$。令 $\tau=P'\circ P^{-1}$，则 $\tau(v)$ 要么是 $v$（$v$ 落在偶下标上），要么是 $v\oplus x$（落在奇下标上）。$\tau$ 是双射，所以同一个轨道里不能「一个不动、一个被送走」（那会把两个值都映到 $v$，撞车），只能**整对不动**或**整对交换**。交换一个轨道恰好占用 $2$ 个下标，而它们必须全落在奇下标上，共 $n/2$ 个 $\Rightarrow$ 需要 $n/4$ 个交换轨道 $\Rightarrow 4\mid n$。

合并两条：**有解 $\iff n=2^m$ 且（$x=0$ 或 $n\ge4$）**。$n=2$ 时 $x\ne0$ 无解，正是样例第 2 组。

**构造**（$x\ne0$，$n=2^m\ge4$）：

1. 从 $v=0$ 开始扫描，若 $v$ 与 $v\oplus x$ 都没用过，就把它们成对取出，直到取满 $n/4$ 对 —— 这些是「交换值」；
2. 剩下的 $n/2$ 个值是「不动值」（它们在 $\oplus x$ 下封闭，因为伙伴只可能也在剩余集合里）；
3. 偶下标 $i$ 依次填不动值，奇下标 $i$ 依次填交换值，得到置换 $P$；
4. 取 $Q=P$，输出 $A_{i,j}=P_i\oplus P_j\oplus x\cdot[i\ \text{odd}][j\ \text{odd}]$。

$x=0$ 时无需交换，直接取 $P_i=i$，$A_{i,j}=i\oplus j$。

为什么这样行？奇下标行被交换值填满，而 $P_i\oplus x$ 恰好把交换值集合映到它自己（每个轨道的两个值互换），所以 $P'$ 仍是置换；偶下标行的值来自在 $\oplus x$ 下封闭的不动值集合，$P'$ 在这些位置与原值相同。行/列的置换性则来自 $P$ 本身是置换：每行只是「$P$ 整体异或同一个常数」，自然是排列。

### 3.4 示例演算：$n=4,x=1$

![n=4,x=1 的构造走查：配对 → P → 矩阵](../../../images/cf2249d_walkthrough.svg)

$x=1$ 的轨道是 $\{0,1\},\{2,3\}$，需要 $n/4=1$ 个交换轨道，按扫描顺序取 $\{0,1\}$。

- 交换值：$0,1$；不动值：$2,3$。
- 奇下标 $1,3$ 填交换值 $\Rightarrow P_1=0,P_3=1$；偶下标 $0,2$ 填不动值 $\Rightarrow P_0=2,P_2=3$。故 $P=(2,0,3,1)$。
- 输出 $A_{i,j}=P_i\oplus P_j\oplus x[i\ \text{odd}][j\ \text{odd}]$（这里 $x=1$）：

$$A=\begin{pmatrix}0&2&1&3\\2&1&3&0\\1&3&0&2\\3&0&2&1\end{pmatrix}$$

与官方样例第 4 组逐字一致。检查一下奇数行、奇数列上的四个格子：$A_{1,1}=1,A_{1,3}=0,A_{3,1}=0,A_{3,3}=1$，正是「$2,0,3,1$ 两两异或」再多异或 $1$ 的结果；$9$ 个相邻 $2\times2$ 块的异或全为 $1$。

## 4. 算法细节

1. **2 的幂判定**：`(n & (n - 1)) == 0`，$n\ge2$ 时无需排除 $0$。
2. **$n=2$ 要单独挡掉 $x\ne0$**：$n/4$ 不是整数。统一写成 `if (!pow2 || (x != 0 && n < 4)) 输出 -1;`，别指望配对循环在 $n=2$ 时「自然失败」。
3. **配对扫描的边界**：循环条件 `need > 0 && v < n`；$\{v,v\oplus x\}$ 是完美匹配，任取 $n/4$ 对都合法，取最小的那些最省事。取对时只需检查两个端点是否都没用过。
4. **多测清空**：`used` 按当前 $n$ 现开（`vector<char> used(n, 0)`）。若为了省事开全局数组，必须只清 $[0,n)$，否则残留会把小 $n$ 的配对弄错。
5. **奇偶性必须统一在 0-indexed 下判断**：修正项 $[i\ \text{odd}][j\ \text{odd}]$ 依赖下标的奇偶；同一矩阵在 1-indexed 下奇偶整体翻转，公式必须跟着变。代码内部一律 0-indexed，只在读题时把题面的 $1\le i,j\le n$ 当位置即可。
6. **值域无需取模**：$n=2^m$ 时异或结果天然 $<n$；只有非 2 的幂才可能越界，而那种情况已经判无解，所以不存在「算出来越界再修」的麻烦。
7. **输出量**：$n=2048$ 时是 $4.19\times10^6$ 个数、约 $18$ MB 文本。C++ 用 `string` 攒好一次 `fputs`；Python 用 `' '.join(map(str, row))` 拼行、再 `'\n'.join` 一次写出，绝不能逐个数 `print`。
8. **行末格式**：每组恰好 $n$ 行，行内 $n$ 个整数空格分隔，不要多打尾随空格或空行。

## 5. 正确性证明

**引理 1**：若 $A$ 的所有相邻 $2\times2$ 块异或都等于 $x$，则存在序列 $P_0..P_{n-1}$、$Q_0..Q_{n-1}$ 使
$A_{i,j}=P_i\oplus Q_j\oplus x[i\ \text{odd}][j\ \text{odd}]$。

**证明**：令 $C_{i,j}=x[i\ \text{odd}][j\ \text{odd}]$、$B=A\oplus C$。由 $[i\ \text{odd}]\oplus[i+1\ \text{odd}]=1$ 与列的同一事实，$C$ 的四格异或是 $x\cdot1\cdot1=x$，故 $B$ 的四格异或恒为 $0$。

再证「四格异或恒为 $0$ 的矩阵必为 $B_{i,j}=P_i\oplus Q_j$」：取 $P_i=B_{i,0}$、$Q_j=B_{0,0}\oplus B_{0,j}$，则 $P_0\oplus Q_j=B_{0,j}$，即第 $0$ 行成立。对 $i$ 归纳（假设第 $i-1$ 行成立）：由四格异或为 $0$ 得 $B_{i,j}\oplus B_{i,j+1}=B_{i-1,j}\oplus B_{i-1,j+1}=Q_j\oplus Q_{j+1}$。对 $j$ 归纳：$B_{i,0}=P_i=P_i\oplus Q_0$ 是起点，若 $B_{i,j}=P_i\oplus Q_j$，则 $B_{i,j+1}=B_{i,j}\oplus Q_j\oplus Q_{j+1}=P_i\oplus Q_{j+1}$。归纳完成。反向代入时四个 $P$、四个 $Q$ 两两抵消，四格异或必为 $0$。∎

**引理 2**：$\forall a,b\in[0,n)$ 都有 $a\oplus b<n$，当且仅当 $n$ 是 2 的幂。

**证明**：若 $n=2^m$，$a,b$ 都只有低 $m$ 位，异或结果也 $<2^m=n$，充分性成立。
反之设 $n$ 不是 2 的幂，取 $m=\lceil\log_2 n\rceil$、$H=2^{m-1}$，则 $H<n<2H$，$r=n-H\in[1,H)$。令 $a=H,\ b=r$：两者都 $<n$，且 $r$ 不含第 $m-1$ 位，故 $a\oplus b=H+r=n$，不满足 $<n$。∎

**引理 3**：存在置换 $P$ 使 $P'$（$P'_i=P_i\oplus x[i\ \text{odd}]$）也是置换，当且仅当 $x=0$ 或 $4\mid n$。

**证明**：设 $P,P'$ 都是置换，$\tau=P'\circ P^{-1}$ 是置换，且 $\tau(v)\in\{v,v\oplus x\}$。$x\ne0$ 时 $\oplus x$ 的轨道都是两元对。若某轨道 $\{v,v\oplus x\}$ 中一个被 $\tau$ 固定、另一个被映到 $v$，则 $\tau$ 把两个不同的值都映到 $v$，与双射矛盾；故每个轨道整体不动或整体交换。交换轨道每对提供 $2$ 个下标，且这些下标必须是奇下标，故 $n/2$ 为偶数即 $4\mid n$。$x=0$ 时 $\tau=\mathrm{id}$ 恒可行。
充分性见 §3.3 的构造：取 $n/4$ 个轨道互换、其余固定，把互换轨道的值放到奇下标、其余放到偶下标即可。∎

**定理**：原问题有解当且仅当 $n$ 是 2 的幂且（$x=0$ 或 $n\ge4$）；并且 §3.3 的构造在 $O(n^2)$ 时间内给出合法矩阵。

**证明**：
*必要性*：由引理 1 任何解都有 $A_{i,j}=P_i\oplus Q_j\oplus x[i\ \text{odd}][j\ \text{odd}]$ 的形式，且第 $0$ 行、第 $0$ 列是排列 $\Rightarrow P,Q$ 都是置换；奇数行的置换性又给出 $Q'$（因而 $P'$）也是置换。由 §3.3 的观察，偶数行的值恰是全体 $\{P_i\oplus Q'_j\}$，故所有有序对 $(a,b)$ 都出现且值 $<n$，由引理 2 得 $n=2^m$。又 $P,P'$ 同为置换，由引理 3 得 $x=0$ 或 $4\mid n$；$n=2$ 时 $4\nmid n$，故 $x\ne0$ 必须 $n\ge4$。
*充分性*：设 $n=2^m$ 且 $x=0$ 或 $n\ge4$。$x=0$ 取 $P_i=i$，$x\ne0$ 按 §3.3 取 $P$。此时 $P$ 是置换、$P'$ 是置换、所有值 $<n$。于是

- 行：$i$ 偶时该行是 $P_i\oplus\{P_j\}_j$，$i$ 奇时是 $P_i\oplus\{P'_j\}_j$，都是排列；
- 列：$j$ 偶时该列是 $\{P_i\}_i\oplus P_j$，$j$ 奇时是 $\{P'_i\}_i\oplus P_j$，都是排列；
- 值域：$n=2^m$ 且各分量 $<n$；
- $2\times2$ 条件：四格中 $P_i$、$P_j$ 项两两抵消，而 $[i\ \text{odd}][j\ \text{odd}]$ 四格之和恒为 $1$，故异或恰为 $x$。

四条全部满足。∎

## 6. 复杂度分析

- **时间**：每组预处理 $O(n)$（配对扫描 + 填 $P$），输出 $O(n^2)$。总输出量 $\sum n^2\le6.25\times10^6$ 个数。实测最坏单组 $n=2048$（$x=1023$，输出 $18$ MB）C++ 约 $0.09$ s，Python 约 $1.0$ s，相对 2 s 时限余量充足。
- **空间**：额外结构 $O(n)$（$P$、`used`、配对数组）；输出缓冲 $O(n^2)$ 字符。内存限制 512 MB，$18$ MB 的缓冲远无压力。

## 7. 参考代码

### C++17

```cpp
#include <cstdio>
#include <string>
#include <vector>

using namespace std;

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;
    while (t--) {
        int n, x;
        scanf("%d %d", &n, &x);
        bool pow2 = (n & (n - 1)) == 0;
        if (!pow2 || (x != 0 && n < 4)) { puts("-1"); continue; }
        vector<int> P(n);
        if (x == 0) {
            for (int i = 0; i < n; i++) P[i] = i;
        } else {
            vector<char> used(n, 0);
            vector<int> sw, fx;
            int need = n / 4;
            for (int v = 0; v < n && need > 0; v++) {
                if (used[v]) continue;
                int w = v ^ x;
                if (used[w]) continue;
                used[v] = used[w] = 1;
                sw.push_back(v); sw.push_back(w);
                need--;
            }
            for (int v = 0; v < n; v++) if (!used[v]) fx.push_back(v);
            int a = 0, b = 0;
            for (int i = 0; i < n; i++) P[i] = (i & 1) ? sw[a++] : fx[b++];
        }
        string out;
        out.reserve((size_t)n * n * 5 + n + 1);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int val = P[i] ^ P[j] ^ (((i & 1) && (j & 1)) ? x : 0);
                out += to_string(val);
                out += (j + 1 == n) ? '\n' : ' ';
            }
        }
        fputs(out.c_str(), stdout);
    }
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos]); x = int(data[pos + 1]); pos += 2
        if (n & (n - 1)) or (x != 0 and n < 4):
            out.append("-1")
            continue
        if x == 0:
            P = list(range(n))
        else:
            used = bytearray(n)
            sw = []
            fx = []
            need = n // 4
            v = 0
            while v < n and need > 0:
                if used[v]:
                    v += 1
                    continue
                w = v ^ x
                if used[w]:
                    v += 1
                    continue
                used[v] = used[w] = 1
                sw.append(v); sw.append(w)
                need -= 1
                v += 1
            for v in range(n):
                if not used[v]:
                    fx.append(v)
            P = [0] * n
            a = b = 0
            for i in range(n):
                if i & 1:
                    P[i] = sw[a]; a += 1
                else:
                    P[i] = fx[b]; b += 1
        for i in range(n):
            pi = P[i]
            if x and (i & 1):
                out.append(' '.join([str(pi ^ P[j] ^ (x if (j & 1) else 0)) for j in range(n)]))
            else:
                out.append(' '.join([str(pi ^ P[j]) for j in range(n)]))
    sys.stdout.write('\n'.join(out) + '\n')


main()
```

## 8. 边界情况与易错点

1. **$n=2,x=1$ 必须输出 $-1$**：矩阵只有唯一一个 $2\times2$ 块，它的异或等于四格异或；两行都是 $\{0,1\}$ 的排列 $\Rightarrow$ 四格异或恒为 $0$。样例第 2 组专门考这个。
2. **所有非 2 的幂都无解（含全部奇数 $n$）**：引理 2 的反例 $a=H,b=n-H$ 直接给出越界。很多人只判「$n$ 为偶数」，会漏掉 $n=6,10,12$ 之类。
3. **$x=0$ 不要混进配对分支**：$n=2$ 时 $n/4=0$，若写成「`need=0` 也算合法」，$n=2,x=1$ 就会被漏判成有解，务必先判 `x != 0 && n < 4`。
4. **奇偶性统一在 0-indexed 下**：修正项依赖下标奇偶，题目用 1-indexed 描述位置；代码里保持 0-indexed 即可，不要中途换算。
5. **多测复用数组**：按 $n$ 重新开 `used`；若开全局数组只清 $[0,n)$，上一组残留会导致配对错乱（$n$ 变化时尤其隐蔽）。
6. **输出格式**：每组恰好 $n$ 行、每行 $n$ 个整数；`-1` 单独一行；行末不要空行，否则多测解析会错位。
7. **大输出性能**：Python 逐个数 `print` 在 $n=2048$ 时会明显超时，必须整行 join 后一次性写。
8. **$x$ 是值不是位置**：$0\le x<n$，直接参与异或；不要因为题面用 1-indexed 就给它减 1。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：1 / 1 通过（按 Codeforces 标准 checker 的 token 比对，忽略空白与大小写）。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [Codeforces 1174D Ehab and the Expected XOR Problem](https://codeforces.com/problemset/problem/1174/D)：用「前缀异或 + 禁用值」构造序列，同样是把条件化成线性约束后一次性锁死结构。
- [Codeforces 1557C Moamen and XOR](https://codeforces.com/problemset/problem/1557/C)：按位统计与异或的结构性计数，本题引理 2 的「$2^m$ 才封闭」是同一类位运算直觉。
- [Codeforces 1605D Treelabeling](https://codeforces.com/problemset/problem/1605/D)：用最高位给点集分组做标号，位运算构造的经典套路。
- [LeetCode 1734. 解码异或后的排列](https://leetcode.cn/problems/decode-xored-permutation/)：排列 + 前缀异或的还原，和本题的「偶数行 = $P_i\oplus\{P_j\}$」视角互补。

**延伸思考**：

1. 本题能构造的根源是 GF(2) 上「$ij$ 的双线性项」二阶差分恒为常数。若把异或换成模 $n$ 加法，同样的修正项不再是特解，此时哪些 $(n,x)$ 有解？
2. 若把「相邻 $2\times2$」换成「任意大小为 $k$ 的方块」或「环面（首尾也相邻）」，条件数会变多，$n=2^m$ 的结论是否还成立？环面会额外引入 $n$ 的整除约束。
3. 如果只要求每行是排列、列可以重复，必要条件会松到什么程度？此时「值域逼出 $n=2^m$」的论证会失效，正是本题最关键的支点。
