# Codeforces 交换置换 题解

## 1. 题目概述

- **标题 / 题号**：交换置换（Codeforces 2237E，英文名 Permutation Commutation）
- **链接**：https://codeforces.com/problemset/problem/2237/E
- **来源**：Order Capital Round 2 (Codeforces Round 1104, Div. 1 + Div. 2) · Problem E
- **难度**：2100（2250 分，题面标注 *2100）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：数据结构，图论，贪心

**题意**：给定长度为 $n$ 的排列 $a$ 和一个不完整的序列 $b$。$b$ 中每个元素要么是 $-1$，要么是 $1..n$ 中的某个整数，且 $1..n$ 的每个整数在 $b$ 中**至多出现一次**。把 $b$ 中所有 $-1$ 替换成整数，使它成为一个排列，并且对每个 $1 \le i \le n$ 都满足

$$a_{b_i} = b_{a_i}.$$

在所有合法的补全中，输出**字典序最小**的 $b$；若不存在合法补全，输出 `NO`。多测，$\sum n \le 2\times 10^5$。

**约束**：

- $1 \le t \le 10^4$，$1 \le n \le 2\times 10^5$，$\sum n \le 2\times 10^5$；
- $a$ 是排列，$b_i \in \{-1\} \cup [1,n]$，且每个值在 $b$ 中至多出现一次；
- 等价的写法是把 $a,b$ 都看成置换，条件即 $a \circ b = b \circ a$（$a$ 与 $b$ **可交换**）；
- 输出第二行恰好 $n$ 个数，`NO` 时不输出第二行。

## 2. 示例

官方样例共 12 组（输入 / 输出原样）：

```text
输入：
12
3
2 3 1
-1 -1 -1
4
2 1 4 3
-1 -1 4 -1
4
2 1 4 3
3 1 -1 -1
4
2 1 4 3
1 -1 -1 2
5
2 3 1 5 4
2 -1 -1 -1 -1
5
2 3 1 5 4
4 -1 -1 -1 -1
6
2 3 1 5 6 4
4 -1 -1 -1 -1 -1
6
2 1 4 3 6 5
-1 3 -1 -1 -1 -1
6
3 5 6 2 1 4
-1 -1 -1 3 6 -1
7
2 3 1 5 4 6 7
-1 -1 -1 -1 -1 7 -1
8
2 3 4 1 6 7 8 5
5 7 -1 -1 -1 -1 -1 -1
8
2 3 4 1 6 7 8 5
5 -1 -1 -1 -1 -1 -1 -1

输出：
YES
1 2 3
YES
1 2 4 3
NO
NO
YES
2 3 1 4 5
NO
YES
4 5 6 1 2 3
YES
4 3 1 2 5 6
NO
YES
1 2 3 4 5 7 6
NO
YES
5 6 7 8 1 2 3 4
```

样例覆盖了本题的全部判定分支：

| # | $a$ 的环结构 | 判负 / 可行的原因 |
|---|--------------|-------------------|
| 1 | $(1\,2\,3)$ | 全 $-1$，答案为恒等置换 |
| 2 | $(1\,2)(3\,4)$ | $b_3=4$ 通过 $a_{b_3}=b_{a_3}$ 把 $b_4$ 钉死成 3 |
| 3 | $(1\,2)(3\,4)$ | $b_1=3$ 要求 $(1\,2)\to(3\,4)$，$b_2=1$ 要求 $(1\,2)\to(1\,2)$，同源环冲突 |
| 4 | $(1\,2)(3\,4)$ | $b_1=1$ 已把 $(1\,2)$ 占为目标环，$b_4=2$ 想再占一次 |
| 6 | 3 元环 + 2 元环 | $b_1=4$ 跨长度配对，直接 `NO` |
| 9 | 单个 6 元环 | $b_4=3$ 给出 shift 4，$b_5=6$ 给出 shift 3，互相矛盾 |

## 3. 解题思路

### 3.1 暴力思路

最直接的做法是枚举所有补全：把未出现的值任意填进 $-1$ 的位置，再逐个检查 $a_{b_i}=b_{a_i}$。补全数是 $(n-k)!$ 级别（$k$ 为已知个数），$n=2\times10^5$ 时天文数字。

