import sys
from collections import deque


class Edge:
    def __init__(self, to: int, rev: int, cap: int):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.flow = 0


class FlowNetwork:
    def __init__(self, n: int):
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        fwd = Edge(v, len(self.adj[v]), cap)
        bwd = Edge(u, len(self.adj[u]), 0)
        self.adj[u].append(fwd)
        self.adj[v].append(bwd)

    def edmonds_karp(self, s: int, t: int) -> int:
        total = 0
        n = len(self.adj)
        parent_edge = [-1] * n

        while True:
            parent_edge = [-1] * n
            dist = [-1] * n
            dist[s] = 0
            q = deque([s])

            while q:
                u = q.popleft()
                for e in self.adj[u]:
                    if e.cap > 0 and dist[e.to] == -1:
                        dist[e.to] = dist[u] + 1
                        parent_edge[e.to] = (u, e)
                        if e.to == t:
                            q.clear()
                            break
                        q.append(e.to)

            if dist[t] == -1:
                break

            bottleneck = float("inf")
            v = t
            while v != s:
                u, e = parent_edge[v]
                bottleneck = min(bottleneck, e.cap)
                v = u

            v = t
            while v != s:
                u, e = parent_edge[v]
                rev = self.adj[e.to][e.rev]
                e.cap -= bottleneck
                e.flow += bottleneck
                rev.cap += bottleneck
                rev.flow -= bottleneck
                v = u

            total += bottleneck

        return total


def solve_case(nk: int, np_: int, demands: list[int], problems: list[list[int]]) -> tuple[bool, list[list[int]]]:
    total_demand = sum(demands)
    s = 0
    cat_base = 1
    prob_base = cat_base + nk
    t = prob_base + np_
    n = t + 1

    net = FlowNetwork(n)

    for i in range(nk):
        net.add_edge(s, cat_base + i, demands[i])

    for j in range(np_):
        net.add_edge(prob_base + j, t, 1)
        for cat in problems[j]:
            net.add_edge(cat_base + cat - 1, prob_base + j, 1)

    max_flow = net.edmonds_karp(s, t)
    if max_flow != total_demand:
        return False, []

    assignment = [[] for _ in range(nk)]
    for i in range(nk):
        u = cat_base + i
        for e in net.adj[u]:
            if prob_base <= e.to < prob_base + np_ and e.flow > 0:
                assignment[i].append(e.to - prob_base + 1)

    for i in range(nk):
        assignment[i].sort()

    return True, assignment


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    it = iter(data)
    out = []

    while True:
        nk = int(next(it))
        np_ = int(next(it))
        if nk == 0 and np_ == 0:
            break

        demands = [int(next(it)) for _ in range(nk)]
        problems = []
        for _ in range(np_):
            k = int(next(it))
            cats = [int(next(it)) for _ in range(k)]
            problems.append(cats)

        ok, assignment = solve_case(nk, np_, demands, problems)
        if ok:
            out.append("1")
            for probs in assignment:
                out.append(" ".join(map(str, probs)))
        else:
            out.append("0")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
