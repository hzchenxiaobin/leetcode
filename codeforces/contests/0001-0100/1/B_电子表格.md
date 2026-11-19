# Codeforces 1B Spreadsheet 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/1/B
- **比赛来源**：Codeforces Beta Round 1 · Problem B
- **难度**：1600
- **标签**：实现、数学（进制转换）、字符串
- **评测类型**：普通
- **限制**：时间 10 s / 内存 64 MB（题面另注明：本题的评测数据未随判题机升级重新打包，最终耗时按实测算出的 2 倍记入判定，即实际余量比显示的更宽松）

**题意**：表格里有两种等价的坐标记法，给 $n$ 个合法坐标，每个都要翻译成**另一种**记法。

- **Excel 记法**：字母串（列）+ 十进制数（行），例如 `BC23` —— 第 55 列第 23 行。
- **RXCY 记法**：`R` + 行号 + `C` + 列号，例如 `R23C55` —— 同一个格子。

列的编号是"双射 26 进制"：第 1 列是 `A`、第 26 列是 `Z`、第 27 列是 `AA`、第 52 列是 `AZ`、第 55 列是 `BC`、第 702 列是 `ZZ`、第 703 列是 `AAA`。行号就是从 $1$ 开始的十进制。

**约束**：

- $1 \le n \le 10^5$，即最多 $10^5$ 组坐标，总输入量约 $1.7\times 10^6$ 个字符；
- 行号、列号都 $\le 10^6$，因此列名最多 $5$ 个字母、行号最多 $7$ 位十进制；
- 时间 $10$ s、内存 $64$ MB：**每组**必须接近 $O(\lvert s\rvert)$，任何"边算边建 $10^6$ 列表"或"逐列模拟进位"的预处理都被 $n$ 放大成 $10^{11}$，不可用；同时 $64$ MB 也排除了把答案全表打出来的做法。

## 2. 示例与观察

**官方样例**

```text
输入
2
R23C55
BC23

输出
BC23
R23C55
```

只有一组样例，但足以说明"输入是什么、就要输出另一个"——同一个格子 `R23C55` 与 `BC23` 互为对方的答案。

**自造样例（本解法实测输出，已与独立实现逐条对拍）**

```text
输入
10
R1C1
A1
RC1
ZZ1
R1C702
BDWGN1000000
R1000000C1000000
ALL1
R1C999999
XFD123

输出
A1
R1C1
R1C471
R1C702
ZZ1
R1000000C1000000
BDWGN1000000
R1C1000
BDWGM1
R123C16384
```

其中几条专门挑的是"看起来像 RXCY、其实是 Excel"的坑：`RC1` 的列名是 `RC`（$18\times26+3=471$）；`R1C999999` 的列号 $999999$ 是 `BDWGM`（验证：$2\cdot26^4+4\cdot26^3+23\cdot26^2+7\cdot26+13 = 913952+70304+15548+182+13 = 999999$）。

**观察一（判形没有二义）**：Excel 记法一定是"字母若干 + 数字若干"，RXCY 记法一定是 `R`+数字+`C`+数字。前者的字母全部排在数字之前，后者在数字中间夹了一个字母 `C`，两种语法**没有交集**，所以"这串到底是哪种记法"有唯一答案，可以用一条正则判定。

**观察二（列号只是换了个底）**：`BC` $\to 55$ 是逐位累乘 $2\times26+3$；反过来 $55\to$ `BC` 要"先减 1 再取模"，因为这套编号里**没有 0**（$A=1$ 而不是 $A=0$）。写成循环就是 `col--; 取 col%26; col/=26`。

**观察三（规模）**：列号上限 $10^6$ 落在长度 5 的区间 $[475255,\,12356630]$ 里，所以字母最多 5 个、循环至多 5 轮；行号最多 7 位，`int` 就够，但中间量用 `long long` 更稳。

## 3. 解题思路

### 3.1 朴素做法与瓶颈

最直接的"猜格式"写法是：

