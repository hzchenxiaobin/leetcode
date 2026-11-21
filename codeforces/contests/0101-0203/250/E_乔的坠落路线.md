# Codeforces 250E 乔的坠落路线 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/250/E
- **比赛来源**：CROC-MBTU 2012, Final Round (Online version, Div. 2) · Problem E（UTC 2012-11-26）
- **难度**：2000
- **标签**：模拟、按段跳跃、预处理
- **评测类型**：普通
- **限制**：时间 1 s / 内存 256 MB

**题意**：房子有 $n$ 层，每层是一条长 $m$ 的格子带，格子是三种之一：空（`.`）、砖（`+`）、混凝土墙（`#`）。每层左右两端都是墙（越界即撞墙）。

Joe 站在第 $n$ 层（最上层）第 1 格，视线朝右。每一秒他执行：

- 若**正下方**的格子是空的，他就往下掉一层（列不变、朝向不变）；
- 否则看视线方向的下一格：
  - 若为空，就走过去；
  - 若是砖，用额头撞碎它（该格变空），并**转身**；
  - 若是混凝土墙，直接**转身**（墙撞不坏）。

到达第 1 层的任意格子即"冷静下来"。求总秒数；若永远到不了，输出 `Never`。

**约束**：

- $2 \le n \le 100$、$1 \le m \le 10^4$：格子总数 $10^6$，**逐格模拟在此不可行**（见下）。
- 保证第 $n$ 层的第 1 格是空的。
- 答案可以很大：每层来回扫荡的开销是 $O(m^2)$，总答案可达 $10^{10}$ 量级，**必须用 64 位整数**。
- 输入的第 $i$ 行是第 $n-i+1$ 层，也就是**最上层最先给出**。

## 2. 示例与观察

官方样例 1：

```text
输入：
3 5
..+.#
#+..+
+.#+.

输出：
14
```

官方样例 2：

```text
输入：
4 10
...+.##+.+
+#++..+++#
++.#++++..
.+##.++#.+

输出：
42
```

官方样例 3：

```text
输入：
2 2
..
++

输出：
Never
```

**样例 1 的演算**：三层分别是（从上到下）`..+.#`、`#+..+`、`+.#+.`。Joe 从第 3 层第 1 格出发：

| 层 | 该层内的动作序列（简写） | 耗时 | 落点 |
|----|--------------------------|------|------|
| 3 | 走到第 2 格 → 撞碎第 3 格的砖并转身 → 回到第 1 格撞左墙 → 再右扫到第 3 格，脚下（第 2 层第 3 格）为空 → 掉下 | 7 s | 第 2 层第 3 列 |
| 2 | 右扫到第 4 格 → 撞碎第 5 格的砖并转身 → 左扫撞碎第 2 格的砖 → 再右扫到第 5 格，脚下（第 1 层第 5 格）为空 → 掉下 | 7 s | 第 1 层第 5 列 |
| 1 | 已到达，结束 | 0 s | — |

合计 $7 + 7 = 14$，与输出一致。

**样例 3**：两层都是 `..` 与 `++`。Joe 在第 2 层来回走，脚下永远是砖（`+`），既掉不下去、又没有砖可以撞碎，于是永远打转 → `Never`。

**观察 1**：Joe 在某一层上反复来回，**已走过的格子始终是一段连续区间** $[l, r]$。原因是他只会往相邻格移动，破砖和撞墙都不改变位置。

**观察 2**：他每撞碎一块砖或撞一次墙就转身，于是"一次方向不变的行进"就是一次从区间一端扫到某个障碍的过程。第 $k$ 次扫荡时，新区间只会把 $[l,r]$ 往两侧扩张。

**观察 3**：既然已访问的区间内所有格子的"下方"都已经被检查过（且当时都不为空，否则他早就掉下去了），那么**只需要检查新扩张出来的那一段里有没有"下方为空"的格子**，第一个遇到的就是落点。

**观察 4**：如果某一层的左右两侧都被墙挡死、砖也全撞完了，他就在区间里无限来回 → 整题输出 `Never`。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

