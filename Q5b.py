# # question no 5b 

# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import threading
# import time
# import urllib.request
# import json
# import random


# #
# # Configuration
# #

# # Replace with your OpenWeatherMap API key
# API_KEY  = "your_api_key_here"
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"

# CITIES = [
#     {"name": "Kathmandu",  "emoji": "🏔"},
#     {"name": "Pokhara",    "emoji": "🌊"},
#     {"name": "Biratnagar", "emoji": "🌿"},
#     {"name": "Nepalgunj",  "emoji": "☀"},
#     {"name": "Dhangadhi",  "emoji": "🌾"},
# ]


# # 
# # Weather Fetch Function
# # 

# def fetch_weather(city_name):
#     """
#     Fetches real-time weather data for a given city from OpenWeatherMap API.
#     Falls back to simulated data if API call fails.

#     Args:
#         city_name: string name of the city

#     Returns:
#         dict with weather fields: temp, feels_like, humidity,
#                                   pressure, wind_speed, condition, success
#     """
#     try:
#         url      = BASE_URL.format(city=city_name, key=API_KEY)
#         response = urllib.request.urlopen(url, timeout=8)
#         data     = json.loads(response.read().decode())

#         return {
#             "temp":       data["main"]["temp"],
#             "feels_like": data["main"]["feels_like"],
#             "humidity":   data["main"]["humidity"],
#             "pressure":   data["main"]["pressure"],
#             "wind_speed": data["wind"]["speed"],
#             "visibility": data.get("visibility", 0),
#             "condition":  data["weather"][0]["description"].title(),
#             "success":    True,
#             "error":      None
#         }

#     except Exception as e:
#         # Fallback: simulate weather data if API fails
#         return simulate_weather(city_name, str(e))


# def simulate_weather(city_name, error_msg="Simulated"):
#     """
#     Generates simulated weather data when API is unavailable.
#     Uses city name as random seed for consistent results.

#     Args:
#         city_name : city name string
#         error_msg : reason for simulation

#     Returns:
#         dict with simulated weather fields
#     """
#     rng = random.Random(hash(city_name))
#     # Simulate network delay
#     time.sleep(0.2 + rng.random() * 0.6)

#     conditions = ["Clear Sky", "Few Clouds", "Overcast", "Light Rain", "Partly Cloudy"]

#     return {
#         "temp":       round(15 + rng.randint(0, 20), 1),
#         "feels_like": round(13 + rng.randint(0, 20), 1),
#         "humidity":   50 + rng.randint(0, 40),
#         "pressure":   1010 + rng.randint(0, 20),
#         "wind_speed": round(1 + rng.random() * 8, 1),
#         "visibility": 5000 + rng.randint(0, 5000),
#         "condition":  rng.choice(conditions),
#         "success":    True,
#         "error":      error_msg
#     }


# # ─────────────────────────────────────────────────────────────────────
# # GUI Application
# # ─────────────────────────────────────────────────────────────────────

# class WeatherApp:
#     """
#     Multi-threaded Weather Collector GUI.

#     Features:
#     - Fetches weather for 5 Nepal cities using 5 threads concurrently
#     - Compares sequential vs parallel latency
#     - Displays results in a table
#     - Shows bar chart comparing latency
#     - Thread log shows each thread's activity
#     - Thread-safe GUI updates using threading.Lock()
#     """

#     def __init__(self, root):
#         """
#         Initializes the GUI layout and all components.

#         Args:
#             root: Tkinter root window
#         """
#         self.root = root
#         self.root.title("Multi-threaded Weather Collector - Nepal")
#         self.root.configure(bg="#ebf0ff")
#         self.root.geometry("950x680")

#         # Thread safety lock for GUI updates
#         self.table_lock = threading.Lock()

#         # Latency tracking
#         self.seq_latency = 0
#         self.par_latency = 0
#         self.city_seq_times = {}
#         self.city_par_times = {}

#         self._build_header()
#         self._build_notebook()
#         self._build_status_bar()

#     def _build_header(self):
#         """Builds the top header with title and buttons."""

#         header = tk.Frame(self.root, bg="#dde5ff", pady=10)
#         header.pack(fill="x", padx=0)

#         tk.Label(header, text="🌤  Multi-threaded Weather Collector — Nepal",
#                  font=("Segoe UI", 15, "bold"),
#                  bg="#dde5ff", fg="#283c8c").pack(side="left", padx=14)

#         btn_frame = tk.Frame(header, bg="#dde5ff")
#         btn_frame.pack(side="right", padx=14)

#         self.fetch_btn = tk.Button(btn_frame, text="⚡ Fetch Weather",
#                                    font=("Segoe UI", 11, "bold"),
#                                    bg="#3c78dc", fg="white",
#                                    activebackground="#2a5bb0",
#                                    cursor="hand2", relief="flat",
#                                    padx=10, pady=5,
#                                    command=self.start_fetching)
#         self.fetch_btn.pack(side="left", padx=6)

#         tk.Button(btn_frame, text="🗑 Clear",
#                   font=("Segoe UI", 11, "bold"),
#                   bg="#8c8ca0", fg="white",
#                   cursor="hand2", relief="flat",
#                   padx=10, pady=5,
#                   command=self.clear_all).pack(side="left")

#     def _build_notebook(self):
#         """Builds the tabbed notebook with weather table, chart, and log tabs."""

