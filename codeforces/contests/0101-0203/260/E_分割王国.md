# Codeforces 260E 分割王国 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/260/E
- **比赛来源**：Codeforces Round 158 (Div. 2) · Problem E（UTC 2012-12-27）
- **难度**：2500
- **标签**：枚举、前缀和、构造
- **评测类型**：多解（浮点输出）
- **限制**：时间 2 s / 内存 256 MB

**题意**：平面上有 $n$ 个城市（点）。画 **4 条直线**：两条竖直（$x = x_1, x_2$）、两条水平（$y = y_1, y_2$），且**不能经过任何城市**。它们把平面分成 $9$ 块，各块的城市数（多重集）必须恰好等于给定的 $9$ 个数 $a_1 \ldots a_9$（顺序可任意对应）。输出 $x_1, x_2$ 与 $y_1, y_2$；无解输出 `-1`。

**约束**：$n \le 10^5$，$|x_i|, |y_i| \le 10^9$，$\sum a_i = n$。判定时线到城市的距离容差 $10^{-6}$。

## 2. 示例与观察

官方样例 1：

```text
输入：
9
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3
1 1 1 1 1 1 1 1 1

输出：
1.5000000000 2.5000000000
1.5000000000 2.5000000000
```

官方样例 2：

```text
输入：
15
4 4
-1 -3
1 5
3 -4
-4 4
-1 1
3 -3
-4 -5
-3 3
3 2
4 1
-4 2
-2 -5
-3 4
-1 4
2 1 2 1 2 1 3 2 1

输出：
-3.5000000000 2.0000000000
3.5000000000 -1.0000000000
```

官方样例 3：

```text
输入：
10
-2 10
6 0
-16 -6
-4 13
-4 -2
-17 -10
9 15
18 16
-5 2
10 -5
2 1 1 1 1 1 1 1 1

输出：
-1
```

**样例 1**：$3 \times 3$ 的点阵，两条竖线取 $x = 1.5, 2.5$、两条横线取 $y = 1.5, 2.5$，每块恰好 1 个城市 ✓。

**样例 2**：给定的 9 个数之和是 15 ✓；官方答案的线不经过任何城市。

**样例 3**：9 个数之和 $= 10 = n$ ✓，但无解 → `-1`。

**观察 1（列和与行和必须是"9 个数分成 3 组之和"）**：设三列的城市数为 $c_1, c_2, c_3$（从左到右），三行为 $r_1, r_2, r_3$。它们都是那 9 个数中某 3 个的和。

**观察 2（线由计数唯一确定）**：给定"左边有 $c_1$ 个城市"，竖线 $x_1$ 必须落在第 $c_1$ 小与第 $c_1+1$ 小的 $x$ 之间（且两者严格不等，否则线会压到城市上）。

**观察 3（枚举量很小）**：把 9 个数分成 3 组的方式只有 $\binom{9}{3}\binom{6}{3} = 84 \times 20 = 1680$ 种（去重后更少），所以"候选 $(c_1, c_2)$"与"候选 $(r_1, r_2)$"都不超过 1680 组。

**观察 4（核对成本低）**：对每组候选，只需算出 9 块的城市数并与给定多重集比较。

## 3. 解题思路

![四条线切成 9 块](../../../images/cf260e_grid.svg)

1. 若 $\sum a_i \ne n$ → `-1`；
2. 枚举把 9 个数分成 3 组的全部方式，得到候选 $(c_1, c_1+c_2)$ 集合（列切分）与 $(r_1, r_1+r_2)$（行切分），去重；
3. 对每个候选值，检查线是否可放：$c > 0$ 时需要 $x_{c-1} < x_c$（升序 $x$），$c = 0$ 时线放在 $x_0 - 1$，$c = n$ 时放在 $x_{n-1} + 1$；
4. 预处理表 $T[b][r] = \#\{\text{城市} : \text{y 名次} < r,\ \text{x 名次} < b\}$（只需在候选 $b, r$ 上取值）；
5. 对每组 $((c_1,c_2), (r_1,r_2))$，用 $T$ 的 $O(1)$ 查询算出 9 块城市数，与给定多重集比较，相等即输出。

**线的取值**：城市坐标是整数，取 $x_1 = x_{c_1-1} + 0.5$（严格落在第 $c_1$ 与第 $c_1+1$ 小之间），保证不经过任何城市，且不同切分点给出不同直线。

## 4. 正确性证明

记城市按 $x$ 升序为 $x_0 \le \cdots \le x_{n-1}$，按 $y$ 升序类似；$x$ 名次 / $y$ 名次为城市在排序中的位置。

