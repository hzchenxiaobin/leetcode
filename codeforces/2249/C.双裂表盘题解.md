# Codeforces 双裂表盘 题解

## 1. 题目概述

- **标题 / 题号**：双裂表盘（Codeforces 2249C，英文名 Double-Rift Dial）
- **链接**：https://codeforces.com/problemset/problem/2249/C
- **来源**：Codeforces Round 1112 (Div. 1) · Problem C
- **难度**：2000（1750 分）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：数据结构，线段树，扫描线，环形区间，实现

**题意**：把排列 $p$ 顺时针写在圆盘上。选起点 $s$，从 $p_s$ 起顺时针读满一圈，得到的序列

$$q=[p_s,p_{s+1},\dots,p_n,p_1,\dots,p_{s-1}]$$

长度仍是 $n$。对 $q$ 的每个非空前缀 $[q_1,\dots,q_k]$，令 $S$ 为其值集合，把 $S$ 拆成极大的连续整数段，称为 $S$ 的**块**（例如 $S=\{1,2,5,7,8,9\}$ 有 3 块）。若对**每个**非空前缀，对应集合的块数都 $\le 2$，则称起点 $s$ 是好的。求好起点的个数。多测：第一行 $t$，每组先给 $n$，再给一行 $n$ 个整数。

**约束**：

- $1\le t\le 10^4$，多测；
- $1\le n\le 2\cdot 10^5$，$p$ 是 $1..n$ 的排列；
- $\sum n\le 2\cdot 10^5$：总规模只有 $2\cdot10^5$，$O(n\log n)$ 可行，$O(n^2)$ 不可行。

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入
4
1
1
5
1 3 5 2 4
6
1 2 4 5 3 6
7
1 3 5 7 2 4 6

输出
1
4
3
0
```

```text
输入（自造，★）
1
7
2 5 4 3 7 6 1

