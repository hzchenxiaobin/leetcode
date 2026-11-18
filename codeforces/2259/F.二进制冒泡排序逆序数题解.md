# Codeforces 二进制冒泡排序逆序数 题解

## 1. 题目概述

- **标题 / 题号**：二进制冒泡排序逆序数（Codeforces 2259F，英文名 Binary Bubble Sort Inversions）
- **链接**：https://codeforces.com/problemset/problem/2259/F
- **来源**：Codeforces Round 1119 (Div. 3) · Problem F
- **难度**：$\ast 1800$
- **限制**：时间 3 s / 内存 256 MB
- **标签**：数据结构、数学、双指针（官方标签：data structures、math、two pointers）

**题意**：给定长度为 $n$ 的 01 数组 $a$ 与长度同为 $n$ 的 01 串 $s$。两种**整趟**操作（作用在当前数组 $b$ 上）：bubble 令 $i=1,2,\dots,n-1$ 依次执行「若 $b_i>b_{i+1}$ 就交换」；reverse bubble 令 $i=n-1,n-2,\dots,1$ 依次做同样的事。依次执行 $n$ 次操作，第 $i$ 次在 $s_i=1$ 时做 bubble、否则做 reverse bubble。输出**初始数组**与**每次操作之后**的逆序对个数，共 $n+1$ 个整数。多测：首行 $t$，每组读 $n$、$n$ 个 $0/1$、字符串 $s$，输出一行 $n+1$ 个数。

**约束**：

- $1\le t\le 10^4$，$\sum n\le 5\times 10^5$：单组须接近 $O(n)$，总计 $O(\sum n)$；
- $1\le n\le 5\times 10^5$，$a_i\in\{0,1\}$，$|s|=n$；
- 逆序数可达 $\lfloor n^2/4\rfloor\approx 6.25\times10^{10}$，**必须 64 位整数**；
- 每组输出 $n+1$ 个数，总输出量 $O(\sum n)$，I/O 常数不可忽略。

## 2. 示例

官方样例 7 组（输入 / 输出原样）：

```text
输入
7
4
1 1 0 0
1010
7
0 1 0 1 1 0 0
0101001
4
0 0 1 1
1001
1
1
1
5
0 1 1 0 0
11101
3
1 0 0
000
6
1 0 1 1 0 0
011000
```

```text
输出
4 2 1 0 0
7 4 2 0 0 0 0 0
0 0 0 0 0
0 0
4 2 0 0 0 0
2 1 0 0
7 4 2 1 0 0 0
```

题面 Note 给出第 1 组的数组轨迹：$1\,1\,0\,0\to1\,0\,0\,1\to0\,1\,0\,1\to0\,0\,1\,1\to0\,0\,1\,1$，逆序数 $4,2,1,0,0$。第 3 组一开始就有序，之后恒为 $0$；第 4 组 $n=1$，只有 $0$ 个逆序对，输出两个 $0$。

题面样例未覆盖全 $0$、全 $1$ 这类退化数组，它们在 §8 第 1、2 条单独说明；本文实现与暴力对拍时已逐一验过。

## 3. 解题思路

### 3.1 暴力思路

按定义模拟：每趟扫一遍交换 $O(n)$，再数一遍逆序对 $O(n)$，共 $n+1$ 次，单组 $O(n^2)$；$n=5\times10^5$ 时约 $2.5\times10^{11}$ 次基本操作，超时几个数量级。

但 01 数组上的「一趟扫描」并不是只交换一对相邻元素——它会**整段搬运**。把这点说透，状态就能压缩成一个长度不变的序列。

### 3.2 核心观察：一次冒泡 = 删掉一个 1、末尾补一个 1

![一次左冒泡等价于删掉第一个 1 并在末尾补 1；一次右冒泡等价于删掉最后一个 0 并在开头补 0](images/cf2259_f_state_concept.svg)

