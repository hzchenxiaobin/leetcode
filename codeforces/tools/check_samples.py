#!/usr/bin/env python3
"""核对正文第 2 节里贴出的「官方样例」是否与镜像题面逐字一致。

正文不允许自造官方样例：样例块必须来自 .cf-meta/statements 的 samples。
解析约定：```text 块内用「输入：」「输出：」分隔（也接受 样例输入 / Input / Output）。

用法: python3 codeforces/tools/check_samples.py [--only <substr>]
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
# 正文里常见「**输入**：」「输入：」等写法，比对时先去掉强调符号
# 允许「输入（自造 ①：…）：」「样例输入 #2：」这类写法
_SUF = r'\s*(?:[#＃]\s*\d+)?\s*(?:[（(][^）)]*[）)])?\s*[:：]?\s*$'
IN_RE = re.compile(r'^\s*(?:样例)?(?:输入|Input)' + _SUF)
OUT_RE = re.compile(r'^\s*(?:样例)?(?:输出|Output)' + _SUF)


def _clean(l):
    return l.replace('*', '').replace('`', '').strip()
H1 = re.compile(r'^# Codeforces (\d+)([A-Za-z0-9]+) ', re.M)


def norm(s):
    s = s.replace('\r\n', '\n')
    lines = [l.rstrip() for l in s.split('\n')]
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return '\n'.join(lines)


def blocks(src):
    out = []
    for m in re.finditer(r'```(?:text|plaintext)\n(.*?)```', src, re.S):
        body = m.group(1)
        if any(IN_RE.match(_clean(l)) or OUT_RE.match(_clean(l)) for l in body.split('\n')):
            out.append(body)
    return out


def parse(body):
    """-> [(输入, 输出)]；支持一个块里多组「输入 / 输出」。"""
    lines = body.split('\n')
    pairs, cur, mode = [], {}, None
    for raw in lines:
        l = _clean(raw)
        if IN_RE.match(l):
            if mode == 'out' and 'in' in cur:
                pairs.append((cur.get('in', ''), cur.get('out', '')))
                cur = {}
            mode = 'in'
            cur.setdefault('in', '')
            continue
        if OUT_RE.match(l):
            mode = 'out'
            cur.setdefault('out', '')
            continue
        if mode:
            # 保留原始字符（样例里可能有 * 组成的图形、制表符等），只去掉行尾空白
            cur[mode] = cur.get(mode, '') + ('\n' if cur.get(mode) else '') + raw.rstrip()
    if cur:
        pairs.append((cur.get('in', ''), cur.get('out', '')))
    return [(norm(a), norm(b)) for a, b in pairs]


def main():
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else ''
    docs = sorted(glob.glob(os.path.join(CF, 'contests', '*', '*', '*.md')))
    bad, checked, skipped = [], 0, 0
    for doc in docs:
        if only and only not in doc:
            continue
        src = open(doc, encoding='utf-8').read()
        if '<!-- alias-page -->' in src:
            continue
        m = H1.search(src)
        if not m:
            continue
        cache = os.path.join(ROOT, '.cf-meta', 'statements', f'CF{m.group(1)}{m.group(2)}.json')
        if not os.path.exists(cache):
            skipped += 1
            continue
        st = json.load(open(cache, encoding='utf-8'))
        official = [(norm(s['in']), norm(s['out'])) for s in st.get('samples') or []]
        if not official:
            skipped += 1
            continue
        # 同一篇里「输入」和「输出」可能分别放在两个 ```text 块里，按出现顺序拼接后再解析，
        # 这样既支持单块，也支持拆块写法
        got = parse('\n'.join(blocks(src)))
        # 只比对前 k 组官方样例（正文可能另附自造样例，按规范会标注）
        matched = sum(1 for i, o in enumerate(official) if o in got)
        checked += 1
        rel = os.path.relpath(doc, ROOT)
        if matched < len(official):
            miss = [i + 1 for i, o in enumerate(official) if o not in got]
            bad.append((rel, len(official), matched, miss))
    print(f'核对 {checked} 篇（缺少题面缓存跳过 {skipped} 篇）：样例完全一致 {checked - len(bad)} 篇，有问题 {len(bad)} 篇')
    for rel, n, k, miss in bad:
        print(f'  ✘ {rel}: 官方样例 {k}/{n} 一致，缺第 {miss} 组')
    sys.exit(0 if not bad else 1)


if __name__ == '__main__':
    main()
