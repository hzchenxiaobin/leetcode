# Codeforces 101A 最少保留的不同字母 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/101/A
- **比赛来源**：Codeforces Beta Round 79 (Div. 1 Only) · Problem A（UTC 2011-08-03）
- **难度**：1200
- **标签**：贪心、排序、字符串
- **评测类型**：普通（输出任意合法方案）
- **限制**：时间 2 s / 内存 256 MB

**题意**：给出长度 $n$ 的小写字符串与整数 $k$。可以删去不超过 $k$ 个字符（删哪些位置都行，剩下的保持原顺序，即得到原串的一个子序列）。求删完后**不同字母数最少**能是多少（记作 $m$），并输出任意一个达到 $m$ 的剩余字符串。注意要求剩下的字符串恰好含有 $m$ 种不同字母。

**约束**：

- $1 \le n \le 10^5$，$0 \le k \le 10^5$：$O(n + 26\log 26)$ 即可。
- 字母表只有 $26$ 个字母：可以按"字符类"整体删除。
- 至少保证存在合法输出（例如 $m=0$ 时输出空串，见样例三）。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
aaaaa
4
输出：
1
aaaaa
```

官方样例二：

```text
输入：
abacaba
4
输出：
1
aaaa
```

官方样例三：

```text
输入：
abcdefgh
10
输出：
0

```

**样例一走查**：只有 `a` 一种字母，共 $5$ 个。删掉全部 $a$ 需要 $5 > 4$，做不到；所以至少保留一种字母，$m=1$，输出原串（"删 $0$ 个"也满足"不超过 $k$ 个"）。

**样例二走查**：`abacaba` 中 `a` 出现 $4$ 次、`b` 出现 $2$ 次、`c` 出现 $1$ 次。用 $4$ 次预算：先删 `c`（花 $1$，剩 $3$）、再删 `b`（花 $2$，剩 $1$），此时只剩 `a`，$m=1$，输出 `aaaa`。

**样例三走查**：$8$ 种字母各出现 $1$ 次，$k=10 \ge 8$，可以把所有字母都删光，$m=0$，输出空行。

![按出现次数从小到大删](../../../images/cf101a_cases.svg)

**观察**：要减少"不同字母数"，只能把某个字母**全部**删掉（删一半不减少种类数）。删掉字母 $c$ 的代价就是它的出现次数 $\text{cnt}[c]$。所以问题是：在总代价 $\le k$ 的前提下，最多能删掉多少个"字母类"。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举"保留哪些字母类"：$2^{26}$ 种，虽然 $6.7\times10^7$ 在极限上勉强可行，但完全没必要——因为删掉一个类只花 $\text{cnt}[c]$，要让删掉的类数最多，显然优先删代价最小的类。

### 3.2 核心观察：贪心按次数升序删

![样例 2 的过滤结果](../../../images/cf101a_sample.svg)

把出现过的小写字母按出现次数升序排列，依次尝试"整类删除"：若当前剩余预算 $\ge \text{cnt}[c]$，就删掉并扣减预算；否则停止（后面的类次数都不比它小，更删不起）。

剩下的字母类数就是 $m$；输出时把原串中属于被删类的字符全部滤掉（这样天然是子序列，且恰好含 $m$ 种字母）。

**为什么停止是安全的**：若当前类删不起（$\text{cnt}[c] > k_{\text{剩}}$），那么所有次数 $\ge \text{cnt}[c]$ 的类都删不起，继续尝试没有意义；而"跳过它去删更贵的类"只会更差。

### 3.3 算法流程

1. 统计每种字母的出现次数；
2. 把出现过的字母按次数升序排序；
3. 依次尝试整类删除，能删就删并扣预算；
4. $m$ = 未被删除的类数；输出 $m$，再输出原串过滤后的结果。

### 3.4 样例走查

| 样例 | 次数分布 | 删除过程 | $m$ | 输出 |
|---|---|---|---|---|
| 1 | a:5 | a 要 5 > 4，删不动 | 1 | `aaaaa` |
| 2 | c:1, b:2, a:4 | 删 c（剩 3）→ 删 b（剩 1）→ a 要 4 > 1 停 | 1 | `aaaa` |
| 3 | 8 个字母各 1 | 8 个全删（8 ≤ 10） | 0 | 空串 |

## 4. 正确性证明

**引理 1**：一个字母类要么全删、要么一个都不删；只删一部分不会减少"不同字母数"。

**证明**：不同字母数由"至少出现一次"的字母决定；某类只要还剩一个字符，它就仍被计入。∎

**引理 2**：若删掉的字母类集合为 $S$，所需删除字符数恰为 $\sum_{c\in S}\text{cnt}[c]$，且与删除顺序无关。

**证明**：由引理 1，删除每个类的全部字符，总数就是各类次数之和。∎

**引理 3（贪心最优化）**：把各类按次数升序 $c_1, c_2, \dots, c_t$ 排列，贪心"能删就删"得到的删除类数不少于任何其它可行方案。

**证明**：设贪心删了前 $q$ 类（$c_{q+1}$ 删不起，即 $\sum_{i\le q} c_i \le k < \sum_{i\le q+1} c_i$）。任何方案若删了 $r$ 个类，其代价至少是"次数最小的 $r$ 个类之和" $\sum_{i\le r}c_i$（排序不等式：$r$ 个数的和 ≥ 最小的 $r$ 个数之和）。若 $r > q$，则代价 $\ge \sum_{i\le q+1}c_i > k$，不可行。故 $r \le q$，贪心最优。∎

**定理**：算法输出的 $m$ 是最小可能的不同字母数，输出串是合法方案。

**证明**：最少不同字母数 $= 26$ 中出现的类数 $- $ 最多能删的类数，由引理 3 贪心取到最大删除数；输出串由原串滤掉被删类得到，是子序列、恰好含 $m$ 种字母、删除字符数 $= \sum_{c\in S}\text{cnt}[c] \le k$。∎

## 5. 复杂度分析

- **时间**：统计 $O(n)$ + 排序 $O(26\log 26)$ + 输出 $O(n)$。
- **空间**：$O(n)$ 存字符串，计数 $O(26)$。
- **数值范围**：全部是 $10^5$ 级整数，`int` 足够。
- **与时限的关系**：2 s 下实测约 $15$ ms（C++），Python 约 $34$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (!(cin >> s)) return 0;
    int k;
    if (!(cin >> k)) return 0;
    int cnt[26] = {0};
    for (char c : s) cnt[c - 'a']++;
    vector<int> order;
    for (int c = 0; c < 26; ++c) if (cnt[c]) order.push_back(c);
    sort(order.begin(), order.end(), [&](int x, int y) { return cnt[x] < cnt[y]; });
    bool alive[26];
    for (int c = 0; c < 26; ++c) alive[c] = cnt[c] > 0;
    for (int c : order) {
        if (cnt[c] <= k) { k -= cnt[c]; alive[c] = false; }
        else break;
    }
    int m = 0;
    for (int c = 0; c < 26; ++c) if (alive[c]) ++m;
    string out;
    for (char c : s) if (alive[c - 'a']) out.push_back(c);
    printf("%d\n%s\n", m, out.c_str());
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
    k = int(data[1])
    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - 97] += 1
    order = sorted((c for c in range(26) if cnt[c]), key=lambda c: cnt[c])
    alive = [cnt[c] > 0 for c in range(26)]
    for c in order:
        if cnt[c] <= k:
            k -= cnt[c]
            alive[c] = False
        else:
            break
    m = sum(1 for c in range(26) if alive[c])
    out = "".join(ch for ch in s if alive[ord(ch) - 97])
    sys.stdout.write("%d\n%s\n" % (m, out))


main()
```

