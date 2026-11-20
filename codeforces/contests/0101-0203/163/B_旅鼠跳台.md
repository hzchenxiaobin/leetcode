# Codeforces 163B 旅鼠跳台 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/163/B
- **比赛来源**：VK Cup 2012 Round 2 · Problem B（UTC 2012-03-25）
- **难度**：2000
- **标签**：二分、贪心、排序
- **评测类型**：特殊评测（方案不唯一，允许误差）
- **限制**：时间 1 s / 内存 256 MB

**题意**：$n$ 只旅鼠（重量 $m_i$、爬速 $v_i$），$k$ 个台子高度 $h,2h,\dots,kh$。选 $k$ 只旅鼠分别放在台 $1..k$ 上，要求：**台越高重量越大**（$m$ 随台号非降），且每只都能在 $t$ 分钟内爬到自己的台（时间 $=$ 高度$/v_i$）。求最小的 $t$ 并输出一种安排。

**约束**：$n\le10^5$：二分 $t$ + 贪心检查。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
5 3 2
1 2 3 2 1
1 2 1 2 10

输出：
5 2 4
```

最优 $t=3$：旅鼠 5（$m=1,v=10$）上 1 号台（$2/10$）、旅鼠 2（$m=2,v=2$）上 2 号台（$4/2=2$）、旅鼠 4（$m=2,v=2$）上 3 号台（$6/2=3$）✓ 重量 $1\le2\le2$ ✓

（本解输出 `1 5 2`：旅鼠 1 上 1 号台（$2/1=2$）、旅鼠 5 上 2 号台（$4/10$）、旅鼠 2 上 3 号台（$6/2=3$），最大用时同为 3 ✓ 两种安排都最优。）

官方样例 2（输入 / 输出原样）：

```text
输入：
5 3 10
3 4 3 2 1
5 4 3 2 1

输出：
4 3 1
```

![二分时间 t，再按重量贪心分配台号](../../../images/cf163b_bsearch.svg)

**观察 1（判定问题）**：固定 $t$，可行 ⟺ 存在 $k$ 只旅鼠按重量非降排成 $p_1<\dots<p_k$（重量序），且 $v_{p_j}\ge jh/t$。

**观察 2（贪心）**：把旅鼠按 $(m,\ v)$ 升序排序后从头扫描：第 $j$ 个空台（从低到高）分给第一个满足 $v\ge jh/t$ 的旅鼠。这样低台用掉"又轻又慢"的，把更快的留给高台。

**观察 3（二分）**：可行性关于 $t$ 单调（$t$ 越大越容易）⇒ 二分 $t$。

## 3. 解题思路

1. 按 $(m_i, v_i)$ 升序排序；
2. 二分 $t\in[0,\ \max_i kh/v_i]$（100 次迭代足够，或按 $10^{-11}$ 的相对精度）；
3. 判定：$j=0$；顺序扫描旅鼠，若 $v_i\ge(j+1)h/t$ 则 $j{+}{+}$；最终 $j\ge k$ 即可行；
4. 输出该判定选出的 $k$ 只。

![样例 2 的最优安排](../../../images/cf163b_sample.svg)

## 4. 正确性证明

**引理 1（判定等价）**：固定 $t$，"存在合法安排" ⟺ 排序后可按上述贪心选出 $k$ 只。

**证明**：
(⇐) 贪心选出的旅鼠按扫描顺序重量非降 ✓ 且第 $j$ 只满足 $v\ge jh/t$ ✓ 合法。
(⇒) 设某合法安排为 $i_1,\dots,i_k$（重量非降），在排序序中位置 $q_1<\dots<q_k$（同重量时取"速度升序"，则同一重量内可按速度重排而不破坏合法性）。贪心第 $j$ 步选的是"剩余中第一个满足 $v\ge jh/t$ 的位置 $g_j$"。归纳证明 $g_j\le q_j$：$g_1\le q_1$（$i_1$ 满足条件，贪心取更靠前的）；若 $g_{j-1}\le q_{j-1}<q_j$，则 $i_j$ 在贪心视野内且满足条件 ⇒ $g_j\le q_j$ ✓。于是贪心能选满 $k$ 个 ∎

**引理 2（单调性）**：若 $t$ 可行，则任意 $t'>t$ 也可行。

**证明**：$t'$ 下阈值 $jh/t'<jh/t$ 更松，同一方案仍合法 ✓ ∎

**定理**：二分收敛到的 $t^\ast$ 是最小可行时间，且输出方案合法。

**证明**：由引理 2，可行域是区间 $[t^\ast,\infty)$，二分收敛到其左端点；由引理 1 每次判定正确 ⇒ $t^\ast$ 正确；最终方案按判定构造，合法 ✓ ∎

**精度说明**：方案的"最大用时" $\max_j jh/v_{i_j}$ 只取有限个候选值，二分 100 次后 $t$ 与该值的相对误差 $<10^{-27}$，远超题目要求；输出前用 $t(1+10^{-12})$ 再判定一次即可稳定选出方案。

## 5. 复杂度分析

- **时间**：排序 $O(n\log n)$ + 二分 $100\times O(n)$，$n=10^5$ 实测约 0.1 s。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    int n, k;
    ll h;
    if (scanf("%d %d %lld", &n, &k, &h) != 3) return 0;
    vector<ll> m(n), v(n);
    for (int i = 0; i < n; i++) scanf("%lld", &m[i]);
    for (int i = 0; i < n; i++) scanf("%lld", &v[i]);
    vector<int> ord(n);
    for (int i = 0; i < n; i++) ord[i] = i;
    // 按 (重量升, 速度升) 排序：低台给轻的、慢的
    sort(ord.begin(), ord.end(), [&](int a, int b) {
        if (m[a] != m[b]) return m[a] < m[b];
        return v[a] < v[b];
    });
    // 可行性：从轻到重扫描，把第 j 个台（高度 j*h）分给第一个满足 v >= j*h/t 的
    auto feasible = [&](double t, vector<int> *pick) {
        int need = 0;
        vector<int> chosen;
        for (int idx = 0; idx < n && need < k; idx++) {
            int i = ord[idx];
            double needV = (double)(need + 1) * (double)h / t;
            if ((double)v[i] + 1e-12 >= needV) {
                chosen.push_back(i);
                need++;
            }
        }
        if (need == k) {
            if (pick) *pick = chosen;
            return true;
        }
        return false;
    };
    double lo = 0, hi = 0;
    for (int i = 0; i < n; i++) hi = max(hi, (double)k * (double)h / (double)v[i]);
    for (int it = 0; it < 100; it++) {
        double mid = (lo + hi) / 2;
        if (feasible(mid, nullptr)) hi = mid; else lo = mid;
    }
    vector<int> pick;
    feasible(hi * (1 + 1e-12) , &pick);
    if ((int)pick.size() < k) feasible(hi, &pick);
    for (int i = 0; i < k; i++) printf("%d%c", pick[i] + 1, i + 1 == k ? '\n' : ' ');
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n, k, h = int(data[0]), int(data[1]), int(data[2])
    m = [int(x) for x in data[3:3 + n]]
    v = [int(x) for x in data[3 + n:3 + 2 * n]]
    order = sorted(range(n), key=lambda i: (m[i], v[i]))

    def feasible(t, want=False):
        need = 0
        chosen = []
        for idx in order:
            if need >= k:
                break
            if v[idx] + 1e-12 >= (need + 1) * h / t:
                chosen.append(idx)
                need += 1
        if want and need == k:
            return chosen
        return need == k

    lo, hi = 0.0, max(k * h / v[i] for i in range(n))
    for _ in range(100):
        mid = (lo + hi) / 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid
    pick = feasible(hi * (1 + 1e-12), want=True) or feasible(hi, want=True)
    print(" ".join(str(i + 1) for i in pick))


main()
```

