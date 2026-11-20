# 独立暴力 O(n^2)：把所有回文出现 (l,r) 枚举出来，再两两检查是否相交（共享位置）。
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, s = int(data[0]), data[1]

    pals = []
    for i in range(n):
        l, r = i, i                       # 奇
        while l >= 0 and r < n and s[l] == s[r]:
            pals.append((l, r))
            l -= 1
            r += 1
    for i in range(n - 1):
        l, r = i, i + 1                   # 偶
        while l >= 0 and r < n and s[l] == s[r]:
            pals.append((l, r))
            l -= 1
            r += 1

    ans = 0
    m = len(pals)
    for a in range(m):
        l1, r1 = pals[a]
        for b in range(a + 1, m):
            l2, r2 = pals[b]
            if max(l1, l2) <= min(r1, r2):     # 有公共位置
                ans += 1
    print(ans % 51123987)


main()
