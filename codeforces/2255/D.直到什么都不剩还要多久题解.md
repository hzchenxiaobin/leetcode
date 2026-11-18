# Codeforces 直到什么都不剩还要多久 题解

## 1. 题目概述

- **标题 / 题号**：直到什么都不剩还要多久（Codeforces 2255D，英文名 How Long Until Nothing Remains?）
- **链接**：https://codeforces.com/problemset/problem/2255/D
- **来源**：Codeforces Round 1116 (Div. 1) · Problem D（Div. 2 同题是 2256F）
- **难度**：$\ast 2300$
- **限制**：时间 2 s / 内存 256 MB
- **标签**：二分答案，位运算（bitmask），数据结构（堆），贪心，数学，排序

**题意**：给定 $n$ 个正整数。每一秒先选一个下标 $p$，然后**同时**折半：$a_p$ 变 $\left\lfloor a_p/2\right\rfloor$，其余每个 $a_i$ 变 $\left\lceil a_i/2\right\rceil$。求让全部数变成 $0$ 的最少秒数。多测。入口是「同时」二字：每一秒**每个**数都被折半一次，区别只在于它这一秒是「被选中」（下取整）还是「没被选中」（上取整）。

**约束**：$1\le t\le10^4$，$\sum n\le2\times10^5$，$1\le a_i\le10^9<2^{30}$；2 s 下单组需 $O(n\log n)$ 量级。

## 2. 示例

```text
输入
5
1
3
3
1 1 1
3
1 2 4
2
5 2
6
1 2 3 4 5 6

输出
2
3
3
3
6
```

- 第 1 组：$3\to1\to0$，两次都是它自己被选中；第 2 组：三个 $1$ 都只在**自己**被选中时才变 $0$（被挤掉时 $\lceil1/2\rceil=1$），故 3 秒。
- 第 3 组：$[1,2,4]\to[0,1,2]\to[0,0,1]\to[0,0,0]$；第 4 组：$[5,2]\to[2,1]\to[1,0]\to[0,0]$，依次选 $1,2,1$（$5$ 被选了**两次**）；第 5 组每数至少被选一次，答案 $=n=6$。

**自造示例**（说明「只看最大二进制位数」不够）：

```text
输入
2
2
7 1
3
3 2 1

输出
4
3
```

$[7,1]$：若 $7$ 只在最后被选一次，它当时须为 $1$，需要 $3$ 秒垫步再加自己那一秒，共 4 秒；而 3 秒确实喂不饱需求 $7$ 与 $1$。

## 3. 解题思路

### 3.1 暴力思路

直接搜索每秒 $n$ 种选择，$T$ 秒共 $n^T$ 条路径，而答案本身就有 $T\ge n$ 的量级，完全不可行；对单个元素做 DP 也无法同时维护 $n$ 个进度。题面还会诱使人猜两个「显然」结论，都错：

- **答案 $=\max_i\operatorname{bitlen}(a_i)$**：错。$[1,1,1]$ 的 bitlen 全为 $1$，却需 3 秒——每个 $1$ 必须在自己被选中时变 $0$。
- **每数只选一次，答案 $=\max_i(\text{名次}_i+\lceil\log_2a_i\rceil)$**：错。$[5,2]$ 上给 4，实际 3：同一秒只能选一个数，但同一个数可以**被选多次**，$5=4+1$。

### 3.2 核心观察：二进制权值模型

![把每个数看成二进制权值](images/cf2255_d_binary_weight_model.svg)

先统一两种折半（$\left\lceil x/2\right\rceil=\lfloor(x+1)/2\rfloor$），每一秒都是 $v\leftarrow\left\lfloor (v+b)/2\right\rfloor$，其中 $b=0$ 表示这一秒被选中、$b=1$ 表示没被选中（即「多加 1 再取整」）。令 $B_t=\sum_{j=1}^{t}b_j2^{t-j}$（把 $b_1b_2\cdots b_t$ 当二进制数，$b_1$ 为最高位），归纳可得

$$v_t=\left\lfloor\frac{a+B_t}{2^t}\right\rfloor .$$

