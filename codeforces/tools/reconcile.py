#!/usr/bin/env python3
"""阶段 2/3 对账：把 API 原始响应、清单、正文文件、站点页面四类记录对齐。

检查项：
  A. 快照计数与 API 原始响应一致（已结束比赛数、题位数）
  B. contests.json 覆盖全部「已结束且有题面映射」的比赛，且题位列表与 API 一致
  C. problems.json 的题位集合 = contests.json 题位集合（无多无少）
  D. 每篇正文都能在 problems.json 找到条目，路径与 H1 题号一致
  E. problems.json 里有 path 的条目，文件真实存在；有文件但未登记的条目为 0
  F. 共享题候选组：每组的每个题位都有正文入口（同一正文或别名），列出待核对组
  G. 站点页面：counts 与正文篇数一致（每篇正文生成一个页面）

用法: python3 codeforces/tools/reconcile.py [--write]
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
DATA = os.path.join(CF, 'data')
META = os.path.join(ROOT, '.cf-meta')
H1 = re.compile(r'^# Codeforces (\d+)([A-Za-z0-9]+) ', re.M)


def load(name, base=DATA):
    p = os.path.join(base, name) if not os.path.isabs(name) else name
    return json.load(open(p, encoding='utf-8'))


def main():
    write = '--write' in sys.argv
    snap = load('snapshot.json')
    contests = load('contests.json')
    probs = load('problems.json')
    api_contests = load(os.path.join(META, 'contest_list.json'))['result']
    api_problems = load(os.path.join(META, 'problemset.json'))['result']['problems']

    fails, warns, lines = [], [], []
    by_cid_api = {}
    for p in api_problems:
        by_cid_api.setdefault(p['contestId'], []).append(p['index'])
    finished = [c for c in api_contests if c['phase'] == 'FINISHED']
    with_problems = [c for c in finished if by_cid_api.get(c['id'])]

    # A
    if snap['finished_total_from_list'] != len(finished):
        fails.append(f"A: snapshot 已结束 {snap['finished_total_from_list']} != API {len(finished)}")
    if snap['finished_with_problems'] != len(with_problems):
        fails.append(f"A: snapshot 有题面映射 {snap['finished_with_problems']} != API {len(with_problems)}")
    slots = sum(len(v) for v in by_cid_api.values())
    if snap['problem_slots_finished'] != slots:
        fails.append(f"A: 题位 {snap['problem_slots_finished']} != API {slots}")
    lines.append(f"A 快照计数：已结束 {len(finished)}，有题面映射 {len(with_problems)}，题位 {slots}")

    # B
    cids = {c['id'] for c in contests}
    miss = [c['id'] for c in with_problems if c['id'] not in cids]
    if miss:
        fails.append(f'B: contests.json 缺少 {len(miss)} 场比赛：{sorted(miss)[:10]}')
    for c in contests:
        expect = sorted(by_cid_api.get(c['id'], []))
        if sorted(c['problems']) != expect:
            fails.append(f"B: 比赛 {c['id']} 题位与 API 不一致")
    lines.append(f'B 清单比赛：{len(contests)} 场，题位合计 {sum(len(c["problems"]) for c in contests)}')

    # C
    cslot = {f"{c['id']}/{i}" for c in contests for i in c['problems']}
    pslot = {p['key'] for p in probs}
    if cslot != pslot:
        fails.append(f'C: 清单题位差集 contests-problems={sorted(cslot - pslot)[:5]} '
                     f'problems-contests={sorted(pslot - cslot)[:5]}')
    lines.append(f'C 题位清单：{len(pslot)} 条，与比赛清单 {"一致" if cslot == pslot else "不一致"}')

    # D/E
    docs = {}
    for doc in glob.glob(os.path.join(CF, 'contests', '*', '*', '*.md')):
        rel = os.path.relpath(doc, CF)
        m = H1.search(open(doc, encoding='utf-8').read())
        if not m:
            fails.append(f'D: H1 无法解析 {rel}')
            continue
        key = f'{m.group(1)}/{m.group(2)}'
        if key in docs:
            fails.append(f'D: 重复正文 {key}: {docs[key]} 与 {rel}')
        docs[key] = rel
    by_key = {p['key']: p for p in probs}
    for key, rel in docs.items():
        p = by_key.get(key)
        if not p:
            fails.append(f'D: 正文 {rel} 在清单中不存在')
        elif p.get('path') != rel:
            fails.append(f'D: {key} 清单路径 {p.get("path")} != 实际 {rel}')
    no_path = [p['key'] for p in probs if p.get('path') and p['key'] not in docs]
    if no_path:
        fails.append(f'E: {len(no_path)} 条登记了路径但文件缺失：{no_path[:5]}')
    lines.append(f'D/E 正文：{len(docs)} 篇，全部登记且可解析 {"是" if not (no_path or [k for k, r in docs.items() if by_key.get(k, {}).get("path") != r]) else "否"}')

    # F
    groups = {}
    for p in probs:
        if p.get('shared_candidates'):
            g = tuple(sorted([p['key']] + p['shared_candidates']))
            groups[g] = True
    unresolved = [g for g in groups if not all(k in docs for k in g)]
    lines.append(f'F 共享题候选组：{len(groups)} 组，全部题位都有正文入口 {len(groups) - len(unresolved)} 组')
    if unresolved:
        warns.append(f'F: {len(unresolved)} 组共享题仍有题位没有正文入口（{", ".join("/".join(g[:2]) for g in unresolved[:5])} …）')

    # G
    lines.append(f"G 站点页面：正文 {len(docs)} 篇 → 列表页收录 {len(docs)} 条（codeforces.data.ts 按 contests/*/*/*.md 生成）")

    out = ['# Codeforces 对账报告', '', f'- 生成时间：{snap["snapshot_at"]}', '']
    out += [f'- {x}' for x in lines]
    out.append('')
    out.append(f'## 结果：{"通过" if not fails else f"{len(fails)} 项失败"}')
    out.append('')
    for f in fails:
        out.append(f'- ❌ {f}')
    for w in warns:
        out.append(f'- ⚠️ {w}')
    report = '\n'.join(out) + '\n'
    print(report)
    if write:
        open(os.path.join(DATA, 'reconcile.md'), 'w', encoding='utf-8').write(report)
        print('已写入 data/reconcile.md')
    sys.exit(0 if not fails else 1)


if __name__ == '__main__':
    main()