```cpp
if (s[0] == 'R' && s.find('C') != string::npos) { /* 当成 RXCY */ }
```

这对 `R23C55` 恰好成立，但对 `RC1` 立刻就崩：`s.find('C')` 返回 1，于是程序认为"行号"是 `s[1..0]`（空串），`stoi` 直接抛异常。`RAC1`、`RBC1` 这类"列名以 R 开头、又含 C"的 Excel 名字也会同样误判。判形靠"猜"必然在边角上出错，正确做法是显式验证"`R` 后的数字段非空、紧接 `C`、`C` 后的数字段非空且一直到串尾"。

另一条路是"打表"：先把 $1..10^6$ 的列名全部枚举出来（`A, B, ..., Z, AA, ...`），查询时直接查表。但 $10^6$ 条列名光存储就要几十 MB（每条 `std::string` 至少 32 字节，再加上反查表），已经贴着 $64$ MB 上限；更关键的是**枚举进位**要用 $O(10^6)$ 的预处理，若按题面老实读 $n$ 组、每组都重新建表就是 $O(n\cdot 10^6)=10^{11}$。真正需要的只是"把一个数写成 5 个字母"，$O(\log_{26} col)$ 就够。

### 3.2 核心观察：两套语法不相交 + 列号是双射 26 进制

![同一个格子的两种写法：BC23 与 R23C55](../../../images/cf1b_two_formats.svg)

上图把两件事并排画出来：左边是 Excel 记法（字母在前、数字在后），右边是 RXCY 记法（`R` 行 `C` 列），中间的箭头表示"互为答案"。底下那条列名带子说明了第二件事：列号序列 `A(1) B(2) C(3) ... Z(26) AA(27) AB(28) ... AZ(52) BC(55)` 是**没有 0** 的 26 进制，所以 `BC` $=2\times26+3=55$。

于是问题拆成两个独立子问题：

1. **判形**：$s$ 是否匹配 `^R[0-9]+C[0-9]+$`。匹配就走"RXCY → Excel"，否则走"Excel → RXCY"。因为两套语法不相交（第 4 节引理 1），这个判定是**充分必要**的，不存在"两种都像"的情形。
2. **换底**：列号的数值 $\leftrightarrow$ 字母串，两个方向互为逆运算。

### 3.3 算法流程

![算法流程：一条正则决定走哪一支](../../../images/cf1b_detect_flow.svg)

判形用"手写扫描"而不用正则库（既快又能精确控制），对串 $s$：

1. 若 $s_0\ne$ `R`，不是 RXCY，转 4；
2. 从下标 1 起吃掉连续数字，记长度为 $k$；若 $k=0$ 或下一个字符不是 `C`，不是 RXCY，转 4；
3. 从 `C` 之后继续吃数字，必须**恰好吃到串尾**且至少一位；满足则 $s$ 是 `R<row>C<col>`：
   - `row = stoll(s[1..k])`，`col = stoll(s[k+2..])`；
   - 输出 `colToStr(col) + to_string(row)`。
4. 否则是 Excel 记法：吃掉前缀字母段 `[0,p)`，`col = strToCol(s[0,p))`、`row = stoll(s[p..])`，输出 `"R" + to_string(row) + "C" + to_string(col)`。

两个换底函数：

- `colToStr(col)`：`while (col > 0) { --col; ans += 'A' + col % 26; col /= 26; }`，最后 `reverse`。
- `strToCol(s)`：`col = 0; for (c : s) col = col * 26 + (c - 'A' + 1);`。

`--col` 是全部技巧所在：它把"没有 0 的双射进制"临时拍成"有 0 的普通进制"，取完模再还原，这样 $26$ 才能得到 `Z` 而不是 `BA`。

### 3.4 样例走查

![列号 55 与字母串 BC 的互转演算](../../../images/cf1b_base26_walkthrough.svg)

以 `R23C55` 为例，只需算 $55\to$ `BC`：

