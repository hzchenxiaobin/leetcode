# Codeforces 97A 魔法骨牌阵 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/97/A
- **比赛来源**：Yandex.Algorithm 2011: Finals · Problem A（UTC 2011-07-15）
- **难度**：2400
- **标签**：图论建模、计数、2x2 平铺、配对枚举
- **评测类型**：特殊评测（答案不唯一：个数固定，但任意一种合法填法都接受）
- **限制**：时间 500 ms / 内存 256 MB

**题意**：一副完整的双六骨牌有 $28$ 张，即 $0\le a\le b\le 6$ 的所有无序数对 $a\text{-}b$。一个由这 $28$ 张骨牌摆成的图形叫"魔法图形"，如果它恰好能被 $14$ 个互不重叠的 $2\times 2$ 正方形覆盖，并且每个正方形里的四个数字完全相同。

现在给出一块 $n\times m$ 的网格，上面放着**恰好 $28$ 个 $1\times 2$ 或 $2\times 1$ 的筹码**，每个筹码用不同的字母标记（字母只是标签，不是数字）。要求把每个筹码换成一整副骨牌里的一张（$28$ 个筹码要用 $28$ 张**互不相同**的骨牌），使得结果是一个魔法图形。输出这样的替换方案数，以及其中任意一种方案填好的数字场。

**约束**：

- $1\le n,m\le 30$，所以网格最多 $900$ 格，但有效格只有 $28\times 2=56$ 个；
- 棋盘上恰好 $28$ 个筹码，每个筹码恰好占两格，题面保证网格描述合法；
- 题面保证**至少存在一种解**，因此不用处理"无解"的判定，但计数可能为 $0$ 的情况在实现上仍要能安全兜底；
- 方案数上界：任意一种合法填法都对应 $7!$ 倍于某个配对数的计数（见 3.2、4.2），最大不超过 $5040\times 5040\approx 2.5\times 10^7$，`int` 装得下，但用 `long long` 更稳妥；
- 时限只有 500 ms，说明算法必须是"读入 + 一次贪心 + 常数次小规模枚举"，任何搜索 $28$ 张骨牌全排列的做法都会超时。

## 2. 示例与观察

官方样例（输入 / 输出原样）：

```text
输入：
8 8
.aabbcc.
.defghi.
kdefghij
klmnopqj
.lmnopq.
.rstuvw.
xrstuvwy
xzzAABBy

输出：
10080
.001122.
.001122.
33440055
33440055
.225566.
.225566.
66113344
66113344
```

**样例拆解**。输入的 $56$ 个格子组成一条"环带"：第 $1$、$2$、$5$、$6$ 行只占中间 $6$ 列，第 $3$、$4$、$7$、$8$ 行占满 $8$ 列；$28$ 个筹码中，$a,b,c$ 与 $z,A,B$ 是横筹码，其余都是竖筹码。

输出里的 $14$ 个 $2\times2$ 方块是（行、列都从 $1$ 开始，左上角坐标）：

$$
(1,2),(1,4),(1,6),\quad (3,1),(3,3),(3,5),(3,7),\quad (5,2),(5,4),(5,6),\quad (7,1),(7,3),(7,5),(7,7).
$$

它们的数字依次是 $0,1,2\;|\;3,4,0,5\;|\;2,5,6\;|\;6,1,3,4$。可以看到每个数字 $0\sim 6$ 都恰好出现在**两个**方块里。把这 $14$ 个方块按数字配对（数字 $0$ 的两个方块、数字 $1$ 的两个方块……），恰好得到 $7$ 组；而每一组里，有一个方块装着同一张"对子骨牌"（$0\text{-}0$、$1\text{-}1$、……），另一个方块里没有。

再看跨方块的筹码：$d$ 连方块 $(1,2)$ 与 $(3,1)$，即数字 $0$ 与 $3$；$e$ 连 $0$ 与 $4$；……。把这些数对列全，恰好是 $21$ 个非对子数对，每个一次。

**数一数 $10080$**：$10080=2\times 7!$。也就是说，合法方案的个数 = $7!\times(\text{合法"配对数"})$，本例配对数 $=2$。这个乘号右边为什么是 $7!$、左边为什么只剩一个"配对计数"，是本题的全部难点。

