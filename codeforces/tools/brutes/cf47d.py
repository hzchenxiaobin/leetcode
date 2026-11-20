# 独立暴力：n <= 14 时直接枚举所有 2^n 个密码，逐个核对 m 条回应。
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    pat, c = [], []
    p = 2
    for _ in range(m):
        s = data[p]; p += 1
        c.append(int(data[p])); p += 1
        pat.append(int(s, 2) if "1" in s else 0)

    ans = 0
    for code in range(1 << n):
        ok = True
        for i in range(m):
            matches = n - bin(code ^ pat[i]).count("1")
            if matches != c[i]:
                ok = False
                break
        if ok:
            ans += 1
    print(ans)


main()
