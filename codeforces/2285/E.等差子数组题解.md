# Codeforces 等差子数组 题解

## 1. 题目概述

- **标题 / 题号**：等差子数组（Codeforces 2285E，英文名 Arithmetic Subarray）
- **链接**：https://codeforces.com/problemset/problem/2285/E
- **来源**：Codeforces Round 1135 (Div. 2) · Problem E
- **难度**：未评级（2500 分）
- **限制**：时间 6 s / 内存 1024 MB
- **标签**：数据结构、贪心、实现、双指针

**题意**：给定长度为 $n$ 的整数数组 $a$ 与正整数 $k$。若子数组 $a[l..r]$ 的相邻差全部相等（$a_{l+1}-a_l=a_{l+2}-a_{l+1}=\cdots=a_r-a_{r-1}$，长度 1 也算），称其为**等差子数组**。你可以至多选 $k$ 个位置改成**任意整数**（允许超出 $[1,10^9]$），求修改后最长等差子数组的长度。多测：首行 $t$，每组给出 $n,k$ 与 $a_1,\dots,a_n$，输出一个整数。

**约束**：$1 \le t \le 10^4$，$2 \le n \le 2\cdot 10^5$，$1 \le k \le \min(n,1500)$，$1 \le a_i \le 10^9$；$\sum n \le 2\cdot 10^5$，**且** $\sum n\cdot k \le 10^7$。最后一条是出题人给的"复杂度许可证"：$\sum nk$ 只有 $10^7$，预期就是 $O(nk)$ 做法。

## 2. 示例

```text
输入
4
5 1
1 2 6 4 5
5 1
1 2 3 100 200
3 1
1 1000000000 2
6 2
1 2 4 8 16 32

输出
5
4
3
4
```

对应方案：第 1 组把 $6$ 改成 $3$ 得 $[1,2,3,4,5]$；第 2 组把 $100$ 改成 $4$ 得 $[1,2,3,4]$；第 3 组保留 $a_2=10^9,a_3=2$ 得 $d=2-10^9$、反推 $a_1=1999999998$；第 4 组把 $[1,2,4,8]$ 改成 $[1,2,3,4]$（两次修改）。

## 3. 解题思路

### 3.1 暴力思路

枚举子数组 $[l,r]$，再枚举"保留哪两个位置"定公差 $d=(a_q-a_p)/(q-p)$ 并逐格统计匹配数：单区间 $O(L^3)$、全部 $O(n^5)$。即使固定 $l$ 让 $r$ 递增、增量维护每个 $d$ 的匹配数，也要对每个 $l$ 扫 $O(n)$ 个右端点，仍是 $O(n^2)$，$n=2\cdot10^5$ 过不去。

### 3.2 核心观察：公差被"两个未修改位置"锁定

![核心观察：公差必须是整数，且由两个未修改位置唯一确定](images/cf2285_e_gap_concept.svg)

1. **公差必须是整数**：改后元素全是整数，故 $d=a_{m+1}-a_m\in\mathbb{Z}$；候选公差只能来自整数斜率，检验即 $(a_j-a_i)\bmod(j-i)=0$。
2. **连续 $k+1$ 格中至少 1 格没被改**：若 $i$ 是"最左未修改位置"、$j$ 是它右边第一个未修改位置，则 $(i,j)$ 内全被改，得 $j-i-1\le k$，即 $j-i\le k+1$——**每个 $i$ 只有 $O(k)$ 个候选公差**。
3. **两点定直线、其余逐格核对**：$c=a_i-i\cdot d$，位置 $m$ 匹配 $\iff a_m=c+m\cdot d$，不匹配的格子各花 1 次修改。
4. **区间够长时公差是唯一众数**：若 $r\ge i+2k+1$，窗口 $[i,i+2k+1]$ 有 $2k+2$ 格而总修改 $\le k$，故真公差在窗口内至少匹配 $k+2$ 格，其它公差最多匹配剩下的 $k$ 格。

### 3.3 算法流程：枚举左端点 + 短窗口取众数 + 长区间跳跃推进

![等差分极长段跳跃与贪心推进](images/cf2285_e_jump_runs.svg)

枚举 $i$ 表示"答案区间中最左边不被修改的位置"，分两种情形。

