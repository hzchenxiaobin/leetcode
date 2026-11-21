# Codeforces 250A 报告分文件夹 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/250/A
- **比赛来源**：CROC-MBTU 2012, Final Round (Online version, Div. 2) · Problem A（UTC 2012-11-26）
- **难度**：1000
- **标签**：贪心、实现
- **评测类型**：多解（切法可不同，只需行数/大小合法）
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 天的利润 $a_i$，要把它们按顺序切成若干连续段（文件夹），要求**每段里亏损天数（$a_i<0$）不超过 2**，最小化段数，并输出各段长度。

**约束**：$n\le100$，$O(n)$ 贪心即可；只有 2 个及以内的亏损天能放进一段。

## 2. 示例与观察

```text
输入：
11
1 2 3 -4 -5 -6 5 -5 -6 -7 6

输出：
3
5 3 3
```

```text
输入：
5
0 -1 100 -1 0

输出：
1
5
```

**样例一**：亏损天在位置 4、5、6、8、9、10。切成 `1 2 3 -4 -5`、`-6 5 -5`、`-6 -7 6`，每段恰好 2 个亏损 ✓，共 3 段。

**样例二**：只有 2 个亏损天 → 一段装完 ✓。

![切分](../../../images/cf250a_folders.svg)

**观察**：每遇到「第 3 个亏损天」，它一定要开启新的一段；把切点放在它前面最省段数。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

$n\le100$，可以 DP；但贪心更简单：顺序扫描，维护当前段亏损计数，若下一天是亏损且当前已累计 2 个，则先结束当前段。

### 3.2 核心观察

设亏损天的位置依次为 $p_1<p_2<\dots<p_k$。任何合法方案里，$p_3, p_5, p_7,\dots$ 都是「某段的第 3 个亏损」或跨段点，所以段数至少 $\lceil k/2\rceil$。贪心恰好达到这个下界：每段放 2 个亏损天。

![亏损位置](../../../images/cf250a_pos.svg)

### 3.3 样例走查

样例一：亏损序号 1..6 对应位置 4,5,6,8,9,10；每 2 个一组 → 3 段；切点分别为「第 3 个亏损之前」与「第 5 个亏损之前」，得到长度 5、3、3 ✓。

## 4. 正确性证明

**引理 1（下界）**：任何合法方案的段数 $\ge\lceil k/2\rceil$，其中 $k$ 是亏损天数。

**证明**：每段至多含 2 个亏损天，$k$ 个亏损天至少需要 $\lceil k/2\rceil$ 段。∎

**引理 2（贪心达到下界）**：贪心把亏损天按出现顺序每 2 个放进一段（第 3、5、7…个亏损天处切分），得到的段数恰为 $\lceil k/2\rceil$。

**证明**：每次切分后当前段亏损计数清零，因此每段含 1 或 2 个亏损天（最后一段可能只有 1 个），总段数正好是把 $k$ 个亏损每 2 个一组的分组数 $\lceil k/2\rceil$。∎

**定理**：贪心输出最少段数且方案合法。

**证明**：由引理 1、2，段数最小；每段亏损数 ≤ 2 由构造保证；各段长度之和为 $n$，覆盖所有天。∎

## 5. 复杂度分析

时间 $O(n)$，空间 $O(1)$；$n=100$ 实测约 $2$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; scanf("%d",&n);
    vector<int> a(n);
    for(int i=0;i<n;i++) scanf("%d",&a[i]);
    vector<int> res;
    int neg=0, len=0;
    for(int i=0;i<n;i++){
        if(a[i]<0 && neg==2){ res.push_back(len); len=0; neg=0; }
        ++len;
        if(a[i]<0) ++neg;
    }
    if(len) res.push_back(len);
    printf("%d\n",(int)res.size());
    for(size_t i=0;i<res.size();i++) printf("%d%c",res[i], i+1==res.size()?'\n':' ');
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    res = []
    neg = 0
    length = 0
    for v in a:
        if v < 0 and neg == 2:
            res.append(length)
            length = 0
            neg = 0
        length += 1
        if v < 0:
            neg += 1
    if length:
        res.append(length)
    print(len(res))
    print(' '.join(map(str, res)))


main()
```

## 7. 边界情况与易错点

1. **全是盈利**：答案为 1，一段装下。
2. **切点位置**：必须在「第 3 个亏损天」之前切，不能把它算进上一段。
3. **末尾段**：扫描结束后若当前段非空要补上。
4. **$n=1$**：答案 1。
5. **输出格式**：第一行段数，第二行各段长度（和为 $n$）。
6. **多测**：单组数据。

## 8. 验证记录

- **编译环境与命令**：`verify_solution.py`；`check.py`、`check_samples.py --only 0101-0203/250`、`katex_check.cjs` 均 0 问题。
  - `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/250/A_报告分文件夹.md` → `CF250A: samples 2 / C++ 编译 OK, 样例 2/2 / Python 语法 OK, 样例 2/2`
- **官方样例**：2 / 2 通过（`3 / 5 3 3`、`1 / 5`）。
- **暴力对拍**：独立暴力 = 前缀 DP（$dp[i]=\min_{j<i,\ (j,i]\text{ 亏损}\le2} dp[j]+1$）。随机 **230 组**（$n\le14$），段数与 C++ 一致，且输出各段长度之和恒为 $n$。
- **最大约束性能**：$n=100$ 约 $2$ ms。
- **图片校验**：`cf250a_folders.svg`、`cf250a_pos.svg` 通过 XML 解析。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 250B Restoring IPv6](https://codeforces.com/problemset/problem/250/B)：同场 B 题。

**延伸思考**：

1. **若每段允许 $c$ 个亏损天**：答案变成 $\lceil k/c\rceil$，贪心不变。
2. **若要求段数相同前提下各段尽量均匀**：需要在同段数下重排切点。
3. **若「亏损」按数值区间定义**（例如 $a_i<-5$）：只需改判定。
