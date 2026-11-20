import sys
from elems import NUM

def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    a = [NUM[x] for x in data[2:2 + n]]
    b = [NUM[x] for x in data[2 + n:2 + n + k]]

    def rec(j, used):
        if j == k:
            return used == (1 << n) - 1
        def pick(start, acc, used):
            if acc == b[j]:
                return rec(j + 1, used)
            for i in range(start, n):
                if used >> i & 1 or acc + a[i] > b[j]:
                    continue
                if pick(i + 1, acc + a[i], used | 1 << i):
                    return True
            return False
        return pick(0, 0, used)

    print("YES" if rec(0, 0) else "NO")

main()
