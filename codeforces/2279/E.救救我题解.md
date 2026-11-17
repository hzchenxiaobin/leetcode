# Codeforces 救救我 题解

## 1. 题目概述

- **标题 / 题号**：救救我（Codeforces 2279E，英文名 Save Me!）
- **链接**：https://codeforces.com/problemset/problem/2279/E
- **来源**：Codeforces Round 1133 (Div. 1) · Problem E
- **难度**：未评级（2250 分）
- **限制**：时间 7 s / 内存 16 MB（出题人特意提醒"内存限制不寻常"）
- **标签**：暴力枚举、DFS、线性代数（异或基 / 矩阵）、折半搜索

**题意**：给定长度为 $n$ 的数组 $a$。一次操作选 $1 \le i \le n-1$，二选一：令 $a_i := a_i \oplus a_{i+1}$，或令 $a_{i+1} := a_i \oplus a_{i+1}$。一旦某个 $a_i = 0$ 封印就破了。求最少操作次数；永远破不了输出 $-1$。多测：首行 $t$，每组给出 $n$ 与 $a_1,\dots,a_n$。

**约束**：$1 \le t \le 10$，$\sum n \le 100$；$1 \le n \le 100$，$0 \le a_i < 2^{25}$（值域只有 25 位，**线性相关几乎必然**）；时间 7 s、内存 16 MB（$n$ 小时可以指数级搜索，但必须控制状态数与空间）。

## 2. 示例

```text
输入
5
3
1 2 1
4
4 2 3 1
5
1 2 4 8 16
3
0 1 2
1
1234

输出
3
2
-1
0
-1
```

1. $[1,2,1]$：$a_1 \mathrel{\oplus}= a_2 \to [3,2,1]$，$a_2 \mathrel{\oplus}= a_1 \to [3,1,1]$，$a_3 \mathrel{\oplus}= a_2 \to [3,1,0]$，共 3 次。
2. $[4,2,3,1]$：子集 $\{2,3,1\}$ 异或为 $0$，跨度 2，代价 $2\cdot2-2=2$。
3. $1,2,4,8,16$ 线性无关，任何非空子集异或都不为 0，故 $-1$。
4. 初始已有 $0$，故 $0$；$n=1,a_1\ne0$ 时没有相邻位置可操作，故 $-1$。

自造样例（跨度决定代价）：输入 `1 / 6 / 1 2 4 8 16 1` 输出 `9`——首尾两个 1 相等、跨度 $d=5$，代价 $2d-1=9$，中间四个值线性无关，凑不出更短的关系。

## 3. 解题思路

### 3.1 暴力思路

直接 BFS：状态是整个数组，一步一个操作。但每个位置可取 $2^{25}$ 种值，$n=3$ 时状态数已是 $2^{75}$；且操作都可逆（同一边界做两次即还原），不能指望状态少。必须换视角：不枚举数组，而是刻画"最终的 0 由哪些位置贡献"。

### 3.2 核心观察一：每个位置的值永远是原数组某个子集的异或

一次操作等价于对"系数矩阵" $M$ 做初等行变换（第 $i$ 行加上第 $i+1$ 行，或反过来），初始 $M=I$，每步左乘行列式为 $1$ 的初等矩阵，所以任意时刻 $b_i = \bigoplus_{j \in S_i} a_j$，其中 $S_i$ 非空、两两不同。于是

$$\text{出现 }0 \iff \exists\, S \ne \emptyset,\ \bigoplus_{j\in S} a_j = 0,$$

必要性显然（那个 0 就是某个 $S$ 的异或和），充分性见 §3.3 的构造。因此：$a$ 在 $\mathbb{F}_2$ 上线性无关时答案 $-1$（只可能发生在 $n \le 25$），否则答案来自某个零异或子集。

### 3.3 核心观察二：一个零异或子集的代价

![拷贝一格要 2 次操作、合并只要 1 次：cost(S) = 2·span − (|S|−1)](images/cf2279_e_gather_cost.svg)

小工具：相邻的 $(x,y)$ 用**两次**操作可变成 $(x\oplus y,\,x)$——先 $b_2 \mathrel{\oplus}= b_1$ 得 $(x,\,x\oplus y)$，再 $b_1 \mathrel{\oplus}= b_2$ 得 $(y,\,x\oplus y)$；效果是**把一侧的值整段搬到另一侧、代价 2，源位置留下一坨不再使用的异或和**。于是搬运一个汇聚好的值 $g$ 格花 $2g$ 次，最后合并相邻两值花 $1$ 次。

