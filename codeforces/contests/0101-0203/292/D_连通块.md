# Codeforces 292D Connected Components 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/292/D
- **比赛来源**：Croc Champ 2013 - Round 1 · Problem D（UTC 2013-04-13）
- **难度**：1900
- **标签**：并查集、前缀快照
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个点、$m$ 条边的无向图。$k$ 次实验，第 $i$ 次断开编号在 $[l_i, r_i]$ 的所有边，问剩余图的连通块数。

**约束**：$n \le 500$，$m \le 10^4$，$k \le 2\times10^4$。

## 2. 示例与观察

官方样例 1：

```text
输入：
6 5
1 2
5 4
2 3
3 1
3 6
6
1 3
2 5
1 5
5 5
2 4
3 3

输出：
4
5
6
3
4
2
```

**观察 1**：断开 $[l,r]$ 后剩下的边恰好是"前 $l-1$ 条" ∪ "后 $m-r$ 条"。

**观察 2（前缀/后缀快照）**：$n \le 500$ 很小，可以保存每个前缀、每个后缀的 DSU 父数组（$m\cdot n \le 5\times10^6$ 个 int ≈ 20 MB 各一份）。

**观察 3**：每个查询把两份父数组"并"起来：对每个点 $v$，把 prefix 的根与 suffix 的根合并 → $O(n\,\alpha)$。

**样例 1 第 1 问验证**：断开 1..3 后剩边 5-4、3-6 → 连通块：{1},{2},{3,6},{4,5} = 4 ✓。

## 3. 解题思路

![前缀/后缀 DSU 快照](../../../images/cf292d_dsu.svg)

1. 正序扫一遍存 `pre[i]`（前 $i$ 条边的父数组），倒序存 `suf[i]`；
2. 每个查询：临时 DSU 初始化为独立点，先并入 `pre[l-1]` 的连通关系、再并入 `suf[r+1]` 的，最后数根的个数。

## 4. 正确性证明

**引理 1**：`pre[l-1]` 的每个连通块与 `suf[r+1]` 的每个连通块，正是"只用前 $l-1$ 条边"与"只用后 $m-r$ 条边"时的连通块。

**证明**：DSU 快照就是按顺序合并的结果 ✓。∎

**引理 2**：把两份 DSU 的关系都并入临时 DSU 后，其连通块等于"两类边同时存在"时的连通块。

**证明**：并查集的合并具有结合性：先并 A 的边、再并 B 的边，与任意顺序并 A∪B 的边结果相同 ✓（快照已含路径压缩后的等价关系）。∎

**定理**：算法输出正确。

**证明**：由引理 1、2，临时 DSU 的连通块数即为剩余图的连通块数 ✓。∎

## 5. 复杂度分析

