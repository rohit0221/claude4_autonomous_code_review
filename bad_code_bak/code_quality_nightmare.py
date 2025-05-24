"""
CODE QUALITY NIGHTMARE - Violates every best practice
"""
import sys
import os
import random
import time
from datetime import datetime

# GLOBAL VARIABLES EVERYWHERE (terrible practice)
x = 0
data = None
config = {}
users = []
cache = {}
temp_data = []
flag = False

# BAD: No docstrings, terrible naming
class a:  # Single letter class name
    def __init__(self):
        self.b = []  # Single letter attributes
        self.c = 0
        self.d = None
        self.e = {}
        
    def f(self, x, y, z):  # Single letter method and parameters
        # BAD: Function does too many things (SRP violation)
        global data, config, users, cache
        
        # BAD: No comments explaining complex logic
        if x:
            if y:
                if z:
                    for i in range(100):
                        for j in range(100):
                            for k in range(100):
                                self.b.append(i * j * k)
                                
        # BAD: Magic numbers everywhere
        self.c = x * 42 + y * 17 - z * 99
        
        # BAD: Modifying global state
        data = self.b
        cache['last_calc'] = self.c
        
        return self.c

# BAD: Inconsistent naming conventions
class UserManager_Bad:  # Mixed snake_case and PascalCase
    def __init__(self):
        self.userList = []  # camelCase in Python
        self.total_users = 0  # snake_case
        self.MaxUsers = 1000  # PascalCase
        self.CURRENT_USER = None  # SCREAMING_SNAKE_CASE
        
    def AddUser(self, userName, userAge, userEmail):  # PascalCase method
        # BAD: No input validation
        # BAD: Inconsistent parameter naming
        NEW_USER = {  # SCREAMING_SNAKE_CASE for local variable
            'name': userName,
            'Age': userAge,  # Inconsistent key naming
            'email_address': userEmail,
            'created_at': datetime.now(),
            'is_active': True,
            'LoginCount': 0  # Mixed case
        }
        
        self.userList.append(NEW_USER)
        self.total_users += 1
        
        # BAD: Side effects in wrong places
        print(f"Added user: {userName}")  # Should be logging
        global users
        users.append(NEW_USER)  # Modifying global
        
    def getUserByEmail(self, email):  # camelCase method
        # BAD: Linear search when dict lookup would be O(1)
        for USER in self.userList:  # SCREAMING_SNAKE_CASE for loop variable
            if USER['email_address'] == email:
                return USER
        return None
    
    def delete_user_by_id(self, user_id):  # snake_case method
        # BAD: Modifying list while iterating
        for i, user in enumerate(self.userList):
            if user.get('id') == user_id:
                del self.userList[i]  # Can skip elements
                break

# BAD: Functions that do too much
def process_everything(file_path, user_data, config_data, output_format):
    """
    This function does EVERYTHING (violates SRP)
    """
    global x, data, config, users, cache, temp_data, flag
    
    # File processing
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
    except:
        file_content = ""
    
    # User processing
    for user in user_data:
        if user['age'] > 18:
            if user['status'] == 'active':
                if user['verified']:
                    users.append(user)
    
    # Config processing
    for key, value in config_data.items():
        if isinstance(value, str):
            if len(value) > 10:
                if value.startswith('http'):
                    config[key] = value.upper()
                else:
                    config[key] = value.lower()
            else:
                config[key] = value * 2
        elif isinstance(value, int):
            config[key] = value + 42
    
    # Output formatting
    if output_format == 'json':
        import json
        result = json.dumps({'users': users, 'config': config})
    elif output_format == 'csv':
        result = ','.join([str(u['name']) for u in users])
    elif output_format == 'xml':
        # BAD: Manual XML construction instead of using library
        result = '<data>'
        for user in users:
            result += f'<user><name>{user["name"]}</name></user>'
        result += '</data>'
    else:
        result = str(users)  # Generic fallback
    
    # Data caching
    cache['last_result'] = result
    cache['timestamp'] = time.time()
    
    # Random side effects
    temp_data.append(len(result))
    flag = True
    x += 1
    
    return result

# BAD: Deep nesting, no early returns
def validate_complex_user(user_obj):
    if user_obj is not None:
        if 'name' in user_obj:
            if len(user_obj['name']) > 0:
                if 'email' in user_obj:
                    if '@' in user_obj['email']:
                        if 'age' in user_obj:
                            if user_obj['age'] >= 0:
                                if user_obj['age'] <= 150:
                                    if 'status' in user_obj:
                                        if user_obj['status'] in ['active', 'inactive']:
                                            return True
                                        else:
                                            return False
                                    else:
                                        return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

# BAD: Meaningless variable names
def do_stuff(a, b, c, d, e):
    x1 = a + b
    y1 = c * d
    z1 = e / 2
    temp = x1 + y1 - z1
    final = temp * 1.5
    result = final + 10
    return result

