"""CF71E 特殊评测校验器：python3 check.py <input> <output> <answer>
忽略 expected answer，独立判定（NO 时用回溯）并校验 YES 输出的等式。"""
import sys

SYMS = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
        "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
        "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
        "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
        "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
        "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
        "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
        "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
        "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
        "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
NUM = {s: i + 1 for i, s in enumerate(SYMS)}


def solvable(n, k, a, b):
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

    return rec(0, 0)


def main():
    inp, out = sys.argv[1], sys.argv[2]
    data = open(inp).read().split()
    n, k = int(data[0]), int(data[1])
    src = data[2:2 + n]
    dst = data[2 + n:2 + n + k]
    a = [NUM[x] for x in src]
    b = [NUM[x] for x in dst]

    lines = [l.strip() for l in open(out).read().split("\n") if l.strip()]
    assert lines, "输出为空"
    if lines[0] == "NO":
        assert len(lines) == 1, "NO 之后不应再有内容"
        assert not solvable(n, k, a, b), "实际有解，却输出 NO"
        return 0
    assert lines[0] == "YES", f"首行非法: {lines[0]!r}"
    eqs = lines[1:]
    assert len(eqs) == k, f"等式行数 {len(eqs)} != k={k}"
    used, got = [], []
    for e in eqs:
        if "->" not in e:
            raise AssertionError(f"缺少箭头: {e!r}")
        left, y = e.split("->", 1)
        assert y in NUM, f"未知元素 {y!r}"
        xs = left.split("+")
        assert xs and all(x in NUM for x in xs), f"左部含未知元素: {e!r}"
        s = sum(NUM[x] for x in xs)
        assert s == NUM[y], f"不配平: {e}（{s} != {NUM[y]}）"
        used += xs
        got.append(y)
    assert sorted(used) == sorted(src), "初始原子使用情况与输入不一致"
    assert sorted(got) == sorted(dst), "目标原子与输入不一致"
    return 0


sys.exit(main())