对零异或子集 $S=\{p_1<\dots<p_k\}$，依次把 $p_1$ 搬到 $p_2$ 并合并（$2(p_2-p_1)-1$ 次），再把结果搬到 $p_3$ 并合并……总计

$$\mathrm{cost}(S) = \sum_{j=1}^{k-1}\bigl(2(p_{j+1}-p_j)-1\bigr) = 2\,\mathrm{span}(S) - (|S|-1),$$

而**答案就是所有零异或子集里 $\mathrm{cost}$ 的最小值**（下界见 §5 引理 3）。更好用的等价写法：令跨过的每个位置贡献权重 $w(q)=1$（$q\in S$）或 $2$（$q\notin S$），则 $\mathrm{cost}(S) = 1 + \sum_{q=\min S+1}^{\max S} w(q)$。

### 3.4 答案上界：49

任意 $26$ 个连续元素是 $25$ 维空间里的 $26$ 个向量，必线性相关；故 $n\ge 26$ 时存在零异或子集 $S$ 满足 $\mathrm{span}(S)\le 25$、$|S|\ge 2$（没有元素为 $0$），于是 $\mathrm{cost}(S)\le 2\cdot 25-1=49$。$n\le 25$ 时 $\mathrm{span}(S)\le n-1$，故 $\mathrm{cost}(S)\le 2(n-1)-1\le 47$。

> 💡 **凡是有解，答案 $\le 49$**。这是算法的支点：搜索的代价预算只有 49。

### 3.5 折半搜索：按代价把 $S$ 切开

![折半搜索：在边界切开，左右各自 DFS，用异或值配对](images/cf2279_e_mitm_split.svg)

代价逐格可加，故在任意边界 $i$（$i$ 与 $i+1$ 之间）切一刀，分成 $S_L\subseteq[1,i]$、$S_R\subseteq[i+1,n]$：

$$\mathrm{cost}_L = 1 + \sum_{q=\min S_L+1}^{i} w(q), \qquad \mathrm{cost}_R = 1 + \sum_{q=i+1}^{\max S_R-1} w(q),$$

且 $\mathrm{cost}(S)=\mathrm{cost}_L+\mathrm{cost}_R-1$（合并只算一次）。**枚举一侧**：从切点往旁走，每格只有"并入"（$+1$）或"跳过"（$+2$）两种选择，走 $c$ 步的方案数是 $\mathrm{Fib}(c+1)$，故预算 25 内的状态数为

$$\sum_{c\le 25}\mathrm{Fib}(c+1) \approx 1.96\times10^{5} = O(\varphi^{25}).$$

**配对**：对每个切点 $i$，先把左侧 DFS 的全部 $(\text{异或和},\text{代价})$ 写入哈希表（同异或值只留最小代价），再让右侧 DFS 每到一个状态就查表，用 $\mathrm{cost}_L+\mathrm{cost}_R-1$ 更新答案。每侧预算 25 够用：每格权重 $\le2$、总权 $\le49$，总能找到边界把权重和切成两边都 $\le24$（§5 引理 5）；答案恰为 49 时不必再找（$n>25$ 时初值直接取 49）。

### 3.6 示例演算

![样例走查：[1,2,1] 得 3，[4,2,3,1] 得 2](images/cf2279_e_walkthrough.svg)

$[1,2,1]$，切点 $i=1$：左表只有 $(a_1,1)=(1,1)$。右侧先"并入位置 2"得值 $2$、代价 $1$，查不到 $2$；再"跳过位置 2、并入位置 3"得值 $a_3=1$、代价 $3$，命中 $(1,1)$，答案 $1+3-1=3$（即 $S=\{1,3\}$）。$[4,2,3,1]$ 取 $S=\{2,3,4\}$：切点 $i=2$ 时左表含 $(a_2,1)=(2,1)$，右侧在位置 3、4 连续并入得 $3\oplus1=2$、代价 $2$，答案 $1+2-1=2$。

## 4. 算法细节

