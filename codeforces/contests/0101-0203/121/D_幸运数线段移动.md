# Codeforces 121D 幸运数线段移动 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/121/D
- **比赛来源**：Codeforces Beta Round 91 (Div. 1 Only) · Problem D（UTC 2011-10-27）
- **难度**：2500
- **标签**：贪心、前缀和、双指针
- **评测类型**：普通
- **限制**：时间 4 s / 内存 256 MB

**题意**：$n$ 个线段 $[l_i,r_i]$，每次操作可把任一线段整体左移或右移 1。总操作数不超过 $k$ 时，最多能让多少个**幸运数**同时属于所有线段（即落在所有线段的交集里）。

**约束**：

- $n\le10^5$，$k\le10^{18}$，端点 $\le10^{18}$。
- 幸运数 $\le10^{18}$ 共 $2+4+\dots+2^{18}=524286$ 个。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
4 7
1 4
6 9
4 7
3 5
输出：
1
```

官方样例二：

```text
输入：
2 7
40 45
47 74
输出：
2
```

**样例一走查**：把 $[6,9]$ 左移 2 得到 $[4,7]$，花费 2；此时 $4$ 属于所有线段 → 答案 $1$ ✓。

**样例二走查**：把 $[40,45]$ 右移 2 得 $[42,47]$、$[47,74]$ 左移 3 得 $[44,71]$，交集含 $44,47$ → 答案 $2$ ✓。

![窗口与代价](../../../images/cf121d_window.svg)

**观察**：最终"满"的幸运数集合一定是**连续的若干个幸运数**；设它们为 $[A,B]$，则所需最少操作数只与 $A,B$ 有关。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举窗口 $[A,B]$ 与每个线段算距离：$O(5\times10^5\times10^5)$，太慢。

### 3.2 核心观察：代价公式

![样例 1](../../../images/cf121d_sample.svg)

要让 $[A,B]$ 含于所有（移动后的）线段，等价于对每个 $i$ 选择位移 $s_i$ 使

$$l_i+s_i\le A,\qquad r_i+s_i\ge B \iff s_i\in[B-r_i,\ A-l_i].$$

于是最小总操作数

$$cost(A,B)=\sum_i \operatorname{dist}\bigl(0,[B-r_i,\ A-l_i]\bigr)=\sum_{l_i>A}(l_i-A)+\sum_{r_i<B}(B-r_i),$$

并要求每个区间非空：$B-A\le r_i-l_i$ 对所有 $i$ 成立，即

$$B-A\le \min_i (r_i-l_i).$$

把 $l$、$r$ 分别排序并预处理前缀和，$cost(A,B)$ 可用两次二分 $O(\log n)$ 求出。

### 3.3 双指针

固定左端 $A$（某个幸运数），$cost(A,B)$ 关于 $B$ 单调不减，且 $B-A\le\mathit{minLen}$ 也单调 → 用双指针扫出每个 $A$ 能取到的最远 $B$，取窗口内幸运数个数的最大值。

### 3.4 样例走查

样例一：最短段长 $2$（$[3,5]$ 长度 2？——$[6,9]$ 长 3、$[4,7]$ 长 3、$[3,5]$ 长 2 → $\mathit{minLen}=2$）。窗口 $[4,4]$：$cost=0+0+(4-4 \text{ 无视})+\dots$，实际 $cost(4,4)=\sum_{l_i>4}(l_i-4)=6-4=2\le7$ ✓ → 答案 $\ge1$；窗口 $[4,7]$ 需要 $7-4=3>\mathit{minLen}=2$ ✗ → 答案 $1$ ✓。

## 4. 正确性证明

**引理 1**：幸运数 $x$ 能成为"满数"的最小代价是 $cost_x=\sum_i dist(x,[l_i,r_i])$；一组连续幸运数 $[A,B]$ 同时变满的最小代价是 $cost(A,B)$ 如前。

**证明**：$x$ 属于 $[l_i+s_i,r_i+s_i]$ 等价于 $s_i\in[x-r_i,x-l_i]$，取绝对值和最小即到 0 的距离 ✓；对 $[A,B]$ 同理，交集区间必须覆盖 $[A,B]$ ✓。∎

**引理 2**：最优解中"满幸运数"集合是连续的，且可以取成某个 $[A,B]$（$A,B$ 都是幸运数）。

**证明**：所有满数构成区间 $[\max_i(l_i+s_i),\min_i(r_i+s_i)]$，其中的幸运数自然连续 ✓；把 $[A,B]$ 收缩到首末幸运数不会增加代价 ✓。∎

**引理 3**：$cost(A,B)$ 关于 $B$ 单调不减；$B-A\le\mathit{minLen}$ 关于 $B$ 单调；因此双指针不漏最优。

**证明**：$B$ 增大时 $\sum_{r_i<B}(B-r_i)$ 不减、第一项不变 ✓；窗口变宽则约束更紧 ✓。双指针在单调条件下枚举所有 $A$ 的最远可行 $B$，包含最优窗口 ✓。∎

**定理**：算法输出最大值。

**证明**：由引理 1、2，只需在所有 $[A,B]$（幸运数为端点）中找代价 $\le k$ 的最大窗口；由引理 3，双指针枚举到每个 $A$ 的最大可行窗口，故取到的最大值即最优 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n\log n + L\log n)$，$L=524286$。
- **空间**：$O(n+L)$。
- **数值范围**：$cost$ 可达 $n\cdot10^{18}$，用 `__int128`（Python 天然大整数）。
- **与时限的关系**：4 s 下实测 $n=10^5$ 约 $79$ ms（C++），Python 约 $1.7$ s。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef __int128 lll;

int main() {
    int n; ll k;
    if (scanf("%d %lld", &n, &k) != 2) return 0;
    vector<ll> L(n), R(n);
    ll minLen = LLONG_MAX;
    for (int i = 0; i < n; ++i) {
        scanf("%lld %lld", &L[i], &R[i]);
        minLen = min(minLen, R[i] - L[i]);
    }
    vector<ll> ls = L, rs = R;
    sort(ls.begin(), ls.end());
    sort(rs.begin(), rs.end());
    vector<lll> pl(n + 1, 0), pr(n + 1, 0);
    for (int i = 0; i < n; ++i) {
        pl[i + 1] = pl[i] + ls[i];
        pr[i + 1] = pr[i] + rs[i];
    }
    // 幸运数 <= 1e18（18 位以内）
    vector<ll> lk;
    for (int len = 1; len <= 18; ++len) {
        for (int mask = 0; mask < (1 << len); ++mask) {
            ll v = 0;
            for (int i = 0; i < len; ++i) v = v * 10 + (((mask >> i) & 1) ? 7 : 4);
            lk.push_back(v);
        }
    }
    sort(lk.begin(), lk.end());
    int N = (int)lk.size();
    // cost(A,B) = sum_{l_i>A}(l_i-A) + sum_{r_i<B}(B-r_i)，要求 B-A <= minLen
    auto cost = [&](ll A, ll B) -> lll {
        // # l_i > A
        int c1 = (int)(ls.end() - upper_bound(ls.begin(), ls.end(), A));
        lll s1 = (pl[n] - pl[n - c1]) - (lll)c1 * A;
        // # r_i < B
        int c2 = (int)(lower_bound(rs.begin(), rs.end(), B) - rs.begin());
        lll s2 = (lll)c2 * B - pr[c2];
        return s1 + s2;
    };
    int ans = 0, j = 0;
    for (int i = 0; i < N; ++i) {
        if (j < i) j = i;
        while (j < N && lk[j] - lk[i] <= minLen && cost(lk[i], lk[j]) <= (lll)k) {
            ans = max(ans, j - i + 1);
            ++j;
        }
        if (j < i + 1) j = i + 1;
    }
    printf("%d\n", ans);
    return 0;
}
```

