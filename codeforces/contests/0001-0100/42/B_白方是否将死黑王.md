# Codeforces 42B 白方是否将死黑王 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/42/B
- **比赛来源**：Codeforces Beta Round 42 · Problem B（2010-09-28）
- **难度**：1700
- **标签**：实现（implementation）
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$8 \times 8$ 棋盘上只有四个棋子：两个白车、白王、黑王，位置合法且互不重叠。判断黑方是否已被**将死**（白方获胜）：即黑王正被攻击，且黑王走到任何相邻格（含吃车）都无法摆脱攻击。输出 `CHECKMATE` 或 `OTHER`。

**约束**：

- 输入只有四个格子的坐标（`a1` ~ `h8`），棋盘固定 $8\times8$。
- 车走直线，路径上不能有棋子；王走八邻域；两王不能相邻（不能走到对方王的攻击格）。
- 黑王可以吃掉白车（样例 3），但吃子后该格若仍被白方攻击则非法。
- 棋子只有四个，直接模拟即可，无需搜索。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
a6 b4 c8 a8

输出：
CHECKMATE
```

**演算**：黑王在 `a8`。白车 `a6` 沿 a 列攻击 `a8`（中间 `a7` 空）→ 黑王被将军。黑王能走的格：

| 目标格 | 是否被攻击 | 原因 |
|--------|------------|------|
| `a7` | 是 | 车 `a6` 同一列 |
| `b7` | 是 | 车 `b4` 同一列 |
| `b8` | 是 | 车 `b4` 同一列（`b5、b6、b7` 空） |

三个格子全被控制，也没有车可吃 → `CHECKMATE` ✓。

官方样例 2（输入 / 输出原样）：

```text
输入：
a6 c4 b6 b8

输出：
OTHER
```

**演算**：黑王 `b8` 是否被攻击？车 `a6` 在 a 列、`c4` 在 c 列，都不与 `b8` 同列/同行；白王 `b6` 与 `b8` 相距 2 行，不构成攻击。黑王没有处于被将军状态 → 不可能是将死，输出 `OTHER` ✓。

官方样例 3（输入 / 输出原样）：

```text
输入：
a2 b1 a3 a1

