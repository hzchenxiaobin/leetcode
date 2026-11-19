#!/usr/bin/env python3
"""全量审计：逐篇编译代码、跑真实样例、比对，并检查文档结构。

结果写入 .cf-meta/audit.json，供阶段 3 对账使用。
用法: python3 codeforces/tools/audit.py [--limit N] [--only <substr>]
"""
import argparse, glob, json, os, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(ROOT, 'codeforces', 'tools')
sys.path.insert(0, TOOLS)
import verify_solution as V
import check as C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--only', default='')
    a = ap.parse_args()

    docs = sorted(glob.glob(os.path.join(ROOT, 'codeforces', 'contests', '**', '*.md'), recursive=True))
    docs = [d for d in docs if a.only in d]
    if a.limit:
        docs = docs[:a.limit]
    rows = []
    for i, doc in enumerate(docs, 1):
        rec = {'doc': os.path.relpath(doc, ROOT)}
        try:
            errs, warns = C.check_doc(doc)
            rec['doc_errors'] = errs
            rec['doc_warns'] = warns
            d = V.parse_doc(doc)
            st = V.ensure_statement(d['contest'], d['index'])
            rec['pid'] = st.get('pid')
            rec['samples'] = len(st.get('samples') or [])
            rec['title_ok'] = (st.get('name') or '').lower() in doc.lower() if st.get('name') else None
            if d['cpp']:
                with tempfile.TemporaryDirectory(prefix='audit_') as wd:
                    exe, ct, err = V.compile_cpp(d['cpp'], wd)
                    rec['cpp_compiled'] = bool(exe)
                    if exe:
                        ok = 0
                        for s in st.get('samples') or []:
                            out, ms, rc = V.run(exe, s['in'], 10)
                            ok += V.norm(out) == V.norm(s["out"])
                        rec['cpp_samples_ok'] = ok
                    else:
                        rec['cpp_error'] = err.splitlines()[:3]
            if d['py']:
                with tempfile.TemporaryDirectory(prefix='auditpy_') as wd:
                    srcp = os.path.join(wd, 'm.py'); open(srcp, 'w').write(d['py'])
                    r = __import__('subprocess').run([sys.executable, '-c', 'import sys;compile(open(sys.argv[1]).read(),sys.argv[1],"exec")', srcp], capture_output=True, text=True)
                    rec['py_ok_syntax'] = r.returncode == 0
        except Exception as e:
            rec['error'] = str(e)[:300]
        rows.append(rec)
        print(f"[{i}/{len(docs)}] {rec['doc'].split('/')[-1]} cpp={rec.get('cpp_samples_ok')}/{rec.get('samples')} "
              f"docerr={len(rec.get('doc_errors') or [])} py={rec.get('py_ok_syntax')}", flush=True)
    out = os.path.join(ROOT, '.cf-meta', 'audit.json')
    json.dump(rows, open(out, 'w'), ensure_ascii=False, indent=1)
    good = [r for r in rows if r.get('samples') and r.get('cpp_samples_ok') == r.get('samples')]
    print(f"\n审计 {len(rows)} 篇：样例全过 {len(good)}，文档结构无错 {sum(1 for r in rows if not r.get('doc_errors'))}")
    print('明细:', out)


if __name__ == '__main__':
    main()
