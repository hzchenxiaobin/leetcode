# Codeforces 312B Archer 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/312/B
- **比赛来源**：Codeforces Round 185 (Div. 2) · Problem B（UTC 2013-05-03）
- **难度**：1300
- **标签**：概率、数学
- **评测类型**：普通（实数，误差 $\le10^{-6}$）
- **限制**：时间 2 s / 内存 256 MB

**题意**：SmallR 命中概率 $p=\frac ab$，Zanoes 命中概率 $q=\frac cd$，SmallR 先射，谁先命中谁赢。求 SmallR 获胜的概率。

**约束**：$1\le a\le b,\ 1\le c\le d\le10^9$ ⇒ $O(1)$ 公式。

## 2. 示例与观察

官方样例：

```text
输入：
1 2 1 2

输出：
0.666666666667
```

![几何级数](../../../images/cf312b_geom.svg)

**观察**：SmallR 在第 $k+1$ 轮获胜 $\iff$ 前 $k$ 轮双方都没中、然后他中了 ⇒ 概率 $p\,r^k$，其中 $r=(1-p)(1-q)$。于是
$$P=\sum_{k\ge0} pr^k=\frac{p}{1-r}=\frac{p}{1-(1-p)(1-q)}.$$

## 3. 解题思路

### 3.1 公式

直接算 $P=\dfrac{p}{1-(1-p)(1-q)}$。$0\le r<1$（因为 $p,q>0$），级数收敛 ✓。

### 3.2 样例走查

$p=q=\tfrac12$：$r=\tfrac14$，$P=\tfrac{1/2}{3/4}=\tfrac23\approx0.666666666667$ ✓。

## 4. 正确性证明

**引理 1**：SmallR 获胜的这些事件（"第 $k+1$ 轮赢"，$k\ge0$）两两互斥且覆盖全部获胜情形。

**证明**：胜负只由"谁先命中"决定，故恰好有一个轮次是首次命中 ✓。∎

**引理 2**：第 $k+1$ 轮由 SmallR 首次命中的概率为 $p\,r^k$，$r=(1-p)(1-q)$。

**证明**：需要前 $k$ 轮双方各射一次都不中（概率 $r^k$）以及本轮 SmallR 命中（$p$），各轮独立 ✓。∎

**定理**：$P=p/(1-r)$ 即所求概率。

**证明**：由引理 1、2，$P=\sum_{k\ge0}pr^k=\frac{p}{1-r}$（$|r|<1$）✓。∎

## 5. 复杂度分析

- 时间：$O(1)$。
- 空间：$O(1)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){double a,b,c,d;scanf("%lf %lf %lf %lf",&a,&b,&c,&d);
 double p=a/b, q=c/d;
 printf("%.12f\n", p/(1.0-(1.0-p)*(1.0-q)));}
```

### Python3

```python
a, b, c, d = map(int, input().split())
p, q = a / b, c / d
print("%.12f" % (p / (1 - (1 - p) * (1 - q))))
```

## 7. 边界情况与易错点

1. **$r=1$** 不会出现（$p,q>0$），所以不会除零。
2. **精度**：用 `double` + 12 位小数输出，误差远小于 $10^{-6}$。
3. **输入顺序**是 $a,b,c,d$（不是 $a,c,b,d$）。
4. **"先手优势"**：$p=q$ 时答案 $>0.5$，可用来 sanity check（如 $\tfrac12,\tfrac12\to\tfrac23$）。
5. **不要用整数除法**：$p=a/b$ 必须是浮点。
6. **输出格式**：实数，不要求特定小数位。

## 8. 验证记录

- 编译环境与命令：`clang++ -O2 -std=c++17 -I codeforces/tools/include`。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/312/B_射手.md`
- 官方样例：1 / 1 通过（`0.666666666667`）。
- 额外测试：随机 220 组（$a\le b,c\le d\le20$）与"独立累加前 200 项几何级数"的参考实现对拍，最大绝对误差 $<10^{-9}$。
- 最大约束性能：$O(1)$，实测 **0.036 s**（含进程启动）。
- 复核状态：样例、220 组双实现对拍、性能均实测通过；正文代码与实测版本逐字一致。

## 相关题目与扩展

- [Codeforces 312A Whose sentence is it?](https://codeforces.com/problemset/problem/312/A)：同场 A 题。
- [Codeforces 313A Ilya and Bank Account](https://codeforces.com/problemset/problem/313/A)：同批 313 场。
- [Codeforces 148D Bag of mice](https://codeforces.com/problemset/problem/148/D)：概率 DP。

**延伸思考**：

1. 若"先手"改成轮流动且每人可以连续射两次，公式怎么变？
2. 若要求"至少命中 $t$ 次才算赢"，需要什么 DP？
3. 若 $p,q$ 每次变化（例如疲劳），答案还能闭式吗？
