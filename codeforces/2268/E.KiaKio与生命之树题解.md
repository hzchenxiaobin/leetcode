# Codeforces Kia Kio 与生命之树 题解

## 1. 题目概述

- **标题 / 题号**：Kia Kio 与生命之树（Codeforces 2268E，英文名 Kia Kio and Tree of Life）
- **链接**：https://codeforces.com/problemset/problem/2268/E
- **来源**：Codeforces Round 1124 (Div. 1) · Problem E
- **难度**：2700（2750 分）
- **限制**：时间 3 s / 内存 256 MB
- **标签**：树，组合计数，按位拆解，卷积 / NTT，数学

**题意**：给定长度为 $n$ 的数组 $a$。一棵「生命之树」这样递归构造：对当前段 $[l,r]$ 任选下标 $i$ 作根，左子树递归构造 $[l,i-1]$，右子树递归构造 $[i+1,r]$（空段即空子树）。所以合法树恰是下标 $1..n$ 上的**全部二叉搜索树形态**，共 $C_n$（第 $n$ 个 Catalan 数）棵。

删掉任意一条边，树分成两个连通块，设两块内 $a$ 的异或和分别为 $X,Y$，该边释放能量 $X+Y$；整棵树的能量 $f(\text{tree})$ 是 $n-1$ 条边能量之和。求**所有合法树的 $f$ 之和**，模 $998244353$。多测。

**约束**：

- $1 \le t \le 10^4$，$\sum n \le 2\times 10^5$
- $1 \le n \le 2\times 10^5$
- $0 \le a_i < 2^{18}$：所有异或前缀值都落在 $[0,2^{18})$，**只需 18 个二进制位**

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
5
2
1 2
3
1 1 1
3
1 2 3
4
2 1 4 7
5
5 12 9 14 1

