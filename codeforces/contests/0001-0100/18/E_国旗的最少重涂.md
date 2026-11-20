# Codeforces 18E 国旗的最少重涂 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/18/E
- **比赛来源**：Codeforces Beta Round 18 · Problem E（2010-05-06）
- **难度**：2000
- **标签**：动态规划
- **评测类型**：特殊评测（输出方案）
- **限制**：时间 2 s / 内存 128 MB

**题意**：给 $n\\times m$ 的字母矩阵。要求每行**至多两种颜色**，且任何相邻两格（左右、上下）颜色不同。求最少改多少个格子，并输出方案。

**约束**：$n,m\le500$，颜色 26 种。行内相邻不同 + 每行至多两色 ⇒ 每行的颜色必须是 $abab\dots$ 交替（$m\ge2$ 时 $a
eq b$；$m=1$ 时只有一个颜色）。状态只有 $26^2=676$ 种，逐行 DP 即可。

## 2. 示例与观察

官方样例 1（输入 / 输出原样）：

```text
输入：
3 4
aaaa
bbbb
cccc

输出：
6
abab
baba
acac
```

**样例解释**：每行改成 $abab$ 交替，上下相邻位颜色不同；总共改 6 格。

官方样例 2：

```text
输入：
3 3
aba
aba
zzz

输出：
4
aba
bab
zbz
```

**观察 1（行内结构）**：一行内相邻不同且最多两色 ⇒ 颜色按奇偶位交替。所以一行由 $(c_1,c_2)$ 唯一确定：偶数位 $c_1$、奇数位 $c_2$（$m\ge2$ 时 $c_1
e c_2$）。

**观察 2（行间约束）**：上下相邻要求 $c_1
e c_1'$ 且 $c_2
e c_2'$（同奇偶位的颜色不能相同）。列内没有"最多两色"的限制，只需相邻不同。

![每行两种颜色交替](../../../images/cf18e_stripes.svg)

## 3. 解题思路

### 3.1 朴素做法与瓶颈

枚举每行 $26^2$ 种模式、行间再两两比较，是 $O(n\cdot26^4)$ ≈ $2.3\\times10^8$（C++ 勉强），Python 太慢。可以用"排除一行/一列"的最小值技巧降到 $O(n\cdot26^3)$。

### 3.2 DP 设计

![行间 DP 与状态](../../../images/cf18e_dp.svg)

- **状态**：`dp[c1][c2]` = 处理完前若干行、当前行用 $(c_1,c_2)$ 时的最小重涂数。
- **代价**：`cost[i][c1][c2]` = 第 $i$ 行中不等于对应交替颜色的格子数，可用"偶数位各颜色的计数"直接算：
  $$cost = \\bigl(\lceil m/2
ceil - cnt_{even}[c_1]\\bigr)+\\bigl(\lfloor m/2
floor - cnt_{odd}[c_2]\\bigr).$$
- **转移**：
  $$\\text{ndp}[c_1][c_2]=\min_{a
e c_1,\ b
e c_2}\\text{dp}[a][b]+\\text{cost}[i][c_1][c_2].$$
  为避免 $26^4$，对每一行 $a$ 先求"次小值"，再在 $a
e c_1$ 上取最小，$O(26^3)$。

### 3.3 方案还原

存完整的 `dp[i][c1][c2]` 表（$n\\times26\\times26$ 个 `int`，约 1.4 MB）。从最后一行的最优 $(c_1,c_2)$ 往前推：$want=dp[i][c1][c2]-cost$，找 $a
e c_1$ 且上一行在 $b
e c_2$ 上的最小值等于 $want$ 的 $(a,b)$，即为上一行的选择。

### 3.4 样例走查

样例 1：三行 `aaaa`、`bbbb`、`cccc`。第 1 行取 $(a,b)$ 代价 2，第 2 行取 $(b,a)$ 代价 2，第 3 行取 $(a,c)$ 代价 2，总 6 ✓。

## 4. 正确性证明

**引理 1**：合法的行（$m\ge2$）一定形如 $c_1c_2c_1c_2\dots$，$c_1
e c_2$；$m=1$ 时只有一个颜色。

**证明**：行内相邻不同，若用了第三种颜色 $c$，则它在某个位置必须与左右相邻，而左右位置由交替性只能取两种颜色，矛盾（$m\ge2$）。∎

**引理 2**：两行 $(c_1,c_2)$ 与 $(c_1',c_2')$ 在所有列上相邻不同 $\iff c_1
e c_1'$ 且 $c_2
e c_2'$。

**证明**：偶数列比较 $c_1$ 与 $c_1'$，奇数列比较 $c_2$ 与 $c_2'$，逐列即得。∎

**定理**：DP 求出的最小值就是最少重涂数，回溯得到的矩阵合法且达到该值。

**证明**：由引理 1、2，任何合法方案对应一条状态路径，其代价恰为各行重涂数之和；DP 穷尽所有路径并取最小，故最优值正确。回溯按 `want` 反推的每一步都满足转移等式，拼出的矩阵每行合法、行间合法，重涂数之和等于 DP 值。∎

