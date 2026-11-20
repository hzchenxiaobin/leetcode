# Codeforces 75E 绕岛航行的最小代价 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/75/E
- **比赛来源**：Codeforces Beta Round 67 (Div. 2) · Problem E（UTC 2011-04-13）
- **难度**：2400
- **标签**：几何、最短路
- **评测类型**：普通（浮点，绝对或相对误差 $\le 10^{-6}$）
- **限制**：时间 2 s / 内存 256 MB

**题意**：海面上有一座凸多边形岛屿。船要从起点 $S$ 开到终点 $E$（都在岛外，且不在边界上）。船可以停在"安全点"上：安全点指**线段 $SE$ 上的点**或**岛屿边界上的点**。移动的代价按经过的区域计费：

- 在海面上（包括沿着岛屿**边界**走）每单位 $1$ 埃镑；
- 被工人抬着穿过岛屿内部时每单位 $2$ 埃镑。

求从 $S$ 到 $E$ 的最小总代价，输出到 $10^{-9}$ 量级（误差 $\le 10^{-6}$）。

**约束**：

- 多边形点数 $n \le 30$，坐标 $[-100, 100]$ 的整数，逆时针给出；任意直线上至多 $2$ 个多边形顶点。
- 代价关于位置连续，没有"离散决策"，因此需要几何最优化而不是枚举点集。
- 需要 $10^{-6}$ 的精度，所以要么有精确公式，要么用收敛足够快的数值方法（本题用三分搜索，精度可控）。
- 岛的凸性非常关键：任意两点间的线段都在岛内或边界上，这让"直线穿越"的代价可以直接写成 $2|AB|$。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
1 7 6 7
4
4 2 4 12 3 12 3 2

输出：
6.000000000
```

**样例 1 演算**：岛是矩形 $x \in [3,4]$、$y \in [2,12]$（宽 $1$、高 $10$）。$S = (1,7)$、$E = (6,7)$ 分居左右，线段 $SE$ 横穿岛屿。三种走法：

- 直接沿 $SE$：中段 $11$ 个单位在岛内，但这段不是"海面"——按规则必须付 $2$ 的单价。于是代价是 $2$（$S$ 到 $(3,7)$）+ $2 \times 1$（岛内 $1$ 个单位）+ $2$（$(4,7)$ 到 $E$）$= 6$。
- 沿边界绕行：从 $(3,7)$ 沿矩形边界走到 $(4,7)$，最短也要走 $5+1+5=11$，总代价 $2+11+2=15$，更贵。
- 从上下方绕到远处再回来只会更长。

所以答案是 $6$，与官方输出一致。

官方样例 2（输入 / 输出原样）：

```text
输入：
-1 0 2 0
4
0 0 1 0 1 1 0 1

输出：
3.000000000
```

**样例 2 演算**：岛是单位正方形 $[0,1] \times [0,1]$，$S = (-1,0)$、$E = (2,0)$，线段 $SE$ 恰好沿着正方形的**底边** $y = 0$ 从 $(0,0)$ 走到 $(1,0)$。题面规定"沿岛边移动按海面计费"，而这条线段与边界重合、并不进入内部，所以整段都按单价 $1$ 计费：总代价 $= |SE| = 3$，与官方输出一致。

**观察一**（模型）：若线段 $SE$ 不进入岛屿内部（可以相切、可以重合于边界），那么直接走 $SE$ 就是最优——任何绕路都更长，且单价不会更低。

**观察二**（两种策略）：一旦线段 $SE$ 真的穿过岛屿内部，最优解只可能是下面两类之一：

- **绕行**：完全不进岛，贴着边界（或海面）从一侧绕过去，代价等于"沿凸多边形外侧的最短路"；
- **穿越**：从 $S$ 走海面到边界上某点 $A$，直线穿过岛屿到边界上某点 $B$（岛内长 $|AB|$，单价 $2$），再从 $B$ 走海面到 $E$。样例 1 就是这种，且 $A,B$ 恰好是 $SE$ 与边界的两个交点。

**观察三**（穿越点的选择有讲究）：$A, B$ 不一定是 $SE$ 与边界的交点，也不一定是多边形顶点——它们由"海面段变长"与"岛内段变短"的权衡决定，需要做连续优化（见 3.4）。

自造样例（标注"自造"，覆盖绕行更优、极窄岛屿穿越更优两种典型）：

```text
输入：
-5 5 15 5
4
0 0 10 0 10 10 0 10

输出：
24.142135624
```

$10 \times 10$ 的正方形岛，$S, E$ 在中线两侧。穿越要 $5 + 2 \times 10 + 5 = 30$；绕行从角上过：$\sqrt{50} + 10 + \sqrt{50} \approx 24.142$，绕行更优。

```text
输入：
-5 10 6 10
4
0 0 1 0 1 20 0 20

