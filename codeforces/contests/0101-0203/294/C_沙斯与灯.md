# Codeforces 294C Shaass and Lights（沙斯与灯） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/294/C
- **比赛来源**：Codeforces Round 178 (Div. 2) · Problem C（UTC 2013-03-15）
- **难度**：1900
- **标签**：组合计数
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB


**题意**：$n$ 盏灯排成一排，初始有 $m$ 盏亮着。每步可以点亮一盏"相邻至少有一盏亮灯"的暗灯。求把所有灯点亮的不同操作序列数 $\bmod (10^9+7)$。

**约束**：$n \le 1000$。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 1
1

输出：
1
```

官方样例 2：

```text
输入：
4 2
1 4

输出：
2
```

官方样例 3：

```text
输入：
11 2
4 8

输出：
6720
```

**观察 1（按空段分解）**：已亮的灯把 $1..n$ 切成若干段暗灯：**左端段**（在最小亮灯左边）、**右端段**、以及相邻两盏亮灯之间的**内部段**。

**观察 2（段内的合法顺序数）**：

- 左端段长度 $L$：只能从右往左依次点亮 → 1 种；
- 右端段长度 $L$：只能从左往右 → 1 种；
- 内部段长度 $L$：每次可以从左或从右推进 → $2^{L-1}$ 种 ✓（最后一步唯一）。

**观察 3（段间交错）**：只要各段内部的相对顺序确定，把 $n-m$ 步任意交错即可 →

$$\text{答案} = \frac{(n-m)!}{\prod L_i!}\cdot\prod_{\text{内部}} 2^{L_i-1}.$$

**样例 3 验证**：$n=11$，亮灯 4、8：段长 3（左端）、3（内部）、3（右端）→ $9!/(3!3!3!)\times 2^{2} = 1680\times4 = 6720$ ✓。

## 3. 解题思路

![按空段分解 + 交错计数](../../../images/cf294c_gaps.svg)

排序亮灯位置 → 求各段长度 → 用阶乘与逆元计算上式（模素数）。

## 4. 正确性证明

**引理 1**：各段内部的操作顺序互相独立，且任何合法序列限制在某段上必是"该段合法顺序"之一。

**证明**：一段暗灯只能被它两侧（或一侧）的亮灯推进，段与段之间不互相影响 ✓。∎

**引理 2**：内部段长 $L$ 的合法点灯顺序数为 $2^{L-1}$；两端段为 1。

**证明**：内部段每次选择从左端或右端推进，共 $L$ 步，最后一步无选择 → $2^{L-1}$ ✓；端段只有一个推进方向 ✓。∎

**定理**：答案为 $\dfrac{(n-m)!}{\prod L_i!}\prod 2^{L_i-1}$。

**证明**：由引理 1、2，把各段的内部顺序按多重集排列交错起来，方案数即上式 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + m\log \text{MOD})$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 1 s，实测端到端 2.4 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll MOD = 1000000007;
ll pw(ll b, ll e){ ll r=1; b%=MOD; while(e>0){ if(e&1) r=r*b%MOD; b=b*b%MOD; e>>=1; } return r; }
int main(){
    int n,m; if(scanf("%d %d",&n,&m)!=2) return 0;
    vector<int> on(m);
    for(int i=0;i<m;i++) scanf("%d",&on[i]);
    sort(on.begin(), on.end());
    int off = n - m;
    vector<ll> fact(off+1,1), inv(off+1,1);
    for(int i=1;i<=off;i++) fact[i] = fact[i-1]*i%MOD;
    inv[off] = pw(fact[off], MOD-2);
    for(int i=off;i>=1;i--) inv[i-1] = inv[i]*i%MOD;
    ll ans = fact[off];
    // 左端 gap
    int L = on[0]-1;
    ans = ans * inv[L] % MOD;
    // 内部 gap
    for(int i=0;i+1<m;i++){
        int g = on[i+1]-on[i]-1;
        ans = ans * inv[g] % MOD;
        if(g > 0) ans = ans * pw(2, g-1) % MOD;
    }
    // 右端 gap
    int R = n - on[m-1];
    ans = ans * inv[R] % MOD;
    printf("%lld\n", ans);
    return 0;
}
```

### Python3

```python
import sys
MOD = 1000000007
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    on = sorted(int(v) for v in data[2:2+m])
    off = n - m
    fact = [1]*(off+1)
    for i in range(1, off+1): fact[i] = fact[i-1]*i % MOD
    ans = fact[off]
    ans = ans * pow(fact[on[0]-1], MOD-2, MOD) % MOD
    for i in range(m-1):
        g = on[i+1] - on[i] - 1
        ans = ans * pow(fact[g], MOD-2, MOD) % MOD
        if g > 0: ans = ans * pow(2, g-1, MOD) % MOD
    ans = ans * pow(fact[n - on[-1]], MOD-2, MOD) % MOD
    print(ans)
main()
```

## 7. 边界情况与易错点

1. **$m = n$**：答案 1（全亮）。
2. **亮灯在两端**：对应端段长度为 0，阶乘取 $0! = 1$。
3. **只有一本内部段且长 1**：$2^0 = 1$ ✓。
4. **模运算**：除法用逆元。
5. **$n = 1$**：答案 1。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（1、2、6720），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版用记忆化搜索统计合法序列数（状态 = 亮灯集合）。随机 200 组 $n \le 7$，**200 / 200 全部一致**。
- **最大约束性能**：$n = 1000$，实测端到端 2.4 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 294B Shaass and Bookshelf](https://codeforces.com/problemset/problem/294/B)：同场 B 题。
- [LeetCode 1830. 使字符串有序的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-string-sorted/)：多重集排列计数的同类题。

**延伸思考**：

1. **如果灯排成环**：端段消失，全部按内部段计。
2. **如果每步可以点亮任意相邻两盏**：计数量改变。