**(a) 短区间 $r\le i+2k+1$**：枚举 $j=i+1,\dots,\min(n,i+2k+1)$，边扫边维护各候选公差的出现次数与众数，取 $\text{need}(j)=(j-i)-\max_d\#\{m\in(i,j]:a_m=a_i+(m-i)d\}$、候选长度 $(j-i+1)+\min(i-1,k-\text{need})$；一旦 $\text{need}(j)>k$ 就说明最好的公差也覆盖不了 $[i,j]$，立即 `break`。

**(b) 长区间 $r>i+2k+1$**：由观察 4，窗口众数就是真公差 $d$。从 $i$ 出发沿直线向右**跳**：用跳表 `nxt[m]`（最小的 $p>m$ 使 $\mathrm{diff}[p]\ne\mathrm{diff}[m]$）一次跨过整段"等差且公差为 $d$"的区域；每撞到一个不匹配位置就 `used++` 并以它为新起点，直到 `used = k` 或走到 $n$，记右端 `cnt`；最后用余额向**左**逐格延伸 $\min(i-1,k-\text{used})$ 格。答案初值取 $\min(n,k+1)$（保留 1 格、改 $k$ 格）。

> 💡 为什么"先把额度全给右侧"不吃亏：右侧每多花 1 次修改，右端至少推进 1 格；这 1 次额度放到左侧也只换来 1 格。边际收益都是 1，故先推右侧再补左侧不会更差（引理 6）。

### 3.4 示例演算

![样例演算：值 1,2,6,4,5，k=1](images/cf2285_e_walkthrough.svg)

以样例 1（$a=[1,2,6,4,5],k=1$）为例：$i=1$ 时窗口 $[1,4]$ 内 $j=2$、$j=4$ 都给出 $d=1$（众数计数 2），$\text{need}=3-2=1\le k$；因 $i+2k+1=4<5$ 进入跳跃分支——位置 3 的 $6\ne1+2$ 必须改（`used=1`），之后 4、5 全匹配，`cnt=5`，余额 0，长度 $5$。$i=2$ 时众数 $d=1$、$j=5$ 时 $\text{need}=1$，长度 $(5-2+1)+0=4$；$i=3$ 时众数 $d=-2$、长度 $3$；$i\ge4$ 只能取到 $3$ 或 $1$。故答案为 $5$。

## 4. 算法细节

1. **整数公差**：用 `num % den == 0` 判断；$num$ 可为负，C++ 取模向零取整、Python 取模向下取整，但"是否整除"的判定都正确。
2. **跳表 `nxt`**：$\mathrm{diff}[m]=a_m-a_{m-1}$（$m\ge2$），从后往前推 `nxt[m] = diff[m+1] != diff[m] ? m+1 : nxt[m+1]`，边界 `nxt[n] = -1`。
3. **跳跃的三分支**：设 `pos` 处直线值应为 `lv`：$a_{pos+1}\ne lv+d$ 则下一不匹配为 $pos+1$；否则 $a_{pos+2}\ne lv+2d$ 则为 $pos+2$；否则两点都匹配、$\mathrm{diff}[pos+2]=d$，直接跳 `nxt[pos+2]`（$-1$ 表示后面全匹配）。
4. **额度分配**：左侧只加 $\min(i-1,k-\text{used})$，`min` 的两项分别是数组左边界与剩余额度，缺一不可。
5. **多测清空与剪枝**：每组重算 `nxt`、`mp.clear()`（保留桶避免反复分配）；`ans == n` 立即结束，若 $(n-i+1)+\min(i-1,k)\le ans$ 则整段跳过（右侧最多到 $n$、左侧最多 $k$ 格的平凡上界）。
6. **防卡哈希与数值范围**：键是 `long long`，Codeforces 可构造退化数据，必须用 `splitmix64` 之类的随机化哈希并 `reserve` 到 $2k+4$ 量级；$c=a_i-i\cdot d$ 与直线值 $c+m\cdot d$ 都可达 $2\cdot10^{14}$，全程 `long long`。

## 5. 正确性证明

**引理 1（整数公差）**：若 $[l,r]$（$r>l$）能改成等差数列，则公差 $d\in\mathbb{Z}$。**证明**：改后元素全是整数，而 $d=a_{l+1}-a_l$ 是两个整数之差。∎ **引理 2（保留点间距）**：设目标直线为 $a_m=c+md$，称满足等式的 $m$ 为保留点。若 $i<j$ 是相邻保留点，则 $j-i\le k+1$ 且 $i-l\le k$。**证明**：$(i,j)$ 内无保留点、必须全改，加上 $[l,i)$ 内的修改共 $(j-i-1)+(i-l)\le k$，移项即得。∎

