import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

os.makedirs("output", exist_ok=True)

df = pd.read_csv("final_dataset.csv")
df["Time (seconds)"] = pd.to_numeric(df["Time (seconds)"], errors="coerce")
df["Memory (KB)"]    = pd.to_numeric(df["Memory (KB)"],    errors="coerce")


# =============================================================================
# ΑΛΛΑΖΕΙΣ ΜΟΝΟ ΑΥΤΑ
# =============================================================================

# Ενας η περισσοτεροι αλγοριθμοι
ALGORITHMS = [
    "Quick Sort",
    "Merge Sort",
    "Heap Sort",
]



# Μια η περισσοτερες περιπτωσεις: "Best", "Random", "Worst"
CASES = ["Worst"]
# CASES = ["Best", "Random", "Worst"] 


# None = ολα τα N | Λιστα = συγκεκριμενα, π.χ. [1000, 10000]
#N_VALUES = None
#N_VALUES = [1000, 10000, 100000, 1000000]
N_VALUES = [1000]


LOG_SCALE = True



OUTPUT_TIME   = "output/chart_time.png"
OUTPUT_MEMORY = "output/chart_memory.png"









# =============================================================================
# ΛΟΓΙΚΗ (μην αλλαζεις)
# =============================================================================
filtered = df[
    df["Algorithm"].isin(ALGORITHMS) &
    df["Input Case"].isin(CASES)
]
if N_VALUES is not None:
    filtered = filtered[filtered["Array Size"].isin(N_VALUES)]

available_n   = sorted(filtered["Array Size"].dropna().unique())
single_n      = len(available_n) == 1
single_case   = len(CASES) == 1
single_algo   = len(ALGORITHMS) == 1

# Αποφαση: τι γινεται label σε καθε γραμμη/μπαρα
# - πολλοι αλγοριθμοι + 1 case  -> label = αλγοριθμος
# - 1 αλγοριθμος + πολλα cases  -> label = case
# - πολλοι αλγοριθμοι + πολλα cases -> label = "Αλγοριθμος (Case)"
def get_label(algo, case):
    if single_case:
        return algo
    elif single_algo:
        return case
    else:
        return f"{algo} ({case})"

combinations = [(a, c) for c in CASES for a in ALGORITHMS]


def make_chart(metric, ylabel, output_path, bar_color_key):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    color_map = {combo: colors[i % len(colors)] for i, combo in enumerate(combinations)}

    if single_n:
        # Bar chart
        n_val   = available_n[0]
        labels  = []
        values  = []
        clrs    = []
        for algo, case in combinations:
            row = filtered[
                (filtered["Algorithm"] == algo) &
                (filtered["Input Case"] == case) &
                (filtered["Array Size"] == n_val)
            ][metric].dropna()
            if row.empty:
                continue
            labels.append(get_label(algo, case))
            values.append(row.values[0])
            clrs.append(color_map[(algo, case)])

        bars = ax.bar(labels, values, color=clrs, edgecolor="white")
        fmt  = "%.4f" if metric == "Time (seconds)" else "%.1f"
        ax.bar_label(bars, fmt=fmt, padding=3, fontsize=9)
        plt.xticks(rotation=20, ha="right")
        ax.set_xlabel("Αλγοριθμος", fontsize=12)
        cases_str = ", ".join(CASES)
        title = f"{ylabel} — {cases_str} Case (N={n_val:,})"

    else:
        # Line chart
        for algo, case in combinations:
            sub = filtered[
                (filtered["Algorithm"] == algo) &
                (filtered["Input Case"] == case)
            ].dropna(subset=[metric]).sort_values("Array Size")
            if sub.empty:
                continue
            ax.plot(
                sub["Array Size"], sub[metric],
                marker="o", linewidth=2,
                label=get_label(algo, case),
                color=color_map[(algo, case)]
            )
        if LOG_SCALE:
            ax.set_xscale("log")
            ax.set_yscale("log")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.set_xlabel("Μεγεθος πινακα (N)", fontsize=12)
        ax.legend(fontsize=10, loc="upper left")
        cases_str = ", ".join(CASES)
        algos_str = ", ".join(ALGORITHMS) if single_algo else f"{len(ALGORITHMS)} αλγοριθμοι"
        title = f"{ylabel} — {cases_str} | {algos_str}"

    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"OK: {output_path}")


make_chart("Time (seconds)", "Χρονος εκτελεσης (sec)", OUTPUT_TIME,   "blue")
make_chart("Memory (KB)",    "Μνημη (KB)",             OUTPUT_MEMORY, "orange")
