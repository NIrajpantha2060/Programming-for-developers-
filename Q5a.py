# question no 5a


# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import itertools
# import math
# import time



# tourist_spots = [
#     {
#         "name":       "Pashupatinath Temple",
#         "latitude":   27.7104,
#         "longitude":  85.3488,
#         "entry_fee":  100,
#         "open_time":  "06:00",
#         "close_time": "18:00",
#         "tags":       ["culture", "religious"]
#     },
#     {
#         "name":       "Swayambhunath Stupa",
#         "latitude":   27.7149,
#         "longitude":  85.2906,
#         "entry_fee":  200,
#         "open_time":  "07:00",
#         "close_time": "17:00",
#         "tags":       ["culture", "heritage"]
#     },
#     {
#         "name":       "Garden of Dreams",
#         "latitude":   27.7125,
#         "longitude":  85.3170,
#         "entry_fee":  150,
#         "open_time":  "09:00",
#         "close_time": "21:00",
#         "tags":       ["nature", "relaxation"]
#     },
#     {
#         "name":       "Chandragiri Hills",
#         "latitude":   27.6616,
#         "longitude":  85.2458,
#         "entry_fee":  700,
#         "open_time":  "09:00",
#         "close_time": "17:00",
#         "tags":       ["nature", "adventure"]
#     },
#     {
#         "name":       "Kathmandu Durbar Square",
#         "latitude":   27.7048,
#         "longitude":  85.3076,
#         "entry_fee":  100,
#         "open_time":  "10:00",
#         "close_time": "17:00",
#         "tags":       ["culture", "heritage"]
#     },
# ]

# ALL_INTERESTS = ["culture", "nature", "adventure", "heritage", "religious", "relaxation"]


# # 
# # HELPER FUNCTIONS
# # 

# def euclidean_distance(spot1, spot2):
#     """
#     Calculates travel distance between two spots using Euclidean formula.
#     1 degree latitude/longitude = 111 km (as documented).

#     Distance = sqrt((Δlat x 111)² + (Δlon x 111)²)

#     Args:
#         spot1, spot2: spot dicts with latitude and longitude
#     Returns:
#         distance in km
#     """
#     dx = (spot1["latitude"]  - spot2["latitude"])  * 111
#     dy = (spot1["longitude"] - spot2["longitude"]) * 111
#     return math.sqrt(dx**2 + dy**2)


# def travel_time_hours(spot1, spot2):
#     """
#     Estimates travel time between two spots.
#     Travel Time = Distance / 20 km/h (as documented).

#     Args:
#         spot1, spot2: spot dicts
#     Returns:
#         travel time in hours
#     """
#     if spot1 is None or spot2 is None:
#         return 0.0
#     return euclidean_distance(spot1, spot2) / 20.0


# def interest_match(spot, selected_interest):
#     """
#     Counts how many of the spot's tags match the selected interest.

#     Args:
#         spot              : spot dict
#         selected_interest : interest string
#     Returns:
#         integer count of matching tags
#     """
#     if isinstance(selected_interest, str):
#         selected_interest = [selected_interest]
#     return sum(1 for tag in selected_interest if tag in spot["tags"])


# # 
# # TASK 3: Greedy Heuristic Algorithm
# # 

# def greedy_itinerary(spots, total_hours, max_budget, selected_interest):
#     """
#     Greedy heuristic: at each step picks the highest scoring
#     unvisited spot that fits within remaining time and budget.

#     Score = interest_match x 10 - distance_penalty - fee_penalty

#     Steps:
#         1. Filter spots exceeding budget or time
#         2. Score remaining spots
#         3. Pick best score
#         4. Update time and budget
#         5. Repeat until no spot fits

#     Time complexity: O(n^2)

#     Args:
#         spots             : list of all tourist spot dicts
#         total_hours       : total available time in hours
#         max_budget        : maximum budget in Rs.
#         selected_interest : selected interest string
#     Returns:
#         list of dicts with spot, travel_time, cumulative_cost
#     """
#     remaining   = list(spots)
#     itinerary   = []
#     budget_left = max_budget
#     time_left   = total_hours
#     current     = None
#     cum_cost    = 0

#     while remaining:
#         best_spot  = None
#         best_score = float("-inf")

#         for spot in remaining:
#             # Filter: skip if over budget
#             if spot["entry_fee"] > budget_left:
#                 continue
#             # Filter: skip if not enough time
#             travel = travel_time_hours(current, spot)
#             if travel + 1.0 > time_left:
#                 continue

#             # Score the spot
#             match  = interest_match(spot, selected_interest)
#             dist   = euclidean_distance(current, spot) if current else 0
#             score  = match * 10 - dist - (spot["entry_fee"] / 200.0)