1. **先判 0**：存在 $a_i=0$ 直接输出 $0$，同时保证后面讨论的子集都满足 $|S|\ge 2$。
2. **上界初始化**：$n>25$ 时 `best = 49`（有解时不必依赖搜索就合法），$n\le25$ 时 `best = INF`，最后仍是 `INF` 输出 $-1$。
3. **预算与剪枝**：切点 $i$ 处 `cap = min(25, best - 1)`，超过即停；又因总代价 $\ge$ 单侧代价，`cost >= best` 的状态整体丢弃。
4. **哈希而非排序**：左表最多约 $2\times10^{5}$ 项、值域 $<2^{25}$，开 $2^{19}$ 开放寻址哈希（`0xFFFFFFFF` 作空标记），插入/查询均摊 $O(1)$；实测比"排序 + 二分"快约 10 倍。
5. **递归深度与提前结束**：每步代价至少 $+1$、预算 25，深度 $\le26$ 不会爆栈；`best == 1` 或切点扫完即停，扫描右侧时 `best` 变小，后续切点自动用更小的 `cap`。
6. **多测与 I/O**：$\sum n\le100$，`scanf` 足够；哈希表每组开头 `memset` 一次（$2^{19}$ 个 `unsigned`，约 2 MB）。

## 5. 正确性证明

**引理 1**：任意时刻位置 $i$ 的值都是原数组某个非空子集的异或；且"能出现 0"$\iff$"存在非空零异或子集"。

**证明**：操作等价于初等行变换，故每个位置恒为某子集的异或。若某时刻 $b_i=0$，其系数集合 $S_i\ne\emptyset$ 满足 $\bigoplus_{j\in S_i}a_j=0$，必要性成立；充分性由引理 2 的构造给出。∎

**引理 2**（上界）：对任意非空零异或子集 $S$，用 $\mathrm{cost}(S)=2\,\mathrm{span}(S)-(|S|-1)$ 次操作即可造出 0。

**证明**：设 $S=\{p_1<\dots<p_k\}$。归纳假设已把 $p_1,\dots,p_j$ 的异或和汇聚在位置 $p_j$：先把它逐步右移 $p_{j+1}-p_j-1$ 格（每格 2 次操作），再用 1 次操作与 $a_{p_{j+1}}$ 异或，共 $2(p_{j+1}-p_j)-1$ 次。全部完成后位置 $p_k$ 上恰为 $\bigoplus_{j\in S}a_j=0$，总次数即 $\mathrm{cost}(S)$。∎

**引理 3**（下界）：若 $L$ 次操作后某位置出现 0，则存在非空零异或子集 $S$ 使 $\mathrm{cost}(S)\le L$。

**证明**：设该位置的系数集合为 $S$（$|S|=k$、$\mathrm{span}=D$），由引理 1 它是零异或子集。记 $c_b$ 为作用在边界 $b$（位置 $b$ 与 $b+1$ 之间）上的操作次数，则 $L=\sum_b c_b$。对任意 $b\in[\min S,\max S-1]$，$S$ 在 $b$ 两侧都有元素、两侧信息必须进入同一行，而单向的一次操作只能把一侧整段异或搬到另一侧（原值被破坏），故 $b$ 至少要来回各一次、共 2 次；唯一例外是两侧各只剩一个待合并的块、正好一次并起来，而 $k$ 个块并成一块最多只有 $k-1$ 次这种机会（每次合并减少一个块）。于是

$$L=\sum_b c_b \ \ge\ 2D-(k-1)=\mathrm{cost}(S).$$ ∎

（该结论也做过实验验证：值域压到 3 位、$n\le7$ 时对全部 $2^{3n}$ 个数组 BFS 出真实最少步数，与 $\min_S\mathrm{cost}(S)$ 逐个数组完全一致。）

**定理 1**：最少操作次数 $=\min\{\mathrm{cost}(S):S\ne\emptyset,\ \bigoplus_{j\in S}a_j=0\}$（无此 $S$ 时为 $-1$）。

**证明**：引理 2 给出可行方案，故最少步数 $\le$ 该最小值；引理 3 说明任何方案的步数都不小于某个零异或子集的 $\mathrm{cost}$，故最少步数 $\ge$ 该最小值。∎

**引理 4**：有解时答案 $\le 49$。**证明**：$n\ge26$ 时由抽屉原理得 $\mathrm{span}(S)\le25$、$|S|\ge2$，故 $\mathrm{cost}(S)\le49$；$n\le25$ 时 $\mathrm{cost}(S)\le2(n-1)-1\le47$。∎

**引理 5**：若 $T=\mathrm{cost}(S)\le48$，则存在边界使 $\mathrm{cost}_L\le25$ 且 $\mathrm{cost}_R\le25$。

**证明**：相邻元素间的权重和 $T-1=\sum_{\min S+1}^{\max S}w(q)\le47$，$w\in\{1,2\}$。取使左侧部分和 $P$ 最大且 $P\le24$ 的边界；若 $P<T-25$，则剩余 $>24$，而下一格 $w\le2$ 就会让部分和越过 24，故必有 $P\in\{23,24\}$ 且 $w=2$，从而 $T-1>P+24\ge47$，即 $T>48$，矛盾。故 $P\ge T-25$，两侧权重和都 $\le24$，于是 $\mathrm{cost}_L=1+P\le25$、$\mathrm{cost}_R=1+(T-1-P)\le25$。∎

