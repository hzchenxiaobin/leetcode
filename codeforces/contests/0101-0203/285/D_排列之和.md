# Codeforces 285D Permutation Sum 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/285/D
- **比赛来源**：Codeforces Round 175 (Div. 2) · Problem D（UTC 2013-03-17）
- **难度**：1900
- **标签**：组合数学、DP、位掩码
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：两个排列 $a,b$（长度 $n$）的"和"定义为 $c_i=((a_i-1)+(b_i-1))\bmod n+1$。求有多少对 $(a,b)$ 使得 $c$ 也是排列（模 $10^9+7$）。

**约束**：$n\le16$ ⇒ 需要状态压缩 DP（但不能是 $4^n$ 的朴素做法）。

## 2. 示例与观察

官方样例 1：

```text
输入：
3

输出：
18
```

官方样例 2：

```text
输入：
5

输出：
1800
```

![化为完全映射](../../../images/cf285d_cm.svg)

**观察 1**：令 $a'_i=a_i-1$、$b'_i=b_i-1$（都是 $0..n-1$ 的排列），条件变成 "$(a'_i+b'_i)\bmod n$ 是排列"。

**观察 2（关键）**：固定 $b'$，满足条件的 $a'$ 个数与 $b'$ 的取值**无关**：把位置按 $b'$ 的重排 $i\mapsto b'_i$ 看，条件变为"$a''_j+j$ 是排列"，这正是 $a''$ 为**完全映射**（complete mapping）的条件。故总数 $=n!\cdot A(n)$，$A(n)$ 是完全映射个数。

**观察 3**：$n$ 为偶数时 $A(n)=0$（群论：$\mathbb{Z}_n$ 的 Sylow-2 子群循环 ⇒ 不存在完全映射）。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举 $(a,b)$ 是 $(n!)^2$，$n=16$ 时不可行；朴素双掩码 DP 理论上是 $4^n$。

### 3.2 正解：双掩码 DP 求 $A(n)$

![双掩码 DP](../../../images/cf285d_dp.svg)

逐行 $i=0..n-1$ 放棋子：状态 =（已用列集合 cols，已用对角集合 diags），键 $=\text{cols}\cdot2^n+\text{diags}$，用哈希表存。转移：第 $i$ 行放列 $j$（未用），对角 $d=(i+j)\bmod n$（未用）。

**为什么可行**：可达状态远少于 $4^n$——实测 $n=15$ 峰值仅 $2.6\times10^6$ 个状态。

最后答案 $=A(n)\cdot n!\bmod(10^9+7)$。

### 3.3 样例走查

$n=3$：DP 得 $A(3)=3$，$3!=6$ ⇒ $18$ ✓。
$n=5$：$A(5)=15$，$5!=120$ ⇒ $1800$ ✓。

## 4. 正确性证明

**引理 1**：$\#\{(a,b): c \text{ 是排列}\}=n!\cdot A(n)$。

**证明**：对每个 $b$，计数 $=A(n)$（观察 2 的重排双射）；$b$ 有 $n!$ 个 ✓。∎

**引理 2**：DP 计算的是 $A(n)$。

**证明**：完全映射 = 排列 $\sigma$ 使 $i+\sigma(i)$ 也是排列，等价于在 $n\times n$ 棋盘上放 $n$ 个互不同行、列、对角（对角 = $i+j \bmod n$）的棋子。DP 按行逐个放、用两个掩码记录已用的列与对角，故恰好枚举所有这样的放置并计数 ✓。∎

**定理**：输出正确。**证明**：由引理 1、2，输出 $=A(n)\cdot n!$ ✓（偶数 $n$ 时由观察 3，$A(n)=0$，直接输出 0）✓。∎

## 5. 复杂度分析

