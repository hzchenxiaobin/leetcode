#!/usr/bin/env python3
"""按开赛时间从旧到新领取下一批题位。

用法: python3 codeforces/tools/plan_next.py [N]
输出: JSON {"contests":[...], "pairs":[[cid,"A"],...]}；同时写 .cf-meta/tasks/<cid>.json
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, 'codeforces', 'data')
META = os.path.join(ROOT, '.cf-meta')
TASKS = os.path.join(META, 'tasks')
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 8


def main():
    os.makedirs(TASKS, exist_ok=True)
    contests = json.load(open(os.path.join(DATA, 'contests.json')))
    probs = json.load(open(os.path.join(DATA, 'problems.json')))
    by = {}
    for p in probs:
        by.setdefault(p['contestId'], []).append(p)
    pairs, picked = [], []
    for c in contests:  # contests.json 已按开赛时间升序
        todo = [p for p in by.get(c['id'], []) if not p.get('path') and p.get('status') != 'blocked']
        if not todo:
            continue
        todo.sort(key=lambda p: (len(p['index']), p['index']))
        for p in todo:
            pairs.append([c['id'], p['index']])
            picked.append(p)
            if len(pairs) >= LIMIT:
                break
        picked_c = [p['index'] for p in todo][:len(pairs)]
        json.dump({
            'contestId': c['id'],
            'contestName': c['name'],
            'startTime': c['startTime'],
            'durationMin': c['durationMin'],
            'problems': [{'index': p['index'], 'name': p['name'], 'rating': p.get('rating'),
                          'tags': p.get('tags')} for p in by[c['id']]],
        }, open(os.path.join(TASKS, f"{c['id']}.json"), 'w'), ensure_ascii=False, indent=1)
        if len(pairs) >= LIMIT:
            break
    for p in picked:
        p['status'] = 'drafting'
    json.dump(probs, open(os.path.join(DATA, 'problems.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({'contests': sorted({c for c, _ in pairs}), 'pairs': pairs}, ensure_ascii=False))


if __name__ == '__main__':
    main()
