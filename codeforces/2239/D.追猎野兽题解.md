# Codeforces 追猎野兽 题解

## 1. 题目概述

- **标题 / 题号**：追猎野兽（Codeforces 2239D，英文名 Hunting the Beast）
- **链接**：https://codeforces.com/problemset/problem/2239/D
- **来源**：Codeforces Round 1105 (Div. 1) · Problem D
- **难度**：2500（$\ast 2500$，2000 分）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：组合数学、图论、生成函数、拉格朗日反演、容斥（官方标签：combinatorics, dp, graphs, math）

**题意**：给定 $n,m$。称一张有向图为**函数图**，若 $n$ 个点每个点恰有一条出边；本题还保证没有自环，即每个点的出边指向其余 $n-1$ 个点中的任意一个，故共有 $(n-1)^n$ 张图。

对一张图 $G$ 和一个大小恰为 $m$ 的点集 $S$：若从 $S$ 中某个点出发能到达所有点（点可达自身），则称 $S$ 是**成功的**。$G$ 的值 = 成功集合的个数。求所有 $(n-1)^n$ 张图的值的总和，对 $998244353$ 取模。

**约束**：

- $1 \le t \le 10^4$，$\sum n \le 10^6$：必须整体近线性，单组 $O(n)$ 或更优
- $1 \le m \le n \le 10^6$：既不能枚举图（$(n-1)^n$），也不能枚举集合（$\binom{n}{m}$）
- 模数 $998244353$ 是质数：阶乘逆元可用，无需 NTT

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
5
2 1
3 1
3 2
4 2
8 3

输出：
2
12
18
216
20415360
```

补一组自造样例，覆盖 $n=1$、$m=n$、$m=1$ 三种边界（答案依次为 $0$、$(n-1)^n$、$n!(n-1)$）：

```text
输入：
4
1 1
2 2
4 1
5 5

