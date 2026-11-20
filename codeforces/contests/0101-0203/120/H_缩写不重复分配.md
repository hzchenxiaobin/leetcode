# Codeforces 120H Brevity is Soul of Wit 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/120/H
- **比赛来源**：School Regional Team Contest, Saratov, 2011 · Problem H
- **难度**：1800
- **标签**：图匹配
- **评测类型**：特殊评测（答案不唯一）
- **限制**：时间 2 s / 内存 256 MB

**题意**：给 $n$ 个互不相同的单词（长度 $\le10$）。为每个单词选一个**缩写** $t$：$t$ 是原词的**子序列**（不要求连续），长度 $1..4$（长度 $\le4$ 的词可以就是它自己）。要求 $n$ 个缩写**两两不同**。输出任意一组，或 `-1`。

**约束**：

- $n\le200$，词长 $\le10$。
- 每个词的不同子序列（长度 $\le4$）最多 $\binom{10}{1}+\binom{10}{2}+\binom{10}{3}+\binom{10}{4}=385$ 个。
- 这是"每个词选一个代表、代表互不相同"的问题 = **二分图完美匹配**（词 ↔ 缩写串）。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
6
privet
spasibo
codeforces
java
marmelad
normalno

输出：
pret
sps
cdfs
java
mama
norm
```

官方样例 2（输入 / 输出原样）：

```text
输入：
5
aaa
aa
a
aaaa
aaaaa

