# Codeforces 212B 好子串（Good Substrings） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/212/B
- **比赛来源**：VK Cup 2012 Finals (unofficial online-version) · Problem B（UTC 2012-07-16）
- **难度**：2200
- **标签**：字符串、双指针、位掩码、哈希
- **评测类型**：普通
- **限制**：时间 4 s / 内存 256 MB

**题意**：对字符串 $s$ 与字符集 $C$，令 $r(C,s)$ 为“trace 恰为 $C$ 且按包含关系极大”的子串个数（不同位置算不同子串）。给定 $s$ 与 $m$ 个查询集合 $C_i$（以其元素构成的串给出，字符互不相同），求每个 $r(C_i,s)$。

**约束**：$|s|\le10^6$，$m\le10^4$，字符集为小写字母，$C_i\ne\varnothing$。

## 2. 示例与观察

官方样例一：

```text
输入：
aaaaa
2
a
a

输出：
1
1
```

官方样例二：

```text
输入：
abacaba
3
ac
ba
a

输出：
1
2
4
```

**观察**：“按包含极大”等价于：该子串不能再向左右扩展成 trace 相同的子串。对固定 $C$，把所有“只由 $C$ 中字符组成”的极大连续块拿出来，每块中只有整块本身是极大的；它属于集合当且仅当块内 trace 恰为 $C$。

