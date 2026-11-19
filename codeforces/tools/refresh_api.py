#!/usr/bin/env python3
"""拉取 Codeforces API 原始响应，供 build_manifest.py 重建清单（阶段 0 / 阶段 4 增量）。

输出：.cf-meta/contest_list.json、.cf-meta/problemset.json、.cf-meta/api_fetch.json
Codeforces API 支持 CORS 且不需要登录；若被限频会返回 429，按退避重试。
"""
import json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
META = os.path.join(ROOT, '.cf-meta')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
URLS = {
    'contest_list.json': 'https://codeforces.com/api/contest.list?gym=false',
    'problemset.json': 'https://codeforces.com/api/problemset.problems',
}


def get(url, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            last = e
            wait = 2 ** (i + 1)
            print(f'  重试 {i + 1}/{tries}（{e}），等待 {wait}s', flush=True)
            time.sleep(wait)
    raise SystemExit(f'抓取失败：{url} -> {last}')


def main():
    os.makedirs(META, exist_ok=True)
    meta = {'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'endpoints': URLS}
    for name, url in URLS.items():
        print('GET', url, flush=True)
        data = get(url)
        if data.get('status') != 'OK':
            raise SystemExit(f'{url} 返回 status={data.get("status")}')
        json.dump(data, open(os.path.join(META, name), 'w'))
        n = len(data['result']) if isinstance(data['result'], list) else len(data['result'].get('problems', []))
        print(f'  -> .cf-meta/{name}（{n} 条）', flush=True)
        meta[name.replace('.json', '_count')] = n
        time.sleep(1.0)
    json.dump(meta, open(os.path.join(META, 'api_fetch.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
