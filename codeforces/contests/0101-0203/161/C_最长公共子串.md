# Codeforces 161C 最长公共子串 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/161/C
- **比赛来源**：VK Cup 2012 Round 1 · Problem C（UTC 2012-03-11）
- **难度**：2400
- **标签**：递归、字符串、分治
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：字符串 $S_k$ 定义：$S_1=$`a`，$S_k=S_{k-1}+c_k+S_{k-1}$（$c_k$ 是字母表第 $k$ 个字符，字母表 36 位：`a`–`z`,`0`–`9`）。取 $S_{30}$，给两个区间 $[l_1,r_1]$、$[l_2,r_2]$，求这两段子串的**最长公共子串**长度。

**约束**：$l_i,r_i\le10^9$，$|S_{30}|=2^{30}-1$：递归分治。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3 6 1 4

输出：
2
```

$S_3=$`abacaba`：$[3,6]=$`acab`，$[1,4]=$`abac`；公共子串 `ac`（或 `ab`）⇒ 2 ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
1 1 4 4

输出：
0
```

$S_3[1]=$`a`、$S_3[4]=$`c` ⇒ 0 ✓

![S_k 的递归结构：中心唯一](../../../images/cf161c_structure.svg)

**观察 1（位置与字符）**：记 $v_2(i)$ 为 $i$ 中因子 2 的个数，则 $S_\infty[i]=c_{v_2(i)+1}$（例如位置 4 是 `c`、位置 8 是 `d`）。

**观察 2（关键引理）**：设两段在同一位移 $d=q-p$ 上对齐，则位置 $t$ 处字符相同 ⟺ $v_2(p+t)=v_2(q+t)$ ⟺ $v_2(d)>v_2(p+t)$ ⟺ $2^{v_2(d)}\nmid(p+t)$。

**证明见 §4 引理 2**。于是"同一段连续匹配"长度 ≤ $2^{v_2(d)}-1$，且**不能包含 $2^{v_2(d)}$ 的倍数**。

**观察 3（递归）**：据此可以证明：若两段的最长公共子串**跨过了** $S_k$ 的中心位置 $2^{k-1}$（在任一窗口中），则必有 $d=0$（即两段在相同位置对齐）；否则它完整落在某个"半区"里 ⇒ 递归。

## 3. 解题思路

设 `f(a,b,c,d,k)` = $S_k$ 中区间 $[a,b]$ 与 $[c,d]$ 的最长公共子串：

1. **对齐情形**：若两段位置有交集，交集部分逐字符相同 ⇒ 候选值 $\min(b,d)-\max(a,c)+1$；
2. **上界剪枝**：若该值已达 $\min(\text{两段长度})$，直接返回；
3. **递归**：$k\ge1$ 时把 $S_k$ 分成左半 $[1,2^{k-1}-1]$、中心 $2^{k-1}$、右半 $[2^{k-1}+1,2^k-1]$。把每个区间分别裁剪到左半与右半（右半坐标减去 $2^{k-1}$ 映射到左半），对**左右半的组合**递归到 $k-1$；
4. 中心位置不参与递归（见引理 4）；
5. 记忆化避免重复。

![样例 1：acab 与 abac 的公共子串](../../../images/cf161c_sample.svg)

## 4. 正确性证明

**引理 1（字符公式）**：$S_\infty[i]=c_{v_2(i)+1}$。

**证明**：对 $k$ 归纳。$S_k$ 由两段相同的 $S_{k-1}$ 与中心 $c_k$ 构成，位置 $2^{k-1}$ 的 $v_2=k-1$ ⇒ 中心字符 $c_k$ ✓；其余位置 $i$ 落在左半或右半，右半位置 $i=2^{k-1}+j$（$j<2^{k-1}$）满足 $v_2(i)=v_2(j)$ ⇒ 由归纳假设字符为 $c_{v_2(j)+1}=c_{v_2(i)+1}$ ✓ ∎

**引理 2（对齐判定）**：对 $x<y$ 且 $m=v_2(y-x)$：$v_2(x)=v_2(y)$ ⟺ $v_2(x)<m$。

**证明**：设 $x=2^t u$、$y=2^t v$（$u,v$ 奇）。若 $t<m$，则 $y-x=2^t(v-u)$ 且 $v-u$ 偶 ⇒ $v_2(y-x)>t$，即 $v_2(x)=t<v_2(y-x)$ ✓；反之若 $v_2(x)\ne v_2(y)$（不妨 $t_x<t_y$），则 $y-x=2^{t_x}(\text{奇}-\text{偶})$ 为奇数乘 $2^{t_x}$ ⇒ $v_2(y-x)=t_x=v_2(x)$ ✗ 矛盾于 $v_2(x)<m$ ✓ ∎

**引理 3（匹配长度上界）**：位移 $d\ne0$ 时，任何匹配段长 $L\le2^{v_2(d)}-1$。

**证明**：由引理 1、2，匹配要求所有 $p+t$ 满足 $2^{v_2(d)}\nmid(p+t)$；而连续的 $2^{v_2(d)}$ 个整数中必有一个是该数的倍数 ⇒ 连续匹配长度 < $2^{v_2(d)}$ ✓ ∎

**引理 4（跨中心必对齐）**：在 $S_k$ 内（位置 ≤ $2^k-1$），若匹配段包含中心 $2^{k-1}$，则 $d=0$。

**证明**：$d\ne0$ ⇒ $|d|\le2^k-1$ ⇒ $v_2(d)\le k-1=m$。由引理 3，匹配段不能包含 $2^m$ 的倍数；而中心 $2^{k-1}$ 是 $2^{k-1}$ 的倍数 ⇒ 匹配段不含中心 ✓ ∎

