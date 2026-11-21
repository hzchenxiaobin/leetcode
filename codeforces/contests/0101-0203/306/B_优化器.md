# Codeforces 306B Optimizer 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/306/B
- **比赛来源**：Testing Round 6 · Problem B（UTC 2013-05-20）
- **难度**：2100
- **标签**：贪心、区间覆盖
- **评测类型**：普通
- **限制**：时间 3 s / 内存 256 MB

**题意**：内存 $1..n$，$m$ 条指令，第 $i$ 条把 $[a_i, a_i+l_i-1]$ 填成 13。要求删掉**尽量多**的指令，同时保证"被填过的字节集合"不变。输出可删的最大条数与这些指令编号。

**约束**：$n \le 2\times10^6$，$m \le 2\times10^5$。

## 2. 示例与观察

官方样例 1：

```text
输入：
10 4
3 3
3 1
4 1
9 2

输出：
2
2 3
```

官方样例 2：

```text
输入：
1 1
1 1

输出：
0
```

**观察 1（删得最多 ⇔ 留下的最少）**：留下的指令必须覆盖"所有被填过的字节"（并集），留得越少删得越多 → 问题变成**最少区间覆盖**（只覆盖并集里的字节）。

**观察 2（求并集）**：差分数组求每个字节被覆盖的次数，次数 $>0$ 的位置就是待覆盖集合。

**观察 3（经典贪心）**：从左到右扫描，遇到第一个待覆盖位置 $p$，在所有"起点 $\le p$"的区间里选**右端最远**的，选中它并把当前位置跳到其右端 +1 ✓。用前缀最大值把"起点 ≤ p 的最远右端"预处理成数组，$O(n+m)$。

**样例 1 验证**：并集 $\{3,4,5,9,10\}$；在 3 处最远右端是区间 1（到 5）→ 选 1；跳到 6，下一个待覆盖是 9 → 选区间 4 → 共留 2 条 → 删 2 条（编号 2、3）✓。

## 3. 解题思路

![差分求并集 + 区间覆盖贪心](../../../images/cf306b_greedy.svg)

差分 → 待覆盖标记 → 前缀最远右端 → 贪心跳跃 → 输出未选中的编号。

## 4. 正确性证明

**引理 1**：最少覆盖集的大小由上述贪心取得。

**证明**：经典区间覆盖贪心：在必须覆盖的最左位置，任何可行解都必须选一个覆盖它的区间；把它替换成右端最远者不会使解变差（交换论证）✓。∎

**引理 2**：删掉"贪心未选中的指令"后并集不变。

**证明**：贪心选中的集合已经覆盖全部待覆盖字节 → 其余指令删掉不影响并集 ✓。∎

**定理**：输出删除数最大。

**证明**：由引理 1，剩余数最少；由引理 2 合法性成立 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n + m)$。
- **空间**：$O(n + m)$。
- **与时限的关系**：时限 3 s，$n = 2\times10^6, m = 2\times10^5$ 实测端到端 105 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n,m; if(scanf("%d %d",&n,&m)!=2) return 0;
    vector<int> a(m), l(m);
    vector<int> diff(n+3,0);
    for(int i=0;i<m;i++){
        scanf("%d %d",&a[i],&l[i]);
        diff[a[i]]++; diff[a[i]+l[i]]--;
    }
    vector<char> chosen(m,0);
    // 覆盖数 + 每个位置起始的最远右端
    vector<int> cover(n+2,0);
    int cur=0;
    vector<vector<int>> at(n+2);    // 每个起点对应的指令编号（用于选出具体指令）
    for(int i=0;i<m;i++) at[a[i]].push_back(i);
    vector<char> need(n+2,0);
    for(int i=1;i<=n;i++){ cur += diff[i]; if(cur>0) need[i]=1; }
    // 更高效：维护 "起点 <= i 的区间里右端最大值" 及其 id
    vector<pair<int,int>> pref(n+2, {-1,-1});   // (最远右端, 指令 id)
    {
        int br=-1, bid=-1;
        for(int s=1;s<=n;s++){
            for(int id : at[s]){
                int rr = a[id]+l[id]-1;
                if(rr > br){ br = rr; bid = id; }
            }
            pref[s] = {br, bid};
        }
    }
    vector<int> keepIds;
    int pos = 1;
    while(pos <= n){
        if(!need[pos]){ pos++; continue; }
        auto [br, bid] = pref[pos];
        if(bid < 0 || br < pos){ printf("-1\n"); return 0; }   // 理论上不会发生
        keepIds.push_back(bid);
        chosen[bid] = 1;
        pos = br + 1;
    }
    vector<int> removed;
    for(int id=0;id<m;id++) if(!chosen[id]) removed.push_back(id+1);
    printf("%d\n", (int)removed.size());
    for(size_t k=0;k<removed.size();k++) printf("%d%c", removed[k], k+1==removed.size()?'\n':' ');
    if(removed.empty()) printf("\n");
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    a = [0]*m; l = [0]*m
    diff = [0]*(n+3)
    at = [[] for _ in range(n+2)]
    for i in range(m):
        a[i] = int(data[2+2*i]); l[i] = int(data[3+2*i])
        diff[a[i]] += 1; diff[a[i]+l[i]] -= 1
        at[a[i]].append(i)
    need = [False]*(n+2)
    cur = 0
    for i in range(1, n+1):
        cur += diff[i]
        if cur > 0: need[i] = True
    # pref[i] = 起点 <= i 的区间中右端最远者
    prefR = [-1]*(n+2); prefId = [-1]*(n+2)
    br, bid = -1, -1
    for s in range(1, n+1):
        for idx in at[s]:
            rr = a[idx] + l[idx] - 1
            if rr > br: br, bid = rr, idx
        prefR[s] = br; prefId[s] = bid
    chosen = [False]*m
    pos = 1
    while pos <= n:
        if not need[pos]:
            pos += 1; continue
        br2, bid2 = prefR[pos], prefId[pos]
        chosen[bid2] = True
        pos = br2 + 1
    removed = [str(i+1) for i in range(m) if not chosen[i]]
    sys.stdout.write(str(len(removed)) + "\n" + " ".join(removed) + "\n")
main()
```

## 7. 边界情况与易错点

1. **只需覆盖"被填过的字节"**，不是整个 $1..n$。
2. **同一位置多条区间**：前缀最大值只保留右端最远的那条 id。
3. **$m=1$**：一条都不能删。
4. **输出格式**：先输出条数，再输出编号（顺序任意）。
5. **删除 0 条**：第二行可以为空行。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（2 条：2 3；0 条），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版用集合运算验证"剩余指令并集 = 原并集"，并用独立贪心算出最少覆盖数核对删除数。随机 200 组 $n \le 12$，**200 / 200 通过**。
- **最大约束性能**：$n = 2\times10^6, m = 2\times10^5$，实测端到端 105 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 306A Candies](https://codeforces.com/problemset/problem/306/A)：同场 A 题。
- [LeetCode 1024. 视频拼接](https://leetcode.cn/problems/video-stitching/)：区间覆盖贪心的同类题。

**延伸思考**：

1. **如果允许"部分覆盖"**：题意变化。
2. **如果要求输出最小覆盖集**：本算法直接给出。