# BAD: Copy-paste code with slight variations
def calculate_user_score_type1(user):
    score = 0
    if user['login_count'] > 10:
        score += 50
    if user['posts_count'] > 5:
        score += 30
    if user['friends_count'] > 20:
        score += 20
    if user['verified']:
        score += 25
    return score

def calculate_user_score_type2(user):
    score = 0
    if user['login_count'] > 10:
        score += 50
    if user['posts_count'] > 5:
        score += 30
    if user['friends_count'] > 20:
        score += 20
    if user['verified']:
        score += 25
    # Only difference: bonus for premium users
    if user.get('premium', False):
        score += 15
    return score

def calculate_user_score_type3(user):
    score = 0
    if user['login_count'] > 10:
        score += 50
    if user['posts_count'] > 5:
        score += 30
    if user['friends_count'] > 20:
        score += 20
    if user['verified']:
        score += 25
    # Only difference: different premium bonus
    if user.get('premium', False):
        score += 30
    return score

# BAD: Overly complex inheritance
class BaseProcessor:
    def process(self, data):
        pass

class AdvancedProcessor(BaseProcessor):
    def process(self, data):
        return data * 2

class SuperAdvancedProcessor(AdvancedProcessor):
    def process(self, data):
        result = super().process(data)
        return result + 10

class UltraAdvancedProcessor(SuperAdvancedProcessor):
    def process(self, data):
        result = super().process(data)
        return result ** 2

class MegaAdvancedProcessor(UltraAdvancedProcessor):
    def process(self, data):
        result = super().process(data)
        return result / 3

# BAD: Long parameter lists
def create_user_profile(first_name, last_name, email, phone, address, city, 
                       state, zip_code, country, birth_date, gender, 
                       occupation, company, salary, education_level, 
                       marital_status, children_count, interests, hobbies, 
                       emergency_contact_name, emergency_contact_phone,
                       preferences, settings, notifications_enabled, 
                       privacy_level, account_type, subscription_plan):
    # Function with way too many parameters
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        # ... and so on for all 25+ parameters
    }

# BAD: Comments that don't add value
def add_numbers(a, b):
    """
    This function adds numbers
    """
    # Add a to b
    result = a + b  # Addition operation
    # Return the result
    return result  # Return statement

# BAD: Dead code and commented out code
def old_calculation(x, y):
    # This is the old way of doing it
    # result = x * y + 100
    # if result > 1000:
    #     result = result / 2
    # return result
    
    # New way (but keeping old code just in case)
    new_result = x * y * 1.5
    return new_result

def unused_function():
    # This function is never called but still here
    return "This is never used"

# BAD: Hardcoded values everywhere
def process_order(order):
    if order['total'] > 100:  # Magic number
        discount = order['total'] * 0.1  # Magic number
    elif order['total'] > 50:  # Magic number
        discount = order['total'] * 0.05  # Magic number
    else:
        discount = 0
    
    tax = order['total'] * 0.08  # Magic number
    shipping = 15.99  # Magic number
    
    final_total = order['total'] - discount + tax + shipping
    return final_total

# BAD: Print debugging left in code
def debug_heavy_function(data):
    print("Starting function")
    print(f"Data: {data}")
    
    result = []
    for i, item in enumerate(data):
        print(f"Processing item {i}: {item}")
        processed = item * 2
        print(f"Processed value: {processed}")
        result.append(processed)
        print(f"Current result: {result}")
    
    print("Function complete")
    print(f"Final result: {result}")
    return result

# BAD: Mixed concerns
class UserNotificationEmailProcessor:
    """
    Class that handles users, notifications, emails, and processing
    """
    def __init__(self):
        self.users = []
        self.notifications = []
        self.emails = []
        self.processed_data = []
    
    def add_user_and_send_welcome_email_and_create_notification(self, user_data):
        # Method that does too many things
        user = {
            'id': len(self.users) + 1,
            'name': user_data['name'],
            'email': user_data['email']
        }
        self.users.append(user)
        
        # Send email (mixed concern)
        email = f"Welcome {user['name']}!"
        self.emails.append(email)
        print(f"Email sent: {email}")
        
        # Create notification (mixed concern)
        notification = f"New user {user['name']} registered"
        self.notifications.append(notification)
        
        # Process data (mixed concern)
        self.processed_data.append(user['name'].upper())
        
        return user

# Global execution at module level (bad practice)
if __name__ == "__main__":
    # BAD: Code at module level
    print("Starting application...")
    
    manager = UserManager_Bad()
    manager.AddUser("John", 25, "john@example.com")
    
    processor = a()
    result = processor.f(True, True, True)
    
    print(f"Result: {result}")
    print(f"Global x: {x}")
    print(f"Global users: {len(users)}")