于是 $v_t=0\iff a+B_t<2^t\iff a\le 2^t-1-B_t=S_t$，其中 $S_t=\sum_{j:\,b_j=0}2^{t-j}$ 正是**「被选中」那些秒的 $2$ 的幂权值之和**（第 $j$ 秒被选中就记 $2^{t-j}$）。又 $S_{t+1}=2S_t+[\,t+1\text{ 被选中}\,]\ge S_t$，且 $\lfloor0/2\rfloor=\lceil0/2\rceil=0$，所以

> **归零判据**：第 $i$ 个数在 $T$ 秒内变 $0$ $\iff$ 它攒到的权值 $S_i(T)\ge a_i$。例：$a=10$、前两秒被选、后两秒没被选，则 $S_4=2^3+2^2=12\ge10$ 且 $v_4=\lfloor(10+3)/16\rfloor=0$。

### 3.3 算法流程：分物品 + LPT + 30 截断

![归约成分物品，用 LPT 判定](images/cf2255_d_bin_covering.svg)

把「第 $j$ 秒选中第 $i$ 个数」读成「把权值 $2^{T-j}$ 记到箱子 $i$ 头上」，得到

> **等价问题**：把 $T$ 件物品 $2^{T-1},2^{T-2},\dots,2^0$（每件恰好一个）分给 $n$ 个箱子，要求第 $i$ 箱总和 $\ge a_i$；物品必须全部放下，箱子允许溢出。

**判定贪心（LPT）**：物品从大到小处理，每次给「当前剩余需求最大」的箱子。交换论证（引理 4）说明它最优：若有可行分配，贪心也能成。但 $T\approx n\approx2\times10^5$，每个 $T$ 都堆一遍太慢，于是按值域截断：

![按 2^30 截断，只剩 30 件物品要精算](images/cf2255_d_thirty_window.svg)

$a_i\le10^9<2^{30}$，故权值 $\ge2^{30}$ 的物品**一件就能喂饱任何箱子**。设 $k=\min(n,\max(0,T-30))$，前 $k$ 件（$2^{T-1},\dots,2^{T-k}$，全 $\ge2^{30}$）在 LPT 下必按需求降序一对一清零剔除，只剩最小的 $n'=n-k$ 个需求对最后 $T-k$ 件物品（$2^{T-k-1},\dots,2^0$），而 $T\ge n$ 给出 $n'\le30$、$T-k\le30$——每次判定只是 $\le30\times\le30$ 的 LPT，$O(30\log30)$。

**答案范围**：$T<n$ 必不可行（每箱至少 1 件），$T=n+30$ 必可行（前 $n$ 件都 $\ge2^{30}$）；可行性对 $T$ 单调（多一件随便塞），故在 $[n,n+30]$ 上二分，约 5 次判定。**算法**：① $a$ 升序排序；② 二分 $T$ 并用上述截断 LPT 判定；③ 输出最小可行 $T$。

### 3.4 示例演算

![样例 4 的完整走查](images/cf2255_d_walkthrough.svg)

$[5,2]$、$T=3$，物品为 $2^2=4,\;2^1=2,\;2^0=1$（$T=2$ 时只有 $2,1$，喂不饱需求 $5$，故答案 3；「每数只选一次」会错判成 4）：

| 秒 $t$ | 物品 | 选中 $p$ | 状态 | 谁攒到了什么 |
|--------|------|----------|------|--------------|
| 1 | $2^{3-1}=4$ | 1 | $[5,2]\to[2,1]$ | 元素 1 得 4 |
| 2 | $2^{3-2}=2$ | 2 | $[2,1]\to[1,0]$ | 元素 2 得 $2\ge2$ ✓ |
| 3 | $2^{3-3}=1$ | 1 | $[1,0]\to[0,0]$ | 元素 1 共 $4+1=5\ge5$ ✓ |

## 4. 算法细节