**引理 1（冒泡的剪切形态）**：一次左冒泡等价于「删掉数组里**第一个 1**，其余元素整体左移一格，末尾补一个 1」。

*证明思路（携带者）*：把扫描看成维护一个「待定元素」$t$：处理位置 $i$ 时，位置 $i$ 上是 $t$、位置 $i+1$ 仍是**原数组**的 $a_{i+1}$（从未被写过）；比较后位置 $i$ 定稿、此后再不被访问。于是终值 $=\min(t,a_{i+1})$、新的 $t=\max(t,a_{i+1})$，归纳得 $t=\max(a_1,\dots,a_i)$：**一旦遇到首个 1，$t$ 永远是 1**，此后位置 $i$ 终值为 $a_{i+1}$、末尾终值为 1。完整证明见 §5。

同理（数组反转、每个元素换成 $1-x$，左右冒泡互换）：

**引理 2**：一次右冒泡等价于「删掉**最后一个 0**，其余整体右移一格，开头补一个 0」。

**引理 3（$r$ 编码）**：设有 $k$ 个 1、$m$ 个 0，第 $j$ 个 1 的位置为 $p_j$，令 $r_j=p_j-j$（第 $j$ 个 1 左边 0 的个数），则 $0\le r_1\le\cdots\le r_k\le m$，且

$$I=\sum_{j=1}^{k}(m-r_j)=km-\sum_{j=1}^{k}r_j .$$

两种操作在 $r$ 上简单得惊人：

$$\text{bubble}: r\leftarrow(r_2,r_3,\dots,r_k,\ m),\qquad \text{reverse}: r_j\leftarrow\min(r_j+1,\ m).$$

- 左冒泡删掉第一个 1：其余 1 的下标前移一位，而左边被删掉的也是一个 1，故 $r$ 值不变（整体左移一格）；新补到末尾的 1 左边有全部 $m$ 个 0，故末位是 $m$。
- 右冒泡让每个 1 右移一格、左边 0 的个数 $+1$；已贴在右端的 1 满足 $r_j=m$，封顶不动。

两种更新都保序，于是数组可以彻底丢掉，只维护这个长度恒为 $k$ 的非降序列。

### 3.3 算法流程：闭式状态 + 两个指针

![闭式状态 S(L,R) 与阈值 J：指针 i 只右移、J 只左移](images/cf2259_f_formula_flow.svg)

做了 $L$ 次左冒泡、$R$ 次右冒泡后，记 $i=\min(L,k)$。此时 $r$ 里只剩原下标 $>i$ 的元素还「活着」，被 $R$ 次 $+1$ 抬高并封顶；前 $i$ 个位置是被弹到末尾的 1，值恒为 $m$。因此

$$S(L,R)=\sum_j r_j=i\,m+\sum_{j=i+1}^{k}\min(r_j+R,\ m),\qquad I=km-S(L,R).$$

按式求和是每步 $O(k)$。利用 $r$ 非降：满足 $r_j+R\ge m$ 的下标是一段**后缀**，起点 $J=\min\{j:r_j\ge m-R\}$，于是

$$S=i\,m+\bigl(\mathrm{pre}[J]-\mathrm{pre}[i]+(J-i)R\bigr)+(k-J)\,m,$$

$O(1)$ 一步即可。更妙的是 $R$ 只增 ⇒ 阈值 $m-R$ 只减 ⇒ $J$ **只左移**；$L$ 只增 ⇒ $i$ 只右移。两个指针都单向，全部 $n+1$ 次询问合计 $O(k)$。

算法流程：

1. 扫一遍建 $r$（遇到 1 就 push 当前 0 的计数），得 $k,m$；做前缀和 `pre`，令 $total=km$。
2. `L = R = 0`，`J = k`（尚无元素封顶）。
3. 输出 `total - S`；再按 $s_i$ 更新 $L$ 或 $R$（同时推进 `J`）并输出，直到第 $n$ 次操作之后。
4. 每步 `i = min(L, k)`，`while (J > 0 && r[J-1] + R >= m) J--;`，`jj = max(J, i)`，代入上式。