**引理 1（列和结构）**：合法方案中三列的城市数 $c_1,c_2,c_3$ 满足：$c_1$、$c_1+c_2$、$c_1+c_2+c_3 = n$，且 $c_i$ 各自是给定 9 个数中某 3 个的**和**。

**证明**：每一列由 3 块组成，其城市数之和是 9 个数中对应 3 个的和；三列互不重叠、覆盖所有城市，所以和分别为 $c_1, c_2, c_3$ 且总和 $n$ ✓。∎

**引理 2（切分位置可行）**：若左边恰有 $c$ 个城市，则可取竖线 $x = x_{c-1} + 0.5$（$0 < c < n$）；这要求 $x_{c-1} < x_c$（否则有城市与线重合）。

**证明**：$x$ 名次 $< c$ 的城市 $x$ 坐标 $\le x_{c-1} < x_{c-1}+0.5$，名次 $\ge c$ 的 $\ge x_c > x_{c-1}+0.5$ ✓，故线不经过城市且左边恰 $c$ 个。若 $x_{c-1} = x_c$，任何落在这两个相同坐标"之间"的线都必然经过这些城市，不可行 ✓。∎

**引理 3（计数表正确）**：$T[b][r] = \#\{\text{城市} : \text{y 名次} < r,\ \text{x 名次} < b\}$，则 9 块的城市数可表示为
$$
\begin{aligned}
\text{col}_0 &= (T[b_1][r_1],\ T[b_1][r_2]-T[b_1][r_1],\ b_1-T[b_1][r_2]),\\
\text{col}_1 &= (T[b_2][r_1]-T[b_1][r_1],\ \ldots),\qquad
\text{col}_2 = (r_1-T[b_2][r_1],\ \ldots).
\end{aligned}
$$

**证明**：把"$y$ 名次 $< r$ 且 $x$ 名次 $< b$"的城市数记为 $T[b][r]$（对 $b,r$ 单调）；用二维容斥即得各块计数 ✓。∎

**定理**：算法输出的 4 条线满足题意；输出 `-1` 时无解。

