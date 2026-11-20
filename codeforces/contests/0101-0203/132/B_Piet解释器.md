# Codeforces 132B Piet 解释器 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/132/B
- **比赛来源**：Codeforces Beta Round 96 (Div. 1) · Problem B（UTC 2011-12-03）
- **难度**：2100
- **标签**：实现、模拟
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：Piet 程序是一张彩色像素图。本题用它的简化版规则：每个像素是 $0..9$ 的数字，`0` 表示黑色；**同色的连通块保证是矩形**（黑块可以是任意形状）。解释器有一个"指令指针"由三部分组成：

- **BP**（block pointer）：当前指向的色块（注意：没有"当前像素"的概念）；
- **DP**（direction pointer）：朝左/右/上/下之一；
- **CP**（chooser pointer）：相对 DP 偏左或偏右 90°。

初始时 BP 指向包含**左上角**的块，DP 向右，CP 向左。每一步：

1. 在当前块中找 **DP 方向上最远的那条边**；
2. 在这条边上找 **CP 方向上最远的像素**；
3. 从该像素朝 DP 方向再走一格：
   - 若落进一个色块，则该块成为新的 BP，DP、CP 都不变；
   - 若落到黑格或界外，BP 不动，但 CP 翻转：CP 原向左则改为向右（DP 不变）；CP 原向右则改为向左，同时 **DP 顺时针旋转 90°**。

给定程序和步数 $n$，问走完 $n$ 步后 BP 指向的块的颜色。

**约束**：

- 棋盘 $m\le50$ 行、每行长度 $\le50$：块数 $\le2500$，像素总数 $\le2500$。
- $n\le5\times10^7$：直接模拟 $5\times10^7$ 步、每步扫描整个块（$\le2500$ 像素）会到 $10^{11}$，必须优化。
- 关键：**IP 的状态是有限的**——(当前块, DP, CP) 只有 $\le2500\times4\times2=20000$ 种，所以过程必然会进入周期。找到周期后把整周期跳过，$O(\text{状态数}\times\text{块大小})$ 即可。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
2 10
12
43

输出：
1
```

四个格子各成一个块：

```text
1 2
4 3
```

初始 BP = 块 1、DP 向右、CP 向左（即 CP 方向 = 逆时针转 90° = 上）。题解把 10 步的变化列了出来：

- **第 1 步**：块 1 只有 $(1,1)$，DP 方向最远边只有它；朝右走一格进入块 2 ⇒ BP = 块 2；
- **第 2、3 步**：块 2 在右边界上，朝右走会出界。两次"碰壁"：第 2 步让 CP 从左翻到右（DP 不变，仍向右）；第 3 步 CP 从右翻到左，同时 DP 顺时针转成向下；
- **第 4 步**：DP 向下走到 $(2,2)$，正是块 3 ⇒ BP = 块 3；
- **第 5、6 步**：块 3 在下边界上，两次碰壁把 DP 顺时针转成向左（CP 也回到左）；
- **第 7 步**：向左走进 $(2,1)$，即块 4 ⇒ BP = 块 4；
- **第 8、9 步**：块 4 在左边界上，两次碰壁把 DP 转成向上；
- **第 10 步**：向上走进 $(1,1)$，回到块 1 ⇒ BP = 块 1。

所以 10 步后是块 1，颜色 1 ✓ 与输出一致。

官方样例 2（输入 / 输出原样）：

```text
输入：
3 12
1423
6624
6625

输出：
6
```

12 步后 BP 落在颜色 6 的块上。

官方样例 3（输入 / 输出原样）：

```text
输入：
5 9
10345
23456
34567
45678
56789