### 3.4 示例演算

![样例 1 逐步走查：r 从 (0,0) 演化到 (2,2)，答案 4 2 1 0 0](images/cf2259_f_walkthrough.svg)

$n=4$，$a=[1,1,0,0]$，$s=1010$：$k=2$，$m=2$，$r=(0,0)$，$total=4$。

| 步 | 操作 | $L$ | $R$ | $i$ | 存活项取值 | $S$ | $I$ |
|----|------|-----|-----|-----|-----------|-----|-----|
| 0 | 初始 | 0 | 0 | 0 | $r_1=0,\ r_2=0$ | 0 | **4** |
| 1 | bubble | 1 | 0 | 1 | $r_2=0$（$r_1$ 已弹出） | 2 | **2** |
| 2 | reverse | 1 | 1 | 1 | $\min(0+1,2)=1$ | 3 | **1** |
| 3 | bubble | 2 | 1 | 2 | 无（$i=k$） | 4 | **0** |
| 4 | reverse | 2 | 2 | 2 | 无（$i=k$） | 4 | **0** |

输出 $4\,2\,1\,0\,0$，与官方一致。数组轨迹对应的 $r$ 为 $(0,0)\to(0,2)\to(1,2)\to(2,2)\to(2,2)$，正是「左移补 $m$」与「$+1$ 封顶」两种更新。第 3 步后 $L=2=k$，不会再有 1 被弹出，$i$ 必须封顶在 $k$。

## 4. 算法细节

1. **建 $r$**：0-indexed 扫数组，`zeros` 记已见 0 的个数，遇到 1 就 `push(zeros)`，得到的正是 $p_j-j$；$k=0$（全 0）时 `r` 为空。
2. **前缀和**：`pre[0]=0`，`pre[j+1]=pre[j]+r[j]`，长度 $k+1$，元素一律 `long long`；`total = k * m` 也要先转 64 位。
3. **指针 $J$**：初值 `J = k`，只在查询时 `while (J > 0 && r[J-1] + R >= m) J--;`。$R$ 单调不减，故 $J$ 永不回退；先判 `J>0`，空 `r` 也安全。
4. **`jj = max(J, i)`** 不可省：若 $J<i$，存活元素已全部封顶，区间 $[i,J)$ 为空，公式退化为 $S=km$、答案 $0$。
5. **封顶 $i=\min(L,k)$**：$L$ 可能远大于 $k$，直接代入会多算 $(L-k)m$，答案变负。
6. **输出顺序**：先输出初始状态，之后每处理一个 $s_i$ 就更新 $L/R$ 再输出；颠倒会整体错位一格。
7. **多测**：`r`、`pre`、`J`、`L`、`R` 每组重建，不留跨组状态；$\sum n\le5\times10^5$ 保证总分配量可控。
8. **I/O**：共 $O(\sum n)$ 个数字，用一次拼接写回（`fputs`）远快于逐个 `cout`；$s$ 用 `scanf("%s")` 读入定长缓冲。

## 5. 正确性证明

**引理 1**：一次左冒泡的结果等于「删去第一个 1、其余左移一格、末尾补 1」；全 0 数组不变。

**证明**：设扫描到位置 $i$（$1\le i\le n-1$）。归纳断言：位置 $i+1..n$ 仍是原数组元素，$1..i-1$ 已与最终结果相同，位置 $i$ 上是待定元素 $t$。初始 $t=a_1$ 成立。比较 $t$ 与 $a_{i+1}$ 后，位置 $i$ 的终值为 $\min(t,a_{i+1})$、新待定元素为 $\max(t,a_{i+1})$，且位置 $i$ 此后再不被访问。故 $t=\max(a_1,\dots,a_i)$。设首个 1 在 $f$（不存在则数组不变）：$i<f$ 时 $\max(a_1..a_i)=0$，终值 $0=a_i$；$f\le i\le n-1$ 时终值 $a_{i+1}$；位置 $n$ 的终值为 $\max(a_1..a_n)=1$。合起来正是「删去位置 $f$ 的 1、其后左移一格、末尾补 1」。∎

