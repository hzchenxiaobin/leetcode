# Codeforces 291D Parallel Programming 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/291/D
- **比赛来源**：Croc Champ 2013 - Qualification Round · Problem D（UTC 2013-04-12）
- **难度**：2000
- **标签**：构造
- **评测类型**：多解（构造）
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个处理器与 $n$ 个内存单元，初始 $a_i = 1$（$i<n$）、$a_n = 0$。每步每个处理器 $i$ 选一个单元 $c_i$，**同时**执行 $a_i \mathrel{+}= a_{c_i}$。要求恰好 $k$ 步后 $a_i = n-i$，输出每步的 $c_1..c_n$。

**约束**：$n \le 10^4$，$k \le 20$，且保证有解。

## 2. 示例与观察

官方样例 1：

```text
输入：
1 1

输出：
1
```

官方样例 2：

```text
输入：
3 2

输出：
2 3 3
3 3 3
```

**观察 1（自己加自己 = 翻倍）**：$c_i = i$ 时 $a_i \leftarrow 2a_i$；$c_i = n$ 时加的是 0（$a_n$ 恒为 0），相当于"空步"。

**观察 2（借用更深的格子）**：$j > i$ 的格子最终值是 $n-j$，都小于 $n-i$；而且它们**先完成、之后不再变化**（后续都加 0）。

**观察 3（二进制拆分）**：把目标 $T = n-i$ 写成 $T = 2^d + r$（$2^d \le T < 2^{d+1}$，$r = T - 2^d \ge 0$）：

- 前 $d$ 步让格子 $i$ 加自己 → 值变成 $2^d$；
- 若 $r > 0$，第 $d+1$ 步加格子 $i + 2^d$（它的最终值恰好是 $n-(i+2^d) = r$）→ 值变成 $T$ ✓；
- 其余步加格子 $n$（0）→ 保持不变。

**观察 4（时间顺序）**：$r < 2^d$，所以被借用的格子 $i+2^d$ 只需要 $d(r)+1 \le d$ 步就完成，**严格早于**格子 $i$ 的加法步 ✓。因此整个方案在 $k \ge \lceil \log_2 n\rceil$ 时总能成功（这也正是一般解存在的必要条件：每步至多翻倍）。

**样例 2 验证**：$n=3, k=2$：格子 1 目标 2 → $2 = 2^1$ → 第 1 步加自己（1→2），第 2 步加 0 ✓；格子 2 目标 1 → 全加 0 ✓；格子 3 恒 0 ✓。输出 `1 3 3 / 3 3 3`（与官方 `2 3 3 / 3 3 3` 等价）。

## 3. 解题思路

![按二进制拆分安排每一步](../../../images/cf291d_build.svg)

对每个 $i$，按 $T = n-i = 2^d + r$ 安排上述三步走；所有格子独立，直接填表输出。

## 4. 正确性证明

**引理 1**：格子 $i$ 的目标 $T = n-i$ 的执行安排（$d$ 次自我翻倍 + 至多一次"加格子 $i+2^d$"）后其值恰为 $T$，之后不再改变。

**证明**：翻倍 $d$ 次得 $2^d$；若 $r>0$，加格子 $i+2^d$ 的值 $r$ 得 $2^d + r = T$ ✓；之后加的格子 $n$ 值为 0 ✓（$a_n$ 恒 0：$c_n=n$ 时 $a_n \mathrel{+}= a_n = 0$）✓。∎

**引理 2**：格子 $i+2^d$ 在格子 $i$ 的加法步之前已经完成，且其值为 $r$。

**证明**：格子 $i+2^d$ 的目标是 $r < 2^d$，其完成步为 $d(r)+1 \le d < d+1$ ✓（$r=0$ 时无需借用）。∎

**引理 3**：所需步数 $\le k$。

**证明**：最大需求为 $d+1 = \lfloor\log_2(n-1)\rfloor + 1 \le k$（$k \ge \lceil\log_2 n\rceil$ 是解存在的必要条件：$k$ 步最多翻倍到 $2^k$）✓。∎

**定理**：算法输出合法操作序列。

**证明**：由引理 1、2，所有格子在第 $k$ 步后同时满足 $a_i = n-i$；由引理 3 步数合法 ✓。∎

## 5. 复杂度分析

- **时间**：$O(nk)$（输出量）。
- **空间**：$O(nk)$（可 $O(n)$ 逐行输出）。
- **与时限的关系**：时限 2 s，$n = 10^4, k = 20$ 实测端到端 31.1 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n,k; if(scanf("%d %d",&n,&k)!=2) return 0;
    // 对每个 i：目标 T = n-i，写成 T = 2^d + r
    //   前 d 步加自己（翻倍到 2^d），r>0 时第 d+1 步加第 i+2^d 个格子（其最终值正好是 r），其余步加第 n 个格子（值恒 0）
    vector<vector<int>> c(k, vector<int>(n+1, n));
    for(int i=1;i<n;i++){
        long long T = n - i;
        int d = 0;
        while((1LL<<(d+1)) <= T) d++;
        long long r = T - (1LL<<d);
        for(int s=0;s<d && s<k;s++) c[s][i] = i;      // 自我翻倍
        if(r > 0){
            int slot = d;                              // 第 d+1 步（0 基）
            if(slot < k) c[slot][i] = i + (int)(1LL<<d);
            // 若 slot 超界，说明该方案不适用（题面保证存在，正常情况下不会发生）
        }
    }
    for(int s=0;s<k;s++){
        for(int i=1;i<=n;i++) printf("%d%c", c[s][i], i==n?'\n':' ');
    }
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    n, k = map(int, sys.stdin.buffer.read().split()[:2])
    c = [[n]*(n+1) for _ in range(k)]
    for i in range(1, n):
        T = n - i
        d = T.bit_length() - 1
        r = T - (1 << d)
        for s in range(min(d, k)):
            c[s][i] = i
        if r > 0 and d < k:
            c[d][i] = i + (1 << d)
    out = []
    for s in range(k):
        out.append(" ".join(str(c[s][i]) for i in range(1, n+1)))
    sys.stdout.write("\n".join(out) + "\n")
main()
```

## 7. 边界情况与易错点

1. **$n = 1$**：只有 $a_1 = 0$ 恒成立，输出任意（如全 1）。
2. **$r = 0$**：不需要借用，全部后续步加 0。
3. **步数不足**：题面保证有解；实现里对越界做了保护。
4. **格子 $n$**：`c_n = n`（加自己，仍是 0）。
5. **同时性**：必须用"旧值"计算新值（checker 里也是这么模拟的）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（由 checker 模拟判定），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf291d.py`（模拟 $k$ 步，检查最终 $a_i = n-i$）。
- **独立暴力对拍**：对 $n \le 4, k \le 4$ 先用**状态空间 BFS** 判断目标是否可达，仅对可达的组合测试；两个实现全部通过 checker，**189 / 189 通过**。
- **最大约束性能**：$n = 10^4, k = 20$，实测端到端 31.1 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 291C Network Mask](https://codeforces.com/problemset/problem/291/C)：同场 C 题。
- [Codeforces 291E Tree-String Problem](https://codeforces.com/problemset/problem/291/E)：同场 E 题。

**延伸思考**：

1. **如果要求步数最少**：下界是 $\lceil\log_2 n\rceil$ 且本构造可以达到。
2. **如果操作是 $a_i \mathrel{+}= a_{c_i} + a_{d_i}$**：可达集合更大、方案需重设计。

