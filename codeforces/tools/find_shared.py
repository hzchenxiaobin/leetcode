#!/usr/bin/env python3
"""核对清单里的「共享题候选组」，确认哪些是同一道题（Div.1 / Div.2 共用原题）。

清单只能按标题 + rating + 标签产生候选（build_manifest.py），不能据此合并：
本脚本抓取各题位题面，比较「样例集合 + 英文题名 + 输入输出格式」，全部一致才判为重复，
结果写入 .cf-meta/aliases.json：{canonical: "1/A", aliases: ["48/D", ...], evidence: {...}}

用法: python3 codeforces/tools/find_shared.py [--write]
"""
import hashlib, json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
META = os.path.join(ROOT, '.cf-meta')
sys.path.insert(0, os.path.join(CF, 'tools'))
from fetch_problem import fetch  # noqa: E402


def sig(d):
    """题面指纹：样例（去空白）+ 英文名 + 输入输出格式，任一不同即不同题。"""
    if not d.get('ok'):
        return None
    samples = [(re.sub(r'\s+', ' ', s['in']).strip(), re.sub(r'\s+', ' ', s['out']).strip())
               for s in d.get('samples') or []]
    raw = json.dumps({
        'name': (d.get('name') or '').strip().lower(),
        # 必须带完整题面：A1/A2、E1/E2 这类分难度版本只有约束不同，
        # 只比样例会把它们误判成同一道题
        'desc': re.sub(r'\s+', ' ', (d.get('description') or {}).get('en', '')).strip(),
        'in': re.sub(r'\s+', ' ', (d.get('inputFormat') or {}).get('en', '')).strip(),
        'out': re.sub(r'\s+', ' ', (d.get('outputFormat') or {}).get('en', '')).strip(),
        'samples': samples,
    }, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def main():
    write = '--write' in sys.argv
    probs = json.load(open(os.path.join(CF, 'data', 'problems.json'), encoding='utf-8'))
    by = {p['key']: p for p in probs}
    groups = {}
    for p in probs:
        if p.get('shared_candidates'):
            groups[tuple(sorted([p['key']] + p['shared_candidates']))] = True

    confirmed, rejected, missing = [], [], []
    for g in groups:
        sigs = {}
        for k in g:
            cid, idx = k.split('/')
            try:
                d = fetch(int(cid), idx)
            except Exception as e:
                missing.append((k, f'抓取失败 {e}'))
                continue
            time.sleep(0.8)
            s = sig(d)
            if s is None:
                missing.append((k, '镜像无题面'))
            else:
                sigs[k] = s
        if len(sigs) < 2:
            continue
        if len(set(sigs.values())) == 1:
            canonical = sorted(sigs)[0]
            confirmed.append({'canonical': canonical, 'aliases': [k for k in sorted(sigs) if k != canonical],
                              'members': sorted(sigs)})
        else:
            rejected.append(sorted(sigs))

    print(f'候选 {len(groups)} 组 → 确认同一题 {len(confirmed)} 组，不同题 {len(rejected)} 组，缺题面 {len(missing)} 个题位')
    for c in confirmed:
        print(f"  ✔ {' = '.join(c['members'])}（正文放 {c['canonical']}）")
    for r in rejected:
        print(f"  ✘ {' ≠ '.join(r)}")
    for k, why in missing:
        print(f'  ? {k}: {why}')
    if write:
        json.dump({'confirmed': confirmed, 'rejected': rejected,
                   'missing': [{'key': k, 'why': w} for k, w in missing]},
                  open(os.path.join(META, 'aliases.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('已写入 .cf-meta/aliases.json')


if __name__ == '__main__':
    main()
