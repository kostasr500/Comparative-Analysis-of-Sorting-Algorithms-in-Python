# Comparative Analysis of Sorting Algorithms in Python

This repository holds the code behind my thesis, where I benchmarked classic sorting algorithms in Python and compared their real-world runtime and memory behavior across different input sizes and data distributions (random, sorted, reversed, etc.).

The goal wasn't just to implement the algorithms, but to actually measure how they perform under different conditions and see how well that matches the theoretical time complexity everyone learns in textbooks.

## Algorithms covered

The benchmark suite implements 37 sorting algorithm implementations in total (30 pure Python implementations + 7 C-accelerated / alternative variants):

- **Simple Comparison Sorts:** Bubble Sort, Selection Sort, Insertion Sort, Gnome Sort, Cocktail Shaker Sort, Cycle Sort, Pancake Sort, Stooge Sort
- **Advanced Comparison Sorts:** Merge Sort, Quick Sort, Heap Sort, Shell Sort, Comb Sort, Smooth Sort, Strand Sort, Tree Sort, Cartesian Tree Sort, Tournament Sort, Patience Sort
- **Sorting Networks:** Bitonic Sort, Pairwise Sorting Network
- **Hybrid & Composite Sorts:** Simplified Tim Sort, Intro Sort, Block Sort, Merge-Insertion Sort
- **Non-Comparison Sorts:** Counting Sort, Radix Sort, Bucket Sort, Pigeonhole Sort, Flash Sort
- **C-Accelerated Variants (Alt):** Block Sort (Alt), Bucket Sort (Alt), Cartesian Tree Sort (Alt), Merge-Insertion Sort (Alt), Patience Sort (Alt), Tournament Sort (Alt), Tim Sort (Built-in)

## Repository structure

```
.
├── sort.py                          # Main script: implementations of all sorting algorithms + benchmarking (time & memory)
├── merge_data.py                    # Combines the raw benchmark results into a single dataset
├── charts.py                        # Generates comparison plots from the merged data
└── Πτυχιακή_Ρομπόκας - 2.pdf        # Full thesis document
```

## How to run it

**1. Requirements**

You need Python 3. If you also want to generate the plots, install matplotlib:

```bash
pip install matplotlib
```

**2. Run the benchmark**

`sort.py` is the main script — it presents a menu of all 37 algorithms (plus a "run all" option) and records timing (and memory, where applicable):

```bash
python sort.py
```

**3. Merge results and build charts**

```bash
python merge_data.py
python charts.py
```

## Thesis

The full write-up, including the methodology behind the benchmarks, the theoretical background for each algorithm, and the analysis of the results, is in **[`Thesis_GR.pdf`](./Thesis_GR.pdf)**.