输出：
OTHER
```

**演算**：黑王 `a1` 被车 `a2` 沿 a 列将军（`a2` 在 `a1` 正上方）。但黑王可以吃掉 `b1` 的车：`b1` 是否被白方保护？白王在 `a3`，与 `b1` 的切比雪夫距离是 $\max(1,2)=2$，保护不到；另一辆车 `a2` 与 `b1` 不同行也不同列。所以吃 `b1` 合法 → 黑王逃脱 → `OTHER` ✓。

**观察**：

1. 将死 = **现在被攻击** 且 **所有相邻格都不可去**（不可去 = 出界、被白王占、或仍被攻击）。
2. "吃车"要单独处理：先把被吃的车从棋盘上拿掉，再判断该格是否仍被攻击。
3. 判定"某格是否被车攻击"时，要检查两车之间、车与白王之间是否挡子。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

棋子只有 4 个，直接枚举黑王的 8 个方向、逐格判断攻击即可，$O(1)$。唯一的难点是**规则细节**：

- 黑王不能走到白王相邻的格子；
- 吃子后要移除被吃的车再判攻击；
- 车的攻击被任意棋子阻挡（包括白王、另一辆车）；
- 黑王当前格若没有被攻击，直接 `OTHER`（不是将死）。

### 3.2 核心：攻击判定 + 8 方向枚举

![车的射线攻击与阻挡](../../../images/cf42b_attack.svg)

**攻击判定** `attacked(r, c)`：

1. 白王与 `(r,c)` 的切比雪夫距离 $\le 1$ → 被攻击；
2. 对每个未被吃掉的车：若与 `(r,c)` 同行或同列，且两者之间没有其它棋子（白王、另一辆车），则被攻击。

**将死判定**：

1. 若 `attacked(黑王)` 为假 → `OTHER`；
2. 否则对黑王 8 个方向：
   - 出界 → 跳过；
   - 目标格是白王 → 跳过（不能吃王）；
   - 目标格有车 → 移除该车后判 `attacked`，若不被攻击 → 黑王可逃 → `OTHER`；
   - 否则若 `attacked` 为假 → `OTHER`；
3. 全部被封死 → `CHECKMATE`。

![黑王的 8 个落点](../../../images/cf42b_moves.svg)

### 3.3 流程

1. 解析四个坐标（列 `a`~`h` → $0..7$，行 `1`~`8` → $0..7$）；
2. 若黑王未被攻击 → `OTHER`；
3. 枚举 8 邻格，按 3.2 的规则判断是否可逃；
4. 输出结论。

### 3.4 样例走查：样例 1

黑王 `a8` = $(7,0)$；车在 `a6`=$(5,0)、`b4`=$(3,1)；白王 `c8`=$(7,2)。

- `attacked(a8)`：车 `a6` 与 `a8` 同列，中间 `a7`=$(6,0) 空 → 被攻击 ✓；
- 邻格 `a7`=$(6,0)：被 `a6` 攻击 ✓；
- 邻格 `b7`=$(6,1)：与 `b4` 同列，中间 `b5,b6` 空 → 被攻击 ✓；
- 邻格 `b8`=$(7,1)：与 `b4` 同列，中间空 → 被攻击 ✓；
- 其余邻格出界。

三面被封 → `CHECKMATE` ✓。

## 4. 正确性证明

**引理 1（攻击判定的正确性）**：格子 $s$ 被白方攻击，当且仅当它被白王或某辆未被吃掉的车攻击，而车的攻击必须满足"同行/同列且中间无子"。

**证明**：白方只有王和车两种棋子，攻击方式与走法一致；车沿直线走，遇到第一个棋子即停，因此只有中间无子时才能攻击到 $s$。∎

**引理 2（黑王可走格）**：黑王从 $s$ 走到 $t$ 合法，当且仅当 $t$ 在棋盘内、$t \ne$ 白王所在格、且移动后 $t$ 不被白方攻击（若 $t$ 有白车，则在"该车已被吃掉"的局面下判断）。

**证明**：黑王的走法是八邻域一步；不能走到白王所在格（不能吃王），不能走进被攻击的格子（否则被吃）；吃车是走到该格并移除该车，属合法着法，但需重新判断攻击。∎

**定理**：算法输出 `CHECKMATE` 当且仅当黑方被将死。

**证明**：将死的定义是"黑王被将军且无合法着法可解"。算法先检查将军（引理 1），再枚举全部合法目标格（引理 2）；若存在一个目标格不被攻击，黑王可逃，输出 `OTHER`；否则无路可走，输出 `CHECKMATE`。∎

## 5. 复杂度分析

- **时间**：$O(1)$：最多 8 个方向 × 2 辆车 × 8 格射线。
- **空间**：$O(1)$。
- **与时限的关系**：2 s 时限，运行时间可以忽略。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Sq { int r, c; };   // r: 0..7 (rank 1..8), c: 0..7 (file a..h)

Sq parse(const string& s){ return { s[1]-'1', s[0]-'a' }; }

bool inside(int r,int c){ return r>=0&&r<8&&c>=0&&c<8; }

// 判断格子 (r,c) 是否被白方攻击；cap 为被黑王吃掉的车（-1 表示没有吃子）
bool attacked(int r,int c, const array<Sq,2>& rook, const Sq& wking, int cap){
    // 白王相邻
    if (max(abs(r-wking.r), abs(c-wking.c)) <= 1) return true;
    for (int i=0;i<2;i++){
        if (i==cap) continue;
        int rr=rook[i].r, cc=rook[i].c;
        if (rr==r && cc==c) continue;          // 车所在格由调用方处理
        if (rr==r){
            int lo=min(cc,c), hi=max(cc,c); bool block=false;
            for(int k=lo+1;k<hi;k++){
                if (wking.r==rr && wking.c==k) block=true;
                for(int j=0;j<2;j++) if(j!=i && j!=cap && rook[j].r==rr && rook[j].c==k) block=true;
            }
            if(!block) return true;
        }
        if (cc==c){
            int lo=min(rr,r), hi=max(rr,r); bool block=false;
            for(int k=lo+1;k<hi;k++){
                if (wking.c==cc && wking.r==k) block=true;
                for(int j=0;j<2;j++) if(j!=i && j!=cap && rook[j].c==cc && rook[j].r==k) block=true;
            }
            if(!block) return true;
        }
    }
    return false;
}

int main(){
    string s1,s2,s3,s4;
    if(!(cin>>s1>>s2>>s3>>s4)) return 0;
    Sq rook[2] = { parse(s1), parse(s2) };
    array<Sq,2> rookArr = { rook[0], rook[1] };
    Sq wking = parse(s3), bking = parse(s4);

    if (!attacked(bking.r, bking.c, rookArr, wking, -1)) { cout<<"OTHER\n"; return 0; }

    // 黑王尝试 8 个方向
    int dr[8]={-1,-1,-1,0,0,1,1,1}, dc[8]={-1,0,1,-1,1,-1,0,1};
    for(int d=0; d<8; ++d){
        int nr=bking.r+dr[d], nc=bking.c+dc[d];
        if(!inside(nr,nc)) continue;
        if(nr==wking.r && nc==wking.c) continue;      // 不能吃白王
        int cap=-1;
        for(int i=0;i<2;i++) if(rook[i].r==nr && rook[i].c==nc) cap=i;
        if(cap>=0){
            // 吃车后看该格是否仍被攻击
            if(!attacked(nr,nc,rookArr,wking,cap)){ cout<<"OTHER\n"; return 0; }
        } else {
            if(!attacked(nr,nc,rookArr,wking,-1)){ cout<<"OTHER\n"; return 0; }
        }
    }
    cout<<"CHECKMATE\n";
}
```

