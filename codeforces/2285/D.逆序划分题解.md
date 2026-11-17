# Codeforces 逆序划分 题解

## 1. 题目概述

- **标题 / 题号**：逆序划分（Codeforces 2285D，英文名 Reverse Partition）
- **链接**：https://codeforces.com/problemset/problem/2285/D
- **来源**：Codeforces Round 1135 (Div. 2) · Problem D
- **难度**：未评级（2000 分）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：二分查找，组合数学，数据结构

**题意**：给定 $n,m$ 和长度为 $n$ 的数组 $a$。一个**划分** $p$ 是 $m$ 个正整数且 $\sum_j p_j=n$；把数组 $b$ 按 $p$ 依次切成 $m$ 段、每段求和，得到长度 $m$ 的数组 $f(b,p)$。记 $a^{R}$ 是 $a$ 的反转，若 $f(a,p)=f(a^{R},p)$ 则称 $p$ 是 $a$ 的**特殊划分**。接着有 $q$ 次**互相独立**的查询，每次给 $(i,v)$，令 $a_i:=a_i+v$ 后输出此时的特殊划分数，对 $10^9+7$ 取模；每条查询都从**原始** $a$ 出发（不累加）。

**约束**：

- $1\le t\le 10^4$，$1\le m\le n\le 2\cdot10^5$，$1\le q\le 2\cdot10^5$
- $|a_i|\le 10^9$，$|v|\le 10^9$
- $\sum n\le 2\cdot10^5$ 且 $\sum q\le 2\cdot10^5$（决定单次查询必须近似 $O(\log n)$）

## 2. 示例

```text
输入
2
5 2 3
1 2 3 2 1
3 0
2 1
5 -1
8 3 6
3 1 4 5 1 7 2 3
1 0
4 2
8 -2
2 1
5 -1
7 3

输出
4
2
0
3
1
0
6
1
1
```

第一组的 $a=[1,2,3,2,1]$、$m=2$：合法切点是 $k=1,2,3,4$（后文会看到 $D_k$ 全为 $0$），从 $4$ 个位置里选 $m-1=1$ 个，故答案为 $4$；第二条查询把 $a_2$ 加 $1$ 后只剩 $k=1,4$ 合法，答案为 $\binom21=2$；第三条把 $a_5$ 减 $1$ 后无合法切点，答案为 $0$。

## 3. 解题思路

### 3.1 暴力思路

划分 $p$ 与切点序列 $0=P_0<P_1<\dots<P_{m-1}<P_m=n$ 一一对应，总数 $\binom{n-1}{m-1}$，最坏是 $\binom{2\cdot10^5-1}{10^5-1}$ 级别。对每个划分还要比较两个长度 $m$ 的数组，再乘上 $q$ 条查询——即使只做一次都不可行，必须找到「划分之间共享的结构」。

### 3.2 核心观察：合法切点 = 前缀和等于同长后缀和

![前缀和与后缀和相等处即合法切点](images/cf2285_d_prefix_suffix.svg)

记 $S_k=\sum_{j\le k}a_j$，$S^*_k=\sum_{j=1}^{k}a_{n+1-j}$（后 $k$ 项和，也就是 $a^{R}$ 的前缀和），$S_0=S^*_0=0$，总和 $T=S_n=S^*_n$。

用切点写开两边的第 $j$ 段：

$$f(a,p)_j=S_{P_j}-S_{P_{j-1}},\qquad f(a^{R},p)_j=S^*_{P_j}-S^*_{P_{j-1}}$$

于是两个数组相等等价于「每一段上 $S$ 与 $S^*$ 的增量都相同」，即对 $j=1..m$ 有 $D_{P_j}=D_{P_{j-1}}$，其中

$$D_k:=S_k-S^*_k .$$

由 $D_{P_0}=D_0=0$ 归纳得 $D_{P_j}=0$ 对一切 $j$ 成立；反过来若每个切点都满足 $D_{P_j}=0$，增量自然全为 $0$。又 $D_n=S_n-S^*_n=0$ **恒成立**，所以真正的约束只落在 $P_1,\dots,P_{m-1}$ 上：

$$p\ \text{是特殊划分}\iff D_{P_1}=D_{P_2}=\dots=D_{P_{m-1}}=0 .$$

再看 $D$ 的闭式。因为 $S^*_k=T-S_{n-k}$，

$$D_k=S_k+S_{n-k}-T,\qquad D_{n-k}=D_k,\qquad D_0=D_n=0 .$$