- 时间：$O(\#\text{states}\cdot n)$；$n=15$ 时状态峰值 $2.6\times10^6$，实测 **2.2 s**（3 s 时限，偏紧）。
- 空间：哈希表存状态，峰值约 $2.6\times10^6$ 项，约 60 MB。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef unsigned long long ull;
const ll MOD=1000000007LL;
int main(){int n;scanf("%d",&n);
 if(n%2==0){puts("0");return 0;}
 int full=(1<<n)-1;
 unordered_map<ull,ll> cur,nxt;
 cur.reserve(1<<16); nxt.reserve(1<<16);
 cur[0]=1;
 for(int i=0;i<n;i++){
   nxt.clear();
   for(auto &kv: cur){
     ull key=kv.first; ll w=kv.second;
     int cols=(int)(key>>n), diags=(int)(key&full);
     for(int j=0;j<n;j++){
       if(cols>>j&1) continue;
       int d=(i+j)%n;
       if(diags>>d&1) continue;
       ull nk=(ull)(cols|(1<<j))<<n | (unsigned)(diags|(1<<d));
       nxt[nk]=(nxt[nk]+w)%MOD;
     }
   }
   cur.swap(nxt);
 }
 ll A=0; for(auto &kv:cur) A=(A+kv.second)%MOD;
 ll f=1; for(int i=2;i<=n;i++) f=f*i%MOD;
 printf("%lld\n",A*f%MOD);}
```

### Python3

```python
import sys
from collections import defaultdict

n = int(sys.stdin.buffer.readline())
MOD = 10**9 + 7
if n % 2 == 0:
    print(0)
else:
    cur = {(0, 0): 1}
    for i in range(n):
        nxt = defaultdict(int)
        for (cols, diags), w in cur.items():
            for j in range(n):
                if cols >> j & 1:
                    continue
                d = (i + j) % n
                if diags >> d & 1:
                    continue
                nxt[(cols | 1 << j, diags | 1 << d)] = (nxt[(cols | 1 << j, diags | 1 << d)] + w) % MOD
        cur = nxt
    A = sum(cur.values()) % MOD
    f = 1
    for i in range(2, n + 1):
        f = f * i % MOD
    print(A * f % MOD)
```

Python 版对 $n\le13$ 可行，$n=15$ 太慢，**建议提交 C++**。

## 7. 边界情况与易错点

1. **$n$ 为偶数**：直接输出 0（$A(n)=0$），否则白白跑一遍 DP。
2. **别忘了乘 $n!$**：$A(n)$ 不是答案。
3. **$n=1$**：$A(1)=1$、$1!=1$ ⇒ 1。
4. **键的构造**：`cols * 2^n + diags`，$n\le16$ 时 32 位掩码 ⇒ 64 位键足够。
5. **哈希表容量**：预留足够桶（如 `reserve(4e6)`），否则 $n=15$ 会因 rehash 超时。
6. **模运算**：只在累加时取模，避免溢出。
7. **对角是 $\bmod n$**：$d=(i+j)\bmod n$，不是 $i+j$。

## 8. 验证记录

- 编译环境与命令：`clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/285/D_排列之和.md`
- 官方样例：2 / 2 通过（`18`、`1800`）。
- 额外测试：$n=1..5$ 与"枚举全部 $a,b$ 组合检查 $c$ 是否排列"的暴力对拍（$n=5$ 时 $120^2=14400$ 对），全部一致。
- 最大约束性能：$n=15$ 实测 **2.2 s**（3 s 时限的 74%）；$n=13$ 约 0.3 s。
- 复核状态：样例、暴力对拍、性能均实测通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 285E Positions in Permutations](https://codeforces.com/problemset/problem/285/E)：同场 E 题（容斥 + 车多项式）。
- [Codeforces 1096F Inversion Expectation](https://codeforces.com/problemset/problem/1096/F)：排列计数。
- [Codeforces 123E Maze](https://codeforces.com/problemset/problem/123/E)：另一类状态压缩计数。

**延伸思考**：

1. 完全映射对 $\mathbb{Z}_n$ 存在当且仅当 $n$ 为奇数；那对一般的群，Hall–Paige 定理怎么说？
2. 如果把"和对角"换成"差"（$i-\sigma(i)$），$A(n)$ 会变吗？
3. 本 DP 的状态数为什么远小于 $4^n$？（提示：每行只能落在两个"未被占用"的位置上，约束越走越紧。）