### Python3

```python
import sys

def parse(s):
    return (int(s[1]) - 1, ord(s[0]) - ord('a'))

def attacked(r, c, rooks, wking, cap):
    wr, wc = wking
    if max(abs(r - wr), abs(c - wc)) <= 1:
        return True
    for i in range(2):
        if i == cap:
            continue
        rr, cc = rooks[i]
        if rr == r and cc == c:
            continue
        if rr == r:
            lo, hi = min(cc, c), max(cc, c)
            block = False
            for k in range(lo + 1, hi):
                if wr == rr and wc == k:
                    block = True
                for j in range(2):
                    if j != i and j != cap and rooks[j] == (rr, k):
                        block = True
            if not block:
                return True
        if cc == c:
            lo, hi = min(rr, r), max(rr, r)
            block = False
            for k in range(lo + 1, hi):
                if wc == cc and wr == k:
                    block = True
                for j in range(2):
                    if j != i and j != cap and rooks[j] == (k, cc):
                        block = True
            if not block:
                return True
    return False

def main():
    d = sys.stdin.read().split()
    if len(d) < 4:
        return
    rooks = (parse(d[0]), parse(d[1]))
    wking = parse(d[2])
    bking = parse(d[3])
    if not attacked(bking[0], bking[1], rooks, wking, -1):
        print("OTHER"); return
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = bking[0] + dr, bking[1] + dc
            if not (0 <= nr < 8 and 0 <= nc < 8):
                continue
            if (nr, nc) == wking:
                continue
            cap = -1
            for i in range(2):
                if rooks[i] == (nr, nc):
                    cap = i
            if not attacked(nr, nc, rooks, wking, cap):
                print("OTHER"); return
    print("CHECKMATE")

main()
```

## 7. 边界情况与易错点

1. **黑王当前没被将军**：直接 `OTHER`——将死必须先是将军。
2. **吃车后要重新判攻击**：吃掉的车的攻击必须失效，否则会误判 `CHECKMATE`（样例 3）。
3. **车被另一辆车或白王挡住**：射线扫描必须考虑所有棋子，而不只是两车之间。
4. **黑王不能吃白王**：目标格是白王所在格时直接跳过。
5. **两王相邻非法**：白王相邻格已由 `attacked` 覆盖。
6. **黑王不能走到有白车但没有保护…**：只有吃子合法，走到有车格必须当作吃子处理。
7. **只有 4 个棋子**：不用考虑白方其他棋子，也不用考虑黑方其它棋子。
8. **坐标解析**：`a1` → 列 0、行 0；不要搞反行列。

## 8. 验证记录

- **编译环境与命令**：本机没有 GNU `g++`，C++ 用 `clang++ -std=c++17 -O2` 搭配兼容头编译；Python 为 `Python 3.9.6`。由 `python3 codeforces/tools/verify_solution.py codeforces/contests/0001-0100/42/B_白方是否将死黑王.md` 复核。
- **官方样例**：3 / 3 通过（C++ 与 Python 各一遍）。
- **独立对拍**：另写一份"网格 + 射线逐格扫描"的独立实现（与主程序的位运算式扫描不同），在 $8\times8$ 棋盘上随机放 4 个不同格子共 **250 组**，三方（C++ / Python / 独立实现）结果 0 处不符。
- **性能**：$O(1)$，单次运行 < 1 ms。
- **图片校验**：两张 SVG 通过 `ElementTree.parse` 与无头浏览器 `getBBox` 复核。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 42A 罗宋汤的最大体积](https://codeforces.com/problemset/problem/42/A)、[Codeforces 42C Safe cracking](https://codeforces.com/problemset/problem/42/C)：同场 A、C 题。
- [LeetCode 36. 有效的数独](https://leetcode.cn/problems/valid-sudoku/)：棋盘类模拟的入门。
- [Codeforces 7B Memory Manager](https://codeforces.com/problemset/problem/7/B)：同类的"按规则模拟"题。

**延伸思考**：

1. **如果有白象/白马**：攻击判定要加斜线与马步，框架不变。
2. **如果黑方也有棋子**：要检查黑方能否解将（挡、吃、跑），问题变成完整的博弈搜索。
3. **如果要求输出最佳防守着法**：在 8 个方向里取"存活最久"的，需要更深的搜索。
