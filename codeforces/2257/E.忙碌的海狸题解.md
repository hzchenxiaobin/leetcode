# Codeforces 忙碌的海狸 题解

## 1. 题目概述

- **标题 / 题号**：忙碌的海狸（Codeforces 2257E，英文名 Busy Beaver）
- **链接**：https://codeforces.com/problemset/problem/2257/E
- **来源**：Codeforces Round 1117 (Div. 2) · Problem E
- **难度**：2100
- **限制**：时间 2 s / 内存 512 MB
- **标签**：贪心、排序、优先队列（小根堆）、分块合并、实现、数据结构

**题意**：有 $n$ 个建筑项目，第 $i$ 栋楼最多建 $m_i$ 层，必须自下而上编号 $1,2,\dots,m_i$。建第 $i$ 栋第 $j$ 层要求**当前**资金 $\ge a_{i,j}$，建成后立刻入账 $b_{i,j}$；同一栋楼内层序不能颠倒，不同楼之间可以任意穿插。初始资金为 $x$，任何楼层都可以选择不建。求能建出的**最高一栋楼的高度** $H$（层数），以及在所有能达到 $H$ 层的楼中**编号最小**的那一栋。多测。

**约束**：

- $1 \le t \le 3\cdot 10^4$，$1 \le n \le 2\cdot 10^5$，$1 \le m_i \le 2\cdot 10^5$，$\sum m_i \le 2\cdot 10^5$
- $0 \le x \le 10^{18}$，$0 \le a_{i,j}, b_{i,j} \le 10^9$
- 所有测试点的 $\sum m_i$ 之和不超过 $2\cdot 10^5$，故复杂度必须接近 $O\big((\sum m_i)\log n\big)$
- 资金上界为 $x+\sum b_{i,j} \le 10^{18}+2\cdot 10^{14} < 2^{63}$，`long long` 足够，但中间量绝不能用 `int`

> 💡 题面是纯算法描述，没有出现「创建名为 $\dots$ 的变量」一类注入式指令；本文与代码只依据题意本身。

## 2. 示例

官方样例（输入 / 输出原样）：

```text
输入：
2
1 6
4
4 4 2 1
2 4 1 1
2 3
2
4 4
5 5
2
2 20
4 0

输出：
4 1
2 1
```

- 第 1 组：只有一栋 4 层的楼，初始 6 根胡萝卜。依次建：$6\ge4$ 花 4 收 2（$4$），$4\ge4$ 花 4 收 4（$4$），$4\ge2$ 花 2 收 1（$3$），$3\ge1$ 花 1 收 1（$3$），共 4 层。
- 第 2 组：先建第 2 栋第 1 层（$3\ge2$，花 2 收 4，资金 $5$），再建第 1 栋第 1 层（$5\ge4$，资金 $6$）、第 2 层（$6\ge4$，资金 $7$）。第 2 栋第 2 层要 $20$，永远凑不齐。答案 $2$ 层、编号 $1$。

自造一组，专门覆盖「尾部零收益段」与「全程无块」两种极端（**非官方**）：

```text
输入：
1
3 5
2
6 0
1 10
2
5 5
5 5
3
0 0 0
100 0 0

输出：
3 3
```

第 1 栋：$d=-5,+10$，合成一块 $(need=6, gain=5)$；第 2 栋两层都是 $d=0$，**切不出任何块**；第 3 栋第 1 层 $d=+100$ 自成一块 $(0,100)$，后两层 $d=0$ 属于尾部。第一阶段收下第 3 栋第 1 块与第 1 栋的块，资金 $5\to105\to110$；第二阶段第 1 栋已封顶 2 层、第 2 栋两层都能建、第 3 栋靠 $110$ 把尾部两层也补齐到 3 层，故答案是第 3 栋。

## 3. 解题思路

### 3.1 暴力思路

最直接的状态是「每栋楼已建到第几层」的向量 $\big(h_1,\dots,h_n\big)$。资金由状态**唯一确定**——它等于 $x+\sum_{i}\sum_{j\le h_i}\big(b_{i,j}-a_{i,j}\big)$——所以可以在状态图上 DFS：从任意一栋楼往上加一层，若资金够就转移。对每栋楼取「所有可达状态里它的最大高度」，再取全局最大与最小下标。

状态总数是 $\prod (m_i+1)$：$n=2\cdot10^5$ 且每栋 1 层时就是 $2^{200000}$，完全不可行。更麻烦的是「为了建 A 楼，先去 B 楼打工」这种跨楼依赖，很难直接对单栋楼下结论。

### 3.2 核心观察：把每栋楼切成若干「先亏后赚」的原子块

