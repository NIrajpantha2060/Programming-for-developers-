# question no 6 part 2

import math
import heapq
from collections import defaultdict



# Network Data


safety_edges = [
    ("KTM", "JA",  0.90),
    ("KTM", "JB",  0.80),
    ("JA",  "KTM", 0.90),
    ("JA",  "PH",  0.95),
    ("JA",  "BS",  0.70),
    ("JB",  "KTM", 0.80),
    ("JB",  "JA",  0.60),
    ("JB",  "BS",  0.90),
    ("PH",  "JA",  0.95),
    ("PH",  "BS",  0.85),
    ("BS",  "JA",  0.70),
    ("BS",  "JB",  0.90),
    ("BS",  "PH",  0.85),
]

NODES = ["KTM", "JA", "JB", "PH", "BS"]



# Question 2(a): Logarithmic Transformation
# As described in documentation:
# w(e) = -log(p(e))


def show_transformation():
    """
    Shows the logarithmic transformation table
    exactly as described in the documentation.
    w(e) = -log(p(e))
    """

    print("=" * 65)
    print("  QUESTION 6 - PART 2: SAFEST PATH ALGORITHM ADAPTATION")
    print("=" * 65)

    print("\n" + "-" * 65)
    print("Question 2(a): Logarithmic Weight Transformation")
    print("-" * 65)
    print("""
  To solve the multiplicative safety problem, we apply
  a logarithmic transformation.

  For each edge with safety probability p(e),
  define a new weight:

      w(e) = -log(p(e))

  Why This Works:
      Since p(e) is between 0 and 1:
          log(p(e)) <= 0
      Negating it makes:
          -log(p(e)) >= 0

      This satisfies Dijkstra's requirement
      for non-negative weights.

  Maximizing the product:
      p(e1) x p(e2) x ... x p(ek)

  is equivalent to maximizing:
      log(p(e1)) + log(p(e2)) + ... + log(p(ek))

  which is the same as minimizing:
      -log(p(e1)) + -log(p(e2)) + ... + -log(p(ek))

  Therefore after transformation we can safely apply
  Dijkstra's shortest-path algorithm.
    """)

    # Transformation table exactly as in documentation
    print("  Transformed Edge Weights:")
    print(f"  {'Edge':<15} {'Probability':>12} {'Transformed Weight w(e)':>25}")
    print("  " + "-" * 55)
    for u, v, p in safety_edges:
        w = -math.log(p)
        print(f"  {u+' -> '+v:<15} {p:>12.2f} {w:>25.4f}")

    # Exact values from documentation
    print("""
  Example values from documentation:
      p = 0.90  ->  w = 0.1054
      p = 0.80  ->  w = 0.2231
      p = 0.95  ->  w = 0.0513
      p = 0.70  ->  w = 0.3567
      p = 0.60  ->  w = 0.5108
      p = 0.85  ->  w = 0.1625

  After applying this transformation, the problem becomes
  a standard shortest-path problem with non-negative weights.
    """)


# Question 2(b): Adapted Dijkstra Implementation
# As described in documentation:
# - Min-heap priority queue
# - Transformed weights w(e) = -log(p(e))
# - Standard Dijkstra relaxation using additive weights


def build_graph(edges):
    """
    Builds adjacency list with transformed weights.
    w(e) = -log(p(e)) as per documentation.

    Args:
        edges: list of (u, v, probability) tuples
    Returns:
        graph: dict of {node: [(weight, neighbor)]}
    """
    graph = defaultdict(list)
    for u, v, p in edges:
        w = -math.log(p)    # transformation from documentation
        graph[u].append((w, v))
    return graph


def reconstruct_path(prev, source, target):
    """
    Reconstructs path from source to target.

    Args:
        prev  : dict of previous nodes
        source: start node
        target: end node
    Returns:
        list of nodes in path
    """
    path    = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    if path and path[0] == source:
        return path
    return []


