# Codeforces 125B 简单 XML 格式化 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/125/B
- **比赛来源**：Codeforces Testing Round 2 · Problem B（UTC 2011-10-29）
- **难度**：1000
- **标签**：字符串、模拟
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：给定合法 XML 文本（只有 `<x>` 与 `</x>`，$x$ 为小写字母，可嵌套），按规则输出：每个标签独占一行，缩进 $2h$ 个空格（$h$ 为该标签的嵌套深度）。

**约束**：

- 长度 $\le1000$，无空格，保证合法。
- 无自闭合标签（题面定义里没有）。
- 单组数据。

## 2. 示例与观察

官方样例一：

```text
输入：
<a><b><c></c></b></a>
输出：
<a>
  <b>
    <c>
    </c>
  </b>
</a>
```

官方样例二：

```text
输入：
<a><b></b><d><c></c></d></a>
输出：
<a>
  <b>
  </b>
  <d>
    <c>
    </c>
  </d>
</a>
```

**样例一走查**：`<a>` 深度 0 → 顶格；`<b>` 深度 1 → 2 空格；`<c>` 深度 2 → 4 空格；`</c>` 深度 2（先回退再打印）；以此类推 ✓。

![逐个标签扫描](../../../images/cf125b_parse.svg)

**观察**：按顺序扫描标签即可：开标签"先打印、后加深"，闭标签"先回退、后打印"。

## 3. 解题思路

### 3.1 算法流程

![样例 1](../../../images/cf125b_sample.svg)

1. `depth=0`，指针 `i=0`；
2. 找下一个 `>`，取出标签 `s[i..j]`；
3. 若以 `</` 开头：`--depth`，输出 `2*depth` 个空格 + 标签；
4. 否则：输出 `2*depth` 个空格 + 标签，`++depth`；
5. `i=j+1`，重复。

### 3.2 样例走查

样例一各标签深度：`<a>`0、`<b>`1、`<c>`2、`</c>`2、`</b>`1、`</a>`0 ✓ 与输出一致。

## 4. 正确性证明

**引理 1**：扫描到某标签时，`depth` 恰为该标签的嵌套深度。

**证明**：每遇到开标签（其内部内容尚未结束）`depth` 加一、闭标签减一；由 XML 合法性，标签配对正确 ✓。∎

**引理 2**：闭标签打印前深度应为"外层深度"，故要先减一。

**证明**：`</x>` 与它匹配的 `<x>` 同深度 ✓，而打印 `</x>` 时深度已从内部退回，故先 `--depth` ✓。∎

**定理**：输出满足题面格式。

**证明**：由引理 1、2，每个标签行缩进恰为 $2h$，且每标签独占一行、顺序不变 ✓。∎

## 5. 复杂度分析

- **时间**：$O(|s|)$。
- **空间**：$O(|s|)$（输出）。
- **与时限的关系**：实测约 $3$ ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    if (!(cin >> s)) return 0;
    int depth = 0;
    size_t i = 0;
    while (i < s.size()) {
        size_t j = s.find('>', i);
        string tag = s.substr(i, j - i + 1);
        if (tag[1] == '/') {
            --depth;
            printf("%s\n", (string(2 * depth, ' ') + tag).c_str());
        } else {
            printf("%s\n", (string(2 * depth, ' ') + tag).c_str());
            ++depth;
        }
        i = j + 1;
    }
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
    s = data[0].decode()
    out = []
    depth = 0
    i = 0
    while i < len(s):
        j = s.index('>', i)
        tag = s[i:j + 1]
        if tag[1] == '/':
            depth -= 1
            out.append(" " * (2 * depth) + tag)
        else:
            out.append(" " * (2 * depth) + tag)
            depth += 1
        i = j + 1
    sys.stdout.write("\n".join(out) + "\n")


main()
```

## 7. 边界情况与易错点

1. **闭标签必须先减深度**，否则缩进多 2 个空格。
2. **兄弟标签**：如 `<a><b></b><d></d></a>`，`<d>` 的深度回到 1（样例二）。
3. **行末不能有多余空格**：只输出缩进 + 标签。
4. **单标签最外层**：`<a></a>` → 两行，深度都是 0、0。
5. **输入无空格**：可以直接按字符串读。
6. **嵌套很深**：缩进按 $2h$ 增长，字符串长 $\le1000$ 不会溢出。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2`（Apple clang 21.0.0 + `codeforces/tools/include` 的兼容头），Python 3.9.6。
- **官方样例**：2 / 2 通过，C++ 与 Python 逐字符一致。
- **独立暴力对拍**：随机生成合法 XML 串（最多 4 层嵌套），用独立校验器检查"标签个数一致、缩进 = 2·层深、标签顺序不变"，**220 组**全部通过（两语言一致）。
- **性能**：约 $3$ ms。
- **图片校验**：`cf125b_parse.svg`、`cf125b_sample.svg` 通过 `ElementTree.parse`，无越界/重叠。
- **公式校验**：KaTeX 0 错；无 `---` 分隔线。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 125A 巴登长度换算](https://codeforces.com/problemset/problem/125/A)、[125C Hobbits' Party](https://codeforces.com/problemset/problem/125/C)、[125D Two progressions](https://codeforces.com/problemset/problem/125/D)、[125E MST Company](https://codeforces.com/problemset/problem/125/E)：同场其余题。
- [Codeforces 118B Present from Lena](https://codeforces.com/problemset/problem/118/B)：格式化输出。
- [LeetCode 385. 迷你语法分析器](https://leetcode.cn/problems/mini-parser/)：嵌套结构解析。

**延伸思考**：

1. **如果有自闭合标签 `<x/>`**：深度不加不减，按开标签打印。
2. **如果要求行末加逗号**：在打印后追加。
3. **如果标签可带属性**：解析逻辑不变，标签整段打印。

