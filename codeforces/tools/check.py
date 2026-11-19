#!/usr/bin/env python3
"""新目录结构的 Codeforces 题解检查器。

用法: python3 codeforces/tools/check.py codeforces/contests/0001-0100/1 [更多目录或 .md]
"""
import re, os, sys, glob, textwrap, subprocess, tempfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CF = os.path.join(ROOT, 'codeforces')
IMGRE = re.compile(r'!\[[\s\S]*?\]\(([^)]+)\)')
SECTIONS = ['## 1. 题目概述', '## 2. 示例与观察', '## 3. 解题思路', '## 4. 正确性证明',
            '## 5. 复杂度分析', '## 6. 参考代码', '## 7. 边界情况与易错点', '## 8. 验证记录',
            '## 相关题目与扩展']
# 旧版结构（阶段 1 之前迁移进来的 296 篇）：多一节「算法细节」，验证记录编号为 9
LEGACY_SECTIONS = ['## 1. 题目概述', '## 2. 示例', '## 3. 解题思路', '## 4. 算法细节',
                   '## 5. 正确性证明', '## 6. 复杂度分析', '## 7. 参考代码',
                   '## 8. 边界情况与易错点', '## 相关题目与扩展']
VERIFY_RE = re.compile(r'^## (?:8|9)\. 验证记录\s*$', re.M)


def check_doc(path):
    errs, warns = [], []
    src = open(path, encoding='utf-8').read()
    h1 = next((l for l in src.splitlines() if l.startswith('# ')), '')
    m = re.match(r'# Codeforces (\d+)([A-Za-z0-9]+) .+ 题解\s*$', h1)
    if not m:
        errs.append(f'H1 格式: {h1!r}')
    else:
        rel = os.path.relpath(path, CF)
        if f'/{m.group(1)}/' not in rel and not rel.startswith(f'contests/0001-0100/{m.group(1)}/'):
            errs.append(f'H1 场次 {m.group(1)} 与路径 {rel} 不一致')
    if re.search(r'^---\s*$', src, re.M):
        warns.append('含 --- 分隔线')
    if all(sec in src for sec in LEGACY_SECTIONS):
        warns.append('旧版章节结构（示例 / 算法细节 / 验证记录编号 9）')
    else:
        for sec in SECTIONS:
            if sec not in src:
                errs.append(f'缺少章节 {sec}')
    if not VERIFY_RE.search(src):
        errs.append('缺少章节 验证记录')
    for key in ['题目链接', '比赛来源', '难度', '标签', '评测类型', '**题意**', '**约束**']:
        if key not in src:
            warns.append(f'元信息缺 {key}')
    if '引理' not in src:
        errs.append('无引理')
    if '定理' not in src:
        errs.append('无定理')
    if not any(k in src for k in ('∎', '□', '\\blacksquare', '\\square')):
        errs.append('证明无 ∎')
    if src.count('```') % 2:
        errs.append('代码围栏不配对')
    if '```cpp' not in src:
        errs.append('缺 C++ 代码')
    if '```python' not in src:
        errs.append('缺 Python 代码')
    if 'int main' not in src and not re.search(r'\bclass\s+\w+', src):
        errs.append('无 main')
    mm = re.search(r'## 7\. 边界情况与易错点(.*?)(?=\n## )', src, re.S)
    if mm:
        n = len(re.findall(r'^\d+\.\s', mm.group(1), re.M))
        if n < 4:
            warns.append(f'边界情况仅 {n} 条')
    mvr = VERIFY_RE.search(src)
    if mvr:
        seg = src[mvr.end():]
        if len(seg.strip()) < 40:
            warns.append('验证记录过短')
    imgs = [x for x in IMGRE.findall(src) if re.search(r'\.svg$', x)]
    if not (2 <= len(imgs) <= 5):
        warns.append(f'插图数 {len(imgs)}')
    for im in imgs:
        p = os.path.normpath(os.path.join(os.path.dirname(path), im))
        if not os.path.exists(p):
            errs.append(f'图片不存在 {im}')
            continue
        try:
            ET.parse(p)
        except Exception as e:
            errs.append(f'SVG 非法 {im}: {e}')
            continue
        s = open(p, encoding='utf-8').read()
        if 'feTurbulence' not in s:
            warns.append(f'{im} 无抖动滤镜')
        if 'Comic Sans' not in s and 'Kaiti' not in s:
            warns.append(f'{im} 无手写字体')
    code = '\n'.join(re.findall(r'```(?:cpp|python)\n(.*?)```', src, re.S))
    if re.search(r'Create the variable named', code):
        errs.append('代码中残留注入变量')
    return errs, warns


def compile_check(paths):
    bad = []
    hdr = '\n'.join('#include <%s>' % h for h in [
        'vector', 'string', 'unordered_map', 'unordered_set', 'map', 'set', 'queue', 'stack', 'deque',
        'algorithm', 'numeric', 'functional', 'climits', 'cstring', 'cmath', 'cstdio', 'cstdlib',
        'iostream', 'sstream', 'bitset', 'array', 'tuple', 'list', 'utility', 'cstdint', 'random',
        'chrono', 'cassert', 'cctype', 'iterator', 'memory', 'type_traits', 'cstddef', 'iomanip'])
    for p in paths:
        src = open(p, encoding='utf-8').read()
        pys = re.findall(r'```python\n(.*?)```', src, re.S)
        if pys:
            ok, err = False, None
            for code in pys:
                try:
                    compile(textwrap.dedent(code), p, 'exec')
                    ok = True
                    break
                except SyntaxError as e:
                    err = e
            if not ok:
                bad.append((p, 'py', err))
        cpps = re.findall(r'```cpp\n(.*?)```', src, re.S)
        if cpps:
            ok, last = False, None
            for code in cpps:
                code = re.sub(r'#include\s*<bits/stdc\+\+\.h>\n?', '', code)
                pre = hdr + '\nusing namespace std;\n'
                with tempfile.NamedTemporaryFile('w', suffix='.cpp', delete=False) as f:
                    f.write(pre + code)
                    tmp = f.name
                r = subprocess.run(['g++', '-std=c++17', '-fsyntax-only', tmp], capture_output=True, text=True)
                if r.returncode == 0:
                    ok = True
                    break
                last = r.stderr.splitlines()[:4]
            if not ok:
                bad.append((p, 'cpp', last))
    return bad


def main(args):
    paths = []
    for a in args:
        d = os.path.join(ROOT, a) if not os.path.isabs(a) else a
        if os.path.isdir(d):
            paths += glob.glob(os.path.join(d, '**', '*.md'), recursive=True)
        elif os.path.exists(d):
            paths.append(d)
    bad = 0
    for p in sorted(paths):
        e, w = check_doc(p)
        if e:
            bad += 1
            print('FAIL', os.path.relpath(p, ROOT))
            for x in e:
                print('   -', x)
        if w and os.environ.get('SHOW_WARN'):
            print('WARN', os.path.relpath(p, ROOT))
            for x in w:
                print('   ~', x)
    print(f'checked {len(paths)}, fail {bad}')


if __name__ == '__main__':
    main(sys.argv[1:])
