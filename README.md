# Comparative-Analysis-of-Sorting-Algorithms-in-Python (BSc Thesis Project)

This is the code from my bachelor's thesis. The idea was to compare how 30+ sorting algorithms actually perform in Python, not just in theory, but in real runtime and memory usage, across array sizes from a few thousand up to over a million elements.

## Files

**sort.py** — the main script. Contains all the sorting algorithms plus the benchmarking logic: timing each run, tracking peak memory with tracemalloc, handling timeouts for algorithms that take too long (like Bubble Sort on 1M elements), and raising the recursion limit for the more recursive algorithms.
**merge_data.py** — each benchmark run saves its own CSV file. This script collects all of them and merges everything into one clean dataset.
**charts.py** — takes the merged dataset and generates comparison charts (time and memory, per algorithm) using matplotlib.

## How it works

Run sort.py, point it at a CSV file of numbers, and pick an algorithm from the menu (or run all of them at once with option 99). Each run gets timed, memory-profiled, and logged to a results file. Once you've run what you need, merge_data.py combines the results, and charts.py turns them into graphs.

## About the thesis

I'm defending this thesis soon. The full written part covering the methodology and results in detail will go up here once the defense is done. For now, this repo is just the code.