输出：
0
1
72
1024
```

## 3. 解题思路

### 3.1 暴力思路

直接枚举 $(n-1)^n$ 张图，对每张图枚举 $\binom{n}{m}$ 个集合、对每个集合做正向 BFS 判可达性，复杂度 $O\big((n-1)^n\cdot \binom{n}{m}\cdot n\big)$。$n$ 才 $8$ 就已经是 $7^8\times 56\approx 3\times 10^8$，完全不可行。瓶颈在于「图」和「集合」两层枚举都是指数级，必须把两层都数掉。

### 3.2 核心观察：成功集的结构刻画

![成功集的等价刻画](images/cf2239_d_structure.svg)

**第一步：交换求和、固定 $S$。** 设 $A(n,m)$ 为「固定某个 $S$（$|S|=m$）时，使它成功的图数」。图的重标号不改变成功与否，而任何两个 $m$ 元集合都能被某个置换互相映射，故每个 $S$ 对应的图数相同：

$$\text{答案}=\sum_{G}\#\{S:\ |S|=m,\ S\ \text{成功}\}=\binom{n}{m}\cdot A(n,m).$$

因此只需数 $A(n,m)$：把 $S$ 中的点叫**黑点**（$m$ 个），其余叫**白点**（$k=n-m$ 个）。

**第二步：函数图的分量结构。** 每个弱连通分量有 $N$ 个点、$N$ 条边且弱连通，故恰含一个环；其余点构成指向这个环的树（内向树）。因无自环，环长 $\ge 2$。一个分量若「环上没有任何挂树」称为**纯环分量**。

**第三步：刻画成功。** 点 $u$ 被覆盖，等价于「所有正向路径经过 $u$ 的点」中有黑点，也就是 $u$ 的**反向子树**（$u$ 及其所有后代）里含黑点。

- 若 $u$ 是树叶子（入度 $0$），反向子树只有它自己，故它必须在 $S$ 中；
- 反之若所有叶子都在 $S$ 中，则任何点的反向子树必含某个叶子（有限树必有叶子），故一切都覆盖；
- 环上点的反向子树是整个分量（沿环能绕一圈），所以只要分量里有黑点它就安全。

于是：

> **引理（刻画）**：$S$ 成功 $\iff$ (i) 每个叶子都在 $S$ 中；(ii) 每个纯环分量都含 $S$ 中的点。

（非纯环分量必有叶子，由 (i) 自动含黑点，所以 (ii) 只需管纯环。）

### 3.3 计数：组件分解 + 生成函数

![组件分解与生成函数推导](images/cf2239_d_gf_model.svg)

记 $x$ 标记白点、$y$ 标记黑点，用指数型生成函数（EGF）组装「带标记的点集上的图」，最后乘以 $k!\,m!$ 即得个数。

**挂树**：挂在环上的树（根是环点的孩子），要求所有叶子为黑。一棵挂树 = 一个节点 + 一组挂树儿子；节点为空儿子时只能是黑点。故

$$R=y+(x+y)\left(e^{R}-1\right).$$

**纯环**：长度 $L\ge 2$ 的有向环（有向环的 EGF 是 $\sum_{L\ge1}w^{L}/L=-\ln(1-w)$），环上至少一个黑点，无挂树：

$$P=\sum_{L\ge2}\frac{(x+y)^{L}-x^{L}}{L}.$$

**非纯环**：环上每点挂一任意（可空）森林 $e^{R}$，但整体至少挂一棵树：

$$T=\sum_{L\ge2}\frac{\left((x+y)e^{R}\right)^{L}-(x+y)^{L}}{L}.$$

图是组件之集合，故 $G=\exp(P+T)$。令 $s=x+y$，注意 $R=se^{R}-x$ 即 $se^{R}=R+x$，逐项化简：

$$P+T=\Big[-\ln(1-se^{R})-se^{R}\Big]+\ln(1-x)+x=\ln(1-x)-R-\ln(1-x-R),$$

$$G=\exp(P+T)=\frac{(1-x)e^{-R}}{1-x-R}.$$

**换元消去环**：令 $u=x+R$，则 $se^{R}=u$ 且 $u=(x+y)e^{u-x}$，于是

$$G=\frac{(1-x)e^{x-u}}{1-u}=\frac{(x+y)(1-x)}{u(1-u)}.$$

再令 $z=(x+y)e^{-x}$，则 $u=ze^{u}$，$H(z):=\dfrac{z}{u(1-u)}=\dfrac{e^{-u}}{1-u}$，且 $G=(1-x)e^{x}H(z)$。由拉格朗日反演（$u=ze^{u}$）：

$$[z^{j}]H=\frac1j\,[u^{j-2}]\frac{e^{(j-1)u}}{(1-u)^{2}}=\frac1j\cdot\frac{(j-1)^{j}}{(j-1)!}=\frac{(j-1)^{j}}{j!}.$$

**提取系数**：$y$ 只出现在 $(x+y)^{j}$ 中，故

$$A(n,m)=k!\,m!\sum_{j=m}^{n}\frac{(j-1)^{j}}{j!}\binom{j}{m}\,[x^{\,n-j}](1-x)e^{(1-j)x}.$$

$j=n$ 项给出 $(n-1)^{n}$；$j<n$ 时（记 $r=n-j\ge1$、$a=1-j$）

$$[x^{r}](1-x)e^{ax}=\frac{a^{r}}{r!}-\frac{a^{r-1}}{(r-1)!}=\frac{(1-n)(1-j)^{\,n-j-1}}{(n-j)!},$$

代入并利用 $(1-j)^{n-j-1}=(-1)^{n-j-1}(j-1)^{n-j-1}$，这一项化为

$$(n-1)(-1)^{n-j}\binom{n-m}{j-m}(j-1)^{n-1}.$$

令 $t=n-j$（于是 $j-1=m+k-t-1=n-1-t$）并补上 $j=n$ 的项，得到闭式：

$$\boxed{\;A(n,m)=(n-1)\sum_{t=0}^{n-m}(-1)^{t}\binom{n-m}{t}(n-1-t)^{\,n-1}\;}$$

**答案** $=\binom{n}{m}(n-1)\displaystyle\sum_{t=0}^{n-m}(-1)^{t}\binom{n-m}{t}(n-1-t)^{n-1}$，直接逐项计算即可。

> 💡 这个和式本身是一个标准容斥：$\sum_{t=0}^{k}(-1)^{t}\binom{k}{t}(n-1-t)^{n-1}$ 等于「$n-1$ 元到 $n-1$ 元的映射中、像包含某个固定 $k$ 元集的个数」，可以用来交叉验证与记忆。

### 3.4 示例演算

![n=4,m=2 的逐项演算](images/cf2239_d_walkthrough.svg)

取 $n=4,m=2$，则 $k=n-m=2$，$n-1=3$：

| $t$ | $\binom{k}{t}$ | $(-1)^t$ | $(3-t)^3$ | 贡献 |
|-----|-----|-----|-----|-----|
| 0 | 1 | $+$ | $27$ | $+27$ |
| 1 | 2 | $-$ | $8$ | $-16$ |
| 2 | 1 | $+$ | $1$ | $+1$ |

$\sum=27-16+1=12$，故 $A(4,2)=3\times12=36$，答案 $=\binom{4}{2}\cdot36=6\cdot36=216$，与样例一致。

再用样例 $n=8,m=3$（$k=5$）验证：$7^7-5\cdot6^7+10\cdot5^7-10\cdot4^7+5\cdot3^7-2^7=52080$，$A=7\times52080=364560$，答案 $=\binom{8}{3}\cdot364560=56\times364560=20415360$。

## 4. 算法细节

1. **预处理**：先读入全部询问，取 $N=\max n$，一次预处理 $fact[0..N]$ 与 $invfact[0..N]$（$O(N)$），避免每组重复预处理。
2. **组合数**：$\binom{k}{t}=fact[k]\cdot invfact[t]\cdot invfact[k-t]$，两次模乘；**不要**写成 $\binom{n}{t}$，白点数只有 $k=n-m$ 个。
3. **快速幂**：内层每项算 $(n-1-t)^{n-1}$，用 $O(\log n)$ 的快速幂；总项数 $\sum (k+1)\le \sum n\le 10^6$，幂的总代价约 $2\times 10^7$ 次模乘，$2$ s 内非常宽裕。
4. **符号处理**：按 $t$ 的奇偶交替加减；C++ 中做减法后要 `if (S < 0) S += MOD;`，避免负余数。
5. **答案合成**：$\text{ans}=\binom{n}{m}\cdot(n-1)\cdot S \bmod p$，三个因子依次取模，注意 $(n-1)$ 与 $S$ 都是模意义下的数。
6. **底数为 $0$**：$t=k$ 时底数是 $m-1$；$m=1$ 时为 $0^{n-1}=0$（$n\ge2$），快速幂天然给出 $0$，无需特判。
7. **$n=1$**：$(n-1)=0$，答案恒为 $0$；此时式子里的 $0^0$ 由快速幂返回 $1$，再乘 $0$ 仍是 $0$，不会出错。
8. **实现**：用 `scanf`/`printf` 或缓冲输出，$t=10^4$ 组时 I/O 也不能忽视。

## 5. 正确性证明

**引理 1（分量结构）**：任一无自环函数图的每个弱连通分量恰含一个有向环，其余点构成指向该环的树。

**证明**：分量有 $N$ 个点、$N$ 条边（每点出度 $1$）且弱连通，边数等于点数，故恰有一个环；从任一环外点沿出边走必然入环，故所有环外点构成以环为根的内向树。∎

**引理 2（成功集刻画）**：$S$ 成功 $\iff$ (i) 所有叶子（入度 $0$ 的点）属于 $S$；(ii) 每个纯环分量含 $S$ 中的点。

**证明**：$S$ 成功 $\iff$ 对每个点 $u$，其反向子树（能沿出边走到 $u$ 的点集，含 $u$ 自身）含黑点。

- 必要性：叶子 $u$ 的反向子树只有 $u$，故 $u$ 必须为黑。纯环分量中每个环点的反向子树是整个分量（沿环可绕行），若无黑点则环上点全不被覆盖。
- 充分性：设 (i)(ii) 成立。若 $u$ 在环外，其反向子树是有限树，必含一个叶子，由 (i) 该叶子为黑，故 $u$ 被覆盖。若 $u$ 在环上：若该分量非纯环，则它有挂树、从而有叶子，由 (i) 分量内有黑点，$u$ 的反向子树是整个分量，被覆盖；若该分量是纯环，由 (ii) 环上有黑点。∎

**引理 3（挂树生成函数）**：设 $R$ 是「根为非环点、边指向根、所有叶子为黑」的树的 EGF，则 $R=y+(x+y)(e^{R}-1)$。

**证明**：一棵挂树由一个根节点（黑或白，权重 $x+y$）和它的儿子们（一个 SET，EGF 为 $e^{R}$）组成；若儿子集为空则该节点是叶子，只能为黑，权重 $y$，不能用 $x$。故 $R=y+(x+y)(e^{R}-1)$。∎

**引理 4（拉格朗日系数）**：设 $u=ze^{u}$，则 $[z^{j}]\dfrac{e^{-u}}{1-u}=\dfrac{(j-1)^{j}}{j!}$（$j\ge2$），且 $j=0$ 时为 $1$、$j=1$ 时为 $0$。

**证明**：由拉格朗日反演，对 $\Phi(u)=\dfrac{e^{-u}}{1-u}$（$\Phi(u)=z/(u(1-u))$，$\Phi'(u)=\dfrac{ue^{-u}}{(1-u)^{2}}$）：

$$[z^{j}]\Phi=\frac1j\,[u^{j-1}]\Phi'(u)e^{ju}=\frac1j\,[u^{j-2}]\frac{e^{(j-1)u}}{(1-u)^{2}}.$$

而 $\dfrac{1}{(1-u)^{2}}=\sum_{r\ge0}(r+1)u^{r}$，故该系数为 $\sum_{i=0}^{j-2}\dfrac{(j-1)^{i}}{i!}(j-1-i)$，记 $a=j-1$，则

$$\sum_{i=0}^{j-2}\frac{a^{i}}{i!}(a-i)=a\sum_{i=0}^{j-2}\frac{a^{i}}{i!}-a\sum_{i=0}^{j-3}\frac{a^{i}}{i!}=\frac{a^{j-1}}{(j-2)!}=\frac{(j-1)^{j}}{(j-1)!},$$

乘上 $1/j$ 即得。∎

**定理**：固定 $S$ 时成功图数 $A(n,m)=(n-1)\sum_{t=0}^{n-m}(-1)^{t}\binom{n-m}{t}(n-1-t)^{n-1}$。

**证明**：引理 1–3 给出按两类组件组装的 EGF $G=(1-x)e^{-R}/(1-x-R)$，且 $A(n,m)=k!\,m!\,[x^{k}y^{m}]G$；换元 $u=x+R$、$z=(x+y)e^{-x}$ 后化为 $G=(1-x)e^{x}H(z)$，$H(z)=e^{-u}/(1-u)$、$u=ze^{u}$。按 §3.3 的系数提取（引理 4 给出 $[z^{j}]H=(j-1)^{j}/j!$），$j=n$ 项为 $(n-1)^{n}$，$j<n$ 每项化为 $(n-1)(-1)^{n-j}\binom{k}{j-m}(j-1)^{n-1}$；令 $t=n-j$ 并把 $j=n$ 项吸收进和式，即得所证闭式。∎

**推论**：答案 $=\binom{n}{m}A(n,m)=\binom{n}{m}(n-1)\sum_{t=0}^{n-m}(-1)^{t}\binom{n-m}{t}(n-1-t)^{n-1}$。

**证明**：由 3.2 节的对称性论证，$\binom{n}{m}$ 个集合的「成功图数」相同。∎

## 6. 复杂度分析

- **时间**：预处理 $O(N)$（$N=\max n\le10^6$）；每组询问 $O\big((n-m)\log n\big)$，所有询问合计 $O\big(\sum n\cdot\log n\big)\approx 2\times10^7$ 次模乘；本机 C++ 实测最坏（$n=10^6,m=1$）约 $70$ ms，$\ge 25$ 倍余量。
- **空间**：$O(N)$，只有 `fact`、`invfact` 两个长度 $N+1$ 的数组；与 $256$ MB 相比可忽略。
- **说明**：Python 最坏情况约 $1.8$ s（CPython），接近 $2$ s 时限，建议用 PyPy 3 提交，或直接交 C++。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

static const long long MOD = 998244353;

long long mod_pow(long long b, long long e) {
    long long r = 1;
    b %= MOD;
    while (e > 0) {
        if (e & 1) r = r * b % MOD;
        b = b * b % MOD;
        e >>= 1;
    }
    return r;
}

int main() {
    int t;
    if (scanf("%d", &t) != 1) return 0;
    vector<int> ns(t), ms(t);
    int mx = 0;
    for (int i = 0; i < t; i++) {
        scanf("%d %d", &ns[i], &ms[i]);
        if (ns[i] > mx) mx = ns[i];
    }
    vector<long long> fact(mx + 1), invfact(mx + 1);
    fact[0] = 1;
    for (int i = 1; i <= mx; i++) fact[i] = fact[i - 1] * i % MOD;
    invfact[mx] = mod_pow(fact[mx], MOD - 2);
    for (int i = mx; i >= 1; i--) invfact[i - 1] = invfact[i] * i % MOD;

    string out;
    out.reserve((size_t)t * 12);
    for (int idx = 0; idx < t; idx++) {
        int n = ns[idx], m = ms[idx];
        int k = n - m;
        long long S = 0;
        for (int tt = 0; tt <= k; tt++) {
            long long comb = fact[k] * invfact[tt] % MOD * invfact[k - tt] % MOD;
            long long term = comb * mod_pow(n - 1 - tt, n - 1) % MOD;
            if (tt & 1) { S -= term; if (S < 0) S += MOD; }
            else { S += term; if (S >= MOD) S -= MOD; }
        }
        long long ways = fact[n] * invfact[m] % MOD * invfact[k] % MOD;
        long long ans = ways * (n - 1) % MOD * S % MOD;
        out += to_string(ans);
        out += '\n';
    }
    fputs(out.c_str(), stdout);
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
    MOD = 998244353
    t = int(data[0])
    ns = [0] * t
    ms = [0] * t
    pos = 1
    mx = 0
    for i in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        ns[i] = n; ms[i] = m
        if n > mx:
            mx = n

    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (mx + 1)
    invfact[mx] = pow(fact[mx], MOD - 2, MOD)
    for i in range(mx, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    out = []
    for idx in range(t):
        n = ns[idx]; m = ms[idx]; k = n - m
        fk = fact[k]
        S = 0
        base = n - 1
        e = n - 1
        for tt in range(k + 1):
            term = fk * invfact[tt] % MOD * invfact[k - tt] % MOD
            term = term * pow(base - tt, e, MOD) % MOD
            if tt & 1:
                S -= term
            else:
                S += term
        S %= MOD
        ways = fact[n] * invfact[m] % MOD * invfact[k] % MOD
        out.append(str(ways * base % MOD * S % MOD))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：不存在任何无自环图（$(n-1)^n=0$），答案必须是 $0$。公式里 $(n-1)=0$ 自动归零，不需要额外特判。
2. **$m=n$**：只有 $S$ 取全体才可能成功，答案应为 $(n-1)^n$；公式给出 $\binom{n}{n}(n-1)(n-1)^{n-1}=(n-1)^n$，可作自检。
3. **$m=1$**：答案应为 $n!\,(n-1)$（$n$ 个起点、$(n-1)!$ 条哈密顿路径、末尾 $n-1$ 种接法），公式同样吻合。
4. **末项底数为 $0$**：$t=k$ 时底数是 $m-1$，$m=1$ 时为 $0^{n-1}=0$；快速幂返回 $0$ 即可，别写成「底数为 $0$ 就跳过」。
5. **负余数**：交替求和必须用 `(S - term + MOD) % MOD` 或条件修正，Python 的 `%` 天然非负，但最后仍建议 `S %= MOD`。
6. **组合数下标写错**：是 $\binom{n-m}{t}$ 而不是 $\binom{n}{t}$；$n-m$ 可能远大于 $t$ 的上界，写错会直接错答案。
7. **多测预处理**：$t$ 可达 $10^4$，务必先读入取 $\max n$ 再统一预处理，不要每组重建 $10^6$ 的数组。
8. **Python 时限**：最坏 $10^6$ 次快速幂在 CPython 上约 $1.8$ s，接近 $2$ s；请用 PyPy 3 提交。

## 相关题目与扩展

- [Codeforces 2239A. Nim Game Is XOR Game](https://codeforces.com/problemset/problem/2239/A)：同场签到题，异或博弈。
- [Codeforces 2239B. Decidophobia](https://codeforces.com/problemset/problem/2239/B)：同场 Div.1 B，贪心 + 双指针。
- [Codeforces 1109D. Sasha and Interesting Fact from Graph Theory](https://codeforces.com/problemset/problem/1109/D)：Cayley 公式与带约束的树计数，同为组合计数套路。
- [Codeforces 702E. Analysis of Pathes in Functional Graph](https://codeforces.com/problemset/problem/702/E)：函数图上的倍增，熟悉函数图结构的好题。

**延伸思考**：本题的核心是「用容斥把纯环与叶子两类约束同时数掉」+「用拉格朗日反演把环结构消去」。若把条件改为「$S$ 中的点必须**恰好**是最小成功集」，就变成对覆盖结构做 Möbius 反演；若改为求所有 $m$ 的成功集总数之和（不分 $m$），可对式子作二项式反演得到更简洁的形式；若图的出边带权、要求最小权成功集，则需在基环树上做 DP，与本篇的「数结构」思路互补。