输出
5
```

★ 自造样例：好起点是 $s=1,2,5,6,7$（1-indexed）。它专门覆盖「一次读数里出现两次『跳出去另起一块』」：从 $s=1$ 读出的 $q=[2,5,4,3,7,6,1]$ 先 $2\to\{2,5\}$ 起第二块，$4,3$ 填坑回到 1 块，$7$ 再起第二块，$6$ 填坑，最后 $1$ 接上左端。

## 3. 解题思路

### 3.1 暴力思路

固定 $s$ 后线性模拟：维护「已读」标记与当前块数，读到 $x$ 时

$$\text{块数}\;+\!=\;1-[\text{x-1 已读}]-[\text{x+1 已读}],$$

即 $x$ 自成一块，左右各有邻居就各合并一次。每个 $s$ 扫 $n$ 步，总 $O(n^2)$；$n=2\cdot10^5$ 时约 $4\times10^{10}$ 次操作，必然超时。难点在于块数**会升会降**（先孤立插入、后填坑合并），没有单调性可以二分或双指针直接砍掉。

### 3.2 核心观察：块数就是「块首」的个数

![块数 = 块首的个数](images/cf2249_c_block_starts.svg)

把「一个块的最小值」叫**块首**。设 $S\subseteq[1,n]$，则

$$\text{块数}(S)=\#\{\,v\in S:\ v=1\ \text{或}\ v-1\notin S\,\}.$$

于是不必真的数块，只要数「哪些 $v$ 已被读到、而 $v-1$ 还没读到」。

**位置化**：固定 $s$，设当前读到的最远位置为 $p$，则前缀集合 $S$ 恰是顺时针圆弧 $[s,p]$ 上的值。对 $v\ge 2$：

$$v\in S,\ v-1\notin S\iff pos[v]\in[s,p],\ pos[v-1]\notin[s,p].$$

把「$pos[v]$ 在 $pos[v-1]$ 之前（顺时针）」翻译成起点 $s$ 与终点 $p$ 各自的条件，就得到两组弧：

$$B_v=(pos[v-1],\ pos[v]],\qquad A_v=[pos[v],\ pos[v-1]).$$

![v 是块首 ⟺ s∈B_v 且 p∈A_v，是一个矩形](images/cf2249_c_rect_arcs.svg)

$A_v$ 与 $B_v$ 是同一对端点之间的两段互补弧：都在 $pos[v]$ 处相接（都含 $pos[v]$），都在 $pos[v-1]$ 处断开（都不含它）。于是

> **$v$ 是块首 $\iff s\in B_v$ 且 $p\in A_v$**

也就是 $(s,p)$ 平面上的一个**矩形** $B_v\times A_v$。对固定 $s$，记覆盖数 $C_s(p)=\#\{v\ge2:\ s\in B_v,\ p\in A_v\}$，则块数 $(S_p)=C_s(p)+[\,1\in S_p\,]$。$1$ 没有前驱，读到之后永远是块首，做不成矩形——这条单独处理，也正是本题唯一的坑。

### 3.3 算法流程：扫描起点 + 线段树

![扫描 s：区间加 + 区间最大值](images/cf2249_c_sweep.svg)

1. 环上位置 $0..n-1$，弧一律写成半开区间 $[l,\,l+len)$（模 $n$），其中
   $lenA=(pos[v-1]-pos[v]+n)\bmod n$，$lenB=n-lenA$。
2. 把 $B_v$ 看成 $s$ 轴上的弧：在它的起点把 $A_v$ 整段 $+1$，在终点整段 $-1$（跨 $0$ 的弧拆成两段）。$n-1$ 个 $v$ 共 $2(n-1)$ 个事件，按 $s$ 分桶。
3. $s$ 从 $0$ 扫到 $n-1$：先处理 `ev[s]` 的全部加减，此时线段树的叶子 $p$ 恰好等于 $C_s(p)$，再做两次环形区间最大值查询：
   - $P_1=[s,pos[1])$：$1$ 还没读到，块数 $=C_s(p)$，要求 $\le 2$；
   - $P_2=[pos[1],s)$：$1$ 已读到，块数 $=C_s(p)+1$，要求 $\le 1$。
   两段都通过就 `++ans`。注意 $pos[1]=s$ 时 $P_1$ 为空、$P_2$ 退化成整圈。

### 3.4 示例演算

![p=[1,3,5,2,4] 的逐 s 演算](images/cf2249_c_walkthrough.svg)

取官方样例 $p=[1,3,5,2,4]$（位置 0-indexed），有
$B_2=[1,4),B_3=[4,1),B_4=[2,5),B_5=[0,3)$，对应
$A_2=\{3,4\},A_3=\{1,2\},A_4=\{4,0\},A_5=\{2,3\}$。逐 $s$ 得到覆盖数组：

| $s$ | 激活的 $v$ | $C(p),p=0..4$ | $\max P_1$ | $\max P_2$ | 好? |
|---|---|---|---|---|---|
| 0 | 3,5 | 0 1 2 1 0 | 空 | **2** | 坏 |
| 1 | 2,3,5 | 0 1 2 2 1 | 2 | 0 | 好 |
| 2 | 2,4,5 | 1 0 1 2 2 | 2 | 1 | 好 |
| 3 | 4 | 1 0 0 0 1 | 1 | 1 | 好 |
| 4 | 3,4 | 1 1 1 0 1 | 1 | 1 | 好 |

$s=0$ 处 $pos[1]=0=s$，$P_1$ 为空、$P_2$ 是整圈，要求 $\max C\le1$，但 $C(2)=2$，故坏。答案 $4$，与样例一致。

## 4. 算法细节

1. **下标**：位置统一 0-indexed；环上弧 $[l,l+len)$ 用 $len=(b-a+n)\bmod n$ 计算，$1\le len\le n-1$。
2. **端点开闭**：$A_v$、$B_v$ 都含 $pos[v]$、都不含 $pos[v-1]$。前者保证 $s=pos[v]$ 时 $v$ 在第一步就是块首；后者保证 $s=pos[v-1]$ 时 $v-1$ 先被读，$v$ 永不成为块首。
3. **$v=1$ 单独处理**：它的「块首区间」随 $s$ 变成一段以 $s$ 为端点的弧，不是矩形，只能按「$1$ 是否已读」把 $p$ 轴切成两段、阈值分别用 2 和 1。
4. **事件**：每个 $v$ 一加一减；$B_v$ 跨 $0$ 时拆成 $[b_0,n)$ 与 $[0,e)$，其中 $e=b_0+lenB-n\ge1$。同一 $s$ 的事件全部处理完再查询。
5. **多测清空**：事件桶与线段树按当前 $n$ 重建；$\sum n\le2\cdot10^5$ 保证总代价。
6. **线段树写法**：节点维护「子树最大值 + 本条边自己的 tag」，不做 pushdown，查询时把路径上的 tag 累加返回；数组开 $4n$。
7. **$n=1$**：没有 $v\ge2$，唯一前缀块数为 1，答案恒为 1，直接输出。
8. **数值**：只有加减与比较，计数 $\le n$，`int` 足够，无溢出风险。

## 5. 正确性证明

**引理 1（块首计数）**：对任意 $S\subseteq[1,n]$，块数等于 $\#\{v\in S:\ v=1\ \text{或}\ v-1\notin S\}$。

**证明**：每个块是连续整数区间，其最小元 $v$ 满足 $v-1\notin S$（$v=1$ 时无条件成立）；反之若 $v\in S$ 且 $v-1\notin S$，则 $v$ 必为所在块的最小元。块与「块首」一一对应。∎

**引理 2（矩形判定）**：固定 $s$，$p$ 为当前读到的最远位置（前缀即圆弧 $[s,p]$），对 $v\ge2$：$v\in S,\ v-1\notin S\iff s\in B_v,\ p\in A_v$。

**证明**：($\Rightarrow$) $pos[v]\in[s,p]$、$pos[v-1]\notin[s,p]$，故顺时针顺序为 $s\to pos[v]\to p\to pos[v-1]$（允许 $pos[v]=s$ 或 $pos[v]=p$）。按定义 $A_v$ 从 $pos[v]$ 顺时针走到 $pos[v-1]$（不含终点），包含 $p$；$B_v$ 从 $pos[v-1]$ 顺时针走到 $pos[v]$（不含起点），包含 $s$。($\Leftarrow$) 若 $s\in B_v$ 且 $p\in A_v$，则从 $pos[v]$ 顺时针先遇到 $p$、再遇到 $pos[v-1]$，而 $s$ 落在 $pos[v-1]$ 之后（含 $pos[v]$），故 $[s,p]$ 含 $pos[v]$ 而不含 $pos[v-1]$。∎

**引理 3（不变量）**：处理完 `ev[s]` 后，线段树叶子 $p$ 的值等于 $C_s(p)=\#\{v\ge2:\ s\in B_v,\ p\in A_v\}$。

**证明**：对 $s$ 归纳。$s=0$ 时，所有含 $0$ 的 $B_v$（自身含 $0$ 或跨 $0$ 的尾段）都在 `ev[0]` 中被加入，其余不含 $0$ 的 $B_v$ 不在，与 $C_0$ 一致。$s\to s+1$ 时，只有起止点为 $s$ 的 $B_v$ 状态改变，事件恰好在 `ev[s]` 中把对应 $A_v$ 上加减 $\pm1$，其余弧不变。∎

**引理 4（阈值等价）**：全部前缀块数 $\le2$ $\iff$ $\max_{p\in P_1}C_s(p)\le2$ 且 $\max_{p\in P_2}C_s(p)\le1$（$pos[1]=s$ 时 $P_1=\varnothing$、$P_2$ 为整圈）。

**证明**：由引理 1、2，块数 $(S_p)=C_s(p)+[\,1\in S_p\,]$，而 $1\in S_p\iff pos[1]\in[s,p]$。若 $pos[1]\ne s$，则 $p\in[s,pos[1])$ 时 $1\notin S_p$、$p\in[pos[1],s)$ 时 $1\in S_p$，两段恰好剖分所有 $p$；若 $pos[1]=s$，$1$ 在第一步即被读到，所有 $p$ 都有 $1\in S_p$，此时 $P_1$ 为空、$P_2$ 取整圈。两种情形都恰好覆盖全部 $p$，阈值对应块数上界 2。∎

**定理**：算法输出的 `ans` 等于好起点的个数。

**证明**：由引理 3，每次查询看到的就是真实的 $C_s(p)$；由引理 4，两次查询通过 $\iff$ 该 $s$ 的所有前缀块数 $\le2$ $\iff s$ 是好的。算法对每个 $s$ 恰好计数一次，故 `ans` 正确。∎

## 6. 复杂度分析

- **时间**：单组 $O(n\log n)$——求弧 $O(n)$，事件 $2(n-1)$ 次环形区间加（各 $O(\log n)$），$s$ 的每次迭代 2 次环形区间最大值查询（各 $O(\log n)$）。全局 $O(\sum n\log n)$，$\sum n\le2\cdot10^5$ 时约 $3.6\times10^6$ 次线段树基本操作。
- **空间**：事件表 $O(n)$、线段树 $4n$ 个 `int`、$pos$ 数组，合计 $O(n)$，$n=2\cdot10^5$ 时约 8 MB。
- **实测**（Apple clang 21，`-O2`，时限 2 s，文中 C++ 代码原样编译）：$n=2\cdot10^5$ 随机排列 0.46 s；$n=2\cdot10^5$ 升序（答案 $n$，查询量最大）0.33 s；$t=10^4$、$\sum n=2\cdot10^5$ 0.19 s。余量 $\ge3$ 倍。
- **Python**：同算法 CPython3 实测 $n=2\cdot10^5$ 升序 18.8 s、$t=10^4$ 小数据 4.6 s，属于**预期超时**（纯 Python 线段树常数太大）；PyPy3 预计 3–5 s 仍偏紧。文中 Python 版主要用于对拍与思路对照。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SegTree {                       // 区间加 + 区间最大值
    int n; vector<int> mx, tag;
    void init(int n_) { n = n_; mx.assign(4 * n + 4, 0); tag.assign(4 * n + 4, 0); }
    void add(int o, int l, int r, int ql, int qr, int v) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { mx[o] += v; tag[o] += v; return; }
        int m = (l + r) >> 1;
        add(o << 1, l, m, ql, qr, v); add(o << 1 | 1, m, r, ql, qr, v);
        mx[o] = max(mx[o << 1], mx[o << 1 | 1]) + tag[o];
    }
    int qry(int o, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return INT_MIN;
        if (ql <= l && r <= qr) return mx[o];
        int m = (l + r) >> 1;
        int res = max(qry(o << 1, l, m, ql, qr), qry(o << 1 | 1, m, r, ql, qr));
        return res == INT_MIN ? INT_MIN : res + tag[o];
    }
    void addCir(int l, int len, int v) {          // 环形区间 [l, l+len)
        if (l + len <= n) add(1, 0, n, l, l + len, v);
        else { add(1, 0, n, l, n, v); add(1, 0, n, 0, l + len - n, v); }
    }
    int maxCir(int l, int len) {                  // len ∈ [1,n]
        if (len >= n) return qry(1, 0, n, 0, n);
        if (l + len <= n) return qry(1, 0, n, l, l + len);
        return max(qry(1, 0, n, l, n), qry(1, 0, n, 0, l + len - n));
    }
} seg;

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; cin >> T;
    while (T--) {
        int n; cin >> n;
        vector<int> pos(n + 1);
        for (int i = 0; i < n; i++) { int x; cin >> x; pos[x] = i; }
        if (n == 1) { cout << 1 << '\n'; continue; }
        vector<vector<array<int, 3>>> ev(n);      // ev[s]: {a0, lenA, ±1}
        auto pushEv = [&](int s, int a0, int len, int d) {
            if (s >= 0 && s < n) ev[s].push_back({a0, len, d});
        };
        for (int v = 2; v <= n; v++) {
            int pv = pos[v], pm = pos[v - 1];
            int a0 = pv, lenA = (pm - pv + n) % n;          // A_v = [pos[v], pos[v-1])
            int b0 = (pm + 1) % n, lenB = (pv - pm + n) % n; // B_v = (pos[v-1], pos[v]]
            if (b0 + lenB <= n) {                            // B_v 不跨 0
                pushEv(b0, a0, lenA, +1); pushEv(b0 + lenB, a0, lenA, -1);
            } else {                                         // B_v 跨 0，拆两段
                pushEv(b0, a0, lenA, +1); pushEv(b0 + lenB - n, a0, lenA, -1);
                pushEv(0, a0, lenA, +1);
            }
        }
        seg.init(n);
        int ans = 0, p1 = pos[1];
        for (int s = 0; s < n; s++) {
            for (auto &e : ev[s]) seg.addCir(e[0], e[1], e[2]);
            bool ok = true;
            int l1 = (p1 - s + n) % n;                       // P1 = [s, pos[1])
            if (l1 && seg.maxCir(s, l1) > 2) ok = false;
            int l2 = (s - p1 + n) % n;                       // P2 = [pos[1], s)
            if (seg.maxCir(p1, l2 ? l2 : n) > 1) ok = false;
            if (ok) ans++;
        }
        cout << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t, idx, out = data[0], 1, []
    NEG = -(1 << 30)
    for _ in range(t):
        n = data[idx]; idx += 1
        p = data[idx:idx + n]; idx += n
        if n == 1:
            out.append('1'); continue
        pos = [0] * (n + 1)
        for i, v in enumerate(p):
            pos[v] = i
        log = (n - 1).bit_length(); size = 1 << log
        d = [0] * (2 * size); lz = [0] * size          # 区间加 + 区间最大值

        def all_apply(k, f):
            d[k] += f
            if k < size: lz[k] += f

        def push(k):
            z = lz[k]
            if z:
                all_apply(2 * k, z); all_apply(2 * k + 1, z); lz[k] = 0

        def update(k):
            d[k] = (d[2 * k] if d[2 * k] > d[2 * k + 1] else d[2 * k + 1]) + lz[k]

        def apply_range(l, r, f):
            if l >= r: return
            l += size; r += size
            for i in range(log, 0, -1):
                if ((l >> i) << i) != l: push(l >> i)
                if ((r >> i) << i) != r: push((r - 1) >> i)
            l2, r2 = l, r
            while l < r:
                if l & 1: all_apply(l, f); l += 1
                if r & 1: r -= 1; all_apply(r, f)
                l >>= 1; r >>= 1
            l, r = l2, r2
            for i in range(1, log + 1):
                if ((l >> i) << i) != l: update(l >> i)
                if ((r >> i) << i) != r: update((r - 1) >> i)

        def prod(l, r):
            if l >= r: return NEG
            l += size; r += size
            for i in range(log, 0, -1):
                if ((l >> i) << i) != l: push(l >> i)
                if ((r >> i) << i) != r: push((r - 1) >> i)
            a = b = NEG
            while l < r:
                if l & 1: a = a if a > d[l] else d[l]; l += 1
                if r & 1: r -= 1; b = b if b > d[r] else d[r]
                l >>= 1; r >>= 1
            return a if a > b else b

        def add_circ(l, ln, f):
            if ln >= n: apply_range(0, n, f)
            elif l + ln <= n: apply_range(l, l + ln, f)
            else: apply_range(l, n, f); apply_range(0, l + ln - n, f)

        def max_circ(l, ln):
            if ln >= n: return prod(0, n)
            if l + ln <= n: return prod(l, l + ln)
            a, b = prod(l, n), prod(0, l + ln - n)
            return a if a > b else b

        ev = [[] for _ in range(n)]                    # 每个 v：B_v 的进出事件
        for v in range(2, n + 1):
            pv, pm = pos[v], pos[v - 1]
            a0, lenA = pv, (pm - pv) % n
            b0, lenB = (pm + 1) % n, (pv - pm) % n
            if b0 + lenB <= n:
                ev[b0].append((a0, lenA, 1))
                if b0 + lenB < n: ev[b0 + lenB].append((a0, lenA, -1))
            else:
                ev[b0].append((a0, lenA, 1)); ev[0].append((a0, lenA, 1))
                e = b0 + lenB - n
                if e < n: ev[e].append((a0, lenA, -1))
        ans, p1 = 0, pos[1]
        for s in range(n):
            for a0, lenA, f in ev[s]:
                add_circ(a0, lenA, f)
            ok = True
            l1 = (p1 - s) % n
            if l1 and max_circ(s, l1) > 2: ok = False
            l2 = (s - p1) % n
            if max_circ(p1, l2 if l2 else n) > 1: ok = False
            if ok: ans += 1
        out.append(str(ans))
    sys.stdout.write('\n'.join(out) + '\n')

main()
```

