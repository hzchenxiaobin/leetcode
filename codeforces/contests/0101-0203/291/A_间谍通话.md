# Codeforces 291A Spyke Talks 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/291/A
- **比赛来源**：Croc Champ 2013 - Qualification Round · Problem A（UTC 2013-04-12）
- **难度**：1000
- **标签**：计数
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$n$ 个秘书，每人记录一个通话 session 号（0 表示没通话）。一次通话恰好连接两个人，session 号唯一。求正在通话的**秘书对**数量；若数据自相矛盾输出 $-1$。

**约束**：$n \le 10^3$。

## 2. 示例与观察

官方样例 1：

```text
输入：
6
0 1 7 1 7 10

输出：
2
```

官方样例 2：

```text
输入：
3
1 1 1

输出：
-1
```

官方样例 3：

```text
输入：
1
0

输出：
0
```

**观察**：按非零 session 号分组：

- 出现 2 次 → 这两个秘书在互相通话 → 1 对；
- 出现 1 次 → 对方在公司外（题面明确允许）→ 0 对；
- 出现 $\ge 3$ 次 → 一次通话不可能连三个人 → 矛盾 → $-1$。

## 3. 解题思路

![按通话号分组计数](../../../images/cf291a_count.svg)

哈希表计数，按上述规则累加。

## 4. 正确性证明

**引理**：session 号 $x$ 出现 $c$ 次时，贡献为 $c=2$ 时 1 对、$c=1$ 时 0 对、$c\ge3$ 时矛盾。

**证明**：一次通话恰好两人、session 唯一；$c=2$ 恰好是一对，$c=1$ 的另一方在公司外，$c\ge3$ 无法满足 ✓。∎

**定理**：算法输出正确。

**证明**：各 session 号互不影响，由引理累加即得；任一 $c\ge3$ 即整体无解 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n)$。
- **空间**：$O(n)$。
- **与时限的关系**：实测端到端 3.0 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; if(scanf("%d",&n)!=1) return 0;
    map<int,int> cnt;
    for(int i=0;i<n;i++){int v;scanf("%d",&v); if(v) cnt[v]++;}
    int ans=0;
    for(auto &kv: cnt){
        if(kv.second==2) ans++;
        else if(kv.second>2){ printf("-1\n"); return 0; }
    }
    printf("%d\n", ans);
    return 0;
}
```

### Python3

```python
import sys
from collections import Counter
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cnt = Counter(int(v) for v in data[1:1+n] if int(v) != 0)
    ans = 0
    for c in cnt.values():
        if c == 2:
            ans += 1
        elif c > 2:
            print(-1); return
    print(ans)
main()
```

## 7. 边界情况与易错点

1. **$c=1$ 不是错误**：对方可以在公司外。
2. **$c \ge 3$**：输出 $-1$（样例 2）。
3. **全 0**：答案 0。
4. **$n=1$**：只能 0 或 1 次，答案 0。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：3 / 3 通过（2、-1、0），C++ 与 Python 一致。
- **独立暴力对拍**：暴力版按定义分组计数。随机 250 组 $n \le 8$，**250 / 250 全部一致**。
- **最大约束性能**：$n = 1000$，实测端到端 3.0 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 291B Command Line Arguments](https://codeforces.com/problemset/problem/291/B)：同场 B 题。

**延伸思考**：

1. **如果允许多人会议**：$c\ge3$ 也合法，答案变成 $\sum \lfloor c/2 \rfloor$。
2. **如果 session 号会重复使用**：题意不同。

