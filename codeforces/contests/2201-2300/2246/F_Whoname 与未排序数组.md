# Codeforces 2246F Whoname 与未排序数组 题解

## 1. 题目概述

- **标题 / 题号**：Whoname 与未排序数组（Codeforces 2246F，英文名 Whoname and Unsorted Array）
- **链接**：https://codeforces.com/problemset/problem/2246/F
- **来源**：Codeforces Round 1108 (Div. 2) · Problem F（UTC 2026-07-12）
- **难度**：2900（2750 分）
- **限制**：时间 2 s / 内存 256 MB
- **标签**：构造、置换奇偶性、不变量

**题意**：给定长度为 $n$ 的排列 $p$。一次操作选下标 $i$（$1\le i\le n-1$），把 $p_i$ 搬到位置 $1$、$p_{i+1}$ 搬到位置 $n$，其余元素保持相对顺序：

$$p=[p_1,\dots,p_n]\ \longrightarrow\ p'=[\,p_i,\ p_1,\dots,p_{i-1},\ p_{i+2},\dots,p_n,\ p_{i+1}\,]$$

要求给出**不超过 $4n$ 次**操作的序列使 $p_i=i$，或判定无解输出 $-1$。多测：首行 $t$，每组给 $n$ 与排列。

**约束**：

- $2\le n\le 5000$，$1\le t\le 1000$，$\sum n\le 5000$
- 输出先给操作数 $x\le 4n$，再给 $x$ 个下标，每个都在 $[1,n-1]$
- 保证输入是排列；有解时保证存在长度 $\le 4n$ 的解

## 2. 示例与观察
官方样例（$t=4$；本题输出不唯一，只要求合法且不超过 $4n$）：

```text
输入
4
2
2 1
3
3 2 1
5
1 5 4 3 2
4
4 3 2 1

输出
-1
3
1 2 1
4
2 2 3 2
3
1 3 1
```

本文程序的输出（同样合法，长度也都 $\le 4n$）：`-1`；`5 / 2 2 1 2 1`；`12 / 2 1 4 3 2 1 4 1 2 2 2 1`；`8 / 3 2 1 3 2 1 3 1`。

> 💡 输出**不需要最短**。官方第 3 组只用 4 步，我们用了 12 步，但都满足 $\le 4n$（第 3 组 $4n=20$）且确实排好了序（逐条模拟验证过）。

## 3. 解题思路

### 3.1 暴力思路

状态空间是 $n!$ 个排列。把"一次操作能到达的状态"反向建图做 BFS，可求出最短步数：$n=5$ 最坏 5 步、$n=7$ 最坏 7 步；$n\le7$ 时**所有**排列可解，$n=8$ 时恰好一半（偶排列）可解。这说明答案很短、每步应能稳定归位一个元素，但 $n=5000$ 时状态爆炸，必须构造。

### 3.2 核心观察：把 $1,2,\dots,x-1$ 压成有序后缀

![一次操作等于前缀右循环加后缀左循环，恰好 n 减 2 个对换](../../../images/cf2246f_operation_model.svg)

按切口 $i$ 把数组分成左右两段，操作就是**左段右循环一位、右段左循环一位**：

- $p_i$ 被顶到队首、$p_{i+1}$ 被顶到队尾，其余元素相对顺序完全不变；
- 换个说法：挑出相邻对 $(p_i,p_{i+1})$ 分别扔到两端；逆操作是"取出首尾两个元素，成对插回中间"。

第一个硬结论来自**对换计数**：左段右循环是 $i-1$ 个相邻对换，右段左循环是 $n-i-1$ 个，合计 $n-2$ 个。故每次操作对奇偶性的改变量固定为 $(-1)^{n-2}$。

接下来盯住队尾，维护不变量

$$\text{当前数组}=[\,U,\ 1,\ 2,\ \dots,\ x-1\,],\qquad U \text{ 是 } \{x,x+1,\dots,n\} \text{ 的任意排列}$$

想把 $x$ 接到尾巴上，只有两种情况：

![不变量：队尾有序、队首是乱序的 U，x 在队首时三步修补](../../../images/cf2246f_suffix_invariant.svg)

