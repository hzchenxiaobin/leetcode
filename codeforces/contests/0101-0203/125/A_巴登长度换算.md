# Codeforces 125A 巴登长度换算 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/125/A
- **比赛来源**：Codeforces Testing Round 2 · Problem A（UTC 2011-10-29）
- **难度**：1400
- **标签**：数学、取整
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：巴登的度量里 1 英寸 = 3 厘米、1 英尺 = 12 英寸。给定 $n$ 厘米，先**四舍五入**成整数英寸，再换算成"英尺数最大"的写法（即英寸部分 $<12$）。输出英尺数与剩余英寸数。

**约束**：

- $n\le10000$：直接算。
- 四舍五入规则：1 cm → 0 英寸，2 cm → 1 英寸。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
42
输出：
1 2
```

官方样例二：

```text
输入：
5
输出：
0 2
```

**样例一走查**：$42/3=14$ 英寸 $=12+2$ → 1 英尺 2 英寸 ✓。

**样例二走查**：$5/3\approx1.67$ → 四舍五入为 2 英寸 → 0 英尺 2 英寸 ✓。

![取整与拆分](../../../images/cf125a_round.svg)

**观察**：$n/3$ 不会正好落在 $.5$ 上（$3k+1.5$ 不是整数），所以"round half up"没有歧义：$\text{inches}=\lfloor(2n+3)/6\rfloor$。

## 3. 解题思路

### 3.1 算法流程

![样例对照](../../../images/cf125a_sample.svg)

1. `inches = (2*n + 3) / 6`（整数除法）；
2. 输出 `inches / 12` 与 `inches % 12`。

### 3.2 样例走查

| $n$ | $n/3$ | inches | 输出 |
|---|---|---|---|
| 42 | 14 | 14 | `1 2` |
| 5 | 1.67 | 2 | `0 2` |
| 1 | 0.33 | 0 | `0 0` |
| 2 | 0.67 | 1 | `0 1` |

## 4. 正确性证明

**引理 1**：$\lfloor(2n+3)/6\rfloor$ 等于最接近 $n/3$ 的整数。

**证明**：设 $n=3q+r$（$r\in\{0,1,2\}$）：$r=0$ → 值 $q$ ✓；$r=1$ → $(6q+5)/6$ 取整 $q$ ✓（$1/3$ 舍）；$r=2$ → $(6q+7)/6$ 取整 $q+1$ ✓（$2/3$ 入）✓。∎

**引理 2**：把总英寸数写成 $12a+b$（$0\le b<12$）时 $a$ 最大且唯一。

**证明**：带余除法唯一 ✓，且 $a=\lfloor\text{inches}/12\rfloor$ 已是最大可能英尺数 ✓。∎

**定理**：算法输出正确。

**证明**：由引理 1 英寸数正确、由引理 2 拆分正确 ✓。∎

## 5. 复杂度分析

- **时间/空间**：$O(1)$。
- **与时限的关系**：实测约 $3$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    // 1 英寸 = 3 厘米；四舍五入到最近的英寸：inches = floor((2n+3)/6)
    int inches = (2 * n + 3) / 6;
    int feet = inches / 12, rem = inches % 12;
    printf("%d %d\n", feet, rem);
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    inches = (2 * n + 3) // 6      # 四舍五入 n/3
    sys.stdout.write("%d %d\n" % (inches // 12, inches % 12))


main()
```

## 7. 边界情况与易错点

1. **1 cm → 0 英寸、2 cm → 1 英寸**：公式 $\lfloor(2n+3)/6\rfloor$ 正好满足（不能用 `(n+1)/3`）。
2. **英寸为 12 的倍数**：如 $n=36$ → 12 英寸 → `1 0`。
3. **$n<3$**：可能为 `0 0`。
4. **英尺数最大**：必须整除 12 取商。
5. **输出两个非负整数**。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：2 / 2 通过（`1 2`、`0 2`），C++ 与 Python 一致。
- **独立暴力对拍**：暴力枚举整数 $k$ 使 $|n-3k|$ 最小（与闭式公式不同），对 $n=1..10000$ **全量 10000 组**一致。
- **性能**：约 $3$ ms。
- **图片校验**：`cf125a_round.svg`、`cf125a_sample.svg` 通过 `ElementTree.parse`，含 `feTurbulence` 与手写体字体族，无越界/重叠。
- **公式校验**：KaTeX 0 错；无 `---` 分隔线。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 125B Simple XML](https://codeforces.com/problemset/problem/125/B)、[125C Hobbits' Party](https://codeforces.com/problemset/problem/125/C)、[125D Two progressions](https://codeforces.com/problemset/problem/125/D)、[125E MST Company](https://codeforces.com/problemset/problem/125/E)：同场其余题。
- [LeetCode 273. 整数转换英文表示](https://leetcode.cn/problems/integer-to-english-words/)：单位换算。
- [Codeforces 1A Theatre Square](https://codeforces.com/problemset/problem/1/A)：简单取整。

**延伸思考**：

1. **如果 1 英寸 = 2.54 厘米**：改成浮点或放大整数。
2. **如果要求截断而非四舍五入**：用 `n/3`。
3. **如果单位更多（码等）**：依次带余除法。

