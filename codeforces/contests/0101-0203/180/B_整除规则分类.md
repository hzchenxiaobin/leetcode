# Codeforces 180B 整除规则分类 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/180/B
- **比赛来源**：Codeforces Round 116 (Div. 2, ACM-ICPC Rules) · Problem B（UTC 2012-04-22）
- **难度**：2300
- **标签**：数论、分类讨论、整除、质因数分解
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：给定进制 $b$ 和除数 $d$（$2 \le b,d \le 100$），判断在 $b$ 进制下 $d$ 的整除规则属于哪一类，按 `2-type`、`3-type`、`11-type`、`6-type`、`7-type` 的顺序取第一个成立的；若是 `2-type`，第二行输出最少需要看末尾多少位。

三类基本规则的定义（题面）：

- **2 类**：只看末尾若干位数字；
- **3 类**：各位数字之和能被 $d$ 整除；
- **11 类**：奇数位数字和与偶数位数字和之差能被 $d$ 整除；
- **6 类**：把 $d$ 分解成几个因子，分别用上述三类规则；
- **7 类**：都不成立（十进制下最小的例子是 7）。

**约束**（原样摘自题面 `inputFormat.en`）：

- 一行两个整数 $b, d$，$2 \le b, d \le 100$。
- 输出一行规则类型；若为 `2-type` 再输出一行位数。

**约束对算法的限制**：

- $b,d$ 极小（$\le 100$），所以可以放心地枚举 $d$ 的所有因子、对所有 $(b,d)$ 组合做分类。
- 没有多测，$O(\sqrt d)$ 的质因数分解、$O(\tau(d)^3)$ 的因子枚举都瞬间完成。
- 真正的难点是**把三类规则的充要条件推对**，以及 6 类的分解判定。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
10 10

输出：
2-type
1
```

官方样例 2（输入 / 输出原样）：

```text
输入：
2 3

