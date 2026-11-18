# Codeforces 遥远城市 题解

## 1. 题目概述

- **标题 / 题号**：遥远城市（Codeforces 2258C，英文名 Far Cities）
- **链接**：https://codeforces.com/problemset/problem/2258/C
- **来源**：Codeforces Round 1118 (Div. 2) · Problem C
- **难度**：1600（1250 分）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：交互、树、双指针（单调增量探测）

**题意**：评测机里藏着一棵 $n$ 个点的树，只能靠询问了解它。一次询问给出 $u,v,d$（$1\le u,v\le n$，$0\le d\le n$），评测机回答 $1$ 当且仅当 $\mathrm{dist}(u,v)\ge d$，否则回答 $0$。最多询问 $3n$ 次，最后输出一条直径 `! u v d`：$u,v$ 为直径两端，$d$ 为它们的距离（$0\le d\le n-1$）。

多测格式：第一行 $t$，每组先给 $n$，随后**你的程序**发问、评测机逐条回 $0/1$。评测机非自适应（树在开局固定），可放心按固定策略提问；若读到 $-1$ 或输入流关闭，必须立刻退出。

**约束**：

- $1\le t\le 500$，$2\le n\le 1000$，$\sum n\le 1000$
- 每组询问数 $\le 3n$，即**每个点平均只有 3 次机会**
- 询问的 $d\in[0,n]$，输出的 $d\in[0,n-1]$
- 交互题：每条询问后 flush；答案不计入询问次数

## 2. 示例

官方样例。交互题的“输入”是评测机回给你的 $0/1$，“输出”是程序打印的内容（原样）：

```text
输入：
3
4
1
0
0
0
2
4
1
1
1
1
0
0
0
0
```

```text
输出：
? 1 2 1
? 1 2 2
? 2 3 2
? 3 4 2
! 1 4 3
! 1 2 1
? 1 2 1
? 1 3 1
? 1 4 1
? 3 4 2
? 3 4 3
? 1 2 2
? 1 3 2
? 1 4 2
! 4 2 2
```

按题面 Note，三棵隐藏树依次是路径 $1-2-3-4$、单边 $1-2$、以 $1$ 为中心的星。第 1 组用掉 4 条询问、消耗输入的 $1,0,0,0$，给出 `! 1 4 3`；第 2 组 $n=2$ 不询问直接给 `! 1 2 1`；第 3 组用掉 8 条询问、消耗剩下的 $1,1,1,1,0,0,0,0$，给出 `! 4 2 2`。样例序列只是出题人写法之一，任何合法序列都行（本仓库实现在这三棵树上分别用 $9,3,8$ 次）。

**自造示例**（本实现实跑，$n=6$：$1\text{-}2\text{-}3\text{-}4\text{-}5$ 再挂 $2\text{-}6$）：$d$ 先推到 $4$（$A=5$），随后查询全回 $0$，输出 `! 5 1 4`，$\mathrm{dist}(5,1)=4$ 即直径，共 $14=2\cdot5+4$ 次，与全源 BFS 一致。

## 3. 解题思路

### 3.1 暴力思路

树已知时两次 BFS 即可求直径，$O(n)$。但这里只有“距离是否 $\ge d$”一位信息：对每个点二分深度约需 $n\log_2 n\approx10^4$ 次询问，超限 3 倍；瓶颈在于**每定位一次真实距离都要额外 $\log n$ 次二分**。

### 3.2 核心观察：最远点即端点 + 单调增量探测

![两次扫描：最远点一定是直径端点](images/cf2258_c_double_sweep.svg)

**观察 1（直径端点引理）**：从任意点 $r$ 出发，离 $r$ 最远的点 $A$ 一定是某条直径的端点。于是两次扫描即可：由 $1$ 求 $A$，再由 $A$ 求 $B$，$d=\mathrm{dist}(A,B)$ 即直径（证明见 §5 引理 3）。

**观察 2（增量探测）**：求最远点要取 $\max$，但我们不需要每个点的精确距离，只需知道“有没有人超过当前最大值”。维护 $d=$ 已确认的最大距离、$last=$ 一个满足 $\mathrm{dist}(r,last)=d$ 的点；对每个新点 $v$ **只问一次** $\mathrm{dist}(r,v)\ge d+1$：

