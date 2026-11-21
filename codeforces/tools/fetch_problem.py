#!/usr/bin/env python3
"""从洛谷镜像抓取 Codeforces 题面（题意、输入输出格式、样例），供写作与验证使用。

Codeforces 主站题面页对无浏览器环境的请求返回 403，洛谷镜像保存了完整题面与样例，
可以作为「官方页面来源记录」的替代来源；样例文本与 Codeforces 原页一致。

用法：
  python3 codeforces/tools/fetch_problem.py 4 A            # 打印 JSON
  python3 codeforces/tools/fetch_problem.py 4 A -o /tmp/x.json
  python3 codeforces/tools/fetch_problem.py --batch 3,4,5  # 抓整场比赛到 .cf-meta/statements/<cid>.json

缓存：.cf-meta/statements/<pid>.json，重复抓取直接读缓存（加 --force 覆盖）。
"""
import html as _html, json, os, re, sys, time, urllib.parse, urllib.request, http.cookiejar

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, '.cf-meta', 'statements')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

_jar = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_jar))


def _get(url, tries=4):
    last = None
    for i in range(tries):
        req = urllib.request.Request(url, headers={
            'User-Agent': UA,
            'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.luogu.com.cn/',
        })
        try:
            with _opener.open(req, timeout=30) as r:
                return r.read().decode('utf-8', 'ignore')
        except Exception as e:  # 302 机器人校验、限频(401/429)、超时都退避重试
            last = e
            code = getattr(e, 'code', None)
            time.sleep((12 if code in (401, 403, 429) else 2) * (i + 1))
    raise RuntimeError(f'fetch failed {url}: {last}')


def _context(html):
    m = re.search(r'<script id="lentille-context" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def _strip(md):
    """洛谷题面是 Markdown，保留可用结构，去掉多余的 HTML 标记。"""
    if not md:
        return ''
    md = re.sub(r'<script[\s\S]*?</script>', '', md)
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'</?(div|p|span|center|font)[^>]*>', '', md)
    md = md.replace('\r\n', '\n')
    return md.strip()


def fetch(contest, index, force=False, delay=1.2):
    pid = f'CF{contest}{index}'
    os.makedirs(CACHE, exist_ok=True)
    cache = os.path.join(CACHE, pid + '.json')
    if os.path.exists(cache) and not force:
        return json.load(open(cache, encoding='utf-8'))

    time.sleep(delay)
    html = _get(f'https://www.luogu.com.cn/problem/{pid}')
    ctx = _context(html)
    if not ctx or ctx.get('status') != 200:
        # 302 校验页：重新取一次（cookie 已写入）
        time.sleep(1.0)
        html = _get(f'https://www.luogu.com.cn/problem/{pid}')
        ctx = _context(html)
    if not ctx or ctx.get('status') != 200:
        data = {'pid': pid, 'ok': False, 'error': 'no lentille-context (status=%s)' % (ctx or {}).get('status')}
    else:
        pr = ctx['data']['problem']
        # 洛谷返回的样例常带 HTML 实体（&quot; / &lt; / &gt;），必须还原成真实字符
        samples = [{'in': _html.unescape(s[0]), 'out': _html.unescape(s[1])}
                   for s in (pr.get('samples') or [])]
        zh = pr.get('contenu') or {}
        en = pr.get('content') or {}

        def pick(field):
            """英文原文优先用于核对格式，中文译文用于快速理解题意。"""
            return {'zh': _strip(zh.get(field)), 'en': _strip(en.get(field))}

        data = {
            'pid': pid,
            'ok': True,
            'name': pr.get('name'),
            'cf_url': (pr.get('vjudge') or {}).get('link'),
            'background': pick('background'),
            'description': pick('description'),
            'inputFormat': pick('formatI'),
            'outputFormat': pick('formatO'),
            'hint': pick('hint'),
            'samples': samples,
            'limits': pr.get('limits'),
            'difficulty': pr.get('difficulty'),
            'tags': pr.get('tags'),
            'submitted': pr.get('totalSubmit'),
            'accepted': pr.get('totalAccepted'),
            'fetched_from': f'https://www.luogu.com.cn/problem/{pid}',
        }
    json.dump(data, open(cache, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return data


def main(argv):
    force = '--force' in argv
    argv = [a for a in argv if a != '--force']
    if not argv:
        print(__doc__)
        return
    batch = None
    out = None
    rest = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--batch':
            batch = argv[i + 1]; i += 2; continue
        if a == '-o':
            out = argv[i + 1]; i += 2; continue
        rest.append(a); i += 1

    if batch:
        res = {}
        for cid in [int(x) for x in batch.split(',')]:
            res[cid] = {}
            for idx in rest:
                res[cid][idx] = fetch(cid, idx, force)
                time.sleep(1.0)
        payload = json.dumps(res, ensure_ascii=False, indent=1)
    else:
        cid, idx = rest[0], rest[1]
        d = fetch(cid, idx, force)
        payload = json.dumps(d, ensure_ascii=False, indent=1)

    if out:
        open(out, 'w', encoding='utf-8').write(payload)
        print('wrote', out)
    else:
        print(payload)


if __name__ == '__main__':
    main(sys.argv[1:])