## 5. 复杂度分析

- **时间**：$O(n\cdot26^3)$（约 $8.8\\times10^6$，加上每行 $O(m)$ 的代价计算）。
- **空间**：$O(n\cdot26^2)$ 的 DP 表（约 1.4 MB）。
- **与时限的关系**：$n=m=500$ 实测远低于 2 s。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
const int C=26, INF=1000000000;
int n,m; vector<string> g;
vector<array<int,C>> cntEven,cntOdd;
int rowCost(int r,int c1,int c2){
    int e=(m+1)/2, o=m/2;
    return (e-cntEven[r][c1]) + (o-cntOdd[r][c2]);
}
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin>>n>>m; g.resize(n); for(auto&r:g) cin>>r;
    cntEven.assign(n,{}); cntOdd.assign(n,{});
    for(int i=0;i<n;i++) for(int j=0;j<m;j++){ int c=g[i][j]-'a'; if(j%2==0) cntEven[i][c]++; else cntOdd[i][c]++; }
    if(m==1){
        vector<array<int,C>> dp(n), par(n);
        for(int c=0;c<C;c++){ dp[0][c]=(g[0][0]-'a'!=c); par[0][c]=-1; }
        for(int i=1;i<n;i++) for(int c=0;c<C;c++){
            int best=INF,bp=-1;
            for(int p=0;p<C;p++) if(p!=c && dp[i-1][p]<best){ best=dp[i-1][p]; bp=p; }
            dp[i][c]=best+(g[i][0]-'a'!=c); par[i][c]=bp;
        }
        int bc=0,bv=INF; for(int c=0;c<C;c++) if(dp[n-1][c]<bv){bv=dp[n-1][c];bc=c;}
        cout<<bv<<"\n";
        vector<int> col(n); int cur=bc;
        for(int i=n-1;i>=0;i--){ col[i]=cur; cur=par[i][cur]; }
        for(int i=0;i<n;i++) cout<<(char)('a'+col[i])<<"\n";
        return 0;
    }
    vector<vector<vector<int>>> dp(n, vector<vector<int>>(C, vector<int>(C, INF)));
    for(int a=0;a<C;a++) for(int b=0;b<C;b++) if(a!=b) dp[0][a][b]=rowCost(0,a,b);
    int rb[C][C];
    for(int i=1;i<n;i++){
        for(int a=0;a<C;a++){
            int m1=INF,b1=-1,m2=INF,b2=-1;
            for(int b=0;b<C;b++){ int v=dp[i-1][a][b]; if(v<m1){m2=m1;b2=b1;m1=v;b1=b;} else if(v<m2){m2=v;b2=b;} }
            for(int c2=0;c2<C;c2++) rb[a][c2]=(c2==b1)?m2:m1;
        }
        for(int c1=0;c1<C;c1++) for(int c2=0;c2<C;c2++) if(c1!=c2){
            int best=INF;
            for(int a=0;a<C;a++) if(a!=c1) best=min(best, rb[a][c2]);
            dp[i][c1][c2]=best+rowCost(i,c1,c2);
        }
    }
    int bv=INF,f1=0,f2=1;
    for(int a=0;a<C;a++) for(int b=0;b<C;b++) if(dp[n-1][a][b]<bv){bv=dp[n-1][a][b];f1=a;f2=b;}
    cout<<bv<<"\n";
    vector<pair<int,int>> seq(n); seq[n-1]={f1,f2};
    for(int i=n-1;i>0;i--){
        int c1=seq[i].first, c2=seq[i].second;
        int want=dp[i][c1][c2]-rowCost(i,c1,c2);
        for(int a=0;a<C;a++) if(a!=c1){
            int m1=INF,b1=-1,m2=INF,b2=-1;
            for(int b=0;b<C;b++){ int v=dp[i-1][a][b]; if(v<m1){m2=m1;b2=b1;m1=v;b1=b;} else if(v<m2){m2=v;b2=b;} }
            int need=(c2==b1)?m2:m1;
            if(need==want){ seq[i-1]={a, (c2==b1)? b2 : b1}; break; }
        }
    }
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++) cout<<(char)('a'+((j%2==0)?seq[i].first:seq[i].second));
        cout<<"\n";
    }
    return 0;
}
```

### Python3

```python
import sys
def main():
    data=sys.stdin.buffer.read().split()
    n=int(data[0]); m=int(data[1]); g=[data[2+i].decode() for i in range(n)]
    C=26; INF=10**9
    ce=[[0]*C for _ in range(n)]; co=[[0]*C for _ in range(n)]
    for i in range(n):
        for j,ch in enumerate(g[i]):
            (ce if j%2==0 else co)[i][ord(ch)-97]+=1
    def cost(i,c1,c2):
        return ((m+1)//2-ce[i][c1]) + (m//2-co[i][c2])
    if m==1:
        dp=[[INF]*C for _ in range(n)]; par=[[-1]*C for _ in range(n)]
        for c in range(C): dp[0][c]=0 if g[0]==chr(97+c) else 1
        for i in range(1,n):
            for c in range(C):
                best=INF; bp=-1
                for p in range(C):
                    if p!=c and dp[i-1][p]<best: best=dp[i-1][p]; bp=p
                dp[i][c]=best+(0 if g[i]==chr(97+c) else 1); par[i][c]=bp
        bc=min(range(C), key=lambda c: dp[n-1][c]); bv=dp[n-1][bc]
        col=[0]*n; cur=bc
        for i in range(n-1,-1,-1): col[i]=cur; cur=par[i][cur]
        print(bv); print("\n".join(chr(97+c) for c in col)); return
    dp=[[[INF]*C for _ in range(C)] for _ in range(n)]
    for a in range(C):
        for b in range(C):
            if a!=b: dp[0][a][b]=cost(0,a,b)
    for i in range(1,n):
        rb=[[INF]*C for _ in range(C)]
        for a in range(C):
            row=sorted(dp[i-1][a])
            m1,m2=row[0],row[1]
            b1=dp[i-1][a].index(m1)
            rest=min(dp[i-1][a][b] for b in range(C) if b!=b1)
            b2=next(b for b in range(C) if b!=b1 and dp[i-1][a][b]==rest)
            for c2 in range(C): rb[a][c2]= (rest if c2==b1 else m1)
        for c1 in range(C):
            for c2 in range(C):
                if c1==c2: continue
                best=min(rb[a][c2] for a in range(C) if a!=c1)
                dp[i][c1][c2]=best+cost(i,c1,c2)
    bv=INF; f1=f2=0
    for a in range(C):
        for b in range(C):
            if dp[n-1][a][b]<bv: bv=dp[n-1][a][b]; f1,f2=a,b
    seq=[None]*n; seq[n-1]=(f1,f2)
    for i in range(n-1,0,-1):
        c1,c2=seq[i]; want=dp[i][c1][c2]-cost(i,c1,c2)
        for a in range(C):
            if a==c1: continue
            row=dp[i-1][a]; b1=row.index(min(row))
            rest=min(row[b] for b in range(C) if b!=b1)
            b2=next(b for b in range(C) if b!=b1 and row[b]==rest)
            need=rest if c2==b1 else row[b1]
            if need==want: seq[i-1]=(a, b2 if c2==b1 else b1); break
    out=[str(bv)]
    for i in range(n):
        out.append(''.join(chr(97+(seq[i][0] if j%2==0 else seq[i][1])) for j in range(m)))
    sys.stdout.write('\n'.join(out)+'\n')
main()
```

## 7. 边界情况与易错点

1. **$m=1$**：每行只有一种颜色，退化成"相邻行不同"的一维 DP，必须单独处理（交替公式会用到 $c_2$）。
2. **$c_1=c_2$ 非法**（$m\ge2$）：同一行相邻两格会同色，状态要跳过。
3. **行间两个颜色都要比较**：只比 $c_1$ 会漏掉奇数列的冲突。
4. **重涂数统计**：用奇偶位计数，避免逐格重算（$O(n\cdot26^2\cdot m)$ 也能过，但慢）。
5. **方案还原**：回溯时要用"上一行的 dp 表 + 排除 $c_2$ 的最小值"，否则可能拼出不满足列约束的矩阵。
6. **特殊评测**：任何最优方案都接受，本地要用 checker 验证合法性、重涂数以及最优性。
7. **字母映射**：统一 `c-'a'`，输出时 `+'a'`。

## 8. 验证记录

- **编译环境**：`Apple clang 21.0.0`（`-O2`），Python 3.9.6。特殊评测，checker 校验：每行至多两色、行列相邻不同、重涂数等于输出值，并用独立 DP 复核最优值。
- **官方样例**：2 / 2 通过（6、4，方案与样例不同但 checker 判定合法且最优）。
- **对拍**：随机 **80 组**（$n,m\le6$，颜色 `a/b/c/z`），C++ 与 Python 的方案都通过 checker（合法性 + 重涂数一致 + 最优性），**0 处不符**；另外与题面样例的答案值一致。
- **性能**：$n=m=500$ 远低于 2 s。
- **图片/公式**：两张 SVG 通过检查；KaTeX 无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 18D Seller Bob](https://codeforces.com/problemset/problem/18/D)：同场 D 题。
- [LeetCode 1411. 给 N x 3 网格图涂色的方案数](https://leetcode.cn/problems/number-of-ways-to-paint-n-3-grid/)：行内模式 + 行间转移的同类 DP。

**延伸思考**：

1. **每行至多 $k$ 种颜色**：状态变成排列数 $26\cdot25\cdots$，$k$ 稍大就不可行，需要状态压缩或贪心。
2. **列也有"至多两色"限制**：行列同时约束，问题变成网格着色，可能需要流/匹配。
3. **要求字典序最小的方案**：在 DP 值相同时加二次比较，或从前往后贪心 + 后缀 DP。
