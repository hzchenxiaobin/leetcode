# 题解配套 checker

部分题解需要特殊评测（构造题、多解题、浮点答案），校验器统一放在本目录，命名 `cf<contestId><index小写>.py`，
**不要放在 /tmp**——临时目录会被清空，导致「验证记录」里的命令无法复现。

约定：`python3 cf<id><idx>.py <input> <output> <answer>`，通过返回 0。

已有通用件：

- `float.py`：浮点答案按容差比较（默认 abs/rel 1e-6，可用 `CF_ABS_TOL`/`CF_REL_TOL` 覆盖），
  可直接用于「实数答案」类题目：`python3 codeforces/tools/verify_solution.py <doc> --checker codeforces/tools/checkers/float.py`。

新写的 checker 请：

1. 放在本目录并提交；
2. 在题解第 8 节写清「校验条件」与可复现命令；
3. 对 `No solution` 类分支要说明如何独立确认（不能只靠样例）。
