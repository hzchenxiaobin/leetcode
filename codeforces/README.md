# Codeforces 题解专区

本目录按 [全量比赛中文题解编写计划](../codeforces-solutions-plan.md) 组织：覆盖 Codeforces 非 Gym 的全部已结束比赛，逐题给出题意、思路、证明、复杂度、可提交代码与验证记录。

## 目录结构

```text
codeforces/
├── contests/<区间>/<contestId>/<题号>_<题名>.md   # 题解正文
├── images/                                        # 手绘 SVG 插图
├── data/
│   ├── snapshot.json     # API 快照与总量
│   ├── contests.json     # 比赛清单（按开赛时间升序）
│   ├── problems.json     # 题位清单、路径与状态
│   └── progress.md       # 覆盖率与阻塞项
├── tools/                # 清单、迁移、校验、进度脚本
├── README.md
└── SKILL.md              # 写作规范
```

## 使用

- 站内列表：`/codeforces.html`，按场次与题号检索。
- 题解源文件：`codeforces/contests/…`；图片：`codeforces/images/…`。
- 写作与验收规范见 [SKILL.md](SKILL.md)。

## 统计口径

- **比赛覆盖率** = 所有题位都已有正文的比赛数 / 有题面映射的已结束比赛数。
- **题位覆盖率** = 已有正文的原始题位数 / 快照题位总数。
- **唯一题解覆盖率** = 已发布唯一题目数 / 去重题目总数（共享题以别名入口指向唯一正文）。

当前进度与阻塞项见 [data/progress.md](data/progress.md)，原始数据见 [data/snapshot.json](data/snapshot.json)。

## 工作流

1. `python3 codeforces/tools/build_manifest.py`：重建快照与清单。
2. `python3 codeforces/tools/plan_next.py 8`：按开赛时间从旧到新领取下一批题位。
3. 按 `SKILL.md` 写作、验证，图片放 `codeforces/images/`。
4. 更新 `data/problems.json` 状态，运行 `python3 codeforces/tools/update_progress.py`。
5. 每批结束执行站点分批构建与覆盖率对账。
