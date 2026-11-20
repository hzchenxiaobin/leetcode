# Codeforces 109E 幸运区间平移 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/109/E
- **比赛来源**：Codeforces Beta Round 84 (Div. 1 Only) · Problem E（UTC 2011-08-29）
- **难度**：2700
- **标签**：数位分析、周期、贪心构造
- **评测类型**：普通
- **限制**：时间 4 s / 内存 512 MB

**题意**：记 $F(x)$ 为 $x$ 的十进制表示中数字 4 与 7 的个数。给定 $a,l$（$1\le a,l\le10^9$），求最小的 $b>a$，使得

$$F(a)=F(b),\quad F(a+1)=F(b+1),\quad\dots,\quad F(a+l-1)=F(b+l-1).$$

**约束**：

- $a,l\le10^9$：$b$ 可能达到 $2\times10^{10}$ 量级（$b=a+10^k$，$10^k>a+l$），必须 64 位。
- 不能枚举 $b$：答案可能离 $a$ 很远（例：$a=777777777,l=1$ 时答案是 $1444444444$，差 $6.7\times10^8$）。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
7 4
输出：
17
```

官方样例二：

```text
输入：
4 7
输出：
14
```

**样例一走查**：区间 $[7,10]$ 的 $F$ 值：$F(7)=1,F(8)=0,F(9)=0,F(10)=0$。看 $b=17$：$F(17)=1,F(18)=0,F(19)=0,F(20)=0$ ✓ 完全相同，且没有更小的 $b$（$8\ldots16$ 都对不上）。

**样例二走查**：$[4,10]$ 的 $F=[1,0,0,1,0,0,0]$；$b=14$ 时 $[14,20]=[1,0,0,1,0,0,0]$ ✓ 相同。

![把窗口按 10^M 分块](../../../images/cf109e_reduce.svg)

**观察一**：$F$ 是"逐位可加"的：$F(x)=F(\lfloor x/10^k\rfloor)+F(x\bmod 10^k)$（低 $k$ 位补前导零不影响 4/7 计数）。

**观察二**：第 $k$ 位的"是否 4 或 7"随 $x$ 变化是一个**周期为 $10^{k+1}$ 的方波**（高电平在 $[4\cdot10^k,5\cdot10^k)$ 与 $[7\cdot10^k,8\cdot10^k)$）。窗口长度一旦不小于周期，窗口内容就把相位"钉死"了。

## 3. 解题思路

### 3.1 为什么位移必须是 $10$ 的幂的倍数

记 $d=b-a$，并考虑任意一个数位 $k\ge0$。要求 $F(a+i)=F(b+i)$ 对窗口内所有 $i$ 成立，则第 $k$ 位的指示序列也必须逐位相同。

该指示序列周期为 $P_k=10^{k+1}$，且在一个周期内**没有非平凡的旋转对称**（高电平是两段长 $10^k$ 的区间，间隔各 $2\cdot10^k$，任何非零旋转都会把一段高电平挪进低电平）。因此当 $l\ge P_k$ 时，长度 $l$ 的窗口完整包含一个周期，窗口内容唯一决定相位 $\Rightarrow d\equiv0\pmod{P_k}$。

取 $M$ 为**不超过 $l$ 的最大 $10$ 的幂**，就有

$$d=t\cdot M,\qquad t\ge1 .$$

### 3.2 降维到"块下标"

由观察一：

$$F(a+i)=F\!\left(\left\lfloor\frac{a+i}{M}\right\rfloor\right)+F\bigl((a+i)\bmod M\bigr),$$

而 $d=tM$ 不改变低 $M$ 位（$(b+i)\bmod M=(a+i)\bmod M$），所以条件等价于

$$\boxed{F(p+t)=F(p)\quad\text{对窗口内出现的每个块下标 } p=\left\lfloor\frac{x}{M}\right\rfloor}$$

窗口长度 $l<10M$，因此跨过的块数不超过 $10$ 个。若恰好跨 $10$ 个块，还可以用同样的理由再降一层（此时 $t$ 必须是 $10$ 的倍数），于是递归到"块数 $\le9$"。

### 3.3 基例：块数 $\le9$ 时求最小 $t$

![低两位枚举 + 数位贪心](../../../images/cf109e_digits.svg)

此时 $M=1$（或已降到很小），问题变成：**求最小的 $b>p_0$，使 $F(b+i)=F(p_0+i)$（$i<r\le9$）**。

因为 $i\le8$，加法只会影响 $b$ 的低两位（最多进位一次）。写 $b=100H+L$（$L\in[0,100)$，$H\ge0$），则

$$F(b+i)=F(H+c_i)+F\big((L+i)\bmod 100\big),\qquad c_i=[L+i\ge100].$$

对每个 $L$ 逐个检查：把 $i$ 按 $c_i=0/1$ 分成两组，每组都要求 $F(H)$（或 $F(H+1)$）等于一个确定的值；组内不一致则该 $L$ 不可行。

于是只剩一个子问题：**求最小的 $H\ge H_0$ 使 $F(H)=u_0$、$F(H+1)=u_1$**（某个约束可缺省）。按 $H$ 末尾连续 9 的个数 $j$ 与末尾 9 前面的数字 $d$ 分类：

$$H=P\cdot10^{j+1}+d\cdot10^j+(10^j-1)\ \ (0\le d\le8),$$

于是

$$F(H)=F(P)+\text{lucky}(d),\qquad F(H+1)=F(P)+\text{lucky}(d+1).$$

两式相减就能判断 $d$ 是否可行，随后只需：

> **求最小的 $P\ge P_0$ 使 $F(P)=u$。**

这个用数位贪心即可：从右往左找到第一个可以"增大"的数位，后面的位填最少量的 4（0 比 4 小，所以 0 放前面）；若同位数做不到，就加一位（形如 `1` 后接若干个 0 与 4）。

最后取所有 $L$ 中最小的 $b$，再乘回降维时累积的 $10^k$ 与 $M$，得到 $b=a+tM$。

### 3.4 样例走查

- $a=7,l=4$：$M=1$（$l<10$），块数 $r=4$，基例求得最小 $b=17$ ✓。
- $a=4,l=7$：$M=1$，$r=7$，求得 $b=14$ ✓。
- $a=777777777,l=1$：$M=1$，$r=1$；要最小 $b>a$ 且 $F(b)=9$。$L=44$ 时 $F(44)=2$，需 $F(H)=7$；最小的 8 位数 $H\ge7777778$ 且含 7 个幸运位是 $14444444$ → $b=1444444444$ ✓（比 $a+10^9$ 更小）。

## 4. 正确性证明

**引理 1**：对任意 $k\ge0$，$F(x)=F(\lfloor x/10^k\rfloor)+F(x\bmod 10^k)$。

**证明**：十进制表示中，高位部分与低 $k$ 位互不重叠；低位的补前导零不含 4/7，不影响计数 ✓。∎

**引理 2**：若 $l\ge10^{k+1}$，则任何合法的 $d=b-a$ 满足 $d\equiv0\pmod{10^{k+1}}$。

**证明**：设 $s_k(x)=[\,x\text{ 的第 }k\text{ 位}\in\{4,7\}\,]$。$s_k$ 周期为 $10^{k+1}$，在一个周期内高电平为 $[4\cdot10^k,5\cdot10^k)$ 与 $[7\cdot10^k,8\cdot10^k)$（两段、每段长 $10^k$，彼此间隔 $2\cdot10^k$）。$F(a+i)=F(b+i)$ 对所有 $i<l$ 成立 $\Rightarrow$ $s_k(a+i)=s_k(b+i)$，即两个长度 $\ge10^{k+1}$ 的窗口内容相同 ⇒ 相位相同 ⇒ $b\equiv a\pmod{10^{k+1}}$ ✓。∎

**引理 3**：令 $M$ 为不超过 $l$ 的最大 $10$ 的幂，则合法 $d$ 必为 $tM$ 形式；且 $d=tM$ 合法 $\iff$ 对窗口内每个块下标 $p$ 有 $F(p+t)=F(p)$。

**证明**：前半由引理 2（$M=10^{k+1}$ 对应的那个 $k$）。后半：由引理 1 展开 $F(a+i)$ 与 $F(b+i)$，低 $M$ 位两项相同，故条件等价 ✓。∎

**引理 4**：块数 $\le9$ 时，3.3 的枚举覆盖了所有可能的 $b$，且对每个 $L$ 求出的 $H$ 是最小的。

**证明**：任何 $b$ 都有唯一的 $L=b\bmod100$ 与 $H=\lfloor b/100\rfloor$，落在某个 $L$ 的枚举中；进位关系 $c_i=[L+i\ge100]$ 精确决定了 $F(b+i)$ 的分解，因此 $u_0,u_1$ 的约束是充要条件 ✓。$H$ 的最小性由"按末尾 9 的个数 $j$ 与数字 $d$ 分类"的穷举（$j\le13$、$d\le8$）加上子程序"最小 $P\ge P_0$ 且 $F(P)=u$"的最小性保证 ✓。

**子引理（数位贪心的最小性）**：若存在 $P\ge P_0$ 且 $F(P)=u$，3.3 的子程序给出其中最小者。

**证明**：最小的 $P>P_0$ 必在某个数位上大于 $P_0$ 的对应位、且更低的位任意（更高位与 $P_0$ 相同，或位数更多）。程序从最低位向上枚举"第一个增大的位置"并取后缀最小的可行填法（先 0 后 4），故给出最小 ✓。∎

**定理**：算法输出最小的合法 $b$。

**证明**：由引理 3，合法 $b$ 都是 $a+tM$ 形式且等价于块级条件；由引理 4，块级问题被精确求解并取到最小 $t$；降维时每次乘回 $10$ 不改变最小性（$t$ 必须是 $10$ 的倍数，逐层等价）✓。∎

## 5. 复杂度分析

- **时间**：块数 $\le10$，基例枚举 $100$ 个 $L$，每个 $L$ 做常数次数位贪心（$\le13\times9$ 种分类）⇒ 常数级，实测 $2$ ms。
- **空间**：$O(1)$。
- **数值范围**：$b\le a+10^{11}$，`long long` 足够；中间量 $P\cdot10^{j+1}$ 也在 $10^{12}$ 内。
- **与时限的关系**：4 s 下实测约 $2$ ms（C++），Python 约 $21$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

static int F(ll x) {
    int c = 0;
    while (x) { int d = (int)(x % 10); if (d == 4 || d == 7) ++c; x /= 10; }
    return c;
}

static ll ipow10(int k) { ll r = 1; while (k-- > 0) r *= 10; return r; }

// 最小的 P >= P0 且 F(P) == u；无解返回 -1
static ll smallest_ge(ll P0, int u) {
    if (u < 0) return -1;
    if (u > 25) return -1;
    if (F(P0) == u) return P0;
    if (P0 == 0) {                    // 0 本身 F=0，u>0 时取 u 个 4
        ll val = 0;
        for (int k = 0; k < u; ++k) val = val * 10 + 4;
        return val;
    }
    vector<int> digs;
    for (ll t = P0; t > 0; t /= 10) digs.push_back((int)(t % 10));
    reverse(digs.begin(), digs.end());
    int n = (int)digs.size();
    vector<int> pref(n + 1, 0);
    for (int i = 0; i < n; ++i) pref[i + 1] = pref[i] + ((digs[i] == 4 || digs[i] == 7) ? 1 : 0);
    // 在某个位置 i 上把数字增大
    for (int i = n - 1; i >= 0; --i) {
        for (int d = digs[i] + 1; d <= 9; ++d) {
            int cnt = pref[i] + ((d == 4 || d == 7) ? 1 : 0);
            int rem = n - i - 1;
            int need = u - cnt;
            if (need < 0 || need > rem) continue;
            ll val = 0;
            for (int k = 0; k < i; ++k) val = val * 10 + digs[k];
            val = val * 10 + d;
            for (int k = 0; k < rem - need; ++k) val = val * 10;        // 0
            for (int k = 0; k < need; ++k) val = val * 10 + 4;           // 4
            return val;
        }
    }
    // 位数增加
    for (int len = n + 1; len <= n + 2; ++len) {
        if (u < 0 || u > len) continue;
        if (u <= len - 1) {
            ll val = 1;
            for (int k = 0; k < len - 1 - u; ++k) val = val * 10;
            for (int k = 0; k < u; ++k) val = val * 10 + 4;
            return val;
        } else {
            ll val = 0;
            for (int k = 0; k < len; ++k) val = val * 10 + 4;
            return val;
        }
    }
    return -1;
}

static ll ceil_div(ll x, ll y) { if (x <= 0) return 0; return (x + y - 1) / y; }

// 最小的 H >= H0 满足 F(H) == u0（u0<0 表示无约束）与 F(H+1) == u1；无解返回 -1
static ll smallest_H(ll H0, int u0, int u1) {
    if (u0 < 0 && u1 < 0) return H0;
    if (u1 < 0) return smallest_ge(H0, u0);
    if (u0 < 0) { ll v = smallest_ge(H0 + 1, u1); return v < 0 ? -1 : v - 1; }
    ll best = -1;
    // 全 9 的特例：H = 10^m - 1，H+1 = 10^m
    if (u0 == 0 && u1 == 1) {
        int m = 1;
        while (ipow10(m) - 1 < H0) ++m;
        best = ipow10(m) - 1;
    }
    for (int j = 0; j <= 13; ++j) {
        ll tj = ipow10(j);
        ll p10 = tj * 10;
        for (int d = 0; d <= 8; ++d) {
            int ld = (d == 4 || d == 7) ? 1 : 0;
            int ld1 = ((d + 1) == 4 || (d + 1) == 7) ? 1 : 0;
            if (u0 - ld != u1 - ld1) continue;
            int uP = u0 - ld;
            ll base = (ll)d * tj + (tj - 1);
            ll P0 = ceil_div(H0 - base, p10);
            ll P = smallest_ge(P0, uP);
            if (P < 0) continue;
            ll H = P * p10 + base;
            if (F(H) == u0 && F(H + 1) == u1) {
                if (best < 0 || H < best) best = H;
            }
        }
    }
    return best;
}

// 最小的 b > p0 使 F(b+i) == F(p0+i)（i < r），返回 b - p0
static ll solve_base(ll p0, int r) {
    ll best = -1;
    for (int L = 0; L < 100; ++L) {
        ll H0 = ceil_div(p0 + 1 - L, 100);
        bool has0 = false, has1 = false, ok = true;
        int u0 = 0, u1 = 0;
        for (int i = 0; i < r; ++i) {
            int need = F(p0 + i);
            int c = (L + i >= 100) ? 1 : 0;
            int low = (L + i) % 100;
            int rem = need - F(low);
            if (rem < 0) { ok = false; break; }
            if (c == 0) {
                if (!has0) { has0 = true; u0 = rem; } else if (u0 != rem) { ok = false; break; }
            } else {
                if (!has1) { has1 = true; u1 = rem; } else if (u1 != rem) { ok = false; break; }
            }
        }
        if (!ok) continue;
        ll H = smallest_H(H0, has0 ? u0 : -1, has1 ? u1 : -1);
        if (H < 0) continue;
        ll b = 100 * H + L;
        if (b > p0 && (best < 0 || b < best)) best = b;
    }
    return best < 0 ? -1 : best - p0;
}

int main() {
    ll a, l;
    if (scanf("%lld %lld", &a, &l) != 2) return 0;
    ll M = 1;
    while (M * 10 <= l) M *= 10;
    ll p0 = a / M;
    ll p1 = (a + l - 1) / M;
    ll mult = M;
    int guard = 0;
    while (p1 - p0 + 1 >= 10 && guard < 5) {
        mult *= 10;
        p0 /= 10;
        p1 /= 10;
        ++guard;
    }
    ll t = solve_base(p0, (int)(p1 - p0 + 1));
    printf("%lld\n", a + t * mult);
    return 0;
}
```