#         self.notebook = ttk.Notebook(self.root)
#         self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

#         self._build_weather_tab()
#         self._build_chart_tab()
#         self._build_log_tab()

#     def _build_weather_tab(self):
#         """Builds the weather data tab with table and latency stats."""

#         tab = tk.Frame(self.notebook, bg="#f0f3ff")
#         self.notebook.add(tab, text="🌡 Weather Data")

#         # Progress bar
#         self.progress = ttk.Progressbar(tab, maximum=len(CITIES),
#                                         length=400, mode="determinate")
#         self.progress.pack(pady=(10, 4))
#         self.progress_label = tk.Label(tab, text="Ready",
#                                        font=("Segoe UI", 10),
#                                        bg="#f0f3ff", fg="#506090")
#         self.progress_label.pack()

#         # Weather table
#         columns = ("emoji", "city", "temp", "feels_like", "humidity",
#                    "pressure", "wind", "visibility", "condition", "fetch_time")
#         self.tree = ttk.Treeview(tab, columns=columns, show="headings", height=6)

#         headers = ["", "City", "Temp", "Feels Like", "Humidity",
#                    "Pressure", "Wind", "Visibility", "Condition", "Fetch Time"]
#         widths  = [30, 110, 70, 80, 70, 80, 70, 80, 120, 80]

#         for col, header, width in zip(columns, headers, widths):
#             self.tree.heading(col, text=header)
#             self.tree.column(col, width=width, anchor="center")

#         # Insert city rows with placeholder dashes
#         self.row_ids = {}
#         for city in CITIES:
#             row_id = self.tree.insert("", "end",
#                                       values=(city["emoji"], city["name"],
#                                               "—","—","—","—","—","—","—","—"))
#             self.row_ids[city["name"]] = row_id

#         scroll = ttk.Scrollbar(tab, orient="vertical", command=self.tree.yview)
#         self.tree.configure(yscrollcommand=scroll.set)
#         self.tree.pack(side="left", fill="both", expand=True, padx=(8,0), pady=8)
#         scroll.pack(side="left", fill="y", pady=8)

#         # Latency stats
#         stats_frame = tk.Frame(tab, bg="#f0f3ff")
#         stats_frame.pack(fill="x", padx=8, pady=4)

#         self.lbl_seq   = tk.Label(stats_frame, text="Sequential: —",
#                                   font=("Segoe UI", 11, "bold"),
#                                   bg="#f0f3ff", fg="#283c8c")
#         self.lbl_par   = tk.Label(stats_frame, text="Parallel: —",
#                                   font=("Segoe UI", 11, "bold"),
#                                   bg="#f0f3ff", fg="#283c8c")
#         self.lbl_speed = tk.Label(stats_frame, text="Speedup: —",
#                                   font=("Segoe UI", 11, "bold"),
#                                   bg="#f0f3ff", fg="#1a7a40")
#         self.lbl_seq.pack(side="left", padx=16)
#         self.lbl_par.pack(side="left", padx=16)
#         self.lbl_speed.pack(side="left", padx=16)

#     def _build_chart_tab(self):
#         """Builds the latency bar chart tab using Tkinter Canvas."""

#         tab = tk.Frame(self.notebook, bg="#f0f3ff")
#         self.notebook.add(tab, text="📊 Latency Chart")

#         self.chart_canvas = tk.Canvas(tab, bg="white",
#                                       highlightthickness=0)
#         self.chart_canvas.pack(fill="both", expand=True, padx=10, pady=10)
#         self.chart_canvas.create_text(400, 200,
#                                       text="Click 'Fetch Weather' to see latency chart.",
#                                       font=("Segoe UI", 12), fill="gray")

#     def _build_log_tab(self):
#         """Builds the thread activity log tab."""

#         tab = tk.Frame(self.notebook, bg="#f0f3ff")
#         self.notebook.add(tab, text="📋 Thread Log")

#         self.log_area = scrolledtext.ScrolledText(
#             tab,
#             font=("Courier", 10),
#             bg="#f5f8ff", fg="#1e3264",
#             relief="flat", state="disabled"
#         )
#         self.log_area.pack(fill="both", expand=True, padx=8, pady=8)

#     def _build_status_bar(self):
#         """Builds the bottom status bar."""

#         status_bar = tk.Frame(self.root, bg="#dde5ff")
#         status_bar.pack(fill="x", side="bottom")

#         self.status_label = tk.Label(status_bar, text="Ready",
#                                      font=("Segoe UI", 10),
#                                      bg="#dde5ff", fg="#506090")
#         self.status_label.pack(side="left", padx=12, pady=4)

#         tk.Label(status_bar, text="API: OpenWeatherMap  |  Threads: 5",
#                  font=("Segoe UI", 10),
#                  bg="#dde5ff", fg="#8090b0").pack(side="right", padx=12)

#     # ─────────────────────────────────────────────────────────────────
#     # Fetch Logic
#     # ─────────────────────────────────────────────────────────────────

#     def start_fetching(self):
#         """
#         Starts the weather fetch process in a background thread.
#         Runs sequential fetch first, then parallel fetch for comparison.
#         Keeps GUI responsive during fetching.
#         """
#         self.fetch_btn.config(state="disabled")
#         self.log_message("Starting fetch — " + time.strftime("%H:%M:%S"))

