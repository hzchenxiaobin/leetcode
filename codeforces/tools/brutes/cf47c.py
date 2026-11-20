# 独立暴力：枚举六个词的排列，把网格“画”出来，再从网格里反读六个词，
# 检查它们恰好是输入的多重集合（用反读来验证，而不是直接比较 7 个交点）。
import sys
from itertools import permutations


def build(words, perm):
    H1, V1, M, V2, H3, V3 = [words[i] for i in perm]
    a, b, L, H = len(H1), len(V1), len(M), len(V2)
    c, d = len(H3), len(V3)
    if c != L - a + 1 or d != H - b + 1 or a < 1 or b < 1 or c < 1 or d < 1:
        return None
    g = [["."] * L for _ in range(H)]
    for j in range(a):
        g[0][j] = H1[j]
    for i in range(b):
        g[i][0] = V1[i]
    for j in range(L):
        g[b - 1][j] = M[j]
    for i in range(H):
        g[i][a - 1] = V2[i]
    for j in range(c):
        g[H - 1][a - 1 + j] = H3[j]
    for i in range(d):
        g[b - 1 + i][L - 1] = V3[i]
    return g


def extract(g):
    H, L = len(g), len(g[0])
    words = []
    # 上横：row 0 从 col0 起的连续字母
    row0 = "".join(ch for ch in g[0] if ch != ".")
    words.append(row0)
    # 左竖：col0 的连续字母
    col0 = "".join(g[i][0] for i in range(H) if g[i][0] != ".")
    words.append(col0)
    # 中横：最长的行（第 b-1 行整行都是字母且长度 L）
    mid = None
    for i in range(H):
        if all(ch != "." for ch in g[i]):
            mid = "".join(g[i])
            break
    if mid is None:
        return None
    words.append(mid)
    # 中竖：col a-1 整列
    colmid = None
    for j in range(L):
        if all(g[i][j] != "." for i in range(H)):
            colmid = "".join(g[i][j] for i in range(H))
            break
    if colmid is None:
        return None
    words.append(colmid)
    # 下横：最后一行去点
    words.append("".join(ch for ch in g[H - 1] if ch != "."))
    # 右竖：最后一列去点
    words.append("".join(g[i][L - 1] for i in range(H) if g[i][L - 1] != "."))
    return words


def main():
    words = sys.stdin.read().split()[:6]
    want = sorted(words)
    best = None
    for perm in permutations(range(6)):
        g = build(words, perm)
        if g is None or extract(g) is None:
            continue
        # 反读校验：网格里读出来的六个词必须正好是输入的多重集合
        if sorted(extract(g)) != want:
            continue
        rows = tuple("".join(r) for r in g)
        if best is None or rows < best:
            best = rows
    print("Impossible" if best is None else "\n".join(best))


main()