输出：
5
```

![IP 的三部分与「走一步」的规则](../../../images/cf132b_ip.svg)

**观察**：一个色块是矩形，所以"DP 方向上的最远边"就是该矩形对应方向的那条边；再在边上按 CP 方向取最远像素，其实就是取矩形的某个**角**（具体是哪个角由 DP 与 CP 共同决定）。于是"选像素"可以 $O(1)$ 完成，不需要遍历块内所有像素。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

逐步模拟，每步扫描当前块的所有像素找两个方向上的极值。复杂度 $O(n\cdot\text{块大小})$，最坏 $5\times10^7\times2500=1.25\times10^{11}$，不可行。

即使把"找像素"优化到 $O(1)$（利用矩形性质），$5\times10^7$ 步本身在 2 s 内也很勉强（每步有十几次操作）。真正的解法是利用**周期性**。

### 3.2 核心观察：状态有限，过程必然周期

IP 的完整状态是三元组 (BP, DP, CP)：BP 有 $B\le2500$ 种、DP 4 种、CP 2 种，共 $\le20000$ 种。而每一步的转移是**确定性**的（给定状态，下一步唯一确定）。由抽屉原理，从初始状态出发，至多 $20001$ 步就会出现重复状态，此后进入一个长度 $\le20000$ 的循环。

于是：记录每种状态**第一次**被访问时的步号，走到重复状态时，设循环长度为 $c$、当前步号为 $s$，剩下 $n-s$ 步中有 $\lfloor(n-s)/c\rfloor$ 个完整循环可以直接跳过（状态不变），只模拟余下的 $(n-s)\bmod c$ 步。

总步数降到 $O(\text{状态数})=20000$ 量级。

### 3.3 算法流程

1. 读入 $m$、$n$ 与网格；
2. 用 BFS/DFS 给同色连通块编号（`blk[r][c]`），记录每个块的颜色与像素列表；
3. `b = blk[0][0]`、`dp = 右`、`cp = 左`，步数 `step = 0`，用哈希表记录 `(b,dp,cp) → step`；
4. 当 `step < n`：
   - 若当前状态访问过：算出周期 $c$，跳过 $\lfloor(n-\text{step})/c\rfloor$ 个周期；若已到 $n$ 就结束，否则清空记录继续模拟（此时剩余步数 $<c$）；
   - 否则记录当前步号；
   - 按规则算"最远边上的最远像素"，尝试朝 DP 前进一步，更新 BP/CP/DP；
   - `step++`；
5. 输出当前块的颜色。

关于方向：用 0..3 表示右、下、左、右上的循环，顺时针 = `d+1 mod 4`、逆时针 = `d+3 mod 4`（网格行坐标向下增大）。CP 为"左"时方向是 `ccw(dp)`，为"右"时是 `cw(dp)`。

### 3.4 样例走查

样例 1 已在第 2 节逐步走过。用脚本验证：初始 (块1, 右, 左) → 10 步后回到 块1，颜色 1 ✓。

样例 2：网格 3 行 4 列，块有 1、2、3、4、6、2、5、4 等（`6624`/`6625` 里 6 连成一块）；12 步后落在颜色 6 的块上 ✓（程序输出 6）。

样例 3：5×5 的阶梯状图案，9 步后颜色 5 ✓。

## 4. 正确性证明

**引理 1（转移确定）**：给定 (BP, DP, CP)，下一步的 (BP, DP, CP) 唯一确定。

**证明**：规则里没有任何随机或输入相关成分：最远边由矩形决定，最远像素由 DP、CP 决定，前进/碰壁的分支由网格内容决定。∎

**引理 2（周期存在）**：从初始状态出发，至多 $B\cdot4\cdot2+1$ 步内必然有两个时刻的状态相同，且此后状态序列以该周期循环。

**证明**：状态数 $N=B\cdot8\le20000$；确定性转移（引理 1）意味着状态序列 $s_0,s_1,\dots$ 满足 $s_{i+1}=f(s_i)$。由抽屉原理，$s_0..s_N$ 这 $N+1$ 个状态中必有两个相同，设 $s_a=s_b$（$a<b$），则对任意 $k\ge0$ 有 $s_{a+k}=s_{b+k}$（因为 $f$ 确定，归纳即得），即从 $a$ 起以 $c=b-a$ 为周期。∎

**引理 3（跳周期不改变结果）**：若在步号 $s$ 处检测到周期 $c$，则把剩余步数 $n-s$ 减去若干个 $c$ 不改变最终状态。

**证明**：由引理 2，$s_{s+k}=s_{s+k\bmod c}$（对任意 $k\ge0$）。所以走 $n-s$ 步与走 $(n-s)\bmod c$ 步到达的状态相同。∎

**定理**：程序输出的颜色等于"走满 $n$ 步后 BP 所指块的颜色"。

**证明**：若没有触发周期性跳过，程序就是逐字模拟题面规则，显然正确。若在 $s$ 处触发，由引理 3，跳过整周期后继续模拟剩余的 $(n-s)\bmod c$ 步，最终状态与真实地走满 $n$ 步相同。∎

## 5. 复杂度分析

- **时间**：建块 $O(m\cdot W)$（$\le2500$）；模拟至多 $O(N)$ 步（$N\le20000$），每步 $O(1)$（利用矩形性质，或直接扫描块内像素 $O(\text{块大小})$，最坏 $2500$，总量 $5\times10^7$ 也尚可，但本实现用扫描方式配合状态上限，实测 3 ms）。总体与 $n$ 无关。
- **空间**：块编号与像素列表 $O(mW)$、状态表 $O(N)$，合计约 $10^5$ 字节。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int m, n;
vector<string> g;
vector<vector<int>> blk;
vector<vector<pair<int, int>>> cells;  // 每个块的像素列表
vector<int> color;

// 方向：0=右 1=下 2=左 3=上（行向下为 y 轴）
static const int DR[4] = {0, 1, 0, -1};
static const int DC[4] = {1, 0, -1, 0};

static int cw(int d) { return (d + 1) & 3; }              // 屏幕上的顺时针 90°
static int ccw(int d) { return (d + 3) & 3; }

int main() {
    if (scanf("%d %d", &m, &n) != 2) return 0;
    g.resize(m);
    for (int i = 0; i < m; i++) {
        char buf[64];
        scanf("%s", buf);
        g[i] = buf;
    }
    int cols = (int)g[0].size();
    blk.assign(m, vector<int>(cols, -1));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < cols; j++) {
            if (g[i][j] == '0' || blk[i][j] != -1) continue;
            int id = (int)cells.size();
            cells.push_back({});
            color.push_back(g[i][j] - '0');
            // 洪水填充同一颜色（保证是矩形）
            vector<pair<int, int>> st{{i, j}};
            blk[i][j] = id;
            while (!st.empty()) {
                auto [r, c] = st.back();
                st.pop_back();
                cells[id].push_back({r, c});
                for (int d = 0; d < 4; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= m || nc < 0 || nc >= cols) continue;
                    if (blk[nr][nc] != -1 || g[nr][nc] != g[i][j]) continue;
                    blk[nr][nc] = id;
                    st.push_back({nr, nc});
                }
            }
        }

    int B = (int)cells.size();
    // 状态：(块, DP, CP) —— CP: 0=左 1=右；用编码做环检测
    int startBlk = blk[0][0];
    int dp = 0, cp = 0;  // 初始 DP 向右、CP 向左
    vector<int> seen((long long)B * 8, -1);
    auto enc = [&](int b, int d, int c) { return (b * 4 + d) * 2 + c; };
    long long step = 0;
    int b = startBlk;
    while (step < n) {
        int code = enc(b, dp, cp);
        if (seen[code] >= 0) {
            long long cyc = step - seen[code];
            long long left = n - step;
            step += (left / cyc) * cyc;
            if (step >= n) break;
            // 跳过整周期后继续模拟
            seen.assign((long long)B * 8, -1);
        } else {
            seen[code] = (int)step;
        }
        // 找块在 DP 方向上的最远边
        int dr = DR[dp], dc = DC[dp];
        int cpr = DR[cp == 0 ? ccw(dp) : cw(dp)], cpc = DC[cp == 0 ? ccw(dp) : cw(dp)];
        int best1 = INT_MIN, best2 = INT_MIN, br = -1, bc = -1;
        for (auto [r, c] : cells[b]) {
            int v1 = r * dr + c * dc;
            if (v1 > best1) { best1 = v1; best2 = INT_MIN; }
            if (v1 != best1) continue;
            int v2 = r * cpr + c * cpc;
            if (v2 > best2) { best2 = v2; br = r; bc = c; }
        }
        int nr = br + dr, nc = bc + dc;
        if (nr >= 0 && nr < m && nc >= 0 && nc < cols && g[nr][nc] != '0') {
            b = blk[nr][nc];
        } else {
            if (cp == 0) {
                cp = 1;
            } else {
                cp = 0;
                dp = cw(dp);
            }
        }
        step++;
    }
    printf("%d\n", color[b]);
    return 0;
}
```

