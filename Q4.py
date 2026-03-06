# question no 4


# TASK 1: Model the Input Data

# Hourly demand data for District A, B, C (in kWh)
demand_data = {
    6:  {"A": 20, "B": 15, "C": 25},
    7:  {"A": 22, "B": 16, "C": 28},
    8:  {"A": 25, "B": 18, "C": 30},
    9:  {"A": 28, "B": 20, "C": 32},
    10: {"A": 30, "B": 22, "C": 35},
    11: {"A": 32, "B": 24, "C": 38},
    12: {"A": 35, "B": 26, "C": 40},
    13: {"A": 33, "B": 25, "C": 38},
    14: {"A": 30, "B": 23, "C": 36},
    15: {"A": 28, "B": 21, "C": 34},
    16: {"A": 26, "B": 20, "C": 32},
    17: {"A": 30, "B": 22, "C": 35},
    18: {"A": 35, "B": 25, "C": 40},
    19: {"A": 38, "B": 28, "C": 42},
    20: {"A": 40, "B": 30, "C": 45},
    21: {"A": 35, "B": 27, "C": 40},
    22: {"A": 28, "B": 22, "C": 35},
    23: {"A": 20, "B": 15, "C": 25},
}

# Energy source properties: id, type, max capacity/hr, available window, cost per kWh
energy_sources = [
    {"id": "S1", "type": "Solar",  "capacity": 50, "start": 6,  "end": 18, "cost": 1.0},
    {"id": "S2", "type": "Hydro",  "capacity": 40, "start": 0,  "end": 24, "cost": 1.5},
    {"id": "S3", "type": "Diesel", "capacity": 60, "start": 17, "end": 23, "cost": 3.0},
]

DISTRICTS  = ["A", "B", "C"]
TOLERANCE  = 0.10   # ±10% flexibility as described in Task 4
HOURS      = sorted(demand_data.keys())


# ─────────────────────────────────────────────────────────────────────
# TASK 3: Greedy Source Prioritization
# ─────────────────────────────────────────────────────────────────────

def get_available_sources(hour):
    """
    Returns energy sources available at the given hour,
    sorted by cost ascending (cheapest first - Greedy approach).

    Priority order: Solar (Rs.1.0) -> Hydro (Rs.1.5) -> Diesel (Rs.3.0)

    Args:
        hour: integer hour value (0-23)

    Returns:
        List of available source dicts sorted by cost (cheapest first)
    """
    available = []
    for source in energy_sources:
        if source["start"] <= hour < source["end"]:
            available.append(dict(source))  # copy dict to avoid modifying original

    # Greedy: sort by cheapest first to minimize total cost
    return sorted(available, key=lambda s: s["cost"])


# ─────────────────────────────────────────────────────────────────────
# TASK 2: Hourly Allocation using Dynamic Programming + Greedy
# ─────────────────────────────────────────────────────────────────────

def allocate_hour(hour, demands):
    """
    Allocates energy to each district for a given hour.

    Dynamic Programming: remaining_capacity tracks available source state
                         across all district allocations within the hour.
    Greedy Strategy    : within each hour, picks cheapest source first.

    Args:
        hour   : integer hour value
        demands: dict {"A": kWh, "B": kWh, "C": kWh}

    Returns:
        results dict with per-district allocation details,
        and hour_cost (total cost for this hour)
    """
    available_sources = get_available_sources(hour)

    # DP state: remaining capacity of each source shared across districts
    remaining_capacity = {s["id"]: s["capacity"] for s in available_sources}

    # Track allocation per district per source
    allocation = {d: {"S1": 0, "S2": 0, "S3": 0} for d in DISTRICTS}

    hour_cost = 0.0
    results   = {}

    for district in DISTRICTS:
        demand         = demands[district]
        min_acceptable = demand * (1 - TOLERANCE)  # 0.9 x demand (Task 4)
        fulfilled      = 0.0

        # Greedy: use cheapest source first, then next cheapest
        for source in available_sources:
            if fulfilled >= min_acceptable:
                break

            # How much this source can give to this district
            can_supply = min(demand - fulfilled, remaining_capacity[source["id"]])

            if can_supply > 0:
                allocation[district][source["id"]] = can_supply

                # Update DP state: reduce remaining capacity for next district
                remaining_capacity[source["id"]] -= can_supply
                fulfilled                        += can_supply

                # Accumulate cost for this hour
                hour_cost += can_supply * source["cost"]

        total_supplied = sum(allocation[district].values())
        pct_met        = round((total_supplied / demand) * 100, 1) if demand > 0 else 0.0
        is_satisfied   = pct_met >= (1 - TOLERANCE) * 100

        results[district] = {
            "solar":  allocation[district]["S1"],
            "hydro":  allocation[district]["S2"],
            "diesel": allocation[district]["S3"],
            "total":  total_supplied,
            "demand": demand,
            "pct":    pct_met,
            "ok":     is_satisfied
        }

    return results, hour_cost


# ─────────────────────────────────────────────────────────────────────
# TASK 5 & 6: Output Table + Cost and Resource Analysis
# ─────────────────────────────────────────────────────────────────────

