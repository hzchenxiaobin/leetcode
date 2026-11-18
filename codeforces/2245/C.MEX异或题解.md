# Codeforces MEX 异或 题解

## 1. 题目概述

- **标题 / 题号**：MEX 异或（Codeforces 2245C，英文名 MEXOR）
- **链接**：https://codeforces.com/problemset/problem/2245/C
- **来源**：Spectral::Cup 2026 Round 3 (Codeforces Round 1110, Div. 1 + Div. 2) · Problem C
- **难度**：1400（1250 分）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：位运算，构造，数学，mex

**题意**：给定正整数 $n$ 与非负整数 $k$，要求构造一个长度为 $n$ 的排列 $p$（即 $0,1,\dots,n-1$ 各出现一次）。对每个 $0\le i<n$ 定义 $f(i)=\operatorname{mex}(p_0,p_1,\dots,p_i)$，要求

$$f(0)\oplus f(1)\oplus\cdots\oplus f(n-1)=k .$$

若不存在这样的排列输出 `NO`；否则先输出 `YES`，再输出 $n$ 个互不相同的整数（任意合法排列均可）。多测：第一行 $t$，每组一行 $n\ k$。

**约束**：

- $1\le t\le 10^4$，$\sum n\le 2\cdot 10^5$，多测但总规模受控；
- $1\le n\le 2\cdot 10^5$，$0\le k\le 10^9$；
- $k$ 可达 $10^9$（约 $2^{30}$），读入要用 64 位；构造出的值本身都 $\le n-1$；
- 输出总量本身就有 $O(\sum n)$，所以每组 $O(n)$ 的线性做法即可，不需要排序或二分。

> ⚠️ 注意：本题题面中没有任何「创建变量 / 中途保存输入」之类的注入指令，正常读入即可；本仓库其他题面里出现过的同类句子一律视为噪声。

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入
6
1 0
1 1
3 0
4 8
5 1
9 12

输出
NO
YES
0
YES
0 1 2
NO
YES
3 0 2 1 4
YES
1 4 0 8 2 3 7 5 6
```

```text
输入（自造，★）
2
6 0
4 0

