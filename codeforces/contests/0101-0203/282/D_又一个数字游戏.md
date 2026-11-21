# Codeforces 282D Yet Another Number Game 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/282/D
- **比赛来源**：Codeforces Round 173 (Div. 2) · Problem D（UTC 2013-03-13）
- **难度**：2100
- **标签**：博弈论、动态规划
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 堆非负整数 $a_1..a_n$（$n\le3$，$a_i<300$）。两人轮流操作，每步必须做且只能做以下之一：

1. 选一堆 $a_i$，选 $x\in[1,a_i]$，令 $a_i\leftarrow a_i-x$；
2. 选 $x\in[1,\min_i a_i]$，令所有 $a_i\leftarrow a_i-x$。

不能操作者负。BitLGM 先手，问谁赢。

**约束**：$n\le3$、$a_i<300$ ⇒ 状态数 $\le 300^3 = 2.7\times10^7$，可以整体 DP；关键是转移要 $O(1)$ 而不是枚举 $x$。

## 2. 示例与观察

官方样例 1：

```text
输入：
2
1 1

输出：
BitLGM
```

先手直接"全体减 1"到 $(0,0)$，对手无路可走 ✓。

官方样例 2：

```text
输入：
2
1 2

输出：
BitAryo
```

任何一步都会把局面送到必胜态（这正是 Wythoff 游戏的第一个必败态）。

官方样例 3：

```text
输入：
3
1 2 1

输出：
BitLGM
```

![两种走法](../../../images/cf282d_moves.svg)

**观察 1**：两种走法都让总和严格下降 ⇒ 状态图是 DAG，可按 $a_1+a_2+a_3$ 递增递推。

**观察 2**：$n=1$ 就是普通 Nim（一堆），$n=2$ 是 **Wythoff 游戏**（斜着走 + 单堆走）。$n=3$ 没有简单闭式，但状态数小，可以全 DP。

**观察 3**：状态 $(a,b,c)$ 的走法有两种"扁平"结构：
- 单堆走法只改变一个坐标 ⇒ 对固定的另外两个坐标，只需知道"存在哪个更小的必败值"；
- 全体走法保持所有**差值**不变 ⇒ 按差值分组维护。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

对每个状态枚举所有走法（$\sum a_i$ 种），总复杂度 $O(300^3\cdot 900) \approx 2.4\times10^{10}$，太慢。

### 3.2 O(1) 转移：四个"最小必败值"结构

![四个 O(1) 查询](../../../images/cf282d_struct.svg)

按总和递增处理状态 $(a,b,c)$，维护：

- `minA[b][c]` = 固定 $(b,c)$ 时，已发现的必败态中**最小的 $a$**；
- `minB[a][c]`、`minC[a][b]` 同理；
- `diag[a-b][b-c]` = 同一"差值类"上已发现的必败态中**最小的 $\min(a,b,c)$**。

判定：$(a,b,c)$ 必胜 ⟺ `minA[b][c] < a` 或 `minB[a][c] < b` 或 `minC[a][b] < c` 或 `diag[a-b][b-c] < min(a,b,c)`。若是必败态，就把 $a$（或 $b$、$c$、$\min(a,b,c)$）更新进对应结构。

$n=1$：直接判 $a_1>0$；$n=2$ 用降一维的结构（`minA[b]`、`minB[a]`、`diag[a-b]`）。

### 3.3 样例走查

$n=2$：$(0,0)$ 必败 → $(1,0),(0,1),(1,1)$ 都必胜（能到 $(0,0)$）→ $(1,2)$：单堆走到 $(0,2)/（1,1)/(1,0)$ 全必胜，斜走到 $(0,1)$ 也必胜 ⇒ 必败 ✓（BitAryo）。$(1,1)$ 斜走到 $(0,0)$ ⇒ 必胜 ✓。

$n=3$ 的 $(1,2,1)$ 由 DP 判定为必胜（样例 ✓）。

## 4. 正确性证明

**引理 1**：状态图无环，且按 $a_1+\dots+a_n$ 递增处理时，所有可达状态都已处理。

**证明**：两种走法都使总和至少减 1（走法 1 减 $x\ge1$；走法 2 减 $nx\ge n\ge1$）⇒ 严格递减 ⇒ 无环；按总和递增即拓扑序。∎