1. **多测清空**：堆与临时变量每组新建，不用跨用例的全局数组；$\sum n\le2\times10^5$，排序即 $O(n\log n)$。
2. **二分写法**：`lo = n, hi = n + 30`（`hi` 必可行），`while (lo < hi) { mid; feasible(mid) ? hi = mid : lo = mid + 1; }`；`lo = n` 可能不可行，别用「先记录再收缩」的 `lo <= hi` 版本。
3. **常数 30 与权值写法**：$10^9<2^{30}$，故 $2^{30}$ 以上物品能独吞任一需求；若上界换成 $10^{18}$ 就必须改成 60。权值写 `1LL << e`（$e\le29$），剩余需求一律 `long long`，便于日后扩容常数。
4. **LPT 实现**：大顶堆存「剩余需求」。取堆顶 $x$ 减去权值 $w$，$x-w>0$ 才压回；堆空即全部达标。C++ 用 `priority_queue<long long>`，Python 用 `heapq` 存负值。
5. **只排序一次**：升序后判定只取前缀 `a[0..nrem-1]`（最小的 `nrem` 个），不必每次二分重排。
6. **I/O**：C++ `sync_with_stdio(false)` + `cin.tie(nullptr)`；Python 一次 `read().split()` 读完再切片。

## 5. 正确性证明

**引理 1（展开式）**：$v_t=\left\lfloor (a+B_t)/2^t\right\rfloor$，$B_t=\sum_{j\le t}b_j2^{t-j}$。

**证明**：对 $t$ 归纳。设 $v_{t-1}=\lfloor(a+B_{t-1})/2^{t-1}\rfloor$，则 $v_t=\lfloor(v_{t-1}+b_t)/2\rfloor=\lfloor(a+B_{t-1}+b_t2^{t-1})/2^t\rfloor=\lfloor(a+B_t)/2^t\rfloor$，用了 $\lfloor(\lfloor x/m\rfloor+c)/n\rfloor=\lfloor(x+cn)/(mn)\rfloor$（$m,n\ge1$）。∎

**引理 2（归零判据）**：$v_t=0\iff S_t\ge a$，$S_t=\sum_{j\le t,\,b_j=0}2^{t-j}$；且 $S_t$ 关于 $t$ 单调不减，$0$ 是吸收态。

**证明**：由引理 1，$v_t=0\iff a+B_t<2^t\iff a\le2^t-1-B_t$；又 $\sum_{j\le t}2^{t-j}=2^t-1$，故 $2^t-1-B_t=S_t$。单调性由 $S_{t+1}=2S_t+[\,t+1\text{ 被选中}\,]\ge S_t$，吸收态由 $\lfloor0/2\rfloor=\lceil0/2\rceil=0$ 得。∎

**引理 3（覆盖模型等价）**：$T$ 秒内全归零 $\iff$ 能把 $T$ 件物品 $2^{T-1},\dots,2^0$ 分给 $n$ 个箱子且第 $i$ 箱总和 $\ge a_i$。

**证明**：($\Rightarrow$)「第 $j$ 秒选中第 $i$ 个数」$\mapsto$「物品 $2^{T-j}$ 给箱子 $i$」是双射，由引理 2 每箱总和即 $S_i(T)\ge a_i$。($\Leftarrow$) 反过来按物品归属决定每秒选谁，引理 2 给出 $v_i(T)=0$。∎

**引理 4（LPT 最优）**：物品从大到小依次给「当前剩余需求最大」的箱子；若覆盖问题有可行分配，贪心也给出可行分配。

**证明**：对物品件数归纳。设最大物品 $m=2^{T-1}$，需求最大的箱子 $X$、需求 $d$，取任一可行分配 $O$。

- $d>m$：任何可行分配都必须把 $m$ 给 $X$（否则 $X$ 能拿到的总和 $\le2^{T-1}-1<d$，矛盾），故 $O$ 已如此，删去 $m$ 与 $X$ 后归纳。
- $d\le m$：贪心把 $m$ 给 $X$，$X$ 立即达标剔除。若 $O$ 中 $m$ 在箱子 $Y\ne X$，构造 $O'$：$m$ 归 $X$，$O$ 中 $X$ 的全部物品并入 $Y$。则 $X$ 达标（$d\le m$），$Y$ 的总和 $\ge\operatorname{sum}(O_X)\ge d\ge d_Y$（$X$ 需求最大），其余不动，$O'$ 可行且 $m$ 归 $X$，归纳。∎