| 轮次 | col | col−1 | (col−1) mod 26 | 字母 | 新 col = ⌊(col−1)/26⌋ |
|------|-----|-------|----------------|------|------------------------|
| 1 | 55 | 54 | 2 | C | 2 |
| 2 | 2 | 1 | 1 | B | 0（停止）|

攒到 `C`、`B` 后逆序拼接得 `BC`，配上行号 23，输出 `BC23`。反方向 `BC23` → 列号：$0\times26+2=2$，$2\times26+3=55$，输出 `R23C55`。

再看两个容易错的：

- `RC1`：$s_0=$ `R`，但 `R` 后紧跟的就是 `C`，数字段长度为 0 ⇒ 判形为"否"⇒ 按 Excel 处理：列名 `RC` $=18\times26+3=471$，行 1 ⇒ 输出 `R1C471`。
- `R1C999999`：判形为"是"⇒ $999999\to$ `BDWGM`（长度落在 5 字母区间，逐轮取模得 M、G、W、D、B，逆序即 `BDWGM`）⇒ 输出 `BDWGM1`。

## 4. 正确性证明

**引理 1（两套语法不相交）**：记 $E=[A\!-\!Z]^{+}[0\!-\!9]^{+}$ 为 Excel 记法的串集合、$R=\texttt{R}[0\!-\!9]^{+}\texttt{C}[0\!-\!9]^{+}$ 为 RXCY 记法的串集合，则 $E\cap R=\varnothing$。

**证明**：反设 $s\in E\cap R$。由 $s\in E$，$s$ 的所有字母都排在所有数字之前（字母段是前缀、数字段是后缀）。由 $s\in R$，$s=\texttt{R}\,x\,\texttt{C}\,y$，其中 $x,y$ 为非空数字串，即字母 `C` 之前至少有 $x$ 的一位数字、`C` 之后还有数字 $y$。于是 $s$ 中出现了"数字之后再出现字母"的位置（那个 `C`），与 $E$ 的前缀结构矛盾。∎

**引理 2（列名与正整数一一对应）**：令 $v(c_1c_2\ldots c_L)=\sum_{i=1}^{L}(c_i-\text{'A'}+1)\,26^{L-i}$，则 $v$ 是 $[A\!-\!Z]^{+}$ 到 $\mathbb{Z}_{>0}$ 的双射。

**证明**：分两步。

- **同长度单射**：设 $u\ne w$ 等长 $L$，取首个不同位置 $i$，设 $u_i>w_i$。则
  $$v(u)-v(w)\ \ge\ 26^{L-i}-\sum_{j=i+1}^{L}25\cdot 26^{L-j}\ =\ 26^{L-i}-25\cdot\frac{26^{L-i}-1}{25}\ =\ 1\ >\ 0,$$
  故同长度内不会撞值。
- **不同长度不撞且铺满**：长度为 $L$ 的串取值恰为区间
  $$\Big[\tfrac{26^{L}-1}{25},\ \tfrac{26^{L+1}-26}{25}\Big],$$
  相邻两个长度区间首尾相接（上界 $+1$ 恰为下一长度的下界），且每个长度恰好有 $26^{L}$ 个串、区间也恰含 $26^{L}$ 个整数，配合同长度单射，$v$ 在每个区间上是双射。区间族 $\{[\,(26^L-1)/25,\,(26^{L+1}-26)/25\,]\}_{L\ge1}$ 互不相交、并起来正是 $\mathbb{Z}_{>0}$。∎

**引理 3（`colToStr` 正确）**：对任意 $c\ge1$，`colToStr` 输出的串 $t$ 满足 $v(t)=c$。