**引理 2**：对固定 $(b,c)$，"存在 $a'<a$ 使 $(a',b,c)$ 必败" ⟺ `minA[b][c] < a`。

**证明**：`minA[b][c]` 记录的是该列所有必败态的最小 $a$，若它 $<a$ 则取那个必败态即可；反之若存在这样的必败态，其 $a'\ge$ `minA[b][c]`，故 `minA[b][c] ≤ a' < a` ✓。∎

**引理 3**：走法 2 的终点集合 = 同一差值类 $(a-b,b-c)$ 上所有 $t<\min(a,b,c)$ 的状态，其中 $t=\min(a,b,c)-x$。

**证明**：全体减 $x$ 时 $a-b$、$b-c$ 不变，$\min$ 恰好减 $x$；反之同一差值类内 $\min$ 更小的状态都可经走法 2 到达 ✓。∎

**定理**：算法输出正确的胜负。

**证明**：博弈论基本定理——局面必败 ⟺ 无一步可到必败态。由引理 1 的拓扑序、引理 2 与引理 3，四个判定条件精确覆盖了所有走法；故每次判定正确，最终输出正确 ✓。∎

## 5. 复杂度分析

- 时间：$n=3$ 时 $O(300^3)=2.7\times10^7$（每个状态 4 次 $O(1)$ 判断），实测 **0.10 s**（2 s 时限）。
- 空间：`minA/minB/minC` 各 $301^2$、`diag` 为 $601^2$，加上 `lose` 三维表约 $301^3$ 字节 ≈ 27 MB（256 MB 限制内）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){int n;scanf("%d",&n);int v[3]={0,0,0};for(int i=0;i<n;i++)scanf("%d",&v[i]);
 if(n==1){puts(v[0]>0?"BitLGM":"BitAryo");return 0;}
 if(n==2){
   int A=v[0],B=v[1];
   static int minA[302], minB[302], diag[605];
   for(int i=0;i<302;i++){minA[i]=1000;minB[i]=1000;}
   for(int i=0;i<605;i++)diag[i]=1000;
   static char lose[302][302];
   for(int s=0;s<=A+B;s++)for(int a=0;a<=min(s,A);a++){
     int b=s-a; if(b>B)continue;
     bool win=(minA[b]<a)||(minB[a]<b)||(diag[a-b+300]<min(a,b));
     lose[a][b]=!win;
     if(lose[a][b]){minA[b]=min(minA[b],a);minB[a]=min(minB[a],b);
       diag[a-b+300]=min(diag[a-b+300],min(a,b));}
   }
   puts(lose[A][B]?"BitAryo":"BitLGM");return 0;
 }
 int A=v[0],B=v[1],C=v[2];
 static int minA[301][301],minB[301][301],minC[301][301],diag[605][605];
 for(int i=0;i<=300;i++)for(int j=0;j<=300;j++){minA[i][j]=minB[i][j]=minC[i][j]=1000;}
 for(int i=0;i<605;i++)for(int j=0;j<605;j++)diag[i][j]=1000;
 static char lose[301][301][301];
 for(int s=0;s<=A+B+C;s++)for(int a=0;a<=min(s,A);a++)
   for(int b=0;b<=min(s-a,B);b++){
     int c=s-a-b; if(c>C)continue;
     bool win=(minA[b][c]<a)||(minB[a][c]<b)||(minC[a][b]<c)
              ||(diag[a-b+300][b-c+300]<min(a,min(b,c)));
     lose[a][b][c]=!win;
     if(lose[a][b][c]){
       minA[b][c]=min(minA[b][c],a); minB[a][c]=min(minB[a][c],b);
       minC[a][b]=min(minC[a][b],c);
       int k=min(a,min(b,c)), &d=diag[a-b+300][b-c+300]; d=min(d,k);
     }
   }
 puts(lose[A][B][C]?"BitAryo":"BitLGM");
}
```

### Python3

