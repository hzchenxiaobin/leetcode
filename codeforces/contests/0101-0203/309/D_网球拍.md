# Codeforces 309D Tennis Rackets 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/309/D
- **比赛来源**：Croc Champ 2013 - Finals (online version, Div. 1) · Problem D（UTC 2013-05-25）
- **难度**：2700
- **标签**：组合计数、几何
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：正三角形三条边各被 $n$ 个洞等分成 $n+1$ 段。每边**两端各 $m$ 个洞**只用于通风、不能穿网；其余洞可以穿网。求"三边各取一个可用洞、且三点构成**钝角**三角形"的方案数（三条边各取一点，位置不同即不同方案）。

**约束**：$1 \le n \le 32000$，$0 \le m \le n/2$。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 0

输出：
9
```

官方样例 2：

```text
输入：
4 0

输出：
24
```

官方样例 3：

```text
输入：
10 1

输出：
210
```

官方样例 4：

```text
输入：
8 4

输出：
0
```

**观察 1（钝角至多一个）**：每个三角形至多一个钝角 → 总数 $=3\times$（"钝角出现在 AB 边上的那个点"的方案数）。

**观察 2（坐标化）**：设 $L=n+1$，三角形取 $A(0,0)$、$B(1,0)$、$C(\tfrac12,\tfrac{\sqrt3}2)$。三边上的点用**洞的编号** $U,T,S \in [m+1,\ n-m]$ 表示：

$$P=\Bigl(\tfrac UL,0\Bigr),\quad Q=\Bigl(1-\tfrac{T}{2L},\ \tfrac{T}{L}\cdot\tfrac{\sqrt3}2\Bigr),\quad R=\Bigl(\tfrac{S}{2L},\ \tfrac{S}{L}\cdot\tfrac{\sqrt3}2\Bigr).$$

**观察 3（钝角判据）**：$P$ 处钝角 ⇔ $(Q-P)\cdot(R-P)<0$。把 $\tfrac{\sqrt3}2$ 的系数单独代入，利用 $\bigl(\tfrac{\sqrt3}2\bigr)^2=\tfrac34$：

$$\Bigl(1-\tfrac{T}{2L}-\tfrac UL\Bigr)\Bigl(\tfrac{S}{2L}-\tfrac UL\Bigr)+\tfrac{3TS}{4L^2}<0 .$$

两边乘 $4L^2$ 并整理得

$$\boxed{\,S\,(L-U+T) < U\,(2L-T-2U)\,}$$

（用整数算，无浮点误差）。

**观察 4（固定 $(T,U)$ 时 $S$ 是前缀）**：$L-U+T>0$ 恒成立，故 $\{S: \text{满足上式}\}$ 是 $[1,1]$ 内的一段前缀，上界

$$S \le \Bigl\lfloor \frac{U(2L-T-2U)-1}{L-U+T}\Bigr\rfloor .$$

于是对每个 $(T,U)$ 用 $O(1)$ 算出可用的 $S$ 个数（再截断到 $[m+1, n-m]$），总 $O(n^2)$。

**样例 1 验证**：$n=3,m=0,L=4$，$U,T,S\in[1,3]$；枚举得 3 个"P 处钝角"的构型 → $3\times3=9$ ✓。

## 3. 解题思路

![钝角判据](../../../images/cf309d_dot.svg)

枚举 $(T,U)$，用整数公式算 $S$ 的可行个数并累加，最后乘 3。

## 4. 正确性证明

**引理 1**：$P$ 处为钝角 ⇔ 上式成立。

**证明**：钝角 ⇔ 两边向量点积为负；代入坐标并乘正数 $4L^2$ 得该式 ✓（$\tfrac{\sqrt3}{2}$ 的乘积用 $\tfrac34$ 化简）✓。∎

**引理 2**：固定 $(T,U)$ 时合法的 $S$ 恰为 $[m+1,\ \min(n-m,\ \lfloor\frac{U(2L-T-2U)-1}{L-U+T}\rfloor)]$。

**证明**：引理 1 的不等式对 $S$ 线性且系数 $L-U+T>0$，故解集是前缀；整数解的上界由取下整得到 ✓。∎

**引理 3**：钝角三角形数目 = 3 × （$P$ 处钝角的数目）。

**证明**：三角形至多一个钝角，且三个"钝角位置"在正三角形的旋转对称下计数相同 ✓。∎

**定理**：算法输出正确答案。

**证明**：由引理 2 逐个 $(T,U)$ 精确计数、引理 3 乘 3 ✓。∎

## 5. 复杂度分析

- **时间**：$O((n-2m)^2)$，最坏 $n=32000$ 约 $10^9$ 次内层（实测 755 ms，内层只有几次整数运算）。
- **空间**：$O(1)$。
- **与时限的关系**：时限 3 s，$n=32000, m=0$ 实测端到端 755 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main(){
    ll n, m; if(scanf("%lld %lld",&n,&m)!=2) return 0;
    ll L = n+1;
    ll lo = m+1, hi = n-m;                 // 可用洞的编号范围
    if(lo > hi){ printf("0\n"); return 0; }
    ll tot=0;
    for(ll T=lo; T<=hi; T++){
        for(ll U=lo; U<=hi; U++){
            ll D = L - U + T;              // >0
            ll E = 2*L - T - 2*U;
            if(E <= 0) continue;
            ll mx = (U*E - 1) / D;         // S < U*E/D
            if(mx <= m) continue;
            if(mx > hi) mx = hi;
            tot += mx - m;
        }
    }
    printf("%lld\n", 3*tot);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    n, m = map(int, sys.stdin.buffer.read().split()[:2])
    L = n+1
    lo, hi = m+1, n-m
    if lo > hi:
        print(0); return
    tot = 0
    for T in range(lo, hi+1):
        for U in range(lo, hi+1):
            D = L - U + T
            E = 2*L - T - 2*U
            if E <= 0: continue
            mx = (U*E - 1)//D
            if mx <= m: continue
            if mx > hi: mx = hi
            tot += mx - m
    print(3*tot)
main()
```

