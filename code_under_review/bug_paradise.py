"""
BUG PARADISE - Every possible bug and error handling nightmare
"""
import json
import datetime
from typing import List, Dict, Optional

class BuggyCalculator:
    def __init__(self):
        self.history = []
        self.memory = 0
        
    def divide(self, a, b):
        # BUG: No division by zero check
        result = a / b
        return result
    
    def calculate_average(self, numbers):
        # BUG: No check for empty list
        total = sum(numbers)
        average = total / len(numbers)  # ZeroDivisionError if empty
        return average
    
    def get_percentage(self, part, whole):
        # BUG: No validation of inputs
        return (part / whole) * 100  # Can divide by zero
    
    def factorial(self, n):
        # BUG: No input validation for negative numbers
        # BUG: Will cause infinite recursion for negative inputs
        if n == 0:
            return 1
        return n * self.factorial(n - 1)
    
    def square_root(self, number):
        # BUG: No check for negative numbers
        return number ** 0.5  # Will return complex number for negative input

class DataProcessor:
    def __init__(self):
        self.data = None
        self.processed_count = 0
        
    def process_file(self, filename):
        # BUG: No error handling for file operations
        f = open(filename, 'r')  # File might not exist
        content = f.read()
        f.close()  # Should use context manager
        
        # BUG: Assumes file contains valid JSON
        data = json.loads(content)  # Will crash if not valid JSON
        return data
    
    def process_list(self, items):
        # BUG: Assumes items is always a list
        processed = []
        for item in items:  # Will crash if items is None
            # BUG: Assumes item has specific structure
            processed_item = {
                'id': item['id'],  # KeyError if 'id' doesn't exist
                'name': item['name'].upper(),  # AttributeError if name is None
                'value': item['value'] * 2  # TypeError if value is not numeric
            }
            processed.append(processed_item)
        return processed
    
    def get_item_by_index(self, items, index):
        # BUG: No bounds checking
        return items[index]  # IndexError if index out of range
    
    def update_data(self, new_data):
        # BUG: Modifying mutable default argument indirectly
        self.data.update(new_data)  # AttributeError if self.data is None

class DateTimeProcessor:
    def parse_date(self, date_string):
        # BUG: No error handling for invalid date formats
        return datetime.datetime.strptime(date_string, "%Y-%m-%d")
    
    def calculate_age(self, birth_date_string):
        # BUG: Multiple potential failures
        birth_date = self.parse_date(birth_date_string)  # Can fail
        today = datetime.datetime.now()
        age = today.year - birth_date.year  # Incomplete age calculation
        return age
    
    def format_date(self, date_obj):
        # BUG: Assumes date_obj is always a datetime object
        return date_obj.strftime("%Y-%m-%d")  # AttributeError if wrong type

class StringProcessor:
    def extract_numbers(self, text):
        # BUG: No validation of input type
        numbers = []
        for char in text:  # TypeError if text is not iterable
            if char.isdigit():
                numbers.append(int(char))
        return numbers
    
    def split_and_clean(self, text, delimiter):
        # BUG: No null checks
        parts = text.split(delimiter)  # AttributeError if text is None
        cleaned = []
        for part in parts:
            cleaned.append(part.strip().lower())  # AttributeError if part is None
        return cleaned
    
    def get_first_word(self, sentence):
        # BUG: Assumes sentence has words
        words = sentence.split()  # AttributeError if sentence is None
        return words[0]  # IndexError if empty list

class NetworkProcessor:
    def __init__(self):
        self.cache = {}
        
    def fetch_data(self, url):
        # BUG: No error handling for network requests
        import requests
        response = requests.get(url)  # Can fail with network errors
        return response.json()  # Can fail if response is not JSON
    
    def process_api_response(self, response):
        # BUG: Assumes specific response structure
        results = []
        for item in response['data']:  # KeyError if 'data' doesn't exist
            processed = {
                'id': item['id'],
                'title': item['title'],
                'status': item['metadata']['status']  # Nested KeyError possible
            }
            results.append(processed)
        return results