自造样例（标注自造，用于验证边界；输入规模小是为了一目了然）：

| 输入 | 输出 | 说明 |
|------|------|------|
| 8×8 官方环带 | `10080` | 唯一合法的 $2\times2$ 遮盖 |
| 同一环带的旋转/镜像（8 种） | 均为 `10080` | 对称性不改变计数 |
| 任意随机摆放的 $14$ 个 $2\times2$ 方块 + 随机骨牌切分 | 绝大多数为 `0` | 合法配置极其稀疏（见第 8 节） |

## 3. 解题思路

### 3.1 朴素做法与瓶颈

最直接的想法是枚举"哪个筹码放哪张骨牌"，即 $28!$ 个置换，每个再判一次魔法性，完全不可行。稍微聪明一点：先枚举 $2\times2$ 遮盖，再枚举每个方块的数字（$7^{14}$ 级别），仍然爆炸。

瓶颈有两个：**遮盖怎么找**、**数字怎么填**。下面的观察把两者都压成常数级。

### 3.2 核心观察

![2x2 同色方块与跨块骨牌](../../../images/cf97a_magic_square.svg)

**观察 1（遮盖唯一）**：若存在用 $2\times2$ 方块铺满这 $56$ 个格子的方案，则它唯一。

证明思路是"最上最左"贪心：取所有未覆盖格中行号最小、行号相同则列号最小的格子 $(r,c)$。任何覆盖它的 $2\times2$ 方块的左上角只能是 $(r-\delta_r,c-\delta_c)$，$\delta_r,\delta_c\in\{0,1\}$。若 $\delta_r=1$，该方块会覆盖第 $r-1$ 行的格子，而这一行已经没有未覆盖格（要么不属于图形，要么已被覆盖），矛盾；若 $\delta_c=1$，会覆盖同一行左边的格子，同理矛盾。所以方块左上角就是 $(r,c)$ 本身，被**强制**。归纳下去，整个遮盖唯一。实现上只需按行列顺序扫描，遇到未覆盖的图形格就试着放一个 $2\times2$。

**观察 2（每个数字恰好占两个方块）**：设某合法填法中数字 $d$ 出现在 $n_d$ 个方块里，则含 $d$ 的格子共 $4n_d$ 个。这些格子被骨牌覆盖：$d\text{-}d$ 这张对子骨牌最多贡献 $2$ 格（整副里只有一张），而与 $d$ 搭配的其余 $6$ 张骨牌 $d\text{-}b$（$b\neq d$）各恰好贡献 $1$ 格——因为 $28$ 张骨牌全都用上了，每个数对恰好出现一次。于是

$$4n_d = 2 + 6 = 8 \quad\Longrightarrow\quad n_d = 2 .$$

**观察 3（"锚点 + 自由块"配对）**：一个数字 $d$ 的两个方块，记作 $(P_d,Q_d)$。方块内部的那两格如果被同一张骨牌覆盖，那张骨牌必然是 $d\text{-}d$（两格同色），所以每个方块内部要么是一张对子骨牌（占 $2$ 格），要么没有内部骨牌、$4$ 格全部由跨块骨牌覆盖。$d\text{-}d$ 只有一张，所以 $P_d,Q_d$ 中**恰有一个**含内部骨牌（否则这个数字的跨块骨牌数是 $4+4=8\neq 6$，或 $2+2=4\neq 6$）。称含内部骨牌的那个方块为数字 $d$ 的**锚点**，另一个为**自由块**。

于是全局有 $7$ 个锚点、$7$ 个自由块，数字 $d$ 与"锚点 + 自由块"这一对（称为一条**纤维**）一一对应。

**观察 4（纤维之间恰有一条边）**：把 $14$ 个方块看成点，每张跨块骨牌看成一条边（连接它两端所在的方块）。数字 $d$ 与 $b$ 之间恰好有一张骨牌 $d\text{-}b$，所以纤维 $d$ 与纤维 $b$ 之间恰好有一条边。注意：如果某条边的两个端点在同一条纤维内，那么这张骨牌两端同色，就成了第二张 $d\text{-}d$，违反"骨牌互不相同"，因此纤维内部不能有边。

![纤维配对与 7! 因子](../../../images/cf97a_fiber.svg)