- **情形 1（$x$ 在位置 $i\ge2$）**：执行 $\mathrm{apply}(i-1)$，$p_i=x$ 飞到队尾、$p_{i-1}$ 飞到队首（乱序区，无所谓），尾巴变成 $[1..x-1,x]$，**1 步**。
- **情形 2（$x$ 就在队首）**：$\mathrm{apply}(0)$ 不存在，需**三步修补**：
  1. $\mathrm{apply}(2)$：$x$ 挪到位置 2，$U_1$ 顶到队首、$U_2$ 掉到队尾；
  2. $\mathrm{apply}(1)$：只做后缀左循环、不动 $p_1$，$x$ 落到队尾，但 $U_2$ 卡在尾巴前面；
  3. $\mathrm{apply}(n-1)$：只做前缀右循环、不动 $p_n=x$，把碍事的 $U_2$ 顶回队首。

  代价 **3 步**，不变量依旧成立。

### 3.3 算法流程

![收尾只剩两种形态 A 与 B](../../../images/cf2246f_tail_cases.svg)

1. **判无解**：$n$ 为偶数且 $p$ 是奇排列 $\Rightarrow$ 输出 $-1$（引理 1）。
2. **主循环**：$x=1,2,\dots,n-2$ 依次归位；$x$ 在位置 $i\ge2$ 就 $\mathrm{apply}(i-1)$，在队首就 $\mathrm{apply}(2),\mathrm{apply}(1),\mathrm{apply}(n-1)$。
3. **收尾**：循环结束时前两个元素恰为 $\{n-1,n\}$，只有两种形态：
   - 形态 A $[n-1,n,1,\dots,n-2]$：$\mathrm{apply}(2),\mathrm{apply}(1),\mathrm{apply}(n-1),\mathrm{apply}(1)$，共 4 步；
   - 形态 B $[n,n-1,1,\dots,n-2]$：$\mathrm{apply}(1)$ 得 $[n,1,2,\dots,n-1]$，再连续 $n-2$ 次 $\mathrm{apply}(2)$ 得 $[1,n,2,\dots,n-1]$，最后 $\mathrm{apply}(1)$ 收工，共 $n$ 步。形态 B 只在 $n$ 为奇数时出现。
4. **输出**：总步数 $\le 3(n-2)+\max(4,n)$，即 $n\ge4$ 时 $\le 4n-6$、$n=3$ 时 $\le 7$，一律 $\le 4n$。

### 3.4 示例演算

![n 等于 4 时 p 为 4 3 2 1 的 8 步走查](../../../images/cf2246f_walkthrough.svg)

以样例 4（$n=4$，$p=[4,3,2,1]$）为例：$x=1$ 在位置 4，一步归位；$x=2$ 正好在队首，走三步修补；数组变成 $[3,4,1,2]$ 后进入形态 A，4 步收尾，合计 8 步（$\le16$）：

$$[4,3,2,1]\xrightarrow{3}[2,4,3,1]\xrightarrow{2}[4,2,1,3]\xrightarrow{1}[4,1,3,2]\xrightarrow{3}[3,4,1,2]$$

$$[3,4,1,2]\xrightarrow{2}[4,3,2,1]\xrightarrow{1}[4,2,1,3]\xrightarrow{3}[1,4,2,3]\xrightarrow{1}[1,2,3,4]$$

即第 $1\sim8$ 步依次用下标 $3,2,1,3,2,1,3,1$。

## 4. 算法细节

1. **多测清空**：每组重读 $n$ 与 $p$，`ans` 清空；$x=0$ 时第二行输出空行。
2. **奇偶判定用环分解**：奇偶性 $=(n-\text{环数})\bmod 2$，$O(n)$ 完成，避免 $O(n^2)$ 数逆序对。
3. **`apply` 用两次 `std::rotate`**：先右循环前缀 $[0,i-1]$（`rotate(begin,begin+i-1,begin+i)`），再左循环后缀 $[i,n-1]$（`rotate(begin+i,begin+i+1,end)`）。$O(n)$、零额外内存；$i=1$ 或 $i=n-1$ 时其中一次退化为空操作。
4. **找位置直接扫**：每个 $x$ 线性扫一遍（$O(n)$），总计 $O(n^2)$，比维护 `pos[]` 每次 $O(n)$ 更新更好写也更稳。
5. **循环上界是 $n-2$ 不是 $n-1$**：三步修补要求 $|U|\ge3$；若做到 $n-1$，$|U|=2$ 时 $\mathrm{apply}(2)$ 会把有序尾巴转坏。
6. **小 $n$ 不必特判**：$n=3$ 时 $\mathrm{apply}(2)$ 与 $\mathrm{apply}(n-1)$ 是同一下标，公式自动成立；只有 $n=2$ 的 $[1,2]$ 要单独输出 0。
7. **已排好直接输出 0**，既省操作也让输出干净。
8. **I/O**：输出总量 $\le4\sum n=2\times10^4$ 个整数，`sync_with_stdio(false)` 足够，别用 `endl`。

