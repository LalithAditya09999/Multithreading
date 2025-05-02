Python Multithreading and Concurrency Projects
This repository showcases three Python projects that demonstrate how to use multithreading and concurrency for performance optimization in sorting algorithms and file downloading.

Project Structure

File	Description
Task_1.py	Merge sort implementation comparing single-threaded and multithreaded performance using ThreadPoolExecutor.
Task_2.py	Quick sort implementation using manual thread splitting to parallelize sorting operations.
Task_3.py	A command-line file downloader that compares sequential and multithreaded file downloads using Python’s threading module.
 
Features

Multithreaded Sorting: Boosts sorting speed for large datasets using parallel computation.
Concurrent File Downloading: Downloads multiple files simultaneously, reducing total time for I/O-bound operations.
Performance Comparison: Each task includes timing output to show the speedup from multithreading.
No External Dependencies: All scripts use only Python’s standard libraries.

Sample Output
Example output from Task_1.py:
Single-threaded sort time: 3.28 seconds
Multi-threaded sort time: 1.22 seconds
Example output from Task_3.py:

Sequential download finished: 5/5 files in 20.44 seconds
Threaded download completed: 5/5 files in 6.93 seconds
Speedup: 2.95x

Learning Objectives

Understand the differences between CPU-bound and I/O-bound tasks.
Learn how Python's threading and concurrent.futures modules work.
Explore the performance impact of multithreading on different problem types.