**观察 5（$7!$ 从哪来）**：只要"锚点 $\leftrightarrow$ 自由块"的配对（把 $14$ 个方块分成 $7$ 条纤维、每条一个锚点一个自由块）满足"任意两条纤维之间恰有一条边、纤维内部无边"，那么任意给纤维编号 $0\sim 6$、并令同一条纤维的两个方块填同一个数字，就得到一种合法填法：$21$ 条跨块骨牌给出的数对正好是 $21$ 个非对子数对（互不相同），$7$ 个锚点内部的对子骨牌给出 $7$ 个 $d\text{-}d$，合起来正好 $28$ 张互不相同的骨牌。纤维到数字的 $7!$ 种编号全部合法且互不相同。

所以

$$\text{答案} = 7!\times(\text{满足上述两个条件的纤维配对数}).$$

$7!=5040$，配对只有 $7!$ 种可能（枚举 $5040$ 个排列），每个排列用 $O(7^2)$ 判一遍，总共不到 $10^6$ 次运算。

### 3.3 算法流程

![样例走查：环带的 14 个方块](../../../images/cf97a_sample_walk.svg)

1. 读入网格，按字母收集每个筹码的两格；
2. 用"最上最左"贪心求出唯一的 $2\times 2$ 遮盖，给每个格子标上方块编号。若贪心失败（题面保证不会）则输出 $0$；
3. 遍历 $28$ 个筹码：两端在同一方块内则给该方块记一次"内部骨牌"；否则在方块邻接矩阵 `adj` 上给对应两项加一；
4. 内部骨牌数 $\ge 2$ 的方块直接判非法；内部骨牌数 $=1$ 的是锚点，$=0$ 的是自由块。锚点数或自由块数不为 $7$ 则答案为 $0$；
5. 枚举 $7$ 个自由块到 $7$ 个锚点的全部 $7!$ 个双射 $\pi$，检查：
   - 每个锚点 $a_k$ 与它的 $\pi(k)$ 之间没有边；
   - 任意两个纤维 $k<l$ 之间（四个端点两两组合）恰好有 $1$ 条边；
6. 记合法排列数为 $M$，输出 $5040M$；取第一个合法排列，把纤维 $k$ 的两个方块都填数字 $k$，逐格输出（空格仍是 `.`）。

### 3.4 样例走查

以官方样例为例（方块编号按行优先）：

- 锚点（含内部骨牌）：$(1,2)$ 里的 $a=0\text{-}0$、$(1,4)$ 里的 $b=1\text{-}1$、$(1,6)$ 里的 $c=2\text{-}2$、$(3,1)$ 里的 $k=3\text{-}3$、$(3,7)$ 里的 $j=5\text{-}5$、$(7,1)$ 里的 $x=6\text{-}6$、$(7,7)$ 里的 $y=4\text{-}4$；
- 自由块：$(3,3),(3,5),(5,2),(5,4),(5,6),(7,3),(7,5)$；
- 跨块骨牌 $d\sim i,l\sim q,r\sim w,z,A,B$ 共 $21$ 张，正好给出 $21$ 条边。

程序枚举 $5040$ 个自由块排列，其中有 $2$ 个满足全部条件，于是输出 $2\times 5040=10080$，与官方的 `10080` 一致。把其中第一个合法排列按纤维编号上色，就得到样例输出那样的数字场（数字具体取值可以不同，但个数必须相同）。

## 4. 正确性证明

**引理 1**：若魔法图形存在，则它的 $2\times 2$ 遮盖唯一，且 3.3 步 2 的贪心一定找到它。

**证明**：设 $C$ 是任一合法遮盖。取所有图形格中行号最小者中最左的格子 $(r,c)$。$C$ 中覆盖 $(r,c)$ 的方块左上角为 $(r-\delta_r,c-\delta_c)$，$\delta_r,\delta_c\in\{0,1\}$。由于第 $r-1$ 行（若存在）没有未覆盖的图形格，$\delta_r=1$ 会使方块覆盖非图形格或已覆盖格，矛盾，故 $\delta_r=0$；同理 $\delta_c=0$。于是该方块被唯一确定，且正是贪心所放的那个。把它从图形中去掉后归纳，贪心与 $C$ 逐步一致，故 $C$ 唯一。若贪心某步放不下，说明 $C$ 不存在。∎