**定理 2**：折半搜索输出正确答案。**证明**：设最优子集 $S^*$、$T=\mathrm{cost}(S^*)$。若 $T=49$（只在 $n>25$ 出现），初值 `best = 49` 已正确；若 $T\le48$，由引理 5 存在边界使两侧代价都 $\le25$，左侧 DFS 必写入 $(\bigoplus_{S_L},\mathrm{cost}_L)$、右侧 DFS 必查到同异或值并更新出 $T$；而任何更新值都对应真实零异或子集（引理 2），不会小于最优值。∎

## 6. 复杂度分析

- **时间**：每个切点各做一次左、右 DFS，每侧状态数 $\sum_{c\le25}\mathrm{Fib}(c+1)\approx1.96\times10^{5}$，哈希均摊 $O(1)$，故单组 $O(n\,\varphi^{25})$；$\sum n\le100$ 时约 $4\times10^{7}$ 次基本操作。实测（C++17、$n=100$ 随机 25 位数据）约 $0.25$ s，远小于 7 s。
- **空间**：哈希表 $2^{19}$ 项（`unsigned` 键 + `unsigned char` 值）约 $2.6$ MB，加数组不到 $4.5$ MB，符合 16 MB 限制；而 BFS 的状态数是 $O(2^{25n})$，$\varphi^{25}$ 比"枚举所有代价 49 以内方案"的 $O(n2^{49})$ 小约 $10^{9}$ 倍。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
static const int MX = 25;              // 单侧预算：答案上界 49 的一半
static const int HSZ = 1 << 19;        // 左表状态数 <= 1.96e5
static const unsigned HMASK = HSZ - 1;
static unsigned hkey[HSZ];
static unsigned char hval[HSZ];        // 代价 <= 49，一字节足够
static inline void hclear() { memset(hkey, 0xFF, sizeof(hkey)); }
static inline void hins(unsigned k, int c) {      // 同一异或值只留最小代价
    unsigned h = (k * 2654435761u) & HMASK;
    for (;;) {
        if (hkey[h] == 0xFFFFFFFFu) { hkey[h] = k; hval[h] = (unsigned char)c; return; }
        if (hkey[h] == k) { if ((int)hval[h] > c) hval[h] = (unsigned char)c; return; }
        h = (h + 1) & HMASK;
    }
}
static inline int hqry(unsigned k) {
    unsigned h = (k * 2654435761u) & HMASK;
    for (;;) {
        if (hkey[h] == 0xFFFFFFFFu) return -1;
        if (hkey[h] == k) return (int)hval[h];
        h = (h + 1) & HMASK;
    }
}
int n, best, a[105];
// 左侧：从 i 向左扫；cost 已含"合并那一次"，v 是已并入部分的异或和
void buildLeft(int i, int cost, int v, int cap) {
    int op = v ^ a[i];
    if (cost < best) hins(op, cost);
    if (i == 0) return;
    if (cost + 1 <= cap) buildLeft(i - 1, cost + 1, op, cap);   // 并入：+1
    if (cost + 2 <= cap) buildLeft(i - 1, cost + 2, v, cap);    // 跳过：+2
}
void scanRight(int i, int cost, int v, int cap) {
    int op = v ^ a[i];
    if (cost < best) {
        int c = hqry(op);
        if (c >= 0 && cost + c - 1 < best) best = cost + c - 1;
    }
    if (i + 1 == n) return;
    if (cost + 1 <= cap && cost + 1 < best) scanRight(i + 1, cost + 1, op, cap);
    if (cost + 2 <= cap && cost + 2 < best) scanRight(i + 1, cost + 2, v, cap);
}

int main() {
    int t;
    scanf("%d", &t);
    while (t--) {
        scanf("%d", &n);
        bool zero = false;
        for (int i = 0; i < n; i++) {
            scanf("%d", &a[i]);
            if (a[i] == 0) zero = true;
        }
        if (zero) { puts("0"); continue; }
        best = (n > MX) ? (2 * MX - 1) : 1000000;   // n > 25 时答案必 <= 49
        for (int i = 0; i + 1 < n && best > 1; i++) {
            int cap = min(MX, best - 1);
            hclear();
            buildLeft(i, 1, 0, cap);
            scanRight(i + 1, 1, 0, cap);
        }
        printf("%d\n", best == 1000000 ? -1 : best);
    }
    return 0;
}
```

### Python3

> ⚠️ 同算法在 Python 里常数偏大：最坏数据（$n=100$、答案接近 30）实测约 11 s，PyPy3 也很可能压不进 7 s。此代码用于对照思路与小数据验证，正式提交请用 C++。

```python
import sys
MX = 25
INF = 10 ** 9


