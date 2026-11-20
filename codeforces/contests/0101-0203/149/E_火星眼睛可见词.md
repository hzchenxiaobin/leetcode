# Codeforces 149E 火星眼睛可见词 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/149/E
- **比赛来源**：Codeforces Round 106 (Div. 2) · Problem E（UTC 2012-02-10）
- **难度**：2300
- **标签**：字符串、KMP/Z 函数
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给定串 $s$（$|s|\le10^5$）与 $m$ 个互不相同的"美丽词" $p_i$（$m\le100$，$|p_i|\le1000$）。火星人可以打开两段**不重叠**的连续眼睛（左段在前、右段在后），把看到的字符按顺序连成一个词。问有多少个美丽词能被这样看到（即 $p_i$ 可以拆成 $p_i[0..k-1]+p_i[k..]$ 两段，第一段是 $s$ 的某子串、第二段出现在它后面且不重叠）。

**约束**：

- $|s|$ 大、$m$ 小、$|p_i|$ 中等：对每个词做一次 $O(|s|+|p|)$ 的匹配即可，总 $O(m(|s|+|p|))\le1.1\times10^7$。
- 两段都必须**非空**且不重叠。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
ABCBABA
2
BAAB
ABBA

输出：
1
```

- `ABBA`：拆成 `AB` + `BA`；`AB` 出现在 $s[0..1]$，`BA` 出现在 $s[3..4]$（或 $s[5..6]$），不重叠 ⇒ 可见 ✓
- `BAAB`：唯一可能的前缀 `BA` 最早结束于 $s[4]$，而后缀 `AB` 最晚开始于 $s[4]$ ⇒ 重叠，不可见 ✗

所以答案是 1 ✓

![前缀的最早结束位置 vs 后缀的最晚开始位置](../../../images/cf149e_split.svg)

**观察**：对一个固定的拆分 $p=p_1+p_2$，条件等价于

$$\min_{\text{occurrence of }p_1}\text{end} < \max_{\text{occurrence of }p_2}\text{start}.$$

即"$p_1$ 的最早结束位置"严格小于"$p_2$ 的最晚开始位置"。只要这两个极值之一存在且满足不等式，就有合法的两段。

- **最早结束位置**：用 KMP 扫描 $s$，记录"每个前缀长度 $l$ 匹配结束时 $s$ 的下标"，再取后缀最小值即可（长度 $l$ 的匹配蕴含长度 $k<l$ 的前缀在前面的位置结束）。
- **最晚开始位置**：把 $s$ 与 $p$ 都反转，用同样的方法求"反转后的最早结束位置"，再由 $n-1-e$ 换回原串的**开始**位置（反转后"最早结束"对应原串"最晚开始"）。

## 3. 解题思路

1. 对每个 $p$：
   - 计算 `pre[k]`（$k=1..|p|$）= 前缀 $p[0..k-1]$ 在 $s$ 中的**最小结束下标**；
   - 计算 `suf[j]` = 后缀 $p[|p|-j..|p|-1]$ 在 $s$ 中的**最大开始下标**；
2. 枚举拆分点 $k=1..|p|-1$（两段都非空）：若 `pre[k] < suf[|p|-k]` 则可见；
3. 统计可见的词数。

**`pre` 的求法**（KMP）：
- 求出 $p$ 的前缀函数 $\pi$；
- 用 $\pi$ 在 $s$ 上做匹配，维护当前匹配长度 $l$；每次匹配到长度 $l$ 结束时记录 `best[l] = min(best[l], i)`；
- 长度 $l$ 的匹配也说明前缀 $k$（$k\le l$）在 $i-(l-k)$ 处结束，所以
  $$\text{pre}[k]=k+\min_{l\ge k}\big(\text{best}[l]-l\big).$$

![样例：ABBA 可见、BAAB 重叠](../../../images/cf149e_sample.svg)

## 4. 正确性证明

**引理 1（拆分判据）**：固定拆分 $p=p_1+p_2$（两段非空），存在两段不重叠的可见区域当且仅当 $\min\text{end}(p_1)<\max\text{start}(p_2)$。

**证明**：若存在区间 $[a,b]$、$[c,d]$（$b<c$）使 $s[a..b]=p_1$、$s[c..d]=p_2$，则 $\min\text{end}\le b<c\le\max\text{start}$，故不等式成立。反之，取达到 $\min\text{end}$ 的出现与达到 $\max\text{start}$ 的出现，由不等式可知前者的结束位置严格小于后者的开始位置，两段不重叠。∎

**引理 2（`pre` 计算正确）**：$\text{pre}[k]=k+\min_{l\ge k}(\text{best}[l]-l)$。

**证明**：若 $p[0..l-1]$ 在 $s$ 中结束于 $i$，则对任意 $k\le l$，$p[0..k-1]$ 结束于 $i-(l-k)$。因此 $\text{pre}[k]\le\min_{l\ge k}(\text{best}[l]-(l-k))$。反向：任何 $p[0..k-1]$ 的出现都对应某个 $l\ge k$ 的匹配（取 $l=k$ 即可，$\text{best}[k]$ 记录了它），故等号可以取到。∎

**引理 3（`suf` 计算正确）**：把 $s,p$ 同时反转后按引理 2 求出的 $\text{pre}^{\text{rev}}[j]$，对应原串中后缀的最晚开始位置 $n-1-\text{pre}^{\text{rev}}[j]$。

**证明**：反转后位置 $e$ 对应原位置 $n-1-e$；反转后"前缀结束于 $e$"意味着原串"后缀开始于 $n-1-e$"，最小 $e$ 对应最大开始位置。∎

**定理**：程序统计的词数正确。

**证明**：由引理 1，对每个拆分只需比较两个极值；由引理 2、3，极值计算正确。程序枚举全部 $|p|-1$ 个拆分，只要有一个满足就计数，恰好等于"存在合法可见方式"的词数。∎

## 5. 复杂度分析

- **时间**：每个词 $O(|s|+|p|)$ 做两次 KMP，总 $O(m(|s|+|p|))\le1.1\times10^7$；实测 C++ 约 0.14 s，Python 约 3.2 s。
- **空间**：$O(|s|+|p|)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
static const int INF = 1e9;

// 返回 res[k] = pat 的前缀 pat[0..k-1] 在 text 中出现的「最小结束位置」（0 基，k>=1）
static vector<int> minEndOfPrefixes(const string &text, const string &pat) {
    int n = (int)text.size(), m = (int)pat.size();
    vector<int> pi(m, 0);
    for (int i = 1; i < m; i++) {
        int j = pi[i - 1];
        while (j > 0 && pat[i] != pat[j]) j = pi[j - 1];
        if (pat[i] == pat[j]) j++;
        pi[i] = j;
    }
    vector<int> best(m + 1, INF);
    int len = 0;
    for (int i = 0; i < n; i++) {
        while (len > 0 && text[i] != pat[len]) len = pi[len - 1];
        if (text[i] == pat[len]) len++;
        if (len > 0 && i < best[len]) best[len] = i;   // 长度 len 的前缀在 i 结束
        if (len == m) len = pi[len - 1];
    }
    // res[k] = min_{l>=k} (best[l] - (l - k)) = k + min_{l>=k} (best[l] - l)
    vector<int> b2(m + 2, INF);
    for (int l = 1; l <= m; l++) if (best[l] < INF) b2[l] = best[l] - l;
    for (int l = m - 1; l >= 1; l--) b2[l] = min(b2[l], b2[l + 1]);
    vector<int> res(m + 1, INF);
    for (int k = 1; k <= m; k++) if (b2[k] < INF) res[k] = b2[k] + k;
    return res;
}

int main() {
    string s;
    if (!(cin >> s)) return 0;
    int m;
    cin >> m;
    string rs = s;
    reverse(rs.begin(), rs.end());
    int answer = 0;
    for (int t = 0; t < m; t++) {
        string p;
        cin >> p;
        int len = (int)p.size();
        if (len < 2) continue;
        vector<int> pre = minEndOfPrefixes(s, p);
        string rp = p;
        reverse(rp.begin(), rp.end());
        vector<int> suf = minEndOfPrefixes(rs, rp);
        bool ok = false;
        for (int k = 1; k < len && !ok; k++) {
            int j = len - k;                                   // 后缀长度
            if (pre[k] >= INF || suf[j] >= INF) continue;
            int startSuffix = (int)s.size() - 1 - suf[j];      // 0 基开始位置
            if (pre[k] < startSuffix) ok = true;
        }
        if (ok) answer++;
    }
    printf("%d\n", answer);
    return 0;
}
```