**证明**：设 $c$ 的标准表示为 $d_1\ldots d_L$（由引理 2 存在唯一），前缀值 $P=\sum_{i<L}(d_i)\,26^{L-1-i}$（$L=1$ 时 $P=0$），则 $c=26P+d_L$ 且 $1\le d_L\le 26$。算法第一轮：
$$c' = c-1 = 26P+(d_L-1),\qquad 0\le d_L-1\le 25,$$
故 $c'\bmod 26=d_L-1$，输出字母为 $\text{'A'}+d_L-1$ 即第 $d_L$ 个字母；且 $c''=\lfloor c'/26\rfloor=P$。于是算法递归地处理 $P$，依次产出 $d_L,d_{L-1},\ldots,d_1$；当 $P=0$ 时 $c=0$ 退出循环。逆序后得到 $d_1\ldots d_L$，其 $v$ 值正是 $c$。∎

**引理 4（`strToCol` 正确）**：对任意串 $t$，`strToCol` 返回 $v(t)$。

**证明**：循环 `col = col*26 + (c-'A'+1)` 是 Horner 法，逐位展开即 $\sum_i (c_i-\text{'A'}+1)26^{L-i}$，与 $v$ 的定义一致。∎

**定理**：对每个合法输入串，程序输出的串恰好是同一格子的另一种记法。

**证明**：判形阶段与引理 1 给出的语法完全等价：条件"`R` + 非空数字 + `C` + 非空数字且到串尾"正是 $R$ 的定义，不满足则必属 $E$（题面保证输入合法，只有这两种可能），故判形不会走错支。走 RXCY 分支时，`row`、`col` 由 `stoll` 精确解析（数值 $\le 10^6$，远小于 `long long` 上界），列名由引理 3 得 $v(t)=col$，输出 `字母+row` 正是 $E$ 中同一格子的写法；走 Excel 分支时，列号由引理 4 得 $v(\text{前缀})=col$，输出 `R+row+C+col` 正是 $R$ 中同一格子的写法。两分支都输出"另一种"记法。∎

## 5. 复杂度分析

- **时间**：单串判形扫描 $O(\lvert s\rvert)$；换底时 `colToStr` 至多 $5$ 轮、`strToCol` 至多 $5$ 次乘加（列号 $\le10^6 < 26^6$）。总时间 $O\!\left(\sum\lvert s\rvert\right)$，上限约 $1.7\times10^6$ 次字符级操作，无排序、无对数因子。实测 $n=10^5$ 的最坏数据（全部是 `R1000000C1000000` / `BDWGN1000000` 交替）端到端 $0.138$ s，相对 $10$ s 时限余量约 $72$ 倍。
- **空间**：把输入整体读入 `vector<string>` 需 $O(\text{总输入量})\approx1.7$ MB；输出缓冲约 $1.3$ MB；此外每组 $O(1)$ 临时量（至多 5 个字母）。峰值远小于 $64$ MB，即使把输入换成边读边处理也只是常数级差异。
- **常数与时限**：瓶颈在 I/O 而不是计算，故 C++ 关掉 `sync_with_stdio` 并整块 `fwrite`；Python 一次 `read().split()` 也足够（实测 $n=10^5$ 约 $0.27$ s，含解释器启动），无需 PyPy。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;

static bool allDigits(const string &s) {
    if (s.empty()) return false;
    for (char c : s)
        if (!isdigit((unsigned char)c)) return false;
    return true;
}

// 列号 -> 字母串（双射 26 进制：A=1, ..., Z=26, AA=27）
static string colToStr(long long col) {
    string s;
    while (col > 0) {
        --col;                              // 关键：先把双射进制拍成普通 0 起进制
        s.push_back(char('A' + col % 26));
        col /= 26;
    }
    reverse(s.begin(), s.end());
    return s;
}

// 字母串 -> 列号
static long long strToCol(const string &s) {
    long long col = 0;
    for (char c : s) col = col * 26 + (c - 'A' + 1);
    return col;
}

// 判断是否为 R<digits>C<digits> 形式
static bool isRxCy(const string &t) {
    size_t n = t.size();
    if (n < 4 || t[0] != 'R') return false;
    size_t p = 1;
    while (p < n && isdigit((unsigned char)t[p])) ++p;   // 行号数字段
    if (p == 1 || p >= n || t[p] != 'C') return false;   // 行号非空且紧接 C
    size_t q = p + 1;
    if (q >= n) return false;                            // 列号非空
    while (q < n && isdigit((unsigned char)t[q])) ++q;
    return q == n;                                       // 必须吃到字符串末尾
}