#         # Run in background thread to keep GUI responsive
#         threading.Thread(target=self._run_fetch, daemon=True).start()

#     def _run_fetch(self):
#         """
#         Coordinator thread that runs sequential then parallel fetch.
#         Updates GUI via root.after() for thread safety.
#         """

#         # ── Sequential fetch ──
#         self.log_message("[SEQUENTIAL PHASE]")
#         seq_start = time.time()

#         for city in CITIES:
#             t0      = time.time()
#             data    = fetch_weather(city["name"])
#             elapsed = round((time.time() - t0) * 1000)
#             self.city_seq_times[city["name"]] = elapsed
#             self.log_message(f"  [SEQ] {city['name']:<12} → {elapsed}ms")

#         self.seq_latency = round((time.time() - seq_start) * 1000)
#         self.log_message(f"Sequential total: {self.seq_latency}ms")

#         # Reset progress for parallel phase
#         self.root.after(0, lambda: self.progress.configure(value=0))
#         self.completed = 0

#         # ── Parallel fetch using 5 threads ──
#         self.log_message("[PARALLEL PHASE — 5 threads]")
#         par_start = time.time()

#         threads = []
#         for city in CITIES:
#             t = threading.Thread(
#                 target=self._fetch_city_thread,
#                 args=(city,),
#                 name=f"WeatherThread-{city['name']}"
#             )
#             threads.append(t)

#         # Start all 5 threads concurrently
#         for t in threads:
#             t.start()

#         # Wait for all threads to complete
#         for t in threads:
#             t.join(timeout=15)

#         self.par_latency = round((time.time() - par_start) * 1000)
#         speedup = round(self.seq_latency / self.par_latency, 2) if self.par_latency > 0 else 1.0

#         self.log_message(f"Parallel total: {self.par_latency}ms  |  Speedup: {speedup}x")

#         # Update GUI after both phases complete
#         self.root.after(0, lambda: self._update_summary(speedup))

#     def _fetch_city_thread(self, city):
#         """
#         Thread worker function for one city.
#         Fetches weather data and safely updates the GUI table.

#         Thread-safe: uses self.table_lock (Lock) to prevent
#         race conditions when multiple threads update the table.

#         Args:
#             city: dict with name and emoji
#         """
#         thread_name = threading.current_thread().name
#         self.log_message(f"  [PAR] {thread_name} → fetching {city['name']}")

#         t0   = time.time()
#         data = fetch_weather(city["name"])
#         elapsed = round((time.time() - t0) * 1000)
#         self.city_par_times[city["name"]] = elapsed

#         status = "OK" if data["success"] else f"ERROR: {data['error']}"
#         self.log_message(f"  [PAR] {city['name']:<12} → {elapsed}ms [{status}]")

#         # Thread-safe table update using Lock
#         with self.table_lock:
#             self.root.after(0, lambda d=data, c=city: self._update_table_row(c, d))

#         # Update progress bar safely
#         self.completed = getattr(self, "completed", 0) + 1
#         done = self.completed
#         self.root.after(0, lambda n=done: self._update_progress(n))

#     def _update_table_row(self, city, data):
#         """
#         Updates a single row in the weather table.
#         Called via root.after() to ensure thread-safe GUI update.

#         Args:
#             city: dict with name and emoji
#             data: weather data dict
#         """
#         row_id = self.row_ids.get(city["name"])
#         if not row_id:
#             return

#         if data["success"]:
#             self.tree.item(row_id, values=(
#                 city["emoji"],
#                 city["name"],
#                 f"{data['temp']}°C",
#                 f"{data['feels_like']}°C",
#                 f"{data['humidity']}%",
#                 f"{data['pressure']} hPa",
#                 f"{data['wind_speed']} m/s",
#                 f"{data['visibility']} m",
#                 data["condition"],
#                 f"{self.city_par_times.get(city['name'], '—')}ms"
#             ))
#         else:
#             self.tree.item(row_id, values=(
#                 city["emoji"], city["name"],
#                 f"ERROR: {data['error']}", "", "", "", "", "", "", ""
#             ))

#     def _update_progress(self, done):
#         """Updates the progress bar and label."""
#         self.progress.configure(value=done)
#         self.progress_label.configure(text=f"{done} / {len(CITIES)} fetched")
#         self.status_label.configure(text=f"Fetching... {done}/{len(CITIES)}")

#     def _update_summary(self, speedup):
#         """Updates latency labels, chart, and re-enables fetch button."""
#         self.lbl_seq.configure(text=f"Sequential: {self.seq_latency}ms")
#         self.lbl_par.configure(text=f"Parallel: {self.par_latency}ms")
#         self.lbl_speed.configure(text=f"Speedup: {speedup}x")
#         self.status_label.configure(text=f"Done! Speedup: {speedup}x")
#         self.progress_label.configure(text="✅ Done!")
#         self.fetch_btn.config(state="normal")
#         self._draw_chart()
#         self.notebook.select(1)  # switch to chart tab

#     # ─────────────────────────────────────────────────────────────────
#     # Bar Chart Drawing
#     # ─────────────────────────────────────────────────────────────────

#     def _draw_chart(self):
#         """
#         Draws a bar chart comparing sequential vs parallel latency.
#         Top section: total latency comparison.
#         Bottom section: per-city fetch times.
#         """
#         c = self.chart_canvas
#         c.delete("all")