### Python3

```python
import sys

DR = [0, 1, 0, -1]
DC = [1, 0, -1, 0]


def main():
    data = sys.stdin.read().split()
    m, n = int(data[0]), int(data[1])
    g = data[2:2 + m]
    cols = len(g[0])
    blk = [[-1] * cols for _ in range(m)]
    cells = []
    color = []
    for i in range(m):
        for j in range(cols):
            if g[i][j] == '0' or blk[i][j] != -1:
                continue
            bid = len(cells)
            cells.append([])
            color.append(int(g[i][j]))
            st = [(i, j)]
            blk[i][j] = bid
            while st:
                r, c = st.pop()
                cells[bid].append((r, c))
                for d in range(4):
                    nr, nc = r + DR[d], c + DC[d]
                    if 0 <= nr < m and 0 <= nc < cols and blk[nr][nc] == -1 and g[nr][nc] == g[i][j]:
                        blk[nr][nc] = bid
                        st.append((nr, nc))

    B = len(cells)
    b = blk[0][0]
    dp, cp = 0, 0
    seen = {}
    step = 0
    while step < n:
        key = (b, dp, cp)
        if key in seen:
            cyc = step - seen[key]
            step += ((n - step) // cyc) * cyc
            if step >= n:
                break
            seen = {}
        else:
            seen[key] = step
        dr, dc = DR[dp], DC[dp]
        cpd = (dp + 3) % 4 if cp == 0 else (dp + 1) % 4
        cpr, cpc = DR[cpd], DC[cpd]
        best1 = -10 ** 9
        best2 = -10 ** 9
        br = bc = -1
        for (r, c) in cells[b]:
            v1 = r * dr + c * dc
            if v1 > best1:
                best1 = v1
                best2 = -10 ** 9
            if v1 != best1:
                continue
            v2 = r * cpr + c * cpc
            if v2 > best2:
                best2 = v2
                br, bc = r, c
        nr, nc = br + dr, bc + dc
        if 0 <= nr < m and 0 <= nc < cols and g[nr][nc] != '0':
            b = blk[nr][nc]
        else:
            if cp == 0:
                cp = 1
            else:
                cp = 0
                dp = (dp + 1) % 4   # 顺时针
        step += 1
    print(color[b])


main()
```

