import csv
import time
import tracemalloc
import os
import sys
import math
import bisect
import heapq
import signal   # για linux
import gc       # Garbage Collector linux


# Όριο χρόνου εκτέλεσης ανά αλγόριθμο
TIMEOUT_LIMIT_SECONDS = 180  # Όριο 3 λεπτών 

#Οριο Αναδρομής
sys.setrecursionlimit(20000)

# Κάνε το False όταν δεν θέλεις πια να σώζονται τα αρχεία ελέγχου
SAVE_SORTED_OUTPUT = False  



# Timeout
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()




# ------------ Αλγόριθμοι Ταξινόμησης 

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False 
        
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
                
        if not swapped:
            break
            
    return arr


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i] 
        j = i - 1

        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) > 1:
        
        mid = len(arr) // 2
        
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            
    return arr


def _partition(arr, low, high):
    #για να βρω το pivot
    
    mid = (low + high) // 2
    arr[mid], arr[high] = arr[high], arr[mid]
    
    pivot = arr[high] 
    i = low - 1      

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def _quick_sort_recursive(arr, low, high):
    if low < high:
        pi = _partition(arr, low, high)

        _quick_sort_recursive(arr, low, pi - 1)
        _quick_sort_recursive(arr, pi + 1, high)

def quick_sort(arr):
    _quick_sort_recursive(arr, 0, len(arr) - 1)
    return arr


def heapify(arr, n, i):
    largest = i        
    left = 2 * i + 1   
    right = 2 * i + 2 

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  
        heapify(arr, i, 0)             
        
    return arr


def shell_sort(arr):
    n = len(arr)
    gap = n // 2 

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            
            arr[j] = temp
        gap //= 2  
        
    return arr


def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3  
    swapped = True

    while gap > 1 or swapped:
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1

        swapped = False
        
        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
                
    return arr

def tim_insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1

