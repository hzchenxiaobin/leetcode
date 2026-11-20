#!/usr/bin/env python3
"""CF23C checker：校验 YES/NO 判定、选中个数、编号范围/唯一性/升序，以及两条不等式。"""
import sys
from itertools import combinations


def fail(msg):
    print("CHECKER FAIL:", msg)
    sys.exit(1)


def feasible(n, boxes):
    total_a = sum(a for a, o in boxes)
    total_o = sum(o for a, o in boxes)
    for comb in combinations(range(len(boxes)), n):
        sa = sum(boxes[i][0] for i in comb)
        so = sum(boxes[i][1] for i in comb)
        if 2 * sa >= total_a and 2 * so >= total_o:
            return True
    return False


def main():
    inp_path, out_path = sys.argv[1], sys.argv[2]
    expected = sys.stdin.read() if len(sys.argv) > 3 else ""

    raw = open(inp_path).read().split()
    pos = 0
    T = int(raw[pos]); pos += 1
    tests = []
    for _ in range(T):
        n = int(raw[pos]); pos += 1
        boxes = []
        for _ in range(2 * n - 1):
            a = int(raw[pos]); o = int(raw[pos + 1]); pos += 2
            boxes.append((a, o))
        tests.append((n, boxes))

    lines = [ln.rstrip() for ln in open(out_path).read().replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()

    idx = 0
    for t, (n, boxes) in enumerate(tests):
        if idx >= len(lines):
            fail(f"test {t+1}: missing answer")
        verdict = lines[idx].strip()
        idx += 1
        if verdict == "NO":
            # 若断言无解，必须真的无解；本题的构造证明说明永远有解，因此这里直接判错。
            if n <= 5 and feasible(n, boxes):
                fail(f"test {t+1}: said NO but a valid subset exists")
            if n > 5:
                fail(f"test {t+1}: NO is not accepted for this constructive problem")
            continue
        if verdict != "YES":
            fail(f"test {t+1}: first line must be YES or NO, got {verdict!r}")
        if idx >= len(lines):
            fail(f"test {t+1}: missing index line")
        parts = lines[idx].split()
        idx += 1
        if len(parts) != n:
            fail(f"test {t+1}: expected {n} indices, got {len(parts)}")
        ids = []
        for p in parts:
            try:
                v = int(p)
            except ValueError:
                fail(f"test {t+1}: {p!r} is not an integer")
            if not (1 <= v <= 2 * n - 1):
                fail(f"test {t+1}: index {v} out of range")
            ids.append(v)
        if len(set(ids)) != n:
            fail(f"test {t+1}: duplicated indices")
        if ids != sorted(ids):
            fail(f"test {t+1}: indices are not ascending")
        total_a = sum(a for a, o in boxes)
        total_o = sum(o for a, o in boxes)
        sa = sum(boxes[i - 1][0] for i in ids)
        so = sum(boxes[i - 1][1] for i in ids)
        if 2 * sa < total_a:
            fail(f"test {t+1}: apples {sa} < half of {total_a}")
        if 2 * so < total_o:
            fail(f"test {t+1}: oranges {so} < half of {total_o}")

    if idx != len(lines):
        fail(f"extra output lines: {len(lines) - idx}")

    # 与标准答案的 YES/NO 判定一致（标准答案只给出某一种合法方案）
    exp_lines = [ln.strip() for ln in expected.replace("\r\n", "\n").split("\n") if ln.strip()]
    if exp_lines:
        exp_verdicts = [ln for ln in exp_lines if ln in ("YES", "NO")]
        if len(exp_verdicts) != T:
            fail(f"expected-answer verdict count {len(exp_verdicts)} != {T}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