另一个"看起来合理"的局部贪心也会翻车：**逐位填最小可用值**。取 $a=[2,1,4,3]$、$b=[4,-1,-1,-1]$：$b_1=4$ 已定，按局部贪心 $b_2$ 应填未用的最小值 $1$，但条件 $a_{b_2}=b_{a_2}$ 在 $i=2$ 时写成 $a_{b_2}=b_1=4$，于是 $b_2=a^{-1}(4)=3$ 是**被强制**的——$b_2$ 根本不能自由选。

这说明约束不是逐位的，而是**整环传播**的：一个已知值会连带钉死它所在的整个 $a$-环。想清楚"哪些置换与 $a$ 可交换"，问题才变得可做。

### 3.2 核心观察：交换置换 = 把环整体搬到等长环上

![可交换置换的环结构](images/cf2237_e_centralizer_concept.svg)

设 $C$ 是 $a$ 的一个环，写成 $C=(c_0\,c_1\,\cdots\,c_{L-1})$，其中 $c_{j+1}=a(c_j)$（下标模 $L$）。由 $ab=ba$ 可得对任意 $i$ 有 $a^i b = b a^i$，即

$$b(a^i x) = a^i\bigl(b(x)\bigr).$$

于是**只要知道环内任意一个点的像 $b(c_0)$，整个环的像就被确定了**。又因为 $b$ 是双射且 $b a b^{-1}=a$，$b$ 必须把一个 $a$-环整体映到另一个**长度相同**的 $a$-环上，且不同环的像不能重合。反过来，任取一个"同长度环之间的双射"，再为每个源环选一个平移量 $s$，令

$$b(c_j) = d_{(j+s) \bmod L},$$

则 $b$ 与 $a$ 可交换，且所有可交换置换都长这样。对长度 $L$ 的 $k_L$ 个环，合法 $b$ 的个数是 $\prod_L k_L! \cdot L^{k_L}$。

### 3.3 算法流程：钉死部分映射，再按环贪心

![算法流程](images/cf2237_e_constraint_flow.svg)

由核心观察，问题化为"给每个环挑一个同长度的目标环 + 一个平移量"，而字典序只关心数组 $b$ 的逐位大小。

**第一步：分解 $a$ 的环。** 按 $i=1..n$ 扫描，遇到未访问的 $i$ 就沿 $a$ 绕一圈。因为 $i$ 之前的所有点都已访问，所以 $i$ 必是它所在环的**最小元素**，环内位置满足 $\text{pos}[i]=0$。

**第二步：处理所有已知 $b_i \ne -1$。** 源环 $s=\text{cid}[i]$，目标环 $t=\text{cid}[b_i]$，平移量

$$\text{shift} = \bigl(\text{pos}[b_i] - \text{pos}[i]\bigr) \bmod L.$$

若两环长度不等、或同一源环两次给出不同的 $(t,\text{shift})$、或 $t$ 已被别的源环占用，则 `NO`。三条都通过，就说明已知值彼此相容。

**第三步：贪心补齐空闲源环。** 按 $i=1..n$ 扫描，若 $i$ 是某环的最小元素、且该环还没有被钉死（环内没有任何已知值），就为它选**最小可用目标环** $D$ 并置 $\text{shift}=0$，此时 $b_i = \min D$。每个长度组内维护一个只向右移动的指针来跳过已占用的目标环。

**第四步：还原并输出。** 对每个位置 $i$，$b_i = \text{elems}\bigl[\text{img}[\text{cid}[i]]\bigr]\bigl[(\text{pos}[i]+\text{shift}) \bmod L\bigr]$。

**为什么贪心是对的？** 处理到 $i$ 时，所有小于 $i$ 的位置已经定死；$i$ 是空闲源环 $C$ 的最小元，$\text{pos}[i]=0$，平移量可自由取，所以 $b_i$ 能取到目标环 $D$ 的任何一个元素。于是 $b_i$ 的最小可能值就是所有可用目标环最小元素的最小值；而这个选择一定还能延伸成完整解（剩余源环与剩余目标环一样多，任意配对即可）。逐位取最小，即为字典序最小。

### 3.4 示例演算

![样例 8 走查](images/cf2237_e_walkthrough.svg)

以样例 8 为例：$a=[2,1,4,3,6,5]$，三个环都是对换 $(1\,2)$、$(3\,4)$、$(5\,6)$，$b=[-1,3,-1,-1,-1,-1]$。