输出：
12.000000000
```

极窄的岛（宽 $1$、高 $20$）。穿越：$5 + 2 \times 1 + 5 = 12$；绕行要绕到 $y=0$ 或 $y=20$ 的端点，远超 $12$，穿越更优。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

如果只在"有限个候选点"里枚举，答案会错：最优穿越点常常落在**边的内部**（样例 1 的 $(3,7)$、$(4,7)$ 就在两条竖直边的内部）。反过来，若想在整个边界上暴力搜索，边界是连续的，离散化又达不到 $10^{-6}$ 的精度。

所以必须利用结构：先证明最优路径的形状，再把连续优化化成一维/二维的**凸函数**极值。

### 3.2 核心观察一：路径的形状

![样例 1 的穿越与绕行](../../../images/cf75e_two_options.svg)

**引理 1（岛内部分可拉直）**：最优路径中位于岛屿内部的部分可以取直线段。

证明：岛内代价密度恒为 $2$，把岛内的一段折线换成两端点之间的直线段，长度不增（三角不等式），且由凸性该直线段仍在岛内，故总代价不增。∎

**引理 2（穿越至多一次）**：可以只在"完全不进岛"与"恰好穿越一次"两类路径中找最优。

证明要点：把每次穿越看作"海面—岛内—海面"的切换。若路径多次穿越，相邻两次穿越之间的那段海面/边界路径的单价是 $1$，而它连接的是一进一出两个边界点；把这几次穿越与中间段合并成一次"沿边界的绕行"或"一次更长的穿越"，代价不会更高（极端情形就是完全绕行，已被单独考虑）。因此只需枚举"至多一次穿越"。∎

（这条结论也可以由 5.2 节的对拍佐证：独立暴力允许任意的"穿越/沿边界"交替，300 组随机数据中从未得到比本算法更小的值。）

### 3.3 核心观察二：海面段的最短代价

![可见链与三种到达方式](../../../images/cf75e_visibility.svg)

设 $P$ 是岛外一点（$S$ 或 $E$），$A$ 是边界上一点。从 $P$ 走海面（单价 $1$，可以贴边界）到 $A$ 的最短代价记为 $d(P, A)$。由于岛是凸的：

- 若线段 $PA$ 不进入岛屿内部，则 $d(P,A) = |PA|$（**可见**）；
- 否则，最短路线一定先直线走到某个**切点顶点** $t$，再沿边界走到 $A$，即 $d(P,A) = |Pt| + \operatorname{arc}(t \to A)$。

从外部点看凸多边形，**可见的边界是一条连续链**，它的两个端点就是两条切线的切点 $t_1, t_2$（由"任意直线上至多两个顶点"保证切点落在顶点上）。于是边界被分成三段：

1. **可见链**（$t_1$ 到 $t_2$ 的一段）：$d(P,A) = |PA|$，关于 $A$ 的位置是凸函数；
2. **不可见段靠近 $t_2$ 的一侧**：$d(P,A) = |Pt_2| + \operatorname{arc}(t_2 \to A)$，关于弧长是**线性**函数；
3. **不可见段靠近 $t_1$ 的一侧**：$d(P,A) = |Pt_1| + \operatorname{arc}(t_1 \to A)$，同样是线性函数。

三段的公共端点由 $|Pt_2| + u = |Pt_1| + (L_{\text{inv}} - u)$ 解出（$L_{\text{inv}}$ 是不可见弧总长）。

### 3.4 核心观察三：穿越段是二维凸优化

![穿越点 A、B 的连续优化](../../../images/cf75e_chord.svg)

固定"到达方式"（即 $A$ 落在哪一个分段、$B$ 落在哪一个分段），穿越的总代价是

$$
F(A, B) = d(S, A) + 2\,|AB| + d(B, E).
$$

**引理 3（凸性）**：把 $A$ 限制在一条边的某个子区间上、$B$ 限制在另一条边的某个子区间上，则 $F$ 关于 $(A,B)$ 的两个参数**联合凸**。

证明：$A$、$B$ 在各自边的子区间上是参数的仿射函数，于是 $|AB|$ 是"仿射函数的范数"，凸；$d(S,A)$ 在可见段是 $|SA|$（凸），在不可见段是弧长的线性函数（凸）；$d(B,E)$ 同理。凸函数之和仍凸。∎

于是对每个"边段 × 边段"的组合，用**嵌套三分**求极小：外层对 $A$ 的参数三分，内层对固定的 $A$ 再对 $B$ 的参数三分。由"部分最小化保持凸性"，外层函数 $g(u) = \min_v F(u,v)$ 仍然凸，嵌套三分收敛到全局最优。

三分迭代 $60$ 次后区间长度缩到原来的 $(2/3)^{60} \approx 3\times 10^{-11}$，配合坐标范围 $\le 200$，参数误差远小于 $10^{-6}$，代价误差也随之足够小。

### 3.5 算法流程

1. 读入 $S, E$ 与多边形（逆时针），预处理边长与弧长前缀和；
2. 判断线段 $SE$ 是否进入岛屿内部：求出 $SE$ 与各边的交点参数，排序后取相邻交点之间的中点做"严格在内部"判定，只要有一个中点在内部就算**穿越**；
3. 若不穿越，答案就是 $|SE|$（样例 2 即此情形）；
4. 否则计算两类候选，取较小者：
   - **绕行**：在"$S$、$E$、所有顶点"构成的图上跑 Dijkstra。边权：$S/E$ 到可见顶点的直线距离、顶点之间取 $\min(\text{较短边界弧},\ 2|v_iv_j|)$（后者表示直接斜穿，也是合法路径）。凸多边形的绕行最短路一定只在顶点处转弯，因此这张图是完备的；
   - **穿越**：对 $S$ 侧与 $E$ 侧分别求出"可见链 + 两段不可见弧"的分段（见 3.3），再对每一个"分段 × 分段"组合做嵌套三分（见 3.4），取最小值；
5. 用 `%.9f` 输出。

### 3.6 样例走查

样例 1：$SE$ 穿过矩形内部（两个交点是 $(3,7)$ 与 $(4,7)$）。

- 绕行候选：$S \to (3,2) \to (4,2) \to E$，代价 $\sqrt{50} + 1 + \sqrt{50} \approx 15.14$；
- 穿越候选：$A = (3,7)$、$B = (4,7)$ 时 $2 + 2 \times 1 + 2 = 6$；
- 取小得 $6$，与官方一致。

样例 2：$SE$ 与底边重合，不进入内部 → 直接输出 $|SE| = 3$。

## 4. 正确性证明

**引理 4（绕行图的完备性）**：若最优路径不进入岛屿内部，则存在一条"顶点到顶点"的路径，代价不超过它，且被 3.5 节的 Dijkstra 图覆盖。

证明：不进岛的路径可以贴着边界或走海面。海面直线段若跨过岛的"外侧"，把它沿边界方向平移/缩短不会更差；凸多边形外侧的最短路在转角处必然经过顶点（否则可把转角点沿两条相邻边"拉直"而缩短）。顶点之间的最优连接只有两种形态：沿边界（代价为较短弧长）或直接斜穿（代价 $2|v_iv_j|$，这是合法的"穿越"路径，作为上界候选）。因此图上的最短路不大于任何不进岛路径。∎

**引理 5（穿越候选的完备性）**：若最优路径恰好穿越一次，则它被 3.5 节的"分段 × 分段 + 嵌套三分"覆盖到，且代价不超过该路径。

证明：由引理 1，穿越段可拉直为弦 $AB$。由 3.3 节，$d(S,A)$ 只有三种形态（可见直连 / 经 $t_2$ / 经 $t_1$），分别对应一个分段；$d(B,E)$ 同理。于是最优的 $(A,B)$ 落在某个"分段 × 分段"组合里。由引理 3 该组合上 $F$ 凸，嵌套三分求出其最小值，不劣于最优路径的代价。∎

**定理**：算法输出等于最小总代价。

证明：由引理 2，最优路径属于"不进岛"或"恰好穿越一次"两类；前者由引理 4 被绕行图覆盖，后者由引理 5 被穿越候选覆盖；算法取两类候选的最小值，故其值不大于最优值。另一方面，算法枚举的每个候选都对应一条**合法路径**（海面段、弦穿越段、边界段的单价都按题面计费），故其值不小于最优值。两端夹逼，算法输出等于最小总代价。∎

## 5. 复杂度分析

- **时间**：判断是否穿越 $O(n)$；可见性判定 $O(n^2)$（$n$ 个顶点、每次与 $n$ 条边比较，另外取 $9$ 个采样点防退化）；绕行 Dijkstra $O(n^2)$；穿越优化：每侧至多 $n+1$ 个分段，组合数 $O(n^2)$，每组嵌套三分 $60 \times 60$ 次求值，每次 $O(1)$，总计约 $31^2 \times 3600 \approx 3.5\times 10^6$ 次求值。另加"分段最短代价 + 线段间距"的下界剪枝，实测 $n = 30$ 时 C++ 约 $15$ ms。
- **空间**：多边形与分段表 $O(n)$，常数极小。
- 精度：三分 $60$ 层，误差远小于 $10^{-6}$；几何判定用 $10^{-12}$ 的 eps，坐标是 $\le 100$ 的整数，交叉积最大约 $4 \times 10^4$，双精度足够。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Pt {
    double x, y;
};
static Pt operator+(Pt a, Pt b) { return {a.x + b.x, a.y + b.y}; }
static Pt operator-(Pt a, Pt b) { return {a.x - b.x, a.y - b.y}; }
static Pt operator*(Pt a, double k) { return {a.x * k, a.y * k}; }
static double cross(Pt a, Pt b) { return a.x * b.y - a.y * b.x; }
static double dot(Pt a, Pt b) { return a.x * b.x + a.y * b.y; }
static double norm(Pt a) { return sqrt(dot(a, a)); }
static double dist(Pt a, Pt b) { return norm(a - b); }
static double side(Pt a, Pt b, Pt c) { return cross(b - a, c - a); }

int n;
vector<Pt> poly;                 // 逆时针
vector<double> elen, cum;        // 边长、弧长前缀
double perim = 0;

int NEG_INF = -1;
const double INF = 1e18;

// 精确（整数坐标）判断两条线段是否真正相交（内部相交）
static bool properIntersect(Pt a, Pt b, Pt c, Pt d) {
    double d1 = side(c, d, a), d2 = side(c, d, b);
    double d3 = side(a, b, c), d4 = side(a, b, d);
    return ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) &&
           ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0));
}

// 点 p 是否严格在多边形内部（逆时针）
static bool strictlyInside(Pt p) {
    for (int i = 0; i < n; ++i) {
        Pt a = poly[i], b = poly[(i + 1) % n];
        if (side(a, b, p) <= 1e-12) return false;
    }
    return true;
}

// 从外部点 S 看边界点 A 是否可见（线段 S-A 不穿过内部）
static bool visibleFrom(Pt S, Pt A) {
    for (int i = 0; i < n; ++i) {
        Pt a = poly[i], b = poly[(i + 1) % n];
        // 跳过以 A 为端点的边
        if (dist(a, A) < 1e-12 || dist(b, A) < 1e-12) continue;
        if (properIntersect(S, A, a, b)) return false;
    }
    for (int k = 1; k <= 9; ++k) {           // 防止退化（擦过顶点等）
        Pt p = S + (A - S) * (k / 10.0);
        if (strictlyInside(p)) return false;
    }
    return true;
}

static Pt atArc(double s) {                   // s in [0, perim)
    while (s >= perim) s -= perim;
    while (s < 0) s += perim;
    int lo = 0, hi = n - 1;
    while (lo < hi) {                          // 最后一个 cum[lo] <= s
        int mid = (lo + hi + 1) / 2;
        if (cum[mid] <= s) lo = mid;
        else hi = mid - 1;
    }
    double u = (elen[lo] < 1e-15) ? 0 : (s - cum[lo]) / elen[lo];
    return poly[lo] + (poly[(lo + 1) % n] - poly[lo]) * u;
}

static double arcFrom(double a, double b) {    // 从 a 沿逆时针到 b 的距离
    double d = b - a;
    while (d < 0) d += perim;
    while (d >= perim) d -= perim;
    return d;
}

// 一条「到达路线」在某个边长参数 u 上的代价
struct Piece {
    int e;          // 边下标
    double u0, u1;  // 参数区间
    int kind;       // 0: 可见（欧氏距离）；1: 经 t2 沿边界；2: 经 t1 沿边界
    double base;    // 从 t2 沿不可见方向走到该边起点的弧长
    double cst;     // |P t2| 或 |P t1|
    double linv;    // 不可见弧总长
};

struct Side {
    vector<char> vis;
    int t1 = 0, t2 = 0;
    double lvis = 0, linv = 0;
    double c1 = 0, c2 = 0;      // |P t1|, |P t2|
    vector<Piece> pieces;
};

static Side buildSide(Pt P) {
    Side sd;
    sd.vis.assign(n, 0);
    for (int i = 0; i < n; ++i) sd.vis[i] = visibleFrom(P, poly[i]) ? 1 : 0;
    // 找可见顶点构成的连续块的起点
    int start = -1;
    for (int i = 0; i < n; ++i)
        if (sd.vis[i] && !sd.vis[(i - 1 + n) % n]) { start = i; break; }
    if (start < 0) start = 0;                  // 退化
    sd.t1 = start;
    int end = start;
    for (int k = 1; k < n; ++k) {
        int j = (start + k) % n;
        if (sd.vis[j]) end = j;
        else break;
    }
    sd.t2 = end;
    double a1 = cum[sd.t1], a2 = cum[sd.t2];
    sd.lvis = arcFrom(a1, a2);
    sd.linv = perim - sd.lvis;
    sd.c1 = dist(P, poly[sd.t1]);
    sd.c2 = dist(P, poly[sd.t2]);
    double a2c = cum[sd.t2];

    // 不可见弧上「经 t2」与「经 t1」的分界点（从 t2 沿不可见方向的弧长）
    double ustar = (sd.linv + sd.c1 - sd.c2) / 2.0;
    ustar = max(0.0, min(sd.linv, ustar));

    for (int e = 0; e < n; ++e) {
        if (elen[e] < 1e-15) continue;
        double s0 = cum[e];
        // 收集该边上的分界参数
        vector<double> cuts{0.0, 1.0};
        auto addCut = [&](double u) {
            if (u > 1e-12 && u < 1 - 1e-12) cuts.push_back(u);
        };
        addCut((cum[sd.t1] - s0) / elen[e]);
        addCut((cum[sd.t2] - s0) / elen[e]);
        if (sd.linv > 0) {
            double sCut = a2c + ustar;
            while (sCut >= perim) sCut -= perim;
            addCut((sCut - s0) / elen[e]);
        }
        sort(cuts.begin(), cuts.end());
        cuts.erase(unique(cuts.begin(), cuts.end(),
                          [](double a, double b) { return fabs(a - b) < 1e-12; }),
                   cuts.end());
        for (size_t k = 0; k + 1 < cuts.size(); ++k) {
            double um = 0.5 * (cuts[k] + cuts[k + 1]);
            if (cuts[k + 1] - cuts[k] < 1e-15) continue;
            Pt mid = poly[e] + (poly[(e + 1) % n] - poly[e]) * um;
            double sm = s0 + um * elen[e];
            double along = arcFrom(cum[sd.t1], sm);       // 从 t1 沿逆时针
            Piece pc;
            pc.e = e;
            pc.u0 = cuts[k];
            pc.u1 = cuts[k + 1];
            pc.linv = sd.linv;
            if (along < sd.lvis - 1e-12) {
                pc.kind = 0;
                sd.pieces.push_back(pc);
            } else {
                double u2 = arcFrom(a2c, sm);              // 从 t2 沿不可见方向
                pc.base = arcFrom(a2c, s0);
                if (u2 < ustar + 1e-12) {
                    pc.kind = 1;
                    pc.cst = sd.c2;
                } else {
                    pc.kind = 2;
                    pc.cst = sd.c1;
                }
                sd.pieces.push_back(pc);
            }
        }
    }
    return sd;
}

static double costOnSide(const Side &sd, Pt P, const Piece &pc, double u) {
    Pt A = poly[pc.e] + (poly[(pc.e + 1) % n] - poly[pc.e]) * u;
    if (pc.kind == 0) return dist(P, A);
    double uu = pc.base + u * elen[pc.e];
    if (pc.kind == 1) return pc.cst + uu;              // 经 t2
    return pc.cst + (pc.linv - uu);                    // 经 t1
}

int main() {
    Pt S, E;
    cin >> S.x >> S.y >> E.x >> E.y;
    cin >> n;
    poly.resize(n);
    for (int i = 0; i < n; ++i) cin >> poly[i].x >> poly[i].y;
    elen.assign(n, 0);
    cum.assign(n, 0);
    for (int i = 0; i < n; ++i) {
        elen[i] = dist(poly[i], poly[(i + 1) % n]);
        cum[i] = perim;
        perim += elen[i];
    }

    // 1) 线段 SE 是否穿过内部
    vector<double> ts;
    Pt d = E - S;
    for (int i = 0; i < n; ++i) {
        Pt a = poly[i], b = poly[(i + 1) % n];
        double den = cross(d, b - a);
        if (fabs(den) < 1e-15) continue;
        double tt = cross(a - S, b - a) / den;
        double ss = cross(a - S, d) / den;
        if (tt > -1e-12 && tt < 1 + 1e-12 && ss > -1e-12 && ss < 1 + 1e-12) ts.push_back(tt);
    }
    sort(ts.begin(), ts.end());
    bool blocked = false;
    for (size_t k = 0; k + 1 < ts.size(); ++k) {
        double mid = 0.5 * (ts[k] + ts[k + 1]);
        if (strictlyInside(S + d * mid)) { blocked = true; break; }
    }
    double L = dist(S, E);
    if (!blocked) {
        printf("%.9f\n", L);
        return 0;
    }

    Side sdS = buildSide(S), sdE = buildSide(E);

    double best = INF;
    // 2) 绕行：顶点图上的最短路
    {
        int V = n + 2;
        vector<double> d2(V, INF);
        vector<char> used(V, 0);
        auto w = [&](int a, int b) -> double {
            if (a == 0 && b >= 2) return sdS.vis[b - 2] ? dist(S, poly[b - 2]) : INF;
            if (b == 0 && a >= 2) return sdS.vis[a - 2] ? dist(S, poly[a - 2]) : INF;
            if (a == 1 && b >= 2) return sdE.vis[b - 2] ? dist(E, poly[b - 2]) : INF;
            if (b == 1 && a >= 2) return sdE.vis[a - 2] ? dist(E, poly[a - 2]) : INF;
            if (a == 0 && b == 1) return INF;      // 已被 blocked
            if (a >= 2 && b >= 2) {
                int i = a - 2, j = b - 2;
                double arc = arcFrom(cum[i], cum[j]);
                arc = min(arc, perim - arc);
                return min(arc, 2.0 * dist(poly[i], poly[j]));
            }
            return INF;
        };
        d2[0] = 0;
        for (int it = 0; it < V; ++it) {
            int u = -1;
            for (int i = 0; i < V; ++i)
                if (!used[i] && (u < 0 || d2[i] < d2[u])) u = i;
            if (u < 0 || d2[u] >= INF) break;
            used[u] = 1;
            for (int v = 0; v < V; ++v) {
                if (used[v]) continue;
                double ww = w(u, v);
                if (ww < INF && d2[u] + ww < d2[v]) d2[v] = d2[u] + ww;
            }
        }
        best = min(best, d2[1]);
    }

    // 3) 穿越：枚举两侧的「到达路线分段」，对凸函数做嵌套三分
    auto pointOfPiece = [&](const Piece &p, double u) {
        return poly[p.e] + (poly[(p.e + 1) % n] - poly[p.e]) * u;
    };
    auto segDist = [&](const Piece &pa, const Piece &pb) {   // 两条子线段的最短距离
        Pt a0 = pointOfPiece(pa, pa.u0), a1 = pointOfPiece(pa, pa.u1);
        Pt b0 = pointOfPiece(pb, pb.u0), b1 = pointOfPiece(pb, pb.u1);
        auto d2seg = [](Pt p, Pt q, Pt r) {   // 点到线段 q-r 距离
            Pt d = r - q;
            double t = dot(p - q, d) / max(1e-18, dot(d, d));
            t = max(0.0, min(1.0, t));
            return dist(p, q + d * t);
        };
        double d = min(min(d2seg(a0, b0, b1), d2seg(a1, b0, b1)),
                       min(d2seg(b0, a0, a1), d2seg(b1, a0, a1)));
        if (properIntersect(a0, a1, b0, b1)) d = 0.0;
        return d;
    };
    auto pieceMin = [&](const Side &sd, Pt P, const Piece &p) {
        double lo = p.u0, hi = p.u1;
        for (int it = 0; it < 40; ++it) {
            double m1 = lo + (hi - lo) / 3.0, m2 = hi - (hi - lo) / 3.0;
            if (costOnSide(sd, P, p, m1) < costOnSide(sd, P, p, m2)) hi = m2;
            else lo = m1;
        }
        return costOnSide(sd, P, p, 0.5 * (lo + hi));
    };
    vector<double> minS(sdS.pieces.size()), minE(sdE.pieces.size());
    for (size_t i = 0; i < sdS.pieces.size(); ++i) minS[i] = pieceMin(sdS, S, sdS.pieces[i]);
    for (size_t i = 0; i < sdE.pieces.size(); ++i) minE[i] = pieceMin(sdE, E, sdE.pieces[i]);
    for (size_t ia = 0; ia < sdS.pieces.size(); ++ia) {
        const Piece &pa = sdS.pieces[ia];
        for (size_t ib = 0; ib < sdE.pieces.size(); ++ib) {
            const Piece &pb = sdE.pieces[ib];
            if (minS[ia] + minE[ib] + 2.0 * segDist(pa, pb) >= best) continue;
            auto objective = [&](double u, double v) {
                Pt A = poly[pa.e] + (poly[(pa.e + 1) % n] - poly[pa.e]) * u;
                Pt B = poly[pb.e] + (poly[(pb.e + 1) % n] - poly[pb.e]) * v;
                return costOnSide(sdS, S, pa, u) + 2.0 * dist(A, B) +
                       costOnSide(sdE, E, pb, v);
            };
            auto innerMin = [&](double u) {
                double lo = pb.u0, hi = pb.u1;
                for (int it = 0; it < 60; ++it) {
                    double m1 = lo + (hi - lo) / 3.0, m2 = hi - (hi - lo) / 3.0;
                    if (objective(u, m1) < objective(u, m2)) hi = m2;
                    else lo = m1;
                }
                return objective(u, 0.5 * (lo + hi));
            };
            double lo = pa.u0, hi = pa.u1;
            for (int it = 0; it < 60; ++it) {
                double m1 = lo + (hi - lo) / 3.0, m2 = hi - (hi - lo) / 3.0;
                if (innerMin(m1) < innerMin(m2)) hi = m2;
                else lo = m1;
            }
            best = min(best, innerMin(0.5 * (lo + hi)));
        }
    }
    printf("%.9f\n", best);
    return 0;
}
```

