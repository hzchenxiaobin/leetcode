#!/usr/bin/env python3
"""CF150A Win or Freeze 的答案校验器（先手的获胜走法不唯一）。

用法: python3 cf150a.py <input> <output> <expected>

游戏：轮到某人时若无法写出「非平凡因数」则他**获胜**。由归纳可知
    W(q) = (q 的质因子个数 Ω(q) 为奇数)，其中 Ω(1)=Ω(素数)=0/1 都算"无法移动 => 胜"。
q=1 与素数：先手无法移动 => 先手胜，第一着输出 0。
Ω(q) 奇数且 >=2：先手胜，须给出一个使 Ω 变为偶数的真因数（非平凡因数）。
Ω(q) 偶数且 >=2：先手必败，输出 2。

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
    if q == 1:
        return True
    return omega(q) % 2 == 1


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
    if q == 1 or omega(q) == 1:          # 先手无法移动，只能输出 0
        if move != 0:
            print("无可走步时应输出 0", file=sys.stderr)
            return 1
        return 0
    if move <= 1 or move >= q or q % move != 0:
        print(f"{move} 不是 {q} 的非平凡因数", file=sys.stderr)
        return 1
    if first_player_wins(move):          # 走后轮到对手，对手应必败
        print(f"走法 {move} 走后对手仍能赢", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