#             if score > best_score:
#                 best_score = score
#                 best_spot  = spot

#         if best_spot is None:
#             break

#         travel    = travel_time_hours(current, best_spot)
#         cum_cost += best_spot["entry_fee"]

#         itinerary.append({
#             "spot":            best_spot,
#             "travel_time":     round(travel, 2),
#             "cumulative_cost": cum_cost
#         })

#         budget_left -= best_spot["entry_fee"]
#         time_left   -= (travel + 1.0)
#         current      = best_spot
#         remaining.remove(best_spot)

#     return itinerary


# # 
# # TASK 5: Brute Force for Comparison
# # 

# def brute_force_itinerary(spots, total_hours, max_budget, selected_interest):
#     """
#     Brute force: tries ALL permutations of spots and returns
#     the best valid route.

#     Time complexity: O(n!) — practical only for n <= 6

#     Args:
#         spots             : list of spot dicts
#         total_hours       : available time in hours
#         max_budget        : budget in Rs.
#         selected_interest : selected interest string
#     Returns:
#         best valid list of spot dicts
#     """
#     best_route     = []
#     best_score     = float("-inf")
#     best_totaltime = 0.0

#     for perm in itertools.permutations(spots):
#         for length in range(1, len(perm) + 1):
#             candidate  = list(perm[:length])
#             total_fee  = 0
#             total_time = 0.0
#             prev       = None
#             score      = 0
#             valid      = True

#             for spot in candidate:
#                 total_fee += spot["entry_fee"]
#                 if total_fee > max_budget:
#                     valid = False
#                     break
#                 total_time += travel_time_hours(prev, spot) + 1.0
#                 if total_time > total_hours:
#                     valid = False
#                     break
#                 score += interest_match(spot, selected_interest) * 10
#                 score -= (spot["entry_fee"] / 200.0)
#                 prev = spot

#             if valid and score > best_score:
#                 best_score     = score
#                 best_route     = candidate
#                 best_totaltime = total_time

#     return best_route, best_totaltime


# # 
# # TASK 1 & 4: GUI Application
# # 

# class TouristPlannerApp:
#     """
#     Tourist Itinerary Planner GUI.

#     Layout:
#         Left panel  — inputs + output text
#         Right panel — canvas coordinate map (Task 4)

#     Theme: dark
#     """

#     def __init__(self, root):
#         self.root = root
#         self.root.title("Tourist Spot Optimizer")
#         self.root.configure(bg="#1e1e1e")
#         self.root.geometry("960x620")
#         self.root.resizable(True, True)
#         self._build_gui()

#     def _build_gui(self):
#         """Builds the full GUI — left input/output panel + right canvas map."""

#         # ── Outer split: left panel | right canvas ──
#         left  = tk.Frame(self.root, bg="#1e1e1e", padx=24, pady=16)
#         right = tk.Frame(self.root, bg="#1e1e1e", padx=12, pady=16)
#         left.pack(side="left",  fill="both", expand=True)
#         right.pack(side="right", fill="both", expand=True)

#         # ════════════════════════════════
#         # LEFT PANEL
#         # ════════════════════════════════

#         # Title
#         tk.Label(left,
#                  text="Tourist Itinerary Planner",
#                  font=("Helvetica", 18, "bold"),
#                  bg="#1e1e1e", fg="white").pack(pady=(0, 16))

#         # Input form
#         form = tk.Frame(left, bg="#1e1e1e")
#         form.pack(fill="x")

#         # Available Time
#         self._input_row(form, "Available Time (hours)", 0)
#         self.time_entry = tk.Entry(form,
#                                    font=("Helvetica", 12),
#                                    bg="#2e2e2e", fg="white",
#                                    insertbackground="white",
#                                    relief="flat", width=12,
#                                    highlightthickness=1,
#                                    highlightbackground="#555")
#         self.time_entry.insert(0, "1")
#         self.time_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

#         # Maximum Budget
#         self._input_row(form, "Maximum Budget", 1)
#         self.budget_entry = tk.Entry(form,
#                                      font=("Helvetica", 12),
#                                      bg="#2e2e2e", fg="white",
#                                      insertbackground="white",
#                                      relief="flat", width=12,
#                                      highlightthickness=1,
#                                      highlightbackground="#555")
#         self.budget_entry.insert(0, "2000")
#         self.budget_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