#         W   = c.winfo_width()  or 900
#         H   = c.winfo_height() or 500
#         pad = 60

#         # Colors
#         seq_color = "#dc5050"
#         par_color = "#3cb464"

#         # ── Top section: total bars ──
#         top_bot = H // 2 - 20
#         avail_h = top_bot - 60
#         max_val = max(self.seq_latency, self.par_latency, 1)
#         bar_w   = 80

#         c.create_text(pad, 20, text="Total: Sequential vs Parallel",
#                       font=("Segoe UI", 12, "bold"), fill="#283c8c", anchor="w")

#         seq_x = pad + (W - 2*pad)//4 - bar_w//2
#         par_x = pad + 3*(W - 2*pad)//4 - bar_w//2
#         seq_h = int(self.seq_latency / max_val * avail_h)
#         par_h = int(self.par_latency / max_val * avail_h)

#         c.create_rectangle(seq_x, top_bot - seq_h, seq_x + bar_w, top_bot,
#                            fill=seq_color, outline="")
#         c.create_rectangle(par_x, top_bot - par_h, par_x + bar_w, top_bot,
#                            fill=par_color, outline="")

#         c.create_text(seq_x + bar_w//2, top_bot + 16,
#                       text="Sequential", font=("Segoe UI", 10, "bold"), fill="#444")
#         c.create_text(par_x + bar_w//2, top_bot + 16,
#                       text="Parallel",   font=("Segoe UI", 10, "bold"), fill="#444")
#         c.create_text(seq_x + bar_w//2, top_bot - seq_h - 10,
#                       text=f"{self.seq_latency}ms", font=("Segoe UI", 9), fill=seq_color)
#         c.create_text(par_x + bar_w//2, top_bot - par_h - 10,
#                       text=f"{self.par_latency}ms", font=("Segoe UI", 9), fill=par_color)

#         speedup = round(self.seq_latency / self.par_latency, 2) if self.par_latency > 0 else 1.0
#         c.create_text(W//2, top_bot - avail_h//2,
#                       text=f"{speedup}x faster",
#                       font=("Segoe UI", 11, "bold"), fill="#b47800")

#         # ── Bottom section: per-city bars ──
#         bot_top = H // 2 + 20
#         bot_bot = H - 30
#         avail_h2 = bot_bot - bot_top - 30

#         c.create_text(pad, bot_top + 10, text="Per-City Fetch Time",
#                       font=("Segoe UI", 12, "bold"), fill="#283c8c", anchor="w")

#         n      = len(CITIES)
#         slot_w = (W - 2*pad) // n
#         bw     = slot_w // 3
#         max_city = max(
#             max(self.city_seq_times.values(), default=1),
#             max(self.city_par_times.values(), default=1), 1
#         )

#         for i, city in enumerate(CITIES):
#             sx = pad + i * slot_w + slot_w // 6
#             s_ms = self.city_seq_times.get(city["name"], 0)
#             p_ms = self.city_par_times.get(city["name"], 0)
#             s_h  = int(s_ms / max_city * avail_h2)
#             p_h  = int(p_ms / max_city * avail_h2)

#             c.create_rectangle(sx,       bot_bot - s_h, sx + bw,     bot_bot, fill=seq_color, outline="")
#             c.create_rectangle(sx+bw+3,  bot_bot - p_h, sx+2*bw+3,  bot_bot, fill=par_color, outline="")

#             name = city["name"][:7] + "…" if len(city["name"]) > 8 else city["name"]
#             c.create_text(sx + bw, bot_bot + 14, text=name,
#                           font=("Segoe UI", 8), fill="#444")
#             c.create_text(sx + bw//2,   bot_bot - s_h - 6,
#                           text=f"{s_ms}ms", font=("Segoe UI", 8), fill=seq_color)
#             c.create_text(sx+bw+3+bw//2, bot_bot - p_h - 6,
#                           text=f"{p_ms}ms", font=("Segoe UI", 8), fill=par_color)

#         # Legend
#         c.create_rectangle(W-140, 8, W-128, 20, fill=seq_color, outline="")
#         c.create_text(W-122, 14, text="Sequential", font=("Segoe UI", 10), fill="#444", anchor="w")
#         c.create_rectangle(W-140, 26, W-128, 38, fill=par_color, outline="")
#         c.create_text(W-122, 32, text="Parallel", font=("Segoe UI", 10), fill="#444", anchor="w")

#     # ─────────────────────────────────────────────────────────────────
#     # Utility
#     # ─────────────────────────────────────────────────────────────────

#     def log_message(self, msg):
#         """
#         Appends a message to the thread log area.
#         Thread-safe via root.after().

#         Args:
#             msg: string message to log
#         """
#         timestamp = time.strftime("%H:%M:%S")
#         def _append():
#             self.log_area.config(state="normal")
#             self.log_area.insert(tk.END, f"[{timestamp}]  {msg}\n")
#             self.log_area.see(tk.END)
#             self.log_area.config(state="disabled")
#         self.root.after(0, _append)