### Python3

```python
import sys


def F(x):
    c = 0
    while x:
        d = x % 10
        if d == 4 or d == 7: c += 1
        x //= 10
    return c


def smallest_ge(P0, u):
    if u is None or u < 0: return None
    if F(P0) == u: return P0
    if P0 == 0:
        val = 0
        for _ in range(u): val = val * 10 + 4
        return val
    s = str(P0); n = len(s)
    digs = [int(c) for c in s]
    pref = [0]*(n+1)
    for i in range(n): pref[i+1] = pref[i] + (1 if digs[i] in (4,7) else 0)
    for i in range(n-1, -1, -1):
        for d in range(digs[i]+1, 10):
            cnt = pref[i] + (1 if d in (4,7) else 0)
            rem = n - i - 1
            need = u - cnt
            if 0 <= need <= rem:
                val = 0
                for x in digs[:i] + [d] + [0]*(rem-need) + [4]*need:
                    val = val*10 + x
                return val
    for length in range(n+1, n+3):
        if 0 <= u <= length:
            if u <= length - 1:
                val = 1
                for x in [0]*(length-1-u) + [4]*u:
                    val = val*10 + x
                return val
            else:
                val = 0
                for _ in range(length): val = val*10 + 4
                return val
    return None


def ceil_div(x, y):
    if x <= 0: return 0
    return (x + y - 1) // y


def smallest_H(H0, u0, u1):
    if u0 is None and u1 is None: return H0
    if u1 is None: return smallest_ge(H0, u0)
    if u0 is None:
        v = smallest_ge(H0+1, u1)
        return None if v is None else v-1
    best = None
    if u0 == 0 and u1 == 1:
        m = 1
        while 10**m - 1 < H0: m += 1
        best = 10**m - 1
    for j in range(0, 14):
        tj = 10**j
        for d in range(0, 9):
            ld = 1 if d in (4,7) else 0
            ld1 = 1 if (d+1) in (4,7) else 0
            if u0 - ld != u1 - ld1: continue
            uP = u0 - ld
            base = d*tj + (tj - 1)
            P0 = ceil_div(H0 - base, 10**(j+1))
            P = smallest_ge(P0, uP)
            if P is None: continue
            H = P*10**(j+1) + base
            if F(H) == u0 and F(H+1) == u1:
                if best is None or H < best: best = H
    return best


def solve_base(p0, r):
    best = None
    for L in range(100):
        H0 = ceil_div(p0 + 1 - L, 100)
        u0 = u1 = None; ok = True
        for i in range(r):
            need = F(p0 + i)
            c = 1 if L + i >= 100 else 0
            low = (L + i) % 100
            rem = need - F(low)
            if rem < 0:
                ok = False; break
            if c == 0:
                if u0 is None: u0 = rem
                elif u0 != rem: ok = False; break
            else:
                if u1 is None: u1 = rem
                elif u1 != rem: ok = False; break
        if not ok: continue
        H = smallest_H(H0, u0, u1)
        if H is None: continue
        b = 100*H + L
        if b > p0 and (best is None or b < best): best = b
    return None if best is None else best - p0


def solve(a, l):
    M = 1
    while M * 10 <= l: M *= 10
    p0 = a // M
    p1 = (a + l - 1) // M
    mult = M
    guard = 0
    while p1 - p0 + 1 >= 10 and guard < 5:
        mult *= 10
        p0 //= 10
        p1 //= 10
        guard += 1
    t = solve_base(p0, p1 - p0 + 1)
    return a + t * mult


def main() -> None:
    d = sys.stdin.buffer.read().split()
    if not d:
        return
    a = int(d[0]); l = int(d[1])
    sys.stdout.write(str(solve(a, l)) + "\n")


main()
```