#         # Interest dropdown
#         self._input_row(form, "Interest", 2)
#         self.interest_var = tk.StringVar(value="nature")
#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("Dark.TCombobox",
#                          fieldbackground="#2e2e2e",
#                          background="#2e2e2e",
#                          foreground="white",
#                          arrowcolor="white",
#                          bordercolor="#555",
#                          lightcolor="#2e2e2e",
#                          darkcolor="#2e2e2e")
#         self.dropdown = ttk.Combobox(form,
#                                      textvariable=self.interest_var,
#                                      values=ALL_INTERESTS,
#                                      font=("Helvetica", 12),
#                                      style="Dark.TCombobox",
#                                      state="readonly",
#                                      width=14)
#         self.dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

#         # Generate button
#         tk.Button(left,
#                   text="Generate Itinerary",
#                   font=("Helvetica", 12),
#                   bg="white", fg="black",
#                   activebackground="#dddddd",
#                   relief="flat",
#                   padx=14, pady=6,
#                   cursor="hand2",
#                   command=self.generate).pack(pady=14)

#         # Output text area
#         self.output = scrolledtext.ScrolledText(
#             left,
#             font=("Courier", 10),
#             bg="#111111", fg="white",
#             insertbackground="white",
#             relief="flat",
#             height=16,
#             state="disabled",
#             wrap="word"
#         )
#         self.output.pack(fill="both", expand=True)

#         # ════════════════════════════════
#         # RIGHT PANEL — Map (Task 4)
#         # ════════════════════════════════

#         tk.Label(right,
#                  text="Route Map",
#                  font=("Helvetica", 13, "bold"),
#                  bg="#1e1e1e", fg="white").pack(anchor="w", pady=(0, 6))

#         self.canvas = tk.Canvas(right,
#                                 width=340, height=300,
#                                 bg="#111111",
#                                 highlightthickness=1,
#                                 highlightbackground="#444")
#         self.canvas.pack(fill="both", expand=True)

#         # Map placeholder text
#         self.canvas.create_text(170, 150,
#                                 text="Map will appear here\nafter generating itinerary",
#                                 font=("Helvetica", 10),
#                                 fill="#666666",
#                                 justify="center")

#     def _input_row(self, parent, label_text, row):
#         """Helper to add a label in the form grid."""
#         tk.Label(parent,
#                  text=label_text,
#                  font=("Helvetica", 12),
#                  bg="#1e1e1e", fg="white",
#                  anchor="e", width=22).grid(row=row, column=0, sticky="e", pady=5)

#     # 
#     # GENERATE — runs algorithms and updates both panels
#     # 

#     def generate(self):
#         """
#         Main handler: reads inputs, runs greedy + brute force,
#         displays text results and draws coordinate map.
#         """
#         try:
#             total_hours = float(self.time_entry.get().strip())
#             max_budget  = int(self.budget_entry.get().strip())
#         except ValueError:
#             self._write("ERROR: Please enter valid numbers for time and budget.\n")
#             return

#         selected_interest = self.interest_var.get()

#         # ── Run Greedy ──
#         t0            = time.time()
#         greedy_result = greedy_itinerary(tourist_spots, total_hours,
#                                          max_budget, selected_interest)
#         greedy_ms     = round((time.time() - t0) * 1000, 2)

#         # ── Run Brute Force ──
#         t0                    = time.time()
#         bf_result, bf_time_hr = brute_force_itinerary(tourist_spots, total_hours,
#                                                        max_budget, selected_interest)
#         bf_ms                 = round((time.time() - t0) * 1000, 2)

#         # ── Update text output ──
#         self._display_results(greedy_result, bf_result, bf_time_hr,
#                               greedy_ms, bf_ms, selected_interest)

#         # ── Update map ──
#         self._draw_map([item["spot"] for item in greedy_result])

#     def _display_results(self, greedy_result, bf_result, bf_time_hr,
#                          greedy_ms, bf_ms, interest):
#         """Formats and writes results to output text area."""

#         lines = []

#         # ── Suggested Itinerary ──
#         lines.append("Suggested Itinerary\n")
#         if not greedy_result:
#             lines.append("No spots could be visited within the given constraints.\n")
#         else:
#             g_total_cost = 0
#             g_total_time = 0.0
#             for i, item in enumerate(greedy_result):
#                 spot          = item["spot"]
#                 g_total_cost += spot["entry_fee"]
#                 g_total_time += item["travel_time"] + 1.0
#                 lines.append(f"{i+1}. {spot['name']} (Fee {spot['entry_fee']})\n")
#             lines.append(f"\nTotal Cost: {g_total_cost}")
#             lines.append(f"\nTotal Time: {round(g_total_time, 1)} hours\n")

#         # ── Decision Explanation ──
#         lines.append("\nDecision Explanation")
#         if greedy_result:
#             for item in greedy_result:
#                 spot  = item["spot"]
#                 match = interest_match(spot, interest)
#                 lines.append(
#                     f"\n{spot['name']} selected due to "
#                     f"interest match and low travel distance"
#                 )
#         else:
#             lines.append(
#                 f"\nNo spots matched '{interest}' "
#                 f"within the given time and budget."
#             )

