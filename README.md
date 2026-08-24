# Comparative Analysis of Sorting Algorithms in Python

[![Language](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An empirical benchmarking and performance evaluation suite for sorting algorithms in Python, developed alongside an extensive **50+ page research thesis**.

This project implements, tests, and profiles multiple sorting algorithms across varying dataset sizes and input distributions (random, sorted, reverse, nearly sorted) to evaluate practical execution behavior against theoretical bounds.

---

## 📄 Comprehensive Thesis & Research

For an in-depth theoretical breakdown, mathematical proofs, experimental methodology, and detailed graphical analysis, refer to the included **Thesis document**:

* 📖 **[View the Full Thesis Document (PDF)](./thesis.pdf)** *(ή βάλε το ακριβές όνομα του αρχείου σου)*
* **Scope:** 50+ pages covering algorithm classification, runtime profiling, hardware impact, and comparative benchmarking results.

---

## 📌 Features & Implemented Algorithms

The benchmark suite includes implementations and performance profiling for:

* **Comparison-based:** Bubble Sort, Selection Sort, Insertion Sort, Shell Sort
* **Divide & Conquer:** Merge Sort, Quick Sort
* **Heap-based:** Heap Sort
* **Non-comparison:** Counting Sort, Radix Sort

---

## 🚀 How to Run

### 1. Requirements
Ensure Python 3 is installed. If you plan to generate plots using the auxiliary scripts, install `matplotlib`:

```bash
pip install matplotlib
```

### 2. Run the Main Benchmark
The primary engine is `sort.py`. Run it to execute all sorting algorithms and record timing metrics:

```bash
python sort.py
```

### 3. Auxiliary Tools (Data Merging & Chart Generation)
If you want to aggregate separate benchmark outputs and generate comparative visualization plots:

```bash
# Merge raw benchmark data
python merge_data.py

# Generate comparison plots and charts
python charts.py
```

---

## 📁 Repository Structure

```text
.
├── sort.py           # Main script: Sorting implementations & benchmarking engine
├── merge_data.py     # Auxiliary script: Aggregates raw benchmark metrics
├── charts.py         # Auxiliary script: Generates performance graphs
├── thesis.pdf        # Complete 50+ page research thesis and analysis
└── README.md         # Project documentation
```

---

## 🛠️ Skills & Technologies

* **Programming:** Python 3
* **Algorithms & Data Structures:** Sorting algorithms, algorithmic complexity, profiling.
* **Research & Analysis:** Empirical benchmarking, experimental evaluation, technical writing.
