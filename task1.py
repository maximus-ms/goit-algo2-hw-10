import random
import time
import matplotlib.pyplot as plt
from collections import defaultdict

def partition(arr, pivot_idx):
    pivot = arr[pivot_idx]
    low, middle, high = [], [], []
    for i in range(len(arr)):
        if arr[i] < pivot: low.append(arr[i])
        elif arr[i] > pivot: high.append(arr[i])
        else: middle.append(arr[i])
    return low, middle, high    


def randomized_quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot_idx = random.randint(0, len(arr) - 1)
    low, middle, high = partition(arr, pivot_idx)
    return randomized_quick_sort(low) + middle + randomized_quick_sort(high)


def deterministic_quick_sort_middle(arr):
    if len(arr) <= 1: return arr
    pivot_idx = len(arr) // 2
    low, middle, high = partition(arr, pivot_idx)
    return deterministic_quick_sort_middle(low) + middle + deterministic_quick_sort_middle(high)


def deterministic_quick_sort_first(arr):
    if len(arr) <= 1: return arr
    pivot_idx = 0
    low, middle, high = partition(arr, pivot_idx)
    return deterministic_quick_sort_first(low) + middle + deterministic_quick_sort_first(high)


def deterministic_quick_sort_last(arr):
    if len(arr) <= 1: return arr
    pivot_idx = len(arr) - 1
    low, middle, high = partition(arr, pivot_idx)
    return deterministic_quick_sort_last(low) + middle + deterministic_quick_sort_last(high)


def measure_sorting_time(func, arr, num_runs=5):
    total_time = 0
    for _ in range(num_runs):
        start_time = time.time()
        _ = func(arr)
        total_time += time.time() - start_time
    return total_time / num_runs


def test_sorting_algorithms():
    sizes = [10_000, 50_000, 100_000, 500_000]
    functions = [randomized_quick_sort, deterministic_quick_sort_middle, deterministic_quick_sort_first, deterministic_quick_sort_last]
    num_runs = 5
    results = defaultdict(list)
    
    for size in sizes:
        print(f"\nTesting array size: {size}")
        arr = [random.randint(-1000, 1000) for _ in range(size)]
        for func in functions:
            result = measure_sorting_time(func, arr, num_runs)  
            print(f"{func.__name__:32}: {result:.4f} seconds")
            results[func.__name__].append(result)
    
    plt.figure(figsize=(10, 6))
    for func in functions:
        plt.plot(sizes, results[func.__name__], 'o-', label=func.__name__)
    
    plt.title('Comparison of QuickSort Implementations')
    plt.xlabel('Array Size')
    plt.ylabel('Average Execution Time (seconds)')
    plt.grid(True)
    plt.legend()
    
    plt.savefig('quicksort_comparison.png')
    plt.close()
    

if __name__ == "__main__":
    test_sorting_algorithms() 