## 7. 边界情况与易错点

1. **$l\le9$ 时 $M=1$**：此时没有任何强制同余，"位移"可以是任意值（如 $a=4,l=7$ 答案是 $14$，$d=10$ 恰好是 $10$ 的倍数，但 $a=4,l=2$ 的答案 $b=7$，$d=3$ 不是）。
2. **块数达到 10**：必须再降一层（$t$ 为 $10$ 的倍数），否则会漏掉约束。
3. **进位**：$b+i$ 的低两位相加可能 $\ge100$，此时高位用 $H+1$——忘记进位会把很多情形算错。
4. **`smallest_ge` 的 $P_0=0$**：不能按"取数位"处理，要特判（返回 $u$ 个 4）。
5. **位数增长**：同位数无解时要加一位（如 $a=999,\ F=3$ 需 $1444$ 这类），只在本位内找会漏。
6. **64 位**：$b$ 可达 $2\times10^{10}$，中间量 $P\cdot10^{j+1}$ 也可能超 `int`。
7. **$a$ 很大且 $F(a)$ 很小**：如 $a=10^9$，需要向上找很久才遇到同样 $F$ 的数，算法靠数位构造直接跨过。
8. **$l$ 很大**：$M$ 大，块数少，反而更快；不要误以为大 $l$ 更难。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：2 / 2 通过（`17`、`14`），C++ 与 Python 输出一致。
- **独立暴力对拍**：暴力从 $a+1$ 向上逐个检查 $F$ 序列是否与 $[a,a+l-1]$ 相同（$l\le25$ 时窗口很短、可行）。
  - 随机 $a\le8000$、$l\le25$：**400 组**（C++ 与暴力一致）；
  - 结构化边界（$a$ 取 $1,4,7,9,10,40,70,99,100,\dots,777777$，$l$ 取 $1,2,3,4,7,9,10,11,\dots,1000$）：**280 组**一致；
  - Python 版另跑 **300 组**随机小数据一致。