def tim_merge(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left, right = arr[l:m + 1], arr[m + 1:r + 1]
    
    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        k += 1; i += 1

    while j < len2:
        arr[k] = right[j]
        k += 1; j += 1


def simplified_tim_sort(arr):
    n = len(arr)
    min_run = 32

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        tim_insertion_sort(arr, start, end)

    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                tim_merge(arr, left, mid, right)
        size *= 2
    return arr

def tim_sort(arr):
    arr.sort()
    return arr


def intro_insertion_sort(arr, begin, end):
    for i in range(begin + 1, end + 1):
        key = arr[i]
        j = i - 1
        while j >= begin and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def intro_partition(arr, low, high):
    mid = low + (high - low) // 2
    median_idx = sorted([(arr[low], low), (arr[mid], mid), (arr[high], high)])[1][1]
    
    arr[median_idx], arr[high] = arr[high], arr[median_idx]

    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def intro_sort_util(arr, begin, end, depth_limit):
    size = end - begin + 1
    if size < 16:
        intro_insertion_sort(arr, begin, end)
        return
    if depth_limit == 0:
        arr[begin:end+1] = heap_sort(arr[begin:end+1])
        return

    pivot = intro_partition(arr, begin, end)
    intro_sort_util(arr, begin, pivot - 1, depth_limit - 1)
    intro_sort_util(arr, pivot + 1, end, depth_limit - 1)

def intro_sort(arr):
    if len(arr) == 0: return arr
    maxdepth = 2 * math.floor(math.log2(len(arr)))
    intro_sort_util(arr, 0, len(arr) - 1, maxdepth)
    return arr


class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def tree_insert(root, key):
    if root is None:
        return TreeNode(key)
    if root.val < key:
        root.right = tree_insert(root.right, key)
    else:
        root.left = tree_insert(root.left, key)
    return root

def tree_store_sorted(root, arr, i):
    if root is not None:
        i = tree_store_sorted(root.left, arr, i)
        arr[i] = root.val
        i += 1
        i = tree_store_sorted(root.right, arr, i)
    return i

def tree_sort(arr):
    if not arr: return arr
    root = TreeNode(arr[0])
    for i in range(1, len(arr)):
        tree_insert(root, arr[i])
    tree_store_sorted(root, arr, 0)
    return arr


def smooth_sort(arr):
    if len(arr) < 2:
        return arr

    leo = [1, 1]
    while leo[-1] < len(arr):
        leo.append(leo[-1] + leo[-2] + 1)
        
    forest = []
    
    def sift(root, p):
        while p >= 2:
            right_child = root - 1
            left_child = root - 1 - leo[p - 2]
            
            max_node = root
            if arr[left_child] > arr[max_node]:
                max_node = left_child
            if arr[right_child] > arr[max_node]:
                max_node = right_child
                
            if max_node == root:
                break
                
            arr[root], arr[max_node] = arr[max_node], arr[root]
            root = max_node
            if max_node == left_child:
                p -= 1
            else:
                p -= 2

    def trinkle(root, curr_p_idx):
        curr_root = root
        
        while curr_p_idx > 0:
            curr_p = forest[curr_p_idx]
            prev_root = curr_root - leo[curr_p]
            
            if arr[prev_root] > arr[curr_root]:
                if curr_p >= 2:
                    left = curr_root - 1 - leo[curr_p - 2]
                    right = curr_root - 1
                    if arr[prev_root] < arr[left] or arr[prev_root] < arr[right]:
                        break 
                
                arr[curr_root], arr[prev_root] = arr[prev_root], arr[curr_root]
                curr_root = prev_root
                curr_p_idx -= 1
            else:
                break
        
        sift(curr_root, forest[curr_p_idx])

    for i in range(len(arr)):
        if len(forest) >= 2 and forest[-2] == forest[-1] + 1:
            forest.pop()
            forest[-1] += 1
        else:
            if len(forest) >= 1 and forest[-1] == 1:
                forest.append(0)
            else:
                forest.append(1)
        
        trinkle(i, len(forest) - 1)

    for i in range(len(arr) - 1, 0, -1):
        p = forest.pop()
        if p >= 2:
            forest.append(p - 1)
            trinkle(i - 1 - leo[p - 2], len(forest) - 1)
            
            forest.append(p - 2)
            trinkle(i - 1, len(forest) - 1)
            
    return arr



def strand_sort(arr):
    if len(arr) <= 1:
        return arr
    
    items = arr[:]
    arr.clear()
    
    def merge_strands(left, right):
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1
        res.extend(left[i:])
        res.extend(right[j:])
        return res

    while items:
        sublist = [items.pop(0)]
        i = 0
        while i < len(items):
            if items[i] >= sublist[-1]:
                sublist.append(items.pop(i))
            else:
                i += 1
        if not arr:
            arr.extend(sublist)
        else:
            merged = merge_strands(arr, sublist)
            arr.clear()
            arr.extend(merged)
            
    return arr


def patience_sort(arr):
    piles = []
    tops = []  
    for x in arr:
        idx = py_bisect_left(tops, x)
        if idx == len(piles):
            piles.append([x])
            tops.append(x)  
        else:
            piles[idx].append(x)
            tops[idx] = x   

    for p in piles:
        p.reverse()
        
    heap = []
    for i, p in enumerate(piles):
        if p:
            py_heappush(heap, (p[0], i, 0))
            
    sorted_arr = []
    while heap:
        val, pile_idx, item_idx = py_heappop(heap)
        sorted_arr.append(val)
        
        if item_idx + 1 < len(piles[pile_idx]):
            next_val = piles[pile_idx][item_idx + 1]
            py_heappush(heap, (next_val, pile_idx, item_idx + 1))
            
    arr[:] = sorted_arr
    return arr


def patience_sort_Alt(arr):
    piles = []
    tops = [] 
    for x in arr:
        idx = bisect.bisect_left(tops, x)
        if idx == len(piles):
            piles.append([x])
            tops.append(x) 
        else:
            piles[idx].append(x)
            tops[idx] = x  

    for p in piles:
        p.reverse()
    arr[:] = list(heapq.merge(*piles))
    return arr


def merge_insertion_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pairs = []
    for i in range(0, len(arr) - 1, 2):
        if arr[i] > arr[i+1]:
            pairs.append((arr[i], arr[i+1])) 
        else:
            pairs.append((arr[i+1], arr[i]))
            
    unpaired = arr[-1] if len(arr) % 2 != 0 else None
    winners = [p[0] for p in pairs]
    losers = [p[1] for p in pairs]
    
    sorted_winners = merge_insertion_sort(winners)
    result = sorted_winners[:]
    
    if losers:
        result.insert(0, losers[0]) 
        
    for loser in losers[1:]:
        pos = py_bisect_right(result, loser)
        result.insert(pos, loser)
        
    if unpaired is not None:
        pos = py_bisect_right(result, unpaired)
        result.insert(pos, unpaired)
        
    arr[:] = result
    return arr


def merge_insertion_sort_Alt(arr):
    if len(arr) <= 1:
        return arr
    
    pairs = []
    for i in range(0, len(arr) - 1, 2):
        if arr[i] > arr[i+1]:
            pairs.append((arr[i], arr[i+1])) 
        else:
            pairs.append((arr[i+1], arr[i]))
            
    unpaired = arr[-1] if len(arr) % 2 != 0 else None
    
    winners = [p[0] for p in pairs]
    losers = [p[1] for p in pairs]
    
    sorted_winners = merge_insertion_sort(winners)
    result = sorted_winners[:]
    
    if losers:
        result.insert(0, losers[0]) 
        
    for loser in losers[1:]:
        pos = bisect.bisect_right(result, loser)
        result.insert(pos, loser)
        
    if unpaired is not None:
        pos = bisect.bisect_right(result, unpaired)
        result.insert(pos, unpaired)
        
    arr[:] = result
    return arr


def gnome_sort(arr):
    n = len(arr)
    index = 0
    while index < n:
        if index == 0:
            index = index + 1
        if arr[index] >= arr[index - 1]:
            index = index + 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index = index - 1
    return arr

def _stooge_sort_recursive(arr, l, h):
    if l >= h:
        return
    if arr[l] > arr[h]:
        arr[l], arr[h] = arr[h], arr[l]
    if h - l + 1 > 2:
        t = (h - l + 1) // 3
        _stooge_sort_recursive(arr, l, h - t)
        _stooge_sort_recursive(arr, l + t, h)
        _stooge_sort_recursive(arr, l, h - t)

def stooge_sort(arr):
    _stooge_sort_recursive(arr, 0, len(arr) - 1)
    return arr



def py_heappush(heap, item):
    heap.append(item)
    pos = len(heap) - 1
    while pos > 0:
        parent = (pos - 1) // 2
        if heap[pos] < heap[parent]:
            heap[pos], heap[parent] = heap[parent], heap[pos]
            pos = parent
        else:
            break

def py_heappop(heap):
    if len(heap) == 1:
        return heap.pop()
    
    smallest = heap[0]
    heap[0] = heap.pop() 
    pos = 0
    n = len(heap)
    
    while True:
        left = 2 * pos + 1
        right = left + 1
        min_idx = pos
        
        if left < n and heap[left] < heap[min_idx]:
            min_idx = left
        if right < n and heap[right] < heap[min_idx]:
            min_idx = right
            
        if min_idx != pos:
            heap[pos], heap[min_idx] = heap[min_idx], heap[pos]
            pos = min_idx
        else:
            break
            
    return smallest


def py_bisect_left(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def py_bisect_right(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo


def tournament_sort(arr):
    if not arr: return arr
    heap = []
    for item in arr:
        py_heappush(heap, item)
        
    sorted_arr = []
    while heap:
        sorted_arr.append(py_heappop(heap))
        
    arr[:] = sorted_arr
    return arr

def tournament_sort_Alt(arr):
    heapq.heapify(arr)
    sorted_arr = []
    while arr:
        sorted_arr.append(heapq.heappop(arr))
    arr[:] = sorted_arr
    return arr


def _comp_and_swap(arr, i, j, d):
    if (d == 1 and arr[i] > arr[j]) or (d == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def _bitonic_merge(arr, low, cnt, d):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            _comp_and_swap(arr, i, i + k, d)
        _bitonic_merge(arr, low, k, d)
        _bitonic_merge(arr, low + k, k, d)

def _bitonic_sort_rec(arr, low, cnt, d):
    if cnt > 1:
        k = cnt // 2
        _bitonic_sort_rec(arr, low, k, 1)
        _bitonic_sort_rec(arr, low + k, k, 0)
        _bitonic_merge(arr, low, cnt, d)

def bitonic_sort(arr):
    n = len(arr)
    if n <= 1: 
        return arr
    
    next_pow_2 = 1 << (n - 1).bit_length()
    padding_size = next_pow_2 - n
    
    arr.extend([float('inf')] * padding_size)
    
    _bitonic_sort_rec(arr, 0, len(arr), 1)
    
    del arr[n:]
    return arr


def cocktail_shaker_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                
        if not swapped:
            break
            
        swapped = False
        end = end - 1 
        
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                
        start = start + 1 
        
    return arr


def cycle_sort(arr):
    n = len(arr)
    for cycle_start in range(0, n - 1):
        item = arr[cycle_start]
        pos = cycle_start
        
        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1
                
        if pos == cycle_start:
            continue
            
        while item == arr[pos]:
            pos += 1
            
        arr[pos], item = item, arr[pos]
        
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
            
    return arr


def pancake_flip(arr, k):
    left = 0
    while left < k:
        arr[left], arr[k] = arr[k], arr[left]
        left += 1
        k -= 1

def pancake_sort(arr):
    n = len(arr)
    curr_size = n
    while curr_size > 1:
        max_idx = arr.index(max(arr[0:curr_size]))
        
        if max_idx != curr_size - 1:
            # το φέρνουμε στην αρχή 
            pancake_flip(arr, max_idx)
            # το πάμε στο τέλος
            pancake_flip(arr, curr_size - 1)
            
        curr_size -= 1
    return arr


class CartesianNode:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

def cartesian_tree_sort(arr):
    if not arr: return arr
    
    stack = []
    for num in arr:
        last_popped = None
        while stack and stack[-1].val > num:
            last_popped = stack.pop()
        new_node = CartesianNode(num)
        new_node.left = last_popped
        if stack:
            stack[-1].right = new_node
        stack.append(new_node)
        
    root = stack[0]
    
    pq = []
    py_heappush(pq, (root.val, id(root), root))
    sorted_arr = []
    
    while pq:
        val, _, node = py_heappop(pq)
        sorted_arr.append(val)
        if node.left:
            py_heappush(pq, (node.left.val, id(node.left), node.left))
        if node.right:
            py_heappush(pq, (node.right.val, id(node.right), node.right))
            
    arr[:] = sorted_arr
    return arr

def cartesian_tree_sort_Alt(arr):
    if not arr: return arr
    
    #Min-Cartesian Tree
    stack = []
    for num in arr:
        last_popped = None
        while stack and stack[-1].val > num:
            last_popped = stack.pop()
            
        new_node = CartesianNode(num)
        new_node.left = last_popped
        
        if stack:
            stack[-1].right = new_node
        stack.append(new_node)
        
    root = stack[0]
    
    # εξαγωγή με Min-Heap 
    pq = [(root.val, id(root), root)]
    sorted_arr = []
    
    while pq:
        val, _, node = heapq.heappop(pq)
        sorted_arr.append(val)
        if node.left:
            heapq.heappush(pq, (node.left.val, id(node.left), node.left))
        if node.right:
            heapq.heappush(pq, (node.right.val, id(node.right), node.right))
            
    arr[:] = sorted_arr
    return arr


def block_sort(arr):
    n = len(arr)
    if n <= 1: 
        return arr
    
    block_size = int(math.sqrt(n))
    if block_size == 0: block_size = 1
    
    for i in range(0, n, block_size):
        end = min(i + block_size, n)
        temp_block = arr[i:end]
        insertion_sort(temp_block)
        arr[i:end] = temp_block
    
    step = block_size
    while step < n:
        for i in range(0, n, 2 * step):
            mid = min(i + step, n)
            end = min(i + 2 * step, n)
            if mid < end:
                left = arr[i:mid]
                right = arr[mid:end]
                k = i
                l_idx = r_idx = 0
                
                while l_idx < len(left) and r_idx < len(right):
                    if left[l_idx] <= right[r_idx]:
                        arr[k] = left[l_idx]
                        l_idx += 1
                    else:
                        arr[k] = right[r_idx]
                        r_idx += 1
                    k += 1
                while l_idx < len(left):
                    arr[k] = left[l_idx]
                    l_idx += 1
                    k += 1
                while r_idx < len(right):
                    arr[k] = right[r_idx]
                    r_idx += 1
                    k += 1
        step *= 2
    return arr


def block_sort_Alt(arr):
    n = len(arr)
    if n <= 1: 
        return arr
    
    block_size = int(math.sqrt(n))
    if block_size == 0: block_size = 1
    
    for i in range(0, n, block_size):
        end = min(i + block_size, n)
        arr[i:end] = sorted(arr[i:end])
    
    step = block_size
    while step < n:
        for i in range(0, n, 2 * step):
            mid = min(i + step, n)
            end = min(i + 2 * step, n)
            if mid < end:
                left = arr[i:mid]
                right = arr[mid:end]
                k = i
                l_idx = r_idx = 0
                
                while l_idx < len(left) and r_idx < len(right):
                    if left[l_idx] <= right[r_idx]:
                        arr[k] = left[l_idx]
                        l_idx += 1
                    else:
                        arr[k] = right[r_idx]
                        r_idx += 1
                    k += 1
                while l_idx < len(left):
                    arr[k] = left[l_idx]
                    l_idx += 1
                    k += 1
                while r_idx < len(right):
                    arr[k] = right[r_idx]
                    r_idx += 1
                    k += 1
        step *= 2
    return arr


def pairwise_sorting_network(arr):
    n = len(arr)
    if n <= 1: 
        return arr
    
    def oddeven_merge(lo, n_items, r):
        m = r * 2
        if m < n_items:
            oddeven_merge(lo, n_items, m)
            oddeven_merge(lo + r, n_items, m)
            for i in range(lo + r, lo + n_items - r, m):
                if arr[i] > arr[i + r]:
                    arr[i], arr[i + r] = arr[i + r], arr[i]
        else:
            if arr[lo] > arr[lo + r]:
                arr[lo], arr[lo + r] = arr[lo + r], arr[lo]

    def oddeven_merge_sort(lo, n_items):
        if n_items > 1:
            m = n_items // 2
            oddeven_merge_sort(lo, m)
            oddeven_merge_sort(lo + m, m)
            oddeven_merge(lo, n_items, 1)

    next_pow_2 = 1 << (n - 1).bit_length()
    arr.extend([float('inf')] * (next_pow_2 - n))
    
    oddeven_merge_sort(0, next_pow_2)
    
    del arr[n:]
    return arr


def counting_sort(arr):
    if not arr: return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1
    
    count_arr = [0] * range_of_elements
    output_arr = [0] * len(arr)

    for i in range(len(arr)):
        count_arr[arr[i] - min_val] += 1

    for i in range(1, len(count_arr)):
        count_arr[i] += count_arr[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        output_arr[count_arr[arr[i] - min_val] - 1] = arr[i]
        count_arr[arr[i] - min_val] -= 1

    arr[:] = output_arr
    return arr


def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10 
    
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if not arr: return arr
    
    negatives = [-x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]
    
    def sort_positives(arr_pos):
        if not arr_pos: return arr_pos
        max1 = max(arr_pos)
        exp = 1
        while max1 // exp > 0:
            counting_sort_for_radix(arr_pos, exp)
            exp *= 10
        return arr_pos

    negatives = sort_positives(negatives)
    positives = sort_positives(positives)
    
    arr[:] = [-x for x in reversed(negatives)] + positives
    return arr


def bucket_sort(arr):
    if not arr: return arr
    
    min_val, max_val = min(arr), max(arr)
    if min_val == max_val: return arr
        
    bucket_count = int(math.sqrt(len(arr)))
    buckets = [[] for _ in range(bucket_count)]
    
    for num in arr:
        index = int((num - min_val) / (max_val - min_val) * (bucket_count - 1))
        buckets[index].append(num)
        
    arr.clear()
    for bucket in buckets:
        insertion_sort(bucket) 
        arr.extend(bucket)
        
    return arr


def bucket_sort_Alt(arr):
    if not arr: return arr
    
    min_val, max_val = min(arr), max(arr)
    
    if min_val == max_val:
        return arr
        
    bucket_count = int(math.sqrt(len(arr)))
    buckets = [[] for _ in range(bucket_count)]
    
    for num in arr:
        index = int((num - min_val) / (max_val - min_val) * (bucket_count - 1))
        buckets[index].append(num)
        
    arr.clear()
    for bucket in buckets:
        arr.extend(sorted(bucket))
        
    return arr


def pigeonhole_sort(arr):
    if not arr: return arr
    
    min_val = min(arr)
    max_val = max(arr)
    
    size = max_val - min_val + 1
    
    holes = [0] * size
    
    for x in arr:
        holes[x - min_val] += 1
        
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + min_val
            i += 1
            
    return arr


def flash_sort(arr):
    n = len(arr)
    if n <= 1: return arr
    
    min_val = arr[0]
    max_idx = 0
    for i in range(1, n):
        if arr[i] < min_val:
            min_val = arr[i]
        if arr[i] > arr[max_idx]:
            max_idx = i
            
    if min_val == arr[max_idx]:
        return arr
        
    m = int(0.45 * n) 
    if m <= 0: m = 1
    l = [0] * m
    
    c1 = (m - 1) / (arr[max_idx] - min_val)
    for i in range(n):
        k = int(c1 * (arr[i] - min_val))
        l[k] += 1
        
    for i in range(1, m):
        l[i] += l[i - 1]
        
    arr[max_idx], arr[0] = arr[0], arr[max_idx]
    
    nmove = 0
    j = 0
    k = m - 1
    flash = arr[0]
    
    while nmove < n - 1:
        while j > l[k] - 1:
            j += 1
            k = int(c1 * (arr[j] - min_val))
            flash = arr[j]
            
        while j != l[k]:
            k = int(c1 * (flash - min_val))
            l[k] -= 1
            hold = arr[l[k]]
            arr[l[k]] = flash
            flash = hold
            nmove += 1
            
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        
    return arr

















# ------------  Βοηθητικές Συναρτήσεις 

def save_sorted_data(algo_name, sorted_arr):
    #Αποθηκεύει τον ταξινομημένο πίνακα σε αρχείο .txt για έλεγχο
    filename = f"sorted_{algo_name.replace(' ', '_')}.txt"
    try:
        with open(filename, "w", encoding='utf-8') as f:
            f.write("\n".join(map(str, sorted_arr)))
        print(f"  [+] Το αποτέλεσμα αποθηκεύτηκε για έλεγχο στο: {filename}")
    except Exception as e:
        print(f"  [-] Σφάλμα κατά την αποθήκευση του αποτελέσματος: {e}")



def read_csv_file(filename):
    # Διαβάζει το csv και επιστρέφει λίστα ακεραίων
    data = []
    
    filename = filename.strip().strip('"')
    
    print(f"Διαβάζω το αρχείο: {filename}")

    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for item in row:
                    try:
                        data.append(int(item))
                    except ValueError:
                        continue 
        return data
    except FileNotFoundError:
        print(f"\nΣφάλμα: Το αρχείο δεν βρέθηκε στη διαδρομή:\n{filename}")
        return None
    except OSError as e:
        print(f"\nΣφάλμα συστήματος: {e}")
        return None


def save_statistics(algo_name, elapsed_time, peak_memory):
    # Αποθηκεύει τα αποτελέσματα σε αρχείο results.csv
    file_exists = os.path.isfile("results.csv")
    
    with open("results.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        if not file_exists:
            writer.writerow(["Algorithm", "Time (seconds)", "Peak Memory (KB)"])
            
        if isinstance(elapsed_time, str):
            writer.writerow([algo_name, elapsed_time, peak_memory])
        else:
            writer.writerow([algo_name, f"{elapsed_time:.6f}", f"{peak_memory / 1024:.2f}"])
        
    print(f"  [+] Τα στατιστικά αποθηκεύτηκαν στο 'results.csv'.")

def get_cpu_temperature():
    #για θερμοκρασία μάλλον δεν δουλεύει σωστά να δω αν τραβάει σωστά τις τιμές
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read().strip()) / 1000.0
        return temp
    except FileNotFoundError:
        return None # Αν είσαι σε Windows ή Mac, απλά αγνοείται
    except Exception:
        return None    

def run_algorithm(name, sort_function, data):
    print(f"\nΕκτέλεση {name}...")
    
    data_copy = data.copy() 

    # Παύση για να κρυώσει ο επεξεργαστής 
    time.sleep(1)

    # Garbage Collection για να μην επηρεαστεί ο χρόνος μας
    gc.collect()

    # Καταγραφή θερμοκρασίας πριν την εκτέλεση
    temp_start = get_cpu_temperature()
    if temp_start:
        print(f"  [i] Θερμοκρασία έναρξης: {temp_start:.1f}°C")


    # Συνδέουμε το σήμα με τη συνάρτησή 
    signal.signal(signal.SIGALRM, timeout_handler)

    tracemalloc.start()
    start_time = time.perf_counter()
    
    try:
        signal.alarm(TIMEOUT_LIMIT_SECONDS)

        sort_function(data_copy)
        
        # κλείσε το σήμα
        signal.alarm(0)

        end_time = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed_time = end_time - start_time
        print(f"Ολοκληρώθηκε σε {elapsed_time:.4f} sec. Μνήμη: {peak / 1024:.2f} KB")
        
        temp_end = get_cpu_temperature()
        if temp_end:
            print(f"  [i] Θερμοκρασία λήξης: {temp_end:.1f}°C")
            
        save_statistics(name, elapsed_time, peak)

        if SAVE_SORTED_OUTPUT:
            save_sorted_data(name, data_copy)
            
    except TimeoutException:
        # Time limit
        tracemalloc.stop()
        print(f"  [-] ΑΠΕΤΥΧΕ: Ο αλγόριθμος {name} ξεπέρασε το όριο των {TIMEOUT_LIMIT_SECONDS} δευτερολέπτων!")
        save_statistics(name, f"Time Limit", "N/A")

    except RecursionError:
        # πριν κρασάρει το πρόγραμμα σφάλμα αναδρομής
        signal.alarm(0)
        tracemalloc.stop()
        print(f"  [-] ΑΠΕΤΥΧΕ: Ο αλγόριθμος {name} ξεπέρασε το μέγιστο όριο αναδρομής!")
        save_statistics(name, "Recursion Limit", "N/A")









# ------------  Main Menu 


def main():
    print("=== Πρόγραμμα Σύγκρισης Αλγορίθμων Ταξινόμησης ===")
    filename = input("Δώσε το όνομα του αρχείου .csv : ")
    
    data = read_csv_file(filename)
    
    if data:
        print(f"Φορτώθηκαν {len(data)} αριθμοί.")
        
        while True:
            print("\n Επίλεξε αλγόριθμο:")
            print("1. Bubble Sort")
            print("2. Selection Sort")
            print("3. Insertion Sort")
            print("4. Merge Sort")
            print("5. Quick Sort")
            print("6. Heap Sort")
            print("7. Shell Sort")  
            print("8. Comb Sort")
            print("9. Tim Sort (Built-in)")      
            print("10. Intro Sort") 
            print("11. Tree Sort")
            print("12. Smooth Sort")
            print("13. Strand Sort")
            print("14. Patience Sort")        
            print("15. Merge-Insertion Sort") 
            print("16. Gnome Sort")
            print("17. Stooge Sort")
            print("18. Tournament Sort")
            print("19. Bitonic Sort")
            print("20. Cocktail Shaker Sort")     
            print("21. Cycle Sort")
            print("22. Pancake Sort")
            print("23. Cartesian Tree Sort")
            print("24. Block Sort")
            print("25. Pairwise Sorting Network")
            print("26. Counting Sort")
            print("27. Radix Sort")
            print("28. Bucket Sort")
            print("29. Pigeonhole Sort")
            print("30. Flash Sort")
            print(" --- Alt / Built-in Αλγόριθμοι ---")
            print("31. Block Sort (Alternative)")
            print("32. Bucket Sort (Alternative)")
            print("33. Tournament Sort (Alternative)")
            print("34. Cartesian Tree Sort (Alternative)")
            print("35. Patience Sort (Alternative)")
            print("36. Merge-Insertion Sort (Alternative)")
            print("37. Tim Sort (Simplified)")
            print("99. Εκτέλεση Όλων")
            print("00. Έξοδος")
            choice = input("Επιλογή: ")
            

            if choice == '1':
                run_algorithm("Bubble Sort", bubble_sort, data)
            elif choice == '2':
                run_algorithm("Selection Sort", selection_sort, data)
            elif choice == '3':
                run_algorithm("Insertion Sort", insertion_sort, data)
            elif choice == '4':
                run_algorithm("Merge Sort", merge_sort, data)
            elif choice == '5':
                run_algorithm("Quick Sort", quick_sort, data)
            elif choice == '6':
                run_algorithm("Heap Sort", heap_sort, data)
            elif choice == '7':
                run_algorithm("Shell Sort", shell_sort, data)
            elif choice == '8':
                run_algorithm("Comb Sort", comb_sort, data)
            elif choice == '9':
                run_algorithm("Tim Sort", tim_sort, data)
            elif choice == '10':
                run_algorithm("Intro Sort", intro_sort, data)
            elif choice == '11':
                run_algorithm("Tree Sort", tree_sort, data)
            elif choice == '12':
                run_algorithm("Smooth Sort", smooth_sort, data)
            elif choice == '13':
                run_algorithm("Strand Sort", strand_sort, data)
            elif choice == '14':
                run_algorithm("Patience Sort", patience_sort, data)
            elif choice == '15':
                run_algorithm("Merge-Insertion Sort", merge_insertion_sort, data)
            elif choice == '16':
                run_algorithm("Gnome Sort", gnome_sort, data)
            elif choice == '17':
                run_algorithm("Stooge Sort", stooge_sort, data)
            elif choice == '18':
                run_algorithm("Tournament Sort", tournament_sort, data)
            elif choice == '19':
                run_algorithm("Bitonic Sort", bitonic_sort, data)
            elif choice == '20':
                run_algorithm("Cocktail Shaker Sort", cocktail_shaker_sort, data)
            elif choice == '21':
                run_algorithm("Cycle Sort", cycle_sort, data)
            elif choice == '22':
                run_algorithm("Pancake Sort", pancake_sort, data)
            elif choice == '23':
                run_algorithm("Cartesian Tree Sort", cartesian_tree_sort, data)
            elif choice == '24':
                run_algorithm("Block Sort", block_sort, data)
            elif choice == '25':
                run_algorithm("Pairwise Sorting Network", pairwise_sorting_network, data)
            elif choice == '26':
                run_algorithm("Counting Sort", counting_sort, data)
            elif choice == '27':
                run_algorithm("Radix Sort", radix_sort, data)
            elif choice == '28':
                run_algorithm("Bucket Sort", bucket_sort, data)
            elif choice == '29':
                run_algorithm("Pigeonhole Sort", pigeonhole_sort, data)
            elif choice == '30':
                run_algorithm("Flash Sort", flash_sort, data)
            elif choice == '31':
                run_algorithm("Block Sort (Alternative)", block_sort_Alt, data)
            elif choice == '32':
                run_algorithm("Bucket Sort (Alternative)", bucket_sort_Alt, data)
            elif choice == '33':
                run_algorithm("Tournament Sort (Alternative)", tournament_sort_Alt, data)
            elif choice == '34':
                run_algorithm("Cartesian Tree Sort (Alternative)", cartesian_tree_sort_Alt, data)
            elif choice == '35':
                run_algorithm("Patience Sort (Alternative)", patience_sort_Alt, data)
            elif choice == '36':
                run_algorithm("Merge-Insertion Sort (Alternative)", merge_insertion_sort_Alt, data)
            elif choice == '37':
                run_algorithm("Tim Sort (Simplified)", simplified_tim_sort, data)
            elif choice == '99':
                print("\n" + "============")
                print("Ξεκινάει η εκτέλεση ΟΛΩΝ των αλγορίθμων!")
                print("============")

                run_algorithm("Bubble Sort", bubble_sort, data)
                run_algorithm("Selection Sort", selection_sort, data)
                run_algorithm("Insertion Sort", insertion_sort, data)
                run_algorithm("Merge Sort", merge_sort, data)
                run_algorithm("Quick Sort", quick_sort, data)
                run_algorithm("Heap Sort", heap_sort, data)
                run_algorithm("Shell Sort", shell_sort, data)
                run_algorithm("Comb Sort", comb_sort, data)
                run_algorithm("Tim Sort", tim_sort, data)
                run_algorithm("Intro Sort", intro_sort, data)
                run_algorithm("Tree Sort", tree_sort, data)
                run_algorithm("Smooth Sort", smooth_sort, data)
                run_algorithm("Strand Sort", strand_sort, data)
                run_algorithm("Patience Sort", patience_sort, data)
                run_algorithm("Merge-Insertion Sort", merge_insertion_sort, data)
                run_algorithm("Gnome Sort", gnome_sort, data)
                # run_algorithm("Stooge Sort", stooge_sort, data)
                run_algorithm("Tournament Sort", tournament_sort, data)
                run_algorithm("Bitonic Sort", bitonic_sort, data)
                run_algorithm("Cocktail Shaker Sort", cocktail_shaker_sort, data)
                run_algorithm("Cycle Sort", cycle_sort, data)
                run_algorithm("Pancake Sort", pancake_sort, data)
                run_algorithm("Cartesian Tree Sort", cartesian_tree_sort, data)
                run_algorithm("Block Sort", block_sort, data)
                run_algorithm("Pairwise Sorting Network", pairwise_sorting_network, data)
                run_algorithm("Counting Sort", counting_sort, data)
                run_algorithm("Radix Sort", radix_sort, data)
                run_algorithm("Bucket Sort", bucket_sort, data)
                run_algorithm("Pigeonhole Sort", pigeonhole_sort, data)
                run_algorithm("Flash Sort", flash_sort, data)
                print("\n--- Εκτελείται Alternative ---")
                run_algorithm("Block Sort (Alternative)", block_sort_Alt, data)
                run_algorithm("Bucket Sort (Alternative)", bucket_sort_Alt, data)
                run_algorithm("Tournament Sort (Alternative)", tournament_sort_Alt, data)
                run_algorithm("Cartesian Tree Sort (Alternative)", cartesian_tree_sort_Alt, data)
                run_algorithm("Patience Sort (Alternative)", patience_sort_Alt, data)
                run_algorithm("Merge-Insertion Sort (Alternative)", merge_insertion_sort_Alt, data)
                run_algorithm("Tim Sort (simplified)", simplified_tim_sort, data)
                print("\n" + "============")
                print("Η εκτέλεση όλων των αλγορίθμων ολοκληρώθηκε με επιτυχία!")
                print("============")
            elif choice == '00':
                print(" --- Τέλος ---")
                break
            else:
                print("Μη έγκυρη επιλογή.")



if __name__ == "__main__":
    main()