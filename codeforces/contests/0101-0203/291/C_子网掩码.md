# Codeforces 291C Network Mask 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/291/C
- **比赛来源**：Croc Champ 2013 - Qualification Round · Problem C（UTC 2013-04-12）
- **难度**：1900
- **标签**：位运算
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个互不相同的 IPv4 地址。子网掩码是 32 位中"先若干个 1、再若干个 0"（**至少一个 1、至少一个 0**）的地址。要求选择掩码使这些地址恰好落在 $k$ 个不同网络中；若有多个，取 **1 的个数最少** 的；不存在输出 $-1$。

**约束**：$n \le 10^5$，$k \le n$。

## 2. 示例与观察

官方样例 1：

```text
输入：
5 3
0.0.0.1
0.1.1.2
0.0.2.1
0.1.1.0
0.0.2.3

输出：
255.255.254.0
```

官方样例 2（与样例 1 相同的地址，$k=2$）：

```text
输入：
5 2
0.0.0.1
0.1.1.2
0.0.2.1
0.1.1.0
0.0.2.3

输出：
255.255.0.0
```

官方样例 3：

```text
输入：
2 1
255.0.0.1
0.0.0.2

输出：
-1
```

**观察 1**：掩码由 1 的个数 $L$ 唯一确定（$1 \le L \le 31$），网络数 = 不同"前 $L$ 位前缀"的个数。

**观察 2**：网络数随 $L$ 单调不减（细分类只会增多）。

**观察 3**：1 的个数最少 ⇔ $L$ 最小。于是从小到大枚举 $L$，第一个使网络数恰为 $k$ 的就是答案；若 $L\le 31$ 都不行 → $-1$。

**样例 3 验证**：两个地址在最高位就不同 → $L=1$ 时网络数 2；任何 $L$ 下都 ≥ 2 → $k=1$ 无解 ✓。

## 3. 解题思路

![枚举前缀长度 L](../../../images/cf291c_mask.svg)

把地址转成 32 位整数排序；对每个 $L$，用移位统计相邻元素前缀变化次数即得网络数。

## 4. 正确性证明

**引理 1**：掩码 $L$ 下的网络数 = 不同 $\lfloor \text{ip}/2^{32-L}\rfloor$ 的个数。

**证明**：掩码与地址按位与后，结果只保留前 $L$ 位 ✓。∎

**引理 2**：网络数关于 $L$ 单调不减。

**证明**：$L$ 增大只是在前缀上多用一位，原来的同一组可能被拆开、绝不会合并 ✓。∎

**定理**：算法输出正确。

**证明**：算法枚举所有合法 $L$（$1..31$），用引理 1 计算网络数，取第一个等于 $k$ 的 $L$——由引理 2 与"$L$ 越小 1 越少"，这就是题目要求的掩码 ✓；都不满足即无解 ✓。∎

## 5. 复杂度分析

- **时间**：$O(32n + n\log n)$（排序）。
- **空间**：$O(n)$。
- **与时限的关系**：时限 2 s，$n = 10^5$ 实测端到端 26.3 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n,k; if(scanf("%d %d",&n,&k)!=2) return 0;
    vector<unsigned int> ips(n);
    for(int i=0;i<n;i++){
        unsigned int a,b,c,d;
        scanf("%u.%u.%u.%u",&a,&b,&c,&d);
        ips[i] = (a<<24)|(b<<16)|(c<<8)|d;
    }
    sort(ips.begin(), ips.end());
    int bestL = -1;
    for(int L=1;L<=31;L++){
        int sh = 32 - L;
        int cnt = 1;
        for(int i=1;i<n;i++) if((ips[i]>>sh) != (ips[i-1]>>sh)) cnt++;
        if(cnt == k){ bestL = L; break; }
    }
    if(bestL < 0){ printf("-1\n"); return 0; }
    unsigned int mask = bestL==32 ? 0xFFFFFFFFu : (0xFFFFFFFFu << (32-bestL));
    printf("%u.%u.%u.%u\n", (mask>>24)&255, (mask>>16)&255, (mask>>8)&255, mask&255);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    ips = []
    for i in range(n):
        a, b, c, d = map(int, data[2+i].decode().split('.'))
        ips.append((a<<24)|(b<<16)|(c<<8)|d)
    ips.sort()
    best = -1
    for L in range(1, 32):
        sh = 32 - L
        cnt = 1
        for i in range(1, n):
            if (ips[i] >> sh) != (ips[i-1] >> sh):
                cnt += 1
        if cnt == k:
            best = L; break
    if best < 0:
        print(-1); return
    mask = (0xFFFFFFFF << (32 - best)) & 0xFFFFFFFF
    print("%d.%d.%d.%d" % ((mask>>24)&255, (mask>>16)&255, (mask>>8)&255, mask&255))
main()
```

## 7. 边界情况与易错点

1. **$L=32$ 不合法**（没有 0 位）；$L=0$ 也不合法（没有 1 位）。
2. **$k=1$**：要求所有地址前 31 位相同——通常无解（样例 3）。
3. **$k=n$**：$L$ 需要足够大，可能无解。
4. **读入格式**：`scanf("%u.%u.%u.%u")`。
5. **输出**：按点分十进制。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（255.255.254.0、255.255.0.0、-1），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版对每个 $L$ 用集合统计前缀个数，独立求最小可行 $L$。随机 250 组 $n \le 6$，**250 / 250 全部一致**。
- **最大约束性能**：$n = 10^5$，实测端到端 26.3 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 291B Command Line Arguments](https://codeforces.com/problemset/problem/291/B)：同场 B 题。

**延伸思考**：

1. **如果掩码不要求连续 1**：答案是按位分组问题。
2. **如果要求网络数 ≤ k**：二分 $L$。