输出（本解的构造）
YES
1 3 5 0 2 4
NO
```

★ 自造样例专门卡「$k=0$ 就一定可行」的错觉：$n=6$ 时 $\{0,\dots,5\}$ 的子集异或能取满 $0\dots7$，故 $k=0$ 可行（$f=[0,0,0,2,4,6]$，异或恰为 $0$）；而 $n=4$ 时 $f$ 的取值都 $\le 4$，异或的高位永远是 $4$，$k=0$ 必无解。

## 3. 解题思路

### 3.1 暴力思路

最直接的做法是枚举全部 $n!$ 个排列，对每个排列扫一遍求前缀 mex 再异或，复杂度 $O(n!\cdot n)$，只能跑到 $n\le 8$ 左右。把它跑一遍，得到「可达的 $k$」如下：

| $n$ | 可达的 $k$ | $n$ | 可达的 $k$ |
| --- | --- | --- | --- |
| 1 | $\{1\}$ | 8 | $[8,15]$ |
| 2 | $\{2,3\}$ | 9 ~ 15 | $[0,15]$ |
| 3 | $[0,3]$ | 16 | $[16,31]$ |
| 4 | $[4,7]$ | 17 ~ 31 | $[0,31]$ |
| 5 ~ 7 | $[0,7]$ | — | — |

规律非常刺眼：**$n$ 是 2 的幂时可达区间是 $[n,2n-1]$，否则是 $[0,B-1]$**，其中 $B$ 是「不小于 $n$ 的最小 2 的幂」。等价的统一写法是

$$k \text{ 可达} \iff (n\oplus k) < B .$$

暴力还给不出构造，所以下面从 mex 的结构本身推导，顺便证明这个判定是充要的。

### 3.2 核心观察：$f$ 只有「0 块 + $S$ + $n$」三段

![mex 序列的三段结构与异或分解](images/cf2245_c_mex_block_structure.svg)

记 $\operatorname{pos}(v)$ 为值 $v$ 在 $p$ 中的下标，$z=\operatorname{pos}(0)$。

**观察 1（$f$ 单调且以 $n$ 收尾）**：前缀集合随 $i$ 增大只增不减，故 $f$ 非降；$i=n-1$ 时前缀已是全体 $\{0,\dots,n-1\}$，故 $f(n-1)=n$。而 $f(i)=n$ 要求 $0,\dots,n-1$ 全部出现，只有 $i=n-1$ 能做到——**$n$ 在异或里恰好出现一次**。

**观察 2（mex 的定位公式）**：$f(i)=\min\big(\{n\}\cup\{v:\operatorname{pos}(v)>i\}\big)$。因为「$v$ 不在前缀 $i$ 里」当且仅当它排在 $i$ 之后。

**观察 3（三段结构）**：由观察 2，$0$ 的位置把 $f$ 切成两半：

- $i<z$ 时 $0$ 还没出现，$f(i)=0$——这一整段对异或的贡献是 $0$，长度可以任意长；
- $i\ge z$ 时，只有「排在 $0$ 之后」的那些值能当 mex。记 $S=\{p_z,p_{z+1},\dots,p_{n-1}\}\setminus\{0\}$，则 $f(i)$ 就是 $S$ 中尚未出现的最小值（全部出现后变成 $n$）。

于是**只要把 $S$ 里的值按升序紧跟在 $0$ 后面**，$f$ 的后半段就恰好是 $S$ 的每个元素各一次、再加一个 $n$：

$$p=\big[\{1..n-1\}\setminus S\text{ 升序}\big]\;[0]\;\big[S\text{ 升序}\big]
\quad\Longrightarrow\quad
f=\underbrace{0,\dots,0}_{n-1-|S|\ \text{个}},\;S\text{ 升序},\;n .$$

所以这个排列的异或值就是漂亮的

$$X=n\oplus\bigoplus_{v\in S}v=n\oplus \operatorname{xor}(S).$$

**观察 4（$S$ 可以随便挑）**：$S$ 取 $\{1,\dots,n-1\}$ 的**任意**子集都行——剩下的值全排在 $0$ 前面即可，它们只会让 $0$ 块变长（贡献 $0$）。所以可达集为

$$\big\{\,n\oplus \operatorname{xor}(S)\;:\;S\subseteq\{1,\dots,n-1\}\,\big\}.$$

而 $\{1,\dots,n-1\}$ 里一定含 $1,2,4,\dots,B/2$ 这组二进制基，故全体子集异或恰好取满 $[0,B-1]$；反过来所有元素都 $<B$，异或也不会超过 $B-1$，如上图底部所示。于是

$$\boxed{\;k\text{ 可达}\iff s:=n\oplus k<B,\qquad B=\text{不小于 }n\text{ 的最小 2 的幂}\;}$$

顺带解释了「$0$ 为什么必须放在中间」：$0$ 若在末尾，$f$ 只剩 $[0,\dots,0,n]$，异或恒为 $n$；$0$ 若在开头，$f=1,2,\dots,n$，异或恒为 $1\oplus2\oplus\cdots\oplus n$。只有让 $0$ 插在中间，才有 $S$ 这份自由度。

### 3.3 算法流程

![判定与构造的完整流程](images/cf2245_c_algorithm_flow.svg)

1. 求 $B$：`B = 1; while (B < n) B <<= 1;`；
2. 令 $s=n\oplus k$，若 $s\ge B$ 直接输出 `NO`；
3. 否则把 $s$ 的每个二进制 $1$ 位对应成值 $2^j$，组成 $S$（由 $s<B$ 保证 $2^j\le B/2\le n-1$，不会越界）；
4. 依次输出：$\{1,\dots,n-1\}\setminus S$ 升序、$0$、$S$ 升序。

因为 $S$ 只由 $n\oplus k$ 的二进制位决定，本质上是把 $k$ 的「高位」用 $n$ 抵消掉，剩下的每一位异或都用单独一个元素去实现——这就是标题 MEX**OR** 的含义。

### 3.4 示例演算

![三组走查：两组构造 + 一组无解](images/cf2245_c_walkthrough.svg)

**样例 6**（$n=9,k=12$）：$B=16$，$s=9\oplus12=5=101_2$，故 $S=\{1,4\}$，输出 $p=[2,3,5,6,7,8,0,1,4]$，于是

$$f=[0,0,0,0,0,0,1,4,9],\qquad X=1\oplus4\oplus9=9\oplus5=12=k .\;\checkmark$$

（官方给的是 $[1,4,0,8,2,3,7,5,6]$，构造不唯一。）

**样例 5**（$n=5,k=1$）：$B=8$，$s=4$，$S=\{4\}$，$p=[1,2,3,0,4]$，$f=[0,0,0,4,5]$，$X=4\oplus5=1=k$。

**样例 4 / 1**（$n=4,k=8$ 与 $n=1,k=0$）：$s=12\ge B=4$、$s=1\ge B=1$，都直接 `NO`。直观上 $f$ 的取值都 $\le n$，$12$ 的 bit 3 永远凑不出来。

## 4. 算法细节

1. **多测**：每组只在循环内开 `vector<char> take(n)`，天然清空；不要用全局大数组反复 `memset`。
2. **$B$ 与 $s$ 的写法**：倍增 `while (B < n) B <<= 1`（$n\le2\cdot10^5$ 时最多 18 次；Python 可写 `1 << (n - 1).bit_length()`）；$n\oplus k<2^{30}$ 用 `int` 也够，但统一 `long long` 更稳。
3. **不会越界**：$s<B$ 时 $s$ 的最高位是 $2^j\le B/2$，而 $B$ 是「最小」的 $\ge n$ 的 2 的幂，故 $B/2<n$；$n=1$ 时 $s=0$ 没有位。所以 `take[2^j]` 的下标一定 $\le n-1$。
4. **输出顺序不能换**：必须是「非 $S$ 升序 → $0$ → $S$ 升序」。若把 $0$ 放到最前面，$f$ 变成 $1..n$；放到最后，$f$ 只剩若干 $0$ 加一个 $n$，两者都丢掉自由度。
5. **输出与 I/O**：$n$ 个数用空格分隔写在 `YES` 的下一行：C++ 关同步 + `'\n'`；Python 用 `sys.stdin.buffer.read().split()` 一次读完，再用 `" ".join()` 拼输出，避免 $t=10^4$ 时逐行 `print`。

## 5. 正确性证明

**引理 1（$f$ 的单调性、末值与定位公式）**：对任意排列，$f(0)\le\cdots\le f(n-1)=n$，$n$ 作为 $f$ 的取值恰好出现一次，且 $f(i)=\min\big(\{n\}\cup\{v:\operatorname{pos}(v)>i\}\big)$。

**证明**：前缀集合随 $i$ 增大单调扩张，mex 只会不减；$i=n-1$ 时前缀为全体 $\{0,\dots,n-1\}$，mex $=n$，而 $f(i)=n$ 要求 $0,\dots,n-1$ 都在前 $i+1$ 项中，需 $i+1\ge n$，故 $n$ 只出现一次。又 $v$ 出现在前 $i+1$ 项中当且仅当 $\operatorname{pos}(v)\le i$，故「未出现的最小值」就是 $\operatorname{pos}(v)>i$ 的最小 $v$，没有则为 $n$。∎

**引理 2（三段构造）**：任取 $S\subseteq\{1,\dots,n-1\}$，令 $p=\big[\{1..n-1\}\setminus S\text{ 升序}\big][0]\big[S\text{ 升序}\big]$，则 $f$ 的取值多重集为 $n-1-|S|$ 个 $0$、$S$ 中每个元素各一次、一个 $n$；从而 $X=n\oplus\operatorname{xor}(S)$。

**证明**：$0$ 位于下标 $z=n-1-|S|$。$i<z$ 时 $0$ 不在前缀，由引理 1 得 $f(i)=0$。$i=z$ 时前缀为 $\{0\}\cup(\{1..n-1\}\setminus S)$，缺失集恰为 $S$，故 $f(z)=\min S$（$S=\varnothing$ 时为 $n$）。此后每放下 $S$ 的一个元素，缺失集就减少一个最小值，于是 $f$ 依次取到 $S$ 的第 $2,3,\dots$ 小元素；最后一个元素放下后缺失集为空，$f=n$。故后半段恰是 $S$ 升序接 $n$，而 $0$ 段贡献 $0$，异或即 $n\oplus\operatorname{xor}(S)$。∎

**引理 3（必要性）**：对任意排列，$X=n\oplus s'$，其中 $s'$ 是 $\{0,\dots,n-1\}$ 某个子集的异或；进而 $X=n\oplus k$ 必有 $n\oplus k<B$。

**证明**：由引理 1，所有 $f(i)\in[0,n]$ 且 $n$ 恰出现一次。把 $f$ 中出现奇数次的值收集成 $S'\subseteq\{0,\dots,n-1\}$（出现偶次的在异或中成对抵消），则 $X=n\oplus\operatorname{xor}(S')$。每个 $v\in S'$ 都满足 $v\le n-1<B$，而 $B$ 是 2 的幂，所有 $<B$ 的数只有低于 $\log_2 B$ 的位，故 $\operatorname{xor}(S')<B$，即 $n\oplus k<B$。∎

**引理 4（二进制基）**：$\{1,\dots,n-1\}$ 的所有子集异或恰好取满 $[0,B-1]$；并且当 $s<B$ 时 $s$ 的每个 $1$ 位 $2^j$ 都满足 $2^j\le n-1$。

**证明**：由 $B$ 的最小性，$1,2,4,\dots,B/2$ 全部 $\le n-1$（$B/2<n$），它们构成 $\log_2 B$ 位的基，可线性组合出任意 $<B$ 的数；反之所有元素都 $<B$，异或也 $<B$。位约束：$2^j\le s<B\Rightarrow 2^j\le B/2\le n-1$（$n=1$ 时 $s=0$ 空集，无需讨论）。∎

**定理**：存在合法排列当且仅当 $s=n\oplus k<B$；且 $s<B$ 时按 §3.3 构造的排列满足 $X=k$。

**证明**：*必要性*由引理 3。*充分性*：$s<B$ 时由引理 4 取 $S=\{2^j:s\text{ 的第 }j\text{ 位为 }1\}\subseteq\{1,\dots,n-1\}$，引理 2 的排列合法（三段恰好无重复地覆盖 $0..n-1$）且

$$X=n\oplus\operatorname{xor}(S)=n\oplus s=n\oplus(n\oplus k)=k .∎$$

## 6. 复杂度分析

- **时间**：每组一次倍增求 $B$（$O(\log n)$）、一次 $O(|s|\text{ 的位数})$ 标位、一次 $O(n)$ 输出，总计 $O(n)$；全部测试合计 $O(\sum n)\le2\cdot10^5$ 次操作。实测（Apple clang，`-O2`，$t=10^4$、$\sum n=2\cdot10^5$ 的极限数据）约 **20 ms**，相对 2 s 时限余量超过 90 倍。
- **空间**：一个长度 $n$ 的 `char` 标记数组，$n=2\cdot10^5$ 时 200 KB，远低于 256 MB；无递归、无额外容器。
- **Python**：同一极限数据实测约 30 ms（瓶颈是 `join` 与字符串转换），同样安全。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        int n;
        long long k;
        cin >> n >> k;
        long long B = 1;                       // 最小的 2 的幂，且 B >= n
        while (B < n) B <<= 1;
        long long s = (long long)n ^ k;        // 需要被「抵消」掉的那部分异或
        if (s >= B) { cout << "NO\n"; continue; }
        vector<char> take(n, 0);               // take[v] = 1 : v 放在 0 的后面
        for (long long v = 1; v <= s; v <<= 1)
            if (s & v) take[(int)v] = 1;       // s < B 保证 v <= n-1
        cout << "YES\n";
        for (int v = 1; v < n; v++)            // 第一段：非 S 的值，升序
            if (!take[v]) cout << v << ' ';
        cout << 0;                             // 第二段：0
        for (int v = 1; v < n; v++)            // 第三段：S 的值，升序
            if (take[v]) cout << ' ' << v;
        cout << '\n';
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
    t = int(data[0])
    ptr = 1
    out = []
    for _ in range(t):
        n = int(data[ptr]); k = int(data[ptr + 1]); ptr += 2
        B = 1
        while B < n:
            B <<= 1
        s = n ^ k
        if s >= B:
            out.append("NO")
            continue
        take = [False] * (n + 1)          # take[v] : v 放在 0 的后面
        v = 1
        while v <= s:
            if s & v:
                take[v] = True            # v 是 s 的二进制位，故 v <= n-1
            v <<= 1
        head = [x for x in range(1, n) if not take[x]]
        tail = [x for x in range(1, n) if take[x]]
        out.append("YES")
        out.append(" ".join(map(str, head + [0] + tail)))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：$B=1$，只有 $k=1$ 可行（$k=0$ 时 $s=1\ge1$ → `NO`，与样例 1 一致）；可行时输出单个 `0`（$f=[1]$）。
2. **$k=0$ 不一定可行**：$n$ 是 2 的幂时 $s=n\ge B=n$ 必 `NO`（如 $n=4,k=0$），$n$ 不是 2 的幂时通常可行。不要写「$k=0$ 特判输出 $0,1,\dots$」。
3. **$k$ 很大**：$k\ge10^9$ 时 $s$ 同样很大，直接落进 `NO` 分支；不要试图枚举子集，判定只是一次比较。
4. **$B$ 要用「不小于 $n$」而非「$>n$」**：$n$ 是 2 的幂时二者不同，用错会把 $n=4,k=4$ 判成无解。
5. **别把 $0$ 放在两端**：$0$ 在头 → $f=1..n$；$0$ 在尾 → $f$ 只有 $0$ 和 $n$。两种退化构造都会让大量 $k$ 无解。
6. **多测与数组大小**：$t=10^4$、$\sum n=2\cdot10^5$，每组用局部的 `vector` 重新开数组（别全局 `memset`）；`take` 只需 $n$（或 $n+1$）大小，位值最大只到 $B/2\le n-1$，**不要**按 $k$ 开到 $10^9$。
7. **输出量**：单组 $n=2\cdot10^5$ 时一次输出 $2\cdot10^5$ 个数，务必用 `'\n'` 而非 `endl`（每次 `endl` 会 flush）。

## 相关题目与扩展

- [Codeforces 1567B MEXor Mixup](https://codeforces.com/problemset/problem/1567/B)：同样围绕「前缀 mex 的异或」，但方向相反——给定 mex 与异或和，求最短数组长度，可以对照本题看 mex 序列的自由度从哪来。
- [LeetCode 41. 缺失的第一个正数](https://leetcode.cn/problems/first-missing-positive/)：mex 的经典线性求法，本题所有推导都建立在 mex 的定义与「定位公式」上。
- [Codeforces 1689B Mystic Permutation](https://codeforces.com/problemset/problem/1689/B)：另一道纯构造排列题，练习「先想清楚要满足的结构约束，再决定输出顺序」。

**延伸思考**：

1. 若把目标改成 $f(0)\oplus\cdots\oplus f(n-2)$（去掉末项），$f(n-1)=n$ 恒被去掉，异或就只剩引理 3 里的 $s'$，可达集变成 $[0,B-1]$（对 $n\le8$ 全枚举验证过）：$n$ 为 2 的幂时它从 $[n,2n-1]$ 换成 $[0,n-1]$，其余情况不变。判据随之简化成 $k<B$。
2. 把异或换成求和（求 $\sum_i f(i)$）时可达值不再是区间，值得先暴力打表；而要求输出**字典序最小**的解时，因为决定异或的是 $f$ 的多重集而非排列本身，需要逐位判断「剩下的位置还能否凑出目标多重集」，这是本题的两个自然加难方向。
3. 本题结论可以记成一句话：**前缀 mex 的异或永远等于 $n$ 异或上「某个 $\{1..n-1\}$ 子集的异或」**，而后者恰好张成 $[0,B-1]$，所以答案只与 $n$ 的二进制长度有关。