最直白的做法是逐秒模拟：每一秒按规则改状态、时间加一。单步是 $O(1)$，但时间上限是多少？关键是最坏情况下每层要来回走很多趟：砖一块一块被撞碎，每撞碎一块就要走到另一端再走回来，单趟 $O(m)$，每层砖数 $O(m)$，所以每层 $O(m^2) = 10^8$，$n = 100$ 层就是 $10^{10}$ 秒。样例 2 之外的强数据能轻易构造出 $10^9$ 量级的答案（本实现实测的极端数据答案是 $9.8 \times 10^9$），逐秒模拟必然超时。

所以必须**按"扫荡"跳跃**：一次扫荡只处理一个障碍，把中间的移动距离直接用减法算出来。

### 3.2 核心观察：区间不变式与"只查新格子"

![一层之内：已走过的格子永远是一段区间](../../../images/cf250e_sweep.svg)

设 Joe 当前在第 $f$ 层、第 $p$ 列、朝向 $d$，已经走过的区间是 $[l, r]$（$l \le p \le r$），并且**这整段区间内所有格子的正下方都不为空**（否则他早就掉下去了）。

下一段行进的方向是 $d$：

- 若 $d$ 向右，沿路一直向右能找到第一个"非空格"位置 $o$：它要么是砖（撞碎、花 1 秒、转身），要么是墙或边界（撞墙、花 1 秒、转身）。中间 $r+1 \ldots o-1$ 全是空格，构成**新扩张段**。
- 在扩张段里，他依次踩过 $r+1, r+2, \ldots, o-1$。踩到某一格 $q$ 后，下一秒会检查它下方：若为空就掉下去。所以落点是扩张段里**第一个"下方为空"的格子**。
- 若扩张段里没有这样的格子，就把区间扩到 $o-1$，再花 1 秒处理障碍 $o$（碎砖后它还留在原地，下一次扫荡才会被踩到）。

于是每层只需要：

- 预处理"每个位置向右/向左最近的、下方为空的列"（$O(m)$）；
- 预处理"本层 $p$ 两侧的墙位置、砖的位置表"（$O(m)$）；
- 每次扫荡用二分或指针取出"下一个障碍"，$O(1)$ 完成落点判定与距离累加。

每层扫荡次数 $=$ 砖数 $+2 \le m+2$，所以每层总代价 $O(m)$，整体 $O(nm)$。

### 3.3 算法流程

1. 按题面把输入的第 $i$ 行存为第 $n-i+1$ 层；
2. 令 `f = n`、`p = 0`（0 基列）、`d = 1`、`total = 0`；
3. 若 `f == 1` 结束；若第 $f-1$ 层在 $p$ 处是空格，则 `total++`、`f--`，回到 3；
4. 否则在本层上做 3.2 的扫荡：
   - 维护已走区间 `[cl, cr]`、两侧的砖表指针、两侧是否已被墙封死；
   - 每次扫荡：取下一障碍 $o$，在新区间里找第一个"下方为空"的格子 $q$：
     - 找到 → `total += (到 q 的步数) + 1`，落点更新为 $q$，跳 3；
     - 找不到 → 累加移动距离、处理障碍（+1 秒）、转身；若两侧都已封死且砖用完 → 输出 `Never`；
5. 掉到第 $f-1$ 层的同一列、朝向不变，回到 3。

### 3.4 样例走查

![样例走查：第 3 层 7 秒、第 2 层 7 秒](../../../images/cf250e_walk.svg)

第 3 层 `..+.#`（下标 0..4），Joe 在 0 号格朝右：

| 扫荡 | 障碍 $o$ | 扩张段 | 段内有"下方为空"吗 | 动作与耗时 |
|------|-----------|--------|----------------------|--------------|
| 1 | 砖 @2 | $\{1\}$ | 第 2 层 1 号格是 `+`，否 | 走 1 步、撞碎 2 号砖并转身，累计 2 s |
| 2 | 墙 @-1 | 空 | — | 向左走到 0 号格（1 s）、撞墙转身（1 s），累计 4 s |
| 3 | 墙 @4（`#`）| $\{2, 3\}$ | 第 2 层 2 号格是 `.` | 走到 2 号格即掉下：$2$ 步移动 $+1$ 秒下落，累计 7 s |

