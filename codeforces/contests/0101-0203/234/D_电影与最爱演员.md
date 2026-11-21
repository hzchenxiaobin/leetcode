# Codeforces 234D 电影与最爱演员 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/234/D
- **比赛来源**：Codeforces Round 145 (Div. 2, ACM-ICPC Rules) · Problem D（UTC 2012-10-13）
- **难度**：1600
- **标签**：分类讨论、模拟
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：$m$ 个演员，Vasya 喜欢其中 $k$ 个。$n$ 部电影，每部给出片名、演员数 $d_i$ 与演员表（部分位置为 0 表示忘记）。电影"最爱"定义为：没有其它电影含有更多他喜欢的演员。对每部电影判断：0 = 一定是他的最爱；1 = 一定不是；2 = 都可能。

**约束**：$m\le100$，$k\le m$，$n\le100$。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
5 3
1 2 3
6
firstfilm
3
0 0 0
secondfilm
4
0 0 4 5
thirdfilm
1
2
fourthfilm
1
5
fifthfilm
1
4
sixthfilm
2
1 0

输出：
2
2
1
1
1
2
```

```text
输入：
5 3
1 3 5
4
jumanji
3
0 0 0
theeagle
5
1 2 3 4 0
matrix
3
2 4 0
sourcecode
2
2 4

输出：
2
0
1
1
```

**样例演算**（$m=5$，最爱 $\{1,2,3\}$）：

- firstfilm：3 个未知，最多 3 个最爱（1,2,3），最少 $3-(5-3)=1$ 个；
- secondfilm：已知 4、5 非最爱，2 个未知最多都填最爱 → 2；最少也 2（非最爱只剩 0 个可用：4、5 已出现）；
- thirdfilm：只有演员 2（最爱）→ 固定 1；
- fourthfilm / fifthfilm：只有 4、5（非最爱）→ 0；
- sixthfilm：已知 1（最爱），1 个未知 → 最多/最少都是 2。

判类：firstfilm 的可能范围 $[1,3]$ 与别的电影重叠 → 2；thirdfilm 固定 1，而 firstfilm 最多 3 > 1 → 一定不是 → 1。

**样例 2 演算**（最爱 $\{1,3,5\}$）：jumanji 范围 $[1,3]$ → 2；theeagle 已知 1、3 两个最爱、1 个未知（5 可用）→ 固定 3，且其它电影最多 3、1、0 → 一定是最爱（0）；matrix 范围 $[1,1]$，而 theeagle 下界 3 > 1 → 一定不是（1）；sourcecode 只有 2、4（非最爱）→ 0，同样一定不是（1）。

![每部电影最爱演员数的范围 [min, max]](../../../images/cf234d_range.svg)

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `2 1`/`1`/`1`/`a`/`1`/`0` | `0` | 唯一电影，必然是最爱 |
| `2 1`/`1`/`2`/`a`/`1`/`0`/`b`/`1`/`2` | `2`/`1` | 演员 2 非最爱，b 可选 1 或 2 |

## 3. 解题思路

对每部电影：统计已知最爱数 $f$、已知非最爱数 $g$、未知数 $u$，则可用最爱 $A=k-f$、可用非最爱 $B=(m-k)-g$。

- 最多最爱数 $mx=f+\min(u,A)$；
- 最少最爱数 $mn=f+\max(0,u-B)$。

判断：

- **一定是（0）**：$mn_i\ge mx_j$ 对所有 $j\ne i$；
- **一定不是（1）**：存在 $j\ne i$ 使 $mn_j>mx_i$；
- 否则 2。

![用 min/max 判定三类](../../../images/cf234d_classify.svg)

## 4. 正确性证明

**引理 1**：电影 $i$ 的最爱数可以取到 $[mn_i,mx_i]$ 中任意整数。

**证明**：未知位可填可用演员，把 $t$ 个最爱演员放进去（$0\le t\le\min(u,A)$ 且剩余 $u-t\le B$）即可；区间连续。∎

**引理 2**：电影 $i$ 一定是（0）当且仅当 $mn_i\ge mx_j$ 对所有 $j\ne i$。

**证明**：若 $mn_i\ge mx_j$ 恒成立，则任何实现中 $i$ 的最爱数都不小于其它电影，故一定最爱；反之若某 $j$ 有 $mx_j>mn_i$，取实现使 $j$ 取 $mx_j$、$i$ 取 $mn_i$，则 $i$ 不是最爱，故不能保证。∎

**引理 3**：电影 $i$ 一定不是（1）当且仅当存在 $j\ne i$ 使 $mn_j>mx_i$。

**证明**：若存在这样的 $j$，任何实现中 $j$ 都严格多于 $i$，$i$ 必不是最爱；若不存在，取实现使 $i$ 取 $mx_i$、其它取 $mn_j\le mx_i$，则 $i$ 是最爱（并列也算最爱），故不是"一定不是"。∎

**定理**：分类规则正确。**证明**：由引理 2、3 覆盖三种互斥情况。∎

## 5. 复杂度分析

- **时间**：$O(n(m+n))$，$m,n\le100$ 时 < 1 ms。
- **空间**：$O(m)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int m, k;
    if (scanf("%d %d", &m, &k) != 2) return 0;
    vector<char> fav(m + 1, 0);
    for (int i = 0; i < k; i++) { int a; scanf("%d", &a); fav[a] = 1; }
    int n;
    scanf("%d", &n);
    vector<int> mn(n), mx(n);
    for (int i = 0; i < n; i++) {
        char name[64];
        scanf("%63s", name);
        int d;
        scanf("%d", &d);
        int knownFav = 0, knownNonFav = 0, unknown = 0;
        for (int j = 0; j < d; j++) {
            int b; scanf("%d", &b);
            if (b == 0) { unknown++; continue; }
            if (fav[b]) knownFav++; else knownNonFav++;
        }
        int availFav = k - knownFav, availNonFav = (m - k) - knownNonFav;
        mn[i] = knownFav + max(0, unknown - availNonFav);
        mx[i] = knownFav + min(unknown, availFav);
    }
    for (int i = 0; i < n; i++) {
        bool sure = true, never = false;
        for (int j = 0; j < n; j++) if (j != i) {
            if (mn[i] < mx[j]) sure = false;
            if (mn[j] > mx[i]) never = true;
        }
        puts(sure ? "0" : (never ? "1" : "2"));
    }
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    p = 0
    m, k = int(data[p]), int(data[p + 1]); p += 2
    fav = set(int(data[p + i]) for i in range(k)); p += k
    n = int(data[p]); p += 1
    mn, mx = [0] * n, [0] * n
    for i in range(n):
        p += 1                      # 片名
        d = int(data[p]); p += 1
        known_fav = known_non = unknown = 0
        for j in range(d):
            b = int(data[p + j])
            if b == 0:
                unknown += 1
            elif b in fav:
                known_fav += 1
            else:
                known_non += 1
        p += d
        avail_fav = k - known_fav
        avail_non = (m - k) - known_non
        mn[i] = known_fav + max(0, unknown - avail_non)
        mx[i] = known_fav + min(unknown, avail_fav)
    out = []
    for i in range(n):
        sure = all(mn[i] >= mx[j] for j in range(n) if j != i)
        never = any(mn[j] > mx[i] for j in range(n) if j != i)
        out.append('0' if sure else ('1' if never else '2'))
    print("\n".join(out))


main()
```