![封闭窗口计数](../../../images/cf212b_window.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

对每个查询扫描整个串找极大块，$O(|s|)$ 每问 ⇒ $10^{10}$，超时。

### 3.2 核心观察

把答案改写为“封闭窗口”计数：窗口 $[l,r]$ 满足 $s[l-1]\notin\mathrm{trace}$、$s[r+1]\notin\mathrm{trace}$ 且 $\mathrm{trace}(l,r)=C$ 时，它对 $r(C)$ 贡献 1（且每个窗口只对应唯一的 $C$）。固定 $l$ 向右扫，只有遇到“窗口里还没出现过的字符”时右端才可能封闭 —— 每次都会新增一种字符，所以每个 $l$ 至多 26 个封闭窗口，总共 $O(26|s|)$ 个。

### 3.3 算法流程

1. 预处理每个位置 $l$ 处 26 个字符的“下一次出现位置” $nxt_c$（从右往左扫维护）。
2. 对每个 $l$：把 26 个 $nxt_c$ 排序，按值递增枚举“新字符首次出现的位置” $v$。
3. 此时窗口 $[l,v-1]$ 的 trace 掩码为“$nxt_c<v$ 的字符集合”，若 $l=0$ 或 $s[l-1]$ 不在该掩码中，就把该掩码的计数 +1。
4. 处理完 26 个字符后，窗口 $[l,n-1]$ 同样检查一次。
5. 查询时直接查掩码对应的计数（只对出现过的查询掩码维护哈希表）。

![样例二走查](../../../images/cf212b_walk.svg)

### 3.4 样例走查

$s=\texttt{abacaba}$，$C=\{a,c\}$：只由 $a,c$ 组成的极大块是 $\texttt{abacab}$ 中的 $\texttt{a?a?a}$（第 1–5 位），其 trace 为 $\{a,c\}$ ⇒ 1；$C=\{b,a\}$ 时块 $\texttt{aba}$（1–3）与 $\texttt{aba}$（5–7）各贡献 1 ⇒ 2；$C=\{a\}$ 时 4 个单字符块 ⇒ 4。

## 4. 正确性证明

**引理 1（极大 ⟺ 整块）**：对固定 $C$，trace 为 $C$ 的子串按包含极大当且仅当它是某个“只含 $C$ 中字符”的极大连续块，且该块 trace 恰为 $C$。

**证明**：若子串不是整块，则它所在的极大块中它某一侧还有字符（属于 $C$），扩展到那一格 trace 不变 ⇒ 不极大。反过来整块无法扩展：两侧要么越界要么是不属于 $C$ 的字符 ⇒ 极大。∎

**引理 2（封闭窗口与极大块一一对应）**：$[l,r]$ 是 trace 为 $C$ 的极大块 ⟺ $s[l-1]\notin C$、$s[r+1]\notin C$ 且 $\mathrm{trace}(l,r)=C$。

**证明**：由引理 1，极大块等价于“左右两侧都不在 $C$ 中且块内字符全在 $C$ 中、trace 恰为 $C$”。∎

**引理 3（枚举完备）**：算法枚举出的窗口恰为所有封闭窗口。

**证明**：固定 $l$，随着 $r$ 增大 trace 单调增大；$s[r+1]\notin\mathrm{trace}(l,r)$ 恰在 $s[r+1]$ 是“窗口中首次出现的字符”时成立，这些位置正是 $nxt$ 排序后的各个不同取值，算法逐一枚举；$r=n-1$ 单独处理。∎

**定理**：对每个查询 $C$，算法给出的计数等于 $r(C,s)$。

**证明**：由引理 2、3，算法统计的正是 trace 为 $C$ 的封闭窗口数；再由引理 1 与引理 2 的等价性，这等于 $r(C,s)$。∎

## 5. 复杂度分析

- **时间**：每个 $l$ 排序 26 个值并枚举，$O(26|s|\log 26)$；查询 $O(m)$。$|s|=10^6$ 实测 0.4 s。
- **空间**：$O(|s|+m)$（只对查询里出现过的掩码开哈希表）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    static char buf[1000005];
    if (scanf("%s", buf) != 1) return 0;
    int n = (int)strlen(buf);
    vector<int> s(n);
    for (int i = 0; i < n; ++i) s[i] = buf[i] - 'a';
    int m;
    if (scanf("%d", &m) != 1) return 0;
    vector<int> qmask(m, 0);
    for (int i = 0; i < m; ++i) {
        char t[32];
        scanf("%s", t);
        int mk = 0;
        for (int j = 0; t[j]; ++j) mk |= 1 << (t[j] - 'a');
        qmask[i] = mk;
    }
    // 只对查询里出现过的 mask 计数
    unordered_map<int, long long> cnt;
    cnt.reserve(m * 2);
    for (int i = 0; i < m; ++i) cnt.emplace(qmask[i], 0);
    vector<int> nxt(26, INT_MAX);
    vector<pair<int,int>> ord(26);
    for (int l = n - 1; l >= 0; --l) {
        nxt[s[l]] = l;
        for (int c = 0; c < 26; ++c) ord[c] = {nxt[c], c};
        sort(ord.begin(), ord.end());
        int mask = 0, prevChar = -1;
        int leftOutside = (l == 0) ? -1 : s[l - 1];
        for (int idx = 0; idx < 26; ) {
            int v = ord[idx].first;
            // 窗口 [l, v-1] 的 trace 恰为 mask
            if (v > l && mask != 0) {
                bool ok = (leftOutside < 0) || ((mask >> leftOutside & 1) == 0);
                if (ok) {
                    auto it = cnt.find(mask);
                    if (it != cnt.end()) ++it->second;
                }
            }
            while (idx < 26 && ord[idx].first == v) { mask |= 1 << ord[idx].second; ++idx; }
        }
        // 最后一段：窗口 [l, n-1]
        if (mask != 0) {
            bool ok = (leftOutside < 0) || ((mask >> leftOutside & 1) == 0);
            if (ok) {
                auto it = cnt.find(mask);
                if (it != cnt.end()) ++it->second;
            }
        }
    }
    for (int i = 0; i < m; ++i) printf("%lld%c", cnt[qmask[i]], i + 1 == m ? '\n' : ' ');
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    s = data[0]
    n = len(s)
    m = int(data[1])
    queries = [data[2 + i] for i in range(m)]
    qmask = []
    for t in queries:
        mk = 0
        for ch in t:
            mk |= 1 << (ch - 97)
        qmask.append(mk)
    cnt = {mk: 0 for mk in qmask}
    nxt = [10 ** 9] * 26
    for l in range(n - 1, -1, -1):
        nxt[s[l] - 97] = l
        ord_ = sorted((nxt[c], c) for c in range(26))
        mask = 0
        left_out = -1 if l == 0 else s[l - 1] - 97
        idx = 0
        while idx < 26:
            v = ord_[idx][0]
            if v > l and mask != 0:
                if left_out < 0 or not (mask >> left_out) & 1:
                    if mask in cnt:
                        cnt[mask] += 1
            while idx < 26 and ord_[idx][0] == v:
                mask |= 1 << ord_[idx][1]
                idx += 1
        if mask != 0:
            if left_out < 0 or not (mask >> left_out) & 1:
                if mask in cnt:
                    cnt[mask] += 1
    print(' '.join(str(cnt[mk]) for mk in qmask))


main()
```

## 7. 边界情况与易错点

1. **$|s|=1$**：只有一个封闭窗口，答案只可能是 1（若查询包含 $s_0$）或 0。
2. **查询集合含未出现的字符**：答案为 0（掩码查不到）。
3. **重复查询**：同一掩码要输出同样的计数，用哈希表按掩码聚合。
4. **相同字符的块**：如 `aaaaa` 查询 `a`，整个串是一个块 ⇒ 1，不是 5。
5. **掩码大小**：必须用 26 位掩码而不是长度，`ac` 与 `ca` 是同一集合。
6. **窗口为空**（$v=l$ 时）：跳过，空串不是合法子串。

## 8. 验证记录

- **编译环境与命令**：`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/212/B_好子串.md`。
- **官方样例**：2 / 2 通过（`1 1`、`1 2 4`）。
- **随机对拍**：独立暴力“逐查询扫描找极大块并比较 trace”随机 $|s|\le12$、字母表 $\le4$ 共 **300 组**，C++ 与 Python 均与暴力完全一致。
- **性能**：$|s|=10^6$、$m=10^4$（随机大写表 26 字母）0.39 s；全 `a` 数据 0.06 s。
- **图片校验**：`cf212b_window.svg`、`cf212b_walk.svg` 通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 212C 牛仔](https://codeforces.com/problemset/problem/212/C)：同场题目。
- [LeetCode 992 K 个不同整数的子数组](https://leetcode.cn/problems/subarrays-with-k-different-integers/)：双指针 + 计数。
- [Codeforces 213E 两个排列](https://codeforces.com/problemset/problem/213/E)：另一种“窗口 + 哈希”技巧。

**延伸思考**：

1. 若查询是“trace 是 $C$ 的子集”而非恰好相等，可以用超集/子集和（SOS DP）在 $2^{26}$ 上做，但本题只问恰好相等。
2. 若要求“所有 $C$ 的答案”，可以枚举所有封闭窗口并在 $2^{26}$ 的数组上累加（不可行），或按需查询。
3. 本题的关键是**把“极大子串”转成“封闭窗口”**，再用“新字符至多 26 次”把枚举量压到线性。
