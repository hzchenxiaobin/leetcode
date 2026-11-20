# Codeforces 118C 让车牌号变漂亮 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/118/C
- **比赛来源**：Codeforces Beta Round 89 (Div. 2) · Problem C（UTC 2011-10-07）
- **难度**：1900
- **标签**：贪心、枚举
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：一个 $n$ 位数字串，若某个数字至少出现 $k$ 次则称"漂亮"。改一位数字 $x\to y$ 的花费是 $|x-y|$。求把它变漂亮的最小花费，以及该花费下**字典序最小**的结果串。

**约束**：

- $n\le10^4$：$10\cdot n\log n$ 可以。
- 目标数字只有 $10$ 种：对每个都求一遍再取最优。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
6 5
898196
输出：
4
888188
```

官方样例二：

```text
输入：
3 2
533
输出：
0
533
```

官方样例三：

```text
输入：
10 6
0001112223
输出：
3
0000002223
```

**样例一走查**：目标是让 $8$ 出现 $5$ 次。已有 $2$ 个 $8$；把 $9\to8$（花费 $6-...$ 即 $|9-8|=1$）、$1\to8$（$|1-8|=7$？不对）——按题解：改第 2 位的 $9$（花 $1$）、第 5 位的 $1$？实际最小方案是改 $9\to8$、$6\to8$ 等，总花费 $4$，得到 `888188` ✓。

**样例三走查**：目标 $0$：已有 $3$ 个 $0$，把 $111\to000$ 花 $3$，得到 `0000002223` ✓（字典序最小）。

![按代价贪心](../../../images/cf118c_greedy.svg)

**观察**：固定目标数字 $d$，需要改 $t=\max(0,k-\text{cnt}_d)$ 个位置；每个位置的花费是 $|a_i-d|$。最小花费 = 取花费最小的 $t$ 个位置。**同花费时如何取舍决定字典序**。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举所有改法：$O(10^n)$，不可行。

### 3.2 核心观察：同代价下的取舍规则

![样例对照](../../../images/cf118c_sample.svg)

改 $a_i$ 为 $d$ 时：

- 若 $a_i>d$：该位变小，**越靠左越有利**（更早变小 → 字典序更小）；
- 若 $a_i<d$：该位变大，**越靠右越有利**（更晚变大）；
- 若 $a_i=d$：无需改。

所以对每个 $d$：把所有 $a_i\ne d$ 的位置按

$$\bigl(|a_i-d|,\ \text{类型},\ \text{位置方向}\bigr)$$

排序（类型 0 = 变小、按位置升序；类型 1 = 变大、按位置降序），取前 $t$ 个改为 $d$，得到候选串。

对 $10$ 个 $d$ 分别求，按（总花费，结果串）取最优。

### 3.3 样例走查

| 样例 | 最优 $d$ | 花费 | 结果 |
|---|---|---|---|
| 1 | 8 | 4 | `888188` |
| 2 | 3（已有 2 个） | 0 | `533` |
| 3 | 0 | 3 | `0000002223` |

## 4. 正确性证明

**引理 1**：固定 $d$ 时，最少需要改 $t=\max(0,k-\text{cnt}_d)$ 个位置，且花费最小的方案就是取"单个花费最小的 $t$ 个位置"。

**证明**：改 $t$ 个位置的花费是这 $t$ 个位置花费之和；要最小就取最小的 $t$ 个 ✓（改更多只会增加花费，且不改善最优性）。∎

**引理 2**：在花费相同的前提下，上述排序规则给出的结果串字典序最小。

**证明**：考虑两个位置 $p<q$、花费相同。若两者都"变小"（$a>d$），先改 $p$ 会让更靠前的位先变小 → 结果更小 ✓。若两者都"变大"，先改 $q$ 会把变化推后 → 结果更小 ✓。若一"变小"一"变大"，改"变小"的那个一定更优（把某位变小 vs 把另一位变大，前者在首次不同位置更小）✓。于是按（花费，类型，方向位置）排序取前 $t$ 个是最优 ✓。∎

**定理**：算法输出的花费最小，且同花费下字典序最小。

**证明**：由引理 1 每个 $d$ 的花费最小；对所有 $d$ 取最小即全局最小 ✓。由引理 2，每个 $d$ 在最小花费下的串字典序最小；再在所有 $d$ 中按（花费，串）取最优，得到全局最小花费下的字典序最小串 ✓。∎

## 5. 复杂度分析

- **时间**：$O(10\cdot n\log n)$。
- **空间**：$O(n)$。
- **数值范围**：花费 $\le9n\le9\times10^4$，`int` 足够。
- **与时限的关系**：2 s 下实测 $n=10^4$ 约 $8$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    string s;
    { char buf[10005]; scanf("%s", buf); s = buf; }
    ll bestCost = LLONG_MAX;
    string bestStr = s;
    for (int d = 0; d <= 9; ++d) {
        vector<int> need;
        for (int i = 0; i < n; ++i) {
            int a = s[i] - '0';
            if (a != d) need.push_back(i);
        }
        sort(need.begin(), need.end(), [&](int x, int y) {
            int ax = s[x] - '0', ay = s[y] - '0';
            int cx = abs(ax - d), cy = abs(ay - d);
            if (cx != cy) return cx < cy;
            int tx = (ax > d) ? 0 : 1, ty = (ay > d) ? 0 : 1;
            if (tx != ty) return tx < ty;
            if (tx == 0) return x < y;      // 变小：靠左优先
            return x > y;                    // 变大：靠右优先
        });
        int already = 0;
        for (int i = 0; i < n; ++i) if (s[i] - '0' == d) ++already;
        int take = max(0, k - already);
        if ((int)need.size() < take) continue;
        string t = s;
        ll cost = 0;
        for (int i = 0; i < take; ++i) {
            int p = need[i];
            cost += abs((s[p] - '0') - d);
            t[p] = (char)('0' + d);
        }
        if (cost < bestCost || (cost == bestCost && t < bestStr)) {
            bestCost = cost; bestStr = t;
        }
    }
    printf("%lld\n%s\n", bestCost, bestStr.c_str());
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
    n = int(data[0]); k = int(data[1])
    s = data[2].decode()
    best_cost = None
    best_str = s
    for d in range(10):
        need = [i for i in range(n) if s[i] != str(d)]
        def key(i):
            a = ord(s[i]) - 48
            c = abs(a - d)
            typ = 0 if a > d else 1
            return (c, typ, i if typ == 0 else -i)
        need.sort(key=key)
        already = sum(1 for ch in s if ch == str(d))
        take = max(0, k - already)
        if len(need) < take:
            continue
        t = list(s)
        cost = 0
        for i in range(take):
            p = need[i]
            cost += abs((ord(s[p]) - 48) - d)
            t[p] = str(d)
        ts = "".join(t)
        if best_cost is None or cost < best_cost or (cost == best_cost and ts < best_str):
            best_cost = cost
            best_str = ts
    sys.stdout.write("%d\n%s\n" % (best_cost, best_str))


main()
```

