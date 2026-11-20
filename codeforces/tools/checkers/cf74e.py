#!/usr/bin/env python3
"""74E Shift It! 的 checker（构造题，答案不唯一）。

用法: python3 cf74e.py <input> <output> <answer>
校验：
  1. 输出第一行是操作次数 n，0 <= n <= 10000；
  2. 恰好有 n 行操作，每行形如 "L/R/U/D" + 行号或列号（1..6）；
  3. 从初始局面出发依次执行这些操作，最终必须等于
     "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"（行优先读取）。
"""
import sys

N = 6
GOAL = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def shift(board, direction, k):
    """把第 k 行（k 从 0 计）或第 k 列循环移动一格。"""
    b = board[:]
    if direction == 'R':
        for c in range(N):
            b[k * N + (c + 1) % N] = board[k * N + c]
    elif direction == 'L':
        for c in range(N):
            b[k * N + (c - 1) % N] = board[k * N + c]
    elif direction == 'D':
        for r in range(N):
            b[((r + 1) % N) * N + k] = board[r * N + k]
    elif direction == 'U':
        for r in range(N):
            b[((r - 1) % N) * N + k] = board[r * N + k]
    else:
        raise ValueError(direction)
    return b


def main():
    inp = open(sys.argv[1]).read().split()
    out = open(sys.argv[2]).read().split()
    board = list("".join(inp))
    if len(board) != N * N or sorted(board) != sorted(GOAL):
        sys.exit(1)

    if not out:
        sys.exit(1)
    if not out[0].isdigit():
        sys.exit(1)
    n = int(out[0])
    if n > 10000 or len(out) - 1 != n:
        sys.exit(1)
    for op in out[1:]:
        if len(op) != 2 or op[0] not in "LRUD" or op[1] not in "123456":
            sys.exit(1)
        board = shift(board, op[0], int(op[1]) - 1)

    sys.exit(0 if "".join(board) == GOAL else 1)


if __name__ == "__main__":
    main()