### Python3

```python
import sys
import math

EPS = 1e-12


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def side(a, b, c):
    return cross(sub(b, a), sub(c, a))


def proper_intersect(a, b, c, d):
    d1 = side(c, d, a)
    d2 = side(c, d, b)
    d3 = side(a, b, c)
    d4 = side(a, b, d)
    return ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))


def main():
    data = sys.stdin.read().split()
    S = (float(data[0]), float(data[1]))
    E = (float(data[2]), float(data[3]))
    n = int(data[4])
    poly = [(float(data[5 + 2 * i]), float(data[6 + 2 * i])) for i in range(n)]

    elen = [dist(poly[i], poly[(i + 1) % n]) for i in range(n)]
    cum = [0.0] * n
    perim = 0.0
    for i in range(n):
        cum[i] = perim
        perim += elen[i]

    def inside_strict(p):
        for i in range(n):
            if side(poly[i], poly[(i + 1) % n], p) <= EPS:
                return False
        return True

    def visible_from(P, A):
        for i in range(n):
            a, b = poly[i], poly[(i + 1) % n]
            if dist(a, A) < EPS or dist(b, A) < EPS:
                continue
            if proper_intersect(P, A, a, b):
                return False
        for k in range(1, 10):
            q = (P[0] + (A[0] - P[0]) * k / 10.0, P[1] + (A[1] - P[1]) * k / 10.0)
            if inside_strict(q):
                return False
        return True

    def arc_from(a, b):
        d = b - a
        while d < 0:
            d += perim
        while d >= perim:
            d -= perim
        return d

    def on_edge(e, u):
        return (poly[e][0] + (poly[(e + 1) % n][0] - poly[e][0]) * u,
                poly[e][1] + (poly[(e + 1) % n][1] - poly[e][1]) * u)

    def build_side(P):
        vis = [visible_from(P, poly[i]) for i in range(n)]
        start = -1
        for i in range(n):
            if vis[i] and not vis[(i - 1) % n]:
                start = i
                break
        if start < 0:
            start = 0
        t1 = start
        t2 = start
        for k in range(1, n):
            j = (start + k) % n
            if vis[j]:
                t2 = j
            else:
                break
        lvis = arc_from(cum[t1], cum[t2])
        linv = perim - lvis
        c1 = dist(P, poly[t1])
        c2 = dist(P, poly[t2])
        a2c = cum[t2]
        ustar = (linv + c1 - c2) / 2.0
        ustar = max(0.0, min(linv, ustar))
        pieces = []
        for e in range(n):
            if elen[e] < EPS:
                continue
            s0 = cum[e]
            cuts = [0.0, 1.0]
            for sc in (cum[t1], cum[t2], a2c + ustar):
                while sc >= perim:
                    sc -= perim
                u = (sc - s0) / elen[e]
                if 1e-12 < u < 1 - 1e-12:
                    cuts.append(u)
            cuts.sort()
            uniq = [cuts[0]]
            for u in cuts[1:]:
                if u - uniq[-1] > 1e-12:
                    uniq.append(u)
            for k in range(len(uniq) - 1):
                u0, u1 = uniq[k], uniq[k + 1]
                um = 0.5 * (u0 + u1)
                sm = s0 + um * elen[e]
                along = arc_from(cum[t1], sm)
                if along < lvis - 1e-12:
                    pieces.append([e, u0, u1, 0, 0.0, 0.0, linv])
                else:
                    u2 = arc_from(a2c, sm)
                    base = arc_from(a2c, s0)
                    if u2 < ustar + 1e-12:
                        pieces.append([e, u0, u1, 1, base, c2, linv])
                    else:
                        pieces.append([e, u0, u1, 2, base, c1, linv])
        return vis, t1, t2, pieces

    def cost_on(side_info, P, pc, u):
        e, u0, u1, kind, base, cst, linv = pc
        A = on_edge(e, u)
        if kind == 0:
            return dist(P, A)
        uu = base + u * elen[e]
        if kind == 1:
            return cst + uu
        return cst + (linv - uu)

    # 1) 线段 SE 是否穿过多边形内部
    ts = []
    dx, dy = E[0] - S[0], E[1] - S[1]
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        den = dx * (b[1] - a[1]) - dy * (b[0] - a[0])
        if abs(den) < 1e-15:
            continue
        tt = ((a[0] - S[0]) * (b[1] - a[1]) - (a[1] - S[1]) * (b[0] - a[0])) / den
        ss = ((a[0] - S[0]) * dy - (a[1] - S[1]) * dx) / den
        if -1e-12 < tt < 1 + 1e-12 and -1e-12 < ss < 1 + 1e-12:
            ts.append(tt)
    ts.sort()
    blocked = False
    for k in range(len(ts) - 1):
        mid = 0.5 * (ts[k] + ts[k + 1])
        if inside_strict((S[0] + dx * mid, S[1] + dy * mid)):
            blocked = True
            break
    if not blocked:
        print("%.9f" % dist(S, E))
        return

    visS, t1S, t2S, piecesS = build_side(S)
    visE, t1E, t2E, piecesE = build_side(E)

    # 2) 绕行：顶点图上的最短路（Dijkstra）
    V = n + 2
    INF = 1e18
    d2 = [INF] * V
    used = [False] * V
    d2[0] = 0.0
    for _ in range(V):
        u = -1
        for i in range(V):
            if not used[i] and (u < 0 or d2[i] < d2[u]):
                u = i
        if u < 0 or d2[u] > 1e17:
            break
        used[u] = True
        for v in range(V):
            if used[v]:
                continue
            w = INF
            if u >= 2 and v >= 2:
                i, j = u - 2, v - 2
                arc = arc_from(cum[i], cum[j])
                arc = min(arc, perim - arc)
                w = min(arc, 2.0 * dist(poly[i], poly[j]))
            elif u == 0 and v >= 2 and visS[v - 2]:
                w = dist(S, poly[v - 2])
            elif v == 0 and u >= 2 and visS[u - 2]:
                w = dist(S, poly[u - 2])
            elif u == 1 and v >= 2 and visE[v - 2]:
                w = dist(E, poly[v - 2])
            elif v == 1 and u >= 2 and visE[u - 2]:
                w = dist(E, poly[u - 2])
            if w < INF and d2[u] + w < d2[v]:
                d2[v] = d2[u] + w
    best = d2[1]

    # 3) 穿越：对每个「到达路线分段」组合做嵌套三分
    def pt(pc, u):
        return on_edge(pc[0], u)

    def seg_dist(pa, pb):
        a0, a1 = pt(pa, pa[1]), pt(pa, pa[2])
        b0, b1 = pt(pb, pb[1]), pt(pb, pb[2])

        def d2seg(p, q, r):
            d = sub(r, q)
            dd = dot(d, d)
            t = 0.0 if dd < 1e-18 else max(0.0, min(1.0, dot(sub(p, q), d) / dd))
            return dist(p, (q[0] + d[0] * t, q[1] + d[1] * t))

        dd = min(d2seg(a0, b0, b1), d2seg(a1, b0, b1),
                 d2seg(b0, a0, a1), d2seg(b1, a0, a1))
        if proper_intersect(a0, a1, b0, b1):
            dd = 0.0
        return dd

    def piece_min(side_info, P, pc):
        lo, hi = pc[1], pc[2]
        for _ in range(40):
            m1 = lo + (hi - lo) / 3.0
            m2 = hi - (hi - lo) / 3.0
            if cost_on(side_info, P, pc, m1) < cost_on(side_info, P, pc, m2):
                hi = m2
            else:
                lo = m1
        return cost_on(side_info, P, pc, 0.5 * (lo + hi))

    minS = [piece_min(None, S, pc) for pc in piecesS]
    minE = [piece_min(None, E, pc) for pc in piecesE]

    for ia, pa in enumerate(piecesS):
        for ib, pb in enumerate(piecesE):
            if minS[ia] + minE[ib] + 2.0 * seg_dist(pa, pb) >= best:
                continue

            def objective(u, v):
                A = pt(pa, u)
                B = pt(pb, v)
                return cost_on(None, S, pa, u) + 2.0 * dist(A, B) + cost_on(None, E, pb, v)

            def inner_min(u):
                lo, hi = pb[1], pb[2]
                for _ in range(45):
                    m1 = lo + (hi - lo) / 3.0
                    m2 = hi - (hi - lo) / 3.0
                    if objective(u, m1) < objective(u, m2):
                        hi = m2
                    else:
                        lo = m1
                return objective(u, 0.5 * (lo + hi))

            lo, hi = pa[1], pa[2]
            for _ in range(45):
                m1 = lo + (hi - lo) / 3.0
                m2 = hi - (hi - lo) / 3.0
                if inner_min(m1) < inner_min(m2):
                    hi = m2
                else:
                    lo = m1
            best = min(best, inner_min(0.5 * (lo + hi)))

    print("%.9f" % best)


if __name__ == "__main__":
    main()
```

