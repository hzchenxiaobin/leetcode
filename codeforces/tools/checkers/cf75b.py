import re
import sys


def main():
    lines = sys.stdin.read().splitlines()
    me = lines[0].strip()
    n = int(lines[1].strip())
    pri = {}
    names = set()
    for i in range(n):
        line = lines[2 + i].strip()
        # 独立实现：正则匹配三种动作
        m = re.fullmatch(r"(\w+) posted on (\w+)'s wall", line)
        if m:
            x, y, pts = m.group(1), m.group(2), 15
        else:
            m = re.fullmatch(r"(\w+) commented on (\w+)'s post", line)
            if m:
                x, y, pts = m.group(1), m.group(2), 10
            else:
                m = re.fullmatch(r"(\w+) likes (\w+)'s post", line)
                assert m, line
                x, y, pts = m.group(1), m.group(2), 5
        names.add(x)
        names.add(y)
        if x == me:
            pri[y] = pri.get(y, 0) + pts
        if y == me:
            pri[x] = pri.get(x, 0) + pts
    names.discard(me)
    out = sorted(names, key=lambda s: (-pri.get(s, 0), s))
    print("\n".join(out))


main()
