# Codeforces 题解写作规范

本文件是 Codeforces 题解的唯一写作规范。所有新题解必须遵守；历史题解在审计阶段逐步对齐。

## 1. 目录与命名

```text
codeforces/
├── README.md
├── SKILL.md
├── data/                 # snapshot / contests / problems / progress
├── tools/                # 清单、迁移、校验脚本
├── images/               # 全部插图，命名 cf<contestId><problemIndex>_<用途>.svg（小写）
└── contests/
    └── 2201-2300/
        └── 2285/
            ├── A_合数排列.md
            └── B_数字串.md
```

- 区间目录按 contestId 每 100 个一场：`0001-0100`、`0101-0200`、…、`2201-2300`。
- 文件名 `<题号>_<中文题名>.md`，题号保留 `A1`、`G2`、`E1` 等原始形式。
- 插图放 `codeforces/images/`，正文用相对路径 `../../../images/<文件名>`（从场次目录向上三级）。
- 一幅图只服务一篇题解；跨题复用请复制成新名字。

## 2. 文章模板

```markdown
# Codeforces <contestId><problemIndex> <题名> 题解

## 1. 题目概述

- **题目链接**：https://codeforces.com/problemset/problem/<cid>/<index>
- **比赛来源**：<比赛全名> · Problem <index>
- **难度**：<rating 或 未评级（points 分）>
- **标签**：<中文标签>
- **评测类型**：普通 / 特殊评测 / 交互 / 多解 / 多子任务
- **限制**：时间 <x> s / 内存 <y> MB

**题意**：用自己的话概括输入、操作与目标。

**约束**：列出影响算法选择的约束，并指出它排除了哪些复杂度。

## 2. 示例与观察

官方样例（输入/输出原样），必要时补自造样例并标注；随后逐步演算关键样例，提炼核心观察。

## 3. 解题思路

### 3.1 朴素做法与瓶颈
### 3.2 核心观察（配图）
### 3.3 算法流程 / 状态转移（配图）
### 3.4 样例走查（配图）

## 4. 正确性证明

引理 1 … 证明 … ∎
引理 2 …
定理 … 证明 … ∎

## 5. 复杂度分析

时间、空间分点，说明常数与时限/内存的关系。

## 6. 参考代码

### C++17
### Python3

## 7. 边界情况与易错点

至少 4 条，覆盖溢出、空结构、极值、多测清空、下标、递归深度、精度等。

## 8. 验证记录

- 编译环境与命令：
- 官方样例：k / k 通过
- 额外测试（对拍/全枚举/构造 checker/交互模拟器）与规模：
- 最大约束性能（耗时/内存）：
- 复核状态：

## 相关题目与扩展

相关题链接 + **延伸思考**
```

章节之间不要 `---` 分隔线。公式用 `$...$` / `$$...$$`，星号写 `*`（禁止 `\*`），`\text{}` 内不写裸 `#`，证明结尾用 `∎`（不要 `\qed`）。

## 3. 插图

- 手绘 sketch 风：`feTurbulence` + `feDisplacementMap`（`id="rough2"`）、`Comic Sans MS` / `Kaiti SC`、背景 `#fafafa`、3–4 种柔和色。
- 每个图形与文字元素加 `filter="url(#rough2)"`；文字不得越出 `viewBox` 或方框。
- 优先画核心观察、流程/状态转移、样例走查；简单模拟题不为了数量重复画图。
- 禁止 ASCII 字符画与截图。

## 4. 代码

- 必须完整可提交：`#include <bits/stdc++.h>`、`int main()`、按题意处理多测。
- 先写对拍通过的参考实现，再从实现反推正文步骤；正文代码必须与验证过的版本逐字一致。
- Python 为补充版本：若满数据会超时，在正文注明“建议 PyPy3 / 提交 C++”。
- 交互题必须附本地交互模拟器；构造题必须附合法性 checker；特殊评测题必须验证输出约束。

## 5. 验证与状态

状态流转：`pending → drafting → sample_passed → verified → review_passed → published`；`blocked` 不属于完成。

普通题最低要求：
1. GNU C++17 `-O2` 编译通过；
2. 全部官方样例通过；
3. 与独立暴力随机/全枚举对拍（小数据 ≥200 组或穷举）；
4. 最大约束性能测试，C++ 至少 2 倍时限余量；
5. 图片 `ElementTree.parse` 通过；
6. 公式经 KaTeX 校验（`throwOnError`）无错。

完成后在 `data/problems.json` 把对应条目 `status` 置为 `verified`（复核后 `published`）并写入 `path`，最后运行 `tools/update_progress.py`。