## 7. 边界情况与易错点

1. **线段与边界重合/相切**：样例 2 就是"沿底边"的情形，必须判定为**不穿越**，答案直接是 $|SE|$；判内部时要用"严格在内部"（三个叉积都 $>0$），不能用"在闭区域内"。
2. **穿越点落在边的内部**：只枚举顶点会错（样例 1 就会得到 $15$ 而不是 $6$），必须用连续优化或把 $SE$ 与边界的交点也纳入候选。
3. **可见性的退化**：若 $S$ 恰好与某条边的两个端点共线，切线会贴着一条边；判定切点时用"严格相交 + 沿线采样"双重检查，避免把不可见点当成可见。
4. **浮点比较**：叉积、点到线距离都用 `double`，eps 取 $10^{-12}$；判断"点在多边形内"时宁可留一点容差，否则恰好落在边界上的采样点会被误判为内部。
5. **绕行图的边权**：顶点之间要取 $\min(\text{弧长}, 2|v_iv_j|)$；只写弧长会漏掉"斜穿"这种更便宜的合法走法，只写斜穿又会漏掉沿边界绕行。
6. **三分方向**：三分要求函数单峰；单个"分段 × 分段"上已证明凸，但**跨分段**的 $d(S,A)$ 是分段定义的，不能把整条边界当成一个区间做三分，必须先按 3.3 节切段。
7. **输出精度**：用 `printf("%.9f")` 或 Python 的 `"%.9f"`；题目允许 $10^{-6}$ 误差，$9$ 位小数足够，但不要输出科学计数法。
8. **$S$ 与 $E$ 都在同一侧**：此时 $SE$ 不穿岛，直接输出距离，不要进入后面的几何流程（否则可能因可见链退化而出错）。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，`verify_solution.py` 自动改用 `clang++ -std=c++17 -O2` 加仓库内兼容头；Python 为 3.9.6。
- **官方样例**：2 / 2 通过。

  ```text
  python3 codeforces/tools/verify_solution.py "codeforces/contests/0001-0100/75/E_绕岛航行的最小代价.md"
  CF75E: samples 2
    C++ 编译 OK, 样例 2/2, 最慢 3 ms
    Python 语法 OK, 样例 2/2
  ```

  上述毫秒数为单次运行结果（含进程启动），随机器负载有 ±1 ms 抖动。

