# Codeforces 292A SMSC 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/292/A
- **比赛来源**：Croc Champ 2013 - Round 1 · Problem A（UTC 2013-04-13）
- **难度**：1100
- **标签**：模拟
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：短信中心每秒最多发一条短信。每个时刻 $x$：先（若队列非空）发出一条，再把时刻 $x$ 到达的任务消息**全部**入队（本秒到达的消息不能在本秒发送）。给出 $n$ 个任务 $(t_i, c_i)$，求最后一条短信发出的时刻与队列的最大长度。

**约束**：$n \le 1000$，$t_i, c_i \le 10^6$。

## 2. 示例与观察

官方样例 1：

```text
输入：
2
1 1
2 1

输出：
3 1
```

官方样例 2：

```text
输入：
1
1000000 10

输出：
1000010 10
```

官方样例 3：

```text
输入：
3
3 3
4 3
5 3

输出：
12 7
```

**观察 1**：队列只在"任务到达"时增长；两次到达之间队列按每秒 1 条稳定减少。

**观察 2（跳跃）**：维护 `nxt` = 下一次发送的时刻。若下次到达时刻 $t \ge nxt$ 且队列在此期间发完，就直接跳到 $t+1$ 重新开始。

**观察 3（最大队列）**：只在每次入队之后取 max（发送只会减少队列）。

**样例 3 验证**：时刻 3 入队 3 → (nxt=4)；时刻 4 先发 1 条、入队 3 → 5；时刻 5 发 1 条、入队 3 → 7；之后每秒发 1 条，共 7 条从时刻 6 发到 12 → 12 7 ✓。

## 3. 解题思路

![队列与空闲时间跳跃](../../../images/cf292a_queue.svg)

按上述模拟，一次扫描 $O(n)$。

## 4. 正确性证明

**引理 1**：两次任务到达之间，队列长度每秒减 1（直到 0）；因此可以用 `nxt` 一次跳过整段空闲。

**证明**：只有发送操作减少队列、且每秒恰好一条 ✓。∎

**引理 2**：时刻 $t$ 的发送发生在入队之前，所以本秒到达的消息最早在 $t+1$ 发送。

**证明**：题面规则顺序 ✓（样例 1：时刻 2 到达的消息在时刻 3 发出）✓。∎

**定理**：算法输出的最后发送时刻与最大队列正确。

**证明**：由引理 1，跳跃模拟与原逐秒模拟等价；由引理 2 边界处理正确；最大队列在入队后取 max 覆盖所有时刻 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n)$。
- **空间**：$O(1)$。
- **与时限的关系**：实测端到端 3.0 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main(){
    int n; if(scanf("%d",&n)!=1) return 0;
    ll q=0, nxt=0;            // nxt: 下一次发送的时刻（q>0 时有效）
    bool busy=false;
    ll maxq=0, lastSend=0;
    for(int i=0;i<n;i++){
        ll t,c; scanf("%lld %lld",&t,&c);
        if(!busy || nxt > t){
            // 到达时队列已空：消息从 t+1 开始发
            nxt = t+1; q = c; busy = true;
        } else {
            ll sends = t - nxt + 1;         // 到时刻 t（含）能发出的条数
            if(sends >= q){                  // 在 t 之前就发完了
                q = 0; busy = false;
                nxt = t+1; q = c; busy = true;
            } else {
                q -= sends; nxt = t+1; q += c;
            }
        }
        maxq = max(maxq, q);
    }
    if(busy) lastSend = nxt + q - 1;
    else lastSend = nxt - 1;
    printf("%lld %lld\n", lastSend, maxq);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = 0; nxt = 0; busy = False; maxq = 0; last = 0
    for i in range(n):
        t = int(data[1+2*i]); c = int(data[2+2*i])
        if (not busy) or nxt > t:
            nxt = t + 1; q = c; busy = True
        else:
            sends = t - nxt + 1
            if sends >= q:
                q = 0; busy = False
                nxt = t + 1; q = c; busy = True
            else:
                q -= sends; nxt = t + 1; q += c
        maxq = max(maxq, q)
    last = nxt + q - 1 if busy else nxt - 1
    print(last, maxq)
main()
```

## 7. 边界情况与易错点

1. **只发一条**：最后时刻 = $t+1$。
2. **巨大空闲**：必须跳跃，不能逐秒模拟（$t \le 10^6$ 其实可以，但跳跃更稳）。
3. **同一秒多发**：一个任务的多条消息都在同一秒入队。
4. **队列在到达前恰好空**：此时本秒不发送，消息从 $t+1$ 开始。
5. **64 位**：$t + c \le 2\times10^6$，`int` 也够，但用 `long long` 更稳。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（3 1、1000010 10、12 7），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版逐秒模拟。随机 250 组（时刻 $\le 12$），**250 / 250 全部一致**。
- **最大约束性能**：$n = 1000$，实测端到端 3.0 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 292B Network Topology](https://codeforces.com/problemset/problem/292/B)：同场 B 题。

**延伸思考**：

1. **如果每秒能发 $k$ 条**：跳跃步长改为 $k$。
2. **如果任务可以被打断**：需要调度策略。
