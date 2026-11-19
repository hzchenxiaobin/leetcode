#!/usr/bin/env python3
"""根据 data/{snapshot,contests,problems}.json 重新生成 data/progress.md。"""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')


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
    lines = []
    lines.append('# Codeforces 题解进度\n')
    lines.append(f"- 快照时间：{snap['snapshot_at']}")
    lines.append(f"- 已结束比赛（contest.list）：{snap['finished_total_from_list']}，其中有题面映射：{snap['finished_with_problems']}，无映射（如 ICPC/IOI 镜像）：{snap['finished_without_problems']}")
    lines.append(f"- 原始题位：{snap['problem_slots_finished']}；唯一题目：{snap['unique_problems_finished']}")
    lines.append('')
    def pct(a, b):
        return f'{a / b * 100:.2f}%' if b else '0%'
    lines.append('## 覆盖率\n')
    lines.append('| 指标 | 数值 |')
    lines.append('| --- | --- |')
    lines.append(f"| 比赛覆盖率 | {len(full)} / {len(contests)}（{pct(len(full), len(contests))}） |")
    lines.append(f"| 题位覆盖率 | {len(done)} / {len(probs)}（{pct(len(done), len(probs))}） |")
    lines.append(f"| 已发布正文 | {len(done)} |")
    lines.append(f"| blocked | {len(blocked)} |")
    lines.append('')
    lines.append('## 最近完成的场次\n')
    recent = sorted(full, key=lambda c: -c['id'])[:10]
    for c in recent:
        lines.append(f"- {c['id']} {c['name']}")
    lines.append('')
    lines.append('## 阻塞项\n')
    if blocked:
        for p in blocked:
            lines.append(f"- `{p['key']}` {p['name']}：{p.get('blocked_reason', '待记录')}")
    else:
        lines.append('- 无')
    lines.append('')
    lines.append('## 下一批\n')
    nxt = [p for p in probs if not p.get('path') and p.get('status') != 'blocked'][:12]
    for p in nxt:
        lines.append(f"- `{p['key']}` {p['name']}（{p.get('rating') or '未评级'}）")
    open(os.path.join(DATA, 'progress.md'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:12]))


if __name__ == '__main__':
    main()