class MutableDefaultBug:
    # BUG: Mutable default arguments
    def __init__(self, items=[]):  # DANGEROUS: shared mutable default
        self.items = items
        
    def add_item(self, item, categories=[]):  # DANGEROUS: shared mutable default
        categories.append('default')
        self.items.append({'item': item, 'categories': categories})
    
    def process_data(self, data, results={}):  # DANGEROUS: shared mutable default
        results['processed'] = True
        results['count'] = len(data)
        return results

class MemoryLeakGenerator:
    def __init__(self):
        self.circular_ref = self  # Circular reference
        self.data_store = []
        
    def create_memory_leak(self):
        # Creating circular references without cleanup
        for i in range(1000):
            obj = {'id': i, 'parent': self}
            obj['self_ref'] = obj  # Circular reference
            self.data_store.append(obj)

class ConcurrencyBugs:
    def __init__(self):
        self.counter = 0
        self.shared_data = {}
        
    def increment_counter(self):
        # BUG: Race condition in multithreading
        current = self.counter
        # Simulating some processing time
        import time
        time.sleep(0.001)
        self.counter = current + 1
    
    def update_shared_data(self, key, value):
        # BUG: Race condition when modifying shared dictionary
        if key in self.shared_data:
            self.shared_data[key] += value
        else:
            self.shared_data[key] = value

# Functions with various bugs
def buggy_search(data, target):
    # BUG: Doesn't handle None inputs
    for i in range(len(data)):  # TypeError if data is None
        if data[i] == target:
            return i
    return -1

def unsafe_cast(value, target_type):
    # BUG: No error handling for type conversion
    if target_type == 'int':
        return int(value)  # ValueError for invalid strings
    elif target_type == 'float':
        return float(value)  # ValueError for invalid strings
    else:
        return str(value)

def process_nested_data(data):
    # BUG: Assumes complex nested structure exists
    result = []
    for category in data['categories']:  # KeyError if 'categories' missing
        for item in category['items']:  # KeyError if 'items' missing
            result.append(item['name'])  # KeyError if 'name' missing
    return result

def calculate_compound_interest(principal, rate, time):
    # BUG: No input validation
    # BUG: Doesn't handle negative values appropriately
    amount = principal * (1 + rate) ** time
    return amount

def merge_dictionaries(dict1, dict2):
    # BUG: Modifies input dictionary (side effect)
    dict1.update(dict2)  # Changes dict1 unexpectedly
    return dict1

def process_user_input(user_input):
    # BUG: No validation of user input
    commands = user_input.split(';')  # AttributeError if None
    results = []
    for command in commands:
        # BUG: eval is dangerous but also assumes valid Python
        result = eval(command)  # Can crash with SyntaxError
        results.append(result)
    return results

# Global variables that can cause issues
GLOBAL_COUNTER = 0
GLOBAL_CACHE = {}  # Never cleared, potential memory leak

def update_global_state(value):
    # BUG: Modifying global state without proper synchronization
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += value
    GLOBAL_CACHE[GLOBAL_COUNTER] = value  # Growing unbounded

# Edge case bugs
def get_last_n_items(items, n):
    # BUG: Doesn't handle edge cases properly
    return items[-n:]  # Returns wrong result when n > len(items)

def calculate_discount(price, discount_percent):
    # BUG: No bounds checking on discount
    discount = price * (discount_percent / 100)
    final_price = price - discount
    return final_price  # Can return negative prices

if __name__ == "__main__":
    # Running buggy code
    calc = BuggyCalculator()
    
    # These will all crash or behave unexpectedly
    try:
        print(calc.divide(10, 0))  # Division by zero
    except:
        pass
    
    try:
        print(calc.calculate_average([]))  # Empty list
    except:
        pass
    
    try:
        print(calc.factorial(-5))  # Infinite recursion
    except:
        pass
    
    processor = DataProcessor()
    try:
        processor.process_file("nonexistent.json")  # File not found
    except:
        pass