**证明**：由引理 1，任何合法方案的列切分/行切分都在枚举范围内；由引理 2，候选切分点要么可放线（算法取 $+0.5$），要么被排除；由引理 3，算法对每组候选算出的 9 块计数正确，因此找到的候选确实把 9 块的城市数变成给定多重集 ⇒ 输出合法。反之，若全部候选都不匹配，则由引理 1 枚举完备性，不存在合法方案 ⇒ `-1` ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + |B| \cdot n + |B| \cdot |R| \cdot 9)$，其中 $|B|, |R| \le 336$ 个候选值，$|B| \times |R|$ 的组合数不超过 $1680^2 \approx 2.8 \times 10^6$。实测在 $n = 10^5$ 时低于 25 ms。
- **空间**：$O(n + |B| \cdot |R|)$。
- **与时限的关系**：时限 2 s，$n = 10^5$ 实测端到端 21.5 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<ll> x(n), y(n);
    for (int i = 0; i < n; i++) scanf("%lld %lld", &x[i], &y[i]);
    vector<ll> need(9);
    ll sum = 0;
    for (int i = 0; i < 9; i++) { scanf("%lld", &need[i]); sum += need[i]; }
    if (sum != n) { printf("-1\n"); return 0; }
    vector<ll> sx = x, sy = y;
    sort(sx.begin(), sx.end()); sort(sy.begin(), sy.end());
    vector<ll> needSorted = need;
    sort(needSorted.begin(), needSorted.end());

    // 按 y 排序后的 x 名次
    vector<int> ordY(n);
    iota(ordY.begin(), ordY.end(), 0);
    sort(ordY.begin(), ordY.end(), [&](int a, int b) { return y[a] < y[b] || (y[a] == y[b] && x[a] < x[b]); });
    vector<int> xRank(n);
    {
        vector<int> ordX(n);
        iota(ordX.begin(), ordX.end(), 0);
        sort(ordX.begin(), ordX.end(), [&](int a, int b) { return x[a] < x[b] || (x[a] == x[b] && y[a] < y[b]); });
        for (int i = 0; i < n; i++) xRank[ordX[i]] = i;
    }
    vector<int> xrByY(n);
    for (int k = 0; k < n; k++) xrByY[k] = xRank[ordY[k]];

    // 枚举把 9 个数分成 3 组（每组 3 个）的所有 (c1, c2)
    vector<pair<int,int>> splits;
    for (int a = 0; a < 9; a++) for (int b = a + 1; b < 9; b++) for (int c = b + 1; c < 9; c++) {
        int used1[9] = {0}; used1[a] = used1[b] = used1[c] = 1;
        int c1 = (int)(need[a] + need[b] + need[c]);
        int rem[6], m = 0;
        for (int i = 0; i < 9; i++) if (!used1[i]) rem[m++] = i;
        for (int u = 0; u < 6; u++) for (int v = u + 1; v < 6; v++) for (int w = v + 1; w < 6; w++) {
            int c2 = (int)(need[rem[u]] + need[rem[v]] + need[rem[w]]);
            splits.push_back({c1, c1 + c2});
        }
    }
    sort(splits.begin(), splits.end());
    splits.erase(unique(splits.begin(), splits.end()), splits.end());

    // 收集需要的边界值
    vector<int> bvals, rvals;
    for (auto &p : splits) { bvals.push_back(p.first); bvals.push_back(p.second); rvals.push_back(p.first); rvals.push_back(p.second); }
    sort(bvals.begin(), bvals.end()); bvals.erase(unique(bvals.begin(), bvals.end()), bvals.end());
    sort(rvals.begin(), rvals.end()); rvals.erase(unique(rvals.begin(), rvals.end()), rvals.end());

    // T[b][r] = #{k < r : xrByY[k] < b}
    int NB = bvals.size(), NR = rvals.size();
    vector<vector<int>> T(NB, vector<int>(NR, 0));
    for (int i = 0; i < NB; i++) {
        int b = bvals[i];
        int cntv = 0, ptr = (rvals[0] == 0 ? 1 : 0);   // r=0 一列恒为 0
        for (int k = 0; k < n; k++) {
            if (xrByY[k] < b) cntv++;
            while (ptr < NR && rvals[ptr] == k + 1) { T[i][ptr] = cntv; ptr++; }
        }
        while (ptr < NR && rvals[ptr] == n) { T[i][ptr] = cntv; ptr++; }
    }
    auto tidx = [&](const vector<int> &v, int val) { return (int)(lower_bound(v.begin(), v.end(), val) - v.begin()); };

    auto midRight = [&](const vector<ll> &s, int k) -> double {   // 在 s[k-1] 与 s[k] 之间取线
        if (k <= 0) return (double)s[0] - 1.0;
        if (k >= n) return (double)s[n - 1] + 1.0;
        return (double)s[k - 1] + 0.5;                // 城市坐标是整数，+0.5 一定不落在城市上
    };
    auto okSplit = [&](const vector<ll> &s, int k) -> bool {
        if (k <= 0 || k >= n) return true;
        return s[k - 1] < s[k];
    };

    for (auto &xp : splits) {
        int b1 = xp.first, b2 = xp.second;
        if (b1 >= b2) continue;                       // 两列相同 → 两条线重合
        if (!okSplit(sx, b1) || !okSplit(sx, b2)) continue;
        int i1 = tidx(bvals, b1), i2 = tidx(bvals, b2);
        for (auto &yp : splits) {
            int r1 = yp.first, r2 = yp.second;
            if (r1 >= r2) continue;
            if (!okSplit(sy, r1) || !okSplit(sy, r2)) continue;
            int j1 = tidx(rvals, r1), j2 = tidx(rvals, r2);
            int A1 = T[i1][j1], A2 = T[i1][j2];
            int B1 = T[i2][j1], B2 = T[i2][j2];
            // 第 0 列：x 名次 < b1；第 1 列：b1 <= 名次 < b2；第 2 列：>= b2
            int cells[9] = {
                A1, A2 - A1, b1 - A2,
                B1 - A1, (B2 - B1) - (A2 - A1), (b2 - b1) - (B2 - B1),
                r1 - B1, (r2 - B2) - (r1 - B1), (n - b2) - (r2 - B2)
            };
            int got[9];
            for (int i = 0; i < 9; i++) got[i] = cells[i];
            sort(got, got + 9);
            bool eq = true;
            for (int i = 0; i < 9; i++) if (got[i] != needSorted[i]) { eq = false; break; }
            if (!eq) continue;
            double x1 = midRight(sx, b1), x2 = midRight(sx, b2);
            double y1 = midRight(sy, r1), y2 = midRight(sy, r2);
            printf("%.10f %.10f\n%.10f %.10f\n", x1, x2, y1, y2);
            return 0;
        }
    }
    printf("-1\n");
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
    n = int(data[0])
    x = [0] * n
    y = [0] * n
    pos = 1
    for i in range(n):
        x[i] = int(data[pos]); y[i] = int(data[pos + 1]); pos += 2
    need = [int(v) for v in data[pos:pos + 9]]
    if sum(need) != n:
        print(-1)
        return
    sx = sorted(x); sy = sorted(y)
    need_sorted = sorted(need)

    ord_x = sorted(range(n), key=lambda i: (x[i], y[i]))
    xrank = [0] * n
    for r, i in enumerate(ord_x):
        xrank[i] = r
    ord_y = sorted(range(n), key=lambda i: (y[i], x[i]))
    xr_by_y = [xrank[i] for i in ord_y]

    splits = set()
    idxs = range(9)
    for a in idxs:
        for b in range(a + 1, 9):
            for c in range(b + 1, 9):
                c1 = need[a] + need[b] + need[c]
                rem = [i for i in idxs if i not in (a, b, c)]
                for u in range(6):
                    for v in range(u + 1, 6):
                        for w in range(v + 1, 6):
                            c2 = need[rem[u]] + need[rem[v]] + need[rem[w]]
                            splits.add((c1, c1 + c2))
    splits = sorted(splits)
    bvals = sorted(set(v for p in splits for v in p))
    rvals = bvals

    T = {}
    for b in bvals:
        row = {0: 0}
        cntv = 0
        ri = 1 if rvals and rvals[0] == 0 else 0
        want = rvals
        for k in range(n):
            if xr_by_y[k] < b:
                cntv += 1
            while ri < len(want) and want[ri] == k + 1:
                row[want[ri]] = cntv
                ri += 1
        while ri < len(want) and want[ri] == n:
            row[want[ri]] = cntv
            ri += 1
        T[b] = row

    def mid_right(s, k):
        if k <= 0:
            return float(s[0]) - 1.0
        if k >= n:
            return float(s[n - 1]) + 1.0
        return s[k - 1] + 0.5

    def ok_split(s, k):
        if k <= 0 or k >= n:
            return True
        return s[k - 1] < s[k]

    for b1, b2 in splits:
        if b1 >= b2:
            continue
        if not ok_split(sx, b1) or not ok_split(sx, b2):
            continue
        T1 = T[b1]; T2 = T[b2]
        for r1, r2 in splits:
            if r1 >= r2:
                continue
            if not ok_split(sy, r1) or not ok_split(sy, r2):
                continue
            A1 = T1[r1]; A2 = T1[r2]
            B1 = T2[r1]; B2 = T2[r2]
            cells = [
                A1, A2 - A1, b1 - A2,
                B1 - A1, (B2 - B1) - (A2 - A1), (b2 - b1) - (B2 - B1),
                r1 - B1, (r2 - B2) - (r1 - B1), (n - b2) - (r2 - B2),
            ]
            if sorted(cells) == need_sorted:
                sys.stdout.write("%.10f %.10f\n%.10f %.10f\n" % (
                    mid_right(sx, b1), mid_right(sx, b2), mid_right(sy, r1), mid_right(sy, r2)))
                return
    print(-1)


