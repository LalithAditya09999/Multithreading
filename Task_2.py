import threading
import time
import random

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

class ThreadedQuicksort(threading.Thread):
    def __init__(self, arr, num_threads):
        super().__init__()
        self.arr = arr
        self.sorted_arr = []
        self.num_threads = num_threads

    def run(self):
        self.sorted_arr = multi_threaded_quicksort(self.arr, self.num_threads)

def multi_threaded_quicksort(arr, num_threads=2):
    if len(arr) <= 1:
        return arr
    if num_threads <= 1 or len(arr) < 10000:
        return quicksort(arr)

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    threads = []
    left_thread = ThreadedQuicksort(left, num_threads // 2)
    right_thread = ThreadedQuicksort(right, num_threads // 2)

    left_thread.start()
    right_thread.start()

    left_thread.join()
    right_thread.join()

    return left_thread.sorted_arr + middle + right_thread.sorted_arr

def generate_random_list(size):
    return [random.randint(0, 10000) for _ in range(size)]

def compare_sorting_methods(size):
    arr = generate_random_list(size)

    start_time = time.time()
    sorted_single = quicksort(arr)
    single_thread_time = time.time() - start_time

    start_time = time.time()
    sorted_multi = multi_threaded_quicksort(arr, num_threads=4)
    multi_thread_time = time.time() - start_time

    print(f"Single-threaded sort time: {single_thread_time:.4f} seconds")
    print(f"Multi-threaded sort time: {multi_thread_time:.4f} seconds")
    assert sorted_single == sorted_multi, "Error: outputs do not match!"

compare_sorting_methods(100000)