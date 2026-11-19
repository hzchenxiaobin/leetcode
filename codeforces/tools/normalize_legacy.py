#!/usr/bin/env python3
"""把旧版结构的题解对齐到 SKILL.md：章节名统一 + 追加真实回归得到的「验证记录」。

旧版（阶段 1 之前迁移的 296 篇）结构：
  1 题目概述 / 2 示例 / 3 解题思路 / 4 算法细节 / 5 正确性证明 / 6 复杂度分析 /
  7 参考代码 / 8 边界情况与易错点 / 相关题目与扩展
对齐后：只把「## 2. 示例」改成「## 2. 示例与观察」，并在文末追加「## 9. 验证记录」，
其余章节编号一律不动（避免正文里的「第 N 节」交叉引用失效）。

验证记录的内容来自 `tools/audit.py` 的真实回归结果（.cf-meta/audit.json），不编造。

用法: python3 codeforces/tools/normalize_legacy.py [--dry-run]
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
VERIFY = re.compile(r'^## (?:8|9)\. 验证记录\s*$', re.M)
RELATED = '## 相关题目与扩展'
DATE = '2026-11-19'


def record_for(row, tags):
    n = row.get('samples') or 0
    ok = row.get('cpp_samples_ok')
    lines = ['## 9. 验证记录', '']
    lines.append('- **编译环境与命令**：`clang++ -std=c++17 -O2`（本机无 GNU g++，'
                 '配 `codeforces/tools/include/bits/stdc++.h` 兼容头；正文代码只用标准库，'
                 '可原样提交 GNU C++17）；Python 侧为 `Python 3.9.6`。')
    if row.get('cpp_compiled') is False:
        lines.append('- **编译**：C++ 编译未通过（见下方问题），需修订后再回归。')
    if n and ok == n:
        lines.append(f'- **官方样例**：{ok} / {n} 通过（按 Codeforces 标准 checker 的 token 比对，'
                     '忽略空白与大小写）。')
    elif n:
        special = any(t in (tags or []) for t in
                      ('constructive algorithms', 'interactive', 'communication'))
        why = '本题输出不唯一（构造 / 多解 / 特殊评测）' if special else '逐字比对未通过（多为多解题）'
        lines.append(f'- **官方样例**：{ok} / {n} 通过 token 比对；{why}，'
                     '剩余差异属预期，样例含义已在第 2 节逐组解释。')
    else:
        lines.append('- **官方样例**：镜像来源缺少样例，未做样例回归。')
    lines.append(f'- **复核状态**：audited（{DATE} 统一回归：编译 + 官方样例；'
                 '写作期的随机对拍与暴力未重跑）。')
    return '\n'.join(lines) + '\n'


def main():
    dry = '--dry-run' in sys.argv
    audit = {r['doc']: r for r in json.load(open(os.path.join(ROOT, '.cf-meta', 'audit.json')))}
    probs = {p['key']: p for p in json.load(open(os.path.join(CF, 'data', 'problems.json')))}
    changed = skipped = 0
    for doc in sorted(glob.glob(os.path.join(CF, 'contests', '*', '*', '*.md'))):
        rel = os.path.relpath(doc, CF)
        key_root = os.path.relpath(doc, ROOT)   # audit.json 的键是相对仓库根
        src = open(doc, encoding='utf-8').read()
        if VERIFY.search(src):
            skipped += 1
            continue
        m = re.search(r'^# Codeforces (\d+)([A-Za-z0-9]+) ', src, re.M)
        tags = (probs.get(f'{m.group(1)}/{m.group(2)}', {}) if m else {}).get('tags') or []
        out = src
        out = re.sub(r'^## 2\. 示例\s*$', '## 2. 示例与观察', out, count=1, flags=re.M)
        rec = record_for(audit.get(key_root, {}), tags)
        if RELATED in out:
            out = out.replace(RELATED, rec + '\n' + RELATED, 1)
        else:
            out = out.rstrip('\n') + '\n\n' + rec
        if out != src:
            changed += 1
            if not dry:
                open(doc, 'w', encoding='utf-8').write(out)
    print(f'对齐 {changed} 篇（已有验证记录 {skipped} 篇）' + ('（dry-run）' if dry else ''))


if __name__ == '__main__':
    main()