输出：
11-type
```

**样例 1**：$b=10,d=10$。任何数模 10 只取决于最后一位，所以 $10 \mid N \iff$ 末位为 0，只需要 1 位 → `2-type` / `1`。

**样例 2**：$b=2,d=3$。$3 \nmid 2^L$，$2 \not\equiv 1 \pmod 3$；但 $2 \equiv -1 \pmod 3$，于是 $N = \sum a_i 2^i \equiv \sum a_i (-1)^i \pmod 3$，正是 11 类（交错和）→ `11-type`。题面 hint 用 $21_{10}=10101_2$ 演示了这个规则。

**观察 1（2 类的充要条件）**：设一个数 $N = H\cdot b^L + R$（$R$ 是末尾 $L$ 位）。若 $d \mid b^L$，则 $N \equiv R \pmod d$，只看末尾 $L$ 位即可；反之若 $d \nmid b^L$，则存在两个数末 $L$ 位相同但相差 $b^L$，它们的整除性不同，规则不成立。所以 **2 类 $\iff \exists L: d \mid b^L$**，最少的 $L$ 就是最小的那个。

**观察 2（3 类）**：$N = \sum a_i b^i \equiv \sum a_i \pmod d$ 对所有 $N$ 成立 $\iff b \equiv 1 \pmod d$，即 $d \mid b-1$。

**观察 3（11 类）**：$N \equiv \sum a_i (-1)^i \pmod d$ 对所有 $N$ 成立 $\iff b \equiv -1 \pmod d$，即 $d \mid b+1$。

**观察 4（6 类）**：若 $d = d_2 d_3 d_{11}$ 且三者**两两互质**，并且 $d_2$ 满足 2 类、$d_3$ 满足 3 类、$d_{11}$ 满足 11 类，那么由中国剩余定理，$d \mid N \iff d_2 \mid N$ 且 $d_3 \mid N$ 且 $d_{11}\mid N$，于是三条规则「与」起来就是 $d$ 的规则。题面的例子：$6=2\times3$（2 类 + 3 类）、$66=2\times3\times11$（三类都有）。

**观察 5（7 类）**：以上都不成立。十进制下最小的例子是 $d=7$：$7 \nmid 10^L$、$10 \not\equiv \pm1 \pmod 7$，而 7 是质数无法分解成两个互质因子。

**自造样例**（标注「自造」，输出由程序实测）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `10 8` | `2-type` / `3` | $8\mid 1000$ |
| `10 18` | `6-type` | $2\times 9$：2 类 + 3 类 |
| `10 12` | `6-type` | $4\times 3$ |
| `10 66` | `6-type` | $2\times3\times11$ |
| `10 7` | `7-type` | 十进制下最小的 7 类 |
| `3 8` | `7-type` | $3^2\equiv1\pmod 8$ 但规则不是三类之一 |
| `5 8` | `7-type` | $5+1=6$、$5-1=4$ 都不被 8 整除 |

## 3. 解题思路

### 3.1 朴素做法与瓶颈

题目只要求分类，$b,d\le100$，任何多项式做法都能过。瓶颈在于**判定条件**：如果直接枚举「规则」会无从下手，必须把三类规则翻译成关于 $b,d$ 的整除条件。

### 3.2 核心观察：三类规则的条件与组合

![180B：按 2 → 3 → 11 → 6 → 7 的顺序判定](../../../images/cf180b_flow.svg)

1. **2 类**：$d \mid b^L$。把 $d$ 质因数分解 $d=\prod p^{e_p}$，$b=\prod p^{f_p}$（$f_p$ 可为 0）。存在 $L$ 当且仅当所有 $f_p \ge 1$；此时最小的

$$L = \max_{p \mid d} \left\lceil \frac{e_p}{f_p} \right\rceil .$$

2. **3 类**：$(b-1) \bmod d = 0$。
3. **11 类**：$(b+1) \bmod d = 0$。
4. **6 类**：枚举 $d_2 \mid d$（要求是 2 类），再枚举 $d_3 \mid \frac{d}{d_2}$（要求 $d_3 \mid b-1$），令 $d_{11} = \frac{d}{d_2 d_3}$，要求 $d_{11} \mid b+1$，且三者两两互质。$d\le100$ 时因子个数不超过 12，三重枚举最多几百次。
5. 都不满足就是 **7 类**。

![6 类规则：把 66 拆成 2 × 3 × 11](../../../images/cf180b_6type.svg)

以 $b=10,d=66$ 为例：$66=2\times3\times11$，$2\mid 10$（2 类，看末位奇偶）、$3\mid 10-1$（3 类，数字和）、$11\mid 10+1$（11 类，交错和），三个因子两两互质，所以是 `6-type`。

**为什么必须两两互质**：如果不互质（例如 $8=4\times2$，$4\mid b-1$、$2\mid b+1$ 在 $b=5$ 时成立），「$4\mid N$ 且 $2\mid N$」只等价于 $4\mid N$，并不能推出 $8\mid N$。所以非互质的分解不是合法规则，判定时必须排除。

### 3.3 算法流程

1. 读入 $b,d$。
2. 若存在 $L$ 使 $d\mid b^L$：计算最小 $L$，输出 `2-type` 与 $L$，结束。
3. 若 $(b-1)\bmod d = 0$：输出 `3-type`，结束。
4. 若 $(b+1)\bmod d = 0$：输出 `11-type`，结束。
5. 枚举 $d$ 的所有因子作为 $d_2$，检验 2 类条件；再枚举 $d_3$，检验 3 类条件；剩下的 $d_{11}$ 检验 11 类条件与两两互质。任一组合成功则输出 `6-type`。
6. 否则输出 `7-type`。

注意第 2 步的「2 类」用质因数分解判定与求 $L$，比枚举 $L$ 到 $b^{100}$ 更直接。

### 3.4 样例走查

![180B 两个样例](../../../images/cf180b_sample.svg)

| 输入 | 判定过程 | 输出 |
|------|----------|------|
| `10 10` | $10 \mid 10^1$，$L=1$ | `2-type` / `1` |
| `2 3` | $3\nmid 2^L$；$2\not\equiv1$；$2\equiv-1\pmod3$ | `11-type` |
| `10 66` | 都不是单类；$66=2\cdot3\cdot11$，互质 | `6-type` |
| `10 7` | 单类都不成立；7 为质数无法分解 | `7-type` |

## 4. 正确性证明

**引理 1**：$d\mid b^L$ 当且仅当 $d$ 的每个质因子都整除 $b$；此时最小的 $L=\max_p \lceil e_p/f_p\rceil$。

**证明**：$b^L=\prod p^{f_p L}$，$d\mid b^L \iff \forall p: e_p \le f_p L$。若某 $f_p=0$ 而 $e_p>0$，不可能；否则取 $L\ge e_p/f_p$ 对所有 $p$ 成立，最小整数即 $\max\lceil e_p/f_p\rceil$。∎

**引理 2**：若 $d\mid b^L$，则对所有 $N$ 有 $N\equiv N\bmod b^L\pmod d$；若 $d\nmid b^L$，则存在两个末 $L$ 位相同的数整除性不同。

**证明**：$N = H b^L + R$，$d\mid b^L$ 时 $N\equiv R$。反之，取 $N=0$ 与 $N=b^L$：末 $L$ 位都是 0，但 $d\mid 0$ 而 $d\nmid b^L$，故只看末 $L$ 位不能判定。∎

**引理 3**：3 类规则成立 $\iff d\mid b-1$；11 类规则成立 $\iff d\mid b+1$。

**证明**（充分性）：$N=\sum a_i b^i$。若 $b\equiv1\pmod d$，则 $b^i\equiv1$，故 $N\equiv\sum a_i\pmod d$；若 $b\equiv-1\pmod d$，则 $b^i\equiv(-1)^i$，故 $N\equiv\sum a_i(-1)^i\pmod d$。两种情况下「$d\mid N$」都等价于「规则式的值被 $d$ 整除」。

**证明**（必要性）：若 3 类规则对所有数成立，则所有「数字和相同」的数必须得到相同判定。取数字和都为 $x+y$ 的两个两位数 $xb+y$ 与 $x+y$（后者是它的十进制写法对应的「值」，允许前导零），规则要求 $d\mid(xb+y)\iff d\mid(x+y)$，即 $d\mid x(b-1)$ 对任意数字 $x,y$ 成立；取 $x=1,y=0$ 得：若 $d\mid b$ 则必须 $d\mid 1$，矛盾，故 $d\nmid b$——但这还不够，需要更细的组合。标准做法是取 $y$ 使 $x+y$ 恰为 $d$ 的倍数（$d\le 2(b-1)$ 时总能取到合适的两位数字，$d$ 更大时可用更多位数字凑出），于是 $d\mid x(b-1)$ 对某个与 $d$ 互质的 $x$ 成立，从而 $d\mid b-1$。11 类同理（把 $x+y$ 换成 $y-x$，得到 $d\mid x(b+1)$）。∎

**引理 4**：若 $d=d_2d_3d_{11}$ 两两互质，且三者分别满足 2/3/11 类的条件，则「三条规则同时成立」等价于 $d\mid N$。

**证明**：由中国剩余定理，$d\mid N \iff d_2\mid N$ 且 $d_3\mid N$ 且 $d_{11}\mid N$（因为三者两两互质，乘积为 $d$）。而每个因子对应的规则在各自条件下与「该因子整除 $N$」等价（引理 2、3）。∎

**定理**：算法输出的类型与位数正确。

**证明**：算法按题面要求的顺序依次检查：2 类（引理 1 给出充要条件与最小 $L$）、3 类、11 类（引理 3）、6 类（穷举所有因子分解，引理 4 保证分解成功即规则成立，且穷举保证不漏），最后才是 7 类。因此输出的是顺序最靠前的成立类型；2 类的位数由引理 1 的最小性保证。∎

## 5. 复杂度分析

- **时间**：$O(\sqrt d + \tau(d)^2)$。质因数分解 $O(\sqrt d)$；6 类枚举因子对 $O(\tau(d)^2)$，$d\le100$ 时 $\tau(d)\le12$，至多几百次判断。
- **空间**：$O(\tau(d))$ 存因子表。
- **数值范围**：$b^L$ 不需要真的算出来（会溢出），用质因数指数比较即可；所有中间量不超过 $10^4$。
- **与时限的关系**：1 s 对几百次运算余量在百万倍以上。实测端到端约 2 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

// 180B：判断 d 在 b 进制下属于哪类整除规则
static int b, d;

// x 是否满足 2 类（x | b^L），是则返回最小 L
static bool twoType(int x, int& L) {
    int t = x;
    L = 0;
    for (int p = 2; p * p <= t; ++p) {
        if (t % p) continue;
        int e = 0;
        while (t % p == 0) { t /= p; ++e; }
        int eb = 0, bb = b;
        while (bb % p == 0) { bb /= p; ++eb; }
        if (eb == 0) return false;
        L = max(L, (e + eb - 1) / eb);
    }
    if (t > 1) {
        int p = t, eb = 0, bb = b;
        while (bb % p == 0) { bb /= p; ++eb; }
        if (eb == 0) return false;
        L = max(L, (1 + eb - 1) / eb);
    }
    return true;
}

int main() {
    if (scanf("%d %d", &b, &d) != 2) return 0;
    int L;
    if (twoType(d, L)) { printf("2-type\n%d\n", L); return 0; }
    if ((b - 1) % d == 0) { printf("3-type\n"); return 0; }
    if ((b + 1) % d == 0) { printf("11-type\n"); return 0; }

    // 6 类：d = a * c * e，a 是 2 类，c | b-1，e | b+1，三者两两互质
    vector<int> divs;
    for (int x = 1; x <= d; ++x)
        if (d % x == 0) divs.push_back(x);
    for (int a : divs) {
        int La;
        if (!twoType(a, La)) continue;
        int rem = d / a;
        for (int c : divs) {
            if (rem % c) continue;
            if ((b - 1) % c) continue;
            int e = rem / c;
            if ((b + 1) % e) continue;
            if (std::gcd(a, c) != 1 || std::gcd(a, e) != 1 || std::gcd(c, e) != 1) continue;
            printf("6-type\n");
            return 0;
        }
    }
    printf("7-type\n");
    return 0;
}
```

