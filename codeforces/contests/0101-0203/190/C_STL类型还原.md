# Codeforces 190C STL 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/190/C
- **比赛来源**：Codeforces Round 120 (Div. 2) · Problem C（UTC 2012-05-16）
- **难度**：1500
- **标签**：解析、递归下降、栈
- **评测类型**：普通（多解？题面保证唯一）
- **限制**：时间 2 s / 内存 256 MB

**题意**：类型文法是 `type := int | pair<type,type>`。给定 $n$（类型里含 $n$ 个 `int`）与一串被去掉标点的词（只有 `pair` 和 `int`），要求还原出唯一合法的类型串；不可能则输出 `Error occurred`。

**约束**：$1\le n\le10^5$，词总数不超过 $10^5$，其中恰好有 $n$ 个 `int`。

**这档约束排除了什么**：词数 $10^5$ 时，"尝试所有括号摆放"是指数级；但文法无歧义且题面保证答案唯一，所以从左到右一遍扫描就能判定，$O(\text{词数})$。

## 2. 示例与观察

官方样例一：

```text
输入：
3
pair pair int int int

输出：
pair<pair<int,int>,int>
```

官方样例二：

```text
输入：
1
pair int

输出：
Error occurred
```

**样例解释一**：`pair` 需要两个类型；第一个类型又是 `pair`，吃掉接下来的 `int int`；第二个类型是剩下的 `int` ⇒ `pair<pair<int,int>,int>`。

**样例解释二**：`pair` 要两个类型，但只剩一个 `int` ⇒ 失败。

**第一条观察（词数与 $n$ 的关系）**：一个有 $n$ 个 `int` 的合法类型，恰好有 $n-1$ 个 `pair`，词总数 $2n-1$。所以凡词数 $\ne2n-1$ 一定错。

**第二条观察（贪心扫描）**：从左到右：`int` 立刻是一个完整类型；`pair` 先记下"还欠两个类型"，等后面凑齐两个完整类型再把它们合并。合并是**唯一**的，所以不需要回溯。

**第三条观察（判定）**：扫完后栈里必须恰好剩下 1 个完整类型；否则（还有悬空的 `pair`，或剩多个类型）都是错误。

![递归展开成一棵树](../../../images/cf190c_tree.svg)

自造样例（标注"自造"）：

| 输入 | 输出 | 说明 |
|------|------|------|
| `1` / `int` | `int` | 单词 |
| `2` / `pair int int` | `pair<int,int>` | 最简 pair |
| `2` / `pair int pair` | `Error occurred` | 第二个孩子缺 |
| `3` / `pair pair int int int` | `pair<pair<int,int>,int>` | 左深 |
| `3` / `pair int pair int int` | `pair<int,pair<int,int>>` | 右深 |
| `2` / `int int` | `Error occurred` | 剩两个类型 |

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举所有括号摆放：指数级。深度递归下降：递归深度可达 $10^5$，C++ 默认栈会溢出（本机 8 MB 栈下约 $5\times10^4$ 层就崩）。

### 3.2 核心观察：栈式归约

![判定流程](../../../images/cf190c_flow.svg)

维护一个栈，元素是"已完成的类型"或"待凑齐的 pair 记号"：

1. 读到一个词：`int` → 压入一个完整类型；`pair` → 压入一个记号。
2. 反复检查栈顶三个元素：若是「记号，完整，完整」→ 弹出三个、压入合并后的 `pair<A,B>`。
3. 扫完后：栈里恰好一个完整类型 ⇒ 输出；否则 `Error occurred`。

因为每一步合并都是"最近的两个完整类型"，而文法是无歧义的，这个归约顺序与递归下降完全等价，且总工作量与输出长度成正比。

### 3.3 算法流程

见上；输出时用显式栈做中序展开（先 `pair<`，再左，再 `,`，再右，再 `>`），避免递归。

### 3.4 样例走查

`pair pair int int int`：

| 步骤 | 栈（自底向上） |
|------|----------------|
| 读 pair | `[P]` |
| 读 pair | `[P, P]` |
| 读 int | `[P, P, int]` |
| 读 int | `[P, P, int, int]` → 归约 → `[P, pair<int,int>]` |
| 读 int | `[P, pair<int,int>, int]` → 归约 → `[pair<pair<int,int>,int>]` ✓ |