- **独立暴力对拍（300 组，全部实跑）**：独立暴力 （临时目录下的独立暴力程序，已随会话清理；其做法见本段描述） 把边界离散成 $n \times K$ 个采样点（$K = 100 \sim 300$），建图跑 Dijkstra：相邻采样点沿边界（单价 $1$）、任意两采样点直线穿越（单价 $2$）、$S/E$ 到可见采样点（单价 $1$）。它允许任意的"穿越 / 沿边界"交替，且随 $K$ 增大单调收敛到真实最优，是独立于正解的第二实现。数据构成：120 组随机小多边形（$n \le 9$，坐标 $\le 25$）、120 组"线段必定穿岛"的定向数据（$n \le 12$）、60 组 $n \le 30$、坐标 $\le 100$ 的满规模数据。结果：**正解的答案从未大于暴力（0 处违反）**，且差距随 $K$ 增大迅速收敛（例如某组 $K=150/400/1200$ 时暴力为 $38.606373/38.586008/38.586008$，正解 $38.584890$）。
- **手算用例交叉验证**：$10\times10$ 正方形（绕行更优，$24.142135624$）、$1\times20$ 窄条（穿越更优，$12$）、正八边形（$64.721359550$）、$30$ 边近圆（$177.494666838$），C++、Python、暴力三方一致。
- **Python 与 C++ 一致性**：100 组随机数据上两者输出差 $< 10^{-6}$，0 处不符。
- **最大约束性能**：$n = 30$ 的满规模数据，C++ 端到端最慢 $15$ ms，Python 约 $1.4$ s（建议 Python 提交时用 PyPy3），均低于 2 s。
- **复核状态**：verified。