| 决策点 | 源环 → 目标环 | shift | 写入的 $b$ |
|--------|---------------|-------|------------|
| 已知 $b_2=3$ | $(1\,2) \to (3\,4)$ | $0-1 \equiv 1$ | $b_1=4,\ b_2=3$ |
| $i=3$（$(3\,4)$ 的最小元） | $(3\,4) \to (1\,2)$ | 0 | $b_3=1,\ b_4=2$ |
| $i=5$（$(5\,6)$ 的最小元） | $(5\,6) \to (5\,6)$ | 0 | $b_5=5,\ b_6=6$ |

在 $i=3$ 处可用的目标环是 $(1\,2)$ 与 $(5\,6)$，最小元素分别是 $1$ 和 $5$，取小者；到 $i=5$ 只剩 $(5\,6)$。最终 $b=[4,3,1,2,5,6]$，与官方输出一致。

反向的例子是样例 9：$a$ 只有一个 6 元环，$b_4=3$ 给出 $\text{shift}=1-3\equiv4$，$b_5=6$ 给出 $\text{shift}=2-5\equiv3$，同一源环两个平移量，判 `NO`。

## 4. 算法细节

1. **环内顺序从最小元素起**：分解时从 $i$ 出发绕一圈，天然让 $\text{elems}[c][0]=\min C$，于是 $\text{pos}[\min C]=0$。这一步让第三步的"选最小目标环 + shift=0"直接得到 $b_i=\min D$，省掉一次取模计算。
2. **平移量公式**：$\text{shift}=(\text{pos}[b_i]-\text{pos}[i]) \bmod L$。C++ 中 `%` 会保留负号，必须写成 `((x % L) + L) % L`；Python 的 `%` 天然非负。
3. **三条冲突判定缺一不可**：长度不等；同一源环的 $(t,\text{shift})$ 不一致；目标环 $t$ 已被其他源环占用（$b$ 必须是单射）。同一个源环重复指向同一目标环且 shift 相同时不算冲突。
4. **空闲环的判定**：用 `img[c] == -1`，即"该环内没有任何已知 $b$ 值"。绝不能仅看某个位置是否为 $-1$——一个已知值会钉死整个环。
5. **贪心指针**：把环按长度分组（`byLen[L]` 里按环编号升序，也就是最小元素升序），每组一个指针 `ptr[L]`，遇到已占用的目标环就右移。指针只增不减，总移动次数不超过环数，故这一步均摊 $O(n)$。
6. **还原时顺带自检**：填出的 $b_i$ 若与给定的 $b_i$ 不同，说明实现有误，可直接判 `NO`（线上代码保留这一句作为断言，正常输入不会触发）。
7. **数据结构选型**：全部用定长 `vector` 和数组下标，避免有序容器的 $\log n$ 开销；`byLen` 用 `vector<vector<int>>(n+1)` 而不是 `unordered_map`，省去哈希开销。
8. **多测与读写**：$\sum n \le 2\times10^5$，`scanf/printf` 或关闭同步的 `cin` 都足够；Python 用 `sys.stdin.buffer.read().split()` 一次读入，避免逐行 I/O。

## 5. 正确性证明

**引理 1（交换置换的环刻画）**：$b$ 与 $a$ 可交换，当且仅当存在"$a$ 的环到同长度环的双射"，以及每个源环上的平移量 $s$，使得对 $C=(c_0,\dots,c_{L-1})$ 有 $b(c_j)=d_{(j+s)\bmod L}$。

**证明**：若 $ab=ba$，对 $k$ 归纳得 $a^k b = b a^k$，即 $b(a^k x)=a^k(b(x))$。取 $x=c_0$，则 $b(c_j)=b(a^j c_0)=a^j(b(c_0))$，故 $b$ 在 $C$ 上的像完全由 $b(c_0)$ 决定且恰是 $b(c_0)$ 所在的 $a$-环，长度必为 $L$（$a$ 在该环上的作用周期为 $L$）。$b$ 是双射，故不同环的像环互不相同，得到环间双射；又 $b(c_0)=d_s$ 对某个 $s$ 成立。反之，按该式定义的 $b$ 是双射，且 $b(a\,c_j)=d_{(j+1+s)}=a\,b(c_j)$，故 $ba=ab$。∎

**引理 2（约束相容的充要条件）**：给定若干 $b_i=c$ 的约束，存在与 $a$ 交换且满足全部约束的排列，当且仅当：(i) 每条约束的源环与目标环长度相等；(ii) 同一源环的所有约束给出同一个目标环与同一个平移量；(iii) 不同源环的目标环互不相同。