**引理 5（30 截断）**：设 $T\ge n$、$\max a_i<2^{30}$，$k=\min(n,\max(0,T-30))$。则 LPT 前 $k$ 件物品恰按需求降序一对一喂饱 $k$ 个最大需求；判定只剩最小的 $n'=n-k$ 个需求与最后 $T-k$ 件物品，且 $n'\le30$、$T-k\le30$。

**证明**：前 $k$ 件权值均 $\ge2^{30}>10^9\ge$ 任一剩余需求，故 LPT 每次给出后该箱立刻归零并剔除，第 $r$ 件必给第 $r$ 大需求，一对一成立。剩余物品恰为 $2^{T-k-1},\dots,2^0$ 共 $T-k$ 件。由 $T\ge n$：若 $k=n$ 则 $n'=0$；若 $k=T-30<n$ 则 $n'=n-T+30\le30$（用 $n\le T$）且 $T-k=30$；若 $T\le30$ 则 $k=0$，此时 $n\le T\le30$，故 $T-k\le30$。∎

**定理**：算法输出的 $T$ 恰为最少秒数。

**证明**：引理 3 把原问题等价成覆盖问题，引理 4 说明 LPT 判定精确，引理 5 说明截断判定与原 LPT 等价，故 `feasible(T)` 为真当且仅当 $T$ 秒可行。可行性单调（多出的物品 $2^T$ 塞给任一箱子即可），且 $T<n$ 必不可行、$T=n+30$ 必可行，二分区间正确，故输出最小可行值。∎

## 6. 复杂度分析

- **时间**：每组排序 $O(n\log n)$；二分 5 次判定，每次是对 $\le30$ 个箱子、$\le30$ 件物品的堆操作 $O(30\log30)$。合计 $O(n\log n)$，与值域无关，$\sum n=2\times10^5$ 时约 $3\times10^6$ 次基本操作。
- **空间**：$O(n)$ 存 $a$；堆与临时变量 $O(30)$。**实测**：C++17 在最大数据（$n=2\times10^5$ 的随机 / 全 $10^9$ / 全 $1$，以及 $t=10^4$ 个 $n=20$）上 $0.13\text{–}0.34$ s（含 I/O）；Python3 同数据 $0.04\text{–}0.38$ s，相对 2 s 有 5 倍以上余量。

## 7. 参考代码

### C++17