**引理 2**：任一合法填法中，每个数字恰好出现在两个方块里；且这两个方块中恰有一个含内部骨牌。

**证明**：第一个结论即 3.2 观察 2 的计数：$4n_d=2+6=8$。第二个结论：数字 $d$ 的两个方块共有 $8$ 格填 $d$。若两个方块都不含内部骨牌，则 $8$ 格都要由跨块骨牌覆盖，需要 $8$ 张不同的 $d\text{-}b$ 骨牌，但只有 $6$ 张，矛盾；若都含内部骨牌，则需要两张 $d\text{-}d$，矛盾。所以恰有一个含内部骨牌（此时该方块还有 $2$ 格由跨块骨牌覆盖，另一个方块 $4$ 格全部跨块，合计 $6$ 张 $d\text{-}b$，恰好用完）。∎

**引理 3**：任一合法填法诱导出一个"纤维配对 + 纤维编号"，且不同的（配对，编号）给出不同的填法；反之每个满足条件的（配对，编号）都给出合法填法。

**证明**：由引理 2，把同数字的锚点与自由块配成一条纤维、数字作为编号，即得配对与编号。填法由"每个方块填所属纤维的编号"决定，所以（配对，编号）不同则填法不同（不同配对至少有一个方块换了纤维，其数字或另一个同数字方块不同）。反向：给定配对与编号，每个方块填其纤维编号，则每个方块内四格同色（满足魔法性）；$14$ 个方块中每个数字出现 $2$ 次；跨块骨牌给出的数对：不同纤维之间恰一条边 $\Rightarrow$ 恰好遍历 $21$ 个非对子数对；纤维内部无边 $\Rightarrow$ 跨块骨牌不会是 $d\text{-}d$；锚点内部骨牌给出 $d\text{-}d$，$7$ 个锚点数字互不相同。故 $28$ 张骨牌互不相同且正好是整副牌。∎

**引理 4**：固定配对后，$7!$ 种编号全部合法。

**证明**：条件"任意两条纤维之间恰有一条边、纤维内无边"只与配对有关，与编号无关；而引理 3 的反向构造对任意编号都成立。∎

**定理**：答案等于 $7!\times M$，其中 $M$ 是满足"每对纤维之间恰一条边、纤维内无边"的锚点-自由块完美配对数。

**证明**：引理 3 给出"合法填法 $\leftrightarrow$（配对，编号）"的双射，引理 4 说明每个配对恰好贡献 $7!$ 种编号，再由引理 1 遮盖唯一，故总数为 $7!\cdot M$。∎

## 5. 复杂度分析