## 8. 边界情况与易错点

1. **$n=1$**：没有 $v\ge2$，唯一前缀块数为 1，答案 1；不特判时 `pos[1]=s=0` 会走「整圈阈值 1」的分支，也恰好能过，但 `n=1` 时线段树大小为 1，容易写崩。
2. **$pos[1]=s$**：$P_1$ 为空、$P_2$ 必须是**整圈**。若按「长度为 0 就当作空段跳过」，会把这类 $s$ 全部误判为好（官方样例 2 的 $s=1$，即 0-indexed 的 $s=0$，正是如此）。
3. **弧的端点开闭**：$A_v$ 若写成 $[pos[v],pos[v-1]]$，$p=pos[v-1]$ 时会多算一次块首；$B_v$ 若写成 $[pos[v-1],pos[v]]$，$s=pos[v-1]$ 时会把 $v$ 误判为块首（实际上 $v-1$ 先被读）。
4. **环形弧漏拆段**：$B_v$ 跨过 $0$ 时必须拆成 $[b_0,n)$ 与 $[0,e)$ 两段，否则 $s$ 靠前的那一段整体丢失，答案偏大。
5. **阈值记反**：$1$ 已读时块数 $=C+1$，只能容忍 $C\le1$；写成 $\le2$ 会把坏起点判成好。
6. **事件顺序**：同一 $s$ 的所有 $+1/-1$ 必须先全部生效再查询，否则会查到「只加了一半」的中间状态。
7. **多测未清空**：事件桶与线段树要按 $n$ 重建；直接复用上一轮的 `tag` 会污染本组。
8. **下标混用**：位置全用 0-indexed，弧长用 $(b-a+n)\bmod n$；凡是拿 1-indexed 位置直接算弧长，都会整体错一位。