> 💡 令 $g=\#\{k\in[1,n-1]:D_k=0\}$，把 $m-1$ 个切点任意放进这 $g$ 个位置即可（顺序被下标唯一确定），故**答案就是 $\binom{g}{m-1}$**。剩下的事只有一件：$q$ 次修改后 $g$ 变成多少。

### 3.3 算法流程：一次查询只平移一段 D

![一次修改只平移一段 D](images/cf2285_d_query_shift.svg)

令 $b_k=a_k-a_{n+1-k}$，则 $b_{n+1-k}=-b_k$，且

$$D_k=b_1+b_2+\dots+b_k .$$

修改 $a_i\mathrel{+}=v$ 会让 $b_i$ 增加 $v$、$b_{n+1-i}$ 减少 $v$。若 $i=n+1-i$（正中间那个元素），两处是同一位置，$b$ 不动，$D$ 一个都不变。

否则取 $\mathrm{lo}=\min(i,n+1-i)$、$\mathrm{hi}=\max(i,n+1-i)$、$\sigma=+1$（当 $i=\mathrm{lo}$）或 $\sigma=-1$（当 $i=\mathrm{hi}$），则对前缀和数组 $D$ 有

$$D_k\leftarrow D_k+\sigma v\ \ (k\in[\mathrm{lo},\mathrm{hi}-1]);\qquad D_k\ \text{不变}\ \ (k\notin[\mathrm{lo},\mathrm{hi}-1]).$$

**一次查询只是把一段连续区间的 $D$ 整体平移，区间之外纹丝不动。** 因此

$$g'=Z-\#\{k\in I:D_k=0\}+\#\{k\in I:D_k=-\sigma v\},\qquad I=[\mathrm{lo},\mathrm{hi}-1],$$

其中 $Z=g$ 是原始数组的合法切点数。两个计数都是「在某个值的下标升序表上二分」，单次 $O(\log n)$，于是每条查询只需两次二分加一次查值。

### 3.4 示例演算

![样例 1 走查](images/cf2285_d_walkthrough.svg)

对 $a=[1,2,3,2,1]$（$n=5$）：$S=[1,3,6,8,9]$，$S^*=[1,3,6,8,9]$，故 $D_1=D_2=D_3=D_4=0$，$g=4$，$m=2$ 时答案 $\binom41=4$。

- 查询 $(3,0)$：$v=0$，$D$ 不动，$g'=4$，答案 $4$。
- 查询 $(2,+1)$：$i'=4$，$I=[2,3]$，整段 $+1$，区间内原本为 $0$ 的 $2$ 个位置全变坏、原本为 $-1$ 的没有，$g'=4-2+0=2$，答案 $2$。
- 查询 $(5,-1)$：$i'=1$，此时 $i=\mathrm{hi}$、$\sigma=-1$，位移是 $\sigma v=+1$；$I=[1,4]$ 内 $4$ 个位置从 $0$ 变成 $1$ 全变坏，$g'=0$，答案 $0$。

正好对上样例输出的前三个数 $4,2,0$。

## 4. 算法细节

1. **预处理**：一趟前缀和得到 $S$；把 $(D_k,k)$ 打包排序，再按键分组，得到「值 → 下标升序表」。排序 $O(n\log n)$ 顺带保证组内下标递增，不需要额外排序。
2. **查值编号**：去重后的值数组用 `lower_bound` 二分定位；查不到返回 $-1$，表示该值在区间内出现 $0$ 次（从而避免对空表二分）。
3. **区间计数**：`upper_bound(P, hi-1) - lower_bound(P, lo)`，右端是 `hi-1` 而不是 `hi`；这也是本题「二分」标签的落点。
4. **组合数**：$\binom{g}{m-1}$ 用阶乘 + 逆阶乘，预处理到 $2\cdot10^5$；函数内部对 $k<0$ 或 $k>n$ 直接返回 $0$，$m-1>g$ 就靠这一条兜住，不会越界。
5. **溢出**：$|a_i|\le10^9$、$n\le2\cdot10^5$，$S_k$ 可达 $2\cdot10^{14}$，$D_k$ 在 $\pm4\cdot10^{14}$ 内，必须 `long long`；注意我们**从不真的修改 $D$**，只查 $-v$，所以也不会累积漂移。
6. **多测**：全局只保留阶乘表；`pref / val / pos` 每组重建，绝不能沿用上一组的编号表。
7. **I/O**：$\sum n,\sum q\le2\cdot10^5$，`ios::sync_with_stdio(false)` 加 `cin.tie(nullptr)` 足够，换行统一用 `'\n'`。
8. **$v=0$ 的合并**：$-\delta=0$，两个计数相同，$g'=Z$，代码把 $\delta=0$ 单列一支，省掉一次无效查表。

## 5. 正确性证明

