"""
PERFORMANCE DISASTER - O(n³) algorithms and memory leaks everywhere
"""
import time
import random
import copy
from collections import defaultdict

class PerformanceNightmare:
    def __init__(self):
        self.data = []
        self.cache = {}  # Never cleared - memory leak
        self.history = []  # Grows unbounded
        self.duplicate_storage = {}  # Redundant storage
        
    def add_item(self, item):
        # O(n) insertion when O(1) possible with set
        if item not in self.data:  # O(n) lookup every time
            self.data.append(item)
            self.history.append(f"Added {item} at {time.time()}")  # Memory leak
        
        # Redundant storage
        self.duplicate_storage[len(self.data)] = copy.deepcopy(item)  # Unnecessary deep copy
        
    def find_duplicates_nightmare(self, items):
        # O(n³) algorithm when O(n) with set would work
        duplicates = []
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                for k in range(j + 1, len(items)):
                    if items[i] == items[j] and items[j] == items[k]:
                        # Another O(n) operation inside O(n³) loop
                        if items[i] not in duplicates:
                            duplicates.append(items[i])
        return duplicates
    
    def inefficient_sort(self, data):
        # Bubble sort O(n²) when Python's Timsort O(n log n) available
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data
    
    def nested_loop_nightmare(self, matrix):
        # O(n⁴) when O(n²) possible
        result = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for k in range(len(matrix)):
                    for l in range(len(matrix[k])):
                        if matrix[i][j] == matrix[k][l] and (i != k or j != l):
                            result.append((i, j, k, l))
        return result
    
    def memory_leak_function(self, size):
        # Continuously allocating memory without cleanup
        large_data = []
        for i in range(size):
            # Creating large objects in loop
            large_object = [random.random() for _ in range(1000)]
            large_data.append(large_object)
            
            # Storing everything in cache without cleanup
            self.cache[f"data_{i}"] = copy.deepcopy(large_object)
        
        return large_data
    
    def recursive_fibonacci_disaster(self, n):
        # O(2ⁿ) recursive Fibonacci without memoization
        if n <= 1:
            return n
        return self.recursive_fibonacci_disaster(n-1) + self.recursive_fibonacci_disaster(n-2)
    
    def string_concatenation_hell(self, strings):
        # O(n²) string concatenation instead of join()
        result = ""
        for s in strings:
            result += s  # Creates new string object each time
            # Adding unnecessary operations
            result += ""  # Pointless concatenation
            result = result + ""  # More pointless operations
        return result
    
    def database_n_plus_one_simulation(self, user_ids):
        # Simulating N+1 database query problem
        users = []
        
        # One query to get all user IDs (simulated)
        all_ids = self.simulate_db_query("SELECT id FROM users")
        
        # N queries to get each user's details (TERRIBLE)
        for user_id in user_ids:
            user_details = self.simulate_db_query(f"SELECT * FROM users WHERE id = {user_id}")
            users.append(user_details)
            
            # Even worse - nested queries for each user
            user_posts = self.simulate_db_query(f"SELECT * FROM posts WHERE user_id = {user_id}")
            for post in user_posts:
                post_comments = self.simulate_db_query(f"SELECT * FROM comments WHERE post_id = {post['id']}")
                # This creates O(n×m×k) queries
        
        return users
    
    def simulate_db_query(self, query):
        # Simulating slow database operation
        time.sleep(0.01)  # Simulated network delay
        return {"id": random.randint(1, 1000), "name": "User"}
    
    def inefficient_search(self, data, target):
        # Linear search in sorted data instead of binary search
        found_indices = []
        for i, item in enumerate(data):
            if item == target:
                found_indices.append(i)
                # Continuing search even after finding all occurrences
        return found_indices
    
    def redundant_calculations(self, numbers):
        # Recalculating same values repeatedly
        results = []
        for i in range(len(numbers)):
            for j in range(len(numbers)):
                # Recalculating expensive operation instead of caching
                expensive_result = sum(numbers[:i+1]) * sum(numbers[:j+1])
                results.append(expensive_result)
        return results
    
    def memory_inefficient_copy(self, large_list):
        # Making unnecessary copies of large data structures
        copy1 = copy.deepcopy(large_list)
        copy2 = copy.deepcopy(copy1)
        copy3 = copy.deepcopy(copy2)
        copy4 = copy.deepcopy(copy3)
        
        # Processing each copy separately instead of reusing
        result1 = [x * 2 for x in copy1]
        result2 = [x * 2 for x in copy2]  # Same operation on copy
        result3 = [x * 2 for x in copy3]  # Same operation on copy
        result4 = [x * 2 for x in copy4]  # Same operation on copy
        
        return result1 + result2 + result3 + result4
    
    def nested_dictionary_hell(self, data):
        # O(n³) nested dictionary operations
        result = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        
        for i, item1 in enumerate(data):
            for j, item2 in enumerate(data):
                for k, item3 in enumerate(data):
                    # Complex nested structure that's hard to access efficiently
                    key1 = str(item1)
                    key2 = str(item2) 
                    key3 = str(item3)
                    
                    # Inefficient string operations in hot loop
                    combined_key = key1 + "_" + key2 + "_" + key3
                    result[key1][key2][key3] = len(combined_key)
        
        return result
    
    def process_large_file_inefficiently(self, filename):
        # Loading entire file into memory instead of streaming
        try:
            with open(filename, 'r') as f:
                all_lines = f.readlines()  # Loading everything at once
            
            # Processing in most inefficient way possible
            processed_lines = []
            for line in all_lines:
                # String operations in loop
                processed_line = line.strip().lower().replace(' ', '_')
                processed_line = processed_line + "_processed"
                processed_lines.append(processed_line)
            
            # More inefficient operations
            result = ""
            for line in processed_lines:
                result += line + "\n"  # O(n²) string concatenation
            
            return result
        except:
            return "File not found"

# Global instances causing memory issues
nightmare_instance = PerformanceNightmare()
global_cache = {}  # Never cleared
global_history = []  # Grows unbounded

def create_performance_problems():
    # Function that creates performance issues
    large_data = list(range(10000))
    
    # O(n²) operations
    for i in range(1000):
        for j in range(1000):
            global_cache[f"{i}_{j}"] = i * j
            global_history.append(f"Calculated {i} * {j}")
    
    # Memory leaks
    nightmare_instance.memory_leak_function(1000)
    
    # Inefficient algorithms
    duplicates = nightmare_instance.find_duplicates_nightmare(large_data)
    
    return len(duplicates)

# More terrible performance patterns
def inefficient_data_processing(data_list):
    # Multiple passes over data when single pass would work
    # Pass 1: Count items
    count = 0
    for item in data_list:
        count += 1
    
    # Pass 2: Find max (could be done in pass 1)
    max_item = data_list[0]
    for item in data_list:
        if item > max_item:
            max_item = item
    
    # Pass 3: Find min (could be done in pass 1)
    min_item = data_list[0]
    for item in data_list:
        if item < min_item:
            min_item = item
    
    # Pass 4: Calculate sum (could be done in pass 1)
    total = 0
    for item in data_list:
        total += item
    
    return count, max_item, min_item, total

if __name__ == "__main__":
    # Running performance nightmares
    print("Creating performance problems...")
    create_performance_problems()
    print("Performance nightmare complete!")