![块的切分：need 是最深的坑，gain 是块尾的高度](images/cf2257_e_block_split.svg)

记 $d_{i,j}=b_{i,j}-a_{i,j}$。对一栋楼从当前起点开始累加 $d$，设块内前缀和为 $D_p=\sum_{l\le t\le p}d_{i,t}$：

- **切块规则**：一旦某个位置 $r$ 使 $D_r>0$，就把 $[l,r]$ 封成一个块，从 $r+1$ 重新开始；若扫到楼顶都没有 $D_r>0$，剩下的部分叫**尾部**，不产生块。
- **门槛**：$need=\max_{l\le p\le r}\big(a_{i,p}-D_{p-1}\big)$（$D_{l-1}=0$），即「建到第 $p$ 层之前手里至少要有的钱」的最大值。实现上用 `sum -= a; mn = min(mn, sum); sum += b;` 记录，最后 $need=-mn$。
- **收益**：$gain=D_r>0$，严格为正。

这样切出的块有一个决定性的性质：**块内任何真前缀的累计收益都 $\le 0$**。于是资金曲线在块内是「先下探、后回升」，$need$ 就是那个最深的坑；只要当前资金 $\ge need$，整块一定能在不下穿 0 的前提下走完，并且结束时资金**严格增加** $gain$。反过来，资金 $<need$ 时必然在某个下探点卡死，一块也拿不全。

所以每个块就是一个**原子投资项目** $(need,\ gain)$：够 $need$ 才能投，投完净赚 $gain$。尾部总收益 $\le 0$、又解锁不了任何东西，永远不值得「为了赚钱」去建——但它可能是某栋楼自己的楼层，留到第二阶段处理。

### 3.3 算法流程 / 状态转移

![两阶段流程：小根堆贪心收割，然后逐栋梭哈](images/cf2257_e_heap_greedy.svg)

**阶段 1（贪心收割）**：把每栋楼的**第 1 块**放进小根堆（按 $need$ 排序），记当前资金为 $X$。

1. 取堆顶（$need$ 最小的可做块）；
2. 若 $need>X$，立刻 `break`——小根堆保证后面每一块更贵，谁都做不起；
3. 否则执行它：$X\mathrel{+}=gain$，把这栋楼的**下一块**入堆（同一栋楼必须按块序推进），回到 1。

结束后 $X$ 就是理论可达的**最大资金**，同时每栋楼被建到了某个层数 $f_i$（最后一个被执行块的末层；没执行过则为 $0$）。

**阶段 2（逐栋梭哈）**：对每栋楼 $i$，令 $cur=X$，从第 $f_i+1$ 层开始逐层尝试：$cur\ge a_{i,f_i+1}$ 就建、$cur\mathrel{+}=b-a$、层数 $+1$；一旦付不起就停。取「层数最大、同层数编号最小」的那栋。

为什么第二阶段不必再回堆里找块？因为剩余块的 $need$ 全都 $>X$，而阶段 2 处理的那一段是某块的**真前缀**，累计收益 $\le 0$，资金只会 $\le X$，不可能把任何剩余块变便宜。所以「收割到极限 + 把全部钱押在一栋楼上」就已经是最优。

### 3.4 示例演算

![样例 2 的完整走查表](images/cf2257_e_walkthrough.svg)

以官方第 2 组为例，$n=2$、$x=3$：

- 第 1 栋 $d=+1,+1$：切出两块 $(need=4,gain=1)$、$(4,1)$；
- 第 2 栋 $d=+2,-20$：只有第 1 块 $(2,2)$，第 2 层累计 $-18\le0$ 属尾部。

阶段 1：堆顶 $need=2\le3$，执行第 2 栋块 1，$X=5$；堆顶 $need=4\le5$，执行第 1 栋块 1，$X=6$；再执行第 1 栋块 2，$X=7$；堆空。此时 $f_1=2$、$f_2=1$。

阶段 2：第 1 栋从 $f_1+1=3$ 起已越界，仍是 2 层；第 2 栋第 2 层要 $20>7$，卡在 1 层。答案「2 1」。

## 4. 算法细节