Python 版是 $O(n^2)$ 的纯循环，$n=32000$ 时过慢，**建议提交 C++/PyPy3**。

## 7. 边界情况与易错点

1. **$m=0$**：所有洞可用（样例 1、2）。
2. **$2m \ge n$**：可用洞为空 → 答案 0（样例 4）。
3. **上界截断**：$S$ 的上界要 `min` 到 $n-m$，并减去 $m$（编号从 $m+1$ 开始）。
4. **整数运算**：不要用浮点算点积，$4L^2$ 通分后全整数。
5. **乘 3**：答案要 ×3（三个可能的钝角位置）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：4 / 4 通过（9、24、210、0），C++ 与 Python 一致。
- **独立 oracle 对拍**：oracle **直接枚举三元组 $(U,T,S)$**，用 `fractions.Fraction` 精确计算点积判钝角（不走公式推导）。覆盖 **$n=1\ldots12$ 全部 48 组 + $n=13\ldots30$ 全部 207 组 = 255 组**，**255 / 255 全部一致**。
- **最大约束性能**：$n=32000, m=0$，实测端到端 755 ms（答案 20194172518050）。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 309C Memory for Arrays](https://codeforces.com/problemset/problem/309/C)：同场 C 题。
- [Codeforces 309E Sheep](https://codeforces.com/problemset/problem/309/E)：同场 E 题。

**延伸思考**：

1. **如果要求锐角三角形**：把判据改成三个点积都为正。
2. **如果 $n$ 大到 $10^9$**：需要对 $\lfloor \frac{U(2L-T-2U)-1}{L-U+T}\rfloor$ 做 floor-sum 类的加速。
