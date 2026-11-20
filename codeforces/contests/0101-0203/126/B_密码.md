# Codeforces 126B 密码 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/126/B
- **比赛来源**：Codeforces Beta Round 93 (Div. 1 Only) · Problem B（UTC 2011-11-09）
- **难度**：1700
- **标签**：字符串、Z 函数、KMP
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给定串 $s$，求最长的子串 $t$：$t$ 是 $s$ 的前缀、也是后缀、且**严格出现在中间**（既非开头也非结尾的一次出现）。不存在输出 `Just a legend`。

**约束**：

- $|s|\le10^6$：需要 $O(n)$ 的 Z 函数或前缀函数。
- 中间出现要求：存在 $i\ge1$ 使 $s[i..i+k-1]=t$ 且 $i+k\le n-1$。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
fixprefixsuffix
输出：
fix
```

官方样例二：

```text
输入：
abcdabc
输出：
Just a legend
```

**样例一走查**：`fix` 是前缀（位置 0）、后缀（位置 12），也在位置 6 出现（$6+3=9\le14$）✓。

**样例二走查**：`abc` 是前缀与后缀，唯一另一次出现在位置 4，$4+3=7$ 已到结尾 → 不算"中间" ✗ → 无解 ✓。

![Z 数组与候选](../../../images/cf126b_z.svg)

**观察**：需要同时满足两个条件：$k$ 是 border（前缀=后缀），且 $k$ 在中间出现过。前者用前缀函数链，后者用 Z 数组的最大值。

## 3. 解题思路

### 3.1 两个量

![样例对照](../../../images/cf126b_sample.svg)

- **Z 数组**：$z[i]=\mathrm{LCP}(s, s[i:])$。定义

$$\text{maxMid}=\max_{1\le i\le n-2}\min\bigl(z[i],\ n-1-i\bigr),$$

即在严格内部位置出现过的**最长**长度（$i+k\le n-1$ 限制了不能贴到结尾）。
- **前缀函数**：$\pi[n-1],\pi[\pi[n-1]-1],\dots$ 给出全部 border 长度。

### 3.2 算法

答案 = 不超过 $\text{maxMid}$ 的最长 border：从 $\pi[n-1]$ 沿链回溯，取第一个 $\le\text{maxMid}$ 的；若没有则无解。

### 3.3 样例走查

`fixprefixsuffix`：$z$ 在 $i=6$ 处为 3 → $\text{maxMid}\ge3$；border 链：$\pi[n-1]=3$ → 3 ≤ maxMid ✓ → 输出 `fix` ✓。
`abcdabc`：$i=4$ 处 $z=3$，但 $4+3=7=n$ → 被 $n-1-i=2$ 截断 → $\text{maxMid}=2$；border 只有 3 → 无解 ✓。

## 4. 正确性证明

**引理 1**：$\text{maxMid}$ 等于"能在严格中间出现的最长子串长度"。

**证明**：长度 $k$ 的子串在位置 $i$ 出现且严格在内部，等价于 $z[i]\ge k$ 且 $i+k\le n-1$；对每个 $i$ 能取的最大 $k$ 是 $\min(z[i],n-1-i)$，取 max 即得 ✓。∎

**引理 2**：$k$ 是 border 当且仅当 $k$ 出现在前缀函数链 $\pi[n-1],\pi[\pi[n-1]-1],\dots$ 上。

**证明**：标准 KMP 结论：$s[0..k-1]=s[n-k..n-1]$ 等价于 $\pi^{m}(n-1)=k$ 对某个 $m$ ✓。∎

**定理**：算法给出最长合法 $t$ 或正确判定无解。

**证明**：合法 $t$ 的长度必须同时是 border（引理 2）且 $\le\text{maxMid}$（引理 1）；算法沿 border 链取最大的 $\le\text{maxMid}$ 者，正是满足两者的最大长度 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n)$。
- **空间**：$O(n)$。
- **与时限的关系**：2 s 下 $n=10^6$ 实测 C++ 约 $20$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (!(cin >> s)) return 0;
    int n = (int)s.size();
    // Z 函数
    vector<int> z(n, 0);
    z[0] = n;
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
        if (i + z[i] > r) { l = i; r = i + z[i]; }
    }
    // 中间出现的最长长度（严格内部：i>=1 且 i+k<=n-1）
    int maxMid = 0;
    for (int i = 1; i <= n - 2; ++i) maxMid = max(maxMid, min(z[i], n - 1 - i));
    // 前缀函数，收集所有 border
    vector<int> pi(n, 0);
    for (int i = 1; i < n; ++i) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }
    int k = pi[n - 1];
    while (k > 0 && k > maxMid) k = pi[k - 1];
    if (k == 0) printf("Just a legend\n");
    else printf("%s\n", s.substr(0, k).c_str());
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
    s = data[0].decode()
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    max_mid = 0
    for i in range(1, n - 1):
        v = z[i]
        lim = n - 1 - i
        if v > lim:
            v = lim
        if v > max_mid:
            max_mid = v
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    k = pi[n - 1]
    while k > 0 and k > max_mid:
        k = pi[k - 1]
    sys.stdout.write((s[:k] if k > 0 else "Just a legend") + "\n")


main()
```

## 7. 边界情况与易错点

1. **"中间"必须严格**：出现位置 $i\ge1$ 且 $i+k\le n-1$（`abcdabc` 就是被这条否掉的）。
2. **$n\le2$**：不可能有中间出现 → 无解。
3. **整串不能作为答案**：$k<n$。
4. **$\text{maxMid}$ 的截断**：$\min(z[i], n-1-i)$，忘了截断会把"贴结尾"当成中间。
5. **border 链**：必须沿 $\pi$ 回溯，不能只看 $\pi[n-1]$。
6. **输出**：无解输出 `Just a legend`（大小写敏感）。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：2 / 2 通过（`fix`、`Just a legend`），C++ 与 Python 一致。
- **独立暴力对拍**：暴力对所有长度 $k$ 检查"前缀=后缀 + 严格内部出现"，**240 组**随机串（字母表 $\{a,b\}$，长度 $\le14$）全部一致。
- **性能**：$n=10^6$ 时 C++ 约 $20$ ms。
- **图片校验**：`cf126b_z.svg`、`cf126b_sample.svg` 通过 `ElementTree.parse`，无越界/重叠。
- **公式校验**：KaTeX 0 错；无 `---` 分隔线。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 126A Hot Bath](https://codeforces.com/problemset/problem/126/A)、[126C E-reader Display](https://codeforces.com/problemset/problem/126/C)、[126D Fibonacci Sums](https://codeforces.com/problemset/problem/126/D)、[126E Pills](https://codeforces.com/problemset/problem/126/E)：同场其余题。
- [Codeforces 1200E Compress Words](https://codeforces.com/problemset/problem/1200/E)：Z 函数合并。
- [LeetCode 1392. 最长快乐前缀](https://leetcode.cn/problems/longest-happy-prefix/)：几乎同一题的前缀函数版。
- [LeetCode 28. 找出字符串中第一个匹配项的下标](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)：KMP。

**延伸思考**：

1. **如果要求"至少出现 3 次"**：用 Z 数组统计每个长度的出现次数。
2. **如果"中间"允许贴结尾**：去掉 $n-1-i$ 截断即可。
3. **如果要求最长的"出现在中间 2 次"**：需要更细的计数。

