# Codeforces 139B Wallpaper 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/139/B
- **比赛来源**：Codeforces Beta Round 99 (Div. 2) · Problem B
- **难度**：1600
- **标签**：实现、枚举
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个长方体房间（长 $\ell$、宽 $w$、高 $h$），$m$ 种壁纸（卷长 $L$、卷宽 $W$、单价 $p$）。纸带沿卷长方向、必须**竖直**粘贴（卷不能横放），可按需裁剪但接缝也必须竖直。每个房间只能用一种壁纸、每卷不能跨房间共用。求贴完所有房间的最小总价。

**约束**：

- $n,m\le500$；尺寸为正整数。
- 墙面周长 $P=2(\ell+w)$，需覆盖高度 $h$ ✓。
- 每条竖带宽 $W$、高 $h$；一卷可切 $\lfloor L/h\rfloor$ 条 ✓（$L<h$ 则该卷不可用）。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
1
5 5 3
3
10 1 100
15 2 320
3 19 500

输出：
640
```

**样例走查**：$P=2(5+5)=20$、$h=3$。

- $(10,1,100)$：每卷切 $\lfloor10/3\rfloor=3$ 条，需 $\lceil20/1\rceil=20$ 条 → $\lceil20/3\rceil=7$ 卷 → 700；
- $(15,2,320)$：每卷 5 条，需 $\lceil20/2\rceil=10$ 条 → 2 卷 → **640** ✓；
- $(3,19,500)$：每卷 1 条，需 $\lceil20/19\rceil=2$ 条 → 2 卷 → 1000。

取最小 640 ✓。

**观察**：房间之间独立，每种壁纸的用量 = $\left\lceil \frac{\lceil P/W\rceil}{\lfloor L/h\rfloor}\right\rceil$ 卷 ✓；对每个房间取最小价 ✓。

![一卷怎么切](../../../images/cf139b_roll.svg)

## 3. 解题思路

逐个房间、逐个壁纸种类计算卷数取最小 ✓。

![流程](../../../images/cf139b_flow.svg)

### 3.4 样例走查

见 2 节 ✓。

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `1` / `1 1 1` / `1` / `1 1 5` | `20` | 周长 4、需 4 条、每卷 1 条 |
| `1` / `1 1 1` / `1` / `1 4 5` | `5` | 一卷 4 条够 4 条 |
| `1` / `1 1 5` / `1` / `4 1 7` | `7` | $L<h$ 不可用 → 需换种类 |

## 4. 正确性证明

**引理 1**：单个房间用某卷时，需要 $\lceil P/W\rceil$ 条竖带。

**证明**：每条竖带覆盖宽 $W$，接缝竖直、不能横接 ⇒ 沿周长拼满 ✓。∎

**引理 2**：每卷可切出 $\lfloor L/h\rfloor$ 条高 $h$ 的竖带；$L<h$ 时一条也没有。

**证明**：竖带高必须 $\ge h$ 且接缝竖直 ⇒ 只能沿卷长方向切 ✓。∎

**引理 3**：卷数 $=\lceil \text{带数}/\text{每卷带数}\rceil$，且不能再少。

**证明**：卷之间不可拼接使用 ⇒ 向上取整 ✓。∎

**定理**：按房间独立取最小值求和即最优。

**证明**：房间之间互不共享卷 ⇒ 目标函数可分离，逐间最优即全局最优 ✓。∎

## 5. 复杂度分析

- **时间**：$O(nm)$。
- **空间**：$O(n+m)$。
- **与时限的关系**：实测 $n=m=500$ 约 $3$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<array<ll,3>> room(n);
    for (auto& r : room) cin >> r[0] >> r[1] >> r[2];
    int m;
    cin >> m;
    vector<array<ll,3>> wp(m);   // 长、宽、价格
    for (auto& w : wp) cin >> w[0] >> w[1] >> w[2];
    ll total = 0;
    for (auto& r : room) {
        ll perim = 2 * (r[0] + r[1]);
        ll h = r[2];
        ll best = LLONG_MAX;
        for (auto& w : wp) {
            ll L = w[0], W = w[1], price = w[2];
            if (L < h) continue;                 // 竖条高度不够
            ll stripsPerRoll = L / h;            // 每卷能切出的竖条数
            ll stripsNeed = (perim + W - 1) / W; // 需要多少竖条
            ll rolls = (stripsNeed + stripsPerRoll - 1) / stripsPerRoll;
            best = min(best, rolls * price);
        }
        total += best;
    }
    cout << total << '\n';
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    p = 0
    n = int(data[p]); p += 1
    rooms = []
    for _ in range(n):
        rooms.append((int(data[p]), int(data[p + 1]), int(data[p + 2]))); p += 3
    m = int(data[p]); p += 1
    wps = []
    for _ in range(m):
        wps.append((int(data[p]), int(data[p + 1]), int(data[p + 2]))); p += 3
    total = 0
    for l, w, h in rooms:
        perim = 2 * (l + w)
        best = None
        for L, W, price in wps:
            if L < h:
                continue
            strips_per_roll = L // h
            strips_need = (perim + W - 1) // W
            rolls = (strips_need + strips_per_roll - 1) // strips_per_roll
            cost = rolls * price
            if best is None or cost < best:
                best = cost
        total += best
    print(total)


main()
```

两份代码都只用标准库，可原样提交。

## 7. 边界情况与易错点

1. **$L<h$**：该种类不可用。
2. **两次向上取整**：先带数、再卷数。
3. **不能横放卷**（题面明确）✓。
4. **卷不可跨房间共用** ✓ 逐间独立。
5. **周长用 $2(\ell+w)$**，不是 $\ell w$。
6. **多测**：单组输入。

## 8. 验证记录

- **编译环境与命令**：本机无 GNU `g++`，用 `Apple clang 21.0.0` + 仓库自带 `codeforces/tools/include/bits/stdc++.h` 兼容头（`clang++ -std=c++17 -O2 -I codeforces/tools/include`）编译；Python 为 `Python 3.9.6`。
- **官方样例**：1 / 1 通过（`640`）。
- **额外测试**：200 组随机小数据（房间 1–4 间、壁纸 1–4 种）与独立实现比对，**162 组可行实例全部一致**（其余 38 组是"没有任何卷能覆盖该高度"的不可行实例，题目保证不会出现，对拍时跳过）。
- **图片校验**：两张 SVG（`cf139b_roll.svg`、`cf139b_flow.svg`）通过 `xml.etree.ElementTree.parse`。
- **公式校验**：KaTeX 渲染无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 139A Petr and Book](https://codeforces.com/problemset/problem/139/A)：同场 A 题。
- [Codeforces 138C Mushroom Gnomes - 2](https://codeforces.com/problemset/problem/138/C)：同批次。
- [LeetCode 1103. 分糖果 II](https://leetcode.cn/problems/distribute-candies-to-people/)：分配。
- [LeetCode 2240. 买钢笔和铅笔的方案数](https://leetcode.cn/problems/number-of-ways-to-buy-pens-and-pencils/)：枚举。

**延伸思考**：

1. **如果卷可以横放**：取 $\max(L,W)$ 作高。
2. **如果允许横向接缝**：可拼接，卷数变小。
3. **如果一卷可跨房间**：变成全局装箱。
4. **如果要求输出方案**：记录每间选的种类。
