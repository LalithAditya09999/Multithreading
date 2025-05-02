import time
import random
from concurrent.futures import ThreadPoolExecutor

def merge(left, right):
    result = []
    i = j = 0
    len_left, len_right = len(left), len(right)
    while i < len_left and j < len_right:
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def threaded_merge_sort(arr, num_threads=4):
    if len(arr) <= 1:
        return arr

    chunk_size = (len(arr) + num_threads - 1) // num_threads  # Ensure all elements are included
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        sorted_chunks = list(executor.map(merge_sort, chunks))

    # Iteratively merge all sorted chunks
    while len(sorted_chunks) > 1:
        merged_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged_chunks.append(merge(sorted_chunks[i], sorted_chunks[i + 1]))
            else:
                merged_chunks.append(sorted_chunks[i])
        sorted_chunks = merged_chunks

    return sorted_chunks[0]

def generate_random_list(size):
    return [random.randint(0, 10000) for _ in range(size)]

def compare_sorting_methods(size):
    arr = generate_random_list(size)
    
    start_time = time.time()
    sorted_single = merge_sort(arr)
    single_thread_time = time.time() - start_time
    
    start_time = time.time()
    sorted_multi = threaded_merge_sort(arr)
    multi_thread_time = time.time() - start_time

    print(f"Single-threaded sort time: {single_thread_time:.4f} seconds")
    print(f"Multi-threaded sort time: {multi_thread_time:.4f} seconds")
    assert sorted_single == sorted_multi, "Sorted outputs differ!"

compare_sorting_methods(100000)