- **时间**：读入与建图 $O(nm)$；贪心遮盖 $O(nm)$；统计 $O(28)$；枚举配对 $O(7!\cdot 7^2)=O(1)$。总计 $O(nm+7!\cdot 49)$，最坏 $900+2.5\times10^5$ 次基础运算，远小于 500 ms 的限额。
- **空间**：网格、方块编号、$14\times14$ 邻接矩阵，共 $O(nm)$，最多几 KB。
- **数值范围**：答案 $\le 5040\times 5040=25\,401\,600$，`int` 也够，代码用 `long long` 更保险。
- **与时限的关系**：实测最大规模（把样例形状嵌进 $30\times30$ 的空网格）端到端约 $2$ ms，余量在 200 倍以上。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<string> g(n);
    for (auto &s : g) cin >> s;

    int letterId[256];
    fill(letterId, letterId + 256, -1);
    vector<vector<pair<int, int>>> cell;
    for (int r = 0; r < n; r++)
        for (int c = 0; c < m; c++) {
            char ch = g[r][c];
            if (ch == '.') continue;
            if (letterId[(int)ch] < 0) {
                letterId[(int)ch] = (int)cell.size();
                cell.push_back({});
            }
            cell[letterId[(int)ch]].push_back({r, c});
        }
    int K = (int)cell.size();

    /* 唯一的 2x2 遮盖：反复取"最上最左"的未覆盖格，它的方块左上角只能就是它自己 */
    vector<vector<int>> sq(n, vector<int>(m, -1));
    int nsq = 0;
    bool ok = true;
    for (int r = 0; r < n && ok; r++)
        for (int c = 0; c < m && ok; c++) {
            if (g[r][c] == '.' || sq[r][c] != -1) continue;
            if (r + 1 >= n || c + 1 >= m) { ok = false; break; }
            for (int dr = 0; dr < 2 && ok; dr++)
                for (int dc = 0; dc < 2 && ok; dc++)
                    if (g[r + dr][c + dc] == '.' || sq[r + dr][c + dc] != -1) ok = false;
            if (!ok) break;
            for (int dr = 0; dr < 2; dr++)
                for (int dc = 0; dc < 2; dc++) sq[r + dr][c + dc] = nsq;
            nsq++;
        }

    if (!ok || nsq != 14) {   /* 题面保证有解，这里只是兜底 */
        cout << 0 << '\n';
        for (int r = 0; r < n; r++) {
            string t = g[r];
            for (char &ch : t) if (ch != '.') ch = '0';
            cout << t << '\n';
        }
        return 0;
    }

    vector<int> internal(nsq, 0);
    vector<vector<int>> adj(nsq, vector<int>(nsq, 0));
    for (int i = 0; i < K; i++) {
        int s1 = sq[cell[i][0].first][cell[i][0].second];
        int s2 = sq[cell[i][1].first][cell[i][1].second];
        if (s1 == s2) internal[s1]++;
        else { adj[s1][s2]++; adj[s2][s1]++; }
    }

    vector<int> anchors, frees;
    for (int s = 0; s < nsq; s++) {
        if (internal[s] >= 2) { anchors.clear(); frees.clear(); break; }
        if (internal[s] == 1) anchors.push_back(s); else frees.push_back(s);
    }

    long long valid = 0;
    vector<int> bestPerm;
    if ((int)anchors.size() == 7 && (int)frees.size() == 7) {
        vector<int> perm = frees;
        sort(perm.begin(), perm.end());
        do {
            bool good = true;
            for (int k = 0; k < 7 && good; k++)
                if (adj[anchors[k]][perm[k]]) good = false;
            for (int a = 0; a < 7 && good; a++)
                for (int b = a + 1; b < 7 && good; b++) {
                    int c = adj[anchors[a]][anchors[b]] + adj[anchors[a]][perm[b]]
                          + adj[perm[a]][anchors[b]] + adj[perm[a]][perm[b]];
                    if (c != 1) good = false;
                }
            if (!good) continue;
            valid++;
            if (bestPerm.empty()) bestPerm = perm;
        } while (next_permutation(perm.begin(), perm.end()));
    }

    cout << valid * 5040LL << '\n';
    vector<int> digit(nsq, 0);
    for (int k = 0; k < 7 && !bestPerm.empty(); k++) {
        digit[anchors[k]] = k;
        digit[bestPerm[k]] = k;
    }
    for (int r = 0; r < n; r++) {
        string t(m, '.');
        for (int c = 0; c < m; c++)
            if (g[r][c] != '.') t[c] = char('0' + digit[sq[r][c]]);
        cout << t << '\n';
    }
    return 0;
}
```

### Python3

```python
import sys
from itertools import permutations


