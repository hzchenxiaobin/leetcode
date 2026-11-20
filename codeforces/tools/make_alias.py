#!/usr/bin/env python3
"""为「同一道题出现在两个题位」的情况生成别名页（正文只写一篇，另一题位放短链接页）。

判定依据：题面英文 description + 输入输出格式 + 全部样例 + 英文标题完全一致
（见 tools/find_shared.py 的指纹；只用标题/评分/标签会误合并难度版本 A1/A2、E1/E2）。

用法：
  python3 codeforces/tools/make_alias.py <canonical 题位> <alias 题位> [--name 中文题名]
  例：python3 codeforces/tools/make_alias.py 178/B1 178/B2

生成文件：codeforces/contests/<区间>/<alias 场次>/<题号>_<题名>.md
别名页带 `<!-- alias-page -->` 标记，check.py 与 check_samples.py 会按别名页规则处理。
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
CACHE = os.path.join(ROOT, '.cf-meta', 'statements')


def range_dir(cid):
    lo = (int(cid) - 1) // 100 * 100 + 1
    return f'{lo:04d}-{lo + 99:04d}'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 2:
        print(__doc__)
        return
    canon, alias = args[0], args[1]
    name = None
    if '--name' in sys.argv:
        name = sys.argv[sys.argv.index('--name') + 1]

    probs = {p['key']: p for p in json.load(open(os.path.join(CF, 'data', 'problems.json'), encoding='utf-8'))}
    cp, ap = probs[canon], probs[alias]
    st = json.load(open(os.path.join(CACHE, f"CF{ap['contestId']}{ap['index']}.json"), encoding='utf-8'))
    zh = name or f"{ap['name']} 别名页"

    # 正文里已有的中文题名（从 H1 取），保证两页标题同源
    canon_doc = os.path.join(CF, cp['path']) if cp.get('path') else None
    canon_title = None
    if canon_doc and os.path.exists(canon_doc):
        h1 = re.search(r'^# Codeforces \d+[A-Za-z0-9]+ (.+?) 题解', open(canon_doc, encoding='utf-8').read(), re.M)
        canon_title = h1.group(1).strip() if h1 else None
    title = canon_title or zh

    rel_canon = os.path.relpath(canon_doc, os.path.dirname(os.path.join(CF, 'contests'))) if canon_doc else ''
    out_dir = os.path.join(CF, 'contests', range_dir(ap['contestId']), str(ap['contestId']))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{ap['index']}_{title}.md")
    if os.path.exists(out):
        print('已存在:', os.path.relpath(out, ROOT))
        return

    link = os.path.relpath(canon_doc, out_dir).replace(os.sep, '/') if canon_doc else '#'
    body = f"""# Codeforces {ap['contestId']}{ap['index']} {title} 题解

<!-- alias-page -->

> **别名页**：本题与 [Codeforces {canon['contestId']}{canon['index']} {title}]({link}) 是同一道题（题面、样例完全一致），
> 正文只维护一篇，请从上面的链接进入。

## 题目信息

- **题目链接**：https://codeforces.com/problemset/problem/{ap['contestId']}/{ap['index']}
- **比赛来源**：{ap.get('contestId')} · Problem {ap['index']}
- **难度**：{ap.get('rating') if ap.get('rating') else '未评级'}
- **标签**：{'、'.join(ap.get('tags') or [])}
- **规范正文**：[{canon['contestId']}{canon['index']}]({link})
"""
    open(out, 'w', encoding='utf-8').write(body)

    # 清单里登记别名，避免以后重复派单
    for p in probs.values():
        if p['key'] == alias:
            p['path'] = os.path.relpath(out, CF)
            p['status'] = 'published'
            p['alias_of'] = canon
    json.dump(list(probs.values()), open(os.path.join(CF, 'data', 'problems.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('生成', os.path.relpath(out, ROOT))


if __name__ == '__main__':
    main()