## 相关题目与扩展

- [Codeforces 377D Developing Game](https://codeforces.com/problemset/problem/377/D)：矩形 / 区间覆盖的**最大深度**，扫描线 + 线段树，与本题「对每个 $s$ 求 $\max_p$ 覆盖数」完全同构。
- [Codeforces 1555E Boring Segments](https://codeforces.com/problemset/problem/1555/E)：线段树维护覆盖 + 双指针，可对照「事件进出」的写法。
- [Codeforces 526F Pudding Monsters](https://codeforces.com/problemset/problem/526/F)：统计「值集合恰为一段连续整数」的子数组个数，用单调栈 + 线段树维护块首，可看作本题的「单块版本」。
- [LeetCode 732. 我的日程安排表 III](https://leetcode.cn/problems/my-calendar-iii/)：区间加 + 全局最大值，本题线段树的原型。
- [LeetCode 1109. 航班预订统计](https://leetcode.cn/problems/corporate-flight-bookings/)：区间加的最小实现（差分），本题环形区间的退化版。

**延伸思考**：

- **换成 $\le k$ 块**：矩形结构不变，只把「$1$ 已读」那段的阈值改成 $k-1$、未读段改成 $k$，复杂度不变。这说明「块数」这类量一旦写成「前驱是否出现」的计数，就能被 $(s,p)$ 矩形覆盖统一处理。
- **求每个 $s$ 的最长好前缀**：把两次「区间最大值是否超阈值」换成在线段树上沿树下降、找区间内第一个超阈值的位置（$O(\log n)$），总复杂度仍是 $O(n\log n)$。
- **线性版本**（只在数组上从 $i$ 往右读）：删掉环形拆段即可，事件变成普通的前缀事件。
- **反向思考**：一旦把「$S$ 的块数」翻译成「$v-1\notin S$ 的 $v$ 的个数」，问题就从「动态集合」变成了「静态矩形覆盖」，这是处理这类「连续段」问题的通用套路。
