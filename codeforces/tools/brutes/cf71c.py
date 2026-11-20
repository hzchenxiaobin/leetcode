import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    a = data[1:1 + n]
    # 独立实现：枚举「相邻两个好骑士」确定步长 d，
    # 再按 d 环游一圈检查全部顶点是否都是好心情。
    for i in range(n):
        if not a[i]:
            continue
        for j in range(n):
            if i == j or not a[j]:
                continue
            d = (j - i) % n
            if d == 0 or n % d:
                continue
            if n // d < 3:
                continue
            if all(a[(i + t * d) % n] for t in range(n // d)):
                print("YES")
                return
    print("NO")


main()
