#!/usr/bin/env python3
"""扫正文目录，把真实路径与状态写回 data/problems.json，并报告不一致。

用法:
  python3 codeforces/tools/sync_paths.py            # 写回
  python3 codeforces/tools/sync_paths.py --dry-run  # 只报告
  python3 codeforces/tools/sync_paths.py --publish 3/C,4/A   # 复核通过的题位置为 published
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
H1 = re.compile(r'^# Codeforces (\d+)([A-Za-z0-9]+) ', re.M)


def main():
    dry = '--dry-run' in sys.argv
    publish = set()
    if '--publish' in sys.argv:
        publish = {x for x in sys.argv[sys.argv.index('--publish') + 1].split(',') if x}
    probs = json.load(open(os.path.join(CF, 'data', 'problems.json'), encoding='utf-8'))
    by = {p['key']: p for p in probs}
    seen, problems = {}, []
    for doc in sorted(glob.glob(os.path.join(CF, 'contests', '*', '*', '*.md'))):
        rel = os.path.relpath(doc, CF)
        src = open(doc, encoding='utf-8').read()
        m = H1.search(src)
        if not m:
            problems.append(f'H1 无法解析: {rel}')
            continue
        cid, idx = int(m.group(1)), m.group(2)
        # 路径中的场次必须与 H1 一致
        if f'/{cid}/' not in '/' + rel.replace(os.sep, '/'):
            problems.append(f'H1 场次与路径不一致: {rel}')
        key = f'{cid}/{idx}'
        if key in seen:
            problems.append(f'重复正文: {key} -> {seen[key]} 与 {rel}')
            continue
        if key not in by:
            problems.append(f'清单中不存在: {key} ({rel})')
            continue
        seen[key] = rel
        by[key]['path'] = rel
        if by[key].get('status') not in ('blocked', 'published'):
            by[key]['status'] = 'published' if key in publish else 'verified'
    for key, p in by.items():
        if p.get('path') and key not in seen:
            problems.append(f'清单有路径但文件缺失: {key} -> {p["path"]}')
            p['path'] = None
            if p.get('status') == 'verified':
                p['status'] = 'pending'
    print(f'清单 {len(probs)} 题位，正文 {len(seen)} 篇，路径已同步')
    for x in problems:
        print('  !', x)
    if not dry:
        json.dump(probs, open(os.path.join(CF, 'data', 'problems.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('已写入 data/problems.json')


if __name__ == '__main__':
    main()