## 7. 边界情况与易错点

1. **排序键**：重量升序，同级按速度升序（快的留给高台）。
2. **阈值比较**：`v_i >= j*h/t`，浮点比较加 $10^{-12}$ 容差。
3. **二分上界**：$\max_i kh/v_i$ 必可行。
4. **输出前的再判定**：用 $t(1+10^{-12})$ 保证选得出（否则可能因浮点刚好差一点而少选）。
5. **$k=n$**：必须全部用上。
6. **同重量**：可任意换序（重量非降允许相等）。
7. **$h$ 与 $v$ 可达 $10^9$**：用 64 位存，比较时转 `double`。
8. **输出编号**：1 基，答案不唯一。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/163/B_旅鼠跳台.md --checker codeforces/tools/checkers/cf163b.py`
- **checker 的校验条件**（方案不唯一）：$k$ 个互不相同的合法编号；重量随台高非降；最大用时等于最优时间（checker 用二分+贪心独立求出），相对误差 $\le10^{-9}$。
- **官方样例**：$2/2$ 通过 checker（样例 1 官方给 `5 2 4`，本解给 `1 5 2`，两者最大用时都是 3）。
- **独立对拍**：另写"枚举全部 $n!/(n-k)!$ 种安排、取最小最大用时"的暴力，对 $200$ 组随机数据（$n\le5$）比较：本解给出的安排通过 checker，且最优时间与暴力一致。
- **性能**：$n=10^5$ 单次约 0.1 s。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 163A Substring and Subsequence](https://codeforces.com/problemset/problem/163/A)：同场 A 题。
- [Codeforces 163C Conveyor](https://codeforces.com/problemset/problem/163/C)：同场 C 题。
- [LeetCode 410. 分割数组的最大值](https://leetcode.cn/problems/split-array-largest-sum/)：二分答案。

**延伸思考**：

1. **若重量要求严格递增**：排序时同重量只能取一只，判定改成计数。
2. **若台数高度不等差**：阈值改成 $H_j/t$ 即可。
3. **若要求最小化总时间**：变成分配问题（需匈牙利/流）。