```python
import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    v = (data[1:n+1] + [0, 0, 0])[:3]
    if n == 1:
        print("BitLGM" if v[0] > 0 else "BitAryo")
        return
    BIG = 1000
    if n == 2:
        A, B = v[0], v[1]
        minA = [BIG] * (B + 1)
        minB = [BIG] * (A + 1)
        diag = {}
        lose = [[False] * (B + 1) for _ in range(A + 1)]
        for s in range(A + B + 1):
            for a in range(max(0, s - B), min(s, A) + 1):
                b = s - a
                win = (minA[b] < a) or (minB[a] < b) or (diag.get(a - b, BIG) < min(a, b))
                lose[a][b] = not win
                if lose[a][b]:
                    minA[b] = min(minA[b], a)
                    minB[a] = min(minB[a], b)
                    k = min(a, b)
                    if diag.get(a - b, BIG) > k:
                        diag[a - b] = k
        print("BitAryo" if lose[A][B] else "BitLGM")
        return
    A, B, C = v
    minA = [[BIG] * (C + 1) for _ in range(B + 1)]
    minB = [[BIG] * (C + 1) for _ in range(A + 1)]
    minC = [[BIG] * (B + 1) for _ in range(A + 1)]
    diag = {}
    lose = {}
    for s in range(A + B + C + 1):
        for a in range(max(0, s - B - C), min(s, A) + 1):
            for b in range(max(0, s - a - C), min(s - a, B) + 1):
                c = s - a - b
                if c > C:
                    continue
                win = (minA[b][c] < a) or (minB[a][c] < b) or (minC[a][b] < c) \
                      or (diag.get((a - b, b - c), BIG) < min(a, b, c))
                lose[(a, b, c)] = not win
                if lose[(a, b, c)]:
                    if a < minA[b][c]: minA[b][c] = a
                    if b < minB[a][c]: minB[a][c] = b
                    if c < minC[a][b]: minC[a][b] = c
                    key = (a - b, b - c); k = min(a, b, c)
                    if diag.get(key, BIG) > k: diag[key] = k
    print("BitAryo" if lose[(A, B, C)] else "BitLGM")

main()
```

Python 版思路完全一致；$n=3$ 满数据（$299,298,297$）CPython 约 20～30 s，**建议提交 C++**（或 PyPy3）。

## 7. 边界情况与易错点

1. **走法 2 的 $x$ 上界是 $\min a_i$**：不能让任何堆变负。
2. **$n=1$**：两种走法等价于普通 Nim，答案就是 $a_1>0$（先手胜）。
3. **$n=2$ 时不要漏掉"斜走"**：它就是 Wythoff 游戏；只考虑单堆会错（$(1,2)$ 会误判成必胜）。
4. **按总和递增**：坐标不是独立递增的（比如 $(0,5,0)\to(0,4,0)$），必须按 $a+b+c$ 排序。
5. **`diag` 的下标偏移**：$a-b\in[-299,299]$，记得 $+300$。
6. **`lose` 表大小**：$301^3$ 字节 ≈ 27 MB，用 `char` 而不要 `int`（否则 108 MB，逼近 256 MB）。
7. **初始化"最小值"用 INF**：用 1000 而不是 300（因为要判 `<`，取 1000 表示"不存在"）。

## 8. 验证记录

- 编译环境与命令：`clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/282/D_又一个数字游戏.md`
- 官方样例：3 / 3 通过（`BitLGM`、`BitAryo`、`BitLGM`）。
- 额外测试：随机 120 组（$n\le3$，$a_i\le7$）与"递归枚举所有走法求 SG"的暴力对拍，全部一致。
- 最大约束性能：$n=3$、$(299,298,297)$ 实测 **0.10 s**（2 s 时限的 5%）。
- 复核状态：样例、120 组暴力对拍、性能均实测通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 282E Sausage Maximization](https://codeforces.com/problemset/problem/282/E)：同场 E 题。
- [Codeforces 138D World of Darkraft](https://codeforces.com/problemset/problem/138/D)：另一种"整体 DP + 结构优化"的博弈。
- [Codeforces 603C Lieges of Legendre](https://codeforces.com/problemset/problem/603/C)：SG 函数入门。

**延伸思考**：

1. $n=2$ 就是 Wythoff 游戏，其必败态有闭式 $(\lfloor k\varphi\rfloor,\lfloor k\varphi^2\rfloor)$；本解法只是 DP，能推出 $n=3$ 的闭式吗？
2. 如果把"全体减 $x$"改成"全体减**不同**的 $x_i$"，问题会变成什么？
3. 为什么"全体减"要保持差值不变这一观察能把转移从 $O(300)$ 降到 $O(1)$？换成"全体减 $2x$"还成立吗（差值会变成 $a-b$ 不变但奇偶有关）？
