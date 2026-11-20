# 独立暴力：对每个 i，删掉它之后把剩下的区间排序、逐对检查是否重叠（O(n^2 log n)）。
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    segs = []
    p = 1
    for i in range(n):
        segs.append((int(data[p]), int(data[p + 1])))
        p += 2

    ans = []
    for drop in range(n):
        rest = sorted(segs[:drop] + segs[drop + 1:])
        ok = True
        for x in range(len(rest) - 1):
            if rest[x][1] > rest[x + 1][0]:
                ok = False
                break
        if ok:
            ans.append(drop + 1)

    print(len(ans))
    if ans:
        print(" ".join(map(str, ans)) + " ")


main()
