def edmonds_karp(C, source, sink):
    """Max flow"""

    def bfs(C, F, source, sink):
        queue = [source]
        prev = {source: None}
        while queue:
            u = queue.pop(0)
            for v in range(len(C)):
                if C[u][v] - F[u][v] > 0 and v not in prev:
                    prev[v] = u
                    if v == sink:
                        ret = [v]
                        while ret[-1]:
                            ret.append(prev[ret[-1]])
                        ret.reverse()
                        return list(zip(ret[:-1], ret[1:]))
                    queue.append(v)
        return None

    n = len(C) # C is the capacity matrix
    F = [[0] * n for i in range(n)]
    # residual capacity from u to v is C[u][v] - F[u][v]

    while True:
        path = bfs(C, F, source, sink)
        if not path:
            break
        # traverse path to find smallest capacity
        flow = min(C[u][v] - F[u][v] for u,v in path)
        # traverse path to update flow
        for u,v in path:
            F[u][v] += flow
            F[v][u] -= flow
    return sum(F[source][i] for i in range(n)), F

def min_cut(C, F, source):
    queue = [source]
    cut = []
    visited = {source}
    while queue:
        u = queue.pop(0)
        for v in range(len(C)):
            if v not in visited:
                if C[u][v] - F[u][v] > 0:
                    queue.append(v)
                elif C[u][v] != 0:
                    cut.append((u, v))
    return cut

# g = [
#     [0, 2, 1, 0],
#     [0, 0, 0, 1],
#     [0, 0, 0, 4],
#     [0, 0, 0, 0],
# ]
# print(edmonds_karp(g, 0, 3))
# print(min_cut(g, edmonds_karp(g, 0, 3)[1], 0))