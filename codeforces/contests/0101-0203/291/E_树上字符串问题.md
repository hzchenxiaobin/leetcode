# Codeforces 291E Tree-String Problem 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/291/E
- **比赛来源**：Croc Champ 2013 - Qualification Round · Problem E（UTC 2013-04-12）
- **难度**：2500
- **标签**：树、字符串匹配、KMP
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：有根树（根 1），每条边（父 → 子）上写着一个非空小写字符串。一个"位置"是某条边上的某个字母 $(v,x)$。若从 $(v,x)$ 向下沿树走到 $(u,y)$，把经过的字母依次连起来得到字符串，求这样得到的串**恰好等于 $t$** 的位置对个数。

**约束**：$n \le 10^5$，所有字符串字母总数 $\le 3\times10^5$，$|t| \ge 2$。

## 2. 示例与观察

官方样例 1：

```text
输入：
7
1 ab
5 bacaba
1 abacaba
2 aca
5 ba
2 ba
aba

输出：
6
```

官方样例 2：

```text
输入：
7
1 ab
5 bacaba
1 abacaba
2 aca
5 ba
2 ba
bacaba

输出：
4
```

**观察 1（关键转化）**：把"根到每个点"路径上的所有字母按顺序连起来，得到一个"路径串"。从 $(v,x)$ 向下到 $(u,y)$ 的字母序列，恰好是这个路径串的一段**连续子串**。于是问题变成：

> 对每个位置（即路径串的每个字符位置），判断以它结尾、长度为 $|t|$ 的后缀是否等于 $t$，统计这样的位置数。

**观察 2**：不同位置属于不同边，互不重复 → 每个匹配只计一次，不存在重复计数 ✓。

**观察 3（KMP 沿 DFS 走）**：DFS 时维护"当前路径串的后缀与 $t$ 的前缀的最长匹配长度" $j$。每追加一个字符 $c$：沿失配链回溯到可以匹配的位置，$j$ 增 1；若 $j = |t|$ 则记一次匹配并令 $j = \pi[j-1]$ 继续。回溯（离开子树）时把 $j$ 恢复到进入该边之前的值 → 用一个栈保存每个字符对应的旧状态即可。

## 3. 解题思路

![树上沿路径做 KMP](../../../images/cf291e_kmp.svg)

1. 对 $t$ 求前缀函数 $\pi$；
2. 迭代 DFS（显式栈，避免 $10^5$ 深度爆栈）；进入一条边时逐字符推进 KMP 并把旧状态压栈；
3. 退出该边时按字符数弹栈恢复状态；
4. 每完成一次匹配 `ans++`。

## 4. 正确性证明

**引理 1**：从位置 $(v,x)$ 向下到 $(u,y)$ 得到的字符串，等于"根到 $u$ 的路径串"中以 $(u,y)$ 结尾、长度为（路径距离）的那段连续子串。

**证明**：向下走时依次经过 $s_v$ 的后缀、中间各边的整串、$s_u$ 的前缀；这些在路径串中正是连续的一段 ✓。∎

**引理 2**：KMP 状态 $j$ 恰好等于"当前路径串后缀与 $t$ 前缀的最长公共长度"。

**证明**：KMP 的标准不变式，逐字符推进与失配回溯都保持该性质 ✓。∎

**引理 3**：当且仅当某位置使 $j$ 达到 $|t|$ 时，以它结尾的长度 $|t|$ 子串等于 $t$。

**证明**：由引理 2，$j = |t|$ 意味着后缀长度 $|t|$ 与 $t$ 完全匹配 ✓；反之匹配时 $j$ 必达 $|t|$ ✓。∎

**定理**：算法输出正确的对数。

**证明**：由引理 1 把位置对转化为"路径串中长度为 $|t|$ 的子串"；由引理 3，DFS 中每次 $j$ 达到 $|t|$ 恰好对应一个匹配的结束位置，且每个结束位置只被访问一次 ✓。∎

## 5. 复杂度分析

