# 独立暴力：用值域桶标记出现过的页码（1..1000），再从 1 扫到 1000 合并连续段。
import sys


def main() -> None:
    line = sys.stdin.read().strip()
    present = [False] * 1001
    for tok in line.split(","):
        if tok:
            present[int(tok)] = True

    parts = []
    x = 1
    while x <= 1000:
        if not present[x]:
            x += 1
            continue
        y = x
        while y + 1 <= 1000 and present[y + 1]:
            y += 1
        parts.append(str(x) if x == y else f"{x}-{y}")
        x = y + 1
    print(",".join(parts))


main()