### Python3

```python
import sys

INF = 10 ** 9


def min_end_of_prefixes(text, pat):
    """res[k] = pat 的前缀 pat[0..k-1] 在 text 中出现的最小结束位置（0 基）"""
    n, m = len(text), len(pat)
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and pat[i] != pat[j]:
            j = pi[j - 1]
        if pat[i] == pat[j]:
            j += 1
        pi[i] = j
    best = [INF] * (m + 1)
    length = 0
    for i in range(n):
        while length > 0 and text[i] != pat[length]:
            length = pi[length - 1]
        if text[i] == pat[length]:
            length += 1
        if length > 0 and i < best[length]:
            best[length] = i
        if length == m:
            length = pi[length - 1]
    # res[k] = min_{l>=k} (best[l] - (l - k)) = k + min_{l>=k} (best[l] - l)
    b2 = [INF] * (m + 2)
    for l in range(1, m + 1):
        if best[l] < INF:
            b2[l] = best[l] - l
    for l in range(m - 1, 0, -1):
        if b2[l + 1] < b2[l]:
            b2[l] = b2[l + 1]
    return [INF] + [b2[k] + k if b2[k] < INF else INF for k in range(1, m + 1)]


def main():
    data = sys.stdin.read().split()
    s = data[0]
    m = int(data[1])
    rs = s[::-1]
    n = len(s)
    answer = 0
    for t in range(m):
        p = data[2 + t]
        L = len(p)
        if L < 2:
            continue
        pre = min_end_of_prefixes(s, p)
        suf = min_end_of_prefixes(rs, p[::-1])
        for k in range(1, L):
            j = L - k
            if pre[k] >= INF or suf[j] >= INF:
                continue
            if pre[k] < n - 1 - suf[j]:
                answer += 1
                break
    print(answer)


main()
```