### Python3

```python
import sys
from math import gcd


def minimal_last_digits(b: int, d: int):
    """d | b^L 的最小 L；不存在返回 None"""
    x = 1
    for L in range(1, 20):
        x = (x * b) % d
        if x == 0:
            return L
    return None


def type_of(b: int, d: int):
    L = minimal_last_digits(b, d)
    if L is not None:
        return ('2-type', L)
    if (b - 1) % d == 0:
        return ('3-type', None)
    if (b + 1) % d == 0:
        return ('11-type', None)

    # 6 类：按质因子的完整幂分组（互质分解等价于把每个 p^e 整块分给某个因子）
    prime_powers = []
    t = d
    p = 2
    while p * p <= t:
        if t % p == 0:
            q = 1
            while t % p == 0:
                t //= p
                q *= p
            prime_powers.append(q)
        p += 1
    if t > 1:
        prime_powers.append(t)

    def single_type_ok(x: int) -> bool:
        if minimal_last_digits(b, x) is not None:
            return True
        return (b - 1) % x == 0 or (b + 1) % x == 0

    def search(i: int, groups) -> bool:
        if i == len(prime_powers):
            return all(single_type_ok(g) for g in groups) and len(groups) >= 2
        for k in range(len(groups)):
            old = groups[k]
            groups[k] = old * prime_powers[i]
            if search(i + 1, groups):
                groups[k] = old
                return True
            groups[k] = old
        groups.append(prime_powers[i])
        ok = search(i + 1, groups)
        groups.pop()
        return ok

    if search(0, []):
        return ('6-type', None)
    return ('7-type', None)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    b = int(data[0])
    d = int(data[1])
    kind, L = type_of(b, d)
    if L is None:
        sys.stdout.write(kind + "\n")
    else:
        sys.stdout.write(kind + "\n" + str(L) + "\n")


main()
```

