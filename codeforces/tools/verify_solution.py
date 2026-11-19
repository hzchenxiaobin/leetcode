#!/usr/bin/env python3
"""编译题解里的 C++/Python 代码，用真实样例运行并比对，输出可写入「验证记录」的结果。

样例来源：`codeforces/tools/fetch_problem.py` 抓取的洛谷题面缓存（与 Codeforces 原页一致）。

用法：
  python3 codeforces/tools/verify_solution.py codeforces/contests/0001-0100/4/A_西瓜.md
  python3 codeforces/tools/verify_solution.py <doc> --checker /tmp/chk.py   # 特殊评测/构造题
  python3 codeforces/tools/verify_solution.py <doc> --brute /tmp/brute.cpp --random 200  # 随机对拍

checker 约定：`python3 chk.py <input> <output> <answer>`，返回 0 表示通过。
随机对拍约定：brute 程序与题解程序读同一输入、各自输出；对拍由 `tools/stress.py` 调用。
"""
import argparse, json, os, re, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(ROOT, 'codeforces', 'tools')
STATEMENTS = os.path.join(ROOT, '.cf-meta', 'statements')
sys.path.insert(0, TOOLS)


def parse_doc(path):
    src = open(path, encoding='utf-8').read()
    h1 = next((l for l in src.splitlines() if l.startswith('# ')), '')
    m = re.match(r'# Codeforces (\d+)([A-Za-z0-9]+)', h1)
    cpp = re.findall(r'```cpp\n(.*?)```', src, re.S)
    py = re.findall(r'```python\n(.*?)```', src, re.S)

    def full(blocks, needle):
        """正文里可能先给一段讲解用片段，再给完整程序：优先取含入口函数的块。"""
        whole = [b for b in blocks if needle in b]
        return (whole[-1] if whole else (blocks[-1] if blocks else None))

    return {
        'path': path,
        'h1': h1,
        'contest': int(m.group(1)) if m else None,
        'index': m.group(2) if m else None,
        'cpp': full(cpp, 'int main'),
        'py': full(py, 'def main') or (py[-1] if py else None),
    }


def ensure_statement(contest, index, force=False):
    from fetch_problem import fetch
    key = f'CF{contest}{index}'
    p = os.path.join(STATEMENTS, key + '.json')
    if os.path.exists(p) and not force:
        return json.load(open(p, encoding='utf-8'))
    return fetch(contest, index, force=force)


def norm(s, mode='token'):
    """Codeforces 标准 checker 按 token 比对（空白与大小写不敏感）；
    --compare exact 时退化为逐字逐行比对。"""
    s = s.replace('\r\n', '\n')
    if mode == 'exact':
        return '\n'.join(l.rstrip() for l in s.split('\n')).strip('\n')
    return tuple(s.lower().split())


SHIM = os.path.join(TOOLS, 'include')
_CXX = None


def cxx():
    """优先真正的 GNU g++（<bits/stdc++.h> 原生可用）；否则用 clang++ + 兼容头。"""
    global _CXX
    if _CXX:
        return _CXX
    for cand in ('g++-15', 'g++-14', 'g++-13', 'g++-12', 'g++'):
        p = subprocess.run(['which', cand], capture_output=True, text=True).stdout.strip()
        if not p:
            continue
        probe = tempfile.NamedTemporaryFile('w', suffix='.cpp', delete=False)
        probe.write('#include <bits/stdc++.h>\nint main(){std::vector<int> v;return 0;}\n')
        probe.close()
        r = subprocess.run([p, '-std=c++17', '-fsyntax-only', probe.name], capture_output=True, text=True)
        os.unlink(probe.name)
        if r.returncode == 0:
            _CXX = [p]
            return _CXX
    _CXX = ['clang++', '-I', SHIM]
    return _CXX


def compile_cpp(code, workdir):
    src = os.path.join(workdir, 'main.cpp')
    exe = os.path.join(workdir, 'main')
    open(src, 'w').write(code)
    t0 = time.time()
    r = subprocess.run(cxx() + ['-std=c++17', '-O2', '-pipe', '-o', exe, src],
                       capture_output=True, text=True)
    return exe if r.returncode == 0 else None, (time.time() - t0), r.stderr[:2000]