#         # ── Brute Force Comparison ──
#         lines.append("\n\nBrute Force Comparison")
#         g_spots = len(greedy_result)
#         b_spots = len(bf_result)
#         g_cost  = sum(i["spot"]["entry_fee"] for i in greedy_result)
#         b_cost  = sum(s["entry_fee"] for s in bf_result)
#         g_time  = round(sum(i["travel_time"] + 1.0 for i in greedy_result), 2)
#         b_time  = round(bf_time_hr, 2)

#         lines.append(f"\nHeuristic visited : {g_spots} spots")
#         lines.append(f"\nBrute force best  : {b_spots} spots")
#         lines.append(f"\nHeuristic cost    : Rs. {g_cost}")
#         lines.append(f"\nBrute force cost  : Rs. {b_cost}")
#         lines.append(f"\nHeuristic time    : {g_time} hrs")
#         lines.append(f"\nBrute force time  : {b_time} hrs")
#         lines.append(f"\nHeuristic runtime : {greedy_ms} ms")
#         lines.append(f"\nBrute force runtime: {bf_ms} ms")

#         # Accuracy vs performance discussion
#         lines.append("\n\nAccuracy vs Performance:")
#         if g_spots == b_spots and g_cost == b_cost:
#             lines.append("\nBoth methods found the same result.")
#             lines.append(f"\nGreedy was ~{round(bf_ms/greedy_ms)}x faster than brute force.")
#         else:
#             lines.append(f"\nBrute force found {b_spots} spots, greedy found {g_spots}.")
#             lines.append("\nGreedy trades slight accuracy for much faster speed.")

#         self._write("".join(lines))

#     #
#     # TASK 4: Canvas Coordinate Map
#     # 

#     def _draw_map(self, spots):
#         """
#         Draws the route on the canvas as a coordinate plot.

#         - Normalizes lat/lon to canvas pixel coordinates
#         - Draws labeled circles for each spot
#         - Draws arrows between spots showing visit order

#         Args:
#             spots: list of selected spot dicts in visit order
#         """
#         self.canvas.delete("all")

#         if not spots:
#             self.canvas.create_text(170, 150,
#                                     text="No spots to display",
#                                     font=("Helvetica", 10),
#                                     fill="#666666")
#             return

#         W   = self.canvas.winfo_width()  or 340
#         H   = self.canvas.winfo_height() or 300
#         pad = 45

#         # Normalize lat/lon to canvas coordinates
#         lats = [s["latitude"]  for s in spots]
#         lons = [s["longitude"] for s in spots]
#         min_lat, max_lat = min(lats), max(lats)
#         min_lon, max_lon = min(lons), max(lons)

#         def to_xy(lat, lon):
#             """Converts geographic coordinates to canvas x,y pixels."""
#             x_range = max_lat - min_lat if max_lat != min_lat else 1e-5
#             y_range = max_lon - min_lon if max_lon != min_lon else 1e-5
#             x = pad + (lat - min_lat) / x_range * (W - 2 * pad)
#             y = pad + (lon - min_lon) / y_range * (H - 2 * pad)
#             return int(x), int(y)

#         coords = [to_xy(s["latitude"], s["longitude"]) for s in spots]

#         # Draw route arrows between spots
#         for i in range(1, len(coords)):
#             x1, y1 = coords[i - 1]
#             x2, y2 = coords[i]
#             self.canvas.create_line(x1, y1, x2, y2,
#                                     fill="#5588ee",
#                                     width=2,
#                                     arrow=tk.LAST,
#                                     arrowshape=(10, 12, 4))

#         # Draw spot circles and labels
#         for i, (x, y) in enumerate(coords):
#             # Circle
#             self.canvas.create_oval(x-9, y-9, x+9, y+9,
#                                     fill="#4178d2",
#                                     outline="white",
#                                     width=2)
#             # Number inside circle
#             self.canvas.create_text(x, y,
#                                     text=str(i + 1),
#                                     font=("Helvetica", 8, "bold"),
#                                     fill="white")
#             # Spot name label
#             name = spots[i]["name"]
#             if len(name) > 16:
#                 name = name[:15] + "…"
#             self.canvas.create_text(x + 14, y - 12,
#                                     text=name,
#                                     font=("Helvetica", 8),
#                                     fill="#aaaaff",
#                                     anchor="w")

#         # Map title
#         self.canvas.create_text(W // 2, 14,
#                                 text=f"Route: {len(spots)} spot(s) selected",
#                                 font=("Helvetica", 9, "bold"),
#                                 fill="#888888")

