# Codeforces 166E 四面体上的闭合游走 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/166/E
- **比赛来源**：Codeforces Round 113 (Div. 2) · Problem E（UTC 2012-03-23）
- **难度**：1500
- **标签**：组合数学、DP、矩阵快速幂
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：蚂蚁从四面体顶点 $D$ 出发，每步沿棱走到另一个顶点，求走恰好 $n$ 步回到 $D$ 的方案数，模 $10^9+7$。

**约束**：$n\le10^7$：$O(n)$ 递推或 $O(\log n)$ 闭式。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
2
输出：
3
```

两步回到 $D$：$D\to A\to D$、$D\to B\to D$、$D\to C\to D$ ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
4
输出：
21
```

![两种状态：在 D 或不在 D](../../../images/cf166e_states.svg)

**观察**：设 $s_n$ = 走 $n$ 步后位于 $D$ 的方案数，$t_n$ = 位于某个**指定**非 $D$ 顶点（如 $A$）的方案数。由对称性三者相同。转移：

- 从 $D$ 出发：3 条棱分别到 $A,B,C$ ⇒ $s_{n+1}$ 的贡献来自三个非 $D$ 顶点各一条边：$s_{n+1}=3t_n$；
- 到 $A$：可从 $D$ 来（1 条）或从 $B,C$ 来（2 条）⇒ $t_{n+1}=s_n+2t_n$。

初值 $s_0=1,\ t_0=0$。

**闭式**：令 $u_n=s_n$、特征方程为 $\lambda^2-2\lambda-3=0$（$\lambda=3,-1$）⇒

$$s_n=\frac{3^n+3\cdot(-1)^n}{4}.$$

验证：$n=2$：$(9+3)/4=3$ ✓；$n=4$：$(81+3)/4=21$ ✓。

## 3. 解题思路

1. 用闭式 $s_n=(3^n+3(-1)^n)/4$，模 $10^9+7$ 下用逆元算 $4^{-1}$；
2. 或用 $O(n)$ 递推 $s,t$（$n\le10^7$ 也可行）。

![n=2 的 3 条闭合路径](../../../images/cf166e_sample.svg)

## 4. 正确性证明

**引理 1（状态划分）**：任一时刻蚂蚁必在 $D$ 或三个非 $D$ 顶点之一，且三个非 $D$ 顶点的方案数由对称性相等。

**证明**：四面体的自同构群（固定 $D$ 的置换群 $S_3$）传递地作用在 $A,B,C$ 上，而起点 $D$ 在该群作用下不变 ⇒ 三个顶点上的方案数恒相等 ✓ ∎

**引理 2（转移正确）**：$s_{n+1}=3t_n$、$t_{n+1}=s_n+2t_n$。

**证明**：$K_4$ 中 $D$ 与 $A,B,C$ 各有一条边 ⇒ 到 $D$ 的走法 = 三个非 $D$ 顶点各自的走法之和 $=3t_n$ ✓；到 $A$ 的走法 = 从 $D$ 来（$s_n$）或从 $B,C$ 来（各 $t_n$）$=s_n+2t_n$ ✓ ∎

**引理 3（闭式）**：$s_n=\dfrac{3^n+3(-1)^n}{4}$。

**证明**：由引理 2，$s_{n+1}=3t_n$、$t_{n+1}=s_n+2t_n$ ⇒ $s_{n+1}=3t_n=3(s_{n-1}+2t_{n-1})=3s_{n-1}+6t_{n-1}$，又 $3t_{n-1}=s_n$ ⇒ $s_{n+1}=3s_{n-1}+2s_n$。特征方程 $x^2=2x+3$ ⇒ $x=3,-1$；代入 $s_0=1,s_1=0$ 解得 $s_n=\frac{3^n+3(-1)^n}{4}$ ✓ ∎

**定理**：程序输出正确。

**证明**：由引理 3 的闭式（$n\ge0$）在模 $10^9+7$ 下计算（$4$ 有逆元，$10^9+7$ 为素数）✓ ∎

## 5. 复杂度分析

- **时间**：$O(\log n)$（快速幂），实测 < 2 ms。
- **空间**：$O(1)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
static const ll MOD = 1000000007;

static ll pw(ll b, ll e, ll m) {
    ll r = 1 % m;
    b %= m;
    while (e > 0) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; }
    return r;
}

int main() {
    ll n;
    if (scanf("%lld", &n) != 1) return 0;
    // 长度为 n 的闭合游走数 = (3^n + 3*(-1)^n) / 4
    ll inv4 = pw(4, MOD - 2, MOD);
    ll res = (pw(3, n, MOD) + (n % 2 == 0 ? 3 : MOD - 3)) % MOD;
    printf("%lld\n", res * inv4 % MOD);
    return 0;
}
```

### Python3

```python
import sys

MOD = 1000000007


def main():
    n = int(sys.stdin.read().split()[0])
    res = (pow(3, n, MOD) + (3 if n % 2 == 0 else MOD - 3)) % MOD
    print(res * pow(4, MOD - 2, MOD) % MOD)


main()
```

## 7. 边界情况与易错点

1. **$n=0$**：题面 $n\ge1$；闭式给 1（自身到自身 0 步）。
2. **$(-1)^n$ 处理**：$n$ 偶加 3、奇减 3（模意义下加 $MOD-3$）。
3. **逆元**：$4^{-1}$ 用费马小定理。
4. **$n$ 到 $10^7$**：闭式 $O(\log n)$ 更稳（避免 $O(n)$ 在 Python 上超时）。
5. **模运算**：每步取模。
6. **`n % 2`**：用 64 位。
7. **输出**：单个整数。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/166/E_四面体上的闭合游走.md`
- **官方样例**：$2/2$ 通过（`3`、`21`）。
- **独立对拍**：另写 $O(n)$ 递推 $s,t$ 的独立实现，对 $200$ 组随机 $n\le100$ 比较，全部一致。
- **性能**：$n=10^7$ 单次 < 2 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 166D Shoe Store](https://codeforces.com/problemset/problem/166/D)：同场 D 题。
- [LeetCode 935. 骑士拨号器](https://leetcode.cn/problems/knight-dialer/)：图上走 $n$ 步计数。
- [Luogu P1939 矩阵加速（数列）](https://www.luogu.com.cn/problem/P1939)：矩阵快速幂。

**延伸思考**：

1. **若四面体换成 $K_n$**：递推 $s_{n+1}=(n-1)t_n$、$t_{n+1}=s_n+(n-2)t_n$，解特征方程即可。
2. **若要求恰好访问所有顶点**：需要容斥/状态压缩。
3. **若边有重数**：把转移系数换成边权。
