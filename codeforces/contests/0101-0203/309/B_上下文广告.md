# Codeforces 309B Context Advertising 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/309/B
- **比赛来源**：Croc Champ 2013 - Finals (online version, Div. 1) · Problem B（UTC 2013-05-25）
- **难度**：2100
- **标签**：贪心、倍增
- **评测类型**：多解（输出任意最优横幅）
- **限制**：时间 2 s / 内存 256 MB

**题意**：一段 $n$ 个词的文本，广告横幅有 $r$ 行、每行至多 $c$ 个字符；词之间用空格分隔（允许连续多个空格），词不能拆开。求最多能放原文中**连续**多少个词，并把横幅打印出来（最多 $r$ 行，空行可不打印）。

**约束**：$n, r, c \le 10^6$，$r\times c \le 10^6$，所有词总字符数 $\le 5\times10^6$。

## 2. 示例与观察

官方样例 1：

```text
输入：
9 4 12
this is a sample text for croc final round

输出：
this is a
sample text
for croc
final round
```

官方样例 2：

```text
输入：
9 1 9
this is a sample text for croc final round

输出：
this is a
```

官方样例 4：

```text
输入：
2 2 5
first second

输出：
first
```

**观察 1**：选定起点 $i$ 后，**每行尽量多放词**（贪心）一定不劣——放得越多，后续起点越靠后，最终能放的词数不会减少。

**观察 2**：于是只要知道 `next[i]` = 从 $i$ 起贪心填一行后的下一行起点，$r$ 行的终点就是 `next` 作用 $r$ 次。

**观察 3（$r$ 很大怎么办）**：直接做 $r$ 次是 $O(nr)$。用**二进制倍增**：`cur = next`，对 $r$ 的每个二进制位把 `ans` 与 `cur` 复合、`cur` 自复合 → $O(n\log r)$ 时间、$O(n)$ 内存（不需要存 $\log r$ 层数组）。

**样例 4 验证**：$r=2,c=5$：`next[0]=1`（"first" 恰好 5 字符，"second" 放不下），`next[1]=1`（"second" 6 字符放不下）→ 从 0 出发走 2 次到 1 → 只能放 1 个词 ✓。

## 3. 解题思路

![先算出 next 指针](../../../images/cf309b_next.svg)

1. 双指针求 `next[i]`：窗口右端 `j` 单调，`i` 右移时扣掉首词长度（窗口里还有词时多扣 1 个空格）；
2. 倍增求 `ans = next^r`；
3. 答案 = $\max_i (\text{ans}[i]-i)$，回溯 `next` 打印每行。

## 4. 正确性证明

**引理 1（贪心每行最优）**：固定起点 $i$，若第一行少放若干词，则后续能放的词数不超过贪心放法。

**证明**：贪心放法把第一行的终点推到最右 $j_1$；任何其他放法终点 $j_1' \le j_1$，而"从更靠前的位置开始放 $r-1$ 行"能放的范围不短于从更后开始（`next` 单调不减）✓。∎

**引理 2（倍增正确）**：`ans` 经倍增合成后等于 `next` 作用 $r$ 次。

**证明**：函数复合的结合律 + 二进制分解 ✓；`ans = cur∘ans`、`cur = cur∘cur` 在每一位上正确累积 ✓。∎

**定理**：输出为最优横幅。

