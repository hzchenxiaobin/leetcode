# 独立暴力：用“赢了几个人”作为秩，检查秩是否恰为 0,1,2 的排列。
import sys

def main():
    cmps = sys.stdin.read().split()
    wins = {c: 0 for c in "ABC"}
    for s in cmps:
        a, op, b = s[0], s[1], s[2]
        if op == ">":
            wins[a] += 1
        else:
            wins[b] += 1
    ranks = sorted(wins.values())
    if ranks != [0, 1, 2]:
        print("Impossible")
        return
    order = sorted("ABC", key=lambda c: wins[c])
    print("".join(order))

main()