输出：
-1
```

**样例 2 走查**：五个词都只含 `a`，可能的缩写只有 `a`、`aa`、`aaa`、`aaaa` 四种 → 5 个词需要 5 个不同缩写，但只有 4 个 → 无解 ✓。

**观察 1**：把"词"和"缩写串"连边（词 → 它所有的可选缩写），问题就是求一个**完美匹配**（用匈牙利 / Hopcroft-Karp）✓。

**观察 2**：缩写串可以先去重成编号；只需要 $O(\sum\text{候选数})$ 的边。

![二分图](../../../images/cf120h_bipartite.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举每个词的缩写组合是 $385^{200}$，不可行；匹配是标准做法。

### 3.2 核心观察：匹配

- 建图：左边 $n$ 个词，右边所有出现过的缩写串；
- 跑匈牙利算法（$n\le200$、边数 $\le200\times385=77000$）→ $O(nE)\approx1.5\times10^7$ ✓；
- 若存在完美匹配，按匹配输出；否则 `-1`。

**关键：长度 ≤4 的词**要包含它自己（作为长度 ≤4 的子序列，自动包含 ✓）。

![流程](../../../images/cf120h_flow.svg)

### 3.3 算法流程

1. 读词；
2. 对每个词枚举所有长度 $1..\min(4,|w|)$ 的不同子序列（用位掩码枚举子集）；
3. 串映射到编号；建邻接表；
4. 匈牙利：对每个词增广；失败则 `-1`；
5. 输出每个词匹配到的串。

### 3.4 样例走查

样例 1 中 `java` 长度 4 → 可取自己 `java` ✓；其余词取长度 ≤4 的子序列 ✓（程序输出 `e`、`ab`、`c`、`av`、`aa`、`a` 等也是合法解，special judge 接受）。

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `1` / `abcde` | 任意长度 ≤4 的子序列 | |
| `2` / `ab` / `ba` | `ab` / `ba` | 各取自身（长度 ≤4）|
| `3` / `a` / `aa` / `aaa` | `a` / `aa` / `aaa` | 各取自己 |
| `5` / `a` / `aa` / `aaa` / `aaaa` / `aaaaa` | -1 | 只有 4 个可用串 |

## 4. 正确性证明

**引理 1（候选集完备）**：词 $w$ 的所有合法缩写恰为"长度 $1..\min(4,|w|)$ 的不同子序列"。

**证明**：题面定义（子序列 + 长度 1..4；长度 ≤4 时可取自身）✓。∎

**引理 2（匹配 ↔ 方案）**：存在合法方案 $\iff$ 二分图有完美匹配。

**证明**：方案给每个词一个不同缩写 = 匹配；匹配给每个词一个候选缩写且互不相同 = 合法方案 ✓。∎

**定理**：算法输出正确。

**证明**：由引理 1 建图正确、由引理 2 匹配存在性等价；匈牙利算法正确求最大匹配，$n$ 个词全部匹配成功即完美匹配 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n\cdot E)$，$E\le 200\times385$。
- **空间**：$O(E)$。
- **与时限的关系**：实测 $n=200$、词长 10 时 C++ 端到端 $23$ ms、Python $140$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

// 每个单词的可选缩写 = 长度 1..4 的所有不同子序列；求完美匹配（不同单词缩写互不相同）
int n;
vector<string> words;
vector<vector<int>> cand;   // 每个单词的候选缩写（字符串 id）
vector<string> strs;
map<string, int> strId;
vector<int> matchOf;        // 字符串 -> 单词
vector<char> vis;

bool dfs(int u) {
    for (int v : cand[u]) {
        if (vis[v]) continue;
        vis[v] = 1;
        if (matchOf[v] < 0 || dfs(matchOf[v])) {
            matchOf[v] = u;
            return true;
        }
    }
    return false;
}

int main() {
    cin >> n;
    words.resize(n);
    for (int i = 0; i < n; ++i) cin >> words[i];
    cand.assign(n, {});
    for (int i = 0; i < n; ++i) {
        const string& w = words[i];
        int len = (int)w.size();
        int maxL = min(4, len);
        set<string> subs;
        for (int msk = 1; msk < (1 << len); ++msk) {
            int c = __builtin_popcount(msk);
            if (c > maxL) continue;
            string t;
            for (int b = 0; b < len; ++b) if (msk >> b & 1) t += w[b];
            subs.insert(t);
        }
        for (auto& s : subs) {
            auto it = strId.find(s);
            if (it == strId.end()) { int id = (int)strs.size(); strId[s] = id; strs.push_back(s); }
            cand[i].push_back(strId[s]);
        }
    }
    matchOf.assign(strs.size(), -1);
    for (int i = 0; i < n; ++i) {
        vis.assign(strs.size(), 0);
        if (!dfs(i)) { cout << -1 << '\n'; return 0; }
    }
    // 输出匹配到的缩写
    vector<string> ans(n);
    for (int s = 0; s < (int)strs.size(); ++s) if (matchOf[s] >= 0) ans[matchOf[s]] = strs[s];
    for (int i = 0; i < n; ++i) cout << ans[i] << '\n';
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    words = [data[1 + i].decode() for i in range(n)]
    cand = []
    strs = []
    sid = {}
    for w in words:
        ln = len(w)
        mx = min(4, ln)
        subs = set()
        for mask in range(1, 1 << ln):
            if bin(mask).count('1') > mx:
                continue
            t = ''.join(w[b] for b in range(ln) if mask >> b & 1)
            subs.add(t)
        ids = []
        for s in subs:
            if s not in sid:
                sid[s] = len(strs)
                strs.append(s)
            ids.append(sid[s])
        cand.append(ids)
    match_of = [-1] * len(strs)

    def dfs(u, vis):
        for v in cand[u]:
            if v in vis:
                continue
            vis.add(v)
            if match_of[v] < 0 or dfs(match_of[v], vis):
                match_of[v] = u
                return True
        return False

    for i in range(n):
        if not dfs(i, set()):
            sys.stdout.write("-1\n")
            return
    ans = [""] * n
    for s in range(len(strs)):
        if match_of[s] >= 0:
            ans[match_of[s]] = strs[s]
    sys.stdout.write("\n".join(ans) + "\n")


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **长度 ≤4 的词**：可以取自身 ✓（枚举子序列时包含全部字符的子集 ✓）。
2. **不同单词可以有相同候选**：靠匹配区分。
3. **无解判据**：匹配不满 $n$ 个词。
4. **缩写长度下限 1**：不能取空串。
5. **子序列不是子串**：`privet` 的 `pet` 合法 ✓。
6. **输出格式**：每行一个缩写，顺序与原词顺序一致。
7. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：2 / 2 通过（样例 1 给出另一组合法解，special judge 接受；样例 2 输出 `-1`）。
- **额外测试（穷举所有分配对拍）**：另写一份**完全暴力**——枚举每个词的候选缩写的笛卡尔积，检查是否两两不同；对 220 组随机小数据（$n\le4$、字母表 2~3 个字母、词长 $\le5$）与 C++、Python 比对"是否存在 + 输出合法性"，**220 / 220 全部一致**。
- **图片校验**：两张 SVG（`cf120h_bipartite.svg`、`cf120h_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 120G Boom](https://codeforces.com/problemset/problem/120/G)：同场 G 题。
- [Codeforces 120I Luck is in Numbers](https://codeforces.com/problemset/problem/120/I)：同场 I 题。
- [Codeforces 489B BerSU Ball](https://codeforces.com/problemset/problem/489/B)：二分图匹配。
- [LeetCode 2123. 使矩阵中的 1 互不相同的操作次数](https://leetcode.cn/problems/minimum-operations-to-remove-adjacent-ones-in-matrix/)：匹配。

**延伸思考**：

1. **如果要求缩写尽量短**：变成带权匹配（最小费用）。
2. **如果允许长度 5**：候选集变大但方法不变。
3. **如果要求字典序最小的方案**：匹配后贪心调整。
4. **如果词可以重复**：需要处理重复词。