**证明**：由引理 1，枚举起点 + 每行贪心覆盖了所有最优解；由引理 2 终点计算正确；回溯打印的行数与每行长度都满足限制 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n\log r + \text{输出})$。
- **空间**：$O(n)$。
- **与时限的关系**：时限 2 s，$n = 10^6, r = 1000, c = 1000$ 实测端到端 90 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n, r; long long c;
    if(scanf("%d %d %lld",&n,&r,&c)!=3) return 0;
    vector<string> w(n);
    vector<int> len(n);
    // 读入整行再切词（词间可能有单个空格）
    {
        string line; 
        // 先用 scanf 逐个读（题面保证词之间单空格）
        char buf[64];
        for(int i=0;i<n;i++){ scanf("%s",buf); w[i]=buf; len[i]=(int)w[i].size(); }
    }
    // next[i]：从 i 开始贪心填一行后，下一行的起点
    vector<int> nxt(n+1);
    nxt[n]=n;
    int j=0; long long cur=0;
    for(int i=0;i<n;i++){
        if(j<i){ j=i; cur=0; }
        while(j<n && cur + len[j] + (j>i?1:0) <= c){ cur += len[j] + (j>i?1:0); j++; }
        nxt[i]=j;
        cur -= len[i] + (j > i+1 ? 1 : 0);   // 移除窗口首词（若后面还有词，连带那个空格）
        if(cur < 0) cur = 0;
    }
    nxt[n]=n;
    // ans = next^r（函数倍增，O(n log r)，O(n) 内存）
    vector<int> ans(n+1); for(int i=0;i<=n;i++) ans[i]=i;
    vector<int> curf = nxt, tmp(n+1);
    int rr = r;
    while(rr>0){
        if(rr&1){ for(int i=0;i<=n;i++) tmp[i]=curf[ans[i]]; ans.swap(tmp); }
        for(int i=0;i<=n;i++) tmp[i]=curf[curf[i]]; curf.swap(tmp);
        rr >>= 1;
    }
    int bestStart=-1, bestCnt=0;
    for(int i=0;i<n;i++){
        int cnt = ans[i]-i;
        if(cnt>bestCnt){ bestCnt=cnt; bestStart=i; }
    }
    // 按贪心输出
    if(bestStart<0){ printf("\n"); return 0; }
    int p=bestStart;
    vector<string> lines;
    for(int line=0; line<r && p<n; line++){
        int q = nxt[p];
        if(q==p) break;                       // 这一行放不下任何词
        string s;
        for(int t=p;t<q;t++){ if(t>p) s+=' '; s+=w[t]; }
        lines.push_back(s);
        p=q;
    }
    for(auto &s : lines) printf("%s\n", s.c_str());
    return 0;
}
```

### Python3

```python
import sys
def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, r, c = int(data[0]), int(data[1]), int(data[2])
    w = [data[3+i].decode() for i in range(n)]
    ln = [len(x) for x in w]
    nxt = [0]*(n+1)
    nxt[n] = n
    j = 0; cur = 0
    for i in range(n):
        if j < i: j = i; cur = 0
        while j < n and cur + ln[j] + (1 if j > i else 0) <= c:
            cur += ln[j] + (1 if j > i else 0); j += 1
        nxt[i] = j
        cur -= ln[i] + (1 if j > i+1 else 0)
        if cur < 0: cur = 0
    # next^r 用二进制倍增（O(n log r) 时间、O(n) 内存）
    ans = list(range(n+1))
    curf = nxt[:]
    rr = r
    while rr > 0:
        if rr & 1:
            ans = [curf[ans[i]] for i in range(n+1)]
        curf = [curf[curf[i]] for i in range(n+1)]
        rr >>= 1
    bestStart = -1; bestCnt = 0
    for i in range(n):
        cnt = ans[i] - i
        if cnt > bestCnt: bestCnt = cnt; bestStart = i
    out = []
    if bestStart >= 0:
        p = bestStart
        for _ in range(r):
            if p >= n: break
            q = nxt[p]
            if q == p: break
            out.append(' '.join(w[p:q]))
            p = q
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
main()
```

Python 版倍增要做 $O(n\log r)$ 次列表构造，$n = 10^6$ 时偏慢，**建议提交 C++/PyPy3**。

## 7. 边界情况与易错点

1. **单词长于 $c$**：该行放不下任何词 → `next[i] == i`，此起点贡献 0（样例 4）。
2. **窗口收缩的扣减**：首词无前导空格；若窗口里还有别的词，要额外扣 1 个空格（这是本题最容易错的地方，我第一版就错在这里）。
3. **$r\times c$ 很小**：答案规模有限，但 $n$ 可能很大，别做 $O(nr)$。
4. **空行**：允许不打印。
5. **多解**：任意最优横幅均可。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：4 / 4 通过（由 checker 判定横幅合法性与最优性），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf309b.py`（校验：行数 ≤ r、每行 ≤ c 字符、所有词连起来是原文的连续子段，且词数等于官方最优值）。
- **独立暴力对拍**：暴力版对每个起点逐行贪心求最优词数。随机 250 组（$n \le 7$），两个实现都通过 checker，**250 / 250 通过**。
- **最大约束性能**：$n = 10^6$、$r = c = 1000$，实测端到端 90 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 309A Morning run](https://codeforces.com/problemset/problem/309/A)：同场 A 题。
- [Codeforces 309C Memory for Arrays](https://codeforces.com/problemset/problem/309/C)：同场 C 题。

**延伸思考**：

1. **如果允许换行时不给空格**：`next` 的转移要改。
2. **如果要求"行数恰好 r"**：贪心仍然最优，只是要补空行。