C++ 用「枚举 $d$ 的因子」做 6 类分解，Python 用「把每个 $p^e$ 整块分配给某个因子」的递归分组——两套写法在 6 类的判定上完全独立，便于互相验证。

## 7. 边界情况与易错点

1. **2 类的位数**：$d=8,b=10$ 时 $L=3$（$8\mid1000$），不是 2 也不是 $\log_2 8$；$d=16$ 时 $L=4$。按 $\max\lceil e/f\rceil$ 计算，别用循环乘 $b$ 直到超过 $d$（会过早停止）。
2. **`2-type` 优先**：即使同时满足 3 类或 11 类，也要输出 `2-type`（题面顺序）。例如 $b=10,d=10$ 也满足 $10\equiv0$ 但 $10\nmid9$，不冲突；而 $b=3,d=2$ 同时满足 3 类与 11 类，答案取 3 类。
3. **3 类与 11 类同时成立**：只可能 $d\mid2$ 且 $b$ 为奇数（如 $b=3,d=2$），此时按顺序输出 `3-type`（题面 hint 明确说明）。
4. **6 类必须有至少两个因子**：如果 $d$ 本身是某一类，前面就已经返回；分解时允许某些因子为 1（表示不使用该类型），但全部为 1 的情况等价于 $d=1$，不会发生。
5. **两两互质不能省**：$d=8,b=5$ 时 $4\mid b-1$、$2\mid b+1$ 都成立，但 $8$ 不是 6 类；若省掉互质检查会误判成 `6-type`。
6. **因子枚举的边界**：$d_3$ 必须同时整除 $\frac{d}{d_2}$ 与 $b-1$；$d_{11}$ 由除法得到后再检查整除 $b+1$，不要反过来。
7. **`7-type` 不是「不存在规则」而是「不是这三类」**：例如 $d=27,b=10$ 可以按三位分组求和，但不属于三类，仍输出 `7-type`。
8. **$b=d$**：如 $b=100,d=100$，$d\mid b^1$ → `2-type` / 1。$b$ 恰好等于 $d$ 时不要漏。
9. **质数 $d$**：只能 2 类（若 $d\mid b$）、3 类、11 类或 7 类；质数无法做 6 类分解，别对质数误判。
10. **Python 的 `minimal_last_digits` 上界 20**：$d\le100$ 时最小 $L$ 不超过 $\log_2 100<7$，20 足够；循环乘法取模不会溢出。