**引理 2**：一次右冒泡的结果等于「删去最后一个 0、其余右移一格、开头补 0」。

**证明**：令 $c_i=1-a_{n+1-i}$。对 $c$ 做左冒泡时第 $i$ 步比较 $c_i,c_{i+1}$：条件 $c_i>c_{i+1}$ 等价于 $a_{n-i}>a_{n+1-i}$，交换二者等价于交换 $a_{n-i},a_{n+1-i}$；$i$ 从 $1$ 增到 $n-1$ 对应 $j=n-i$ 从 $n-1$ 减到 $1$。故「$c$ 的左冒泡」与「$a$ 的右冒泡」是同一串交换。该变换把首个 1 映为最后一个 0、把末尾补 1 映为开头补 0，由引理 1 得证。∎

**引理 3**：$r_j=p_j-j$ 非降，$I=km-\sum_j r_j$；左冒泡使 $r\leftarrow(r_2,\dots,r_k,m)$，右冒泡使 $r_j\leftarrow\min(r_j+1,m)$，更新后仍非降。

**证明**：$p_{j+1}>p_j$ 给出 $r_{j+1}\ge r_j$，且 $r_k=p_k-k\le n-k=m$。第 $j$ 个 1 右边有 $m-r_j$ 个 0，每个贡献一个逆序对，求和即 $I$。左冒泡：由引理 1，原第 $j$ 个 1（$j\ge2$）移到 $p_j-1$ 成为新的第 $j-1$ 个 1，故 $r'_{j-1}=p_j-1-(j-1)=r_j$；新 1 在位置 $n$，$r'_k=n-k=m$。右冒泡：由引理 2，$p_j<q$（$q$ 为最后一个 0 的位置）的 1 右移一格得 $r_j+1$，其余 $r_j=m$ 且不动，而 $r_j=m$ 与 $p_j>q$ 等价，故统一为 $\min(r_j+1,m)$。两种更新分别保序（左移后末尾接 $m\ge r_k$；$\min(x+1,m)$ 单调）。∎

**引理 4**：执行 $L$ 次左冒泡与 $R$ 次右冒泡后，当前序列恰为 $\bigl(\min(r_{i+1}+R,m),\dots,\min(r_k+R,m)\bigr)$ 后接 $i$ 个 $m$，其中 $i=\min(L,k)$。

**证明**：对 $L+R$ 归纳。$L=R=0$ 时 $i=0$，序列即 $(r_1,\dots,r_k)$。若当前如所述，做一次左冒泡：由引理 3 序列左移一格、末尾补 $m$，得到 $(\min(r_{i+2}+R,m),\dots,\min(r_k+R,m))$ 后接 $i+1$ 个 $m$，而 $i+1=\min(L+1,k)$，与 $L+1$ 的式子一致。做一次右冒泡：逐项 $\min(x+1,m)$，由 $\min(\min(r_j+R,m)+1,m)=\min(r_j+R+1,m)$ 且 $m$ 项仍为 $m$，得到 $R+1$ 的式子。∎

**定理**：程序在第 $t$ 步输出的整数等于第 $t$ 步数组的真实逆序数。

**证明**：由引理 4，当前 $S=i\,m+\sum_{j>i}\min(r_j+R,m)$。因 $r$ 非降，$\{j:r_j\ge m-R\}$ 是后缀，$J$ 取其起点，则 $j\in(i,J)$ 贡献 $r_j+R$、$j\ge J$ 贡献 $m$；程序用 `pre[J]-pre[i]` 与 `(J-i)R` 累加前者、$(k-J)m$ 统计后者。若 $J<i$，由非降性所有 $j>i\ge J$ 都已封顶，`jj=max(J,i)=i` 使公式退化为 $i\,m+(k-i)m=km$，同样正确。故程序算出的 $S$ 即真实 $\sum_j r_j$，由引理 3 得 $I=km-S$ 为真实逆序数。∎