## 7. 边界情况与易错点

1. **CP 与 DP 的旋转方向**：本题最容易错的地方。"CP 向左"是相对 DP 逆时针 90°，"CP 向右"是顺时针 90°；而"CP 原向右、再碰壁"时 DP 旋转的是**顺时针** 90°。在"行向下"的坐标系里，顺时针是 `(dr,dc) → (dc,-dr)`，对应方向编号 `d+1`。若把顺/逆时针弄反，样例 1 的步数序列会立刻对不上。
2. **"最远边"与"边上最远的像素"是两个不同的投影**：先在 DP 方向取极值（得到一条边），再在这条边上按 CP 方向取极值（得到一个角）。把顺序弄反会选到别的像素。
3. **块是矩形但黑色不是**：黑色区域可以是任意形状，不能按矩形处理；我们只在"落点是否黑色"时判断，不需要给黑块建矩形。
4. **落点越界**：朝 DP 前进一步可能越出网格，这算"碰到黑格"，要按碰壁处理（BP 不动、CP/DP 更新）。
5. **$n$ 很大**：必须做周期跳过；否则 $5\times10^7$ 步每步扫块会超时。
6. **周期检测的记录值**：记录"第一次访问该状态的步号"；算循环长度时用当前步号减去记录值，注意在跳过整周期后要清空记录（否则会重复跳过导致死循环）。
7. **恰好 $n$ 步**：循环条件是 `step < n`，每步执行后自增；跳过整周期时若正好到 $n$ 要立即结束并输出当前块。
8. **初始 CP 是"左"**：题面明确"DP 向右、CP 向左"（图里橙色方块）。
9. **单行/单列/单像素**：$1\times1$ 的网格只有 1 个块，若它非黑，则第 1 步就撞墙，之后在 (块, DP, CP) 之间循环；逻辑必须能处理"块内只有 1 个像素"和"宽度为 1"的情况。
10. **颜色 0 不会成为 BP**：题面保证左上角非黑，且 BP 只在色块之间移动；输出不会是 0。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（配 `codeforces/tools/include/bits/stdc++.h` 兼容头）；Python 3.9.6。
  `python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/132/B_Piet解释器.md`