## 5. 正确性证明

**引理 1（对换数）**：一次操作恰是 $(i-1)+(n-i-1)=n-2$ 个相邻对换，故奇偶性改变当且仅当 $n$ 为奇数。∎

**引理 2（一步归位）**：若当前数组为 $[U,1,2,\dots,x-1]$ 且 $x$ 在位置 $i\ge2$，则 $\mathrm{apply}(i-1)$ 之后为 $[U',1,2,\dots,x-1,x]$，其中 $U'$ 是 $\{x+1,\dots,n\}$ 的排列。

**证明**：$\mathrm{apply}(i-1)$ 把 $p_{i-1}$ 送到位置 $1$、$p_i=x$ 送到位置 $n$，其余元素保持相对顺序。有序尾巴整段位于 $i$ 之后，只整体左移一位、仍然连续；$x$ 落到位置 $n$，正好接在尾巴后面。∎

**引理 3（三步修补）**：若当前数组为 $[x,U_1,\dots,U_{m-1},1,\dots,x-1]$ 且 $m=|U|\ge3$，则依次执行 $\mathrm{apply}(2),\mathrm{apply}(1),\mathrm{apply}(n-1)$ 后为 $[U_2,U_1,U_3,\dots,U_{m-1},1,\dots,x-1,x]$。

**证明**：逐步展开：① $\mathrm{apply}(2)$ 得 $[U_1,x,U_3,\dots,U_{m-1},1,\dots,x-1,U_2]$；② $\mathrm{apply}(1)$ 时 $p_1=U_1$ 不动、后缀左循环，得 $[U_1,U_3,\dots,U_{m-1},1,\dots,x-1,U_2,x]$；③ $\mathrm{apply}(n-1)$ 时 $p_{n-1}=U_2$ 被顶到队首、$p_n=x$ 不动，得 $[U_2,U_1,U_3,\dots,U_{m-1},1,\dots,x-1,x]$。三步都只在两端搬运元素，中间段相对顺序不变。∎

**引理 4（收尾）**：主循环结束后数组必为 $[n-1,n,1,\dots,n-2]$ 或 $[n,n-1,1,\dots,n-2]$，两种形态都能在 $\le n$ 步内排好。

**证明**：由引理 2、3 归纳，循环后 $U$ 只剩两个元素、恰为 $\{n-1,n\}$（形态 B 的逆序数为 $2n-3$，$n$ 偶数时是奇排列，故可解输入只会遇到形态 A）。

- 形态 A：$\mathrm{apply}(2)$ 得 $[n,n-1,2,\dots,n-2,1]$，$\mathrm{apply}(1)$ 得 $[n,2,\dots,n-2,1,n-1]$，$\mathrm{apply}(n-1)$ 得 $[1,n,2,\dots,n-1]$，最后 $\mathrm{apply}(1)$ 得 $[1,2,\dots,n]$。
- 形态 B：$\mathrm{apply}(1)$ 把 $n$ 留在队首、$n-1$ 换到队尾，得 $[n,1,2,\dots,n-1]$。记 $A_t$ 为之后第 $t$ 次 $\mathrm{apply}(2)$ 的结果，直接验证

$$A_t=[n,1,t+2,\dots,n-1,2,\dots,t+1]\ (t\text{ 偶}),\qquad A_t=[1,n,t+2,\dots,n-1,2,\dots,t+1]\ (t\text{ 奇})$$

  代入 $t=n-2$（$n$ 奇故为奇数）得 $A_{n-2}=[1,n,2,\dots,n-1]$，再 $\mathrm{apply}(1)$ 即排好。∎

**定理**：若 $n$ 为奇数，或 $n$ 为偶数且 $p$ 为偶排列，则 §3.3 的构造输出合法序列且长度 $\le4n$；否则无解。

**证明**：必要性由引理 1（$n$ 偶数时只有偶排列可达）。充分性：由引理 2、3 归纳，每轮让一个 $x$ 归位且不变量保持；取到 $x=n-2$ 后由引理 4 收尾。长度：主循环每轮 1 或 3 步，共 $\le3(n-2)$；收尾 $\max(4,n)$，合计 $\le3(n-2)+\max(4,n)\le4n$（$n\ge4$ 时为 $4n-6$，$n=3$ 时为 7）。$n=2$ 时仅 $[1,2]$ 可解、0 步。∎

## 6. 复杂度分析

- **时间**：主循环 $n-2$ 轮，每轮找位置 $O(n)$、再执行 1 或 3 次 $O(n)$ 的循环移位，总计 $O(n^2)$；$\sum n\le5000$ 时最坏约 $4\times5000^2/2\approx5\times10^7$ 次基本操作。
- **实测**（Apple clang，$O_2$）：$n=5000$ 随机 16 ms、$n=5000$ 逆序 19 ms、$t=1251$ 组小数据（$\sum n\approx5000$）10 ms；Python3 同数据约 245 / 432 / 26 ms，均远小于 2 s。
- **空间**：$O(n)$，只存排列与答案序列（长度 $\le4n$）。
- 若 $\sum n$ 放大到 $2\times10^5$，需把"找位置 + 循环移位"换成隐式平衡树（按位置维护序列、按值存结点指针），复杂度降到 $O(n\log n)$。

## 7. 参考代码

### C++17

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; cin >> n;
        vector<int> a(n);
        for (auto &v : a) cin >> v;
        // 每次操作 = n-2 个对换：n 为偶数时排列奇偶性是不变量
        if (n % 2 == 0) {
            vector<char> vis(n + 1, 0);
            int cyc = 0;
            for (int i = 1; i <= n; ++i)
                if (!vis[i]) {
                    ++cyc;
                    int j = i;
                    while (!vis[j]) { vis[j] = 1; j = a[j - 1]; }
                }
            if ((n - cyc) & 1) { cout << -1 << "\n"; continue; }   // 奇排列 -> 无解
        }
        bool sorted = true;
        for (int i = 0; i < n; ++i)
            if (a[i] != i + 1) { sorted = false; break; }
        if (sorted) { cout << 0 << "\n\n"; continue; }

        vector<int> ans;
        auto apply = [&](int i) {                                  // 1-based 下标 i
            rotate(a.begin(), a.begin() + (i - 1), a.begin() + i); // p_i 顶到队首
            rotate(a.begin() + i, a.begin() + i + 1, a.end());     // p_{i+1} 顶到队尾
            ans.push_back(i);
        };
        for (int x = 1; x <= n - 2; ++x) {                         // 把 1..n-2 压到队尾
            int i = 1;
            while (a[i - 1] != x) ++i;
            if (i >= 2) apply(i - 1);                              // 一步归位
            else { apply(2); apply(1); apply(n - 1); }             // x 在队首：三步修补
        }
        if (a[0] == n - 1) {                                       // 形态 A
            apply(2); apply(1); apply(n - 1); apply(1);
        } else {                                                   // 形态 B
            apply(1);
            for (int k = 0; k < n - 2; ++k) apply(2);
            apply(1);
        }
        cout << ans.size() << "\n";
        for (size_t j = 0; j < ans.size(); ++j) cout << ans[j] << " \n"[j + 1 == ans.size()];
        if (ans.empty()) cout << "\n";
    }
    return 0;
}
```

### Python3

```python
import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t, ptr, out = data[0], 1, []
    for _ in range(t):
        n = data[ptr]; ptr += 1
        a = data[ptr:ptr + n]; ptr += n

        if n % 2 == 0:                       # 每次操作 = n-2 个对换
            seen = [False] * (n + 1); cycles = 0
            for s in range(1, n + 1):
                if not seen[s]:
                    cycles += 1; j = s
                    while not seen[j]:
                        seen[j] = True; j = a[j - 1]
            if (n - cycles) % 2:             # 奇排列 -> 无解
                out.append("-1"); continue

        if all(a[i] == i + 1 for i in range(n)):
            out.append("0"); out.append("")
            continue

        ans = []

        def apply(k):                        # 1-based 下标 k
            a[:] = [a[k - 1]] + a[:k - 1] + a[k + 1:] + [a[k]]
            ans.append(k)

        for x in range(1, n - 1):            # 把 1..n-2 压到队尾
            i = a.index(x) + 1
            if i >= 2:
                apply(i - 1)
            else:
                apply(2); apply(1); apply(n - 1)
        if a[0] == n - 1:                    # 形态 A
            apply(2); apply(1); apply(n - 1); apply(1)
        else:                                # 形态 B
            apply(1)
            for _ in range(n - 2):
                apply(2)
            apply(1)
        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))
    sys.stdout.write("\n".join(out) + "\n")