**引理 1（划分与切点一一对应）**：$m$ 元正整数划分 $p$ 与满足 $1\le P_1<P_2<\dots<P_{m-1}\le n-1$ 的切点序列一一对应。

**证明**：由 $p$ 取部分和 $P_j=p_1+\dots+p_j$，因 $p_j\ge1$ 故严格递增，且 $P_m=n$、$P_j\le n-1\ (j<m)$。反之给定切点令 $p_j=P_j-P_{j-1}>0$，两者互逆。∎

**引理 2（$D$ 的闭式与对称性）**：对 $0\le k\le n$ 有 $D_k=S_k+S_{n-k}-T$，且 $D_{n-k}=D_k$、$D_0=D_n=0$。

**证明**：$S^*_k=\sum_{j=1}^{k}a_{n+1-j}=T-S_{n-k}$，代入 $D_k=S_k-S^*_k$ 即得闭式；把 $k$ 换成 $n-k$ 时右端仍是 $S_{n-k}+S_k-T$，故对称；$D_0=S_0+S_n-T=0$，$D_n=S_n+S_0-T=0$。∎

**引理 3（切点合法性）**：$p$ 是特殊划分 $\iff$ 对每个 $j\in[1,m-1]$ 有 $D_{P_j}=0$。

**证明**：由 §3.2，$f(a,p)=f(a^{R},p)\iff D_{P_j}=D_{P_{j-1}}\ (j=1..m)$。若成立，由 $D_{P_0}=D_0=0$ 归纳即得所有 $D_{P_j}=0$。反之若 $D_{P_j}=0$ 对 $j=0..m$ 成立（$j=0,m$ 自动成立），则相邻差必为 $0$，条件成立。∎

**引理 4（修改只平移一段）**：修改 $a_i\mathrel{+}=v$ 后 $D'_k=D_k+\Delta_k$，其中 $\Delta_k=\sigma v$ 当 $k\in[\mathrm{lo},\mathrm{hi}-1]$、否则 $\Delta_k=0$；若 $i=n+1-i$（即 $\mathrm{lo}=\mathrm{hi}$），该区间为空，$D$ 完全不变。

**证明**：$a_i$ 对 $S_k$ 有贡献当且仅当 $i\le k$，对 $S_{n-k}$ 有贡献当且仅当 $i\le n-k$，对 $T$ 恒有贡献，故
$$\Delta_k=v\bigl([i\le k]+[i\le n-k]-1\bigr).$$
设 $i\le n+1-i$，即 $i=\mathrm{lo}$、$\mathrm{hi}=n+1-i$。此时 $[i\le k]=[k\ge\mathrm{lo}]$，$[i\le n-k]=[k\le n-i]=[k\le\mathrm{hi}-1]$。两指示函数同时为 $1$ 当且仅当 $k\in[\mathrm{lo},\mathrm{hi}-1]$，此时 $\Delta_k=+v$；只有恰好一个为 $1$（即 $k<\mathrm{lo}$ 或 $k\ge\mathrm{hi}$）时 $\Delta_k=0$。$i>n+1-i$ 时同理，只是两指示函数的角色互换，得 $\Delta_k=-v$ 于 $[\mathrm{lo},\mathrm{hi}-1]$、其余为 $0$。∎

