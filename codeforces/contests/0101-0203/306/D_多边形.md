# Codeforces 306D Polygon 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/306/D
- **比赛来源**：Testing Round 6 · Problem D（UTC 2013-05-20）
- **难度**：2300
- **标签**：构造、计算几何
- **评测类型**：多解（任意合法多边形，浮点 $10^{-3}$）
- **限制**：时间 1 s / 内存 256 MB

**题意**：构造一个 $n$ 边形，要求：**所有内角相等**、**所有边长互不相同**，边长落在 $[1,1000]$，顶点坐标绝对值 $\le 10^6$，按逆时针输出。无解输出 `No solution`。

**约束**：$3 \le n \le 100$。

## 2. 示例与观察

官方样例 1：

```text
输入：
8

输出：
1.000 0.000
7.000 0.000
9.000 2.000
9.000 3.000
5.000 7.000
3.000 7.000
0.000 4.000
0.000 1.000
```

**观察 1（等角 ⟺ 方向序列固定）**：所有内角相等等价于**外角**都等于 $2\pi/n$。于是第 $k$ 条边的方向固定为 $\theta_k = \theta_0 + 2\pi k/n$，多边形完全由 $n$ 个边长 $l_k$ 决定。

**观察 2（闭合条件）**：令 $\zeta = e^{2\pi i/n}$，则

$$\sum_{k=0}^{n-1} l_k \zeta^k = 0$$

（两个实方程），即边长的"零和"约束。

**观察 3（$n=3,4$ 无解）**：$n=3$ 时等角 ⟹ 等边；$n=4$ 时等角 ⟹ 矩形 ⟹ 对边相等。都违反"边长互不相同" ✓。

**观察 4（$n\ge5$ 的构造）**：自由度为 $n-2$。固定前 $n-2$ 条边为 $450\sim550$ 内**随机且彼此远离**的值，把最后两条边当作未知数解 2×2 实线性方程组使闭合精确成立；再检查"所有边长两两相差 $\ge 10^{-2}$"与"落在 $[1,1000]$"，不行就重试（随机重试几乎一次就成功）。

## 3. 解题思路

![等角多边形 ⟺ 方向序列固定](../../../images/cf306d_close.svg)

解出 $l_0..l_{n-1}$ 后，按 $\theta_k$ 依次走边即得顶点。

## 4. 正确性证明

**引理 1**：各内角相等 ⟺ 各边方向构成公差 $2\pi/n$ 的等差数列。

**证明**：相邻边的方向差就是外角，$n$ 个外角和为 $2\pi$ ✓。∎

**引理 2**：边长为正且方向按上述等差数列时，多边形闭合 ⟺ $\sum l_k\zeta^k=0$，且此时它是**逆时针凸**的。

**证明**：闭合即向量和为零 ✓；外角恒为 $2\pi/n>0$ 且边长 $>0$ ⟹ 凸且逆时针 ✓。∎

**引理 3**：方程组 $\sum_{k<n-2} l_k\zeta^k + l_{n-2}\zeta^{n-2} + l_{n-1}\zeta^{n-1} = 0$ 的系数行列式非零（$n\ge5$）。

**证明**：否则 $\zeta^{n-2}, \zeta^{n-1}$ 在实数上线性相关，即两者夹角为 $0$ 或 $\pi$，要求 $n \mid 2$，与 $n\ge5$ 矛盾 ✓。∎

**定理**：算法对 $n\ge5$ 输出合法多边形，对 $n=3,4$ 输出 `No solution`。

**证明**：由引理 1–3，构造满足等角与闭合；随机检查保证边长互异且在范围内；$n=3,4$ 由观察 3 不可行 ✓。∎

## 5. 复杂度分析

- **时间**：$O(n)$（随机重试次数期望 $O(1)$）。
- **空间**：$O(n)$。
- **与时限的关系**：实测端到端 ≈2 ms（$n=100$）。

## 6. 参考代码

### C++17

