#!/usr/bin/env python3
"""CF150A Win or Freeze 的答案校验器（先手的获胜走法不唯一）。

用法: python3 cf150a.py <input> <output> <expected>

游戏：轮到某人时若无法写出「非平凡因数」则他**获胜**。结论：
    W(q) = false  **仅当** Ω(q) == 2（两个质因子），其余情况先手胜。
    （Ω(q) <= 1：无法移动 => 胜；Ω(q) >= 3：可走到两个质因子的乘积 => 对手必败。）
所以 Ω(q) == 2 时输出 2；否则输出 1，并在 Ω(q) >= 3 时给出一个 Ω(d) == 2 的真因数。

校验：解析输出；若声称先手胜，验证走法合法且走后对手必败；若声称后手胜，验证 Ω(q) 为偶数且 >=2。
"""
import sys


def omega(n):
    cnt = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            n //= d
            cnt += 1
        d += 1
    if n > 1:
        cnt += 1
    return cnt


def first_player_wins(q):
    return omega(q) != 2


def main() -> int:
    q = int(open(sys.argv[1]).read().split()[0])
    out = open(sys.argv[2]).read().split()
    if not out:
        print("输出为空", file=sys.stderr)
        return 1
    if out[0] == "2":
        if len(out) != 1:
            print("声称后手胜时不应有第二行", file=sys.stderr)
            return 1
        if first_player_wins(q):
            print("先手其实能赢", file=sys.stderr)
            return 1
        return 0
    if out[0] != "1":
        print("第一行应为 1 或 2", file=sys.stderr)
        return 1
    if len(out) != 2:
        print("先手胜时必须再输出第一着", file=sys.stderr)
        return 1
    if not first_player_wins(q):
        print("先手其实必败", file=sys.stderr)
        return 1
    move = int(out[1])
    if omega(q) <= 1:                    # 先手无法移动，只能输出 0
        if move != 0:
            print("无可走步时应输出 0", file=sys.stderr)
            return 1
        return 0
    if move <= 1 or move >= q or q % move != 0:
        print(f"{move} 不是 {q} 的非平凡因数", file=sys.stderr)
        return 1
    if omega(move) != 2:                 # 走后轮到对手，对手必须必败（Ω == 2）
        print(f"走法 {move} 走后对手仍能赢", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