- **时间**：$O(\sum|s_v| + |t|)$（每个字符最多被 KMP 处理一次，失配指针均摊）。
- **空间**：$O(n + \sum|s_v|)$。
- **与时限的关系**：时限 1 s，字母总数 $3\times10^5$、$n = 10^5$（链）实测端到端 25 ms 级别（见验证记录）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; if(scanf("%d",&n)!=1) return 0;
    vector<vector<pair<int,string>>> ch(n+1);
    for(int v=2;v<=n;v++){
        int p; char buf[300005];
        scanf("%d %s",&p,buf);
        ch[p].push_back({v, string(buf)});
    }
    static char t[300005];
    scanf("%s",t);
    int L = strlen(t);
    vector<int> pi(L,0);
    for(int i=1;i<L;i++){
        int j=pi[i-1];
        while(j>0 && t[i]!=t[j]) j=pi[j-1];
        if(t[i]==t[j]) j++;
        pi[i]=j;
    }
    long long ans=0;
    int state=0;
    vector<int> nodeStack{1}, childIdx{0}, edgeLen{0};   // edgeLen[0]=0（根）
    vector<int> saved;                                  // 每追加一个字符前保存旧 state
    while(!nodeStack.empty()){
        int v = nodeStack.back();
        if(childIdx.back() >= (int)ch[v].size()){
            nodeStack.pop_back(); childIdx.pop_back();
            int k = edgeLen.back(); edgeLen.pop_back();
            for(int i=0;i<k;i++){ state = saved.back(); saved.pop_back(); }
            continue;
        }
        auto &e = ch[v][childIdx.back()++];
        for(char c : e.second){
            int j = state;
            while(j>0 && t[j]!=c) j = pi[j-1];
            if(t[j]==c) j++;
            int ns;
            if(j==L){ ans++; ns = pi[j-1]; }
            else ns = j;
            saved.push_back(state);
            state = ns;
        }
        nodeStack.push_back(e.first);
        childIdx.push_back(0);
        edgeLen.push_back((int)e.second.size());
    }
    printf("%lld\n", ans);
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    ch = [[] for _ in range(n+1)]
    pos = 1
    for v in range(2, n+1):
        p = int(data[pos]); s = data[pos+1].decode(); pos += 2
        ch[p].append((v, s))
    t = data[pos].decode()
    L = len(t)
    pi = [0]*L
    for i in range(1, L):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
    ans = 0
    state = 0
    node_stack = [1]; child_idx = [0]; edge_len = [0]
    saved = []
    while node_stack:
        v = node_stack[-1]
        if child_idx[-1] >= len(ch[v]):
            node_stack.pop(); child_idx.pop()
            k = edge_len.pop()
            for _ in range(k):
                state = saved.pop()
            continue
        to, s = ch[v][child_idx[-1]]
        child_idx[-1] += 1
        for c in s:
            j = state
            while j > 0 and t[j] != c:
                j = pi[j-1]
            if t[j] == c:
                j += 1
            if j == L:
                ans += 1
                ns = pi[j-1]
            else:
                ns = j
            saved.append(state)
            state = ns
        node_stack.append(to); child_idx.append(0); edge_len.append(len(s))
    sys.stdout.write(str(ans) + "\n")
main()
```

## 7. 边界情况与易错点

1. **深链**：$n = 10^5$ 必须迭代 DFS。
2. **$|t| = 2$**：题面下界。
3. **回溯恢复状态**：必须按该边追加的字符数弹栈。
4. **一条边内多次匹配**：逐字符判断，不能只判一次。
5. **答案规模**：可达 $3\times10^5$，用 64 位。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：2 / 2 通过（6、4），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版对每个边上的每个字符位置，用"根到该点的路径串"直接比较后缀。随机 200 组（$n \le 7$，边长 $\le 3$，字母表 `ab`），**200 / 200 全部一致**（最初我的暴力把内层边的字符重复计数，修正后一致）。
- **最大约束性能**：$n = 10^5$ 的链、字母总数 $3\times10^5$，实测端到端 22.4 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 291D Parallel Programming](https://codeforces.com/problemset/problem/291/D)：同场 D 题。
- [LeetCode 1408. 数组中的字符串匹配](https://leetcode.cn/problems/string-matching-in-an-array/)：字符串匹配的入门题。

**延伸思考**：

1. **如果路径允许转弯（向下再向上）**：需要点分治或 AC 自动机。
2. **如果要求统计所有 $t$ 的出现（任意长度）**：哈希或后缀结构。

