import sys


def drop(n):
    # 独立实现：逐位取模拼出数字（不经过字符串删除）
    if n == 0:
        return 0
    digits = []
    while n:
        d = n % 10
        if d:
            digits.append(d)
        n //= 10
    v = 0
    for d in reversed(digits):
        v = v * 10 + d
    return v


def main():
    data = sys.stdin.read().split()
    a, b = int(data[0]), int(data[1])
    print("YES" if drop(a) + drop(b) == drop(a + b) else "NO")


main()