第 2 层 `#+..+`，Joe 在 2 号格朝右：先撞碎 4 号砖（走到 3 号 + 撞砖，2 s），回扫撞碎 1 号砖（走到 2 号 + 撞砖，2 s），再右扫到 4 号格时发现第 1 层 4 号格是 `.`，掉下（$2$ 步移动 $+1$ 秒下落，共 3 s），累计 $7 + 7 = 14$ ✓。

## 4. 正确性证明

把"Joe 在某层的运动"拆成若干次**扫荡**：每次扫荡是从当前列出发、方向不变地连续移动，直到撞碎一块砖或撞一次墙为止。

**引理 1（区间不变式）**：在任一层上，任一时刻已踩过的格子集合是一个区间 $[l,r]$，且这些格子当前都是空格、其正下方都不是空的。

**证明**：Joe 只移动到相邻格，所以"踩过的集合"始终连通，即区间。区间内格子被踩过时按规则必须是空格（否则会撞碎或撞墙，而不会进入）；被踩过之后它仍然是空格（撞碎砖会让它变空，且此后不会再变回砖）。至于"下方为空则掉下去"：每次踩到新格子，下一秒就会检查它下方，若为空则已经掉到下一层去了，因此留在本层的区间里所有格子的下方都不为空。∎

**引理 2（扫荡的正确性）**：设当前区间为 $[l,r]$、位置 $p$、朝向向右。令 $o$ 为 $r+1$ 之后第一个非空格（可能是砖、混凝土，或越界），则：

1. 这一趟行进依次踩过 $r+1, r+2, \ldots, o-1$，随后处理 $o$（碎砖或撞墙）并转身；
2. 若扩张段 $[r+1, o-1]$ 中存在"下方为空"的格子，则 Joe 会在其中**第一个**这样的格子处掉到下一层；否则他不会掉下去。

**证明**：由引理 1，$[l,r]$ 内的格子下方都不空，所以行进途中的检查只可能在新格子上触发。Joe 沿方向逐格前进，直到下一格是砖或墙才停止，所以踩过的正是 $r+1 \ldots o-1$，且顺序递增。到达 $o-1$ 后，下一格是 $o$：若 $o$ 是砖则碎砖转身（砖被清除，位置不变），若是墙或越界则撞墙转身。每个新格子的"下方检查"在踩到它的下一秒进行，所以第一个下方为空的格子就是落点。∎

**引理 3（终止与 `Never`）**：若某一层的左右两侧都已被混凝土墙封死（或到达边界）且所有可达的砖都已撞碎，则 Joe 永远不会离开该层，答案应为 `Never`；否则他一定会在有限次扫荡内掉到下一层。

**证明**：当两侧封死且无砖可撞时，他的行进被完全限制在区间 $[l,r]$ 内，且每次扫荡都只是从一端走到另一端再转身——状态（位置、朝向）至多 $2(r-l+1)$ 种，必然循环，永不掉落。反之，只要还有砖或未封死的边界，每次扫荡要么撞碎一块新砖、要么让一侧封死，两者都只能发生有限次；而每层砖数有限，所以扫荡次数有限。有限次扫荡之后，要么在扩张段里找到"下方为空"的格子（掉落），要么两侧封死（`Never`）。∎

**定理**：算法输出的总秒数等于 Joe 走到第 1 层所需的秒数；若不可能则输出 `Never`。

**证明**：由引理 2，每次扫荡处理的结果（移动距离、碎砖/撞墙、是否掉落、落点）与逐秒模拟完全一致，因此每层累计的耗时也一致；由引理 3，`Never` 的判定与逐秒模拟的无限循环对应。各层依次处理，总时间相加即答案。∎

## 5. 复杂度分析

