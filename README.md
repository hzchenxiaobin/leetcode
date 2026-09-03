# LeetCode 题解

面试高频题与周赛题的中文题解集合，配套手绘 sketch 风 SVG 插图，通过 `build.py` 生成静态网站并部署到 GitHub Pages。

## 在线预览

推送 `main` 分支后由 GitHub Actions 自动构建并部署，站点结构：

- 首页：题解列表（每日一题按题号区间分组 + 周赛按场次降序），含「随机选一道题练习」按钮
- 高频面试题页：`hot-interview.md` 汇总 Hot 100 / CodeTop / 剑指 Offer 高频题，逐题链接站内题解（侧边栏「🔥 高频面试题」入口）
- 算法专题页：`topics/` 下按算法类别组织的专题文档，含核心思想、模板、剪枝/去重技巧、例题精讲与课后练习（侧边栏「📚 专题」目录自动收录 `topics/` 下全部文档）
- 题解页：每篇 Markdown 渲染为独立页面，含侧边栏导航、KaTeX 数学公式、Prism 代码高亮、手绘 SVG 插图

## 仓库结构

```
.
├── build.py                 # 静态网站生成器（扫描 .md → public/）
├── hot-interview.md         # 高频算法面试题汇总页（Hot 100 / CodeTop / 剑指 Offer，链接站内题解）
├── 10-week-plan.md          # 10 周刷题计划（按类别组织 198 道高频题，链接站内题解）
├── cannbot_hello.sh         # 调用 cannbot 按 SKILL.md 自动产出题解的脚本
├── solution/                # 每日一题 / 面试高频题题解
│   ├── 0001-0100/           # 按题号每 100 题一个区间目录
│   ├── 0101-0200/
│   ├── ...
│   ├── 1101-1200/
│   ├── images/              # ⭐ 每日题解 SVG 插图统一存放于此（全库共享）
│   └── SKILL.md             # 每日题解写作规范（选题逻辑、目录、文档结构、SVG 风格）
├── contest/                 # 周赛题解
│   ├── 187/                 # 以周赛编号命名，每场 4 题（Q1-Q4）
│   ├── 503/
│   ├── ...
│   ├── 512/
│   └── SKILL.md             # 周赛题解写作规范（含正确性证明、边界情况）
├── topics/                   # 算法专题文档（侧边栏「📚 专题」自动收录）
├── images/                  # 周赛 SVG/PNG 插图（与每日题解共享）
├── static/                  # 网站静态资源
│   ├── css/                 # style.css + Prism 主题
│   └── js/                  # marked.js、Prism（C/C++/Python/Bash）、KaTeX 适配、main.js
├── .github/workflows/
│   └── deploy.yml           # GitHub Pages 部署工作流
└── public/                  # 构建输出（gitignore，由 build.py 生成）
```

## 本地构建

依赖 Python 3.11，无需额外安装第三方库（仅用标准库）：

```bash
python3 build.py
```

构建产物输出到 `public/`：

- `public/index.html` — 首页（每日一题 + 周赛题目列表）
- `public/problems/<slug>.html` — 每篇题解一个页面
- `public/images/` — 合并 `images/` 与 `solution/images/` 的全部插图
- `public/css/`、`public/js/` — 从 `static/` 复制

本地预览可用任意静态服务器，例如：

```bash
python3 -m http.server 8000 --directory public
```

## 部署

`.github/workflows/deploy.yml` 在 `main` 分支推送 `build.py`、`static/**`、`contest/**`、`images/**` 等路径时触发，执行 `python3 build.py` 后将 `public/` 上传到 GitHub Pages。也支持 `workflow_dispatch` 手动触发。

## 题解写作规范

两类题解各有独立的 `SKILL.md` 约定目录组织、文档结构与插图风格：

| | 每日一题 (`solution/SKILL.md`) | 周赛 (`contest/SKILL.md`) |
|---|---|---|
| **选题** | 面试高频优先（Hot 100 / 面试经典 150），套路代表性强 | 每场 4 题全写，赛后完整复盘 |
| **目录** | `solution/<题号区间>/<题号>_<题名>.md` | `contest/<场次>/Q<n>.<题名>题解.md` |
| **特有章节** | 面试要点 Q&A、同类练习题 | 算法细节、正确性证明、边界情况与易错点 |
| **图片目录** | `solution/images/`，引用 `../images/xxx.svg` | `images/`（顶层），引用 `images/xxx.svg` |

两类题解的文档格式对齐 [leetgpu 题解](https://hzchenxiaobin.github.io/leetgpu/) 样式：一级标题 `# LeetCode <题名> 题解`，元信息（标题 / 题号、链接、难度、标签）放在 `## 1. 题目概述` 内部随正文渲染（同时提取为页头徽章），题意以 `**题意**：` 标签开头，章节间不用 `---` 分隔线，末节「同类练习题 / 相关题目与扩展」不编号（daily 为表格格式）。

### 插图风格

所有示意图、流程图、演算表统一为**手绘 sketch 风**（Excalidraw-like）：

- 用 SVG 滤镜 `feTurbulence` + `feDisplacementMap` 给图形叠加轻微抖动
- 字体 `Comic Sans MS` / `Kaiti SC`（楷体），配色极简 3-4 种柔和色
- **禁止 ASCII 字符画**，一律用 SVG

SVG 模板与命名规则详见各 `SKILL.md`。

## 自动化

`cannbot_hello.sh` 调用 cannbot 按 `solution/SKILL.md` 的规范自动产出一道题解，循环执行 20 次后统一 `git commit` 并推送：

```bash
./cannbot_hello.sh
```

可通过参数自定义发送给 cannbot 的消息：

```bash
./cannbot_hello.sh "使用 SKILL.md 完成 42_接雨水 题解"
```