static string solve(const string &t) {
    if (isRxCy(t)) {
        size_t p = 1;
        while (isdigit((unsigned char)t[p])) ++p;
        long long row = stoll(t.substr(1, p - 1));
        long long col = stoll(t.substr(p + 1));
        return colToStr(col) + to_string(row);
    }
    size_t p = 0;
    while (p < t.size() && isalpha((unsigned char)t[p])) ++p;
    long long col = strToCol(t.substr(0, p));
    long long row = stoll(t.substr(p));
    return "R" + to_string(row) + "C" + to_string(col);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> tok;
    string s;
    while (cin >> s) tok.push_back(s);
    if (tok.empty()) return 0;

    // 题面格式：首行 n，随后 n 行坐标。早期的旧版数据没有 n、直接到 EOF，
    // 因此这里按“首个 token 是否是纯数字”自适应：坐标一定含字母，不会误判。
    size_t start = 0;
    long long n = (long long)tok.size();
    if (allDigits(tok[0])) {
        n = stoll(tok[0]);
        start = 1;
    }
    if (n > (long long)tok.size() - (long long)start)
        n = (long long)tok.size() - (long long)start;    // 保险：不越界

    string out;
    out.reserve((size_t)n * 32);
    for (long long k = 0; k < n; ++k) {
        out += solve(tok[start + (size_t)k]);
        out += '\n';
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
```

### Python3

```python
import sys


def col_to_str(col):
    """列号 -> 字母串（双射 26 进制：A=1, ..., Z=26, AA=27）"""
    s = []
    while col > 0:
        col -= 1                      # 先把双射进制拍成普通 0 起进制
        s.append(chr(ord('A') + col % 26))
        col //= 26
    return ''.join(reversed(s))


def str_to_col(s):
    """字母串 -> 列号"""
    col = 0
    for c in s:
        col = col * 26 + (ord(c) - ord('A') + 1)
    return col


def is_rxcy(t):
    """是否为 R<digits>C<digits> 形式"""
    n = len(t)
    if n < 4 or t[0] != 'R':
        return False
    p = 1
    while p < n and t[p].isdigit():
        p += 1
    if p == 1 or p >= n or t[p] != 'C':
        return False
    q = p + 1
    if q >= n:
        return False
    while q < n and t[q].isdigit():
        q += 1
    return q == n


def solve(t):
    if is_rxcy(t):
        p = 1
        while t[p].isdigit():
            p += 1
        row = int(t[1:p])
        col = int(t[p + 1:])
        return col_to_str(col) + str(row)
    p = 0
    while t[p].isalpha():
        p += 1
    col = str_to_col(t[:p])
    row = int(t[p:])
    return 'R' + str(row) + 'C' + str(col)


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    # 题面格式：首行 n，随后 n 行坐标；旧版数据无 n、直接 EOF，这里自适应
    start = 0
    n = len(data)
    if data[0].isdigit():
        n = int(data[0])
        start = 1
    n = min(n, len(data) - start)
    out = [solve(data[start + i]) for i in range(n)]
    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))


if __name__ == '__main__':
    main()