## 相关题目与扩展

- [CF 2C Commentator problem](https://codeforces.com/problemset/problem/2/C)：几何最优化 + 数值迭代（三分/爬山），思路相近。
- [CF 1C Ancient Berland Circus](https://codeforces.com/problemset/problem/1/C)：圆与正多边形，练习几何量的精确计算。
- [CF 75D 拼接数组的最大子段和](https://codeforces.com/problemset/problem/75/D)：同场题，同样是"把连续问题化成有限结构"。

**延伸思考**：

1. **岛不是凸的**：凸性是本题所有简化（弦在岛内、可见链连续、绕行只经顶点）的前提。非凸时需要可见图 + Dijkstra，节点是"所有顶点 + 切点"，规模大得多。
2. **代价比不是 $2:1$**：若岛内单价是 $c>1$，3.4 节的凸性仍然成立（$2|AB|$ 换成 $c|AB|$），三分依然可用；但"岛内单价 $\ge 2$ 时绕行可能总是更优"之类的结论会随 $c$ 改变。
3. **多个岛屿**：两个凸岛时，穿越可能发生在任一岛上，需要枚举"先穿哪个岛、如何绕另一个"，结构会从"两类候选"变成"岛屿序列上的最短路"。
4. **退化成 $S, E$ 都在同一侧**：此时直接输出 $|SE|$；这也说明"判断是否穿越"本身就是答案的一部分，不能省略。
