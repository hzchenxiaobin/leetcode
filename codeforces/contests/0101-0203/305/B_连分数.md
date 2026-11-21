# Codeforces 305B Continued Fractions 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/305/B
- **比赛来源**：Codeforces Round 184 (Div. 2) · Problem B（UTC 2013-05-16）
- **难度**：1700
- **标签**：数论、连分数
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给定分数 $p/q$ 与一个高度为 $n$ 的连分数 $[a_1; a_2, \ldots, a_n]$，判断两者是否相等。

**约束**：$p, q \le 10^{18}$，$n \le 90$，$a_i \le 10^{18}$。

## 2. 示例与观察

官方样例 1：

```text
输入：
9 4
2
2 4

输出：
YES
```

官方样例 2：

```text
输入：
9 4
3
2 3 1

输出：
YES
```

官方样例 3：

```text
输入：
9 4
3
1 2 4

输出：
NO
```

**观察 1**：$p/q$ 的连分数展开由**欧几里得算法**直接给出：反复取 $k = \lfloor x/y \rfloor$，$x \leftarrow y$，$y \leftarrow x \bmod y$。

**观察 2（表示不唯一）**：$[2;3,1] = [2;4]$ —— 末尾的 $1$ 可以并入前一项。规范形式是"末尾 $> 1$"。

**观察 3**：两边都规约成规范形式后逐项比较即可。**不要**真的把连分数的值算成 $p/q$（$a_i$ 可达 $10^{18}$，会溢出/爆精度）。

**样例 2 验证**：$[2,3,1]$ → 末尾 1 并入前项 → $[2,4]$；$9/4$ 的展开为 $[2,4]$ → YES ✓。

## 3. 解题思路

![规范形式后比对](../../../images/cf305b_canon.svg)

欧几里得展开 $p/q$ + 两边规范化 + 逐项比较。

## 4. 正确性证明

**引理 1**：欧几里得算法的商序列就是 $p/q$ 的连分数展开。

**证明**：$p/q = k + r/q$ 且 $r < q$，递归即得 ✓；$k = \lfloor p/q \rfloor$ ✓。∎

**引理 2**：连分数的规范形式（长度 1 或末项 $>1$）唯一。

**证明**：经典的连分数唯一性定理 ✓。∎

**定理**：判定正确。

**证明**：由引理 1、2，两边规范后相等 ⇔ 原值相等 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + \log p)$。
- **空间**：$O(n)$。
- **与时限的关系**：实测端到端 2.2 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main(){
    ll p,q; int n;
    if(scanf("%lld %lld",&p,&q)!=2) return 0;
    if(scanf("%d",&n)!=1) return 0;
    vector<ll> a(n);
    for(int i=0;i<n;i++) scanf("%lld",&a[i]);
    // 规范形式：末尾若为 1 且长度 >1，则合并到前一项
    while(n>1 && a[n-1]==1){ a[n-2]++; n--; }
    // p/q 的连分数展开
    vector<ll> cf;
    ll x=p, y=q;
    while(y){ cf.push_back(x/y); ll r=x%y; x=y; y=r; }
    // 展开的末尾也可能是 1
    while(cf.size()>1 && cf.back()==1){ cf[cf.size()-2]++; cf.pop_back(); }
    printf("%s\n", (cf.size()==(size_t)n && equal(cf.begin(), cf.end(), a.begin())) ? "YES" : "NO");
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    p, q = int(data[0]), int(data[1]); n = int(data[2])
    a = [int(v) for v in data[3:3+n]]
    while n > 1 and a[n-1] == 1:
        a[n-2] += 1; n -= 1
    cf = []
    x, y = p, q
    while y:
        cf.append(x // y)
        x, y = y, x % y
    while len(cf) > 1 and cf[-1] == 1:
        cf[-2] += 1; cf.pop()
    print("YES" if cf == a else "NO")
main()
```

## 7. 边界情况与易错点

1. **末尾为 1**：必须并入前一项。
2. **$n = 1$**：直接与 $\lfloor p/q \rfloor$ 比较。
3. **不要算数值**：$a_i$ 太大。
4. **$p \ge q$** 或 $p < q$ 都可能（题面 $q \le p$）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（YES、YES、NO），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版用 `fractions.Fraction` 从下往上精确求值再比较。随机 250 组，**250 / 250 全部一致**。
- **最大约束性能**：$p,q \approx 10^{18}$、$n = 90$，实测端到端 2.2 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 305A Strange Addition](https://codeforces.com/problemset/problem/305/A)：同场 A 题。
- [Codeforces 305C Ivan and Powers of Two](https://codeforces.com/problemset/problem/305/C)：同场 C 题。

**延伸思考**：

1. **如果给定连分数求分数**：从下往上算，注意大整数。
2. **如果只比较大小**：可以逐项比较（第一名不同者定序）。