#     def _write(self, text):
#         """Writes text to the output area."""
#         self.output.config(state="normal")
#         self.output.delete("1.0", tk.END)
#         self.output.insert(tk.END, text)
#         self.output.config(state="disabled")


# # ─────────────────────────────────────────────────────────────────────
# # Main Entry Point
# # ─────────────────────────────────────────────────────────────────────

# def main():
#     root = tk.Tk()
#     app  = TouristPlannerApp(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()

# question no 5a

# question no 5a


import tkinter as tk
from tkinter import ttk, scrolledtext
import itertools
import math
import time



tourist_spots = [
    {
        "name":       "Pashupatinath Temple",
        "latitude":   27.7104,
        "longitude":  85.3488,
        "entry_fee":  100,
        "open_time":  "06:00",
        "close_time": "18:00",
        "tags":       ["culture", "religious"]
    },
    {
        "name":       "Swayambhunath Stupa",
        "latitude":   27.7149,
        "longitude":  85.2906,
        "entry_fee":  200,
        "open_time":  "07:00",
        "close_time": "17:00",
        "tags":       ["culture", "heritage"]
    },
    {
        "name":       "Garden of Dreams",
        "latitude":   27.7125,
        "longitude":  85.3170,
        "entry_fee":  150,
        "open_time":  "09:00",
        "close_time": "21:00",
        "tags":       ["nature", "relaxation"]
    },
    {
        "name":       "Chandragiri Hills",
        "latitude":   27.6616,
        "longitude":  85.2458,
        "entry_fee":  700,
        "open_time":  "09:00",
        "close_time": "17:00",
        "tags":       ["nature", "adventure"]
    },
    {
        "name":       "Kathmandu Durbar Square",
        "latitude":   27.7048,
        "longitude":  85.3076,
        "entry_fee":  100,
        "open_time":  "10:00",
        "close_time": "17:00",
        "tags":       ["culture", "heritage"]
    },
]

ALL_INTERESTS = ["culture", "nature", "adventure", "heritage", "religious", "relaxation"]


# 
# HELPER FUNCTIONS
# 

def euclidean_distance(spot1, spot2):
    """
    Calculates travel distance between two spots using Euclidean formula.
    1 degree latitude/longitude = 111 km (as documented).

    Distance = sqrt((Δlat x 111)² + (Δlon x 111)²)

    Args:
        spot1, spot2: spot dicts with latitude and longitude
    Returns:
        distance in km
    """
    dx = (spot1["latitude"]  - spot2["latitude"])  * 111
    dy = (spot1["longitude"] - spot2["longitude"]) * 111
    return math.sqrt(dx**2 + dy**2)


def travel_time_hours(spot1, spot2):
    """
    Estimates travel time between two spots.
    Travel Time = Distance / 20 km/h (as documented).

    Args:
        spot1, spot2: spot dicts
    Returns:
        travel time in hours
    """
    if spot1 is None or spot2 is None:
        return 0.0
    return euclidean_distance(spot1, spot2) / 20.0


def interest_match(spot, selected_interest):
    """
    Counts how many of the spot's tags match the selected interest.

    Args:
        spot              : spot dict
        selected_interest : interest string
    Returns:
        integer count of matching tags
    """
    if isinstance(selected_interest, str):
        selected_interest = [selected_interest]
    return sum(1 for tag in selected_interest if tag in spot["tags"])


# 
# TASK 3: Greedy Heuristic Algorithm
# 

def greedy_itinerary(spots, total_hours, max_budget, selected_interest):
    """
    Greedy heuristic: at each step picks the highest scoring
    unvisited spot that fits within remaining time and budget.

    Score = interest_match x 10 - distance_penalty - fee_penalty

    Steps:
        1. Filter spots exceeding budget or time
        2. Score remaining spots
        3. Pick best score
        4. Update time and budget
        5. Repeat until no spot fits

    Time complexity: O(n^2)

    Args:
        spots             : list of all tourist spot dicts
        total_hours       : total available time in hours
        max_budget        : maximum budget in Rs.
        selected_interest : selected interest string
    Returns:
        list of dicts with spot, travel_time, cumulative_cost
    """
    remaining   = list(spots)
    itinerary   = []
    budget_left = max_budget
    time_left   = total_hours
    current     = None
    cum_cost    = 0

    while remaining:
        best_spot  = None
        best_score = float("-inf")

        for spot in remaining:
            # Filter: skip if over budget
            if spot["entry_fee"] > budget_left:
                continue
            # Filter: skip if not enough time
            travel = travel_time_hours(current, spot)
            if travel + 1.0 > time_left:
                continue

            # Score the spot
            match  = interest_match(spot, selected_interest)
            dist   = euclidean_distance(current, spot) if current else 0
            score  = match * 10 - dist - (spot["entry_fee"] / 200.0)

            if score > best_score:
                best_score = score
                best_spot  = spot

        if best_spot is None:
            break

        travel    = travel_time_hours(current, best_spot)
        cum_cost += best_spot["entry_fee"]

        itinerary.append({
            "spot":            best_spot,
            "travel_time":     round(travel, 2),
            "cumulative_cost": cum_cost
        })

        budget_left -= best_spot["entry_fee"]
        time_left   -= (travel + 1.0)
        current      = best_spot
        remaining.remove(best_spot)

    return itinerary


