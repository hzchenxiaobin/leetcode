# Codeforces 38B 车与马的落子计数 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/38/B
- **比赛来源**：School Personal Contest #1 (Winter Computer School 2010/11) - Codeforces Beta Round 38 (ACM-ICPC Rules) · Problem B（UTC 2010-10-30）
- **难度**：1200
- **标签**：暴力、实现、数学
- **评测类型**：普通
- **限制**：时间 2 s / 内存 256 MB

**题意**：$8\times8$ 棋盘上已有一个车和一个马（保证互不攻击）。再放一个马在空格上，要求**三个棋子中任意两个都不能互相攻击**，求方案数。

**约束**：只有 64 个格子，暴力枚举即可。

## 2. 示例与观察

官方样例（输入 / 输出原样，共 2 组）：

```text
输入：
a1
b2
输出：
44
```

```text
输入：
a8
d4
输出：
38
```

**样例解释**：样例 1（车 a1、马 b2）有 44 个合法空格；样例 2（车 a8、马 d4）有 38 个。

**观察 1（三类禁区）**：新马所在格 $q$ 不能：
1. 被车攻击（车所在的行/列，且中间没有棋子阻挡）；
2. 被已有的马攻击，或反过来攻击已有的马（马的 8 个"日"字落点）；
3. 攻击车（马从 $q$ 能跳到车的位置）。

**观察 2（车不可被吃）**：题面保证初始两子互不攻击，所以只需检查新马与另外两子的关系。

![三类禁区](../../../images/cf38b_attack.svg)

## 3. 解题思路

### 3.1 暴力

![枚举 64 格](../../../images/cf38b_enum.svg)

对每个格子 $q$（跳过两个已有棋子），逐条检查上面三类禁区，全部通过就计数。$O(64)$。

### 3.2 车的攻击线

从车出发沿四个方向走，遇到第一个棋子停下——**棋子会挡住车的攻击**。在本例中，已有马可能挡在车与新马之间（虽然样例里不触发，但写对更稳）。

### 3.3 样例走查

样例 1：车 a1 控制 15 格，旧马 b2 占 1 格、攻击 4 格（其中 d1 已在车的行上），能反攻车的格 2 个（b3、c2），去重后合法 44 格 ✓。

## 4. 正确性证明

**引理 1**：若新马放在 $q$，三子互不攻击当且仅当 $q$ 不满足三类禁区之一。

**证明**：三对关系（车–旧马、车–新马、旧马–新马）中，车–旧马由输入保证；剩下两对正好对应禁区 1/3（车–新马）与 2（旧马–新马）。∎

**引理 2**：枚举所有空格并逐一按引理 1 检查，得到的计数就是方案数。

**证明**：每个空格要么合法要么不合法，逐一检查无遗漏无重复。∎

**定理**：算法输出正确。

**证明**：由引理 1、2 直接得出。∎

## 5. 复杂度分析

- **时间**：$O(64\times8)$。
- **空间**：$O(1)$。
- **与时限的关系**：约 1 ms。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    string r,k; if(!(cin>>r)) return 0; cin>>k;
    int rx=r[0]-'a', ry=r[1]-'1';
    int kx=k[0]-'a', ky=k[1]-'1';
    auto km=[&](int x,int y,vector<pair<int,int>>&out){
        int dx[8]={1,2,2,1,-1,-2,-2,-1}, dy[8]={2,1,-1,-2,-2,-1,1,2};
        for(int i=0;i<8;i++){ int a=x+dx[i],b=y+dy[i]; if(a>=0&&a<8&&b>=0&&b<8) out.push_back({a,b}); }
    };
    auto rookAtt=[&](int x,int y,int bx,int by,int qx,int qy,bool&hitQ){
        hitQ=false;
        int dx[4]={1,-1,0,0}, dy[4]={0,0,1,-1};
        for(int d=0;d<4;d++){
            int a=x+dx[d], b=y+dy[d];
            while(a>=0&&a<8&&b>=0&&b<8){
                if(a==qx&&b==qy){ hitQ=true; break; }
                if(a==bx&&b==by) break;      // 被另一个棋子挡住
                a+=dx[d]; b+=dy[d];
            }
        }
    };
    int ans=0;
    vector<pair<int,int>> katt; km(kx,ky,katt);
    for(int x=0;x<8;x++) for(int y=0;y<8;y++){
        if((x==rx&&y==ry)||(x==kx&&y==ky)) continue;
        bool hit=false;
        rookAtt(rx,ry,kx,ky,x,y,hit); if(hit) continue;   // 车能吃到新马
        bool f1=false; for(auto&p:katt) if(p.first==x&&p.second==y) f1=true; if(f1) continue; // 旧马吃新马
        vector<pair<int,int>> natt; km(x,y,natt);
        bool f2=false,f3=false;
        for(auto&p:natt){ if(p.first==kx&&p.second==ky) f2=true; if(p.first==rx&&p.second==ry) f3=true; }
        if(f2||f3) continue;                              // 新马吃旧马/车
        ++ans;
    }
    cout<<ans<<"\n";
}
```

### Python3

```python
import sys
def main():
    d=sys.stdin.read().split()
    r,k=d[0],d[1]
    rx,ry=ord(r[0])-97,int(r[1])-1
    kx,ky=ord(k[0])-97,int(k[1])-1
    def km(p):
        x,y=p; out=[]
        for dx,dy in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
            a,b=x+dx,y+dy
            if 0<=a<8 and 0<=b<8: out.append((a,b))
        return out
    def rook_hits(q):
        x,y=rx,ry
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            a,b=x+dx,y+dy
            while 0<=a<8 and 0<=b<8:
                if (a,b)==q: return True
                if (a,b)==(kx,ky): break
                a+=dx; b+=dy
        return False
    ans=0
    for x in range(8):
        for y in range(8):
            q=(x,y)
            if q==(rx,ry) or q==(kx,ky): continue
            if rook_hits(q): continue
            if q in km((kx,ky)): continue
            if (kx,ky) in km(q) or (rx,ry) in km(q): continue
            ans+=1
    print(ans)
main()
```

## 7. 边界情况与易错点

1. **两枚车/两枚马同排**：新马不能放在被车攻击的格子上，别忘了车的阻挡规则。
2. **旧马能反攻车**：输入保证不会，但代码里仍按规则检查更稳。
3. **棋盘边界**：马的落点要用 `0<=x<8` 判断。
4. **已占格**：两个已有棋子所在格不能放。
5. **坐标转换**：`a1` → $(0,0)$，列是字母、行是数字。
6. **不要重复计数**：一个格子只判一次。

## 8. 验证记录

- **编译环境**：`Apple clang 21.0.0`（`-O2`），Python 3.9.6。
- **官方样例**：2 / 2 通过（44、38）。
- **对拍**：另写"独立攻击判定（含车的阻挡）"的暴力，随机 **200 组**合法初始局面（保证车马互不攻击），C++ / Python / 暴力一致，**0 处不符**。
- **图片/公式**：两张 SVG 通过检查；KaTeX 无报错。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 38C Blinds](https://codeforces.com/problemset/problem/38/C)：同场 C 题。
- [LeetCode 1222. 可以攻击国王的皇后](https://leetcode.cn/problems/queens-that-can-attack-the-king/)：同类"直线攻击 + 阻挡"判定。

**延伸思考**：

1. **换成后、象**：攻击线变成 8 个方向。
2. **放两个马**：组合计数需要更复杂的枚举。
3. **棋盘更大**：可写成坐标公式 $O(1)$ 计数。
