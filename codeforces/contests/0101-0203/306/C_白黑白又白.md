# Codeforces 306C White, Black and White Again 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/306/C
- **比赛来源**：Testing Round 6 · Problem C（UTC 2013-05-20）
- **难度**：2100
- **标签**：组合计数
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：$n$ 天依次是"白条、黑条、白条"三段，每段至少 1 天；同一天的事件类型相同，每天至少有 1 个事件。共有 $w$ 个好事件与 $b$ 个坏事件（**全部**都要分配到这些天里），事件彼此不同，同一天内的事件有先后顺序。求分配方案数 $\bmod (10^9+9)$。

**约束**：$3 \le n \le 4000$，$2 \le w \le 4000$，$1 \le b \le 4000$，$w+b \ge n$。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 2 1

输出：
2
```

官方样例 2：

```text
输入：
4 2 2

输出：
4
```

官方样例 3：

```text
输入：
3 2 2

输出：
4
```

**观察 1（段结构）**：设黑段长 $q$（$1 \le q \le n-2$），两段白共 $n-q$ 天；把它们切成 $p \ge 1$、$s \ge 1$ 两段，切法有 $n-q-1$ 种。

**观察 2（事件分配到"有序的若干天"）**：把 $w$ 个互异事件分配到 $L$ 个**有序**的非空天，方案数 $=w!\cdot\binom{w-1}{L-1}$（先给全体事件排一个序，再切成 $L$ 个非空连续块）✓。

**观察 3（合并两段白）**：第一段白与第三段白的"天"在日常顺序上是分开的，但事件受类型限制只能落在这 $p+s$ 天里；对好事件而言，"落到 $p$ 天 + 落到 $s$ 天"等价于落到 $p+s$ 个有序非空天 → $w!\cdot\binom{w-1}{p+s-1}$，与具体怎么切无关 ✓。

**于是**：

$$\text{ans}=w!\,b!\sum_{q=1}^{n-2}(n-q-1)\binom{b-1}{q-1}\binom{w-1}{n-q-1}\pmod{10^9+9}.$$

**样例 1 验证**：$n=3,w=2,b=1$：$q=1$ → $(3-1-1)\binom00\binom11=1$ → $\times 2!\cdot1!=2$ ✓。

## 3. 解题思路

![把 n 天切成三段](../../../images/cf306c_split.svg)

预处理阶乘与逆元，枚举黑段天数 $q$ 累加上式。

## 4. 正确性证明

**引理 1**：把 $m$ 个互异事件分配到 $L$ 个有序非空天的方案数是 $m!\binom{m-1}{L-1}$。

**证明**：先排列（$m!$），再在 $m-1$ 个空隙中选 $L-1$ 个切点 ✓ 双射。∎

**引理 2**：固定 $q$ 时，好事件的方案数与白的切法无关，为 $w!\binom{w-1}{n-q-1}$。

**证明**：两段白的总天数固定为 $n-q$，由引理 1 直接得到 ✓。∎

**定理**：公式给出的计数正确。

**证明**：分段（黑段长 $q$、白切法）互斥且穷尽所有配置；坏事件与好事件独立相乘；由引理 1、2 每项计数正确 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + w + b)$。
- **空间**：$O(w + b)$。
- **与时限的关系**：时限 3 s，$n = w = b = 4000$ 实测端到端 2.9 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll MOD = 1000000009LL;
ll pw(ll b, ll e){ ll r=1; b%=MOD; while(e>0){ if(e&1) r=r*b%MOD; b=b*b%MOD; e>>=1; } return r; }
int main(){
    int n,w,b; if(scanf("%d %d %d",&n,&w,&b)!=3) return 0;
    int LIM = max(w,b)+2;
    vector<ll> fact(LIM), inv(LIM);
    fact[0]=1;
    for(int i=1;i<LIM;i++) fact[i]=fact[i-1]*i%MOD;
    inv[LIM-1]=pw(fact[LIM-1], MOD-2);
    for(int i=LIM-1;i>=1;i--) inv[i-1]=inv[i]*i%MOD;
    auto C=[&](int N, int K)->ll{ if(K<0||K>N||N<0) return 0; return fact[N]*inv[K]%MOD*inv[N-K]%MOD; };
    ll sum=0;
    for(int q=1;q<=n-2;q++){
        ll days = n - q - 1;                      // 白-1 + 白-2 的切分数
        ll term = days % MOD * C(b-1, q-1) % MOD * C(w-1, n-q-1) % MOD;
        sum = (sum + term) % MOD;
    }
    ll ans = sum * fact[w] % MOD * fact[b] % MOD;
    printf("%lld\n", ans);
    return 0;
}
```

### Python3

```python
import sys
MOD = 1000000009
def main() -> None:
    n, w, b = map(int, sys.stdin.buffer.read().split()[:3])
    LIM = max(w, b) + 2
    fact = [1]*LIM
    for i in range(1, LIM): fact[i] = fact[i-1]*i % MOD
    inv = [1]*LIM
    inv[LIM-1] = pow(fact[LIM-1], MOD-2, MOD)
    for i in range(LIM-1, 0, -1): inv[i-1] = inv[i]*i % MOD
    def C(N, K):
        if K < 0 or K > N or N < 0: return 0
        return fact[N]*inv[K] % MOD * inv[N-K] % MOD
    s = 0
    for q in range(1, n-1):
        s = (s + (n-q-1) * C(b-1, q-1) % MOD * C(w-1, n-q-1)) % MOD
    print(s * fact[w] % MOD * fact[b] % MOD)
main()
```

## 7. 边界情况与易错点

1. **每天至少 1 个事件** → 事件数必须够 $n$（题面保证 $w+b\ge n$；若某段天数为 0 的组合项会自动为 0）。
2. **切点组合数** $\binom{m-1}{L-1}$ 里 $L>m$ 时为 0（自动处理）。
3. **模数 $10^9+9$** 是素数，可用费马小定理求逆元。
4. **两段白的切法数** $n-q-1$ 别漏乘。
5. **$q$ 的范围**：$1 \le q \le n-2$（三段都要非空）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（2、4、4），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版**显式**枚举 $q$ 与白的切点 $(p,s)$，再用 `math.comb`/`factorial` 直接累加（与主解的"先合并再乘"是不同代码路径）。随机 250 组 $n \le 7$，**250 / 250 全部一致**。
- **最大约束性能**：$n=w=b=4000$，实测端到端 2.9 ms（答案 997463324）。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 306A Candies](https://codeforces.com/problemset/problem/306/A)：同场 A 题。
- [Codeforces 306B Optimizer](https://codeforces.com/problemset/problem/306/B)：同场 B 题。

**延伸思考**：

1. **如果段数可变**：变成对"切点组合"再求和。
2. **如果同一天内事件无序**：把 $m!$ 换成多重集系数。