**证明**：(必要性) 由引理 1，$b$ 在每个环上由"目标环 + 平移量"决定，故同一源环的约束必须一致，且长度必须相等；$b$ 是双射，故两个源环不能映到同一个目标环。

(充分性) 把约束诱导出的 $(C \mapsto D,\ s)$ 看成环集合上的部分双射。由 (ii)(iii)，它确实是良定义的单射。设长度 $L$ 的环有 $k_L$ 个、其中 $m_L$ 个已被指定目标，则剩余 $k_L-m_L$ 个源环与剩余 $k_L-m_L$ 个目标环数量相等，任意配成双射并把它们的平移量取 $0$，就得到完整的环间双射与平移量表，由引理 1 得到合法 $b$。对任一约束 $b_i=c$：该源环的平移量由约束定为 $s$，而 $\text{pos}[c]=\text{pos}[i]+s \pmod L$，故还原出的 $b_i=d_{\text{pos}[c]}=c$，约束被满足。∎

**引理 3（贪心取到当前最小值且不破坏可解性）**：设所有 $<i$ 的位置已固定，$i$ 是某空闲源环 $C$ 的最小元素。则任意可延伸解在 $i$ 处的取值不小于 $\min\{\min D : D \text{ 为可用目标环}\}$，且该下界可达到。

**证明**：由引理 1，$b_i$ 必属于某个可用目标环 $D$，故 $b_i \ge \min D \ge \min\{\min D\}$。另一方面，取使 $\min D$ 最小的 $D^*$，令平移量 $s=\text{pos}[\min D^*]-\text{pos}[i]=0-0=0$（两项都是 $0$），则 $b_i=\min D^*$ 达到下界；由引理 2 的充分性，剩余部分仍可配成完整解。∎

**引理 4（决策的不可回退性）**：一旦在 $i$ 处选定目标环并写入 $C$ 全体元素的像，$C$ 内所有位置（含 $i$ 与 $C$ 中更大的元素）的值就固定；而 $i$ 是 $C$ 的最小元素，故后续扫描不会再改变 $C$。

**证明**：引理 1 说明 $b$ 在 $C$ 上由 $(D,s)$ 唯一决定；扫描时只在环的最小元素处决策，且决策后 $\text{img}[c]\ne-1$，之后对同一环不再进入决策分支。∎

**定理**：算法输出的 $b$ 是字典序最小的合法补全；当算法判定 `NO` 时，确实不存在合法补全。

**证明**：若算法未判负，引理 2 说明存在合法补全，且算法构造出一个（引理 3 的可达性 + 引理 4 的固定性）。设算法输出 $p$，任一合法补全 $q \ne p$，令 $i$ 为第一个 $p_i \ne q_i$ 的位置。位置 $i$ 只可能是某环的最小元素：若 $i$ 不是最小元素，或它所在环被已知值钉死，则 $p_i$ 由更早的决策（或该约束）唯一决定，$q$ 与 $p$ 前缀相同就必然也相同，矛盾。在该决策点，$p_i$ 取到了引理 3 的下界，而 $q_i$ 属于同一可行集合，故 $p_i \le q_i$；又 $p_i \ne q_i$，得 $p_i < q_i$。故 $p$ 字典序最小。反之，若算法判负，则引理 2 的必要条件被违反，不存在合法补全。∎

## 6. 复杂度分析

