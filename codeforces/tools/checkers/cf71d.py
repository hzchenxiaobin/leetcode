"""CF71D 特殊评测校验器：python3 check.py <input> <output> <answer>
忽略 expected answer，独立判定并校验选手输出。"""
import sys
import itertools
import re

RANKS = "23456789TJQKA"
SUITS = "CDHS"
ALL = [RANKS[r] + SUITS[s] for r in range(13) for s in range(4)]
CARD = r"([2-9TJQKA][CDHS])"


def valid9(cards):
    if len({c[1] for c in cards}) == 1:
        return True
    return len({c[0] for c in cards}) == 9


def main():
    inp_path, out_path = sys.argv[1], sys.argv[2]
    no_oracle = len(sys.argv) > 4 and sys.argv[4] == "--nooracle"
    tok = open(inp_path).read().split()
    n, m = int(tok[0]), int(tok[1])
    g = [[tok[2 + i * m + j] for j in range(m)] for i in range(n)]
    jp = [(i, j) for i in range(n) for j in range(m) if g[i][j] in ("J1", "J2")]
    J = len(jp)
    used = {g[i][j] for i in range(n) for j in range(m)} - {"J1", "J2"}
    avail = [c for c in ALL if c not in used]
    sq = [(r, c) for r in range(n - 2) for c in range(m - 2)]

    def cells(r, c):
        return [(i, j) for i in range(r, r + 3) for j in range(c, c + 3)]

    # ---- 独立判定：枚举方块对 + 枚举王牌替换 ----
    truth = False
    board = [row[:] for row in g]
    for ai in range(len(sq) if not no_oracle else 0):
        for bi in range(ai + 1, len(sq)):
            (r1, c1), (r2, c2) = sq[ai], sq[bi]
            if abs(r1 - r2) < 3 and abs(c1 - c2) < 3:
                continue
            for combo in itertools.permutations(avail, J):
                for k, (i, j) in enumerate(jp):
                    board[i][j] = combo[k]
                if valid9([board[i][j] for (i, j) in cells(r1, c1)]) and \
                   valid9([board[i][j] for (i, j) in cells(r2, c2)]):
                    truth = True
                    break
            if truth:
                break
        if truth:
            break

    raw = open(out_path).read()
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    assert lines, "输出为空"

    if lines[0] == "No solution.":
        assert len(lines) == 1, "No solution 之后不应再有内容"
        if not no_oracle:
            assert not truth, "实际存在解，但输出 No solution."
        print("OK (no solution)")
        return 0

    assert lines[0] == "Solution exists.", f"首行非法: {lines[0]!r}"
    assert len(lines) == 4, f"应有 4 行，实际 {len(lines)} 行"
    if not no_oracle:
        assert truth, "实际无解，但输出声称有解"

    line = lines[1]
    repl = {}
    if line == "There are no jokers.":
        assert J == 0, "输入里有王牌，不能输出 There are no jokers."
    else:
        m2 = re.fullmatch(r"Replace J(\d) with " + CARD + r"\.", line)
        if m2:
            assert J == 1, "只有一个王牌时才允许单张替换"
            repl[int(m2.group(1))] = m2.group(2)
        else:
            m3 = re.fullmatch(r"Replace J1 with " + CARD + r" and J2 with " + CARD + r"\.", line)
            assert m3, f"第二行格式非法: {line!r}"
            assert J == 2, "两个王牌时才允许双张替换"
            repl[1] = m3.group(1)
            repl[2] = m3.group(2)
        labels = sorted(int(g[i][j][1]) for (i, j) in jp)
        assert sorted(repl.keys()) == labels, f"替换的王牌编号不匹配: {sorted(repl)} vs {labels}"
        cards = [repl[k] for k in repl]
        assert all(c in ALL for c in cards), "替换牌不是合法牌"
        assert all(c in avail for c in cards), "替换牌已经在布局里"
        assert len(set(cards)) == len(cards), "替换牌重复"

    pos = []
    for idx, pat in ((2, "first"), (3, "second")):
        mm = re.fullmatch(r"Put the " + pat + r" square to \((\d+), (\d+)\)\.", lines[idx])
        assert mm, f"第 {idx+1} 行格式非法: {lines[idx]!r}"
        r, c = int(mm.group(1)), int(mm.group(2))
        assert 1 <= r <= n - 2 and 1 <= c <= m - 2, f"方块越界: ({r}, {c})"
        pos.append((r - 1, c - 1))

    (r1, c1), (r2, c2) = pos
    assert abs(r1 - r2) >= 3 or abs(c1 - c2) >= 3, "两个方块重叠"
    for k, (i, j) in enumerate(jp):
        board[i][j] = repl[int(g[i][j][1])]
    assert valid9([board[i][j] for (i, j) in cells(r1, c1)]), "第一个方块不合法"
    assert valid9([board[i][j] for (i, j) in cells(r2, c2)]), "第二个方块不合法"
    print("OK")
    return 0


sys.exit(main())