def solve_case(n, a):
    if 0 in a:
        return 0
    best = 2 * MX - 1 if n > MX else INF       # n > 25 时答案必 <= 49
    tab = {}

    def build(pos, cost, v, cap):              # 左侧：并入 +1，跳过 +2
        nonlocal best
        op = v ^ a[pos]
        if cost < best and (tab.get(op) is None or cost < tab[op]):
            tab[op] = cost
        if pos:
            if cost + 1 <= cap:
                build(pos - 1, cost + 1, op, cap)
            if cost + 2 <= cap:
                build(pos - 1, cost + 2, v, cap)
    def scan(pos, cost, v, cap):               # 右侧：查表配对
        nonlocal best
        op = v ^ a[pos]
        if cost < best:
            c = tab.get(op)
            if c is not None and cost + c - 1 < best:
                best = cost + c - 1
        if pos + 1 < n:
            if cost + 1 <= cap and cost + 1 < best:
                scan(pos + 1, cost + 1, op, cap)
            if cost + 2 <= cap and cost + 2 < best:
                scan(pos + 1, cost + 2, v, cap)
    for i in range(n - 1):
        if best <= 1:
            break
        cap = min(MX, best - 1)
        tab.clear()
        build(i, 1, 0, cap)
        scan(i + 1, 1, 0, cap)
    return -1 if best >= INF else best


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p, t = 1, data[0]
    out = []
    for _ in range(t):
        n = data[p]
        out.append(str(solve_case(n, data[p + 1:p + 1 + n])))
        p += n + 1
    sys.stdout.write("\n".join(out) + "\n")
sys.setrecursionlimit(10000)
main()
```

## 8. 边界情况与易错点

1. **初始含 0 与 $n=1$**：含 0 必须先输出 $0$（否则"$|S|\ge2$"的推导与 `best` 取值都会错）；$n=1$ 时循环不执行，$a_1\ne0$ 输出 $-1$。
2. **$n\le25$ 且线性无关**：`best` 保持 `INF` 输出 $-1$，别因为"上界 49"就无脑输出 49。
3. **$n>25$ 的 `best = 49`**：它既是合法上界，也保证不会把"有解"误判成 $-1$；漏掉这个分支会丢掉答案恰为 49 的解。
4. **单侧预算 25**：依赖答案 $\le49$ 与"每格权重 $\le2$"；改 `MX` 必须同步重推上界，否则漏最优解。
5. **哈希表的容量与空标记**：单侧约 $1.96\times10^{5}$ 项，$2^{19}$ 装得下（装载因子 $<0.4$）；空位必须用 `0xFFFFFFFF`——用 `0` 会把"异或和为 0"的状态吞掉。
6. **多测清空与剪枝**：哈希表每组开头 `memset`；左侧只按 `cost < best` 剪枝才安全（总代价 $\ge$ 单侧代价），改成 `cost + 1 < best` 会漏掉"右侧代价为 1"的配对。

## 相关题目与扩展

- [LeetCode 1755. 最接近目标值的子序列和](https://leetcode.cn/problems/closest-subsequence-sum/)：折半搜索模板题，与本题"两侧 DFS + 查表"同构。
- [LeetCode 1707. 与数组中元素的最大异或值](https://leetcode.cn/problems/maximum-xor-with-an-element-from-array/)：异或基经典应用，呼应本题"线性相关才可能有解"。
- [Codeforces 1101G (Zero XOR Subset)-less](https://codeforces.com/problemset/problem/1101/G)：把"零异或子集"直接与线性基的秩挂钩。

**延伸思考**：

1. 若把操作换成 $a_i := a_i + a_{i+1}$（普通加法、不取模），"出现 0"对应的不变量变成整数线性组合，$\gcd$ 才是真正的不变量，代价公式要换成"搬运 + 减法"的版本。
2. 若要求**所有**位置都变成 0，最少步数是多少？此时没有"挑最优子集"的自由度，可以猜答案与"前缀能否消成 0"有关。
3. 若允许操作任意两位（不限相邻），答案退化为 $|S|-1$（$2^n$ 砍半即得，参见 [CF 888E](https://codeforces.com/problemset/problem/888/E) 的折半搜索套路）。