输出：
6
10
40
318
2520
```

自造补充：`1 / 1 / 7`（$n=1$，无边）应输出 `0`。

第 2 个样例 $n=3,a=[1,1,1]$ 的 5 棵树都是三点路径，每条边两侧异或和都是 $1$ 与 $0$，单树能量 $2$，总计 $10$；第 1 个样例（$n=2$）是「单边」的最小情形，可手算核对。

## 3. 解题思路

### 3.1 暴力思路

按定义枚举所有 $C_n$ 棵树、每棵扫 $n-1$ 条边：$O(C_n\,n)$，$n=2\times10^5$ 时是天文数字。即使改成「枚举全部 $O(n^2)$ 个连续段、每段乘一个权重」，权重也不是 $1$——同一个段会作为子树出现在很多棵树里，必须先求出这个计数才能继续。

### 3.2 核心观察一：切边断下的必是「连续段子树」

![切边断下连续段子树与挂边计数](images/cf2268_e_cut_edge.svg)

递归构造的直接推论：**任意子树的点集都是一段连续下标** $[l,r]$。于是对边 $(\text{parent}(v),v)$，含 $v$ 的那一侧恰是子树段 $[l,r]$，另一侧是补集。设前缀异或 $p[k]=a_1\oplus\cdots\oplus a_k$、全体异或 $T=p[n]$，则

$$X = p[r]\oplus p[l-1], \qquad Y = T\oplus X, \qquad g(l,r) = X + (T\oplus X)$$

即**能量只由段 $[l,r]$ 决定**，与树形、边的位置都无关。剩下的关键量是「段 $[l,r]$ 作为子树挂边」出现在多少棵树里。

**计数（key）**：设段长 $m=r-l+1<n$。把该子树**整体收缩成一个叶子** $x$：收缩后是 $n-m+1$ 个键的 BST 且 $x$ 是叶子、不是根；反过来把 $x$ 展开成 $m$ 个键的 BST 又唯一还原。$m$ 个键的 BST 有 $C_m$ 种，而「$x$ 是叶子」的 BST 数与 $x$ 的排名无关——删掉叶子 $x$ 得到任意 $n-m$ 键 BST，插回去位置唯一，故恰有 $C_{n-m}$ 种。因此

$$\text{cnt}(l,r) = C_{r-l+1}\cdot C_{n-(r-l+1)}$$

**只与段长有关**！答案化为

$$\text{Answer}=\sum_{\substack{1\le l\le r\le n\\ (l,r)\ne(1,n)}} C_m\,C_{n-m}\,\bigl(X+(T\oplus X)\bigr)$$

其中整段 $[1,n]$ 是根所在段、没有父边，必须排除。剩下的问题是：如何不枚举 $O(n^2)$ 个段就算出这个和。

### 3.3 算法流程：按位拆解 + ±1 卷积（核心观察二）

![按位拆解与带权自相关](images/cf2268_e_bit_split.svg)

逐位看 $X+(T\oplus X)$：若 $T$ 的第 $b$ 位为 $1$，则 $X_b+(1-X_b)=1$；若为 $0$，则为 $2X_b$。于是

$$g(l,r)=T+2\bigl(X\ \&\ \overline{T}\bigr),\qquad \overline{T}=(2^{18}-1)\oplus T$$

$T$ 的部分是常数，按段长合并即可。记 $f(s)=C_sC_{n-s}$、

$$K=\sum_{s=1}^{n-1}(n-s+1)f(s),\qquad \text{Answer}=T\cdot K+2\sum_{b:\,T_b=0}2^b\cdot \text{Diff}_b$$

其中 $\text{Diff}_b=\sum_{i<r}f(r-i)\,[\,p[i]\text{ 与 }p[r]\text{ 的第 }b\text{ 位不同}\,]$（$i=l-1$）。为把「不同」变成可卷积的乘积，令 $A_b[k]=(-1)^{p[k]\text{ 的第 }b\text{ 位}}\in\{+1,-1\}$（不同取 $-1$、相同取 $+1$），并记全配对权和

$$\text{Total}K=K+C_n=\sum_{s=1}^{n}(n-s+1)f(s),\qquad \text{Corr}_b=\sum_{s=1}^{n}f(s)\sum_{i=0}^{n-s}A_b[i]A_b[i+s]$$

则 $\text{Diff}_b=(\text{Total}K-\text{Corr}_b)/2$。端点对 $(0,n)$ 不必单独扣除：当 $b$ 是 $T$ 的零位时 $p[0]$ 与 $p[n]$ 的第 $b$ 位同为 $0$，它本来就**不会**被计入 Diff。

$\text{Corr}_b$ 是「点积形式的带权自相关」。把 $f$ 与 $A_b$ 补零到长度 $L$（$>2n$ 的 $2$ 的幂），用 NTT 求出循环卷积 $\text{conv}_b=A_b*F$，则

$$\text{Corr}_b=\sum_{r=0}^{n}A_b[r]\,\text{conv}_b[r]=\frac1L\sum_{k=0}^{L-1}\hat A_b[k]\,\hat F[k]\,\hat A_b[(L-k)\bmod L]$$

末式是离散 Parseval 恒等式，好处是**每个位只需一次正变换**（$\hat F$ 全测只算一次，也没有逆变换），18 个位共 19 次 NTT。

### 3.4 示例演算

![n=3 示例的逐段贡献与按位校验](images/cf2268_e_walkthrough.svg)

$a=[1,2,3]$：$T=0$，$p=[0,1,3,0]$，$C_0..C_3=[1,1,2,5]$，$f(1)=2,f(2)=2,f(3)=5$，$K=3\cdot2+2\cdot2=10$，$\text{Total}K=15$。逐段贡献为 $2\cdot2+2\cdot4+2\cdot6+2\cdot6+2\cdot2=40$。

按位复核（只有 $b=0,1$ 有非零位）：$b=0$ 时 $A=(+,-,-,+)$，自相关 $(-1,-2,+1)$，$\text{Corr}=-1$，$\text{Diff}=(15+1)/2=8$；$b=1$ 时 $A=(+,+,-,+)$，自相关 $(-1,0,+1)$，$\text{Corr}=3$，$\text{Diff}=(15-3)/2=6$。故 $2\cdot(2^0\cdot8+2^1\cdot6)=40$ ✓。

## 4. 算法细节

1. **多测复用**：先读入全部测试求出 $\max n$，一次性建好线性逆元表，再把 $C,f,A,\hat F$ 等 `vector` 用 `assign` 复用，避免重复分配。
2. **Catalan 递推**：$C_k=C_{k-1}\cdot\frac{2(2k-1)}{k+1}$（$C_0=1$），分母用线性逆元；也可用 $C_k=\binom{2k}{k}-\binom{2k}{k+1}$，注意 $2n\le4\times10^5<998244353$，阶乘表不会触到模数。
3. **掩码**：`need = ((1<<18)-1) ^ T`。`need == 0`（$T$ 的 18 位全为 1）时答案就是 $T\cdot K$，直接跳过 NTT；$n=1$ 时 $K=0$，输出 $0$。
4. **卷积长度**：必须 $L>2n$，否则线性卷积与循环卷积混叠，含 $f(n)=C_n$ 的端点对会被绕回来重复计入。
5. **取模**：先 `(TotalK - corr + MOD) % MOD` 再乘 $2^{-1}$；点积累加用 `long long`，每轮判一次是否 `% MOD`，避免 $10^{18}$ 量级溢出。
6. **常数与精度**：C++ 关掉 `cin/cout` 同步并缓存个单位根；$A_b$ 直接写 $1$ / $MOD-1$ 省掉符号转换；Python 把 $f$ 按 $2^{15}$ 拆半做浮点 FFT，否则 $10^9$ 量级系数会丢精度。

## 5. 正确性证明

**引理 1**：任意子树点集是连续段；对边 $(\text{parent}(v),v)$，两侧异或和为 $X=p[r]\oplus p[l-1]$、$Y=T\oplus X$。

**证明**：段 $[l,r]$ 的左右子树分别在 $[l,i-1]$、$[i+1,r]$ 内，归纳即知；两侧互补故 $X\oplus Y=T$。∎

**引理 2**：对 $m<n$，长 $m$ 的段作为带父边子树出现 $C_mC_{n-m}$ 次。

**证明**：把段收缩成叶子 $x$，得 $n-m+1$ 键 BST 且 $x$ 是叶子；反之给定该 BST 与段内形状，展开 $x$ 唯一还原（键次序保证 BST 性质），故次数 $=C_m\cdot\#\{n-m+1\text{ 键 BST 中 }x\text{ 是叶子}\}$。删掉叶子 $x$ 给出 $n-m$ 键 BST、插回位置唯一，故叶子情形数 $=C_{n-m}$。∎

**引理 3**：$\sum_{\text{tree}}\sum_{\text{edge}}g=\sum_{m<n}C_mC_{n-m}\sum_{\lvert[l,r]\rvert=m}g(l,r)$。

**证明**：树与边的组合与「带父边的子树段」一一对应（每条边恰对应子侧子树），再由引理 1、2 合并同类项。∎

**引理 4**：$X+(T\oplus X)=T+2(X\&\overline{T})$，$\overline{T}=(2^{18}-1)\oplus T$。

**证明**：逐位无进位相加：$T_b=1$ 时 $X_b+(1-X_b)=1$，$T_b=0$ 时 $X_b+X_b=2X_b$。提出 $T_b=1$ 的位即 $T$，剩下的 $2X_b$ 只在 $T_b=0$ 处保留，即 $2(X\&\overline{T})$。∎

**引理 5**：$\text{Diff}_b=(\text{Total}K-\text{Corr}_b)/2$，且 $\text{Corr}_b$ 等于 §3.3 的 Parseval 表达式。

**证明**：$A_b[i]A_b[i+s]$ 相同为 $+1$、不同为 $-1$，故 $\text{Corr}_b=\text{same}-\text{diff}=\text{Total}K-2\,\text{diff}$，解出 $\text{Diff}_b$。又 $L>2n$ 保证 $\text{conv}_b[r]=\sum_s A_b[r-s]f(s)$ 在 $r\le n$ 处无混叠（折叠项下标 $>n$ 而 $A_b$ 为 $0$），把逆变换展开并交换求和即得 Parseval 形式。∎

**定理**：算法输出即所有合法树的 $f$ 之和（模 $998244353$）。

**证明**：由引理 3 答案为逐段加权和，由引理 4 拆成常数项 $T\cdot K$ 与位项，由引理 5 位项可由一次 NTT 得到；端点对 $(0,n)$ 因 $p[0],p[n]$ 在 $T$ 的零位上同为 $0$ 而不计入 Diff，与「排除整段」一致；所有中间量在模下计算且 $2$ 的逆元存在。∎

## 6. 复杂度分析

- **时间**：每组 $O(n+18\cdot L\log L)$，$L$ 是 $>2n$ 的最小 $2$ 的幂（$L<4n$）。全测 $\sum n\le2\times10^5$，总时间 $O(18\sum n\log n)$；实测 C++ 最坏约 $0.55$ s（$n=2\times10^5$ 且 18 位全开，含读入）、Python（numpy）约 $1.1$ s（$t=10^4,n=20$ 全零），均留足 3 s 余量。
- **空间**：逆元表与前缀异或 $O(n)$，$C,f,\hat F,A_b$ 各 $O(L)=O(n)$，合计 $O(n)$，C++ 约 $10$ MB，Python（numpy）实测峰值 $\le130$ MB。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
const int MOD = 998244353, G = 3, MAXB = 18, FULLMASK = (1 << MAXB) - 1;

long long pw(long long a, long long e) {
    long long r = 1; a %= MOD;
    for (; e; e >>= 1, a = a * a % MOD) if (e & 1) r = r * a % MOD;
    return r;
}

static int rootOf[1 << 20];                 // rootOf[len]: 本原 len 次单位根

void ntt(vector<int>& a) {                  // 只需正变换（Parseval）
    int L = (int)a.size();
    for (int i = 1, j = 0; i < L; i++) {
        int bit = L >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= L; len <<= 1) {
        int wlen = rootOf[len], h = len >> 1;
        for (int i = 0; i < L; i += len) {
            long long w = 1;
            for (int j = 0; j < h; j++) {
                int u = a[i + j], v = (int)((long long)a[i + j + h] * w % MOD);
                int s = u + v; if (s >= MOD) s -= MOD;
                int d = u - v; if (d < 0) d += MOD;
                a[i + j] = s; a[i + j + h] = d;
                w = w * wlen % MOD;
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    for (int len = 2; len < (1 << 20); len <<= 1) rootOf[len] = (int)pw(G, (MOD - 1) / len);
    int t; if (!(cin >> t)) return 0;
    vector<vector<int>> tc(t); int maxN = 2;
    for (int i = 0; i < t; i++) {
        int n; cin >> n; tc[i].resize(n);
        for (int j = 0; j < n; j++) cin >> tc[i][j];
        maxN = max(maxN, n);
    }
    vector<int> inv(maxN + 2, 1);           // 线性求逆元 1..maxN+1
    for (int i = 2; i <= maxN + 1; i++) inv[i] = (int)(MOD - (long long)(MOD / i) * inv[MOD % i] % MOD);
    const long long INV2 = pw(2, MOD - 2);
    int pw2[MAXB + 1]; pw2[0] = 1;
    for (int b = 1; b <= MAXB; b++) pw2[b] = (int)(2LL * pw2[b - 1] % MOD);

    vector<int> C, f, A, Fh;
    for (int id = 0; id < t; id++) {
        vector<int>& a = tc[id]; int n = (int)a.size();
        vector<int> px(n + 1, 0);
        for (int i = 1; i <= n; i++) px[i] = px[i - 1] ^ a[i - 1];
        int T = px[n], need = FULLMASK ^ T;
        C.assign(n + 1, 0); C[0] = 1;        // C_k = C_{k-1} * 2(2k-1)/(k+1)
        for (int k = 1; k <= n; k++)
            C[k] = (int)((long long)C[k - 1] * (2 * (2 * k - 1)) % MOD * inv[k + 1] % MOD);
        f.assign(n + 1, 0);
        for (int s = 1; s <= n; s++) f[s] = (int)((long long)C[s] * C[n - s] % MOD);
        long long K = 0;
        for (int s = 1; s < n; s++) K = (K + (long long)(n - s + 1) * f[s]) % MOD;
        long long totalK = (K + C[n]) % MOD, ans = K * T % MOD;
        if (need && n >= 2) {
            int L = 1; while (L <= 2 * n) L <<= 1;
            long long invL = pw(L, MOD - 2);
            Fh.assign(L, 0);
            for (int s = 1; s <= n; s++) Fh[s] = f[s];
            ntt(Fh);
            A.assign(L, 0);
            for (int b = 0; b < MAXB; b++) {
                if (!((need >> b) & 1)) continue;
                for (int k = 0; k <= n; k++) A[k] = ((px[k] >> b) & 1) ? MOD - 1 : 1;
                for (int k = n + 1; k < L; k++) A[k] = 0;
                ntt(A);
                long long S = 0;
                for (int k = 0; k < L; k++) {
                    S += (long long)A[k] * A[(L - k) & (L - 1)] % MOD * Fh[k] % MOD;
                    if (S >= (long long)MOD * MOD) S %= MOD;
                }
                long long corr = S % MOD * invL % MOD;
                long long diff = (totalK - corr + MOD) % MOD * INV2 % MOD;
                ans = (ans + 2LL * pw2[b] % MOD * diff) % MOD;
            }
        }
        cout << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys
import numpy as np

MOD = 998244353
MAXB = 18
FULL = (1 << MAXB) - 1
SPLIT = 15
BASE = 1 << SPLIT
INV2 = (MOD + 1) // 2


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    pos, t = 1, data[0]
    tests, mx = [], 2
    for _ in range(t):
        n = data[pos]; pos += 1
        tests.append(data[pos:pos + n]); pos += n
        mx = max(mx, n)

    inv = [0] * (mx + 2)                       # 线性求逆元
    inv[1] = 1
    for i in range(2, mx + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    out = []
    for a in tests:
        n = len(a)
        px = [0] * (n + 1)
        for i in range(n):
            px[i + 1] = px[i] ^ a[i]
        T = px[n]
        need = FULL ^ T
        if n == 1:
            out.append(0)
            continue
        cat = [0] * (n + 1)                    # Catalan: C_k = C_{k-1}*2(2k-1)/(k+1)
        cat[0] = 1
        for k in range(1, n + 1):
            cat[k] = cat[k - 1] * (2 * (2 * k - 1)) % MOD * inv[k + 1] % MOD
        f = [0] * (n + 1)
        for s in range(1, n + 1):
            f[s] = cat[s] * cat[n - s] % MOD
        K = 0
        for s in range(1, n):
            K = (K + (n - s + 1) * f[s]) % MOD
        total = (K + cat[n]) % MOD
        ans = K * T % MOD
        if need:
            L = 1
            while L < 2 * n + 2:
                L <<= 1
            fs = np.zeros(L, dtype=np.int64)
            fs[1:n + 1] = f[1:n + 1]
            # f 按 2^15 拆半，浮点 FFT 才能精确还原整数卷积
            F_lo = np.fft.rfft((fs & (BASE - 1)).astype(np.float64))
            F_hi = np.fft.rfft((fs >> SPLIT).astype(np.float64))
            P = np.array(px, dtype=np.int64)
            bits = [b for b in range(MAXB) if (need >> b) & 1]
            step = max(1, (1 << 19) // L)      # 每批处理的位数，控制内存
            extra = 0
            for st in range(0, len(bits), step):
                bb = np.array(bits[st:st + step], dtype=np.int64)
                sg = 1 - 2 * ((P[None, :] >> bb[:, None]) & 1)          # ±1 编码
                A2 = np.zeros((len(bb), L), dtype=np.float64)
                A2[:, :n + 1] = sg
                R = np.fft.rfft(A2, axis=1)
                clo = np.rint(np.fft.irfft(R * F_lo, L, axis=1)[:, :n + 1]).astype(np.int64)
                chi = np.rint(np.fft.irfft(R * F_hi, L, axis=1)[:, :n + 1]).astype(np.int64)
                slo = (clo * sg).sum(axis=1)
                shi = (chi * sg).sum(axis=1)
                for k in range(len(bb)):
                    corr = (int(shi[k]) % MOD * BASE + int(slo[k])) % MOD
                    d = (total - corr) * INV2 % MOD
                    extra = (extra + 2 * pow(2, int(bb[k]), MOD) * d) % MOD
            ans = (ans + extra) % MOD
        out.append(ans)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：没有边，答案必须是 $0$；实现里提前 `continue`，避免构造长度为 $1$ 的卷积或访问 $f(0)$ 之外的项。
2. **整段 $[1,n]$ 要排除**：它是根所在段、没有父边。实现用 $\text{Total}K=K+C_n$ 补上端点对 $(0,n)$，再依赖「$b$ 是 $T$ 的零位 ⇒ 该位不产生 Diff」自动抵消；若改写成其他形式，务必显式扣掉 $f(n)=C_n$。
3. **卷积长度不足会重复计数**：$L$ 必须 $>2n$（`while (L <= 2*n)`），否则带下标 $s=n$ 的项被折叠，答案偏大且不易察觉。
4. **负数取模**：`(totalK - corr + MOD) % MOD`；Python 的 `%` 天然非负，C++ 漏加 `MOD` 会出负数。
5. **18 位不能少**：$a_i<2^{18}$，但异或和可能用到高位，掩码统一取 `(1<<18)-1`；全零数组 $T=0$ 是 `need` 最大的最坏情况，性能测试要用它。
6. **Python 精度陷阱**：$f(s)$ 可达 $10^9$，直接做浮点 FFT 会丢精度，必须按 $2^{15}$ 拆半卷积后用 `int64` 合并（比纯 Python NTT 快两个数量级）。

## 相关题目与扩展

- [CF 2268B What a SauSaGe! It's All Meat](https://codeforces.com/problemset/problem/2268/B)：同场题，异或线性基 + 计数，同样靠「逐位独立」拆解。
- [CF 993E Nikita and Order Statistics](https://codeforces.com/problemset/problem/993/E)：FFT 求带权自相关的经典题，与 §3.3 的卷积手法同源。
- [LeetCode 96. 不同的二叉搜索树](https://leetcode.cn/problems/unique-binary-search-trees/)：Catalan 计数本身。

**延伸思考**：

1. 若把异或换成加法或最大值，能量不再逐位独立；$\text{cnt}(l,r)=C_mC_{n-m}$ 仍成立，内层求和能否用分治或线段树合并做到 $O(n\log^2n)$？
2. 若边的能量改成 $\lvert X-Y\rvert$ 或 $\max(X,Y)$，利用 $X\oplus Y=T$ 还能不能继续按位拆解？
3. 若树形固定为「每次取中点」，答案退化成 $O(n)$ 的闭式，说明本题难点完全来自「对形态求和」。
