# Comparative Analysis of Sorting Algorithms in Python

[![Language](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Visualization](https://img.shields.io/badge/Visualization-Matplotlib-orange.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An empirical benchmarking and performance evaluation suite for classic and modern sorting algorithms implemented in Python. 

This project measures, aggregates, and visualizes runtime performance across diverse input sizes ($N$) and data distributions (Random, Sorted, Reverse Sorted, Nearly Sorted) to compare theoretical Big-O complexity against practical execution metrics.

---

## 📊 Implemented Algorithms & Complexity

| Algorithm | Best Case | Average Case | Worst Case | Space Complexity | Paradigm |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Comparison / Brute-force |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Comparison / In-place |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Comparison / Incremental |
| **Shell Sort** | $O(n \log n)$ | $O(n^{4/3})$ | $O(n^{3/2})$ | $O(1)$ | Diminishing Increment |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Divide & Conquer |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | Divide & Conquer / Partitioning |
| **Heap Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | Tree Selection / Heap structure |
| **Counting Sort** | $O(n + k)$ | $O(n + k)$ | $O(n + k)$ | $O(k)$ | Non-Comparison / Key Index |
| **Radix Sort** | $O(nk)$ | $O(nk)$ | $O(nk)$ | $O(n + k)$ | Non-Comparison / Positional |

---

## 🔄 Benchmark Pipeline

```text
┌──────────────┐       ┌─────────────────┐       ┌─────────────┐
│   sort.py    │ ────► │  merge_data.py  │ ────► │  charts.py  │
└──────────────┘       └─────────────────┘       └─────────────┘
  Runs sorting           Aggregates & cleans       Generates line charts
  benchmarks over        raw benchmark CSVs        & comparative plots
  various input sets     into structured metrics   (Time vs. Dataset Size)
```

---

## 📁 Repository Structure

```text
.
├── sort.py           # Core sorting implementations and benchmarking engine
├── merge_data.py     # Aggregation script for raw benchmark output files
├── charts.py         # Data visualization and plotting script
├── requirements.txt  # Project dependencies (matplotlib, pandas, etc.)
└── README.md         # Project documentation
```

---

## ⚙️ Prerequisites & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/Comparative-Analysis-of-Sorting-Algorithms-in-Python.git](https://github.com/your-username/Comparative-Analysis-of-Sorting-Algorithms-in-Python.git)
   cd Comparative-Analysis-of-Sorting-Algorithms-in-Python
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Or install directly: `pip install matplotlib pandas numpy`)*

---

## 🚀 Usage & Reproduction

### 1. Run Sorting Benchmarks
Execute the benchmarking suite across all algorithms and dataset variations:
```bash
python sort.py
```

### 2. Aggregate Benchmark Results
Merge separate dataset runs into consolidated metric tables:
```bash
python merge_data.py
```

### 3. Generate Comparison Charts
Produce performance visualization graphs:
```bash
python charts.py
```
Generated plots will display runtime curves ($N$ vs. Execution Time in milliseconds/seconds) comparing empirical scaling with theoretical upper bounds.

---

## 🛠️ Technologies & Concepts

- **Language:** Python 3
- **Data Structures & Algorithms (DSA):** Time & Space Complexity Analysis, Recursion, In-Place vs. Out-of-Place Sorting, Stability.
- **Data Analysis & Visualization:** Matplotlib, Pandas / NumPy.
- **Empirical Profiling:** High-resolution timing metrics (`time.perf_counter`), automated experiment orchestration.

---