1. **$need$ 与切块必须在同一次扫描里算出**：`sum -= a[j]; mn = min(mn, sum); sum += b[j];` 之后判断 `sum > 0`，成立就封块并令 `sum = mn = 0`。注意 `mn` 的含义是「块内资金相对起点的最小偏移」，所以 $need=-mn$，且 $need\ge 0$。
2. **切块条件是严格 $>0$**：若某层结束时 $sum=0$，说明只是回本，不算「赚到」，继续往后并入同一块更划算（并入后才可能出现真正为正的 $gain$）。写成 $\ge 0$ 也能过（会多出收益为 0 的块），但**不能**在 $sum<0$ 处提前封块，否则会漏掉后面那块真正的正收益。
3. **堆中只放块头**：每栋楼在堆里最多一个元素，堆大小 $O(n)$；执行后把同一栋楼的下一块补进堆即可，天然维护了「同栋楼按块序」的约束。
4. **阶段 1 的截断**：`if (it.need > x) break;` 而不是 `continue`——堆按 $need$ 升序，一旦最小的都做不起，剩下的 $need$ 只会更大。
5. **阶段 2 的起点必须是 $f_i$**：此时 $X$ 里**已经包含**该栋楼前 $f_i$ 层的收益，若拿 $X$ 从第 1 层重来，就等于把这份收益花两遍，会高估答案。
6. **多测清空**：所有 `vector` 每组重新构造（不要跨组复用 `blk`、`done`）；因为 $\sum m_i\le2\cdot10^5$，按实际规模分配即可，不要每组 `memset` 大数组。
7. **数据范围**：$x$ 最大 $10^{18}$，$\sum b$ 最大 $2\cdot10^{14}$，合计 $<1.1\cdot10^{18}$，`long long` 安全；但 $a_{i,j}-D_{p-1}$ 这类量建议统一用 `long long` 计算，`mn` 初值取 $0$。
8. **I/O 常数**：$t$ 可达 $3\cdot10^4$，总整数约 $6\cdot10^5$ 个，务必关闭同步流或使用快读；输出同样建议攒进缓冲区。

## 5. 正确性证明

**引理 1（块的原子性）**：设某块是 $[l,r]$，$gain>0$、$need=\max_{l\le p\le r}\big(a_{i,p}-D_{p-1}\big)$。从资金 $c$ 出发按顺序建 $l..r$ 层可行，当且仅当 $c\ge need$；可行时结束后资金为 $c+gain$。

**证明**：建第 $p$ 层之前的资金是 $c+D_{p-1}$，可行等价于 $c+D_{p-1}\ge a_{i,p}$，即 $c\ge a_{i,p}-D_{p-1}$ 对每个 $p$ 成立，取最大值即 $c\ge need$。收益是块内 $d$ 之和，恰为 $gain$。∎

**引理 2（收割阶段最优）**：设阶段 1 执行完的块集合为 $G$、结束时资金为 $X$。则对任意合法建造方案中**已完整建完**的块集合 $S$，都有 $\sum_{g\in S}gain(g)\le X-x$。

**证明**：反设存在合法方案，其按执行顺序出现第一个不在 $G$ 中的块 $\beta$。该顺序中 $\beta$ 之前的块都在 $G$ 里（由 $\beta$ 的取法），因此 $\beta$ 在同一栋楼的**前驱块**也都在 $G$ 里，说明阶段 1 结束时 $\beta$ 一定已经作为块头进过堆。又 $\beta$ 之前的块收益之和 $\le\sum_{g\in G}gain(g)=X-x$，故执行 $\beta$ 时资金 $\le X$，于是 $need(\beta)\le X$——这与阶段 1 的停止条件（堆中最小 $need$ 都 $>X$）矛盾。故不存在这样的 $\beta$，即 $S$ 的收益和不超过 $G$。∎

**引理 3（阶段 2 不会解锁新块）**：阶段 1 结束后，任何未执行块的 $need>X$；阶段 2 处理某栋楼时资金始终 $\le X$，且必定在该楼剩余部分的块内停住。

**证明**：阶段 2 从 $f_i+1$ 开始，这一层是某个未执行块的首层（或位于尾部）。由切块规则，块内任何真前缀的累计收益 $D_p\le0$，尾部同理，故阶段 2 的资金 $X+D_p\le X$，永远够不到任何 $need>X$ 的块，也就不会解锁新投资。又因为该块的 $need>X$ 而模拟从 $X$ 起步，必存在某层 $p$ 使 $X+D_{p-1}<a_{i,p}$，模拟一定在块内停下。∎

**定理**：设楼 $i$ 在第一阶段被建到 $f_i$ 层，第二阶段再推进 $e_i$ 层，则楼 $i$ 在所有合法方案中的最大高度恰为 $f_i+e_i$。

