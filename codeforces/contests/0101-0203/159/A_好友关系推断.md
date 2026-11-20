# Codeforces 159A 好友关系推断 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/159/A
- **比赛来源**：VK Cup 2012 Qualification Round 2 · Problem A（UTC 2012-03-09）
- **难度**：1400
- **标签**：实现、数据结构
- **评测类型**：特殊评测（输出顺序任意）
- **限制**：时间 3 s / 内存 256 MB

**题意**：给出 $n$ 条消息日志「$A$ 在时刻 $t$ 给 $B$ 发消息」与整数 $d$。若 $A$ 在 $t_1$ 给 $B$ 发过消息、$B$ 在 $t_2$ 给 $A$ 发过消息且 $0<t_2-t_1\le d$，则称 $B$ 的这条消息是 $A$ 的回复。若存在至少一次这样的"一方回复另一方"，两人就是好友。求所有好友对。

**约束**：$n\le1000$：枚举消息对 $O(n^2)$ 即可。输出顺序任意（本题为特殊评测）。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
4 1
vasya petya 1
petya vasya 2
anya ivan 2
ivan anya 4

输出：
1
petya vasya
```

vasya→petya 在 $t=1$，petya→vasya 在 $t=2$，差 $1\le d$ ⇒ 好友 ✓；anya→ivan 在 2、ivan→anya 在 4，差 $2>d=1$ ⇒ 不是 ✓

官方样例 2（输入 / 输出原样）：

```text
输入：
1 1000
a b 0

输出：
0
```

只有一条消息，没有"往来" ⇒ 0 ✓（注意 $t$ 可以为 0）

![一条日志里找方向相反、时间差在 (0,d] 的两条消息](../../../images/cf159a_pairs.svg)

**观察**：对每条消息 $i=(A,B,t_1)$，只需找另一条方向相反的消息 $j=(B,A,t_2)$；若恰好有一条满足时间条件，就把无序对 $\{A,B\}$ 加入答案集合（用集合去重）。

## 3. 解题思路

1. 读入全部消息；
2. 双重循环 $i<j$：若 `A[i]==B[j] && B[i]==A[j]` 且 `0 < T[j]-T[i] <= d`，把排序后的 $(A_i,B_i)$ 放入 `set`；
3. 输出集合大小与内容。

![样例 1：只有 vasya/petya 在 (0,d] 内互发](../../../images/cf159a_sample.svg)

## 4. 正确性证明

**引理**：消息对 $(i,j)$ 构成一次"回复" ⟺ 两条消息方向相反且 $0<t_j-t_i\le d$。

**证明**：题面定义：$B$ 在 $t_2$ 回复 $A$ 在 $t_1$ 的消息需要 $A_i=B_j$、$B_i=A_j$ 且 $0<t_2-t_1\le d$，即 $A$ 发给 $B$、$B$ 发给 $A$、时间差在范围内 ✓ ∎

**定理**：程序输出所有好友对，且每对只出现一次。

**证明**：程序枚举了所有消息对（$i<j$ 覆盖全部无序消息对），由引理凡是满足条件的都记为好友；用有序对 $(x,y)$（$x<y$）作为集合键，保证同一对用户只计一次 ✓ 反向的回复关系（若两条消息各自满足"回复"）也只会得到同一个键 ✓ ∎

## 5. 复杂度分析

- **时间**：$O(n^2)\le10^6$ 次比较，实测约 6 ms（$n=1000$）。
- **空间**：$O(n)$。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, d;
    if (scanf("%d %d", &n, &d) != 2) return 0;
    vector<string> A(n), B(n);
    vector<long long> T(n);
    char a[64], b[64];
    for (int i = 0; i < n; i++) {
        scanf("%63s %63s %lld", a, b, &T[i]);
        A[i] = a; B[i] = b;
    }
    set<pair<string,string>> friends;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            if (A[i] == B[j] && B[i] == A[j] && A[i] != B[i]) {   // 方向相反的一对消息
                long long gap = T[j] - T[i];
                if (0 < gap && gap <= d) {
                    string x = A[i], y = B[i];
                    if (x > y) swap(x, y);
                    friends.insert({x, y});
                }
            }
        }
    printf("%d\n", (int)friends.size());
    for (auto &p : friends) printf("%s %s\n", p.first.c_str(), p.second.c_str());
    return 0;
}
```

### Python3

```python
import sys


def main():
    data = sys.stdin.read().split()
    n, d = int(data[0]), int(data[1])
    A = []; B = []; T = []
    p = 2
    for _ in range(n):
        A.append(data[p]); B.append(data[p + 1]); T.append(int(data[p + 2])); p += 3
    friends = set()
    for i in range(n):
        for j in range(i + 1, n):
            if A[i] == B[j] and B[i] == A[j] and A[i] != B[i]:
                gap = T[j] - T[i]
                if 0 < gap <= d:
                    x, y = A[i], B[i]
                    if x > y:
                        x, y = y, x
                    friends.add((x, y))
    out = [str(len(friends))]
    for x, y in sorted(friends):
        out.append(x + " " + y)
    print("\n".join(out))


main()
```

## 7. 边界情况与易错点

1. **$t$ 可以为 0**（样例 2），不要用 0 当哨兵。
2. **时间差必须严格大于 0**：同时刻的消息不算回复。
3. **差必须 ≤ $d$**：等于 $d$ 算。
4. **去重**：同一对用户可能有多组往来消息，只输出一次。
5. **自己给自己发**：题面消息的 $A_i\ne B_i$？未保证，但"好友"要求两人，代码里加了 `A[i] != B[i]` 保护。
6. **输出顺序任意**：本题特殊评测；本实现按字典序输出。
7. **$n=1$**：答案 0。
8. **名字是字符串**：用 `map`/`set` 处理。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/159/A_好友关系推断.md`
- **官方样例**：$2/2$ 通过（`1 / petya vasya`、`0`）。
- **独立对拍**：另写"对每个有序消息对检查反方向与时间差"的独立实现，对 $200$ 组随机日志（$n\le8$、4 个用户、时间为非降随机）比较好友集合（排序后比较），全部一致。
- **性能**：$n=1000$ 单次约 6 ms。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 159B Matchmaker](https://codeforces.com/problemset/problem/159/B)：同场 B 题。
- [Codeforces 159E Zebra Tower](https://codeforces.com/problemset/problem/159/E)：同场 E 题。
- [LeetCode 1791. 找出星型图的中心节点](https://leetcode.cn/problems/find-center-of-star-graph/)：图关系判定。

**延伸思考**：

1. **若要求"互相回复"**（双方都有回复）：判据变成两个方向都存在满足时间差的消息。
2. **若时间差可以是负的**（乱序日志）：需要排序后再处理。
3. **若 $n$ 到 $10^5$**：按 (发送者,接收者) 分桶，桶内双指针，$O(n\log n)$。
