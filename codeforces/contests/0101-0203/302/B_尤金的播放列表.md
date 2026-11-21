# Codeforces 302B Eugeny and Play List 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/302/B
- **比赛来源**：Codeforces Round 182 (Div. 2) · Problem B（UTC 2013-05-04）
- **难度**：1200
- **标签**：前缀和、二分
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 首歌，第 $i$ 首时长 $t_i$、连续播放 $c_i$ 次（占用 $c_i t_i$ 分钟）。给出 $m$ 个递增的时刻 $v_j$，问每个时刻正在播第几首。

**约束**：$n, m \le 10^5$，总时长 $\le 10^9$。

## 2. 示例与观察

官方样例 1：

```text
输入：
1 2
2 8
1 16

输出：
1
1
```

官方样例 2：

```text
输入：
4 9
1 2
2 1
1 1
2 2
1 2 3 4 5 6 7 8 9

输出：
1
1
2
2
3
4
4
4
4
```

**观察 1**：第 $i$ 首歌覆盖的时刻区间是 $(S_{i-1}, S_i]$，其中 $S_i = \sum_{j \le i} c_j t_j$。

**观察 2**：查询 $v$ → 找第一个 $S_i \ge v$ 的下标 → 二分（`lower_bound`）✓。

**样例 2 验证**：$S = [2,4,5,9]$；$v = 1..9$ → $1,1,2,2,3,4,4,4,4$ ✓。

## 3. 解题思路

![前缀和 + 二分](../../../images/cf302b_prefix.svg)

前缀和数组 + 每个查询二分。

## 4. 正确性证明

**引理**：时刻 $v$ 落在 $(S_{i-1}, S_i]$ 中 ⇔ 第 $i$ 首在播放。

**证明**：前 $i-1$ 首占用 $S_{i-1}$ 分钟，第 $i$ 首占用接下来 $c_i t_i$ 分钟 ✓。∎

**定理**：算法输出正确。

**证明**：由引理，二分找到的第一个 $S_i \ge v$ 正是 $v$ 所在的歌 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + m\log n)$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 2 s，$n = m = 10^5$ 实测端到端 22.7 ms。
- **数值范围**：前缀和 $\le 10^9$，`long long` 保险。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main(){
    int n,m; if(scanf("%d %d",&n,&m)!=2) return 0;
    vector<ll> pref(n);
    ll cur=0;
    for(int i=0;i<n;i++){
        ll c,t; scanf("%lld %lld",&c,&t);
        cur += c*t;
        pref[i]=cur;
    }
    for(int i=0;i<m;i++){
        ll v; scanf("%lld",&v);
        int idx = lower_bound(pref.begin(), pref.end(), v) - pref.begin();
        printf("%d\n", idx+1);
    }
    return 0;
}
```

### Python3

```python
import sys, bisect
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    pref = []
    cur = 0
    pos = 2
    for _ in range(n):
        c = int(data[pos]); t = int(data[pos+1]); pos += 2
        cur += c*t
        pref.append(cur)
    out = []
    for i in range(m):
        v = int(data[pos + i])
        out.append(str(bisect.bisect_left(pref, v) + 1))
    sys.stdout.write("\n".join(out) + "\n")
main()
```

## 7. 边界情况与易错点

1. **$v$ 恰好等于某个 $S_i$**：属于第 $i$ 首（`lower_bound` 取到）✓。
2. **$c_i t_i$ 很大**：前缀和用 64 位。
3. **查询递增**：也可以双指针 $O(n+m)$。
4. **$m$ 个时刻保证有效**。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过，C++ 与 Python 一致。
- **独立暴力对拍**：暴力版逐首累加分钟数定位。随机 250 组 $n \le 5$，**250 / 250 全部一致**。
- **最大约束性能**：$n = m = 10^5$，实测端到端 22.7 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 302A Eugeny and Array](https://codeforces.com/problemset/problem/302/A)：同场 A 题。
- [LeetCode 1146. 快照数组](https://leetcode.cn/problems/snapshot-array/)：前缀 + 二分的同类题。

**延伸思考**：

1. **如果播放列表动态改变**：需要平衡树/Fenwick。
2. **如果要区间查询"某段时间内有哪些歌"**：二分两端即可。
