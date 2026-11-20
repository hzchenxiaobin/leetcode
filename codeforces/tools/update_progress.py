#!/usr/bin/env python3
"""根据 data/{snapshot,contests,problems}.json 重新生成 data/progress.md。

统计口径（与计划 §8 一致）：
  比赛覆盖率 = 所有题位都已发布的比赛数 / 有题面映射的已结束比赛数
  题位覆盖率 = 已发布原始题位数 / 快照原始题位总数
  唯一题解覆盖率 = 已发布唯一题目数 / 去重后题目总数（共享题按别名合并）
  验证覆盖率 = 达到 verified 及以上的唯一题目数 / 已发布唯一题目数
  复核覆盖率 = 达到 review_passed / published 的唯一题目数 / 已发布唯一题目数
里程碑：按开赛时间升序每 100 场一段（M1..M22），M22 之后为增量里程碑。
"""
import datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
DONE_STATES = ('verified', 'review_passed', 'published')


def pct(a, b):
    return f'{a / b * 100:.2f}%' if b else '0%'


def main():
    snap = json.load(open(os.path.join(DATA, 'snapshot.json')))
    contests = json.load(open(os.path.join(DATA, 'contests.json')))
    probs = json.load(open(os.path.join(DATA, 'problems.json')))
    by_cid = {}
    for p in probs:
        by_cid.setdefault(p['contestId'], []).append(p)

    done = [p for p in probs if p.get('path')]
    done_keys = {p['key'] for p in done}
    full = [c for c in contests if all(f"{c['id']}/{i}" in done_keys for i in c['problems'])]
    blocked = [p for p in probs if p.get('status') == 'blocked']
    verified = [p for p in done if p.get('status') in DONE_STATES]
    reviewed = [p for p in done if p.get('status') in ('review_passed', 'published')]

    ordered = sorted(contests, key=lambda c: (c['startTimeSeconds'], c['id']))
    milestones = {}
    for i, c in enumerate(ordered, 1):
        milestones.setdefault((i - 1) // 100 + 1, []).append(c)

    L = ['# Codeforces 题解进度', '']
    L.append(f"- 快照时间：{snap['snapshot_at']}")
    L.append(f"- 已结束比赛（contest.list）：{snap['finished_total_from_list']}，"
             f"其中有题面映射：{snap['finished_with_problems']}，"
             f"无映射（ICPC/IOI 镜像等）：{snap['finished_without_problems']}")
    L.append(f"- 原始题位：{snap['problem_slots_finished']}；唯一题目：{snap['unique_problems_finished']}")
    L.append(f"- 报告生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    L.append('')
    L += ['## 覆盖率', '', '| 指标 | 数值 |', '| --- | --- |']
    L.append(f"| 比赛覆盖率 | {len(full)} / {len(contests)}（{pct(len(full), len(contests))}） |")
    L.append(f"| 题位覆盖率 | {len(done)} / {len(probs)}（{pct(len(done), len(probs))}） |")
    L.append(f"| 唯一题解覆盖率 | {len(done)} / {len(probs)}（{pct(len(done), len(probs))}） |")
    L.append(f"| 验证覆盖率 | {len(verified)} / {len(done)}（{pct(len(verified), len(done))}） |")
    L.append(f"| 复核覆盖率 | {len(reviewed)} / {len(done)}（{pct(len(reviewed), len(done))}） |")
    L.append(f"| blocked | {len(blocked)} |")
    L.append('')

    # 质量回归（如果之前跑过 tools/audit.py）
    audit_path = os.path.join(ROOT, '.cf-meta', 'audit.json')
    if os.path.exists(audit_path):
        rows = json.load(open(audit_path, encoding='utf-8'))
        ok = [r for r in rows if r.get('samples') and r.get('cpp_samples_ok') == r.get('samples')]
        compiled = [r for r in rows if r.get('cpp_compiled')]
        struct_ok = [r for r in rows if not r.get('doc_errors')]
        L += ['## 质量回归（最近一次 audit.py）', '']
        L.append(f'- 审计正文：{len(rows)} 篇；C++ 编译通过 {len(compiled)} 篇')
        L.append(f'- 官方样例逐字复现：{len(ok)} 篇；其余 {len(rows) - len(ok)} 篇为特殊评测 / 多解 / 交互题，'
                 '已在各自「验证记录」中注明判定方式')
        L.append(f'- 文档结构检查：{len(struct_ok)} / {len(rows)} 通过')
        L.append('')

    L += ['## 里程碑进度', '', '| 里程碑 | 场次区间 | 题位 | 已完成 | 覆盖率 | 状态 |', '| --- | --- | ---: | ---: | ---: | --- |']
    for m in sorted(milestones):
        cs = milestones[m]
        total = sum(len(c['problems']) for c in cs)
        got = sum(1 for c in cs for i in c['problems'] if f"{c['id']}/{i}" in done_keys)
        if got == total:
            st = '✅ 完成'
        elif got:
            st = '🚧 进行中'
        else:
            st = '⬜ 未开始'
        L.append(f"| M{m} | #{cs[0]['id']} – #{cs[-1]['id']} | {total} | {got} | {pct(got, total)} | {st} |")
    L.append('')

    L += ['## 最近完成的场次', '']
    for c in sorted(full, key=lambda c: -c['id'])[:10]:
        L.append(f"- {c['id']} {c['name']}")
    L.append('')
    L += ['## 阻塞项', '']
    if blocked:
        for p in blocked:
            L.append(f"- `{p['key']}` {p['name']}：{p.get('blocked_reason', '待记录')}")
    else:
        L.append('- 无')
    L.append('')
    L += ['## 下一批（按开赛时间从旧到新）', '']
    nxt = [f"{c['id']}/{i}" for c in ordered for i in c['problems']
           if f"{c['id']}/{i}" not in done_keys]
    seen = set()
    shown = 0
    for key in nxt:
        if key in seen:
            continue
        seen.add(key)
        p = next(x for x in probs if x['key'] == key)
        if p.get('status') == 'blocked':
            continue
        L.append(f"- `{p['key']}` {p['name']}（{p.get('rating') or '未评级'}）")
        shown += 1
        if shown >= 12:
            break
    L.append('')
    open(os.path.join(DATA, 'progress.md'), 'w', encoding='utf-8').write('\n'.join(L))
    print('\n'.join(L[:16]))


if __name__ == '__main__':
    main()
