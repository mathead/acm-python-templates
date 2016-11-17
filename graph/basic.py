from collections import deque, defaultdict
from copy import deepcopy
from heapq import *

# graph = defaultdict(dict, {})
# graph['jmeno uzlu'] = ['jmenu kam vede hrana']
# graph['jmeno uzlu'] = {'jmenu kam vede hrana': cena}

def BFS(gr, s):
    """ Breadth first search 
    Returns a list of nodes that are "findable" from s """
    prev = {s:None}
    q = deque([s])
    while q:
        node = q.popleft()
        for each in gr[node]:
            if each not in prev:
                prev[each] = node
                q.append(each)
    return prev

def shortest_hops(gr, s):
    """ Finds the shortest number of hops required
    to reach a node from s. Returns a dict with mapping:
    destination node from s -> no. of hops
    """
    dist = {}
    q = deque([s])
    explored = {s}
    for n in gr.nodes():
        if n == s: dist[n] = 0
        else: dist[n] = float('inf')
    while len(q) != 0:
        node = q.popleft()
        for each in gr[node]:
            if each not in explored:
                explored.add(each)
                q.append(each)
                dist[each] = dist[node] + 1
    return dist

def undirected_connected_components(gr):
    """ Returns a list of connected components
    in an undirected graph """
    explored = set([])
    con_components = []
    for node in gr:
        if node not in explored:
            reachable = BFS(gr, node).keys()
            con_components.append(reachable)
            explored |= reachable
    return con_components

def DFS(gr, s, path=None):
    """ Depth first search 
    Returns a list of nodes "findable" from s """
    if path is None:
        path = set()
    if s in path: 
        return path
    path.add(s)
    for each in gr[s]:
        if each not in path:
            DFS(gr, each, path)
    return path

def topological_ordering(digr_ori):
    """ Returns a topological ordering for a 
    acyclic directed graph """

    def find_sink_node(digr):
        """ Finds a sink node (node with all incoming arcs) 
        in the directed graph. Valid for a acyclic graph only """
        # first node is taken as a default
        node = next(iter(digr.keys()))
        while digr[node]:
            node = digr[node][0]
        return node

    digr = deepcopy(digr_ori)
    ordering = []
    n = len(digr)
    while n > 0:
        sink_node = find_sink_node(digr)
        ordering.append((sink_node, n))
        del digr[sink_node]
        n -= 1
    return ordering


def transposed(digr):
    """ Returns the transpose of directed graph
    with edges reversed and nodes same """
    trans = {}
    for n in digr:
        for edge in n:
            trans[edge] = trans.get(edge, []) + [n]
    return trans

def directed_connected_components(digr):
    """ Returns a list of strongly connected components
    in a directed graph using Kosaraju's two pass algorithm """

    def outer_dfs(digr, node, explored, path):
        if node in path or node in explored: 
            return False
        path.append(node)
        for each in digr[node]:
            if each not in path or each not in explored:
                outer_dfs(digr, each, explored, path)

    def DFS_loop(digr):
        """ Core DFS loop used to find strongly connected components
        in a directed graph """
        explored = set([]) # list for keeping track of nodes explored
        finishing_times = [] # list for adding nodes based on their finishing times
        for node in digr:
            if node not in explored:
                leader_node = node
                inner_DFS(digr, node, explored, finishing_times)
        return finishing_times 

    def inner_DFS(digr, node, explored, finishing_times):
        """ Inner DFS used in DFS loop method """
        explored.add(node) # mark explored
        for each in digr[node]:
            if each not in explored:
                inner_DFS(digr, each, explored, finishing_times)
        # adds nodes based on increasing order of finishing times
        finishing_times.append(node) 

    finishing_times = DFS_loop(transposed(digr))
    # use finishing_times in descending order
    explored, connected_components = [], []
    for node in finishing_times[::-1]:
        component = []
        outer_dfs(digr, node, explored, component)
        if component:
            explored += component
            connected_components.append(component)
    return connected_components

def shortest_path(gr, fro, to):
    """ Finds the shortest path from s to every other vertex findable
    from s using Dijkstra's algorithm in O(mlogn) time. Uses heaps
    for super fast implementation """

    closed = set()
    dist = {fro:0}
    heap = [(0, fro)]
    prev = {}

    while heap:
        curd, cur = heappop(heap)
        if cur == to:
            return curd, prev
        if cur in closed:
            continue
        closed.add(cur)

        for n, cost in gr[cur].items():
            if n in closed:
                continue
            if curd + cost < dist.get(n, float('inf')):
                dist[n] = curd + cost
                prev[n] = cur
                heappush(heap, (dist[n], n))

# g = defaultdict(dict, {
#     0: {1: 2, 2: 1, 3: 10},
#     1: {3: 1},
#     2: {3: 4},
# })
# print(shortest_path(g, 0, 3))

def minimum_spanning_tree(gr):
    weight = 0 
    heap = []
    tree = []

    start = next(iter(gr.keys()))
    connected = {start}

    for to, cost in gr[start].items():
        heap.append((cost, start, to))
    heapify(heap)

    while heap:
        cost, fro, to = heappop(heap)
        if to in connected:
            continue
        connected.add(to)
        tree.append((fro, to))
        weight += cost
        for n, cost in gr[to].items():
            heappush(heap, (cost, to, n))
    return weight, tree

# g = defaultdict(dict, {
#     0: {1: 2, 2: 1},
#     1: {3: 1, 0: 2},
#     2: {3: 4, 0: 1},
#     3: {2: 4, 1: 1},
# })
# print(minimum_spanning_tree(g))