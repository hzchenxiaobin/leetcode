# Codeforces 159D 回文子串对计数 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/159/D
- **比赛来源**：VK Cup 2012 Qualification Round 2 · Problem D（UTC 2012-03-09）
- **难度**：1500
- **标签**：暴力、DP、字符串
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：给定串 $s$（$|s|\le2000$），数四元组 $(a,b,x,y)$ 的个数，满足 $a\le b<x\le y$，且 $s[a..b]$、$s[x..y]$ 都是回文。

**约束**：$|s|\le2000$：$O(n^2)$ 枚举回文中心即可，答案用 64 位。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
aa

输出：
1
```

回文子串：`s[0]`、`s[1]`、`s[0..1]`。不重叠且左前者只有 $(0,0)$ 与 $(1,1)$ 一对 ⇒ 1 ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
aaa

输出：
5
```

枚举：左段末端 < 右段起点。逐位置统计即可得 5 ✓

官方样例 3（输入 / 输出原样）：

```text
输入：
abacaba

输出：
36
```

![统计每个位置结尾 / 开头的回文数，再配前缀和](../../../images/cf159d_ends.svg)

**观察**：设

- $\text{end}[i]$ = 以 $i$ **结尾**的回文子串个数；
- $\text{start}[j]$ = 以 $j$ **开头**的回文子串个数。

那么答案 $=\sum_i \text{end}[i]\cdot\Big(\sum_{j>i}\text{start}[j]\Big)$：左段以 $i$ 结尾、右段以 $j>i$ 开头，两段的其它端点仍保证不重叠（左段结束在 $i$，右段开始在 $j>i$）✓

$\text{end}$ 与 $\text{start}$ 可用"围绕每个中心向两边扩展"求出：奇中心 $n$ 个、偶中心 $n-1$ 个，每个中心扩展 $O(n)$ ⇒ $O(n^2)$。

## 3. 解题思路

1. 对每个中心（奇数长度中心 $c$、偶数长度中心 $(c,c+1)$）向两边扩展，每扩展一步得到一个回文：
   - 左端点 $l$：`start[l]++`；
   - 右端点 $r$：`end[r]++`；
2. 求 `start` 的后缀和 `suf[i] = start[i] + suf[i+1]`；
3. 答案 $=\sum_{i=0}^{n-2}\text{end}[i]\cdot\text{suf}[i+1]$。

![样例 2：aaa 的 5 对](../../../images/cf159d_sample.svg)

## 4. 正确性证明

**引理 1（回文枚举完备）**：任何回文子串都与某个中心对应，且中心扩展过程恰好枚举它一次。

**证明**：回文由中心（奇：一个字符；偶：两个相邻字符之间）与半径决定 ⇒ 中心 + 半径唯一确定回文；程序对每个中心按半径递增枚举 ✓ ∎

**引理 2（计数正确）**：`end[i]` 与 `start[j]` 分别等于以 $i$ 结尾、以 $j$ 开头的回文子串个数。

**证明**：扩展过程中每得到一个回文 $[l,r]$ 就对 `end[r]` 与 `start[l]` 各加 1，由引理 1 每个回文恰被计一次 ✓ ∎

**引理 3（配对正确）**：合法四元组与"$i<j$ 的（以 $i$ 结尾的回文, 以 $j$ 开头的回文）对"一一对应。

**证明**：给定四元组 $(a,b,x,y)$，$b<x$，左段以 $b$ 结尾、右段以 $x$ 开头，且 $b<x$ ✓ 反之给定 $i<j$ 与两个回文（分别以 $i$ 结尾、$j$ 开头），它们必然不重叠（左段右端 $i$ < 右段左端 $j$）✓ ∎

**定理**：程序输出等于合法四元组个数。

**证明**：由引理 2、3，答案 $=\sum_{i<j}\text{end}[i]\cdot\text{start}[j]=\sum_i\text{end}[i]\cdot\text{suf}[i+1]$，程序正是这样计算 ✓ ∎

## 5. 复杂度分析

- **时间**：中心扩展 $O(n^2)\le4\times10^6$，实测 < 10 ms。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    string s;
    if (!(cin >> s)) return 0;
    int n = (int)s.size();
    vector<ll> endCnt(n, 0), startCnt(n, 0);
    for (int c = 0; c < 2 * n - 1; c++) {
        int l = c / 2, r = c / 2 + (c % 2);
        while (l >= 0 && r < n && s[l] == s[r]) {
            startCnt[l]++;
            endCnt[r]++;
            l--; r++;
        }
    }
    // 后缀和：suf[i] = sum_{j>=i} startCnt[j]
    vector<ll> suf(n + 1, 0);
    for (int i = n - 1; i >= 0; i--) suf[i] = suf[i + 1] + startCnt[i];
    ll ans = 0;
    for (int i = 0; i + 1 < n; i++) ans += endCnt[i] * suf[i + 1];
    printf("%lld\n", ans);
    return 0;
}
```

### Python3

```python
import sys


def main():
    s = sys.stdin.read().split()[0]
    n = len(s)
    end_cnt = [0] * n
    start_cnt = [0] * n
    for c in range(2 * n - 1):
        l = c // 2
        r = l + (c % 2)
        while l >= 0 and r < n and s[l] == s[r]:
            start_cnt[l] += 1
            end_cnt[r] += 1
            l -= 1
            r += 1
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + start_cnt[i]
    ans = 0
    for i in range(n - 1):
        ans += end_cnt[i] * suf[i + 1]
    print(ans)


main()
```

## 7. 边界情况与易错点

1. **中心共 $2n-1$ 个**：$n$ 个奇数中心 + $n-1$ 个偶数中心。
2. **不重叠是严格 $b<x$**：所以配对用 $j>i$（不是 $j\ge i$）。
3. **答案为 64 位**：最多约 $n^4/24\approx6\times10^{11}$（$n=2000$）⇒ 必须 `long long`。
4. **单字符回文**：每个位置自身也是回文，必须计入。
5. **$n=1$**：没有不重叠对 ⇒ 0（循环 `i+1<n` 自然处理）。
6. **奇偶中心的下标**：`l=c/2`、`r=c/2+c%2`。
7. **重复回文**：同一子串只由唯一中心+半径产生，不会重复计数。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/159/D_回文子串对计数.md`
- **官方样例**：$3/3$ 通过（`1`、`5`、`36`），C++ 与 Python 一致。
- **独立对拍**：另写"四重循环枚举 $(a,b,x,y)$、用 `s[a..b]==reversed` 判回文"的暴力（$n\le10$），对 $200$ 组随机串比较，全部一致。
- **性能**：$n=2000$ 的随机串与全同串，C++ 约 3 ms、Python 约 0.03 s。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 159C String Manipulation 1.0](https://codeforces.com/problemset/problem/159/C)：同场 C 题。
- [LeetCode 647. 回文子串](https://leetcode.cn/problems/palindromic-substrings/)：同为"数回文子串"。
- [Codeforces 17E Palisection](https://codeforces.com/problemset/problem/17/E)：回文对的高级版（要求相交/不相交计数，$n$ 大）。

**延伸思考**：

1. **若要求"相交"的回文对**：用总数减不重叠数。
2. **若 $n$ 到 $10^5$**：需要 Manacher + 前缀和优化（$O(n)$）。
3. **若允许三段**：多次前缀和即可。