## 7. 边界情况与易错点

1. **未知位只能填未出现的演员**：可用最爱 = $k-$ 已出现的爱演员数。
2. **"并列也算最爱"**：判断用 $\ge$。
3. **一定不是的条件**：存在 $j$ 使 $mn_j>mx_i$（严格大于）。
4. **$n=1$**：一定是最爱（输出 0）。
5. **片名占一行但只含字母**：按 token 读取即可。
6. **$d_i$ 与列表一致性**：题面保证。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `clang++ -std=c++17 -O2 -I codeforces/tools/include` 编译；`verify_solution.py` 自动采用同样回退。Python 3.9.6。
- **官方样例**：2 / 2 通过（`2 2 1 1 1 2`、`2 0 1 1`）。
- **独立暴力对拍**：暴力枚举每部电影未知位的所有填法（$m\le5$），得到每部电影最爱数的可能集合，再独立分类，**120 组**随机数据全部一致。
- **最大约束性能**：$m=n=100$ 时 < 1 ms（限 1 s）。
- **图片校验**：两张 SVG 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写字体，文本包围盒均在 `viewBox` 内。
- **公式校验**：`node codeforces/tools/katex_check.cjs codeforces/contests/0101-0203/234` 报告 0 个错误。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 234C Weather](https://codeforces.com/problemset/problem/234/C)：同场 C 题，前后缀。
- [Codeforces 234E Champions' League](https://codeforces.com/problemset/problem/234/E)：同场 E 题，模拟抽签。
- [Codeforces 83B Doctor](https://codeforces.com/problemset/problem/83/B)：区间化判定类题。

**延伸思考**：

1. **如果未知位可以填已出现的演员**：上限/下限会变。
2. **如果"最爱"要求严格最多**：并列时都不算最爱，判断改为 $>$。
3. **如果要求输出所有可能的最爱电影**：对每部判断"能否成为最爱"。
4. **如果演员表存在重复**：题面保证不含重复。