- **官方样例**：$3/3$ 通过（`1`、`6`、`5`），C++ 与 Python 一致。
- **独立实现对拍**：另写一份 Python 解释器（同一规则、不同代码结构），在 $300$ 个随机生成的小程序（$m\le6$、列数 $\le6$、颜色取自 `0..4`，并筛选"同色连通块为矩形"的程序、左上角非 `0`）上比较 $n\le60$ 的输出，全部一致。
- **周期跳过 vs 朴素模拟**：把 C++ 的周期检测去掉，写一份"逐字模拟"的 Python 版本，在 $200$ 组随机小程序（$n\le300$）上对比，结果全部一致——这一步专门验证引理 3 的跳过逻辑。
- **最大规模性能**：$50\times50$、$n=5\times10^7$ 的输入（2500 个块、2500 种以上状态）单次约 3 ms，2 s 余量数百倍；说明与 $n$ 无关。
- **图片校验**：2 张 SVG 均通过 `xml.etree.ElementTree.parse`。
- **复核状态**：verified（样例、独立对拍、周期验证、性能、图片均实跑通过）。

## 相关题目与扩展

- [Codeforces 132C Logo Turtle](https://codeforces.com/problemset/problem/132/C)：同场 C 题，DP。
- [Codeforces 132A Turing Tape](https://codeforces.com/problemset/problem/132/A)：同场 A 题，字符编码可逆。
- [Codeforces 132D Constants in the language of Shakespeare](https://codeforces.com/problemset/problem/132/D)：同场 D 题。
- [Codeforces 1B Spreadsheets](https://codeforces.com/problemset/problem/1/B)：编码/解码模拟。

**延伸思考**：

1. **若块不是矩形**：每步找"最远边"要扫描整个块，复杂度 $O(\text{步数}\times\text{块大小})$；周期跳过后仍是 $O(N\cdot S)$，$N\le20000$、$S\le2500$ 时约 $5\times10^7$，仍可接受。
2. **若 DP 旋转改成逆时针**：只改 `cw`/`ccw` 两处，其余不变；但要重新核对样例。
3. **若要求完整执行（不限步数）直到停机**：Piet 是图灵完备的，本题的简化子集也没有通用停机保证；但在有限状态模型下它最终必然进入周期，可以判定"是否停在某个块"。
4. **若网格到 $10^3\times10^3$**：块数与状态数到 $10^7$，状态表要用哈希；每步 $O(1)$ 的矩形角计算仍是可取的。