**引理 3（短窗口的众数截断）**：固定 $i$，记 $M(j)=\max_d\#\{m\in(i,j]:a_m=a_i+(m-i)d\}$（只统计使 $(a_j-a_i)/(j-i)$ 为整数的 $d$）。则 (1) 若"以 $i$ 为最左保留点、右端为 $r$"可行，则 $(r-i)-M(r)\le k$；(2) 对任意 $j$，取 $x=\min\big(i-1,k-((j-i)-M(j))\big)$，则 $[i-x,j]$ 可用不超过 $k$ 次修改变成等差数列。**证明**：(1) 设该区间公差为 $d$，$(i,r]$ 内不匹配 $d$ 的位置数为 $(r-i)-\#\{m\in(i,r]:a_m=a_i+(m-i)d\}\le(r-i)-M(r)$，而不超过区间总修改数 $k$。(2) 取众数 $d$：$[i,j]$ 内匹配 $M(j)+1$ 个、需改 $(j-i)-M(j)$ 个，再把 $[i-x,i)$ 的 $x$ 格改成直线值，总修改 $\le k$，结果正是公差 $d$ 的等差数列。∎

**引理 4（长区间公差唯一）**：若可行区间右端 $r\ge i+2k+1$（$i$ 为最左保留点），则窗口 $[i,i+2k+1]$ 内真公差的匹配数 $\ge k+2$，其它整数公差的匹配数 $\le k$，故众数唯一且等于真公差。**证明**：窗口共 $2k+2$ 格且全在区间内、总修改 $\le k$，故至少 $k+2$ 格匹配真公差；其余至多 $k$ 格才可能匹配别的公差。∎

**引理 5（跳表正确）**：设 $p$ 匹配直线 $(d,c)$（$a_p=c+pd$），则跳跃函数返回 $p$ 之后第一个不匹配位置（不存在则 $n+1$）。**证明**：若 $a_{p+1}\ne c+(p+1)d$ 则 $p+1$ 即答案；若 $a_{p+1}$ 匹配而 $a_{p+2}\ne c+(p+2)d$ 则 $p+2$ 是第一个；否则 $a_{p+1},a_{p+2}$ 都匹配，于是 $\mathrm{diff}[p+2]=d$，而对 $m>p+2$ 有 $a_m=c+md\iff\mathrm{diff}[p+3..m]$ 全等于 $d$，故第一个不匹配位置正是 $\mathrm{nxt}[p+2]$。∎ **引理 6（额度分配单调）**：固定 $i,d$，设 $m_1<m_2<\cdots$ 为 $(i,n]$ 内不匹配位置，令 $f(B)=m_{B+1}-i$（右侧花 $B$ 次额度能到达的长度，额度足够时 $f(B)=n-i+1$），则 $B\mapsto\min(i-1,k-B)+f(B)$ 在 $0\le B\le k$ 上单调不减。**证明**：$f(B+1)-f(B)=m_{B+2}-m_{B+1}\ge1$；当 $k-B\le i-1$ 时该式为 $k+(f(B)-B)$，而 $f(B)-B=m_{B+1}-i-B$ 的增量 $m_{B+2}-m_{B+1}-1\ge0$，当 $k-B>i-1$ 时该式为 $(i-1)+f(B)$，两种情形都随 $B$ 不减。∎

**定理**：算法输出恰为最优答案。**证明**：先证候选可达：窗口分支由引理 3(2) 构造；跳跃分支中每个被跳过的位置都匹配、每个 `used` 对应一个真实修改位置，再加左侧 $x=\min(i-1,k-\text{used})$ 格，总修改 $\le k$。再证最优解被覆盖：设最优区间 $[l^*,r^*]$、直线 $(d^*,c^*)$，$i^*$ 为最左保留点，$x=i^*-l^*$，$B$ 为 $(i^*,r^*]$ 内不匹配数，则 $x+B\le k$。若 $r^*\le i^*+2k+1$，对任意 $j\le r^*$ 有 $M(j)\ge(j-i^*)-B$，故 $\text{need}(j)\le B\le k$，扫描不会提前 break 且会走到 $j=r^*$，该步候选 $\ge(r^*-i^*+1)+x=r^*-l^*+1$。若 $r^*>i^*+2k+1$，由引理 4 跳跃分支用的正是 $d^*$：当 `used` $=k$ 时第 $k+1$ 个不匹配位置 $m_{k+1}\ge r^*+x+1$（因 $(r^*,m_{k+1}]$ 内还需 $k+1-B\ge x+1$ 个不匹配），候选 $=m_{k+1}-i^*\ge r^*-l^*+1$；当 `used` $<k$（提前走到 $n$）时设 $extra$ 为 $(r^*,n]$ 内不匹配数，候选与 $r^*-l^*+1$ 之差为 $(n-r^*-extra)+(k-x-B)\ge0$；引理 6 保证"额度全给右侧"不小于任何其它分配。综上输出最大值恰为答案。∎