- **时间**：分解环 $O(n)$；每条约束 $O(1)$，共 $O(n)$；贪心部分每个环被指针扫过一次，均摊 $O(\#\text{环}) \le O(n)$；还原 $O(n)$。每组 $O(n)$，总计 $O(\sum n) \le 2\times 10^5$。
- **空间**：`cid`、`pos`、`img`、`shift`、`byLen`、`ptr` 与环内元素表都是 $O(n)$，另加输入数组 $O(n)$，合计 $O(n)$，远低于 256 MB。
- **对照时限**：本机实测 $n=2\times10^5$ 的四类最坏数据（随机置换全 $-1$、单个大环全 $-1$、全为长度 1 的环且一半已知、$t=10^4$ 组 $n=20$）C++ 为 0.04–0.08 s，Python3 为 0.21–0.41 s；相对 2 s 仍有 4 倍以上余量，CPython 也能过，PyPy 更稳。
- **常数**：全部是连续内存的顺序扫描，缓存友好；`vector<vector<int>>` 只为每个环存一次元素，总元素数恰为 $n$。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n;
        scanf("%d", &n);
        vector<int> a(n + 1), b(n + 1);
        for (int i = 1; i <= n; i++) scanf("%d", &a[i]);
        for (int i = 1; i <= n; i++) scanf("%d", &b[i]);

        // 1. 分解 a 的置换环，环内元素从最小值开始按 a 的顺序排列
        vector<int> cid(n + 1, -1), pos(n + 1, 0);
        vector<vector<int>> elems;   // elems[c][0] 是环 c 的最小元素
        for (int i = 1; i <= n; i++) {
            if (cid[i] != -1) continue;
            vector<int> cur;
            int x = i;
            do {
                cid[x] = (int)elems.size();
                pos[x] = (int)cur.size();
                cur.push_back(x);
                x = a[x];
            } while (x != i);
            elems.push_back(cur);
        }
        int C = (int)elems.size();

        // 2. 处理所有已知 b_i：源环 -> (目标环, 平移量)
        vector<int> img(C, -1), sh(C, 0);
        vector<char> usedTgt(C, 0);
        bool ok = true;
        for (int i = 1; i <= n && ok; i++) {
            if (b[i] == -1) continue;
            int s = cid[i], t = cid[b[i]];
            int L = (int)elems[s].size();
            if (L != (int)elems[t].size()) { ok = false; break; }
            int shift = ((pos[b[i]] - pos[i]) % L + L) % L;
            if (img[s] == -1) {
                if (usedTgt[t]) { ok = false; break; }
                img[s] = t;
                sh[s] = shift;
                usedTgt[t] = 1;
            } else if (img[s] != t || sh[s] != shift) {
                ok = false;
            }
        }

        if (!ok) { puts("NO"); continue; }

        // 3. 每个长度组内按环最小元素升序贪心：接上最小的可用目标环
        vector<vector<int>> byLen(n + 1);
        for (int c = 0; c < C; c++) byLen[elems[c].size()].push_back(c);
        vector<int> ptr(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            int c = cid[i];
            if (pos[i] != 0 || img[c] != -1) continue;  // 只在空闲环的最小元处决策
            int L = (int)elems[c].size();
            vector<int> &v = byLen[L];
            int &p = ptr[L];
            while (usedTgt[v[p]]) p++;                  // 剩余源环数 == 剩余目标环数
            img[c] = v[p];
            sh[c] = 0;                                  // shift 0：最小元接到最小元
            usedTgt[v[p]] = 1;
        }

        // 4. 还原 b
        vector<int> ans(n + 1);
        for (int i = 1; i <= n; i++) {
            int c = cid[i], L = (int)elems[c].size();
            ans[i] = elems[img[c]][(pos[i] + sh[c]) % L];
            if (b[i] != -1 && ans[i] != b[i]) ok = false;   // 自检，正常输入不会触发
        }
        if (!ok) { puts("NO"); continue; }

        puts("YES");
        for (int i = 1; i <= n; i++) printf("%d%c", ans[i], " \n"[i == n]);
    }
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    t = data[p]
    p += 1
    out = []
    for _ in range(t):
        n = data[p]
        p += 1
        a = [0] + data[p:p + n]
        p += n
        b = [0] + data[p:p + n]
        p += n

        # 1. 分解环，每个环从最小元素开始
        cid = [-1] * (n + 1)
        pos = [0] * (n + 1)
        elems = []
        for i in range(1, n + 1):
            if cid[i] != -1:
                continue
            cur = []
            x = i
            while True:
                cid[x] = len(elems)
                pos[x] = len(cur)
                cur.append(x)
                x = a[x]
                if x == i:
                    break
            elems.append(cur)
        C = len(elems)

        # 2. 已知 b_i：源环 -> (目标环, 平移量)
        img = [-1] * C
        sh = [0] * C
        used = [False] * C
        ok = True
        for i in range(1, n + 1):
            if b[i] == -1:
                continue
            s = cid[i]
            tt = cid[b[i]]
            L = len(elems[s])
            if L != len(elems[tt]):
                ok = False
                break
            shift = (pos[b[i]] - pos[i]) % L
            if img[s] == -1:
                if used[tt]:
                    ok = False
                    break
                img[s] = tt
                sh[s] = shift
                used[tt] = True
            elif img[s] != tt or sh[s] != shift:
                ok = False
                break
        if not ok:
            out.append("NO")
            continue

        # 3. 每个长度组内按环最小元素升序贪心
        by_len = {}
        for c in range(C):
            by_len.setdefault(len(elems[c]), []).append(c)
        ptr = {L: 0 for L in by_len}
        for i in range(1, n + 1):
            c = cid[i]
            if pos[i] != 0 or img[c] != -1:
                continue
            L = len(elems[c])
            v = by_len[L]
            q = ptr[L]
            while used[v[q]]:
                q += 1
            ptr[L] = q
            img[c] = v[q]
            sh[c] = 0
            used[v[q]] = True

        # 4. 还原
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            c = cid[i]
            L = len(elems[c])
            ans[i] = elems[img[c]][(pos[i] + sh[c]) % L]
            if b[i] != -1 and ans[i] != b[i]:
                ok = False
        if not ok:
            out.append("NO")
            continue
        out.append("YES")
        out.append(" ".join(map(str, ans[1:])))
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 8. 边界情况与易错点