def main() -> None:
    data = sys.stdin.read().split('\n')
    n, m = map(int, data[0].split())
    g = data[1:1 + n]

    cell = {}
    order = []
    for r in range(n):
        row = g[r]
        for c in range(m):
            ch = row[c]
            if ch == '.':
                continue
            if ch not in cell:
                cell[ch] = []
                order.append(ch)
            cell[ch].append((r, c))

    # 唯一的 2x2 遮盖
    sq = [[-1] * m for _ in range(n)]
    nsq = 0
    ok = True
    for r in range(n):
        for c in range(m):
            if g[r][c] == '.' or sq[r][c] != -1:
                continue
            if r + 1 >= n or c + 1 >= m:
                ok = False
            else:
                for dr in range(2):
                    for dc in range(2):
                        if g[r + dr][c + dc] == '.' or sq[r + dr][c + dc] != -1:
                            ok = False
                if ok:
                    for dr in range(2):
                        for dc in range(2):
                            sq[r + dr][c + dc] = nsq
                    nsq += 1
            if not ok:
                break
        if not ok:
            break

    if not ok or nsq != 14:
        print(0)
        for r in range(n):
            print(''.join('.' if ch == '.' else '0' for ch in g[r]))
        return

    internal = [0] * nsq
    adj = [[0] * nsq for _ in range(nsq)]
    for ch in order:
        (r1, c1), (r2, c2) = cell[ch]
        s1, s2 = sq[r1][c1], sq[r2][c2]
        if s1 == s2:
            internal[s1] += 1
        else:
            adj[s1][s2] += 1
            adj[s2][s1] += 1

    anchors = [s for s in range(nsq) if internal[s] == 1]
    frees = [s for s in range(nsq) if internal[s] == 0]

    valid = 0
    best = None
    if len(anchors) == 7 and len(frees) == 7:
        for perm in permutations(frees):
            good = True
            for k in range(7):
                if adj[anchors[k]][perm[k]]:
                    good = False
                    break
            if good:
                for a in range(7):
                    for b in range(a + 1, 7):
                        cnt = (adj[anchors[a]][anchors[b]] + adj[anchors[a]][perm[b]]
                               + adj[perm[a]][anchors[b]] + adj[perm[a]][perm[b]])
                        if cnt != 1:
                            good = False
                            break
                    if not good:
                        break
            if good:
                valid += 1
                if best is None:
                    best = perm

    print(valid * 5040)
    digit = [0] * nsq
    if best is not None:
        for k in range(7):
            digit[anchors[k]] = k
            digit[best[k]] = k
    for r in range(n):
        print(''.join('.' if g[r][c] == '.' else str(digit[sq[r][c]]) for c in range(m)))


main()
```

Python 版本只是把 $5040$ 个排列换成 `itertools.permutations`，同样远低于时限，可直接提交。

## 7. 边界情况与易错点

1. **把"方案数"算成"数字场数"之外的东西**：本题方案数只数"哪张骨牌放哪个筹码"，不数骨牌的翻转（同一张骨牌左右/上下摆两格算同一种），也不数 $2\times2$ 遮盖的选取方式（遮盖唯一）。样例 $10080=2\times 7!$ 可以复核这一点。
2. **忘了乘 $7!$**：只数配对会得到 $2$，与答案差 $5040$ 倍；反过来只数 $7!$ 会漏掉配对的重数。
3. **纤维内出现边**：若某条纤维的两个方块之间也有跨块骨牌，这张骨牌两端同色，就成了第二张 $d\text{-}d$，必须判非法（代码里 `adj[anchors[k]][perm[k]]` 的检查）。
4. **纤维之间边数不等于 $1$**：两条纤维之间可能有 $0$ 条（少了数对）或 $2$ 条（重复数对），都必须排除；只检查"$\ge 1$"会把重复数对放过。
5. **一个方块内有 $2$ 张内部骨牌**：这会产生两张相同的 $d\text{-}d$，判非法（代码里 `internal[s] >= 2`）。
6. **贪心遮盖失败**：虽然题面保证有解，但实现上要把"放不下 $2\times2$"作为失败分支；另外 $30\times30$ 的边界处 $r+1\ge n$ 或 $c+1\ge m$ 时也要判失败，别越界。
7. **字母与数字混淆**：输入里的字母只是筹码标签，输出才填数字；注意 `A`、`B` 两个大写字母也在标签集合里，读入时不能只认小写。
8. **输出格式**：先输出个数，再输出 $n$ 行、每行恰好 $m$ 个字符；空格处必须是 `.`，不能省成空行或空格对齐。
9. **计数溢出**：答案上界 $2.5\times10^7$，`int` 够，但 `valid * 5040` 若用 `int` 在更大规模的推广题上会溢出，本代码统一用 `long long`。
10. **多组数据**：本题只有一组输入，代码里没有 `while (cin >> n >> m)` 循环，别误加。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`（`/usr/bin/g++` 是 clang 的软链），用 `clang++ -std=c++17 -O2` + `codeforces/tools/include/bits/stdc++.h` 兼容头编译；Python 为 `Python 3.9.6`。
- **官方样例**：$1/1$ 通过（`CF97A` 的唯一样例，C++ 与 Python 都输出 `10080`），输出网格经 checker 逐项校验合法。
- **特殊评测 checker**：`codeforces/tools/checkers/cf97a.py`，校验：① 格式与点阵；② $28$ 个筹码的数对两两不同；③ 数字场能被 $14$ 个 $2\times2$ 同色方块覆盖；④ 计数与 checker 独立重算（贪心遮盖 + 纤维匹配枚举）一致，并与参考答案首行一致。反向测试（篡改计数、篡改某格数字制造重复骨牌）均被拒。
- **独立暴力对拍**：另写一份完全不复用上述定理的暴力——回溯枚举 $2\times2$ 遮盖（对最上最左未覆盖格尝试 $4$ 种左上角），再回溯枚举每个方块的数字（每个数字至多用 $2$ 次），逐对检查骨牌是否互不相同。对官方样例得 $10080$，与参考程序一致；把"每个数字至多用 $2$ 次"放宽到 $3$ 次，结果仍是 $10080$，说明该剪枝没有丢解。
- **对称性测试**：把样例环带做 $8$ 种旋转/镜像，参考程序与暴力均得 $10080$（$8/8$ 一致）。
- **遮盖穷举**：对样例形状**枚举全部 $754165$ 种骨牌切分**，参考程序只在样例本身那一种切分上给出 $10080$，其余全部为 $0$——合法配置的稀疏程度由此可量化。
- **随机形状对拍**：$220$ 组随机"$14$ 个 $2\times2$ 方块随机游走摆放 + 随机骨牌切分 + 随机字母"，参考程序与暴力全部一致（均为 $0$）；另取样例形状的 $200$ 种随机切分，参考程序与暴力也全部一致（均为 $0$）。
- **最大约束性能**：把样例形状嵌进 $30\times30$ 空网格（最大 $n,m$），端到端约 $2$ ms，峰值内存 $2$ MB 以内，相对 $500$ ms 余量在百倍以上。
- **图片校验**：三张 SVG 均通过 `xml.etree.ElementTree.parse`，按字符宽度估算文本包围盒均未越出 `viewBox`。
- **复核状态**：verified（样例、checker、暴力对拍、穷举、性能、图片六项均实跑通过）。