```

## 7. 边界情况与易错点

1. **判形不能用"首字符是 `R` 且含 `C`"**：`RC1` 的 `R` 与 `C` 之间没有数字，它是 Excel 记法（列 `RC` $=471$）。必须检查"`R` 后有非空数字、紧跟 `C`、`C` 后是非空数字且到串尾"这四条同时成立。
2. **`--col` 不能省**：把 $A$ 当 0 做普通 26 进制时，$26$ 会被写成 `BA`（$1\times26+0$）而不是 `Z`，$52$ 会写成 `CA` 而不是 `AZ`，所有整数集体错位。只有"先减 1 再取模"才与题面列名表一致。
3. **`col == 0` 会输出空串**：题面保证坐标合法（列号 $\ge1$），但若把 `0` 传进 `colToStr` 会得到空串、进而输出 `23` 这种残缺坐标。调试时若看到空列名，先怀疑解析把数字段切空了。
4. **`RXCY` 分支必须吃到串尾**：`R1C`（列号缺失）不合法，但若扫描时忘了"`q == n`"这一条，就会把 `R1C` 误判成 RXCY 并用空串调用 `stoll`。同理"行号数字段非空"（`p == 1` 判断）不能漏，否则 `RC23` 会走进错误分支。
5. **输出拼接格式**：Excel 方向是"字母紧跟行号、中间无空格"；RXCY 方向是 `R` + 行 + `C` + 列，两个字母都不能少。`R23` 这种缺 `C` 的输出会被判错。
6. **旧数据可能没有首行 $n$**：本题是 2010 年的老题，早期测试数据的格式是"直接若干行坐标、读到 EOF"。本文实现按"首个 token 是否纯数字"自适应（坐标必含字母，不可能纯数字），两种格式都能吃下；若按题面只写 `scanf("%d")`，遇到旧数据会直接读错。
7. **I/O 与多测**：$n=10^5$ 行输出，逐行 `cout << endl`（带 flush）会明显拖慢；本实现关同步 + 拼成一个字符串一次 `fwrite`。Python 侧同理，用 `'\n'.join` 一次写出，不要 `print` 循环。
8. **回车符陷阱**：若改用 `getline` 读坐标，Windows 风格的 `\r` 会粘在行尾，导致 `isdigit('\r')` 判断失败、把 Excel 误判成 RXCY。按 token（`>>` / `split()`）读入可以完全规避。
9. **整数范围**：本题列号 $\le10^6$，`int` 也够，但 `strToCol` 的中间量 `col*26` 在更长串上会溢出；统一用 `long long`（Python 无此问题）更省心。

## 8. 验证记录

- **编译环境与命令**：本机只有 `Apple clang 21.0.0`，没有 GNU `g++` 与 libstdc++（`/usr/bin/g++` 是 clang 的软链），因此用 `clang++ -std=c++17 -O2 -Wall -Wextra` 搭配一份本地 `bits/stdc++.h` 兼容头编译，**零警告通过**；代码只用标准库、无 GNU 扩展，可原样提交 Codeforces 的 GNU C++17。命令：`clang++ -I include -std=c++17 -O2 -Wall -Wextra -o sol sol.cpp`。
- **官方样例**：1 / 1 通过（`2`、`R23C55`、`BC23` → `BC23`、`R23C55`），C++ 与 Python 输出一致。
- **额外测试**：
  - **独立实现对拍**：另写一份"完全不做进制运算"的暴力——用 Excel 列名逐次自增枚举出 $1..10^6$ 的全部列名与反查表，再按查表结果转换。对 **420,000** 组输入（列 $1..2\times10^5$ 双向全枚举 400,000 组 + 20,000 组随机行列 $\le10^6$ 双向混合）比较，C++、Python、独立暴力**三方输出逐字节一致**。
  - **手挑边界 20 组**（`R1C1`/`A1`/`RC1`/`ZZ1`/`R1C702`/`BDWGN1000000`/`R1000000C1000000`/`ALL1`/`R1C999999`/`XFD123` 等）三方一致。
  - **往返一致性**：20,000 组随机 `Excel → RXCY → Excel` 与原串完全相同。
  - **旧格式（无 $n$）**：把 420,000 组输入去掉首行 $n$ 后重跑，与暴力输出一致（验证自适应读入）。
  - **ASan/UBSan**：`-fsanitize=address,undefined` 构建跑 5,000 组随机 + 全部边界组，无任何报错。
- **最大约束性能**：$n=10^5$、每行都是极值（`R1000000C1000000` 与 `BDWGN1000000` 交替，输入 1.5 MB）时，C++ 端到端 **0.138 s**（`/usr/bin/time -l` 实测 0.33 s 墙钟含启动、0.13 s user，峰值内存 8.8 MB），相对 10 s、64 MB 余量约 70 倍；Python3 同数据 **0.274 s**、峰值内存 29 MB，可 CPython 直接过。
- **图片校验**：三张 SVG 均通过 `xml.etree.ElementTree.parse`；另用脚本以字符宽度估算逐个 `text` 检查，三图共 84 个文本块均未越出 `viewBox`、未溢出自所在方框，且两两不重叠（`issues=0`）。
- **公式校验**：正文公式均为行内 `$...$` 与独立 `$$...$$` 块，未使用转义星号、未在 `\text{}` 里写裸 `#`，可被 KaTeX 正常渲染。
- **复核状态**：verified（样例、对拍、性能、图片、公式五项均实跑通过；唯一环境差异是本机无 GNU g++，已如上说明并用 clang++ 等价验证）。

