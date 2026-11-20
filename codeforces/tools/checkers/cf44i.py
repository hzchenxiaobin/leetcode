import sys


def bell(n):
    # Bell triangle
    row = [1]
    for i in range(1, n + 1):
        new = [row[-1]]
        for x in row:
            new.append(new[-1] + x)
        row = new
    return row[0]


def parse(line, n):
    parts = line.split(',{')
    blocks = []
    for p in parts:
        p = p.strip().strip('{}')
        if p == '':
            blocks.append([])
            continue
        blocks.append([int(x) for x in p.split(',')])
    flat = []
    for b in blocks:
        if b != sorted(b) or not b:
            return None
        flat += b
    if sorted(flat) != list(range(1, n + 1)):
        return None
    mins = [b[0] for b in blocks]
    if mins != sorted(mins):
        return None
    return blocks


def relation(blocks):
    s = set()
    for b in blocks:
        for x in b:
            for y in b:
                if x < y:
                    s.add((x, y))
    return s


def main():
    inp = open(sys.argv[1]).read().split()
    out = [l.strip() for l in open(sys.argv[2]).read().splitlines() if l.strip() != '']
    n = int(inp[0])
    B = bell(n)
    if not out:
        print('FAIL empty output')
        sys.exit(1)
    if int(out[0]) != B:
        print('FAIL count %s != %d' % (out[0], B))
        sys.exit(1)
    if len(out) != 1 + B:
        print('FAIL line count')
        sys.exit(1)
    prev = None
    seen = set()
    for line in out[1:]:
        bl = parse(line, n)
        if bl is None:
            print('FAIL bad partition format:', line)
            sys.exit(1)
        key = tuple(tuple(b) for b in bl)
        if key in seen:
            print('FAIL duplicate partition:', line)
            sys.exit(1)
        seen.add(key)
        if prev is not None:
            rp, rc = relation(prev), relation(bl)
            if not any({(a, b) for a, b in rp if a != x and b != x} ==
                       {(a, b) for a, b in rc if a != x and b != x} for x in range(1, n + 1)):
                print('FAIL consecutive not one move:', line)
                sys.exit(1)
        prev = bl
    print('OK')


if __name__ == '__main__':
    main()