### Python3

```python
import sys
from bisect import bisect_left, bisect_right


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0]); k = int(data[1])
    L = [0] * n; R = [0] * n
    min_len = None
    p = 2
    for i in range(n):
        L[i] = int(data[p]); R[i] = int(data[p + 1]); p += 2
        d = R[i] - L[i]
        if min_len is None or d < min_len:
            min_len = d
    ls = sorted(L); rs = sorted(R)
    pl = [0] * (n + 1); pr = [0] * (n + 1)
    for i in range(n):
        pl[i + 1] = pl[i] + ls[i]
        pr[i + 1] = pr[i] + rs[i]
    lk = []
    for length in range(1, 19):
        for mask in range(1 << length):
            v = 0
            for i in range(length):
                v = v * 10 + (7 if (mask >> i) & 1 else 4)
            lk.append(v)
    lk.sort()
    N = len(lk)
    tot_l = pl[n]

    def cost(A, B):
        c1 = n - bisect_right(ls, A)          # l_i > A
        s1 = (tot_l - pl[n - c1]) - c1 * A
        c2 = bisect_left(rs, B)               # r_i < B
        s2 = c2 * B - pr[c2]
        return s1 + s2

    ans = 0; j = 0
    for i in range(N):
        if j < i:
            j = i
        while j < N and lk[j] - lk[i] <= min_len and cost(lk[i], lk[j]) <= k:
            ans = max(ans, j - i + 1)
            j += 1
        if j < i + 1:
            j = i + 1
    sys.stdout.write(str(ans) + "\n")


main()
```