def run_smart_grid():
    """
    Runs the full smart grid simulation across all hours.

    Dynamic Programming (dp[] array):
        dp[i] = minimum cumulative cost from hour 0 up to hour i
        dp[0] = 0 (no cost before simulation starts)
        dp[i+1] = dp[i] + cost of hour i   (optimal substructure)

    Displays allocation table and cost/resource analysis report.
    """

    # ── DP array: dp[i] = cumulative minimum cost up to hour index i ──
    dp         = [0.0] * (len(HOURS) + 1)
    hour_costs = {}   # stores cost per hour for display

    # Accumulators for Task 6 analysis
    total_solar  = 0.0
    total_hydro  = 0.0
    total_diesel = 0.0
    diesel_log   = []   # stores (hour, district, amount) for diesel usage
    all_results  = {}   # stores results per hour for printing

    # ── Run allocation and build dp[] array ──
    for idx, hour in enumerate(HOURS):
        results, hour_cost = allocate_hour(hour, demand_data[hour])

        # DP transition: accumulate minimum cost hour by hour
        dp[idx + 1] = dp[idx] + hour_cost

        hour_costs[hour]  = hour_cost
        all_results[hour] = results

        for district in DISTRICTS:
            r = results[district]
            total_solar   += r["solar"]
            total_hydro   += r["hydro"]
            total_diesel  += r["diesel"]
            if r["diesel"] > 0:
                diesel_log.append((hour, district, r["diesel"]))

    # ── Print allocation table ──
    print("=" * 90)
    print("        SMART ENERGY GRID - HOURLY ALLOCATION TABLE (Nepal)")
    print("=" * 90)
    print(f"{'Hour':<6} {'District':<10} {'Solar(kWh)':>11} {'Hydro(kWh)':>11} "
          f"{'Diesel(kWh)':>12} {'Total':>7} {'Demand':>8} {'% Met':>7}  {'Status':<6}  {'Cumulative Cost(Rs.)'}")
    print("-" * 90)

    for idx, hour in enumerate(HOURS):
        results = all_results[hour]
        for district in DISTRICTS:
            r      = results[district]
            status = "OK" if r["ok"] else "UNMET"

            # Show cumulative DP cost only on first district row of each hour
            dp_display = f"Rs. {dp[idx + 1]:.2f}" if district == "A" else ""

            print(f"  {hour:02d}   {district:<10} {r['solar']:>11} {r['hydro']:>11} "
                  f"{r['diesel']:>12} {r['total']:>7} {r['demand']:>8} "
                  f"{r['pct']:>6}%   {status:<6}  {dp_display}")

        print()  # blank line between hours for readability

    print("=" * 90)

    # ── Print DP array summary ──
    print("\nDYNAMIC PROGRAMMING - CUMULATIVE COST ARRAY (dp[])")
    print("-" * 55)
    print(f"  dp[0]  = Rs. {dp[0]:.2f}  (before simulation)")
    for idx, hour in enumerate(HOURS):
        print(f"  dp[{idx+1:2d}] = Rs. {dp[idx+1]:.2f}  "
              f"(after Hour {hour:02d}, this hour cost = Rs. {hour_costs[hour]:.2f})")
    print(f"\n  Total Minimum Cost (dp[{len(HOURS)}]) = Rs. {dp[len(HOURS)]:.2f}")
    print("-" * 55)

    # ─────────────────────────────────────────────────────────────────
    # TASK 6: Cost and Resource Utilization Analysis
    # ─────────────────────────────────────────────────────────────────

    total_energy  = total_solar + total_hydro + total_diesel
    renewable_pct = round(((total_solar + total_hydro) / total_energy) * 100, 2) if total_energy > 0 else 0
    diesel_pct    = round((total_diesel / total_energy) * 100, 2) if total_energy > 0 else 0

    print("\n" + "=" * 55)
    print("  TASK 6: COST AND RESOURCE UTILIZATION ANALYSIS")
    print("=" * 55)

    print("\n(a) Total Cost Calculation:")
    print(f"    Solar  energy used : {total_solar:.1f} kWh x Rs. 1.0 = Rs. {total_solar * 1.0:.2f}")
    print(f"    Hydro  energy used : {total_hydro:.1f} kWh x Rs. 1.5 = Rs. {total_hydro * 1.5:.2f}")
    print(f"    Diesel energy used : {total_diesel:.1f} kWh x Rs. 3.0 = Rs. {total_diesel * 3.0:.2f}")
    print(f"    ─────────────────────────────────────────")
    print(f"    Total Cost         : Rs. {dp[len(HOURS)]:.2f}")

    print("\n(b) Renewable Energy Contribution:")
    print(f"    Total Renewable (Solar + Hydro) : {total_solar + total_hydro:.1f} kWh")
    print(f"    Total Energy Supplied           : {total_energy:.1f} kWh")
    print(f"    Renewable Energy Share          : {renewable_pct}%")

    print("\n(c) Diesel Usage:")
    if diesel_log:
        print(f"    Diesel Energy Share : {diesel_pct}%")
        print(f"    Diesel was required in the following hours/districts:")
        for hour, district, amount in diesel_log:
            print(f"      Hour {hour:02d}, District {district}: {amount} kWh"
                  f"  (Solar unavailable after 18:00, Hydro capacity exceeded)")
    else:
        print("    Diesel was NOT used - all demand met by renewables!")

    print("\n(d) Algorithm Efficiency and Trade-offs:")
    print("    - Greedy approach  : O(H x D x S)")
    print("      H = hours, D = districts, S = sources")
    print("      Always picks cheapest source first -> minimizes cost")
    print("    - Dynamic Programming: dp[i+1] = dp[i] + hour_cost")
    print("      Tracks cumulative minimum cost across all hours")
    print("      Ensures optimal cost is built up step by step")
    print("    - Trade-off: Greedy is fast but may not always give the")
    print("      globally optimal solution. However, since source priority")
    print("      is fixed by cost, the greedy choice is locally and")
    print("      globally optimal for this problem structure.")
    print("=" * 55)


def main():
    run_smart_grid()


if __name__ == "__main__":
    main()