# 
# TASK 5: Brute Force for Comparison
# 

def brute_force_itinerary(spots, total_hours, max_budget, selected_interest):
    """
    Brute force: tries ALL permutations of spots and returns
    the best valid route.

    Time complexity: O(n!) — practical only for n <= 6

    Args:
        spots             : list of spot dicts
        total_hours       : available time in hours
        max_budget        : budget in Rs.
        selected_interest : selected interest string
    Returns:
        best valid list of spot dicts
    """
    best_route     = []
    best_score     = float("-inf")
    best_totaltime = 0.0

    for perm in itertools.permutations(spots):
        for length in range(1, len(perm) + 1):
            candidate  = list(perm[:length])
            total_fee  = 0
            total_time = 0.0
            prev       = None
            score      = 0
            valid      = True

            for spot in candidate:
                total_fee += spot["entry_fee"]
                if total_fee > max_budget:
                    valid = False
                    break
                total_time += travel_time_hours(prev, spot) + 1.0
                if total_time > total_hours:
                    valid = False
                    break
                score += interest_match(spot, selected_interest) * 10
                score -= (spot["entry_fee"] / 200.0)
                prev = spot

            if valid and score > best_score:
                best_score     = score
                best_route     = candidate
                best_totaltime = total_time

    return best_route, best_totaltime


# 
# TASK 1 & 4: GUI Application
# 

