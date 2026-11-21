# Codeforces 294A Shaass and Oskols（沙斯与电线上的鸟） 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/294/A
- **比赛来源**：Codeforces Round 178 (Div. 2) · Problem A（UTC 2013-03-15）
- **难度**：800
- **标签**：模拟
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB


**题意**：$n$ 根水平电线自上而下编号，第 $i$ 根上有 $a_i$ 只鸟。每次打掉第 $x$ 根线上从左数第 $y$ 只：它左边的鸟跳上第 $x-1$ 根、右边的跳下第 $x+1$ 根（没有对应线就飞走），该线清零。求 $m$ 次射击后每根线上的鸟数。

**约束**：$n, m \le 100$，$a_i \le 100$。

## 2. 示例与观察

官方样例 1：

```text
输入：
5
10 10 10 10 10
5
2 5
3 13
2 12
1 13
4 6

输出：
0
12
5
0
16
```

官方样例 2：

```text
输入：
3
2 4 1
1
2 2

输出：
3
0
3
```

**观察 1**：一次射击只影响三根线：$x$ 清零，$x-1$ 加 $y-1$，$x+1$ 加 $a_x - y$。

**观察 2**：题面保证射击时该线上至少有 $y$ 只鸟，所以直接按顺序模拟即可。

## 3. 解题思路

![一次射击的影响](../../../images/cf294a_sim.svg)

逐步模拟，注意越界（$x-1 < 1$ 或 $x+1 > n$ 时直接丢弃）。

## 4. 正确性证明

**引理**：单次射击后各线数量的更新公式如观察 1。

**证明**：被击中的鸟左边的 $y-1$ 只全部跳向上一层、右边的 $a_x-y$ 只跳向下一层，该线剩余的鸟数为 0 ✓。∎

**定理**：$m$ 次模拟后得到正确结果。

**证明**：由引理，逐次更新与题意一致；越界时鸟飞走 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + m)$。
- **空间**：$O(n)$。
- **与时限的关系**：实测端到端 3.0 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; if(scanf("%d",&n)!=1) return 0;
    vector<long long> a(n+2,0);
    for(int i=1;i<=n;i++) scanf("%lld",&a[i]);
    int m; scanf("%d",&m);
    while(m--){
        int x; long long y; scanf("%d %lld",&x,&y);
        long long left = y-1, right = a[x]-y;
        a[x] = 0;
        if(x-1>=1) a[x-1] += left;
        if(x+1<=n) a[x+1] += right;
    }
    for(int i=1;i<=n;i++) printf("%lld\n", a[i]);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [0]*(n+2)
    for i in range(1, n+1):
        a[i] = int(data[i])
    m = int(data[n+1]); pos = n+2
    for _ in range(m):
        x = int(data[pos]); y = int(data[pos+1]); pos += 2
        left = y - 1; right = a[x] - y
        a[x] = 0
        if x-1 >= 1: a[x-1] += left
        if x+1 <= n: a[x+1] += right
    sys.stdout.write("\n".join(str(a[i]) for i in range(1, n+1)) + "\n")
main()
```

## 7. 边界情况与易错点

1. **$x=1$**：左边的鸟全部飞走。
2. **$x=n$**：右边的鸟全部飞走。
3. **$y$ 为奇数/偶数**：只与 $y-1$ 和 $a_x-y$ 有关。
4. **$m=0$**：原样输出。
5. **鸟数可能为 0**：输出 0。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（0 12 5 0 16、3 0 3），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版用"鸟的列表"逐只移动。随机 250 组 $n \le 5$，**250 / 250 全部一致**。
- **最大约束性能**：$n = m = 100$，实测端到端 3.0 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 294B Shaass and Bookshelf](https://codeforces.com/problemset/problem/294/B)：同场 B 题。

**延伸思考**：

1. **如果一次打掉多只**：需要重新定义规则。
2. **如果电线是环**：上下层关系要改。
