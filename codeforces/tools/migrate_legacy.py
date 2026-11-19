#!/usr/bin/env python3
"""把旧的 codeforces/<cid>/<IDX>.<题名>题解.md 迁移到计划目录结构。

旧: codeforces/2285/A.合数排列题解.md            images/cf2285_a_xxx.svg
新: codeforces/contests/2201-2300/2285/A_合数排列.md  codeforces/images/cf2285a_xxx.svg
"""
import json, os, re, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
IMG = os.path.join(ROOT, 'images')
NEWIMG = os.path.join(CF, 'images')
DRY = '--apply' not in sys.argv


def bucket(cid: int) -> str:
    start = (cid - 1) // 100 * 100 + 1
    return f'{start:04d}-{start + 99:04d}'


def main():
    os.makedirs(NEWIMG, exist_ok=True)
    moved_imgs = {}
    docs = []
    for cid_dir in sorted(os.listdir(CF)):
        if not cid_dir.isdigit():
            continue
        d = os.path.join(CF, cid_dir)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.md'):
                continue
            m = re.match(r'^([A-Za-z0-9]+)\.(.+)题解\.md$', fn)
            if not m:
                print('SKIP (bad name)', fn); continue
            idx, title = m.group(1).upper(), m.group(2).strip()
            src = os.path.join(d, fn)
            text = open(src, encoding='utf-8').read()
            h1 = text.splitlines()[0]
            hm = re.match(r'^#\s+Codeforces\s+(.+?)\s+题解\s*$', h1)
            if hm:
                title = hm.group(1).strip()
            cid = int(cid_dir)
            newdir = os.path.join(CF, 'contests', bucket(cid), cid_dir)
            newfn = f'{idx}_{title}.md'
            newpath = os.path.join(newdir, newfn)

            # images: old images/cf<cid>_<idx>_x.svg -> cf<cid><idx>_x.svg
            def repl(mo):
                old = mo.group(1)
                base = os.path.basename(old)
                mm = re.match(r'^cf(\d+)_([a-zA-Z0-9]+?)_(.+)\.svg$', base)
                if not mm:
                    return mo.group(0)
                ocid, oidx, rest = mm.group(1), mm.group(2).lower(), mm.group(3)
                nb = f'cf{ocid}{oidx}_{rest}.svg'
                moved_imgs[os.path.join(IMG, base)] = os.path.join(NEWIMG, nb)
                return f'](../../../images/{nb})'

            text = re.sub(r'\]\((?:\.\./)*images/(cf[0-9A-Za-z_]+\.svg)\)', repl, text)
            text = re.sub(r'^#\s+Codeforces\s+.*$', f'# Codeforces {cid}{idx} {title} 题解', text, count=1, flags=re.M)
            docs.append((src, newpath, text))

    print(f'docs: {len(docs)}, images: {len(moved_imgs)}')
    if DRY:
        for src, dst, _ in docs[:5]:
            print(' ', os.path.relpath(src, ROOT), '->', os.path.relpath(dst, ROOT))
        return

    # 移动图片
    for old, new in moved_imgs.items():
        if os.path.exists(old):
            os.makedirs(os.path.dirname(new), exist_ok=True)
            shutil.move(old, new)
    # 写文档
    for src, dst, text in docs:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'w', encoding='utf-8').write(text)
        os.remove(src)
    # 删除空目录
    for cid_dir in sorted(os.listdir(CF)):
        d = os.path.join(CF, cid_dir)
        if cid_dir.isdigit() and os.path.isdir(d) and not os.listdir(d):
            os.rmdir(d)
    # 更新 problems.json
    pj = os.path.join(CF, 'data', 'problems.json')
    probs = json.load(open(pj))
    cov = {}
    for src, dst, _ in docs:
        rel = os.path.relpath(dst, CF)
        mm = re.search(r'/(\d+)/([A-Za-z0-9]+)_', rel)
        if mm:
            cov[f'{mm.group(1)}/{mm.group(2)}'] = rel
    for p in probs:
        if p['key'] in cov:
            p['path'] = cov[p['key']]
            p['status'] = 'verified'
    json.dump(probs, open(pj, 'w'), ensure_ascii=False, indent=1)
    print('migrated', len(docs), 'docs; covered keys', len(cov))


if __name__ == '__main__':
    main()
