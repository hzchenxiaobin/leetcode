# 独立暴力：BFS 枚举所有可达串，再数其中"平衡"（三个字母出现次数两两差 <= 1）的个数。
import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    n, s = int(data[0]), data[1]
    seen = {s}
    q = deque([s])
    while q:
        cur = q.popleft()
        for i in range(n - 1):
            for t in (cur[:i + 1] + cur[i] + cur[i + 2:],       # 后一个变成前一个
                      cur[:i] + cur[i + 1] + cur[i + 1:]):      # 前一个变成后一个
                if t not in seen:
                    seen.add(t)
                    q.append(t)
    ans = 0
    for t in seen:
        cnt = [t.count('a'), t.count('b'), t.count('c')]
        if max(cnt) - min(cnt) <= 1:
            ans += 1
    print(ans % 51123987)


main()