**实验验证**：与按题面定义直接模拟的暴力对拍——(1) $n\le7$ 的**全部** $(a,s)$ 组合共 $\sum_{n=1}^{7}4^n=21844$ 组；(2) 1500 组 $n\le16$ 随机数据；(3) 300 组 $n\le300$ 随机数据，操作串刻意做成块状以制造长连续同类操作；(4) 48 组极端数据（全 0、全 1、单 1、单 0、交替、已排序、逆序）。全部 **0 差异**；7 组官方样例逐字符一致；C++ 与 Python 两份实现在最大数据上输出逐字节相同。

## 6. 复杂度分析

- **时间**：建 $r$ 为 $O(n)$，前缀和 $O(k)$，每步查询 $O(1)$ 均摊（`J` 至多左移 $k$ 次，`i` 只增），共 $n+1$ 次查询，输出 $O(n)$ 个数。单组 $O(n)$，总计 $O(\sum n)\le5\times10^5$ 量级。
- **空间**：$O(n)$，只需 $r$、前缀和与输出缓冲，无递归、无哈希表。
- **对照时限**：$n=5\times10^5$ 单组实测 C++ 约 $0.03$ s（3 s 时限，余量约 100 倍）；$t=10^4,\sum n=5\times10^5$ 的多测形态亦约 $0.03$ s；Python 同数据约 $0.36$ s，同样安全。
- **备选写法**：用 `lower_bound` 定位 $J$ 得 $O(n\log n)$，$5\times10^5$ 时约 $10^7$ 次比较，仍在时限内。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;
    static char buf[500005];
    while (t--) {
        int n; scanf("%d", &n);
        vector<int> a(n);
        for (int i = 0; i < n; i++) scanf("%d", &a[i]);
        scanf("%s", buf);                        // s 长度恰为 n
        vector<long long> r;                     // r[j] = 第 j 个 1 左边 0 的个数（非降）
        r.reserve(n);
        long long zeros = 0;
        for (int i = 0; i < n; i++) { if (a[i] == 0) zeros++; else r.push_back(zeros); }
        long long k = (long long)r.size(), m = zeros;
        vector<long long> pre(k + 1, 0);
        for (long long i = 0; i < k; i++) pre[i + 1] = pre[i] + r[i];
        long long total = k * m, L = 0, R = 0;   // 逆序数 I = k*m - sum(r)
        long long J = k;                         // 首个 r_J + R >= m 的下标，随 R 只左移
        auto answer = [&]() -> long long {
            long long i = min(L, k);             // L 超过 k 后不再弹出新元素
            while (J > 0 && r[J - 1] + R >= m) J--;
            long long jj = max(J, i);            // 存活项可能已全部封顶
            long long S = i * m + (pre[jj] - pre[i]) + (jj - i) * R + (k - jj) * m;
            return total - S;
        };
        string out; out.reserve((size_t)n * 8);
        out += to_string(answer());              // 初始状态
        for (int i = 0; i < n; i++) {
            if (buf[i] == '1') L++; else R++;
            out += ' '; out += to_string(answer());
        }
        out += '\n';
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
    t = int(data[0])
    pos = 1
    out_lines = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        a = data[pos:pos + n]; pos += n
        s = data[pos].decode(); pos += 1
        r = []                      # 第 j 个 1 左边 0 的个数（非降）
        zeros = 0
        for x in a:
            if x == b'0': zeros += 1
            else: r.append(zeros)
        k = len(r); m = zeros
        pre = [0] * (k + 1)
        for i in range(k): pre[i + 1] = pre[i] + r[i]
        total = k * m
        L = R = 0                   # 左冒泡 / 右冒泡次数
        J = k                       # 首个 r_j + R >= m 的下标
        res = []
        for step in range(n + 1):
            i = L if L < k else k   # 封顶在 k
            while J > 0 and r[J - 1] + R >= m: J -= 1
            jj = J if J > i else i
            res.append(total - (i * m + (pre[jj] - pre[i]) + (jj - i) * R + (k - jj) * m))
            if step < n:
                if s[step] == '1': L += 1
                else: R += 1
        out_lines.append(' '.join(map(str, res)))
    sys.stdout.write('\n'.join(out_lines) + '\n')


main()
```

## 8. 边界情况与易错点

1. **全 0 数组**（$k=0$）：`r` 为空，`J=0`、`i=0`、$S=0$，答案恒 $0$；`while` 必须先判 `J>0`，否则访问 `r[-1]`。
2. **全 1 数组**（$m=0$）：$total=0$，$\min(r_j+R,0)=0$，$S=0$，答案恒 $0$，右冒泡也不再改变数组。
3. **$L>k$**：必须用 $i=\min(L,k)$，否则多算 $(L-k)m$ 出现负答案——本题最容易漏的一处。
4. **$R\ge m$**：阈值 $m-R\le0$，`while` 把 `J` 推到 $0$，`jj=max(0,i)=i`，全部按 $m$ 计，结果仍是 $km$（正确），无需额外特判。
5. **溢出**：$k\cdot m$ 与 $S$ 可达 $6.25\times10^{10}$，`int` 溢出，一律 `long long`（Python 无此问题）。
6. **输出个数是 $n+1$**：最后一次操作之后的状态也要输出，漏掉就是「答案少一个」。
7. **顺序**：先输出当前状态，再按 $s_i$ 更新 $L/R$；反过来整体错位一格。
8. **多测重置**：`J`、`L`、`R`、`r`、`pre` 每组重新初始化，不能沿用上一组；$n=1$ 时只会输出两个数，逻辑上无需特判。

## 相关题目与扩展

- [Codeforces 2259G. Index Removal](https://codeforces.com/problemset/problem/2259/G)：同场 G 题，二分答案 + 数据结构维护，可与本题的「状态压缩 + 闭式」对照。
- [Codeforces 2259E. Treasure Map Destruction (Constructive Version)](https://codeforces.com/problemset/problem/2259/E)：同场构造题，练习「先找不变量再构造」。
- [LeetCode 775. 全局倒置与局部倒置](https://leetcode.cn/problems/global-and-local-inversions/)：逆序数与「相邻交换」的关系，引理 1 正是「一趟扫描搬动多格」的极端形态。
- [LeetCode 493. 翻转对](https://leetcode.cn/problems/reverse-pairs/)：逆序类计数的分治 / BIT 模板，适合处理多值版本。
- [Codeforces 1676H2. Maximum Crossings (Hard Version)](https://codeforces.com/problemset/problem/1676/H2)：用 BIT 统计逆序对，对照本题「不数对子、直接维护总量」。

**延伸思考**：

1. **要求输出每次操作后的数组本身**：记录每步「被删掉的是哪个 1 / 哪个 0」的下标，用双端队列维护剩余元素顺序，仍是 $O(n)$。
2. **询问任意时刻 $(L,R)$ 的答案**：引理 4 的闭式对任意 $L,R$ 成立，离线询问可 $O(1)$（预处理 $J$ 的跳变点），在线用二分找 $J$，$O(\log n)$。
3. **把「整趟」换成「只处理一对相邻元素」**：一步至多减少 1 个逆序对，状态无法用闭式压缩，只能模拟；这反过来说明本题的关键是整趟扫描的搬运量。
4. **多值数组**（$a_i\in\{0,\dots,V\}$）：$r$ 编码失效，需要块状链表或树套树模拟整趟冒泡，复杂度升到 $O(n\log n)$ 以上。