def dijkstra_safest(source, edges):
    """
    Adapted Dijkstra using -log transformation.

    As described in documentation:
    - Uses min-heap priority queue
    - Transformed weights w(e) = -log(p(e))
    - Standard additive RELAX operation:
      dist[v] = min(dist[v], dist[u] + w(u,v))

    This guarantees the path with smallest transformed sum
    corresponds to the path with highest safety probability.

    Complexity: O((V + E) log V)

    Args:
        source: starting node
        edges : list of (u, v, probability) tuples
    Returns:
        dist  : minimum transformed distances
        prev  : previous nodes for path reconstruction
        safety: actual safety probabilities
    """
    graph = build_graph(edges)

    dist = {node: float('inf') for node in NODES}
    dist[source] = 0.0
    prev = {node: None for node in NODES}

    # Min-heap priority queue as described in documentation
    heap = [(0.0, source)]

    while heap:
        d_u, u = heapq.heappop(heap)

        if d_u > dist[u]:
            continue

        for w, v in graph[u]:
            # Standard Dijkstra RELAX operation
            # additive on transformed weights
            candidate = dist[u] + w
            if candidate < dist[v]:
                dist[v] = candidate
                prev[v] = u
                heapq.heappush(heap, (candidate, v))

    # Convert back: safety = exp(-dist)
    safety = {}
    for node in NODES:
        if dist[node] == float('inf'):
            safety[node] = 0.0
        else:
            safety[node] = round(math.exp(-dist[node]), 4)

    return dist, prev, safety


def show_implementation():
    """
    Runs adapted Dijkstra and displays results.
    """

    print("-" * 65)
    print("Question 2(b): Adapted Algorithm Implementation")
    print("-" * 65)
    print("""
  The adapted solution uses:
      - A min-heap priority queue
      - Transformed weights w(e) = -log(p(e))
      - Standard Dijkstra relaxation using additive weights

  The RELAX operation becomes:
      dist[v] = min(dist[v], dist[u] + (-log(p(u,v))))

  This guarantees that the path with the smallest
  transformed sum corresponds to the path with the
  highest safety probability.

  Complexity: O((V + E) log V)
  The logarithmic transformation does not increase
  time complexity significantly.
    """)

    dist, prev, safety = dijkstra_safest("KTM", safety_edges)

    print("  Results - Safest Paths from KTM:")
    print(f"  {'Node':<8} {'Transformed Dist':>18} {'Safety Prob':>13} {'Path'}")
    print("  " + "-" * 65)
    for node in NODES:
        if node == "KTM":
            continue
        path = reconstruct_path(prev, "KTM", node)
        pstr = " -> ".join(path) if path else "No path"
        print(f"  {node:<8} {dist[node]:>18.4f} {safety[node]:>13.4f}   {pstr}")

    # Verify example from documentation
    print()
    print("  Verification - Path KTM -> JA -> PH:")
    print(f"    Safety = 0.90 x 0.95 = {0.90 * 0.95:.4f}")
    w = -math.log(0.90) + (-math.log(0.95))
    print(f"    -log(0.90) + -log(0.95) = {w:.4f}")
    print(f"    exp(-{w:.4f}) = {math.exp(-w):.4f}")

    return dist, prev, safety



# Question 2(c): Proof of Correctness
# As described in documentation


def show_proof():
    """
    Proves correctness exactly as described in documentation.
    """

    print("\n" + "-" * 65)
    print("Question 2(c): Proof of Correctness")
    print("-" * 65)
    print("""
  Claim:
      The adapted algorithm correctly finds the path
      with the maximum product of probabilities.

  Proof:

  Step 1 - Non-negativity:
      For any p(e) in (0, 1]:
          log(p(e)) <= 0
          -log(p(e)) >= 0
      All transformed weights w(e) >= 0
      Dijkstra's non-negativity requirement satisfied. ✓

  Step 2 - Equivalence of objectives:
      Maximizing: p(e1) x p(e2) x ... x p(ek)

      Taking log (monotonically increasing):
          max[ log(p(e1)) + log(p(e2)) + ... ]

      Negating (flips max to min):
          min[ -log(p(e1)) + -log(p(e2)) + ... ]
          = min[ w(e1) + w(e2) + ... ]

      This is exactly the standard shortest path
      objective. ✓

  Step 3 - Dijkstra correctness applies:
      Since all weights are non-negative and
      relaxation is additive, Dijkstra correctly
      finds the minimum sum path. ✓

  Step 4 - Converting back:
      After finding minimum transformed distance d*:
          safety = exp(-d*)
      This gives the maximum safety probability. ✓

  Conclusion:
      The path that minimizes sum of -log(p(e))
      is the same path that maximizes product of p(e).
      Therefore the adapted algorithm is correct. QED ✓
    """)


def main():
    show_transformation()
    show_implementation()
    show_proof()
    print("=" * 65)


if __name__ == "__main__":
    main()