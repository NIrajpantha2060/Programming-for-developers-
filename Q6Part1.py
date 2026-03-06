# Question 6 - Part 1


# Safety probability edges p(u,v)
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

# Capacity edges c(u,v) in trucks/hour
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


def main():

    print("=" * 65)
    print("  QUESTION 6 - PART 1: PROBLEM MODELING")
    print("=" * 65)

    # ── Part A: Network Model ──
    print("\nPart A: Scenario and Network Model")
    print("-" * 65)
    print("""
  The road system is represented as a directed graph G = (V, E).
  Nodes represent important locations (depot and relief centers).
  Edges represent road connections between locations.

  Each edge has:
    - A safety probability p(u,v): how safe that road is
    - A capacity value c(u,v)    : max trucks per hour
    """)

    print("  Nodes:")
    print("    KTM = Kathmandu       (Primary Supply Depot)")
    print("    JA  = Junction A      (Kalanki Chowk)")
    print("    JB  = Junction B      (Koteshwor Chowk)")
    print("    PH  = Patan Hospital  (Relief Center)")
    print("    BS  = Bhaktapur Shelter (Relief Center)")

    print(f"\n  Safety Probability Data:")
    print(f"  {'Source':<10} {'Destination':<15} {'Safety p(e)':>12}")
    print("  " + "-" * 40)
    for u, v, p in safety_edges:
        print(f"  {u:<10} {v:<15} {p:>12.2f}")

    print(f"\n  Capacity Data:")
    print(f"  {'Source':<10} {'Destination':<15} {'Capacity c(e)':>14}")
    print("  " + "-" * 42)
    for u, v, c in capacity_edges:
        print(f"  {u:<10} {v:<15} {c:>14}")

    # ── Question 1(a) ──
    print("\n" + "-" * 65)
    print("Question 1(a): Why Standard Dijkstra Is Not Directly Suitable")
    print("-" * 65)
    print("""
  The classical Dijkstra algorithm is designed to minimize
  the total SUM of edge weights (such as distance or cost).
  It assumes that path weights are additive:

      Total Distance = d(u1,u2) + d(u2,u3) + ... + d(uk-1,uk)

  However in this problem the objective is different.
  We must MAXIMIZE the PRODUCT of safety probabilities:

      Safety = p(u1,u2) x p(u2,u3) x ... x p(uk-1,uk)

  This creates two major issues:

  Issue 1:
      Distance-based optimization uses addition, while
      safety evaluation uses multiplication.
      These are mathematically incompatible operations.

  Issue 2:
      A shorter path does not necessarily mean a safer path.
      Two paths may have the same number of edges but their
      safety probabilities can differ significantly.

  Example:
      Path KTM -> JA -> PH:
      Safety = 0.90 x 0.95 = 0.855

      Path KTM -> JB -> BS:
      Safety = 0.80 x 0.90 = 0.720

  Because of this mismatch between additive and multiplicative
  objectives, directly applying Dijkstra's algorithm is
  inappropriate without modification.
    """)

    # ── Question 1(b) ──
    print("-" * 65)
    print("Question 1(b): Why Using Raw Probabilities Is Incorrect")
    print("-" * 65)
    print("""
  It may seem logical to run Dijkstra in maximum mode using
  probabilities directly as weights. However this approach
  is flawed.

  Dijkstra's correctness depends on the greedy property that
  once a node is selected with the smallest distance, its
  value is final. This works only when:
      - Weights are non-negative
      - Relaxation follows an additive rule:
        dist[v] = min(dist[v], dist[u] + w(u,v))

  In our case the relaxation would be multiplicative:
      safety[v] = max(safety[v], safety[u] x p(u,v))

  Since probabilities are between 0 and 1, multiplying by
  more edges ALWAYS reduces the product. Therefore a path
  that initially looks worse may later become better,
  violating Dijkstra's greedy assumption.

  Thus raw probabilities cannot be directly used
  without transformation.
    """)


if __name__ == "__main__":
    main()