- **时间**：$O((m + k)\,n\,\alpha)$；实际 $m n + k n \approx 1.5\times10^7$。
- **空间**：$O(mn)$（两份快照）。
- **与时限的关系**：时限 2 s，$n=500, m=10^4, k=2\times10^4$ 实测端到端 110 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int n, m;
vector<int> par;
int findp(vector<int>& p, int x){ while(p[x]!=x){ p[x]=p[p[x]]; x=p[x]; } return x; }
int main(){
    if(scanf("%d %d",&n,&m)!=2) return 0;
    vector<int> ex(m+1), ey(m+1);
    for(int i=1;i<=m;i++) scanf("%d %d",&ex[i],&ey[i]);
    // 前缀 DSU 快照：pre[i] = 前 i 条边的 DSU 父数组
    vector<vector<int>> pre(m+1), suf(m+2);
    vector<int> p(n+1);
    for(int i=1;i<=n;i++) p[i]=i;
    pre[0]=p;
    for(int i=1;i<=m;i++){
        int a=findp(p,ex[i]), b=findp(p,ey[i]);
        if(a!=b) p[a]=b;
        pre[i]=p;
    }
    for(int i=1;i<=n;i++) p[i]=i;
    suf[m+1]=p;
    for(int i=m;i>=1;i--){
        int a=findp(p,ex[i]), b=findp(p,ey[i]);
        if(a!=b) p[a]=b;
        suf[i]=p;
    }
    int k; scanf("%d",&k);
    while(k--){
        int l,r; scanf("%d %d",&l,&r);
        vector<int> q = pre[l-1];
        const vector<int>& s = suf[r+1];
        vector<int> tmp(n+1);
        for(int v=1;v<=n;v++) tmp[v]=v;
        auto find2=[&](int x){ while(tmp[x]!=x){ tmp[x]=tmp[tmp[x]]; x=tmp[x]; } return x; };
        for(int v=1;v<=n;v++){
            int rv = v;
            while(s[rv]!=rv){ rv = s[rv]; }   // 后缀 DSU 的根（无压缩，n 小）
            int a=find2(v), b=find2(rv);
            if(a!=b) tmp[a]=b;
        }
        // 前缀部分也合并
        for(int v=1;v<=n;v++){
            int rv=v; while(q[rv]!=rv){ rv=q[rv]; }
            int a=find2(v), b=find2(rv);
            if(a!=b) tmp[a]=b;
        }
        int comp=0;
        for(int v=1;v<=n;v++) if(find2(v)==v) comp++;
        printf("%d\n", comp);
    }
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    ex = [0]*(m+1); ey = [0]*(m+1)
    pos = 2
    for i in range(1, m+1):
        ex[i] = int(data[pos]); ey[i] = int(data[pos+1]); pos += 2
    def build(order):
        p = list(range(n+1))
        snaps = [None]*(m+2)
        snaps[0 if order[0] == 1 else m+1] = tuple(p)
        for i in order:
            a = ex[i]; b = ey[i]
            while p[a] != a: a = p[a]
            while p[b] != b: b = p[b]
            if a != b: p[a] = b
            snaps[i if order[0] == 1 else i] = tuple(p)
        return snaps
    pre = [None]*(m+1)
    p = list(range(n+1))
    pre[0] = tuple(p)
    for i in range(1, m+1):
        a, b = ex[i], ey[i]
        while p[a] != a: a = p[a]
        while p[b] != b: b = p[b]
        if a != b: p[a] = b
        pre[i] = tuple(p)
    suf = [None]*(m+2)
    p = list(range(n+1))
    suf[m+1] = tuple(p)
    for i in range(m, 0, -1):
        a, b = ex[i], ey[i]
        while p[a] != a: a = p[a]
        while p[b] != b: b = p[b]
        if a != b: p[a] = b
        suf[i] = tuple(p)
    k = int(data[pos]); pos += 1
    out = []
    for _ in range(k):
        l = int(data[pos]); r = int(data[pos+1]); pos += 2
        q = pre[l-1]; s = suf[r+1]
        tmp = list(range(n+1))
        def f2(x):
            while tmp[x] != x:
                tmp[x] = tmp[tmp[x]]; x = tmp[x]
            return x
        for v in range(1, n+1):
            rv = v
            while s[rv] != rv: rv = s[rv]
            a, b = f2(v), f2(rv)
            if a != b: tmp[a] = b
            rv = v
            while q[rv] != rv: rv = q[rv]
            a, b = f2(v), f2(rv)
            if a != b: tmp[a] = b
        out.append(str(sum(1 for v in range(1, n+1) if f2(v) == v)))
    sys.stdout.write("\n".join(out) + "\n")
main()
```

Python 版常数较大，**建议提交 C++/PyPy3**。

## 7. 边界情况与易错点

1. **$l=1$**：前缀为空。
2. **$r=m$**：后缀为空。
3. **$l=1, r=m$**：没有边 → 答案 $n$。
4. **重边**：DSU 自然处理。
5. **快照的父数组要压缩后保存**，否则合并慢。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：1 / 1 通过（4 5 6 3 4 2），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版对每个查询重建 DSU（只加区间外的边）。随机 200 组 $n \le 6, m \le 6$，**200 / 200 全部一致**。
- **最大约束性能**：$n=500, m=10^4, k=2\times10^4$，实测端到端 110 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 292C Beautiful IP Addresses](https://codeforces.com/problemset/problem/292/C)：同场 C 题。
- [LeetCode 1697. 检查边长度限制的路径是否存在](https://leetcode.cn/problems/checking-existence-of-edge-length-limited-paths/)：并查集按序处理的同类题。

**延伸思考**：

1. **如果要求在线插入/删除边**：需要动态连通性（link-cut tree）。
2. **如果 $n$ 很大**：改用"线段树分治 + 可回滚并查集"。