- 回 $0$：$\mathrm{dist}(r,v)\le d$，不动（花掉这 1 次）；
- 回 $1$：$d\leftarrow d+1$、$last\leftarrow v$，并**对同一个 $v$ 再问** $d+1$，直到回 $0$。

于是：每次回 $1$ 只让 $d$ 加 $1$，不会跳过头；循环结束时 $\mathrm{dist}(r,v)\le d$，而最后一次回 $1$ 时已知 $\mathrm{dist}(r,v)\ge d$，故 $\mathrm{dist}(r,v)=d$，$last$ 与根的距离**精确等于 $d$**，不变式维持；又因 $d$ 全局共享，一轮下来 $d$ 的净增量恰是 $\mathrm{ecc}(r)$，这一轮询问数就是 $(n-1)+\mathrm{ecc}(r)$。

**观察 3（第二轮不重置 $d$）**：第一轮结束时 $d=\mathrm{ecc}(1)=\mathrm{dist}(1,A)$，把它当第二轮初值、初始 $last=1$（因 $\mathrm{dist}(A,1)=d$），不变式继续成立。第二轮 $d$ 从 $\mathrm{ecc}(1)$ 推到 $\mathrm{ecc}(A)=D$，净增量只有 $D-\mathrm{ecc}(1)$，于是

$$2(n-1)+D\ \le\ 2(n-1)+(n-1)=3n-3\ <\ 3n$$

正好卡进限制且余量恒正。若第二轮重置 $d$，总询问为 $2(n-1)+\mathrm{ecc}(1)+D$，路径（$1$ 在一端）上是 $4n-4$，直接超限。

### 3.3 算法流程

![算法流程与查询预算](images/cf2258_c_incremental_flow.svg)

```text
每组:
  d ← 0, last ← 1                      # 不变式: dist(1, last) = d
  for v = 2 … n:                        # 第一轮
      while ask(1, v, d+1): d ← d+1, last ← v
  A ← last                              # dist(1,A) = d = ecc(1)，A 为直径端点
  B ← 1                                 # 不变式: dist(A, B) = d
  for v = 1 … n (v ≠ A):                # 第二轮，d 不重置
      while ask(A, v, d+1): d ← d+1, B ← v
  输出 "! A B d"                         # d = ecc(A) = D
```

查询预算逐项：基础询问每点恰好一次，两轮共 $2(n-1)$；增量询问第一轮 $\mathrm{ecc}(1)$ 次、第二轮 $D-\mathrm{ecc}(1)$ 次，合计 $D$ 次；总计 $2(n-1)+D\le 3n-3$。

### 3.4 示例演算

![两棵样例树的真实询问轨迹](images/cf2258_c_walkthrough.svg)

路径 $1-2-3-4$（样例 1）的真实轨迹：`? 1 2 1`→$1$（$d:0\to1$）、`? 1 2 2`→$0$（到顶）、`? 1 3 2`→$1$（$d:1\to2$）、`? 1 3 3`→$0$、`? 1 4 3`→$1$（$d:2\to3$）、`? 1 4 4`→$0$，得 $d=3,A=4$；第二轮以 $4$ 为根、$d$ 仍为 $3$，`? 4 1 4`、`? 4 2 4`、`? 4 3 4` 全回 $0$，输出 `! 4 1 3`，共 $9=2\cdot3+3$ 次。星 $\{1\text{-}2,1\text{-}3,1\text{-}4\}$（样例 3）用 $8=2\cdot3+2$ 次：第一轮 $d$ 只到 $1$（$1$ 是中心），第二轮从 $d=1$ 推到 $2$。

§3.2 配图那棵 $10$ 点树（三臂长 $4,3,2$）：$\mathrm{ecc}(1)=4$（$A=10$）、$\mathrm{ecc}(10)=7$（$B=7$），两轮共 $9+4+9+3=25=2(n-1)+D$，而 $3n=30$。

## 4. 算法细节

