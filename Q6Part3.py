# question no 6 part 3


from collections import defaultdict, deque





capacity_edges = [
    ("KTM", "JA",  10),
    ("KTM", "JB",  15),
    ("JA",  "KTM", 10),
    ("JA",  "PH",   8),
    ("JA",  "BS",   5),
    ("JB",  "KTM", 15),
    ("JB",  "JA",   4),
    ("JB",  "BS",  12),
    ("PH",  "JA",   8),
    ("PH",  "BS",   6),
    ("BS",  "JA",   5),
    ("BS",  "JB",  12),
    ("BS",  "PH",   6),
]

NODES      = ["KTM", "JA", "JB", "PH", "BS"]
NODE_INDEX = {node: i for i, node in enumerate(NODES)}
INDEX_NODE = {i: node for i, node in enumerate(NODES)}


# Question 3(a): Model as Maximum Flow Problem


def question3a():
    """
    Models the throughput problem as a max flow problem.
    """

    print("=" * 65)
    print("  QUESTION 6 - PART 3: MAXIMUM THROUGHPUT ANALYSIS")
    print("=" * 65)

    print("\n" + "-" * 65)
    print("Question 3(a): Maximum Flow Problem Model")
    print("-" * 65)
    print("""
  This is modeled as a Maximum Flow problem where:

      Source (s) = KTM  (Kathmandu - supply depot)
      Sink   (t) = BS   (Bhaktapur Shelter)

  Each directed edge (u,v) has capacity c(u,v)
  representing the maximum trucks per hour.

  Objective:
      Find the maximum number of trucks that can
      travel from KTM to BS simultaneously per hour.

  Capacity constraints:
      0 <= f(u,v) <= c(u,v)  for every edge

  Flow conservation:
      For every node except source and sink:
      Total flow in = Total flow out
    """)

    print("  Edge Capacities relevant to KTM -> BS:")
    print(f"  {'Source':<10} {'Destination':<15} {'Capacity c(e)':>14}")
    print("  " + "-" * 42)
    for u, v, c in capacity_edges:
        print(f"  {u:<10} {v:<15} {c:>14}")


# ─────────────────────────────────────────────────────────────────────
# Edmonds-Karp Implementation
# ─────────────────────────────────────────────────────────────────────

def build_residual_graph():
    """
    Builds residual graph from capacity data.

    Returns:
        capacity: 2D residual capacity matrix
        graph   : adjacency list
    """
    n        = len(NODES)
    capacity = [[0] * n for _ in range(n)]
    graph    = defaultdict(set)

    for u, v, c in capacity_edges:
        i, j = NODE_INDEX[u], NODE_INDEX[v]
        capacity[i][j] += c
        graph[i].add(j)
        graph[j].add(i)

    return capacity, graph


def bfs(source, sink, capacity, graph, n):
    """
    BFS to find augmenting path in residual graph.

    Args:
        source  : source index
        sink    : sink index
        capacity: residual capacity matrix
        graph   : adjacency list
        n       : number of nodes
    Returns:
        parent array if path found, None otherwise
    """
    parent  = [-1] * n
    visited = [False] * n
    visited[source] = True
    queue   = deque([source])

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if not visited[v] and capacity[u][v] > 0:
                visited[v] = True
                parent[v]  = u
                if v == sink:
                    return parent
                queue.append(v)
    return None


def edmonds_karp(source_name, sink_name):
    """
    Edmonds-Karp maximum flow algorithm.

    Steps per iteration:
        1. BFS to find shortest augmenting path
        2. Find bottleneck capacity along path
        3. Push flow through path
        4. Update residual graph capacities
        5. Repeat until no augmenting path found

    Complexity: O(V x E^2)

    Args:
        source_name: source node name
        sink_name  : sink node name
    Returns:
        max_flow      : total maximum flow
        steps         : list of augmentation steps
        final_capacity: residual graph after algorithm
    """
    capacity, graph = build_residual_graph()
    source   = NODE_INDEX[source_name]
    sink     = NODE_INDEX[sink_name]
    n        = len(NODES)
    max_flow = 0
    steps    = []
    step_num = 1

    while True:
        parent = bfs(source, sink, capacity, graph, n)
        if parent is None:
            break

        # Find bottleneck
        path_flow  = float('inf')
        path_nodes = []
        v = sink

        while v != source:
            u         = parent[v]
            path_flow = min(path_flow, capacity[u][v])
            path_nodes.append(INDEX_NODE[v])
            v = u
        path_nodes.append(INDEX_NODE[source])
        path_nodes.reverse()

        # Update residual capacities
        changes = []
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            changes.append(
                f"  {INDEX_NODE[u]}->{INDEX_NODE[v]}: "
                f"forward -{path_flow}, backward +{path_flow}"
            )
            v = u

        max_flow += path_flow
        steps.append({
            "step":    step_num,
            "path":    " -> ".join(path_nodes),
            "flow":    path_flow,
            "total":   max_flow,
            "changes": changes
        })
        step_num += 1

    return max_flow, steps, capacity