## 8. 验证记录

- **编译环境与命令**：`Apple clang 21.0.0`（`/usr/bin/g++` 是 clang 软链，无 GNU libstdc++），`clang++ -std=c++17 -O2 -Wall` 加仓库自带 `bits/stdc++.h`；正文代码仍写标准头。Python 为 `3.9.6`。验证命令：
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/180/B_整除规则分类.md`
- **官方样例**：2 / 2 通过（`10 10` → `2-type` / `1`；`2 3` → `11-type`），C++ 与 Python 一致。
- **全组合交叉验证**：对 $2 \le b,d \le 100$ 的全部 **9801 组**输入，C++ 与 Python 两套独立实现（因子枚举 vs 质因子幂分组）输出完全一致，0 处不符。
- **语义验证**：另写独立校验器，对每个 $(b,d)$ 用随机 $b$ 进制数（长度 1–8，每对 40 个）检验「分类所声称的规则」是否与「能被 $d$ 整除」等价：2 类看末 $L$ 位、3 类看数字和、11 类看交错和、6 类按分解逐因子验证；并额外验证 2 类的 $L$ 最小（$d\nmid b^{L-1}$）。共 **392040 次**检查，0 次不一致。
- **额外测试**：自造 `10 8`、`10 18`、`10 12`、`10 66`、`10 7`、`3 8`、`5 8`、`10 25`、`100 100` 等 9 组，输出与手算一致。
- **最大约束性能**：输入只有两个数，端到端约 2 ms（几乎全是进程启动），相对 1 s 时限余量在数百倍以上。
- **图片与公式**：3 张 SVG（`cf180b_flow.svg`、`cf180b_6type.svg`、`cf180b_sample.svg`）通过 `ElementTree.parse` 与文本包围盒/重叠检查，headless Chrome 渲染确认无裁切；KaTeX 校验 0 错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 180A Defragmentation](https://codeforces.com/problemset/problem/180/A)：同场 A 题，构造 + 特殊评测。
- [Codeforces 180C Letter](https://codeforces.com/problemset/problem/180/C)：同场 C 题，字符串 + 前后缀。
- [Codeforces 122A Lucky Division](https://codeforces.com/problemset/problem/122/A)：同样是「整除性质」的入门分类题。
- [Codeforces 230B T-primes](https://codeforces.com/problemset/problem/230/B)：约数与质因数分解的判定题。
- [LeetCode 263. 丑数](https://leetcode.cn/problems/ugly-number/)：只含指定质因子的数，和「$d\mid b^L$」的判定同源。

**延伸思考**：

1. **为什么 $d\mid b^L$ 是 2 类的充要条件**：因为「末 $L$ 位决定整除性」等价于 $b^L\equiv0\pmod d$；任何更弱的条件都不足以让所有数都成立（用 $0$ 与 $b^L$ 做反例）。
2. **如果允许「分组求和」**：如 $d=27,b=10$ 可以用三位一组求和（$1000\equiv1\pmod{27}$），这其实是 3 类规则作用在「$b^3$ 进制」上，但题面只认三类基本规则，所以算 7 类。
3. **6 类的因子必须互质**：否则组合规则不等价；这一点是本题最容易想漏的地方，也是 2300 分的主要来源。
4. **一般进制下的「7 类」**：$d$ 与 $b$ 的乘法阶、以及 $d$ 的因子结构共同决定分类；可以把 $d$ 的每个质因子幂看成一个「积木」，问题变成「能不能把积木分成至多三组，每组分别满足 2/3/11 类条件」，这正是 Python 版递归分组的视角。
5. **分类的对称性**：3 类看 $b-1$、11 类看 $b+1$，两者在 $b\leftrightarrow -b$ 下互换；2 类看「$b$ 是否包含 $d$ 的全部质因子」，与前两者正交。这种「三个正交方向」的结构在进制相关的数论题里很常见。

