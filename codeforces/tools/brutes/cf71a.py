import sys


def brute(s):
    # 独立实现：逐字符数出首尾之间的字母个数
    if len(s) <= 10:
        return s
    middle = 0
    for _ in s[1:-1]:
        middle += 1
    return s[0] + str(middle) + s[-1]


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    out = [brute(data[i]) for i in range(1, n + 1)]
    sys.stdout.write("\n".join(out) + "\n")


main()