# ─────────────────────────────────────────────────────────────────────
# Helper: find reachable nodes from source in residual graph
# ─────────────────────────────────────────────────────────────────────

def find_reachable(source_name, final_capacity):
    """
    BFS on final residual graph to find nodes reachable from source.
    These nodes form the S-side of the minimum cut.

    Args:
        source_name    : source node name
        final_capacity : residual capacity matrix after Edmonds-Karp
    Returns:
        set of reachable node names
    """
    source  = NODE_INDEX[source_name]
    n       = len(NODES)
    visited = [False] * n
    queue   = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and final_capacity[u][v] > 0:
                visited[v] = True
                queue.append(v)

    return {INDEX_NODE[i] for i in range(n) if visited[i]}


# Question 3(b): Display Edmonds-Karp Steps


def question3b(steps):
    """
    Displays each augmenting path step.
    """

    print("\n" + "-" * 65)
    print("Question 3(b): Edmonds-Karp Algorithm Execution")
    print("-" * 65)
    print("""
  For each step of the algorithm:
      1. Augmenting path found in residual graph
      2. Amount of flow pushed through that path
      3. Updated residual graph after augmenting
    """)

    for s in steps:
        print(f"  Step {s['step']}:")
        print(f"    Augmenting Path     : {s['path']}")
        print(f"    Flow Pushed         : {s['flow']} trucks/hr")
        print(f"    Cumulative Flow     : {s['total']} trucks/hr")
        print(f"    Residual Graph Updates:")
        for change in s["changes"]:
            print(f"     {change}")
        print()


# Question 3(c): Max Flow Value + Min Cut Proof  ← FIXED


def question3c(max_flow, final_capacity):
    """
    States final max flow and proves min cut equals
    max flow using the actual residual graph analysis.

    FIXED: Min-cut is correctly identified as
    S = {KTM, JA, JB, PH}, T = {BS}
    with cut capacity = JA->BS(5) + JB->BS(12) + PH->BS(6) = 23
    which equals max flow = 23. ✓
    """

    print("-" * 65)
    print("Question 3(c): Maximum Flow Value and Min-Cut Theorem")
    print("-" * 65)

    # Dynamically find the actual min cut from residual graph
    S_set = find_reachable("KTM", final_capacity)
    T_set = set(NODES) - S_set

    # Find original capacities for cut edges (S -> T)
    original_cap = {(u, v): c for u, v, c in capacity_edges}
    cut_edges = []
    cut_capacity = 0
    for u in S_set:
        for v in T_set:
            if (u, v) in original_cap:
                cut_edges.append((u, v, original_cap[(u, v)]))
                cut_capacity += original_cap[(u, v)]

    print(f"""
  Final Maximum Flow (KTM -> BS) = {max_flow} trucks/hour

  Identifying the Minimum s-t Cut:
  ─────────────────────────────────────────────────────────
  After running Edmonds-Karp, we perform BFS on the final
  residual graph to find all nodes reachable from KTM.

      S = nodes reachable from KTM in residual graph
        = {sorted(S_set)}

      T = nodes NOT reachable from KTM in residual graph
        = {sorted(T_set)}

  Edges crossing the cut from S to T (in original graph):""")

    for u, v, c in cut_edges:
        print(f"      {u} -> {v} : capacity = {c}")

    print(f"""
  Min-Cut Capacity = {' + '.join(f'{c}' for _, _, c in cut_edges)} = {cut_capacity} trucks/hour

  Max-Flow Min-Cut Theorem Verification:
  ─────────────────────────────────────────────────────────
      Maximum Flow     = {max_flow} trucks/hour
      Min-Cut Capacity = {cut_capacity} trucks/hour
      Match            = {max_flow == cut_capacity} ✓

  Since Maximum Flow ({max_flow}) = Min-Cut Capacity ({cut_capacity}),
  the Max-Flow Min-Cut theorem is demonstrated for this
  emergency supply logistics network. ✓

  Interpretation:
      The bottleneck in the network is the set of edges
      directly entering BS (Bhaktapur Shelter).
      No matter how trucks are routed from KTM,
      the maximum throughput is capped at {max_flow} trucks/hour
      by these incoming edges to BS.
    """)


def main():
    question3a()

    max_flow, steps, final_capacity = edmonds_karp("KTM", "BS")

    question3b(steps)
    question3c(max_flow, final_capacity)   # ← now passes final_capacity

    print("=" * 65)


if __name__ == "__main__":
    main()