- **时间**：$O(nm)$。每层预处理"最近的下方空格"与障碍位置 $O(m)$，扫荡次数不超过"砖数 $+2$"，每次 $O(1)$。$n \le 100$、$m \le 10^4$ 时约 $10^6$ 次操作。
- **空间**：$O(nm)$ 存输入（约 1 MB）加 $O(m)$ 的辅助数组。
- **与时限的关系**：时限 1 s。极端数据（每层只有一个"下方为空"的格子、且与进入列在两端，逼出 $9.8 \times 10^9$ 的答案）实测端到端 **11.6 ms**；Python 版同数据约 680 ms。
- **数值范围**：答案可达 $10^{10}$ 以上，必须 `long long`；但 `long long` 远远够用。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

static int n, m;
static vector<string> row;   // row[f] = 第 f 层的字符串（1 基）

int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    row.assign(n + 1, string());
    for (int i = 0; i < n; i++) {
        char buf[10005];
        scanf("%s", buf);
        row[n - i] = string(buf, m);       // 第 i 行是第 n-i 层
    }

    long long total = 0;
    int f = n, pos = 0, dir = 1;
    vector<int> nxtE(m + 1), prvE(m + 1);
    while (true) {
        const string &s = row[f];
        if (f == 1) { printf("%lld\n", total); return 0; }
        const string &bel = row[f - 1];
        if (bel[pos] == '.') {             // 脚下是空的，直接掉下去
            total += 1;
            f -= 1;
            if (f == 1) { printf("%lld\n", total); return 0; }
            continue;
        }
        // 每层（只在第一次进入时）预处理：下方是否空 / 障碍位置
        nxtE[m] = m;
        for (int i = m - 1; i >= 0; i--) nxtE[i] = (bel[i] == '.') ? i : nxtE[i + 1];
        prvE[0] = (bel[0] == '.') ? 0 : -1;
        for (int i = 1; i < m; i++) prvE[i] = (bel[i] == '.') ? i : prvE[i - 1];

        int rightStop = m;
        for (int i = pos + 1; i < m; i++) if (s[i] == '#') { rightStop = i; break; }
        int leftStop = -1;
        for (int i = pos - 1; i >= 0; i--) if (s[i] == '#') { leftStop = i; break; }
        vector<int> brR, brL;
        for (int i = pos + 1; i < rightStop; i++) if (s[i] == '+') brR.push_back(i);
        for (int i = pos - 1; i > leftStop; i--) if (s[i] == '+') brL.push_back(i);

        int curL = pos, curR = pos, iR = 0, iL = 0;
        bool deadR = false, deadL = false;
        long long cost = 0;
        bool fell = false;
        int fallCol = -1;
        while (true) {
            if (dir == 1) {
                if (!deadR) {
                    int obst = (iR < (int)brR.size()) ? brR[iR] : rightStop;
                    int firstNew = curR + 1, lastNew = obst - 1;
                    if (firstNew <= lastNew) {
                        int q = nxtE[firstNew];
                        if (q <= lastNew) {                       // 新格子里第一个"下方为空"的
                            cost += (q - pos) + 1;
                            fallCol = q;
                            fell = true;
                            break;
                        }
                    }
                    cost += (obst - 1 - pos);
                    pos = obst - 1;
                    curR = obst - 1;
                    cost += 1;                                    // 撞砖或撞墙，都要花 1 秒转身
                    if (iR < (int)brR.size() && obst == brR[iR]) iR++;
                    else deadR = true;
                    dir = -1;
                } else {
                    cost += (curR - pos);
                    pos = curR;
                    cost += 1;
                    dir = -1;
                }
            } else {
                if (!deadL) {
                    int obst = (iL < (int)brL.size()) ? brL[iL] : leftStop;
                    int firstNew = obst + 1, lastNew = curL - 1;
                    if (firstNew <= lastNew) {
                        int q = prvE[lastNew];
                        if (q >= firstNew) {
                            cost += (pos - q) + 1;
                            fallCol = q;
                            fell = true;
                            break;
                        }
                    }
                    cost += (pos - (obst + 1));
                    pos = obst + 1;
                    curL = obst + 1;
                    cost += 1;
                    if (iL < (int)brL.size() && obst == brL[iL]) iL++;
                    else deadL = true;
                    dir = 1;
                } else {
                    cost += (pos - curL);
                    pos = curL;
                    cost += 1;
                    dir = 1;
                }
            }
            if (deadR && deadL) { printf("Never\n"); return 0; }
        }
        if (fell) {
            total += cost;
            f -= 1;
            pos = fallCol;                 // 掉到下一层同一列，朝向不变
            if (f == 1) { printf("%lld\n", total); return 0; }
        }
    }
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n, m = int(data[0]), int(data[1])
    row = [""] * (n + 1)
    for i in range(n):
        row[n - i] = data[2 + i].decode()      # 第 i 行（0 基）是第 n-i 层

    total = 0
    f, pos, dir_ = n, 0, 1
    while True:
        if f == 1:
            sys.stdout.write(str(total) + "\n")
            return
        s = row[f]
        bel = row[f - 1]
        if bel[pos] == '.':                    # 脚下是空的
            total += 1
            f -= 1
            if f == 1:
                sys.stdout.write(str(total) + "\n")
                return
            continue

        # 预处理：每个位置向右/向左最近的"下方为空"的列
        nxt_e = [m] * (m + 1)
        for i in range(m - 1, -1, -1):
            nxt_e[i] = i if bel[i] == '.' else nxt_e[i + 1]
        prv_e = [-1] * m
        for i in range(m):
            prv_e[i] = i if bel[i] == '.' else (prv_e[i - 1] if i else -1)

        right_stop = m
        for i in range(pos + 1, m):
            if s[i] == '#':
                right_stop = i
                break
        left_stop = -1
        for i in range(pos - 1, -1, -1):
            if s[i] == '#':
                left_stop = i
                break
        br_r = [i for i in range(pos + 1, right_stop) if s[i] == '+']
        br_l = [i for i in range(pos - 1, left_stop, -1) if s[i] == '+']

        cur_l = cur_r = pos
        i_r = i_l = 0
        dead_r = dead_l = False
        cost = 0
        fell = False
        fall_col = -1
        while True:
            if dir_ == 1:
                if not dead_r:
                    obst = br_r[i_r] if i_r < len(br_r) else right_stop
                    first_new, last_new = cur_r + 1, obst - 1
                    if first_new <= last_new:
                        q = nxt_e[first_new]
                        if q <= last_new:
                            cost += (q - pos) + 1
                            fall_col = q
                            fell = True
                            break
                    cost += obst - 1 - pos
                    pos = obst - 1
                    cur_r = obst - 1
                    cost += 1                    # 撞砖 / 撞墙都要一秒转身
                    if i_r < len(br_r) and obst == br_r[i_r]:
                        i_r += 1
                    else:
                        dead_r = True
                    dir_ = -1
                else:
                    cost += cur_r - pos
                    pos = cur_r
                    cost += 1
                    dir_ = -1
            else:
                if not dead_l:
                    obst = br_l[i_l] if i_l < len(br_l) else left_stop
                    first_new, last_new = obst + 1, cur_l - 1
                    if first_new <= last_new:
                        q = prv_e[last_new]
                        if q >= first_new:
                            cost += (pos - q) + 1
                            fall_col = q
                            fell = True
                            break
                    cost += pos - (obst + 1)
                    pos = obst + 1
                    cur_l = obst + 1
                    cost += 1
                    if i_l < len(br_l) and obst == br_l[i_l]:
                        i_l += 1
                    else:
                        dead_l = True
                    dir_ = 1
                else:
                    cost += pos - cur_l
                    pos = cur_l
                    cost += 1
                    dir_ = 1
            if dead_r and dead_l:
                sys.stdout.write("Never\n")
                return
        if fell:
            total += cost
            f -= 1
            pos = fall_col
            if f == 1:
                sys.stdout.write(str(total) + "\n")
                return