## 7. 边界情况与易错点

1. **必须整类删除**：只删某个字母的一部分不会减少种类数，反而浪费预算；样例二若只删两个 `a` 会得到 $m=2$，不是最优。
2. **"不超过 $k$"而非"恰好"**：可以一个都不删（样例一），所以预算有剩没关系。
3. **输出空串的情况**：$m=0$ 时要输出一个空行（样例三）；用 `printf("%d\n%s\n", 0, "")` 正好得到 `0` 加空行。
4. **输出的字符串必须恰好含 $m$ 种字母**：滤掉被删类即可；不要额外去重或重排，否则可能不再是子序列。
5. **$k=0$**：一个都删不了，$m$ 就是原串的不同字母数，输出原串。
6. **剩余预算刚好等于某类次数**：要删（条件用 `cnt[c] <= k`），用 `<` 会少删一类。
7. **次数相同的情况**：任意顺序都可，贪心结论与顺序无关（引理 3 的最优性只依赖"最小的 $r$ 个之和"）。
8. **字母表固定 26 个**：用数组而非 `map`，常数更小。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：3 / 3 通过（`1/aaaaa`、`1/aaaa`、`0/空行`），C++ 与 Python 输出一致。
- **独立暴力对拍**：暴力枚举"保留哪些字母类"的全部子集（$2^{|\Sigma|}$，$\Sigma$ 为出现过的字母），检查删除代价 $\le k$ 并取最小类数；另外校验输出串是子序列、恰含 $m$ 种字母、删除数 $\le k$。对 $n \le 14$、字母表大小 $1\sim5$ 的 **320 组**随机数据，参考 C++、参考 Python 与暴力三方一致，**0 失败**。
- **最大约束性能**：$n = 10^5$、$k = 5\times10^4$ 时 C++ 端到端约 $15$ ms，Python 约 $34$ ms；相对 2 s 余量在百倍以上。
- **图片校验**：`cf101a_cases.svg`、`cf101a_sample.svg` 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写体字体族，文本包围盒未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError`）渲染无报错；无 `---` 分隔线。
- **复核状态**：verified（样例、对拍、性能、图片、公式均实跑通过）。

## 相关题目与扩展

- [Codeforces 101B Buses](https://codeforces.com/problemset/problem/101/B)、[101C Vectors](https://codeforces.com/problemset/problem/101/C)、[101D Castle](https://codeforces.com/problemset/problem/101/D)、[101E Candies and Stones](https://codeforces.com/problemset/problem/101/E)：同场其余题。
- [Codeforces 102B Sum of Digits](https://codeforces.com/problemset/problem/102/B)：同轮 Div.2 的 B 题。
- [Codeforces 101A 同类练习 1104B Game with string](https://codeforces.com/problemset/problem/1104/B)：按字符频次贪心。
- [LeetCode 1647. 字符频次唯一的最小删除次数](https://leetcode.cn/problems/minimum-deletions-to-make-character-frequencies-unique/)：同样是"按频次处理字符类"的贪心。

**延伸思考**：

1. **如果要求"恰好删 $k$ 个"**：贪心停止后可能还要多删一些字符（但不能再整类删），需要另作处理，答案的 $m$ 可能不变。
2. **如果代价不是字符次数而是别的（如每个字符 1 分）**：问题变成"选字母类的背包"，贪心不再成立。
3. **如果要求输出字典序最小的剩余串**：在 $m$ 最优的前提下还要选保留哪些类、删哪些位置，需要额外的最优化（可用后缀自动机/贪心）。
4. **如果字母表是 $10^5$ 种字符**：把数组换成哈希表 + 排序，复杂度仍是 $O(n\log n)$。