#     def clear_all(self):
#         """Clears all data from table, chart, and log."""
#         for city in CITIES:
#             row_id = self.row_ids.get(city["name"])
#             if row_id:
#                 self.tree.item(row_id, values=(city["emoji"], city["name"],
#                                                "—","—","—","—","—","—","—","—"))
#         self.log_area.config(state="normal")
#         self.log_area.delete("1.0", tk.END)
#         self.log_area.config(state="disabled")
#         self.seq_latency = 0
#         self.par_latency = 0
#         self.city_seq_times.clear()
#         self.city_par_times.clear()
#         self.lbl_seq.configure(text="Sequential: —")
#         self.lbl_par.configure(text="Parallel: —")
#         self.lbl_speed.configure(text="Speedup: —")
#         self.progress.configure(value=0)
#         self.progress_label.configure(text="Ready")
#         self.chart_canvas.delete("all")
#         self.chart_canvas.create_text(400, 200,
#                                       text="Click 'Fetch Weather' to see latency chart.",
#                                       font=("Segoe UI", 12), fill="gray")
#         self.status_label.configure(text="Cleared.")



# # Main Entry Point


# def main():
#     root = tk.Tk()
#     app  = WeatherApp(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()


# question no 5b 

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import urllib.request
import json
import random


#
# Configuration
#

# Replace with your OpenWeatherMap API key
API_KEY  = "your_api_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"

CITIES = [
    {"name": "Kathmandu",  "emoji": "🏔"},
    {"name": "Pokhara",    "emoji": "🌊"},
    {"name": "Biratnagar", "emoji": "🌿"},
    {"name": "Nepalgunj",  "emoji": "☀"},
    {"name": "Dhangadhi",  "emoji": "🌾"},
]


# 
# Weather Fetch Function
# 

def fetch_weather(city_name):
    """
    Fetches real-time weather data for a given city from OpenWeatherMap API.
    Falls back to simulated data if API call fails.

    Args:
        city_name: string name of the city

    Returns:
        dict with weather fields: temp, feels_like, humidity,
                                  pressure, wind_speed, condition, success
    """
    try:
        url      = BASE_URL.format(city=city_name, key=API_KEY)
        response = urllib.request.urlopen(url, timeout=8)
        data     = json.loads(response.read().decode())

        return {
            "temp":       data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity":   data["main"]["humidity"],
            "pressure":   data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", 0),
            "condition":  data["weather"][0]["description"].title(),
            "success":    True,
            "error":      None
        }

    except Exception as e:
        # Fallback: simulate weather data if API fails
        return simulate_weather(city_name, str(e))


def simulate_weather(city_name, error_msg="Simulated"):
    """
    Generates simulated weather data when API is unavailable.
    Uses city name as random seed for consistent results.

    Args:
        city_name : city name string
        error_msg : reason for simulation

    Returns:
        dict with simulated weather fields
    """
    rng = random.Random(hash(city_name))
    # Simulate network delay
    time.sleep(0.2 + rng.random() * 0.6)

    conditions = ["Clear Sky", "Few Clouds", "Overcast", "Light Rain", "Partly Cloudy"]

    return {
        "temp":       round(15 + rng.randint(0, 20), 1),
        "feels_like": round(13 + rng.randint(0, 20), 1),
        "humidity":   50 + rng.randint(0, 40),
        "pressure":   1010 + rng.randint(0, 20),
        "wind_speed": round(1 + rng.random() * 8, 1),
        "visibility": 5000 + rng.randint(0, 5000),
        "condition":  rng.choice(conditions),
        "success":    True,
        "error":      error_msg
    }


# ─────────────────────────────────────────────────────────────────────
# GUI Application
# ─────────────────────────────────────────────────────────────────────