```cpp
#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    const int BIG = 30;                          // a_i <= 1e9 < 2^30
    while (t--) {
        int n; cin >> n;
        vector<long long> a(n);
        for (auto &x : a) cin >> x;
        sort(a.begin(), a.end());                // 升序，判定只取最小的一段
        auto ok = [&](long long T) -> bool {
            if (T < n) return false;             // 每箱至少一件物品
            long long k = min<long long>(n, max<long long>(0, T - BIG));
            int nrem = n - (int)k;               // 剩余箱子 = 最小的 nrem 个需求
            if (nrem == 0) return true;          // 大物品一人一件，全喂饱
            priority_queue<long long> pq;        // 大顶堆：剩余需求
            for (int i = 0; i < nrem; i++) pq.push(a[i]);
            for (int e = (int)(T - k) - 1; e >= 0; e--) {   // 2^(T-k-1) .. 2^0
                if (pq.empty()) break;
                long long r = pq.top(); pq.pop();
                r -= (1LL << e);
                if (r > 0) pq.push(r);           // 未达标才回堆
            }
            return pq.empty();                   // 堆空 = 全部达标
        };
        long long lo = n, hi = (long long)n + BIG;      // hi 必然可行
        while (lo < hi) {
            long long mid = (lo + hi) / 2;
            if (ok(mid)) hi = mid; else lo = mid + 1;
        }
        cout << lo << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys, heapq


def main():
    d = sys.stdin.buffer.read().split()
    p = 0; t = int(d[p]); p += 1
    out = []; BIG = 30                            # a_i <= 1e9 < 2^30
    for _ in range(t):
        n = int(d[p]); p += 1
        a = sorted(int(x) for x in d[p:p + n]); p += n

        def ok(T):
            if T < n: return False                # 每箱至少一件物品
            k = min(n, max(0, T - BIG))           # 权值 >= 2^30：一件喂饱一个
            nrem = n - k                          # 剩余箱子 = 最小的 nrem 个需求
            if nrem == 0: return True
            hp = [-a[i] for i in range(nrem)]      # 小顶堆存负值 = 大顶堆
            heapq.heapify(hp)
            for e in range(T - k - 1, -1, -1):    # 2^(T-k-1) .. 2^0
                if not hp: break
                r = -heapq.heappop(hp) - (1 << e)
                if r > 0: heapq.heappush(hp, -r)
            return not hp

        lo, hi = n, n + BIG                        # hi 必然可行
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid): hi = mid
            else: lo = mid + 1
        out.append(str(lo))
    print("\n".join(out))


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：只能是「每次都被选中」的向下取整链，答案恰为 $\operatorname{bitlen}(a_1)$（$a=10^9$ 时为 30）。此时 $T\ge n$、$T\le n+30$ 自然满足。
2. **满场 $a_i=1$**：$\lceil1/2\rceil=1$，每个 $1$ 都必须在自己被选中那一秒才归零，答案就是 $n$；若把「需求 1」当成不需要物品，会错答成 $n-1$。
3. **区间端点**：$T\ge n$ 因每箱至少 1 件；$T\le n+30$ 因 $T=n+30$ 时前 $n$ 件都 $\ge2^{30}$。上界写成 $n+29$ 或截断常数写成 31/29 都会在特定数据上错。
4. **不能「每数只选一次」**：$[5,2]$ 单次选取要 4 秒，允许一个箱子收多件后才 3 秒（$5=4+1$），这正是必须用 LPT 的原因。
5. **常数 30 与值域绑定**：判定依赖 $2^{30}>10^9$。若 $a_i$ 上界变到 $10^{18}$，`BIG` 必须改 60，否则会把「必须靠大物品」的需求错判为可合并。
6. **堆方向与 I/O**：Python `heapq` 是小顶堆必须存负值，C++ `priority_queue` 默认大顶堆，写反等于「给需求最小的箱子」；$t$ 可达 $10^4$，每组重建堆，Python 用一次 `read().split()` 避免逐行 `input()` 超时。

## 相关题目与扩展

- [Codeforces 2255A. Hot Potatoes at the Fairy Warehouse](https://codeforces.com/problemset/problem/2255/A)：同场签到题，先热身。
- [Codeforces 2256F](https://codeforces.com/problemset/problem/2256/F)：本题的 Div. 2 同题，做法完全一致。
- [LeetCode 1011](https://leetcode.cn/problems/capacity-to-ship-packages-within-d-days/) / [LeetCode 410](https://leetcode.cn/problems/split-array-largest-sum/)：同为「二分答案 + 贪心判定」的骨架。

**延伸思考**：

1. **换成 $b$ 进制**：把「除以 2」改成「除以 $b$」，则 $v_t=\lfloor(a+B_t)/b^t\rfloor$，物品变成 $1,b,b^2,\dots$ 每级各一件，LPT 与截断结构不变，只是常数由 $2^{30}$ 换成 $b^{\lceil\log_bA\rceil}$。
2. **每秒可选 $k$ 个**：等价于每件物品可复制 $k$ 份，下界从 $n$ 降到 $\lceil n/k\rceil$，物品池需按幂次拆位维护，判定仍是 LPT。
3. **要求「恰好」凑出 $a_i$**：覆盖升级为精确覆盖，LPT 失效（NP 难味道），需状压或数位 DP。截断技巧的价值也在这里：只需把 `BIG` 改 60 就能承受 $a_i\le10^{18}$，复杂度不变——答案区间长度只依赖 $\log A$，与 $n$ 无关。