## 4. 正确性证明

**引理 1（词数）**：含 $n$ 个 `int` 的合法类型恰有 $n-1$ 个 `pair`，总词数 $2n-1$。

**证明**：对类型结构归纳：`int` 有 1 个词、0 个 pair；`pair<A,B>` 的词数 = $1+|A|+|B|$，pair 数 = $1+p_A+p_B$，由归纳 $|A|=2n_A-1$ 等即得。∎

**引理 2（归约的局部正确性）**：若某一步栈顶形如「记号，完整，完整」，则这三个元素在任何一个合法解析中必然合并成一个 `pair<A,B>`。

**证明**：记号只能由 `pair` 产生，它需要的两个类型紧跟在它后面；而这两个位置的元素已经是完整类型（不会再有词并入它们），所以它们正是 `pair` 的两个孩子。∎

**引理 3（无歧义）**：任意时刻至多有一种归约可做，且做与不做不影响最终可归约性。

**证明**：栈顶三元素的结构由扫描顺序唯一决定；`pair` 的两个孩子必须紧邻其后，因此归约位置唯一。∎

**定理（判定正确）**：算法输出合法类型当且仅当该词序列能还原成合法类型。

**证明**：

- **充分性**：若算法输出，则每一步归约都由引理 2 保证是合法解析的一部分，最终得到的就是一个合法类型。
- **必要性**：若存在合法解析，则按引理 3 的归约顺序一定能把整串归约成一个类型；若算法在扫完后没有得到单个完整类型，说明存在悬空记号或剩余类型，与"存在合法解析"矛盾（合法解析中每个 `pair` 都恰好有两个孩子、整体是一个类型）。∎

## 5. 复杂度分析

- **时间**：$O(\text{词数}+\text{输出长度})$，总长 $O(n)$。
- **空间**：$O(n)$（栈 + 节点数组 + 输出）。
- **数值范围**：不涉及大数。
- **与时限的关系**：$n=5\times10^4$ 的深嵌套实测 111 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

// 迭代版：用显式栈把 "pair 值 值" 归约成一个值，避免深递归爆栈
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> tok;
    string s;
    while (cin >> s) tok.push_back(s);

    vector<pair<int, int>> nodes;   // (l, r)；l == -1 表示 int，l == -2 表示尚未归约的 pair 记号
    vector<int> st;
    for (const string &t : tok) {
        if (t == "int") { nodes.push_back({-1, -1}); }
        else { nodes.push_back({-2, -2}); }
        st.push_back((int)nodes.size() - 1);
        while (st.size() >= 3) {
            int c = st[st.size() - 1], b = st[st.size() - 2], a = st[st.size() - 3];
            if (nodes[a].first == -2 && nodes[b].first != -2 && nodes[c].first != -2) {
                st.pop_back(); st.pop_back(); st.pop_back();
                nodes.push_back({b, c});
                st.push_back((int)nodes.size() - 1);
            } else break;
        }
    }
    if (st.size() != 1 || nodes[st[0]].first == -2) { cout << "Error occurred\n"; return 0; }

    // 迭代输出，避免递归深度过大
    struct Item { bool isNode; int idx; const char *lit; };
    vector<Item> work;
    work.push_back({true, st[0], nullptr});
    string out;
    while (!work.empty()) {
        Item it = work.back();
        work.pop_back();
        if (!it.isNode) { out += it.lit; continue; }
        const pair<int, int> &nd = nodes[it.idx];
        if (nd.first == -1) { out += "int"; }
        else {
            work.push_back({false, 0, ">"});
            work.push_back({true, nd.second, nullptr});
            work.push_back({false, 0, ","});
            work.push_back({true, nd.first, nullptr});
            work.push_back({false, 0, "pair<"});
        }
    }
    cout << out << '\n';
    return 0;
}
```

### Python3

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    tok = [t.decode() for t in data[1:]]

    nodes = []      # (l, r)：l = -1 表示 int，l = -2 表示未归约的 pair 记号
    st = []
    for t in tok:
        if t == "int":
            nodes.append((-1, -1))
        else:
            nodes.append((-2, -2))
        st.append(len(nodes) - 1)
        while len(st) >= 3:
            a, b, c = st[-3], st[-2], st[-1]
            if nodes[a][0] == -2 and nodes[b][0] != -2 and nodes[c][0] != -2:
                st.pop(); st.pop(); st.pop()
                nodes.append((b, c))
                st.append(len(nodes) - 1)
            else:
                break

    if len(st) != 1 or nodes[st[0]][0] == -2:
        sys.stdout.write("Error occurred\n")
        return

    out = []
    work = [(True, st[0], None)]
    while work:
        is_node, idx, lit = work.pop()
        if not is_node:
            out.append(lit)
            continue
        l, r = nodes[idx]
        if l == -1:
            out.append("int")
        else:
            work.append((False, 0, ">"))
            work.append((True, r, None))
            work.append((False, 0, ","))
            work.append((True, l, None))
            work.append((False, 0, "pair<"))
    sys.stdout.write("".join(out) + "\n")


main()
```