main()
```

Python 版逻辑一致，最坏数据约 680 ms；对 1 s 的时限余量不大，**建议优先提交 C++ / PyPy3**。

## 7. 边界情况与易错点

1. **输入行序**：第 $i$ 行是第 $n-i+1$ 层（最上层在前）。存反了会让整个模拟从最底层开始，答案完全错。
2. **`#` 与 `+` 的区别**：撞 `#` 只转身，撞 `+` 会把它变空。实现里必须把"撞碎的砖"当成后续可通过的空格，否则会重复计算。
3. **越界即墙**：每层左右两端都视为混凝土墙。`o = -1`（左越界）与 `o = m`（右越界）都要按"撞墙、花 1 秒、转身"处理。
4. **落点判定必须先于撞砖**：扩张段里的格子是"踩上去 → 下一秒检查下方"，而障碍格（砖）是"不踩、直接撞碎"。混淆这两者会导致漏掉落点或多算一步。
5. **`Never` 的判定条件**：必须同时满足"两侧都被墙封死"且"没有剩余可撞的砖"。只看一侧或只看砖都会把"还能继续扩展"的层误判成死循环。
6. **方向在掉落时保持**：题面明确"掉下去时视线方向不变"，所以 `p` 更新、`d` 不变；这一点在样例 1 的第 2 层会直接影响后续扫荡方向。
7. **`long long`**：答案是秒数，量级 $10^{10}$，`int` 会溢出；本实现用 `long long` 累加。
8. **$m = 1$**：单格层。若脚下为空就掉，否则左右都是墙，永远打转（除非有砖可撞——单格里不可能有砖，因为 Joe 站的那格必须是空的）。代码中"扩张段为空 + 两侧墙"会正确给出 `Never`。
9. **某层一开始就往下方看**：进入一层的第一个动作就是检查脚下，而不是先走一格。所以"掉落"在代码里是每层入口处的第一件事。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2 -Wall`（配合 `codeforces/tools/include` 兼容头，可原样提交 GNU C++17）；Python 3.9.6。
- **官方样例**：3 / 3 通过（→ 14、42、`Never`），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版**逐秒**按题面规则模拟（每步 $O(1)$，并在超过步数上限时判定为 `Never`），与参考实现的"扫荡跳跃"完全独立。随机 1600 组（$n \le 6$、$m \le 9$，字符集包含 `.`/`+`/`#` 的不同混合比例，并强制第 $n$ 层首格为空），**1600 / 1600 全部一致**，其中约 870 组是 `Never`、其余答案最大 71。
- **最大约束性能**：$n = 100$、$m = 10^4$，构造"每层只有一个下方为空的格子、且与进入列分居两端"的极端数据，答案为 $9800000098$，7 次取最小 C++ 端到端 **11.6 ms**、Python 约 680 ms（均含进程启动），远低于 1 s。
- **图片校验**：两张 SVG（`cf250e_sweep.svg`、`cf250e_walk.svg`）通过 `ElementTree.parse`，含 `feTurbulence` 与手写字体。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 250A Paper Work](https://codeforces.com/problemset/problem/250/A)：同场 A 题，简单的贪心分组。
- [Codeforces 250C Movie Critics](https://codeforces.com/problemset/problem/250/C)：同场 C 题，同样是"按段压缩模拟"的思路。
- [Codeforces 119A Epic Game](https://codeforces.com/problemset/problem/119/A)：另一道纯模拟题，可作为本题的入门对照。
- [LeetCode 874. 模拟行走机器人](https://leetcode.cn/problems/walking-robot-simulation/)：网格上的行走模拟 + 障碍集合，与本题"撞到障碍改变状态"的骨架相似。

**延伸思考**：

1. **如果砖撞碎后仍然算障碍**（不可通过）：那就不存在"扩张区间"，每层的行进会退化成"在两个砖之间来回"，可以直接算出总步数或立刻判定死循环，难度反而降低。
2. **如果允许向上走**：楼层不再是单向的，需要把 $n \times m$ 的格子建成图做 BFS/最短路，本解法的"逐层"结构失效。
3. **如果要求输出落点序列**：本实现已经记录了每次掉落的列，直接在扫荡结束时追加即可，不影响复杂度。
4. **如果 $m$ 放大到 $10^5$、$n$ 放大到 $10^4$**：$O(nm)$ 会到 $10^9$；此时需要利用"每层只有第一个下方空格重要"的结构，把每层压缩成若干个关键位置，用二分/倍增跳转，把单层代价降到 $O(\log m)$。