- **大范围抽查**：随机 $a,l\le10^9$ 的 **80 组**，对每个答案检查 $b>a$ 且在窗口内随机采样 200 个位置都有 $F(a+i)=F(b+i)$；另把 C++ 与 Python 在 **552 组**输入（含 $a$ 或 $l$ 取 $10^9$ 等极值）上互查，**全部一致**。
- **已知难题手测**：$a=777777777,l=1$ → $1444444444$（与手工推导一致）；$a=4,l=2$ → $7$；$a=40,l=10$ → $70$。
- **最大约束性能**：$a=l=10^9$ 时 C++ 端到端约 $2$ ms，Python 约 $21$ ms。
- **图片校验**：`cf109e_reduce.svg`、`cf109e_digits.svg` 均通过 `xml.etree.ElementTree.parse`，含 `feTurbulence` 与手写体字体族，文本包围盒未越出 `viewBox`。
- **公式校验**：KaTeX（`throwOnError`）渲染无报错；无 `---` 分隔线。
- **复核状态**：verified（样例、对拍、性能、图片、公式均实跑通过）。

## 相关题目与扩展

- [Codeforces 109A 最小幸运数位和](https://codeforces.com/problemset/problem/109/A)、[109B Lucky Probability](https://codeforces.com/problemset/problem/109/B)、[109C Lucky Tree](https://codeforces.com/problemset/problem/109/C)、[109D Lucky Sorting](https://codeforces.com/problemset/problem/109/D)：同场其余题。
- [Codeforces 110A Nearly Lucky Number](https://codeforces.com/problemset/problem/110/A)、[110B Lucky String](https://codeforces.com/problemset/problem/110/B)：同轮 Div.2。
- [Codeforces 1213C Book Reading](https://codeforces.com/problemset/problem/1213/C)：按周期分块计数。
- [LeetCode 902. 最大为 N 的数字组合](https://leetcode.cn/problems/numbers-at-most-n-given-digit-set/)：数位构造 + 贪心最小。

**延伸思考**：

1. **如果 $F$ 统计的是"数字 4 的个数"**：方波只有一段高电平，周期结构更简单，但对称性分析类似。
2. **如果要求 $b<a$**：对称地向下找，数位贪心改成"最大不超过"。
3. **如果 $l$ 到 $10^{18}$**：$M$ 最大 $10^{18}$，块数仍是 $\le10$，算法不变，只需 128 位整数。
4. **如果要求所有满足条件的 $b$**：会是一个等差数列族（每个 $L$、每个 $j$ 对应一族），可枚举输出。