1. **不变式维护**：只有回 $1$ 时才 `d++` 与 `last=v`；回 $0$ 时两者都不动。`last` 必须始终是**与当前根距离恰为 $d$** 的点，这是第二轮能接着用的前提。
2. **第二轮初值**：`d` 保留第一轮结果，$B$ 初始化为 $1$ 而非 $A$——因 $\mathrm{dist}(A,1)=d$ 恰好维持不变式；若初始化成 $A$ 就变成 $0\ne d$，不变式破坏。
3. **参数范围**：$d\le D\le n-1$，故 `d+1 ≤ n` 恒合法；$d=n-1$ 时问 $n$ 只会回 $0$，循环必然终止。
4. **多测清空**：$t$ 可达 $500$，每组开头重置 `d=0, last=1`；“不重置”只指同一组内第一轮→第二轮。
5. **$A\ne 1$**：$n\ge2$ 时 $\mathrm{ecc}(1)\ge1$，故 $A\ne1$，第二轮遍历 $v=1..n$ 时跳过 $v=A$ 不会漏掉 $1$ 号点。
6. **I/O**：每条询问与答案后都 flush；读到 `-1`/EOF 立刻 `exit(0)`，否则可能拿到 Idleness limit exceeded。
7. **输出**：`! u v d` 直接输出原编号（1-indexed），$d$ 必须是这两点的真实距离，任意一条直径均可。
8. **常数**：每点至多 $1+\Delta$ 次询问（$\Delta$ 为该点造成的增量），而 $\sum\Delta\le n-1$，所以询问数稳定为 $2n-2+D$，与树的形状无关，路径最坏 $2997$ 次。

## 5. 正确性证明

**引理 1（不变式）**：对固定根 $r$，按上述循环处理完任意前缀 $S$ 后，$d=\max_{v\in S}\mathrm{dist}(r,v)$ 且 $\mathrm{dist}(r,last)=d$。

**证明**：初始 $S=\{r\}$、$d=0=\mathrm{dist}(r,r)$。设处理 $v$ 前成立。若循环体未执行，查询已回 $0$，即 $\mathrm{dist}(r,v)\le d$，最大值与 $last$ 不变。若执行了 $k\ge1$ 次，第 $k$ 次执行时阈值为 $d+k-1$ 且回 $1$，故 $\mathrm{dist}(r,v)\ge d+k$；循环在阈值 $d+k$ 处首次回 $0$，故 $\mathrm{dist}(r,v)\le d+k$，于是 $\mathrm{dist}(r,v)=d+k$。新 $d'=d+k=\mathrm{dist}(r,v)$，新 $last=v$ 满足 $\mathrm{dist}(r,v)=d'$，其余点距离 $\le d\le d'$，最大值正是 $d'$。∎

**引理 2（询问计数）**：一轮（$n-1$ 个点）的询问数等于 $(n-1)+$ 该轮 $d$ 的净增量。

**证明**：每点贡献 $1$ 次基础询问；每次回 $1$ 恰好令 $d$ 增 $1$，对同一点的续问次数等于它造成的回 $1$ 次数，相加即得。∎

**引理 3（最远点是直径端点）**：设 $D$ 为直径、$A$ 使 $\mathrm{dist}(r,A)$ 最大，则 $\mathrm{ecc}(A)=D$。

**证明**：取直径 $(x,y)$，$\mathrm{dist}(x,y)=D$。$x,y,A$ 的极小连通子树是“Y”形，设分叉点 $m$，臂长 $h=\mathrm{dist}(A,m)$、$c_1=\mathrm{dist}(m,x)$、$c_2=\mathrm{dist}(m,y)$（$A$ 落在路径 $x\text{-}y$ 上时取 $m=A,h=0$，仍有 $c_1+c_2=D$）。因 $D$ 是直径上界，$\mathrm{dist}(A,x)=h+c_1\le D$、$\mathrm{dist}(A,y)=h+c_2\le D$，即 $h\le\min(c_1,c_2)$。