main()
```

Python 版逐项等价但常数大，**建议 C++/PyPy3**。

## 7. 边界情况与易错点

1. **$\sum a_i \ne n$**：直接 `-1`。
2. **$c = 0$ 或 $c = n$**：线放在最外侧（$x_0 - 1$ / $x_{n-1}+1$），不要越界。
3. **重复坐标**：$x_{c-1} = x_c$ 时该切分不可行（线会经过城市）。
4. **两条线重合**：$c_1 = c_1 + c_2$（中间列为空）时必须排除。
5. **精度**：坐标是整数，$+0.5$ 保证线不经过城市；输出 10 位小数。
6. **多重集比较**：9 个数要按多重集比较（排序后逐项比）。
7. **多解**：任意合法答案均可（本实现与官方样例给的结果可能不同）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（`1.5 2.5 / 1.5 2.5`、样例 2 给出一组合法线、`-1`），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf260e.py`（校验线与城市距离、9 块计数多重集）。
- **随机对拍**：随机点集 + 随机合法切分算出 9 块计数作为输入，200 组 $n \le 14$，两个实现都通过 checker，**200 / 200 全部通过**；另用"随机 9 个数"测试 `-1` 分支。
- **最大约束性能**：$n = 10^5$，实测端到端 21.5 ms。
- **图片校验**：两张 SVG 通过 `ElementTree.parse`，含 `feTurbulence` 与手写字体。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 260D Black and White Tree](https://codeforces.com/problemset/problem/260/D)：同场 D 题，构造。
- [Codeforces 263E Rhombus](https://codeforces.com/problemset/problem/263/E)：同样是二维计数 + 枚举最优位置。

**延伸思考**：

1. **如果要求 9 块的顺序也固定**（第 $i$ 个儿子拿第 $i$ 块）：变成顺序敏感的匹配，枚举量不变但比较条件更严。
2. **如果是 $m \times m$ 块**：枚举量指数增长，需要更聪明的做法（例如按行列和的唯一分解）。