## 7. 边界情况与易错点

1. **`pair` 悬空**：如 `pair int`（样例 2）——扫完后栈里是「记号，完整」⇒ 错。
2. **多余类型**：如 `int int`——扫完后栈里有两个完整类型 ⇒ 错。
3. **词数不为 $2n-1$**：直接可判错，但代码用栈判定也能覆盖。
4. **深嵌套**：递归实现会爆栈，必须用显式栈（本机在 8 MB 栈下约 $5\times10^4$ 层崩溃）。
5. **输出不能有空格**：`pair<int,int>` 中间不能加空格。
6. **唯一的解析**：题面保证若有解则唯一，所以不需要在多个解析里挑选。
7. **`n` 与词数不一致**：以词为准判定；`n` 只用于读入。

## 8. 验证记录

- **编译环境与命令**：`clang++ -std=c++17 -O2` + 兼容头；Python 3.9.6。文档级校验：`python3 codeforces/tools/verify_solution.py codeforces/contests/0101-0203/190/C_STL类型还原.md`。
- **官方样例**：2 / 2 通过（`pair<pair<int,int>,int>`、`Error occurred`）。
- **独立对拍**：
  - 随机生成合法类型（递归展开成词流）**300 组**，要求程序还原出**同一个**字符串；
  - 随机非法词流 **300 组**，与"区间 DP 求每个位置能解析到哪些终点"的独立判定比对；
  - C++/Python 全部一致。
- **深度测试**：$n=5\times10^4$ 的左深嵌套（词数 $10^5$）111 ms 正常输出，无栈溢出。
- **图片校验**：两张 SVG（`cf190c_tree.svg`、`cf190c_flow.svg`）通过 `xml.etree.ElementTree.parse`，文本未越界、无重叠。
- **复核状态**：verified（样例、600 组对拍、深度测试、图片均实跑通过）。

## 相关题目与扩展

- [Codeforces 190D Non-Secret Cypher](https://codeforces.com/problemset/problem/190/D)：同场双指针题。
- [Codeforces 5C Longest Regular Bracket Sequence](https://codeforces.com/problemset/problem/5/C)：括号序列的经典。
- [LeetCode 20 有效的括号](https://leetcode.cn/problems/valid-parentheses/)：栈式匹配入门。
- [Codeforces 4C Registration system](https://codeforces.com/problemset/problem/4/C)：字符串处理。
- [Codeforces 190E Counter Attack](https://codeforces.com/problemset/problem/190/E)：同场图论题。

**延伸思考**：

1. **为什么无歧义**：文法 `type := int | pair<type,type>` 的最外层结构由第一个词决定（`int` 或 `pair`），递归下去唯一。
2. **如果允许 `pair` 的第三种写法**：歧义出现，需要回溯或动态规划。
3. **如果要输出"任意一种"合法类型**：本算法给出的就是唯一解，无需挑选。
4. **如果词数达到 $10^6$**：栈式实现仍然是线性的，只是输出构造要注意内存。