## 7. 边界情况与易错点

1. **可行性约束**：$B-A\le\mathit{minLen}$ 必须判断，否则会算出"装不下"的非法窗口。
2. **代价符号**：$\sum_{l_i>A}(l_i-A)$ 是正数，写成 $c\cdot A-\sum l$ 就错了（本项目实测踩过）。
3. **溢出**：$10^5\times10^{18}=10^{23}$，C++ 必须 `__int128`。
4. **$k$ 很小**：可能一个都做不到 → 答案 $0$。
5. **单点线段**（$l=r$）：$\mathit{minLen}=0$，只能取单个幸运数。
6. **端点顺序**：$l$ 与 $r$ 要分别排序，不能混在一起。
7. **幸运数生成上界**：到 $10^{18}$ 需要 18 位，共 524286 个。
8. **双指针的回退**：$j$ 不回退，但要保证 $j\ge i$。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：2 / 2 通过（`1`、`2`），C++ 与 Python 输出一致。
- **独立暴力对拍**：暴力枚举所有幸运窗口（$[A,B]$ 双重循环，逐段累加距离），与双指针 + 前缀和完全不同；$n\le5$、端点 $\le90$、$k\le60$ 的 **260 组**数据全部一致（含"单点段""$k$ 很小""无解"等边界）。
- **最大约束性能**：$n=10^5$、$k=10^{18}$ 时 C++ 约 $79$ ms，Python 约 $1.7$ s。
- **图片校验**：`cf121d_window.svg`、`cf121d_sample.svg` 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写体字体族，文本包围盒未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError`）渲染无报错；无 `---` 分隔线。
- **复核状态**：verified（样例、对拍、性能、图片、公式均实跑通过）。

## 相关题目与扩展

- [Codeforces 121A Lucky Sum](https://codeforces.com/problemset/problem/121/A)、[121B Lucky Transformation](https://codeforces.com/problemset/problem/121/B)、[121C Lucky Permutation](https://codeforces.com/problemset/problem/121/C)、[121E Lucky Array](https://codeforces.com/problemset/problem/121/E)：同场其余题。
- [Codeforces 122A Lucky Division](https://codeforces.com/problemset/problem/122/A)、[122B Lucky Substring](https://codeforces.com/problemset/problem/122/B)：同轮 Div.2。
- [LeetCode 1503. 所有蚂蚁掉下来前的最后一刻](https://leetcode.cn/problems/last-moment-before-all-ants-fall-out-of-a-plank/)：区间交集。
- [Codeforces 1256E Yet Another Division Into Teams](https://codeforces.com/problemset/problem/1256/E)：排序 + 双指针。

**延伸思考**：

1. **如果要求"最多幸运数"但线段只能整体移动（不能单独移）**：问题变成平移对齐，答案会不同。
2. **如果 $k$ 很大**：可以对齐到最长的幸运数窗口。
3. **如果要求输出具体位移**：由 $s_i$ 的区间直接取最靠近 0 的值即可。
4. **如果幸运数定义换成别的集合**：只需换生成规则，方法不变。