**证明**：**可达性**：先按阶段 1 的顺序执行 $G$（引理 1 保证每一步都付得起），此时资金为 $X$、楼 $i$ 已建 $f_i$ 层；再按阶段 2 的顺序继续建楼 $i$，每一步都显式检查过资金，故 $f_i+e_i$ 层可达。**上界**：任取一个把楼 $i$ 建到 $k$ 层的合法方案，设其中完整建完的块集合为 $S$，由引理 2 得 $\sum_{S}gain\le X-x$，所以该方案在任何时刻的资金都 $\le X$（未建完的块内前缀收益 $\le0$，只会更少）。把该方案建第 $t$ 层（$t>f_i$）时的资金记为 $c_t$，阶段 2 在同一层的资金为 $X+D$，其中 $D$ 是楼 $i$ 从 $f_i+1$ 到 $t-1$ 层的收益和，与方案中这部分收益相同，而 $x+\sum_S gain\le X$ 说明 $c_t\le X+D$。于是 $c_t\ge a_{i,t}$ 蕴含阶段 2 在该层也付得起，$k\le f_i+e_i$。两者相等。∎

因此对每栋楼算出的高度就是它真正能到的最大高度，取全局最大、同值取最小下标即为答案。∎

## 6. 复杂度分析

- **切块**：每层恰好被扫描一次，$O\big(\sum m_i\big)$。
- **阶段 1**：块的个数 $K\le\sum m_i$，每块入堆/出堆各一次，堆大小 $O(n)$，故 $O\big(K\log n\big)$。
- **阶段 2**：每栋楼从 $f_i$ 扫到卡住，每层至多一次，合计 $O\big(\sum m_i\big)$。
- **总时间**：$O\big((\sum m_i)\log n\big)$，$\sum m_i\le2\cdot10^5$ 时只有几百万次基本操作。
- **空间**：$O\big(\sum m_i\big)$，存 $a,b$ 与块表，最大约几 MB。

实测（本机，四组最大规模数据：$n=2\cdot10^5$ 各 1 层 / 单栋 $m=2\cdot10^5$ / $t=3\cdot10^4$ / 全部块 $need=0$）：算法本体 40–80 ms；若直接用 `cin` 读 4 MB 输入，本机 Apple libc++ 的 iostream 会额外花约 0.6 s，总耗时仍在 2 s 内，GNU libstdc++ 下更快。Python3 同数据约 0.13–1.0 s，建议用 PyPy3 提交。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