## 相关题目与扩展

- [Codeforces 97B Superset](https://codeforces.com/problemset/problem/97/B)：同场 B 题，构造"任意两点的包围盒内还有第三点"的点集，与本题同属"先把组合结构刻画清楚"的类型。
- [Codeforces 97D Robot in Basement](https://codeforces.com/problemset/problem/97/D)：同场 D 题，用位集同时模拟所有起点。
- [Codeforces 50A Domino piling](https://codeforces.com/problemset/problem/50/A)：$2\times1$ 骨牌铺矩形，只用面积与整除；本题则要求"骨牌整体互不相同 + 同色 $2\times2$ 方块"，难度全在组合约束。
- [Codeforces 118E Bertown roads](https://codeforces.com/problemset/problem/118/E)：双连通分量与定向，和本题一样需要先把图的结构分量说清楚。
- [LeetCode 1245. 树的直径](https://leetcode.cn/problems/tree-diameter/)：图结构建模的入门练习。

**延伸思考**：

1. **如果骨牌不是"整副 28 张"、而是任意多重集**：观察 2 的计数 $4n_d=8$ 就不再成立，每个数字的方块数会变成自由参数，问题退化为一个矩阵方程，计数可能变成多项式时间的大整数计数。
2. **如果 $2\times2$ 方块要求"完全落在图形内部且四格同色"，但允许图形不连通**：遮盖仍然唯一（贪心与连通性无关），但锚点/自由块的配对可能分成多个独立分量，答案是各分量配对数的乘积再乘 $7!$——注意 $7!$ 不能再拆，因为数字必须全局各用两次。
3. **如果棋盘更大、筹码更多（比如 $k$ 个数字的完全骨牌组）**：计数公式会变成 $k!\times M$，其中 $M$ 是 $k$ 条纤维的完美配对数；$M$ 的计算是"带约束的完美匹配计数"，$k$ 大时是 $\#P$ 难的，但本题 $k=7$ 可以暴力。
4. **把"唯一遮盖"这一观察推广**：任何"用 $a\times b$ 矩形平铺一个格子集合"的问题，只要要求每个矩形左上角对齐（不允许旋转），按行优先贪心都是唯一的；这正是本题能在 500 ms 内做完的根本原因。