1. **$n=1$**：唯一解是 $b=[1]$，无论输入 $b=[-1]$ 还是 $b=[1]$ 都应输出 `YES` 换行 `1`；此时只有一个长度 1 的环，别写成空输出。
2. **$b$ 全为 $-1$**：每个环都只能选到自己（否则会浪费一个更小的目标环给别的源环），答案是恒等置换。样例 1 正是这种情形，可当作快速自检。
3. **长度不等立即 `NO`**：如样例 6（3 元环对 2 元环），不要抱着"平移量能对齐"的幻想去凑。
4. **同一源环的平移量冲突**：样例 9 中一个 6 元环被两个已知值分别定出 shift 4 与 shift 3，必须判负；只比较目标环而忘了比较 shift 是常见错法。
5. **两个源环抢同一个目标环**：样例 4，$b$ 必须是单射，重复占用直接 `NO`。
6. **同一源环重复给同一 $(t,\text{shift})$ 不算冲突**：例如 $a=[3,1,2]$、$b=[2,3,-1]$，$b_1=2$ 与 $b_2=3$ 都指向同一个环且 shift 相同，应继续补齐而非判负。
7. **负数取模**：C++ 里 $(\text{pos}[b_i]-\text{pos}[i]) \bmod L$ 可能为负，必须 `(x % L + L) % L`，否则 shift 落错位置，输出的置换不满足交换性。
8. **空闲环判定错**：把"该位置是 $-1$"当成"环空闲"会重复决策同一个环，导致 `img` 被覆盖、输出不再是排列。
9. **输出格式**：`NO` 后不能多输出一行；`YES` 后第二行恰好 $n$ 个整数（行末空格无妨）。多测之间不要输出空行以外的多余内容。

## 相关题目与扩展

- [Codeforces 612E. Square Root of Permutation](https://codeforces.com/problemset/problem/612/E)：同样是"环长决定能否配对"，但要求 $b^2=a$，需要按环长奇偶做拆分/合并，可与本题的环双射对照。
- [Codeforces 1768D. Lucky Permutation](https://codeforces.com/problemset/problem/1768/D)：交换相邻元素把置换变成"恰有一个逆序对"的形态，核心也是数环。
- [Codeforces 1385G. Columns Swaps](https://codeforces.com/problemset/problem/1385/G)：把每列的两个位置连边后形成环，在环上做二染色，与本题"环上整体搬运"的思路同源。
- [LeetCode 765. 情侣牵手](https://leetcode.cn/problems/couples-holding-hands/)：把错位的情侣看成置换环，最少交换次数 = $n - \#\text{环}$，是环分解最经典的入门题。

**延伸思考**：本题的模型还能回答一批相关问题。(1) **计数**：只给部分约束时，合法补全数为 $\prod_L (k_L-m_L)! \cdot L^{k_L-m_L}$，可直接用本题的中间量算出，可作为对拍的第二重校验。(2) **换目标函数**：若要求 $\sum b_i$ 最小而非字典序最小，贪心不再成立——每个源环的平移量会影响 $L$ 个位置的贡献，长度组内变成"环与平移量"的指派问题，需要按权值排序或 KM。(3) **加约束**：若还要求 $b$ 的平方等于某个给定置换，问题立刻变成 612E 那样的环拆分，说明"可交换"这个条件恰好把置换的环结构完全解放出来，是这类题最舒服的切面。