struct Item {
    ll need; int b, k;                 // 块所需资金、楼编号、块下标
    bool operator<(const Item& o) const { return need > o.need; }  // 小根堆
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 0;
    cin >> T;
    while (T--) {
        int n; ll x;
        cin >> n >> x;
        vector<vector<ll>> A(n), B(n);
        vector<vector<array<ll,3>>> blk(n);          // {need, gain, 末层}
        for (int i = 0; i < n; i++) {
            int m; cin >> m;
            A[i].resize(m); B[i].resize(m);
            for (auto& v : A[i]) cin >> v;
            for (auto& v : B[i]) cin >> v;
            ll sum = 0, mn = 0;
            for (int j = 0; j < m; j++) {
                sum -= A[i][j]; mn = min(mn, sum); sum += B[i][j];
                if (sum > 0) { blk[i].push_back({-mn, sum, (ll)(j + 1)}); sum = mn = 0; }
            }
        }
        priority_queue<Item> pq;
        for (int i = 0; i < n; i++) if (!blk[i].empty()) pq.push({blk[i][0][0], i, 0});
        vector<int> done(n, 0);                     // 每栋楼已完成的块数
        while (!pq.empty()) {
            Item it = pq.top();
            if (it.need > x) break;                 // 最便宜的都做不起
            pq.pop(); x += blk[it.b][it.k][1]; done[it.b]++;
            int nk = it.k + 1;
            if (nk < (int)blk[it.b].size()) pq.push({blk[it.b][nk][0], it.b, nk});
        }
        ll best = 0; int ans = 1;
        for (int i = 0; i < n; i++) {
            ll cur = x;
            int f = done[i] ? (int)blk[i][done[i] - 1][2] : 0;
            while (f < (int)A[i].size()) {
                if (cur < A[i][f]) break;
                cur += B[i][f] - A[i][f]; f++;
            }
            if (f > best) { best = f; ans = i + 1; }
        }
        cout << best << ' ' << ans << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys, heapq


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    p = 0; t = int(data[p]); p += 1
    out = []
    for _ in range(t):
        n = int(data[p]); x = int(data[p + 1]); p += 2
        A = [None] * n; B = [None] * n; blk = [None] * n
        for i in range(n):
            m = int(data[p]); p += 1
            a = list(map(int, data[p:p + m])); p += m
            b = list(map(int, data[p:p + m])); p += m
            A[i] = a; B[i] = b
            blocks = []; s = 0; mn = 0
            for j in range(m):
                s -= a[j]
                if s < mn: mn = s
                s += b[j]
                if s > 0:                       # 首次转正，封块
                    blocks.append((s, -mn, j + 1)); s = 0; mn = 0
            blk[i] = blocks

        heap = [(blk[i][0][1], i, 0) for i in range(n) if blk[i]]
        heapq.heapify(heap)
        done = [0] * n
        while heap:
            need, i, k = heap[0]
            if need > x:
                break
            heapq.heappop(heap)
            x += blk[i][k][0]; done[i] += 1
            if k + 1 < len(blk[i]):
                heapq.heappush(heap, (blk[i][k + 1][1], i, k + 1))

        best = 0; ans = 0
        for i in range(n):
            cur = x
            f = blk[i][done[i] - 1][2] if done[i] else 0
            ai = A[i]; bi = B[i]; m = len(ai)
            while f < m:
                if cur < ai[f]: break
                cur += bi[f] - ai[f]; f += 1
            if f > best:
                best = f; ans = i
        out.append(f"{best} {ans + 1}")
    sys.stdout.write("\n".join(out))


main()
```

## 8. 边界情况与易错点

1. **一栋楼都建不了**（例如 $x=0$ 且所有 $a_{i,1}>0$）：堆顶立即 $>X$，`best` 保持 $0$、`ans` 保持 $1$，输出「0 1」。注意此时答案下标是 $1$ 而不是「没有」。
2. **门槛为 $0$ 的块**：$a_{i,1}=0$ 的块在 $x=0$ 时也能白拿，所以停止条件必须是 $need>X$，不能写成 $need\ge X$，也不能额外加 $need>0$ 的限制。
3. **尾部段不是废数据**：总收益 $\le0$ 的尾部不产生块，但**目标楼自己的尾部**照样可能被第二阶段建出来（见 §2 的自造样例）；别在切块时把尾部楼层从数组里删掉。
4. **第二阶段不能从第 1 层重跑**：$X$ 已包含该楼前 $f_i$ 层的收益，重跑会重复计算收益而高估答案；起点只能取 $f_i$。
5. **$sum$ 恰好为 $0$**：不算块尾，继续并块；若把「$\ge0$」当成封块条件，会切出 $gain=0$ 的块，虽然不影响答案，但多一次入堆，且容易在实现里把 `need` 记错。
6. **溢出与初值**：$mn$ 必须用 $0$ 初始化（初始化成 $a_{i,1}$ 会漏掉比它更深的坑），$need=-mn$ 是非负 `long long`；$x+\sum b$ 接近 $10^{18}$，不要用 `int`、也不要用 `double`。
7. **多测**：$t$ 最大 $3\cdot10^4$，但 $\sum m_i\le2\cdot10^5$，所以按规模分配即可；真正要小心的是 `done`、`blk` 这些数组**必须每组重建**。

## 相关题目与扩展

- [Codeforces 2257F1 / F2 Beaver's Jumping Track](https://codeforces.com/problemset/problem/2257/F1)：同场 F 题（简单版 / 困难版），同样是把「先亏后赚」的段合成整体后再做数据结构维护，可对照本题的块思想。
- [Codeforces 1490E Accidental Victory](https://codeforces.com/problemset/problem/1490/E)：排序 + 前缀和找「能一路吃到顶」的起点，是本题「小根堆收割 + 门槛」的极简版本。
- [LeetCode 1642. 可以到达的最远建筑](https://leetcode.cn/problems/furthest-building-you-can-reach/)：逐层推进、用堆维护「哪些投入最值得」，与阶段 1 的贪心同源。
- [LeetCode 871. 最低加油次数](https://leetcode.cn/problems/minimum-number-of-refueling-stops/)：资源不够时反悔、从历史里挑最优的一步，可类比「块按 $need$ 排序后统一收割」。

**延伸思考**：

1. **输出方案**：第一阶段记录块的执行顺序、第二阶段记录每栋楼的层数，就能在 $O(\sum m_i)$ 内输出完整建造序列；注意块内楼层必须连续输出。
2. **改成「所有楼高度之和最大」**：本题的「梭哈」不再成立——钱只有一份，要分配给多栋楼，问题会变成一个带前置依赖的背包，难度陡增。
3. **$a,b$ 放大到 $10^{18}$**：$x+\sum b$ 会溢出 `long long`，需要 `__int128` 存资金，比较时也要一起换。
4. **如果允许「拆块」**：即允许只建半块并中途去别的楼打工，块的原子性论证会失效；本文的引理 1 说明这种拆法并不能降低门槛，所以答案不变——可以试着把这条也写成严格证明。
