# Codeforces 144C Anagram Search 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/144/C
- **比赛来源**：Codeforces Round 103 (Div. 2) · Problem C
- **难度**：1500
- **标签**：字符串、滑动窗口
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给 $s$（含小写字母与 `?`）和 $p$（只含小写字母）。称 $s$ 的一个长度 $|p|$ 的子串"好"，当且仅当把其中的 `?` 各换成某个字母后，能成为 $p$ 的**变位词**（同字母多重集）。求好子串个数（按出现位置计）。

**约束**：

- $|s|,|p|\le10^5$；$|p|$ 可大于 $|s|$（此时答案 0）✓。
- `?` 可任意替换，每个独立 ✓。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
bb??x???
aab

输出：
2
```

官方样例 2（输入 / 输出原样）：

```text
输入：
ab?c
acb

输出：
2
```

**样例 2 走查**：窗口长 3：`ab?` → 已有 a,b，`?`→c ✓；`b?c` → 已有 b,c，`?`→a ✓ → 2 ✓。

**样例 1 走查**：长 3 的窗口共 6 个：`bb?`（两个 b，p 只要 1 个 b ✗）、`b??`（b ✓，两个 `?` 填 a,a ✓）、`??x`（含 x ✗）、`?x?` ✗、`x??` ✗、`???`（可填 a,a,b ✓）→ 2 ✓。

**观察**：窗口好 $\iff$ 对每个字母 $c$：`窗口里 c 的个数 ≤ p 中 c 的个数` ✓（`?` 填剩下的空位，个数自动吻合，因为窗口长度 = $|p|$）✓。

![窗口](../../../images/cf144c_window.svg)

## 3. 解题思路

滑动窗口 + 维护"超量字母种类数" `bad`：

- 加入/移除一个字母 $c$ 时，只需看 `cnt[c] > need[c]` 是否跨越边界，$O(1)$ 更新 `bad` ✓；
- `bad == 0` 的窗口计数 ✓。

![流程](../../../images/cf144c_flow.svg)

### 3.4 样例走查

见 2 节 ✓。自造样例（标注"自造"）：`a?` / `a` → 2（`a` 与 `?`→`a`）；`a` / `ab` → 0；`abc` / `cba` → 1。

## 4. 正确性证明

**引理 1**：窗口（含 $q$ 个 `?`）可变成 $p$ 的变位词 $\iff$ 对每个 $c$，`cnt_c ≤ need_c`。

**证明**：(⇐) 需填的空位 $=m-\sum_c cnt_c$，而 $\sum_c need_c=m$，故 $\sum_c(need_c-cnt_c)=$ 空位数 ✓，按差值逐字母填即可 ✓。(⇒) 若某 `cnt_c>need_c`，无论怎么填 `?` 都会多出 $c$ ✗。∎

**引理 2**：滑动窗口的 `bad` 计数正确维护。

**证明**：`bad` = 满足 `cnt_c>need_c` 的字母种数；单字母增减只影响该字母的布尔值，增量式更新准确 ✓。∎

**定理**：算法计数正确。

**证明**：逐窗口判据由引理 1，状态维护由引理 2 ✓。∎

## 5. 复杂度分析

- **时间**：$O(|s|+|p|)$。
- **空间**：$O(1)$（26 个桶）。
- **与时限的关系**：实测 $|s|=10^5$ 约 $5$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, p;
    if (!(cin >> s >> p)) return 0;
    int n = (int)s.size(), m = (int)p.size();
    if (m > n) { cout << 0 << '\n'; return 0; }
    int need[26] = {0};
    for (char c : p) need[c - 'a']++;
    int cnt[26] = {0};
    int bad = 0;        // 有多少字母"窗口里多于 p 中"
    auto addBad = [&](int c, int delta) {
        // 只在跨过 need 的边界时更新 bad
        int before = (cnt[c] > need[c]);
        cnt[c] += delta;
        int after = (cnt[c] > need[c]);
        bad += after - before;
    };
    for (int i = 0; i < m; ++i) if (s[i] != '?') addBad(s[i] - 'a', 1);
    int ans = (bad == 0);
    for (int i = m; i < n; ++i) {
        if (s[i - m] != '?') addBad(s[i - m] - 'a', -1);
        if (s[i] != '?') addBad(s[i] - 'a', 1);
        if (bad == 0) ++ans;
    }
    cout << ans << '\n';
    return 0;
}
```

### Python3

```python
import sys
from collections import Counter


def main() -> None:
    data = sys.stdin.buffer.read().split()
    s = data[0].decode()
    p = data[1].decode()
    n, m = len(s), len(p)
    if m > n:
        print(0)
        return
    need = Counter(p)
    cnt = Counter()
    for ch in s[:m]:
        if ch != '?':
            cnt[ch] += 1
    bad = sum(1 for c in cnt if cnt[c] > need[c])
    ans = 1 if bad == 0 else 0
    for i in range(m, n):
        out = s[i - m]
        if out != '?':
            c = out
            before = cnt[c] > need[c]
            cnt[c] -= 1
            after = cnt[c] > need[c]
            bad += after - before
        inc = s[i]
        if inc != '?':
            c = inc
            before = cnt[c] > need[c]
            cnt[c] += 1
            after = cnt[c] > need[c]
            bad += after - before
        if bad == 0:
            ans += 1
    print(ans)


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **$|p|>|s|$**：答案 0。
2. **`?` 不参与计数**：只统计真实字母。
3. **`bad` 的增量更新**：必须比较更新前后的布尔值。
4. **窗口长度固定为 $|p|$** ✓。
5. **字母表 26** ✓。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：2 / 2 通过。
- **额外测试**：220 组随机串（窗口长度 1–5、字母表 `ab`）与"逐窗口重建计数"的暴力比对，C++/Python 共 **440 次运行全部一致**。
- **图片校验**：两张 SVG（`cf144c_window.svg`、`cf144c_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 144B Meeting](https://codeforces.com/problemset/problem/144/B)：同场 B 题。
- [Codeforces 145A Lucky Conversion](https://codeforces.com/problemset/problem/145/A)：同批次。
- [LeetCode 438. 找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)：滑动窗口计数。
- [LeetCode 567. 字符串的排列](https://leetcode.cn/problems/permutation-in-string/)：同型。

**延伸思考**：

1. **如果 `?` 必须换成不同字母**：判据变复杂。
2. **如果要求输出所有位置**：记录下标即可。
3. **如果字母表更大**：用哈希表。
4. **如果 $|p|$ 变化**：改成多重窗口。