设 $w$ 为 $r$ 到该子树的投影，则 $\mathrm{dist}(r,z)=\mathrm{dist}(r,w)+\mathrm{dist}(w,z)$；由 $A$ 最远得 $\mathrm{dist}(w,A)\ge\max(\mathrm{dist}(w,x),\mathrm{dist}(w,y))$。

- $w$ 在 $x$ 臂上（$y$ 臂对称）、距 $m$ 为 $t$：$\mathrm{dist}(w,A)=t+h$、$\mathrm{dist}(w,y)=t+c_2$，得 $h\ge c_2$；结合 $h\le\min(c_1,c_2)$ 有 $h=c_2\le c_1$，故 $\mathrm{dist}(A,x)=h+c_1=c_2+c_1=D$。
- $w$ 在 $A$ 臂上、距 $m$ 为 $s$：$\mathrm{dist}(w,A)=h-s$、$\mathrm{dist}(w,x)=s+c_1$，得 $h\ge c_1+2s$ 且同法 $h\ge c_2+2s$，故 $h\ge\max(c_1,c_2)$；与 $h\le\min(c_1,c_2)$ 合并只能是 $c_1=c_2=h=D/2$，故 $\mathrm{dist}(A,x)=h+c_1=D$。
- $w=m$：$h\ge\max(c_1,c_2)$ 且 $h\le\min(c_1,c_2)$，故 $c_1=c_2=h=D/2$，$\mathrm{dist}(A,y)=h+c_2=D$。

三种情形都有 $\max(\mathrm{dist}(A,x),\mathrm{dist}(A,y))=D$，又 $D$ 是上界，故 $\mathrm{ecc}(A)=D$。∎

**定理**：算法输出的 $(A,B,d)$ 满足 $\mathrm{dist}(A,B)=d=D$，且询问数 $2(n-1)+D\le3n-3<3n$。

**证明**：第一轮由引理 1 得 $d=\mathrm{ecc}(1)$、$\mathrm{dist}(1,A)=d$，且 $n\ge2$ 时 $d\ge1$ 故 $A\ne1$；由引理 3 得 $\mathrm{ecc}(A)=D$。第二轮以 $A$ 为根、初值 $d=\mathrm{dist}(A,1)$、$B=1$ 满足引理 1 的初始条件，故结束时 $d=\mathrm{ecc}(A)=D$ 且 $\mathrm{dist}(A,B)=d$。询问数由引理 2 为 $(n-1)+\mathrm{ecc}(1)+(n-1)+(D-\mathrm{ecc}(1))=2(n-1)+D\le3n-3$。∎

## 6. 复杂度分析

- **询问次数**：恒为 $2(n-1)+D$，上界 $3n-3$；$n=1000$ 的路径取到 $2997$，为全部算例中的最大值。
- **时间**：每组 $O(n+D)=O(n)$ 次询问与读入，总量 $O(\sum n)$；程序自身计算量 $O(1)$（只维护 $d,last$）。空间 $O(1)$，连树都不用存。
- **实测**：本地自写交互评测机 + 管道回环，$n=1000$ 路径 C++17 约 $0.05$ s、Python3 约 $0.07$ s（含进程启动），$2$ s 时限余量在 $30$ 倍以上；真实评测成本主要是 $\le3000$ 次往返 I/O，同样宽裕。

## 7. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

static int n;

static int ask(int u, int v, int d) {
    cout << "? " << u << " " << v << " " << d << "\n";
    cout.flush();
    int r;
    if (!(cin >> r)) exit(0);
    if (r < 0) exit(0);          // 交互器关闭：立即退出
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        cin >> n;
        // ---- 第一轮：以 1 为根，找离 1 最远的点 A（必为直径端点） ----
        int d = 0, last = 1;      // 不变式：dist(root, last) = d
        for (int v = 2; v <= n; ++v)
            while (ask(1, v, d + 1)) { ++d; last = v; }
        int A = last;             // 直径端点，dist(1, A) = d
        // ---- 第二轮：以 A 为根，不重置 d（此时 dist(A, 1) = d） ----
        int B = 1;                // 距 A 恰为 d 的已知点
        for (int v = 1; v <= n; ++v) {
            if (v == A) continue;
            while (ask(A, v, d + 1)) { ++d; B = v; }
        }
        cout << "! " << A << " " << B << " " << d << "\n";
        cout.flush();
    }
    return 0;
}
```

### Python3

```python
import sys