```cpp
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n; if(scanf("%d",&n)!=1) return 0;
    if(n==3 || n==4){ printf("No solution\n"); return 0; }
    const double PI = acos(-1.0);
    // 等角多边形：边方向固定为 theta_k = 2*pi*k/n，闭合条件 sum l_k zeta^k = 0。
    // 固定前 n-2 条边为 500+小扰动，解最后两条边的长度使其闭合（2x2 实线性方程）。
    mt19937 rng(12345);
    for(int attempt=0; attempt<20000; attempt++){
        vector<double> l(n);
        vector<double> dx(n), dy(n);
        for(int k=0;k<n;k++){ dx[k]=cos(2*PI*k/n); dy[k]=sin(2*PI*k/n); }
        bool ok=true;
        for(int k=0;k<n-2;k++){
            l[k] = 500.0 + (double)(rng()%1000000)/1000000.0*100.0 - 50.0;  // [450,550] 连续随机
        }
        // 解 l_{n-2}*dx + l_{n-1}*dx = -sum_{k<n-2} ...
        double rx=0, ry=0;
        for(int k=0;k<n-2;k++){ rx += l[k]*dx[k]; ry += l[k]*dy[k]; }
        int a=n-2, b=n-1;
        double det = dx[a]*dy[b] - dy[a]*dx[b];
        if(fabs(det) < 1e-12) continue;
        l[a] = (-rx*dy[b] + ry*dx[b]) / det;
        l[b] = (-ry*dx[a] + rx*dy[a]) / det;
        if(l[a] < 1.0 || l[a] > 1000.0 || l[b] < 1.0 || l[b] > 1000.0) continue;
        vector<double> s = l; sort(s.begin(), s.end());
        for(int i=0;i+1<n;i++) if(s[i+1]-s[i] < 1e-2){ ok=false; break; }
        if(!ok) continue;
        double x=0,y=0;
        for(int k=0;k<n;k++){
            printf("%.6f %.6f\n", x, y);
            x += l[k]*dx[k];
            y += l[k]*dy[k];
        }
        return 0;
    }
    printf("No solution\n");
    return 0;
}
```

### Python3

```python
import sys, math, random
def main() -> None:
    n = int(sys.stdin.buffer.read().split()[0])
    if n in (3, 4):
        print("No solution"); return
    PI = math.pi
    dx = [math.cos(2*PI*k/n) for k in range(n)]
    dy = [math.sin(2*PI*k/n) for k in range(n)]
    rng = random.Random(12345)
    for _ in range(20000):
        l = [450.0 + rng.random()*100.0 for _ in range(n-2)]
        rx = sum(l[k]*dx[k] for k in range(n-2))
        ry = sum(l[k]*dy[k] for k in range(n-2))
        a, b = n-2, n-1
        det = dx[a]*dy[b] - dy[a]*dx[b]
        if abs(det) < 1e-12: continue
        la = (-rx*dy[b] + ry*dx[b]) / det
        lb = (-ry*dx[a] + rx*dy[a]) / det
        if not (1.0 <= la <= 1000.0 and 1.0 <= lb <= 1000.0): continue
        l = l + [la, lb]
        s = sorted(l)
        if any(s[i+1]-s[i] < 1e-2 for i in range(n-1)): continue
        x = y = 0.0; out = []
        for k in range(n):
            out.append("%.6f %.6f" % (x, y))
            x += l[k]*dx[k]; y += l[k]*dy[k]
        sys.stdout.write("\n".join(out) + "\n"); return
    print("No solution")
main()
```

## 7. 边界情况与易错点

1. **$n=3,4$**：必须输出 `No solution`。
2. **边长互不相同**：判定用"排序后相邻差 $\ge 10^{-2}$"，避免评测精度 $10^{-3}$ 下被判相同。
3. **坐标范围**：边长 $\le 1000$、$n \le 100$ ⟹ $|坐标| \le 10^5$ ✓。
4. **精度**：方程组用 `double` 解，闭合误差 $10^{-10}$ 量级。
5. **方向基准 $\theta_0$**：取 $0$ 即可（旋转不影响合法性）。

## 8. 验证记录

- **编译环境**：`clang++ -std=c++17 -O2 -Wall`；Python 3.9.6。
- **官方样例**：1 / 1（由 checker 判定；我给出的是另一个合法八边形），C++ 与 Python 一致。
- **checker**：`codeforces/tools/checkers/cf306d.py`（校验逆时针凸、内角极差 $<10^{-3}$、边长两两相差 $>10^{-6}$、边长 $\in[1,1000]$、坐标 $\le10^6$；$n=3,4$ 只接受 `No solution`）。
- **全量对拍**：对 **$n=3\ldots100$ 共 98 组**逐一运行 C++ 与 Python 并交给 checker，**98 / 98 全部通过**（这是我第一次用"全枚举 n"代替随机对拍的题：$n$ 只有 98 个取值）。
- **最大约束性能**：$n=100$，实测端到端 ≈2 ms。
- **图片校验**：两张 SVG 已生成并通过 `ElementTree.parse`。
- **复核状态**：verified。

## 相关题目与扩展

- [Codeforces 306C White, Black and White Again](https://codeforces.com/problemset/problem/306/C)：同场 C 题。
- [LeetCode 1924. 安装栅栏 II](https://leetcode.cn/problems/erect-the-fence-ii/)：几何构造的同类题。

**延伸思考**：

1. **如果要求边长是整数**：需要解整数线性方程组，难度大增。
2. **如果要求"正多边形"**：边长必须全等，与题意冲突。