main()
```

> ✅ 两份代码已对 $n\le8$ 的**全部**排列（共 46232 组）枚举对拍：无解判定与 BFS 的可解集合完全一致，有解组的序列逐条模拟后都能排好且长度 $\le4n$；随机 $n\le40$ 的 200 组与 $n=5000$ 的极值数据也全部通过。

## 8. 边界情况与易错点

1. **唯一无解情形**：$n$ 偶数且 $p$ 为奇排列（$n=2$ 的 $[2,1]$ 就是它）。别把奇偶性判反。
2. **$n=2$ 且 $p=[1,2]$**：输出 `0`，第二行为空，绝不能输出非法下标 2。
3. **$x=0$ 的格式**：先输出 `0`，再输出空行；$x=0$ 时第二行为空即正确。
4. **主循环必须停在 $n-2$**：三步修补要求 $|U|\ge3$，做到 $n-1$ 会破坏有序尾巴。
5. **别漏形态 B**：$n$ 为奇数时它真会出现，且 $\mathrm{apply}(2)$ 的次数是 $n-2$，多一次少一次都不行。
6. **下标范围**：所有输出都在 $[1,n-1]$；$n=3$ 时 $\mathrm{apply}(2)$ 与 $\mathrm{apply}(n-1)$ 重合属正常。
7. **多测**：`ans` 每组清空，组间不要多空行也不要少空行。
8. **性能**：Python 用切片整体重建列表（C 层搬运）在 $\sum n=5000$ 时约 0.4 s；逐元素循环模拟会慢一个量级。

## 9. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。
- **官方样例**：0 / 1 通过 token 比对；本题输出不唯一（构造 / 多解 / 特殊评测），剩余差异属预期，样例含义已在第 2 节逐组解释。
- **复核状态**：audited（2026-11-19 统一回归：编译 + 官方样例；写作期的随机对拍与暴力未重跑）。

## 相关题目与扩展

- [Codeforces 2246D. diss_quack and Array Game](https://codeforces.com/problemset/problem/2246/D)：同场的双端操作博弈，同样靠"操作不变量 + 极小状态"破局。
- [LeetCode 31. 下一个排列](https://leetcode.cn/problems/next-permutation/)：排列与相邻对换的入门版，可熟悉对换计数。
- [LeetCode 1053. 交换一次的先前排列](https://leetcode.cn/problems/previous-permutation-with-one-swap/)：交换一次的字典序与奇偶性变化，可与引理 1 对照。
- [Codeforces 1430E. String Reversal](https://codeforces.com/problemset/problem/1430/E)：同样以"每次操作改变固定数量的逆序对"为核心计数。

**延伸思考**：

1. 上界能否收紧到 $2n$？我们的构造最坏 $4n-6$（所有 $x$ 都落在队首时才逼近），实测随机数据只有约 $1.0n$、逆序约 $2.0n$，说明 $2n$ 有很大机会，但需要新的归位策略。
2. 若把操作改成"$p_i$ 去队尾、$p_{i+1}$ 去队首"，构造左右对称，奇偶性结论完全不变。
3. 若问最少操作数的最大值：$n$ 为奇数时循环移位型状态要 $\Theta(n)$ 步，能否证明这是紧的？
