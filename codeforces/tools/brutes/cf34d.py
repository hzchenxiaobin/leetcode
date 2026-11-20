# 独立暴力：递归 DFS 从新首都出发重新定根（与参考解的迭代 BFS 不同）。
import sys
sys.setrecursionlimit(10000)


def main() -> None:
    data = sys.stdin.read().split()
    n, r1, r2 = int(data[0]), int(data[1]), int(data[2])

    adj = [[] for _ in range(n + 1)]
    p = 3
    for i in range(1, n + 1):
        if i == r1:
            continue
        par = int(data[p]); p += 1
        adj[i].append(par)
        adj[par].append(i)

    parent = [0] * (n + 1)
    seen = [False] * (n + 1)

    def dfs(u: int) -> None:
        seen[u] = True
        for v in adj[u]:
            if not seen[v]:
                parent[v] = u
                dfs(v)

    dfs(r2)
    print(" ".join(str(parent[i]) for i in range(1, n + 1) if i != r2), "")


main()