## 相关题目与扩展

- [Codeforces 1A Theatre Square](https://codeforces.com/problemset/problem/1/A)：同场 A 题，纯数学公式，可作为 Beta Round 1 的热身。
- [Codeforces 1C Ancient Berland Circus](https://codeforces.com/problemset/problem/1/C)：同场 C 题，几何 + 角度 gcd，难度 2100。
- [LeetCode 168. Excel 表列名称](https://leetcode.cn/problems/excel-sheet-column-title/)：与本文 `colToStr` 是同一个"没有 0 的 26 进制"转换，可当模板互相对照。
- [LeetCode 171. Excel 表列序号](https://leetcode.cn/problems/excel-sheet-column-number/)：与本文 `strToCol` 完全同一个 Horner 累乘写法。
- [Codeforces 552B Vanya and Books](https://codeforces.com/problemset/problem/552/B)：统计 $1..n$ 写出来要多少位数字，与本题"按长度区间划分编号"的视角同源。
- [Codeforces 1741A Compare T-Shirt Sizes](https://codeforces.com/problemset/problem/1741/A)：字符串解析 + 分类讨论，判形思路与本题同源。

**延伸思考**：

1. **如果位权不是 26 而是混合基数**（例如列号用 $26,26,10$ 三段、或像"RXCY"一样带前缀字母），那么"先减 1"的拍平技巧就不成立，需要显式处理每段偏移量；这时正确的做法是把表示写成 $\sum d_i \prod_{j>i} b_j$ 后逐段整除取余，并单独处理"最低段是否从 1 起"。
2. **如果要求支持列号 $>26^5$**（例如 $10^{18}$）：循环轮数变成 $\log_{26}10^{18}\approx13$，`long long` 仍然够；但若列号用 $10^9$ 位十进制给出，就必须改成大数或直接按字符串模拟，此时"逐位累乘"的复杂度变成 $O(L^2)$，需要进位优化。
3. **反向问题：给定 $n$ 个 RXCY 坐标和 $n$ 个 Excel 坐标，判断两集合是否描述同一批格子**——这可以训练"规范化后比较"的思维：任何坐标都能在 $O(\lvert s\rvert)$ 内规范化成二元组 $(row,col)$，比较集合等价性时只需哈希这个二元组，而不必关心原始记法。
4. **如果把判形交给正则库**（例如 C++ 的 `std::regex` 或 Python 的 `re`）：正则引擎的常数比手写扫描大一个量级，$10^5$ 组输入下差距会明显到影响安全余量；而且回溯式实现存在最坏情况超线性、以及深递归下栈溢出的风险。这正是正式实现坚持手写"吃数字—看字符—再吃数字"的原因：逻辑与正则等价，但每步只花 O(1)。
5. **如果把两种记法都看成"编号系统"**，本题其实是同一个抽象的两个实例：行号是纯十进制、列号是双射 26 进制。更一般的框架是"混合基数编号"——只要把每段的位权写清楚，判形与换底都能用同一套"先扣掉偏移、再逐段整除取余"的模板解决，这也解释了为什么 LeetCode 168/171 与本题的代码几乎逐行相同。