**定理**：对每条查询，算法输出的 $\binom{g'}{m-1}$ 恰为修改后数组的特殊划分数。

**证明**：由引理 1、3，特殊划分数等于「在 $\{k\in[1,n-1]:D_k=0\}$ 中选 $m-1$ 个」的方案数，即 $\binom{g'}{m-1}$。由引理 4，$D$ 只在 $I$ 上整体加 $\sigma v$：$I$ 内原本为 $0$ 的位置全部变坏（$-\#$ 项），原本为 $-\sigma v$ 的位置恰好变成 $0$（$+\#$ 项），$I$ 外完全不变，故算法的 $g'=Z-\#\{D_k=0\}+\#\{D_k=-\sigma v\}$ 正是修改后的合法切点数。组合数在 $m-1>g'$ 时返回 $0$，与「选不出 $m-1$ 个切点」一致。∎

## 6. 复杂度分析

- **时间**：每组 $O(n)$ 求前缀和，$O(n\log n)$ 排序分组；每条查询 $O(\log n)$（一次查值 + 至多两次区间二分），共 $O(q\log n)$。总计 $O\bigl((\sum n+\sum q)\log n\bigr)$，按 $\sum n+\sum q\le4\cdot10^5$ 估算不超过 $7\times10^6$ 次基本操作。
- **空间**：$O(n)$ 的 $S$、`val`、`pos`（下标表总长恰为 $n-1$），加全局阶乘表 $2\times2\cdot10^5$ 个 `int`（约 $1.6$ MB），总计约 $10$ MB，远低于 $256$ MB。
- **可行性**：本机（Apple clang + libc++）三个最大数据实测最慢 $0.80$ s，其中 $4\times10^5$ 个整数的 `cin` 解析约占 $0.75$ s；同一逻辑改用 `scanf/printf` 只需 $0.09$ s。对 $2$ s 限时余量约 $2.5$ 倍（换成 GNU libstdc++ 时更快）。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

const int MOD = 1000000007;
const int MAXN = 200005;              // sum(n) <= 2e5

int fact_[MAXN], inv_fact_[MAXN];

ll power(ll b, ll e, ll m) {
    ll r = 1 % m;
    b %= m;
    while (e > 0) {
        if (e & 1) r = r * b % m;
        b = b * b % m;
        e >>= 1;
    }
    return r;
}

int comb(int n, int k) {              // C(n, k) mod 1e9+7
    if (k < 0 || k > n) return 0;
    return (ll)fact_[n] * inv_fact_[k] % MOD * inv_fact_[n - k] % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    fact_[0] = 1;
    for (int i = 1; i < MAXN; i++) fact_[i] = (ll)fact_[i - 1] * i % MOD;
    inv_fact_[MAXN - 1] = (int)power(fact_[MAXN - 1], MOD - 2, MOD);
    for (int i = MAXN - 1; i > 0; i--) inv_fact_[i - 1] = (ll)inv_fact_[i] * i % MOD;

    int t;
    cin >> t;
    while (t--) {
        int n, m, q;
        cin >> n >> m >> q;
        vector<ll> pref(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            ll x;
            cin >> x;
            pref[i] = pref[i - 1] + x;
        }
        ll tot = pref[n];

        // D[k] = 前缀长 k 之和 - 后缀长 k 之和 = pref[k] + pref[n-k] - tot
        vector<pair<ll, int>> vp(n - 1);
        for (int k = 1; k <= n - 1; k++)
            vp[k - 1] = make_pair(pref[k] + pref[n - k] - tot, k);
        sort(vp.begin(), vp.end());
        vector<ll> val;                      // 去重后的 D 值
        vector<vector<int>> pos;             // 每个值对应的 k 升序表
        for (int i = 0; i < n - 1; i++) {
            if (val.empty() || val.back() != vp[i].first) {
                val.push_back(vp[i].first);
                pos.push_back(vector<int>());
            }
            pos.back().push_back(vp[i].second);
        }
        auto idOf = [&](ll x) -> int {       // 值 -> 编号（二分），不存在返回 -1
            auto it = lower_bound(val.begin(), val.end(), x);
            return (it != val.end() && *it == x) ? (int)(it - val.begin()) : -1;
        };
        int id0 = idOf(0);
        int ztotal = (id0 < 0 ? 0 : (int)pos[id0].size());   // 全体 0 的个数
        int K = m - 1;

        for (int qi = 0; qi < q; qi++) {
            int i; ll v;
            cin >> i >> v;
            int i2 = n + 1 - i;              // 镜像位置
            int g;
            if (i == i2) {                   // 正中间元素：整条 D 不变
                cout << comb(ztotal, K) << '\n';
                continue;
            }
            int lo = min(i, i2), hi = max(i, i2);
            ll delta = (i < i2) ? v : -v;    // D[k] 在 [lo, hi-1] 上整体 += delta
            auto cntIn = [&](int id) -> int {         // 区间内取该值的 k 的个数
                if (id < 0) return 0;
                const vector<int>& P = pos[id];
                return (int)(upper_bound(P.begin(), P.end(), hi - 1) - P.begin())
                     - (int)(lower_bound(P.begin(), P.end(), lo) - P.begin());
            };
            int bad = cntIn(id0);                       // 原本为 0 -> 变坏
            int good = (delta == 0) ? bad : cntIn(idOf(-delta));   // 原本为 -delta -> 变好
            g = ztotal - bad + good;
            cout << comb(g, K) << '\n';
        }
    }
    return 0;
}
```

### Python3

```python
import sys
from bisect import bisect_left, bisect_right

MOD = 10**9 + 7
MAXN = 200005                      # sum(n) <= 2e5

fact = [1] * MAXN
for i in range(1, MAXN):
    fact[i] = fact[i - 1] * i % MOD
inv_fact = [1] * MAXN
inv_fact[MAXN - 1] = pow(fact[MAXN - 1], MOD - 2, MOD)
for i in range(MAXN - 1, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD


def comb(n, k):
    if k < 0 or k > n:
        return 0
    return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n, m, q = int(data[p]), int(data[p + 1]), int(data[p + 2]); p += 3
        pref = [0] * (n + 1)
        for i in range(1, n + 1):
            pref[i] = pref[i - 1] + int(data[p]); p += 1
        tot = pref[n]
        groups = {}                               # D 值 -> k 的升序表
        for k in range(1, n):
            groups.setdefault(pref[k] + pref[n - k] - tot, []).append(k)
        Z = len(groups.get(0, ()))
        K = m - 1
        for _ in range(q):
            i, v = int(data[p]), int(data[p + 1]); p += 2
            i2 = n + 1 - i
            if i == i2:                           # 正中间元素：D 不变
                g = Z
            else:
                lo, hi = (i, i2) if i < i2 else (i2, i)
                d = v if i < i2 else -v
                P = groups.get(0, ())
                bad = bisect_right(P, hi - 1) - bisect_left(P, lo)
                if d == 0:                        # v = 0：两个计数相等
                    g = Z
                else:
                    Q = groups.get(-d, ())
                    g = Z - bad + bisect_right(Q, hi - 1) - bisect_left(Q, lo)
            out.append(str(comb(g, K)))
    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：没有候选切点，$g=0$；又因 $m\le n$ 必有 $m=1$，输出 $\binom00=1$。划分 $[1]$ 显然特殊，别写成 $0$。
2. **右端点取 $[\mathrm{lo},\mathrm{hi}-1]$**：若错取成 $[\mathrm{lo},\mathrm{hi}]$，会把 $k=n$（$D_n$ 恒为 $0$）当成候选切点，答案整体偏大。
3. **$m=1$**：任意数组都只有 $p=[n]$ 一个划分且必然特殊，答案恒为 $1$；此时 $K=0$，$\binom{g}{0}=1$，不要因为 $g=0$ 提前返回 $0$。
4. **$m-1>g$**：答案必须是 $0$，靠 `comb` 里的 `k > n` 判据拦下；若不判就会越界读阶乘表或算出非零。
5. **正中间元素**：$i=(n+1)/2$ 时 $b_i$ 同时 $+v$ 和 $-v$，$D$ 完全不变；若按 $\mathrm{lo}=\mathrm{hi}$ 走通用分支，区间 $[\mathrm{lo},\mathrm{lo}-1]$ 为空，也能得到同样结果，但要确保二分不会用非法下标。
6. **负数**：$D_k$ 与 $-v$ 都可能为负，哈希 `map`/排序二分都必须用带符号的 64 位；计数过程**不能取模**，只有最后的组合数取模。
7. **全 0 数组或 $v=0$**：某个值可能对应 $2\cdot10^5$ 个下标，二分仍是 $O(\log n)$，但千万不能退化成逐个扫描。
8. **多测清空**：$\sum n,\sum q$ 有上界，但 $t$ 可达 $10^4$，每组都要重新建表；只有阶乘表是全局共享的。

## 相关题目与扩展

- [LeetCode 560. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/)：前缀和 + 哈希计数，与本题「值 → 下标表」的查表思路同源。
- [LeetCode 974. 和可被 K 整除的子数组](https://leetcode.cn/problems/subarray-sums-divisible-by-k/)：前缀和对 $K$ 取余后计数，同一模板的取模版本。
- [LeetCode 1546. 和为目标值且不重叠的非空子数组的最大数目](https://leetcode.cn/problems/maximum-number-of-non-overlapping-subarrays-with-sum-equals-target/)：前缀和 + 贪心挑切点，和本题「挑合法切点」的结构几乎一致。
- [Codeforces 2285C. Max Substitution](https://codeforces.com/problemset/problem/2285/C)：同场 C 题，排序 + 双指针/数据结构，可对照「查询独立 ⇒ 只预处理一次」的套路。

**延伸思考**：

1. 若查询**不独立**（在上一结果上累加），问题变成「区间加 + 全局 $0$ 计数」，需要分块或线段树 + 每块哈希表，$O(\sqrt n\log n)$ 或 $O(n\log^2 n)$。
2. 若要统计**所有段数**的特殊划分数，答案退化为 $\sum_{m\ge1}\binom{g}{m-1}=2^{g}$（$g\ge1$），一次预处理即可。
3. 把「反转」换成「循环移位」后，$D$ 会变成环上的差分，需要额外处理「绕一圈」的位移，但「$D=0$ 处即合法切点」这一核心不变。
4. 若进一步限制每段长度 $p_j\in[L,R]$，切点之间就有了间距约束，答案变成带间隙限制的组合计数，可用容斥或 DP + 前缀和解决。
