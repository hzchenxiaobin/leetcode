# Codeforces 264C 选球 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/264/C
- **比赛来源**：Codeforces Round 162 (Div. 1) · Problem C（UTC 2013-01-20）
- **难度**：2000
- **标签**：动态规划、贪心
- **评测类型**：普通
- **限制**：时间 5 s / 内存 256 MB

**题意**：$n$ 个球排成一排，第 $i$ 个有颜色 $c_i$ 与价值 $v_i$。选一个子序列（可空）。若某球是序列第一个、或颜色与上一个不同，贡献 $v_i \cdot b$；否则（同色接龙）贡献 $v_i \cdot a$。对 $q$ 组 $(a,b)$ 求最大总价值。

**约束**：$n \le 10^5$，$q \le 500$，$|v_i|, |a|, |b| \le 10^5$。

## 2. 示例与观察

官方样例 1：

```text
输入：
6 3
1 -2 3 4 0 -1
1 2 1 2 1 1
5 1
-2 1
1 0

输出：
20
9
4
```

**样例 1 第一问**（$a=5,b=1$）：官方说选第 1、3、4 个球。按顺序：球 1（颜色 1，开头）→ $+1$；球 3（颜色 1，与上一个同色）→ $+3\cdot 5 = 15$；球 4（颜色 2，换色）→ $+4\cdot 1 = 4$；合计 20 ✓。

官方样例 2：

```text
输入：
4 1
-3 6 -1 2
1 2 3 1
1 -1

输出：
5
```

**观察 1（状态）**：`best[c]` = 以颜色 $c$ 结尾的最优序列值。对球 $i$：

- 同色接龙：`best[c_i] + v_i·a`；
- 换色/开头：`(非 c_i 颜色的最大值) + v_i·b`，或直接 `v_i·b`。

**观察 2（取"非 $c$ 的最大值"）**：维护**前两大**的颜色与值（`bc1/bv1`、`bc2/bv2`），$O(1)$ 得到"除 $c$ 外的最大值"。

**观察 3**：答案可以为 0（空序列）。每个 $v_i$ 可能为负，所以 `best` 初值取 $-\infty$，不要强取负数。

## 3. 解题思路

![按颜色做 DP](../../../images/cf264c_dp.svg)

对每组 $(a,b)$：清空 `best`（$-\infty$），遍历球 $i$，按上面的转移更新 `best[c_i]` 与前两大，答案取全局最大（含 0）。$O(n)$ 每组，总 $O(nq)$。

## 4. 正确性证明

**引理 1**：处理完前 $i$ 个球后，`best[c]` 等于"以颜色 $c$ 结尾、只使用前 $i$ 个球的最优序列值"（不存在则为 $-\infty$）。

**证明**：对 $i$ 归纳。考虑以球 $i$ 结尾的序列：若其前一个球同色，则值为前一个同色结尾的最优值 $+ v_i a$；若不同色（或 $i$ 是第一个），则值为"其它颜色的最优值" $+ v_i b$。两者取最大即转移式 ✓；不选球 $i$ 的情况保留旧值 ✓。∎

**引理 2**：`bc1/bv1`、`bc2/bv2` 正确给出"最大值"与"不同颜色的次大值"。

**证明**：每次更新 `best[c]` 后与当前两大比较并维护（只在变大时替换）✓。∎

**定理**：算法对每组 $(a,b)$ 输出正确答案。

**证明**：由引理 1、2，所有可能结尾的最优值都被正确计算，答案取最大（含空序列 0）✓。∎

## 5. 复杂度分析