## 7. 边界情况与易错点

1. **两段都必须非空**：$k$ 从 1 到 $|p|-1$，不能取 0 或 $|p|$（那等于"一段就是整个词"）。
2. **不重叠**：要求 `end_1 < start_2`（严格小于），等于就是重叠（样例的 `BAAB` 正是这种情形）。
3. **极值不足**：`pre[k]` 或 `suf[j]` 不存在（INF）时该拆分不可行。
4. **反转映射**：原串位置 $=n-1-e$；漏掉 `-1` 会整体偏移一位。
5. **KMP 的 `len == m` 复位**：匹配到整词后要退到 $\pi[m-1]$ 继续，否则会漏后续匹配。
6. **$|p|=1$**：不可能拆成两段非空 ⇒ 一定不可见（代码直接跳过）。
7. **$m$ 个词互不相同**：不需要去重。
8. **大小写**：题目只有大写字母，KMP 直接比较字符即可。
9. **Python 性能**：$m=100$、$|s|=10^5$ 时约 3 s（纯 Python），建议 PyPy3/C++。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/149/E_火星眼睛可见词.md`
- **官方样例**：$1/1$ 通过（`1`），C++ 与 Python 一致。
- **独立对拍**：另写"对每个词枚举拆分点、用 Python 的 `str.find` 逐个找出现位置"的暴力，对 $200$ 组随机（$|s|\le14$、字母表 `{A,B}`、$m\le4$、$|p|\le5$）比较，全部一致。
- **性能**：$|s|=10^5$、$m=100$、$|p|=1000$ 的随机数据，C++ 约 0.14 s、Python 约 3.2 s。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 149D Coloring Brackets](https://codeforces.com/problemset/problem/149/D)：同场 D 题。
- [Codeforces 126B Password](https://codeforces.com/problemset/problem/126/B)：前缀函数应用。
- [LeetCode 28. 找出字符串中第一个匹配项的下标](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)：KMP 入门。

**延伸思考**：

1. **若允许三段**：需要"两段前缀 + 后缀"的中间极值，思路类似但要多一层。
2. **若 $|p_i|$ 到 $10^5$**：仍可 $O(|s|+|p|)$；若 $m$ 也到 $10^5$，需要 AC 自动机/后缀结构。
3. **若要求输出具体区间**：记录达到极值的匹配位置即可。