def main():
    inp = sys.stdin.buffer
    out = sys.stdout

    line = inp.readline()
    if not line:
        return
    t = int(line)

    def ask(u, v, d):
        out.write("? %d %d %d\n" % (u, v, d))
        out.flush()
        r = inp.readline()
        if not r:
            sys.exit(0)
        r = int(r)
        if r < 0:
            sys.exit(0)
        return r

    for _ in range(t):
        n = int(inp.readline())
        d = 0
        last = 1
        for v in range(2, n + 1):          # 第一轮
            while ask(1, v, d + 1):
                d += 1
                last = v
        a = last
        b = 1
        for v in range(1, n + 1):          # 第二轮，d 不重置
            if v == a:
                continue
            while ask(a, v, d + 1):
                d += 1
                b = v
        out.write("! %d %d %d\n" % (a, b, d))
        out.flush()


main()
```

## 8. 边界情况与易错点

1. **$n=2$**：第一轮 `? 1 2 1`→$1$、`? 1 2 2`→$0$，得 $d=1,A=2$；第二轮只剩 $1$ 可问，`? 2 1 2`→$0$，输出 `! 2 1 1`，共 $3$ 次（$3n=6$ 的一半）。
2. **第二轮重置 `d`**：最致命的错误。重置后总询问变 $2(n-1)+\mathrm{ecc}(1)+D$，$1$ 在路径端点时 $\mathrm{ecc}(1)=D=n-1$，需要 $4n-4$ 次，直接超限。
3. **$B$ 初值写成 $A$**：此时 $\mathrm{dist}(A,B)=0\ne d$，一旦后续没有点突破 $d$，就会输出 `! A A d`，距离对不上；正确初值是 $1$。
4. **忘记 flush / 不处理 $-1$**：交互题每条输出后必须 flush；读到 $-1$ 或 EOF 要立即退出，否则可能拿到 Idleness 而非清晰的 WA。
5. **$d$ 的范围**：询问参数必须 $\le n$，因 $d\le D\le n-1$ 故 `d+1 ≤ n` 恒成立，不必额外判；输出的 $d$ 必须 $\le n-1$。
6. **多测变量残留**：$t$ 可到 $500$（$\sum n\le1000$），每组的 `d`、`last` 都要重新初始化，不要复用上一组的 $A$。
7. **端点与长度不一致**：评测机不接受“长度对但端点不对”，$d$ 必须是输出点对的真实距离；用 `last` 记录端点天然保证一致。
8. **想当然地二分**：每次回 $1$ 后用二分定位真实距离，会额外花 $\log$ 次，合计 $2n+2\sum\log(\text{gap})$，在“深度每隔 $2\sim3$ 跳一次”的路径上超过 $3n$；增量法把定位成本摊到 $D$ 且全局共享，才是安全写法。

## 相关题目与扩展

- [Codeforces 455C Civilization](https://codeforces.com/problemset/problem/455/C)：并查集维护每棵树的直径，合并时用端点交叉算新直径，是“直径端点性质”的另一处应用。
- [Codeforces 1405D Tree Tag](https://codeforces.com/problemset/problem/1405/D)：追逃判定完全由直径与两点距离决定，可与“两次扫描”对照。
- [LeetCode 543. 二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/)：树形 DP（后序返回高度）求直径，与“两次扫描／交互探测”是同一问题的两种信息模型。

**延伸思考**：

1. 若询问直接返回精确距离，两次 BFS 用 $2(n-1)$ 次询问即可，不需要“增量”这层设计；本题的难度正来自只有一位比较信息。
2. $2(n-1)+D$ 已贴近“每点至少问一次”的 $2(n-1)$ 下界：路径上 $D=n-1$，本算法用 $3n-3$，几乎用满 $3n$。能否在不牺牲正确性的前提下再压低常数，值得玩味。
3. 若评测机改成**自适应**（随询问换树），增量法的论证失效——本文结论都依赖“树在开局固定”。