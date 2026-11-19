#!/usr/bin/env python3
"""构建 Codeforces 全量清单（阶段 0）。

输入：.cf-meta/contest_list.json、.cf-meta/problemset.json（API 原始响应）
输出：codeforces/data/{snapshot,contests,problems}.json
"""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
META = os.path.join(ROOT, '.cf-meta')
DATA = os.path.join(ROOT, 'codeforces', 'data')
TZ = datetime.timezone(datetime.timedelta(hours=8))


def sortkey(i: str):
    m = re.match(r'^([A-Z]+)(\d*)$', i)
    if m:
        return (m.group(1), int(m.group(2) or 0))
    m = re.match(r'^(\d+)$', i)
    if m:
        return ('#', int(m.group(1)))
    return (i, 0)


def main():
    os.makedirs(DATA, exist_ok=True)
    contests = json.load(open(os.path.join(META, 'contest_list.json')))['result']
    problems = json.load(open(os.path.join(META, 'problemset.json')))['result']['problems']

    # 增量重建时必须保留已完成的写作状态，否则一次刷新就会把进度清零
    old = {}
    old_path = os.path.join(DATA, 'problems.json')
    if os.path.exists(old_path):
        for p in json.load(open(old_path, encoding='utf-8')):
            old[p['key']] = p

    by_cid = {}
    for p in problems:
        by_cid.setdefault(p['contestId'], []).append(p)

    fin = [c for c in contests if c['phase'] == 'FINISHED' and by_cid.get(c['id'])]
    fin.sort(key=lambda c: (c['startTimeSeconds'], c['id']))
    now = datetime.datetime.now(TZ).strftime('%Y-%m-%dT%H:%M:%S%z')

    out_contests = []
    for c in fin:
        ps = sorted(by_cid[c['id']], key=lambda p: sortkey(p['index']))
        out_contests.append({
            'id': c['id'],
            'name': c['name'],
            'startTime': datetime.datetime.fromtimestamp(c['startTimeSeconds'], TZ).strftime('%Y-%m-%d %H:%M'),
            'startTimeSeconds': c['startTimeSeconds'],
            'durationMin': c['durationSeconds'] // 60,
            'problems': [p['index'] for p in ps],
        })

    slots = sum(len(c['problems']) for c in out_contests)
    # 共享题候选：同名 + 同 rating + 同标签
    groups = {}
    for p in problems:
        if p['contestId'] not in by_cid or not any(c['id'] == p['contestId'] for c in fin):
            continue
        key = (p['name'], p.get('rating'), tuple(sorted(p.get('tags') or [])))
        groups.setdefault(key, []).append(f"{p['contestId']}/{p['index']}")

    out_problems = []
    for p in problems:
        if not any(c['id'] == p['contestId'] for c in fin):
            continue
        key = (p['name'], p.get('rating'), tuple(sorted(p.get('tags') or [])))
        aliases = [x for x in groups[key] if x != f"{p['contestId']}/{p['index']}"]
        k = f"{p['contestId']}/{p['index']}"
        prev = old.get(k) or {}
        out_problems.append({
            'key': k,
            'contestId': p['contestId'],
            'index': p['index'],
            'name': p['name'],
            'rating': p.get('rating'),
            'tags': p.get('tags') or [],
            'shared_candidates': aliases,
            'path': prev.get('path'),
            'status': prev.get('status', 'pending'),
            **({'blocked_reason': prev['blocked_reason']} if prev.get('blocked_reason') else {}),
        })
    out_problems.sort(key=lambda p: (p['contestId'], sortkey(p['index'])))

    fin_list = [c for c in contests if c['phase'] == 'FINISHED']
    no_problem = sorted(c['id'] for c in fin_list if not by_cid.get(c['id']))
    snapshot = {
        'snapshot_at': now,
        'finished_total_from_list': len(fin_list),
        'finished_with_problems': len(fin),
        'finished_without_problems': len(no_problem),
        'finished_without_problems_sample': no_problem[:20],
        'source': 'https://codeforces.com/api/contest.list?gym=false + problemset.problems',
        'contest_total_non_gym': len(contests),
        'finished_total': len(fin),
        'max_finished_contest_id': max(c['id'] for c in fin),
        'problem_slots_finished': slots,
        'unique_problems_finished': len(out_problems),
        'shared_candidate_groups': sum(1 for v in groups.values() if len(v) > 1),
    }
    json.dump(snapshot, open(os.path.join(DATA, 'snapshot.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(out_contests, open(os.path.join(DATA, 'contests.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(out_problems, open(os.path.join(DATA, 'problems.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(snapshot, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