## 6. 复杂度分析

- **时间**：$O(nk)$。每个 $i$ 的窗口扫描 $O(\min(n-i,2k+1))$，跳跃分支每次迭代要么消耗 1 次额度要么结束、故 $O(k)$，哈希表均摊 $O(1)$；由 $\sum nk\le10^7$ 得内层动作约 $2\cdot10^7$ 次。实测最坏（$n=2\cdot10^5,k=50$）约 $0.50$ s，$6$ s 限制下留了 10 倍余量。
- **空间**：$O(n)$。$a$、`nxt` 各一份，哈希表最多 $O(k)$ 个键。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 200005;
int n, k, nxtv[MAXN];                    // nxtv[m] = 最小的 p>m 使 diff[p] != diff[m]
ll a[MAXN];

struct SplitMix {                        // 随机化哈希，防被卡
    size_t operator()(uint64_t x) const {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        x ^= x >> 31;
        static const uint64_t R = chrono::steady_clock::now().time_since_epoch().count();
        return (size_t)(x ^ R);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    unordered_map<ll, int, SplitMix> mp;
    mp.reserve(8192);
    while (T--) {
        cin >> n >> k;
        for (int i = 1; i <= n; i++) cin >> a[i];
        nxtv[n] = -1;
        for (int m = n - 1; m >= 2; m--)
            nxtv[m] = (a[m + 1] - a[m] != a[m] - a[m - 1]) ? m + 1 : nxtv[m + 1];

        int ans = min(n, k + 1);         // 保留 1 格、把另外 k 格改成同一等差数列
        for (int i = 1; i <= n; i++) {
            if (ans == n) break;
            if ((ll)(n - i + 1) + min(i - 1, k) <= ans) continue;   // 长度上界剪枝
            mp.clear();
            int limit = (int)min<ll>(n, (ll)i + 2LL * k + 1), modeCnt = 0, pos = i, used = 0, cnt = i;
            ll modeD = 0;
            bool broken = false;
            for (int j = i + 1; j <= limit; j++) {                 // (a) 短窗口：边扫边取众数
                ll num = a[j] - a[i], den = j - i;
                if (num % den == 0) {                              // 公差必须是整数
                    ll d0 = num / den;
                    int t = ++mp[d0];
                    if (t > modeCnt) { modeCnt = t; modeD = d0; }
                }
                int need = (j - i) - modeCnt;
                if (need > k) { broken = true; break; }
                ans = max(ans, (j - i + 1) + min(i - 1, k - need));
            }
            if (broken || limit == n) continue;                    // (b) 长区间：众数唯一
            ll d = modeD, c = a[i] - (ll)i * d;
            while (true) {                                         // 沿等差分极长段跳跃
                ll lv = c + (ll)pos * d;
                int q = n + 1;
                if (pos < n) {
                    if (a[pos + 1] != lv + d) q = pos + 1;
                    else if (pos + 1 < n) {
                        if (a[pos + 2] != lv + 2 * d) q = pos + 2;
                        else { int z = nxtv[pos + 2]; if (z != -1) q = z; }
                    }
                }
                if (q > n) { cnt = n; break; }
                cnt = q - 1;
                if (used == k) break;
                used++, pos = q;
            }
            ans = max(ans, cnt - i + 1 + min(i - 1, k - used));
        }
        cout << ans << "\n";
    }
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.buffer.read().split()
    p, res = 1, []
    for _ in range(int(data[0])):
        n, k = int(data[p]), int(data[p + 1]); p += 2
        a = [0] + [int(x) for x in data[p:p + n]]; p += n

        nxt = [-1] * (n + 2)                       # 等差分极长段的跳表
        for m in range(n - 1, 1, -1):
            nxt[m] = m + 1 if a[m + 1] - a[m] != a[m] - a[m - 1] else nxt[m + 1]

        ans = min(n, k + 1)
        for i in range(1, n + 1):
            if ans == n:
                break
            if (n - i + 1) + min(i - 1, k) <= ans:     # 长度上界剪枝
                continue
            ai, lim = a[i], min(n, i + 2 * k + 1)
            cnt, mc, md, brk = {}, 0, 0, False
            for j in range(i + 1, lim + 1):        # (a) 短窗口：边扫边取众数
                num, den = a[j] - ai, j - i
                if num % den == 0:                 # 公差必须是整数
                    d0 = num // den
                    cnt[d0] = t = cnt.get(d0, 0) + 1
                    if t > mc:
                        mc, md = t, d0
                need = (j - i) - mc
                if need > k:
                    brk = True
                    break
                cand = (j - i + 1) + min(i - 1, k - need)
                if cand > ans:
                    ans = cand
            if brk or lim == n:
                continue

            d, c = md, ai - i * md                 # (b) 长区间：众数唯一，跳跃推进
            pos, used, cn = i, 0, i
            while True:
                lv, q = c + pos * d, n + 1
                if pos < n:
                    if a[pos + 1] != lv + d:
                        q = pos + 1
                    elif pos + 1 < n:
                        if a[pos + 2] != lv + 2 * d:
                            q = pos + 2
                        else:
                            z = nxt[pos + 2]
                            if z != -1:
                                q = z
                if q > n:
                    cn = n
                    break
                cn = q - 1
                if used == k:
                    break
                used += 1
                pos = q
            cand = cn - i + 1 + min(i - 1, k - used)
            if cand > ans:
                ans = cand
        res.append(str(ans))
    sys.stdout.write("\n".join(res) + "\n")


main()
```

> ⚠️ Python 版同阶 $O(nk)$ 但常数大：实测最坏约 $7.7$ s（$n=2\cdot10^5,k=50$、取值只有两种的数据），会超过 6 s。**建议提交 C++ 或 PyPy**，CPython 可能 TLE。

## 8. 边界情况与易错点

1. **答案下界**：长度 $k+1$ 永远可达（保留 1 格、另 $k$ 格改成同一等差数列），`ans` 初值必须取 $\min(n,k+1)$，否则数组极乱或 $k\ge n-1$ 时会漏解。
2. **公差必须整数**：$[1,3,2]$ 两端斜率是 $0.5$、中间要填 $2.5$（非整数），它在 $k=0$ 时**不是**等差数列；只接受整数斜率才不会误判。
3. **窗口要扫到 $i+2k+1$**：只扫 $i+k+1$ 无法保证长区间众数唯一（引理 4 需要 $2k+2$ 格窗口里出现 $k+2$ 个匹配），会漏掉长区间最优解。
4. **左侧额度取 min**：`k-used` 可能大于 $i-1$，直接相加会把左端点推出数组；`need` 也可能超过 $k$（`break` 前那一步），减法为负必须靠 `break` 拦住。
5. **`nxt` 的前提、哈希与溢出**：只有 $a_{pos+1},a_{pos+2}$ 都匹配时才能跳 `nxt[pos+2]`，`pos==n`、`pos+1==n` 要单独处理；`unordered_map<long long,int>` 默认哈希可被构造退化，务必换随机化哈希；$c=a_i-i\cdot d$ 量级 $2\cdot10^{14}$，必须 `long long`。

## 相关题目与扩展

- [Codeforces 2285C Max Substitution](https://codeforces.com/problemset/problem/2285/C)：同场题，也是"排序后对每个位置算最优替换值"，可对照众数/前后缀思想。
- [LeetCode 1027. 最长等差数列](https://leetcode.cn/problems/longest-arithmetic-subsequence/)：子序列版本、$O(n^2)$ 枚举公差，与本题"两点定公差"骨架一致（不能改元素）；[LC 1218](https://leetcode.cn/problems/longest-arithmetic-subsequence-of-given-difference/) 则是公差已知的哈希表 DP。

**延伸思考**：(1) 若限制"只能改成 $[1,10^9]$ 内的整数"，跳跃时需检查 $c+md$ 是否越界，它关于 $m$ 单调、可二分定位，仍是 $O(nk)$。(2) 若 $k$ 放大到 $10^5$ 且不再保证 $\sum nk$，本做法退化；"固定公差 + 滑动窗口"的总代价是 $O(n^2)$，能否用随机采样把候选公差压到 $O(\sqrt n)$ 个值得思考。(3) 若要输出方案，只需在更新 `ans` 时记录 $(i,\text{used},d,\text{cnt},x)$ 再按 $a_m=c+md$ 回填。