**引理 5（递归完备）**：任一匹配段（$d\ne0$）完整落在"某个半区"内（两段各自的那一半），因此由某个"半区对"的递归覆盖。

**证明**：由引理 4，匹配段不含中心，故在每段中它都落在左半或右半之一（连续且不含中心）✓ 两侧的半区内容都是 $S_{k-1}$，把右半坐标映射到左半后比较即得同一问题 ✓ ∎

**定理**：`f` 返回最长公共子串长度。

**证明**：对齐情形（$d=0$）由"交集逐字符相同"给出精确值；$d\ne0$ 由引理 5 归约到半区（规模减半）；引理 3、4 保证没有遗漏的跨中心情形。递归在 $k=0$ 终止，故返回最大值 ✓ ∎

## 5. 复杂度分析

- **时间**：每层最多 4 个分支、深度 30，加记忆化与剪枝；实测单次 < 10 ms。
- **空间**：$O(\text{状态数})$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

// abracadabra：第 k 步的串长 2^k-1，中心字符在第 2^{k-1} 位
// f(a,b,c,d,k) = S_k[a..b] 与 S_k[c..d] 的最长公共子串长
static map<tuple<ll,ll,ll,ll,int>, ll> memo;

ll f(ll a, ll b, ll c, ll d, int k) {
    if (a > b || c > d) return 0;
    ll ans = min(b, d) - max(a, c) + 1;          // 位置对齐的情形（含不相交）
    if (ans < 0) ans = 0;
    ll limit = min(b - a + 1, d - c + 1);
    if (ans >= limit) return ans;                // 已取到上界
    if (k == 0) return ans;
    auto key = make_tuple(a, b, c, d, k);
    auto it = memo.find(key);
    if (it != memo.end()) return it->second;
    ll mid = 1LL << (k - 1);
    vector<pair<ll,ll>> p1, p2;
    auto split = [&](ll lo, ll hi, vector<pair<ll,ll>> &out) {
        if (lo <= mid - 1) out.push_back({lo, min(hi, mid - 1)});
        if (hi >= mid + 1) out.push_back({max(lo, mid + 1) - mid, hi - mid});
    };
    split(a, b, p1);
    split(c, d, p2);
    for (auto &u : p1)
        for (auto &v : p2) {
            ll r = f(u.first, u.second, v.first, v.second, k - 1);
            if (r > ans) { ans = r; if (ans >= limit) break; }
        }
    memo[key] = ans;
    return ans;
}

int main() {
    ll l1, r1, l2, r2;
    if (scanf("%lld %lld %lld %lld", &l1, &r1, &l2, &r2) != 4) return 0;
    // 30 步的串长 2^30-1 >= 1e9，位置都在其中
    printf("%lld\n", f(l1, r1, l2, r2, 30));
    return 0;
}
```

### Python3

```python
import sys
from functools import lru_cache


def main():
    data = sys.stdin.read().split()
    l1, r1, l2, r2 = (int(v) for v in data[:4])

    @lru_cache(maxsize=None)
    def f(a, b, c, d, k):
        if a > b or c > d:
            return 0
        ans = min(b, d) - max(a, c) + 1      # 位置对齐（含不相交时为负）
        if ans < 0:
            ans = 0
        limit = min(b - a + 1, d - c + 1)
        if ans >= limit:
            return ans
        if k == 0:
            return ans
        mid = 1 << (k - 1)
        parts1 = []
        if a <= mid - 1:
            parts1.append((a, min(b, mid - 1)))
        if b >= mid + 1:
            parts1.append((max(a, mid + 1) - mid, b - mid))
        parts2 = []
        if c <= mid - 1:
            parts2.append((c, min(d, mid - 1)))
        if d >= mid + 1:
            parts2.append((max(c, mid + 1) - mid, d - mid))
        for u in parts1:
            for v in parts2:
                ans = max(ans, f(u[0], u[1], v[0], v[1], k - 1))
                if ans >= limit:
                    return ans
        return ans

    print(f(l1, r1, l2, r2, 30))


main()
```

## 7. 边界情况与易错点

1. **位置从 1 开始**：中心是 $2^{k-1}$，别用 0 基。
2. **两段可以不重叠**：此时对齐值为 0。
3. **$k=0$**：串长 1（只有 `a`）。
4. **递归层数**：$S_{30}$ 从 $k=30$ 开始。
5. **剪枝**：`ans >= limit` 时提前返回，否则分支数会爆炸。
6. **记忆化键**：$(a,b,c,d,k)$ 五元组。
7. **`long long`**：坐标到 $10^9$，$2^{k-1}$ 也大。
8. **右半坐标映射**：减去 $2^{k-1}$ 后再递归。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/161/C_最长公共子串.md`
- **官方样例**：$2/2$ 通过（`2`、`0`），C++ 与 Python 一致。
- **独立对拍**：用 $S_{10}$（长 1023）做暴力 LCS（$O(n^2)$ 逐对扩展），对 $150$ 组随机区间比较，全部一致；另对 $S_{12}$ 的若干大区间抽查一致。
- **性能**：$10^9$ 级区间的多个极端输入（全串对全串、单点对单点、错位大区间）C++ 均 < 10 ms、Python 约 26 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 161B Discounts](https://codeforces.com/problemset/problem/161/B)：同场 B 题。
- [Codeforces 161D Distance in Tree](https://codeforces.com/problemset/problem/161/D)：同场 D 题。
- [LeetCode 1143. 最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/)：LCS 基础。

**延伸思考**：

1. **若取 $S_k$ 的两个不同位置区间**（本题即如此）：递归分治。
2. **若字母表不同**：中心字符唯一性仍然成立，结论不变。
3. **若要求公共子串的出现次数**：需要额外的计数 DP。