def run(exe, inp, timeout=10):
    t0 = time.time()
    try:
        r = subprocess.run([exe], input=inp, capture_output=True, text=True, timeout=timeout)
        return r.stdout, (time.time() - t0) * 1000, r.returncode
    except subprocess.TimeoutExpired:
        return '', timeout * 1000, -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('doc')
    ap.add_argument('--checker', help='特殊评测校验器 (input output answer)')
    ap.add_argument('--compare', choices=['token', 'exact'], default='token')
    ap.add_argument('--timeout', type=float, default=10.0)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()

    d = parse_doc(a.doc)
    if not d['contest']:
        print('无法从 H1 解析题号'); sys.exit(2)
    st = ensure_statement(d['contest'], d['index'])
    samples = st.get('samples') or []
    result = {'doc': os.path.relpath(a.doc, ROOT), 'pid': st['pid'],
              'samples': len(samples), 'cpp': None, 'py': None,
              'cpp_ok': 0, 'py_ok': 0, 'max_ms': 0}

    with tempfile.TemporaryDirectory(prefix='cfverify_') as wd:
        if d['cpp']:
            exe, ct, err = compile_cpp(d['cpp'], wd)
            result['cpp'] = {'compiled': bool(exe), 'compile_ms': round(ct)}
            if not exe:
                result['cpp']['error'] = err
            else:
                ok = 0
                for i, s in enumerate(samples):
                    out, ms, rc = run(exe, s['in'], a.timeout)
                    result['max_ms'] = max(result['max_ms'], round(ms))
                    if a.checker:
                        ip = os.path.join(wd, 'in.txt'); op = os.path.join(wd, 'out.txt')
                        open(ip, 'w').write(s['in']); open(op, 'w').write(out)
                        good = subprocess.run([sys.executable, a.checker, ip, op, '/dev/stdin'],
                                              input=s['out'], capture_output=True, text=True).returncode == 0
                    else:
                        good = norm(out, a.compare) == norm(s['out'], a.compare)
                    if good:
                        ok += 1
                    else:
                        result.setdefault('fails', []).append({
                            'sample': i + 1, 'expected': s['out'][:200], 'got': out[:200]})
                result['cpp_ok'] = ok
        if d['py']:
            src = os.path.join(wd, 'main.py')
            open(src, 'w').write(d['py'])
            ok = 0
            r = subprocess.run([sys.executable, '-c', 'import sys;compile(open(sys.argv[1]).read(),sys.argv[1],"exec")', src],
                               capture_output=True, text=True)
            result['py'] = {'compiled': r.returncode == 0}
            if r.returncode == 0:
                for s in samples:
                    try:
                        p = subprocess.run([sys.executable, src], input=s['in'], capture_output=True,
                                           text=True, timeout=a.timeout)
                        out = p.stdout
                    except subprocess.TimeoutExpired:
                        out = ''
                    if a.checker:
                        ip = os.path.join(wd, 'in.txt'); op = os.path.join(wd, 'out.txt')
                        open(ip, 'w').write(s['in']); open(op, 'w').write(out)
                        good = subprocess.run([sys.executable, a.checker, ip, op, '/dev/stdin'],
                                              input=s['out'], capture_output=True, text=True).returncode == 0
                    else:
                        good = norm(out, a.compare) == norm(s['out'], a.compare)
                    ok += good
                result['py_ok'] = ok

    if a.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"{result['pid']}: samples {result['samples']}")
        if result['cpp']:
            print(f"  C++ 编译 {'OK' if result['cpp']['compiled'] else 'FAIL'}, "
                  f"样例 {result['cpp_ok']}/{result['samples']}, 最慢 {result['max_ms']} ms")
        if result['py']:
            print(f"  Python 语法 {'OK' if result['py']['compiled'] else 'FAIL'}, 样例 {result['py_ok']}/{result['samples']}")
        for f in result.get('fails', [])[:3]:
            print(f"  样例 {f['sample']} 不符: 期望 {f['expected']!r} 实际 {f['got']!r}")
    sys.exit(0 if (result['cpp_ok'] == result['samples'] and result['samples'] > 0) else 1)


if __name__ == '__main__':
    main()