- **时间**：$O(nq)$，$n=10^5, q=500$ 时约 $5\times 10^7$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 5 s，最大数据实测端到端 358.7 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;
    vector<ll> v(n);
    vector<int> c(n);
    for (int i = 0; i < n; i++) scanf("%lld", &v[i]);
    for (int i = 0; i < n; i++) scanf("%d", &c[i]);
    const ll NEG = LLONG_MIN / 4;
    while (q--) {
        ll a, b;
        scanf("%lld %lld", &a, &b);
        vector<ll> best(n + 1, NEG);
        ll ans = 0;
        int bc1 = 0, bc2 = 0;                 // 值最大的两种颜色（bc1 最大）
        ll bv1 = NEG, bv2 = NEG;
        for (int i = 0; i < n; i++) {
            int col = c[i];
            ll takeSame = (best[col] == NEG ? NEG : best[col] + v[i] * a);
            ll other = (bc1 != col ? bv1 : bv2);
            ll takeNew = (other == NEG ? NEG : other + v[i] * b);
            ll cur = max(takeSame, takeNew);
            cur = max(cur, v[i] * b);         // 作为第一个元素
            if (cur > best[col]) {
                best[col] = cur;
                if (bc1 == col) bv1 = max(bv1, cur);
                else if (cur > bv1) { bc2 = bc1; bv2 = bv1; bc1 = col; bv1 = cur; }
                else if (cur > bv2) { bc2 = col; bv2 = cur; }
            }
            ans = max(ans, cur);
        }
        printf("%lld\n", ans);
    }
    return 0;
}
```

### Python3

```python
import sys

def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    v = [int(x) for x in data[2:2 + n]]
    c = [int(x) for x in data[2 + n:2 + 2 * n]]
    pos = 2 + 2 * n
    NEG = -10**18
    out = []
    for _ in range(q):
        a, b = int(data[pos]), int(data[pos + 1]); pos += 2
        best = [NEG] * (n + 1)
        ans = 0
        bc1 = bc2 = 0
        bv1 = bv2 = NEG
        for i in range(n):
            col = c[i]
            same = best[col] + v[i] * a if best[col] != NEG else NEG
            other = bv1 if bc1 != col else bv2
            newp = other + v[i] * b if other != NEG else NEG
            cur = max(same, newp, v[i] * b)
            if cur > best[col]:
                best[col] = cur
                if bc1 == col:
                    bv1 = max(bv1, cur)
                elif cur > bv1:
                    bc2, bv2 = bc1, bv1
                    bc1, bv1 = col, cur
                elif cur > bv2:
                    bc2, bv2 = col, cur
            ans = max(ans, cur)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")

main()
```

Python 版每组 $O(n)$，500 组时明显偏慢，**建议提交 C++/PyPy3**。

## 7. 边界情况与易错点

1. **答案为 0 的下界**：空序列合法，`ans` 初始为 0。
2. **$a$ 或 $b$ 为负**：`best` 不能初始化为 0（否则会错误地"免费"接龙）。
3. **前两大的维护**：同一颜色只保留一次；更新时要正确处理"$c$ 就是当前最大颜色"的情形。
4. **$v_i = 0$**：贡献 0，可以选也可以不选。
5. **颜色范围**：$c_i \le n$，数组开 $n+1$。
6. **多组查询互不影响**：每组都要重置 `best`。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（20/9/4、5），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版枚举所有 $2^n$ 子集直接算价值。随机 250 组 $n \le 6$、$a,b \in [-3,3]$，**250 / 250 全部一致**。
- **最大约束性能**：$n = 10^5, q = 500$，实测端到端 358.7 ms。
- **图片校验**：两张 SVG 通过 `ElementTree.parse`，含 `feTurbulence` 与手写字体。
- **复核状态**：verified（唯一视觉瑕疵：SVG 说明文字里的数值仅作示意）。

## 相关题目与扩展

- [Codeforces 264B Good Sequences](https://codeforces.com/problemset/problem/264/B)：同场 B 题。
- [LeetCode 740. 删除并获得点数](https://leetcode.cn/problems/delete-and-earn/)：按"相邻/颜色"约束做 DP 的同类题。

**延伸思考**：

1. **如果要求"相邻必须不同色"**：去掉同色接龙分支。
2. **如果 $q$ 很大（$10^5$）**：需要离线/凸包技巧，本题 $q \le 500$ 才允许 $O(nq)$。