class TouristPlannerApp:
    """
    Tourist Itinerary Planner GUI.

    Layout:
        Left panel  — inputs + output text
        Right panel — canvas coordinate map (Task 4)

    Theme: dark
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Tourist Spot Optimizer")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("960x620")
        self.root.resizable(True, True)
        self._pending_draw = None   # tracks scheduled draw job
        self._build_gui()

    def _build_gui(self):
        """Builds the full GUI — left input/output panel + right canvas map."""

        # ── Outer split: left panel | right canvas ──
        left  = tk.Frame(self.root, bg="#1e1e1e", padx=24, pady=16)
        right = tk.Frame(self.root, bg="#1e1e1e", padx=12, pady=16)
        left.pack(side="left",  fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        # ════════════════════════════════
        # LEFT PANEL
        # ════════════════════════════════

        # Title
        tk.Label(left,
                 text="Tourist Itinerary Planner",
                 font=("Helvetica", 18, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=(0, 16))

        # Input form
        form = tk.Frame(left, bg="#1e1e1e")
        form.pack(fill="x")

        # Available Time
        self._input_row(form, "Available Time (hours)", 0)
        self.time_entry = tk.Entry(form,
                                   font=("Helvetica", 12),
                                   bg="#2e2e2e", fg="white",
                                   insertbackground="white",
                                   relief="flat", width=12,
                                   highlightthickness=1,
                                   highlightbackground="#555")
        self.time_entry.insert(0, "1")
        self.time_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Maximum Budget
        self._input_row(form, "Maximum Budget", 1)
        self.budget_entry = tk.Entry(form,
                                     font=("Helvetica", 12),
                                     bg="#2e2e2e", fg="white",
                                     insertbackground="white",
                                     relief="flat", width=12,
                                     highlightthickness=1,
                                     highlightbackground="#555")
        self.budget_entry.insert(0, "2000")
        self.budget_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Interest dropdown
        self._input_row(form, "Interest", 2)
        self.interest_var = tk.StringVar(value="nature")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TCombobox",
                         fieldbackground="#2e2e2e",
                         background="#2e2e2e",
                         foreground="white",
                         arrowcolor="white",
                         bordercolor="#555",
                         lightcolor="#2e2e2e",
                         darkcolor="#2e2e2e")
        self.dropdown = ttk.Combobox(form,
                                     textvariable=self.interest_var,
                                     values=ALL_INTERESTS,
                                     font=("Helvetica", 12),
                                     style="Dark.TCombobox",
                                     state="readonly",
                                     width=14)
        self.dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Generate button
        tk.Button(left,
                  text="Generate Itinerary",
                  font=("Helvetica", 12),
                  bg="white", fg="black",
                  activebackground="#dddddd",
                  relief="flat",
                  padx=14, pady=6,
                  cursor="hand2",
                  command=self.generate).pack(pady=14)

        # Output text area
        self.output = scrolledtext.ScrolledText(
            left,
            font=("Courier", 10),
            bg="#111111", fg="white",
            insertbackground="white",
            relief="flat",
            height=16,
            state="disabled",
            wrap="word"
        )
        self.output.pack(fill="both", expand=True)

        # ════════════════════════════════
        # RIGHT PANEL — Map (Task 4)
        # ════════════════════════════════

        tk.Label(right,
                 text="Route Map",
                 font=("Helvetica", 13, "bold"),
                 bg="#1e1e1e", fg="white").pack(anchor="w", pady=(0, 6))

        self.canvas = tk.Canvas(right,
                                width=340, height=300,
                                bg="#111111",
                                highlightthickness=1,
                                highlightbackground="#444")
        self.canvas.pack(fill="both", expand=True)

        # Map placeholder text
        self.canvas.create_text(170, 150,
                                text="Map will appear here\nafter generating itinerary",
                                font=("Helvetica", 10),
                                fill="#666666",
                                justify="center")

    def _input_row(self, parent, label_text, row):
        """Helper to add a label in the form grid."""
        tk.Label(parent,
                 text=label_text,
                 font=("Helvetica", 12),
                 bg="#1e1e1e", fg="white",
                 anchor="e", width=22).grid(row=row, column=0, sticky="e", pady=5)

    # 
    # GENERATE — runs algorithms and updates both panels
    # 

    def generate(self):
        """
        Main handler: reads inputs, runs greedy + brute force,
        displays text results and draws coordinate map.
        """
        try:
            total_hours = float(self.time_entry.get().strip())
            max_budget  = int(self.budget_entry.get().strip())
        except ValueError:
            self._write("ERROR: Please enter valid numbers for time and budget.\n")
            return

        selected_interest = self.interest_var.get()

        # ── Run Greedy ──
        t0            = time.time()
        greedy_result = greedy_itinerary(tourist_spots, total_hours,
                                         max_budget, selected_interest)
        greedy_ms     = round((time.time() - t0) * 1000, 2)

        # ── Run Brute Force ──
        t0                    = time.time()
        bf_result, bf_time_hr = brute_force_itinerary(tourist_spots, total_hours,
                                                       max_budget, selected_interest)
        bf_ms                 = round((time.time() - t0) * 1000, 2)

        # ── Update text output ──
        self._display_results(greedy_result, bf_result, bf_time_hr,
                              greedy_ms, bf_ms, selected_interest)

        # ── Update map ──
        # Cancel any previously scheduled draw first (stale draw prevention)
        if self._pending_draw is not None:
            self.root.after_cancel(self._pending_draw)
            self._pending_draw = None

        # Clear canvas immediately so old map never shows through
        self.canvas.delete("all")

        # Schedule fresh draw after layout settles
        spots_to_draw = [item["spot"] for item in greedy_result]
        self._pending_draw = self.root.after(
            80, lambda: self._draw_map(spots_to_draw)
        )

    def _display_results(self, greedy_result, bf_result, bf_time_hr,
                         greedy_ms, bf_ms, interest):
        """Formats and writes results to output text area."""

        lines = []

        # ── Suggested Itinerary ──
        lines.append("Suggested Itinerary\n")
        if not greedy_result:
            lines.append("No spots could be visited within the given constraints.\n")
        else:
            g_total_cost = 0
            g_total_time = 0.0
            for i, item in enumerate(greedy_result):
                spot          = item["spot"]
                g_total_cost += spot["entry_fee"]
                g_total_time += item["travel_time"] + 1.0
                lines.append(f"{i+1}. {spot['name']} (Fee {spot['entry_fee']})\n")
            lines.append(f"\nTotal Cost: {g_total_cost}")
            lines.append(f"\nTotal Time: {round(g_total_time, 1)} hours\n")

        # ── Decision Explanation ──
        lines.append("\nDecision Explanation")
        if greedy_result:
            for item in greedy_result:
                spot  = item["spot"]
                match = interest_match(spot, interest)
                lines.append(
                    f"\n{spot['name']} selected due to "
                    f"interest match and low travel distance"
                )
        else:
            lines.append(
                f"\nNo spots matched '{interest}' "
                f"within the given time and budget."
            )

        # ── Brute Force Comparison ──
        lines.append("\n\nBrute Force Comparison")
        g_spots = len(greedy_result)
        b_spots = len(bf_result)
        g_cost  = sum(i["spot"]["entry_fee"] for i in greedy_result)
        b_cost  = sum(s["entry_fee"] for s in bf_result)
        g_time  = round(sum(i["travel_time"] + 1.0 for i in greedy_result), 2)
        b_time  = round(bf_time_hr, 2)

        lines.append(f"\nHeuristic visited : {g_spots} spots")
        lines.append(f"\nBrute force best  : {b_spots} spots")
        lines.append(f"\nHeuristic cost    : Rs. {g_cost}")
        lines.append(f"\nBrute force cost  : Rs. {b_cost}")
        lines.append(f"\nHeuristic time    : {g_time} hrs")
        lines.append(f"\nBrute force time  : {b_time} hrs")
        lines.append(f"\nHeuristic runtime : {greedy_ms} ms")
        lines.append(f"\nBrute force runtime: {bf_ms} ms")

        # Accuracy vs performance discussion
        lines.append("\n\nAccuracy vs Performance:")
        if g_spots == b_spots and g_cost == b_cost:
            lines.append("\nBoth methods found the same result.")
            lines.append(f"\nGreedy was ~{round(bf_ms/greedy_ms)}x faster than brute force.")
        else:
            lines.append(f"\nBrute force found {b_spots} spots, greedy found {g_spots}.")
            lines.append("\nGreedy trades slight accuracy for much faster speed.")

        self._write("".join(lines))

    #
    # TASK 4: Canvas Coordinate Map  ← FIXED
    # 

    def _draw_map(self, spots):
        """
        Draws the route on the canvas as a coordinate plot.

        FIX 1: Use canvas.winfo_width/height AFTER layout with update_idletasks()
                so we always get the real rendered size, not 1x1.
        FIX 2: lon = X axis (east-west = horizontal direction)
                lat = Y axis (north-south = vertical direction, inverted so north is up)
                Previously lat was used as X which caused wrong positions.

        Args:
            spots: list of selected spot dicts in visit order
        """
        self._pending_draw = None   # job is now running, clear the reference

        self.canvas.delete("all")

        if not spots:
            self.canvas.create_text(170, 150,
                                    text="No spots to display",
                                    font=("Helvetica", 10),
                                    fill="#666666")
            return

        # Force layout update so winfo returns real rendered size
        self.canvas.update_idletasks()
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()

        # Reliable fallback if canvas not yet rendered
        if W < 10:
            W = 340
        if H < 10:
            H = 300

        pad = 45

        lats = [s["latitude"]  for s in spots]
        lons = [s["longitude"] for s in spots]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        def to_xy(lat, lon):
            """
            Converts geographic coordinates to canvas x,y pixels.

            FIX 2: lon maps to X (horizontal/east-west - correct)
                   lat maps to Y inverted (vertical/north-south
                   inverted so north=top - correct)
            """
            x_range = max_lon - min_lon if max_lon != min_lon else 1e-5
            y_range = max_lat - min_lat if max_lat != min_lat else 1e-5
            # longitude → X axis (east is right)
            x = pad + (lon - min_lon) / x_range * (W - 2 * pad)
            # latitude → Y axis inverted (north is up = smaller y pixel)
            y = pad + (max_lat - lat) / y_range * (H - 2 * pad)
            return int(x), int(y)

        coords = [to_xy(s["latitude"], s["longitude"]) for s in spots]

        # Draw route arrows between spots
        for i in range(1, len(coords)):
            x1, y1 = coords[i - 1]
            x2, y2 = coords[i]
            self.canvas.create_line(x1, y1, x2, y2,
                                    fill="#5588ee",
                                    width=2,
                                    arrow=tk.LAST,
                                    arrowshape=(10, 12, 4))

        # Draw spot circles and labels
        for i, (x, y) in enumerate(coords):
            # Circle
            self.canvas.create_oval(x-9, y-9, x+9, y+9,
                                    fill="#4178d2",
                                    outline="white",
                                    width=2)
            # Number inside circle
            self.canvas.create_text(x, y,
                                    text=str(i + 1),
                                    font=("Helvetica", 8, "bold"),
                                    fill="white")
            # Spot name label
            name = spots[i]["name"]
            if len(name) > 16:
                name = name[:15] + "…"
            self.canvas.create_text(x + 14, y - 12,
                                    text=name,
                                    font=("Helvetica", 8),
                                    fill="#aaaaff",
                                    anchor="w")

        # Map title
        self.canvas.create_text(W // 2, 14,
                                text=f"Route: {len(spots)} spot(s) selected",
                                font=("Helvetica", 9, "bold"),
                                fill="#888888")

    def _write(self, text):
        """Writes text to the output area."""
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state="disabled")


# ─────────────────────────────────────────────────────────────────────
# Main Entry Point
# ─────────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    app  = TouristPlannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()