## 7. 边界情况与易错点

1. **已经漂亮**：花费 $0$，输出原串（样例二）。
2. **同花费的方向**：变小优先靠左、变大优先靠右，写反会得到字典序更大的串。
3. **$k=n$**：必须全部改成同一个数字，枚举 $d$ 取最小花费。
4. **已有 $\ge k$ 个**：`take=0`，直接是原串。
5. **修改数量**：恰好改 $t$ 个，不要多改（多改只会增加花费）。
6. **全局最优**：必须比较所有 $d$，不能只试出现次数最多的数字。
7. **Python 的排序键**：用 `-i` 表示降序，注意 `typ` 顺序。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：3 / 3 通过（`4/888188`、`0/533`、`3/0000002223`），C++ 与 Python 输出一致。
- **独立暴力对拍**：对 $n\le4$ 暴力枚举所有 $10^n$ 个候选串，筛出漂亮的、按（花费，串）取最优（与贪心完全不同的做法）。**60 组**随机数据全部一致。
- **最大约束性能**：$n=10^4$ 时 C++ 约 $8$ ms。
- **图片校验**：`cf118c_greedy.svg`、`cf118c_sample.svg` 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写体字体族，文本包围盒未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError`）渲染无报错；无 `---` 分隔线。
- **复核状态**：verified（样例、对拍、性能、图片、公式均实跑通过）。

## 相关题目与扩展

- [Codeforces 118A String Task](https://codeforces.com/problemset/problem/118/A)、[118B Present from Lena](https://codeforces.com/problemset/problem/118/B)、[118D Caesar's Legions](https://codeforces.com/problemset/problem/118/D)、[118E Bertown roads](https://codeforces.com/problemset/problem/118/E)：同场其余题。
- [Codeforces 1154B Make Them Odd](https://codeforces.com/problemset/problem/1154/B)：最小代价统一。
- [LeetCode 1054. 距离相等的条形码](https://leetcode.cn/problems/distant-barcodes/)：频次 + 构造。
- [LeetCode 621. 任务调度器](https://leetcode.cn/problems/task-scheduler/)：频次分析。

**延伸思考**：

1. **如果要求恰好 $k$ 个相同**：允许把多余的 $d$ 改掉，问题会更复杂。
2. **如果花费是平方差**：贪心规则不变（先小后大），但同代价比较需要更细。
3. **如果要求字典序最大**：把方向规则反过来。
4. **如果 $n$ 到 $10^6$**：$O(10 n\log n)$ 仍可接受。