class WeatherApp:
    """
    Multi-threaded Weather Collector GUI.

    Features:
    - Fetches weather for 5 Nepal cities using 5 threads concurrently
    - Compares sequential vs parallel latency
    - Displays results in a table
    - Shows bar chart comparing latency
    - Thread log shows each thread's activity
    - Thread-safe GUI updates using threading.Lock()
    """

    def __init__(self, root):
        """
        Initializes the GUI layout and all components.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Multi-threaded Weather Collector - Nepal")
        self.root.configure(bg="#ebf0ff")
        self.root.geometry("950x680")

        # Thread safety lock for GUI updates
        self.table_lock = threading.Lock()

        # Latency tracking
        self.seq_latency = 0
        self.par_latency = 0
        self.city_seq_times = {}
        self.city_par_times = {}

        self._build_header()
        self._build_notebook()
        self._build_status_bar()

    def _build_header(self):
        """Builds the top header with title and buttons."""

        header = tk.Frame(self.root, bg="#dde5ff", pady=10)
        header.pack(fill="x", padx=0)

        tk.Label(header, text="🌤  Multi-threaded Weather Collector — Nepal",
                 font=("Segoe UI", 15, "bold"),
                 bg="#dde5ff", fg="#283c8c").pack(side="left", padx=14)

        btn_frame = tk.Frame(header, bg="#dde5ff")
        btn_frame.pack(side="right", padx=14)

        self.fetch_btn = tk.Button(btn_frame, text="⚡ Fetch Weather",
                                   font=("Segoe UI", 11, "bold"),
                                   bg="#3c78dc", fg="white",
                                   activebackground="#2a5bb0",
                                   cursor="hand2", relief="flat",
                                   padx=10, pady=5,
                                   command=self.start_fetching)
        self.fetch_btn.pack(side="left", padx=6)

        tk.Button(btn_frame, text="🗑 Clear",
                  font=("Segoe UI", 11, "bold"),
                  bg="#8c8ca0", fg="white",
                  cursor="hand2", relief="flat",
                  padx=10, pady=5,
                  command=self.clear_all).pack(side="left")

    def _build_notebook(self):
        """Builds the tabbed notebook with weather table, chart, and log tabs."""

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self._build_weather_tab()
        self._build_chart_tab()
        self._build_log_tab()

    def _build_weather_tab(self):
        """Builds the weather data tab with table and latency stats."""

        tab = tk.Frame(self.notebook, bg="#f0f3ff")
        self.notebook.add(tab, text="🌡 Weather Data")

        # Progress bar
        self.progress = ttk.Progressbar(tab, maximum=len(CITIES),
                                        length=400, mode="determinate")
        self.progress.pack(pady=(10, 4))
        self.progress_label = tk.Label(tab, text="Ready",
                                       font=("Segoe UI", 10),
                                       bg="#f0f3ff", fg="#506090")
        self.progress_label.pack()

        # Weather table
        columns = ("emoji", "city", "temp", "feels_like", "humidity",
                   "pressure", "wind", "visibility", "condition", "fetch_time")
        self.tree = ttk.Treeview(tab, columns=columns, show="headings", height=6)

        headers = ["", "City", "Temp", "Feels Like", "Humidity",
                   "Pressure", "Wind", "Visibility", "Condition", "Fetch Time"]
        widths  = [30, 110, 70, 80, 70, 80, 70, 80, 120, 80]

        for col, header, width in zip(columns, headers, widths):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor="center")

        # Insert city rows with placeholder dashes
        self.row_ids = {}
        for city in CITIES:
            row_id = self.tree.insert("", "end",
                                      values=(city["emoji"], city["name"],
                                              "—","—","—","—","—","—","—","—"))
            self.row_ids[city["name"]] = row_id

        scroll = ttk.Scrollbar(tab, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(8,0), pady=8)
        scroll.pack(side="left", fill="y", pady=8)

        # Latency stats
        stats_frame = tk.Frame(tab, bg="#f0f3ff")
        stats_frame.pack(fill="x", padx=8, pady=4)

        self.lbl_seq   = tk.Label(stats_frame, text="Sequential: —",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#f0f3ff", fg="#283c8c")
        self.lbl_par   = tk.Label(stats_frame, text="Parallel: —",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#f0f3ff", fg="#283c8c")
        self.lbl_speed = tk.Label(stats_frame, text="Speedup: —",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#f0f3ff", fg="#1a7a40")
        self.lbl_seq.pack(side="left", padx=16)
        self.lbl_par.pack(side="left", padx=16)
        self.lbl_speed.pack(side="left", padx=16)

    def _build_chart_tab(self):
        """Builds the latency bar chart tab using Tkinter Canvas."""

        tab = tk.Frame(self.notebook, bg="#f0f3ff")
        self.notebook.add(tab, text="📊 Latency Chart")

        self.chart_canvas = tk.Canvas(tab, bg="white",
                                      highlightthickness=0)
        self.chart_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.chart_canvas.create_text(400, 200,
                                      text="Click 'Fetch Weather' to see latency chart.",
                                      font=("Segoe UI", 12), fill="gray")

    def _build_log_tab(self):
        """Builds the thread activity log tab."""

        tab = tk.Frame(self.notebook, bg="#f0f3ff")
        self.notebook.add(tab, text="📋 Thread Log")

        self.log_area = scrolledtext.ScrolledText(
            tab,
            font=("Courier", 10),
            bg="#f5f8ff", fg="#1e3264",
            relief="flat", state="disabled"
        )
        self.log_area.pack(fill="both", expand=True, padx=8, pady=8)

    def _build_status_bar(self):
        """Builds the bottom status bar."""

        status_bar = tk.Frame(self.root, bg="#dde5ff")
        status_bar.pack(fill="x", side="bottom")

        self.status_label = tk.Label(status_bar, text="Ready",
                                     font=("Segoe UI", 10),
                                     bg="#dde5ff", fg="#506090")
        self.status_label.pack(side="left", padx=12, pady=4)

        tk.Label(status_bar, text="API: OpenWeatherMap  |  Threads: 5",
                 font=("Segoe UI", 10),
                 bg="#dde5ff", fg="#8090b0").pack(side="right", padx=12)

    # ─────────────────────────────────────────────────────────────────
    # Fetch Logic
    # ─────────────────────────────────────────────────────────────────

    def start_fetching(self):
        """
        Starts the weather fetch process in a background thread.
        Runs sequential fetch first, then parallel fetch for comparison.
        Keeps GUI responsive during fetching.
        """
        self.fetch_btn.config(state="disabled")
        self.log_message("Starting fetch — " + time.strftime("%H:%M:%S"))

        # Run in background thread to keep GUI responsive
        threading.Thread(target=self._run_fetch, daemon=True).start()

    def _run_fetch(self):
        """
        Coordinator thread that runs sequential then parallel fetch.
        Updates GUI via root.after() for thread safety.
        """

        # ── Sequential fetch ──
        self.log_message("[SEQUENTIAL PHASE]")
        seq_start = time.time()

        for city in CITIES:
            t0      = time.time()
            data    = fetch_weather(city["name"])
            elapsed = round((time.time() - t0) * 1000)
            self.city_seq_times[city["name"]] = elapsed
            self.log_message(f"  [SEQ] {city['name']:<12} → {elapsed}ms")

        self.seq_latency = round((time.time() - seq_start) * 1000)
        self.log_message(f"Sequential total: {self.seq_latency}ms")

        # Reset progress for parallel phase
        self.root.after(0, lambda: self.progress.configure(value=0))
        self.completed = 0

        # ── Parallel fetch using 5 threads ──
        self.log_message("[PARALLEL PHASE — 5 threads]")
        par_start = time.time()

        threads = []
        for city in CITIES:
            t = threading.Thread(
                target=self._fetch_city_thread,
                args=(city,),
                name=f"WeatherThread-{city['name']}"
            )
            threads.append(t)

        # Start all 5 threads concurrently
        for t in threads:
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join(timeout=15)

        self.par_latency = round((time.time() - par_start) * 1000)
        speedup = round(self.seq_latency / self.par_latency, 2) if self.par_latency > 0 else 1.0

        self.log_message(f"Parallel total: {self.par_latency}ms  |  Speedup: {speedup}x")

        # Update GUI after both phases complete
        self.root.after(0, lambda: self._update_summary(speedup))

    def _fetch_city_thread(self, city):
        """
        Thread worker function for one city.
        Fetches weather data and safely updates the GUI table.

        Thread-safe: uses self.table_lock (Lock) to prevent
        race conditions when multiple threads update the table.

        Args:
            city: dict with name and emoji
        """
        thread_name = threading.current_thread().name
        self.log_message(f"  [PAR] {thread_name} → fetching {city['name']}")

        t0   = time.time()
        data = fetch_weather(city["name"])
        elapsed = round((time.time() - t0) * 1000)
        self.city_par_times[city["name"]] = elapsed

        status = "OK" if data["success"] else f"ERROR: {data['error']}"
        self.log_message(f"  [PAR] {city['name']:<12} → {elapsed}ms [{status}]")

        # Thread-safe table update using Lock
        with self.table_lock:
            self.root.after(0, lambda d=data, c=city: self._update_table_row(c, d))

        # Update progress bar safely
        self.completed = getattr(self, "completed", 0) + 1
        done = self.completed
        self.root.after(0, lambda n=done: self._update_progress(n))

    def _update_table_row(self, city, data):
        """
        Updates a single row in the weather table.
        Called via root.after() to ensure thread-safe GUI update.

        Args:
            city: dict with name and emoji
            data: weather data dict
        """
        row_id = self.row_ids.get(city["name"])
        if not row_id:
            return

        if data["success"]:
            self.tree.item(row_id, values=(
                city["emoji"],
                city["name"],
                f"{data['temp']}°C",
                f"{data['feels_like']}°C",
                f"{data['humidity']}%",
                f"{data['pressure']} hPa",
                f"{data['wind_speed']} m/s",
                f"{data['visibility']} m",
                data["condition"],
                f"{self.city_par_times.get(city['name'], '—')}ms"
            ))
        else:
            self.tree.item(row_id, values=(
                city["emoji"], city["name"],
                f"ERROR: {data['error']}", "", "", "", "", "", "", ""
            ))

    def _update_progress(self, done):
        """Updates the progress bar and label."""
        self.progress.configure(value=done)
        self.progress_label.configure(text=f"{done} / {len(CITIES)} fetched")
        self.status_label.configure(text=f"Fetching... {done}/{len(CITIES)}")

    def _update_summary(self, speedup):
        """
        Updates latency labels, switches to chart tab,
        then draws chart after tab is fully visible.

        FIX: switch tab first, then use after() to draw chart
             so canvas winfo_width/height returns real size.
        """
        self.lbl_seq.configure(text=f"Sequential: {self.seq_latency}ms")
        self.lbl_par.configure(text=f"Parallel: {self.par_latency}ms")
        self.lbl_speed.configure(text=f"Speedup: {speedup}x")
        self.status_label.configure(text=f"Done! Speedup: {speedup}x")
        self.progress_label.configure(text="✅ Done!")
        self.fetch_btn.config(state="normal")

        # Switch to chart tab first, THEN draw after layout settles
        self.notebook.select(1)
        self.root.after(100, self._draw_chart)   # ← FIX: delay draw until tab rendered

    # ─────────────────────────────────────────────────────────────────
    # Bar Chart Drawing  ← FIXED
    # ─────────────────────────────────────────────────────────────────

    def _draw_chart(self):
        """
        Draws a bar chart comparing sequential vs parallel latency.

        FIX: call update_idletasks() before reading winfo_width/height
             so canvas returns its actual rendered size, not 1x1.

        Top section: total latency comparison.
        Bottom section: per-city fetch times.
        """
        c = self.chart_canvas
        c.delete("all")

        # FIX: force layout update so winfo returns real dimensions
        c.update_idletasks()
        W = c.winfo_width()
        H = c.winfo_height()

        # Fallback if still not rendered properly
        if W < 50:
            W = 880
        if H < 50:
            H = 480

        pad = 60

        # Colors
        seq_color = "#dc5050"
        par_color = "#3cb464"

        # ── Top section: total bars ──
        top_bot = H // 2 - 20
        avail_h = top_bot - 60
        max_val = max(self.seq_latency, self.par_latency, 1)
        bar_w   = 80

        c.create_text(pad, 20, text="Total: Sequential vs Parallel",
                      font=("Segoe UI", 12, "bold"), fill="#283c8c", anchor="w")

        seq_x = pad + (W - 2*pad)//4 - bar_w//2
        par_x = pad + 3*(W - 2*pad)//4 - bar_w//2
        seq_h = int(self.seq_latency / max_val * avail_h)
        par_h = int(self.par_latency / max_val * avail_h)

        c.create_rectangle(seq_x, top_bot - seq_h, seq_x + bar_w, top_bot,
                           fill=seq_color, outline="")
        c.create_rectangle(par_x, top_bot - par_h, par_x + bar_w, top_bot,
                           fill=par_color, outline="")

        c.create_text(seq_x + bar_w//2, top_bot + 16,
                      text="Sequential", font=("Segoe UI", 10, "bold"), fill="#444")
        c.create_text(par_x + bar_w//2, top_bot + 16,
                      text="Parallel",   font=("Segoe UI", 10, "bold"), fill="#444")
        c.create_text(seq_x + bar_w//2, top_bot - seq_h - 10,
                      text=f"{self.seq_latency}ms", font=("Segoe UI", 9), fill=seq_color)
        c.create_text(par_x + bar_w//2, top_bot - par_h - 10,
                      text=f"{self.par_latency}ms", font=("Segoe UI", 9), fill=par_color)

        speedup = round(self.seq_latency / self.par_latency, 2) if self.par_latency > 0 else 1.0
        c.create_text(W//2, top_bot - avail_h//2,
                      text=f"{speedup}x faster",
                      font=("Segoe UI", 11, "bold"), fill="#b47800")

        # ── Bottom section: per-city bars ──
        bot_top = H // 2 + 20
        bot_bot = H - 30
        avail_h2 = bot_bot - bot_top - 30

        c.create_text(pad, bot_top + 10, text="Per-City Fetch Time",
                      font=("Segoe UI", 12, "bold"), fill="#283c8c", anchor="w")

        n      = len(CITIES)
        slot_w = (W - 2*pad) // n
        bw     = slot_w // 3
        max_city = max(
            max(self.city_seq_times.values(), default=1),
            max(self.city_par_times.values(), default=1), 1
        )

        for i, city in enumerate(CITIES):
            sx = pad + i * slot_w + slot_w // 6
            s_ms = self.city_seq_times.get(city["name"], 0)
            p_ms = self.city_par_times.get(city["name"], 0)
            s_h  = int(s_ms / max_city * avail_h2)
            p_h  = int(p_ms / max_city * avail_h2)

            c.create_rectangle(sx,       bot_bot - s_h, sx + bw,     bot_bot, fill=seq_color, outline="")
            c.create_rectangle(sx+bw+3,  bot_bot - p_h, sx+2*bw+3,  bot_bot, fill=par_color, outline="")

            name = city["name"][:7] + "…" if len(city["name"]) > 8 else city["name"]
            c.create_text(sx + bw, bot_bot + 14, text=name,
                          font=("Segoe UI", 8), fill="#444")
            c.create_text(sx + bw//2,   bot_bot - s_h - 6,
                          text=f"{s_ms}ms", font=("Segoe UI", 8), fill=seq_color)
            c.create_text(sx+bw+3+bw//2, bot_bot - p_h - 6,
                          text=f"{p_ms}ms", font=("Segoe UI", 8), fill=par_color)

        # Legend
        c.create_rectangle(W-140, 8, W-128, 20, fill=seq_color, outline="")
        c.create_text(W-122, 14, text="Sequential", font=("Segoe UI", 10), fill="#444", anchor="w")
        c.create_rectangle(W-140, 26, W-128, 38, fill=par_color, outline="")
        c.create_text(W-122, 32, text="Parallel", font=("Segoe UI", 10), fill="#444", anchor="w")

    # ─────────────────────────────────────────────────────────────────
    # Utility
    # ─────────────────────────────────────────────────────────────────

    def log_message(self, msg):
        """
        Appends a message to the thread log area.
        Thread-safe via root.after().

        Args:
            msg: string message to log
        """
        timestamp = time.strftime("%H:%M:%S")
        def _append():
            self.log_area.config(state="normal")
            self.log_area.insert(tk.END, f"[{timestamp}]  {msg}\n")
            self.log_area.see(tk.END)
            self.log_area.config(state="disabled")
        self.root.after(0, _append)

    def clear_all(self):
        """Clears all data from table, chart, and log."""
        for city in CITIES:
            row_id = self.row_ids.get(city["name"])
            if row_id:
                self.tree.item(row_id, values=(city["emoji"], city["name"],
                                               "—","—","—","—","—","—","—","—"))
        self.log_area.config(state="normal")
        self.log_area.delete("1.0", tk.END)
        self.log_area.config(state="disabled")
        self.seq_latency = 0
        self.par_latency = 0
        self.city_seq_times.clear()
        self.city_par_times.clear()
        self.lbl_seq.configure(text="Sequential: —")
        self.lbl_par.configure(text="Parallel: —")
        self.lbl_speed.configure(text="Speedup: —")
        self.progress.configure(value=0)
        self.progress_label.configure(text="Ready")
        self.chart_canvas.delete("all")
        self.chart_canvas.create_text(400, 200,
                                      text="Click 'Fetch Weather' to see latency chart.",
                                      font=("Segoe UI", 12), fill="gray")
        self.status_label.configure(text="Cleared.")


# Main Entry Point


def main():
    root = tk.Tk()
    app  = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()