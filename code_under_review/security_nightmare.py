"""
SECURITY NIGHTMARE - Maximum vulnerabilities for testing
"""
import os
import subprocess
import pickle
import sqlite3
import hashlib
from datetime import datetime
import json
import requests

# CRITICAL SECURITY ISSUES
SECRET_KEY = "admin123"  # Hardcoded secret
API_KEY = "sk-1234567890abcdef"  # Hardcoded API key
DATABASE_PASSWORD = "password123"  # Hardcoded DB password
ADMIN_TOKEN = "super_secret_admin_token"  # Another hardcoded secret
JWT_SECRET = "my-jwt-secret-key"  # Hardcoded JWT secret

# Global variables (bad practice)
db_connection = None
user_sessions = {}
admin_users = ["admin", "root", "administrator"]

class UserManager:
    def __init__(self):
        self.users = []
        
    def create_user(self, username, password, email):
        # SQL injection vulnerability
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
        cursor = db_connection.cursor()
        cursor.execute(query)  # No parameterized queries
        db_connection.commit()
        
    def authenticate_user(self, username, password):
        # SQL injection + weak password hashing
        password_hash = hashlib.md5(password.encode()).hexdigest()  # MD5 is broken
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
        cursor = db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    
    def get_user_by_id(self, user_id):
        # SQL injection in parameter
        query = f"SELECT * FROM users WHERE id = {user_id}"
        cursor = db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    
    def update_user_role(self, user_id, role):
        # No authorization checks
        query = f"UPDATE users SET role = '{role}' WHERE id = {user_id}"
        cursor = db_connection.cursor()
        cursor.execute(query)
        db_connection.commit()

def init_database():
    global db_connection
    # Hardcoded database credentials
    db_connection = sqlite3.connect('app.db', check_same_thread=False)
    
def execute_system_command(command):
    # CRITICAL: Command injection vulnerability
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except:
        return "Command failed"

def deserialize_user_data(data):
    # CRITICAL: Unsafe deserialization
    try:
        user_obj = pickle.loads(data)  # Extremely dangerous
        return user_obj
    except:
        return None

def process_file_upload(filename, file_data):
    # CRITICAL: Path traversal vulnerability
    # CRITICAL: No file type validation
    file_path = f"/uploads/{filename}"  # Can be ../../../etc/passwd
    with open(file_path, 'wb') as f:
        f.write(file_data)
    return file_path

def generate_session_token(username):
    # Weak token generation
    timestamp = str(int(datetime.now().timestamp()))
    token = hashlib.md5(f"{username}{timestamp}{SECRET_KEY}".encode()).hexdigest()
    return token

def validate_admin_token(token):
    # Timing attack vulnerability - not constant time
    return token == ADMIN_TOKEN

def execute_dynamic_code(user_code):
    # CRITICAL: Code injection via exec/eval
    try:
        result = eval(user_code)  # Extremely dangerous
        return str(result)
    except Exception as e:
        # Information disclosure in error messages
        return f"Error: {str(e)} | Code: {user_code}"

def fetch_external_api(url, params):
    # SSRF vulnerability - no URL validation
    # Insecure SSL verification
    try:
        response = requests.get(url, params=params, verify=False, timeout=None)
        return response.json()
    except:
        return {"error": "Request failed"}

def log_sensitive_data(username, password, credit_card):
    # CRITICAL: Logging sensitive information
    log_entry = f"[{datetime.now()}] User: {username}, Pass: {password}, CC: {credit_card}"
    with open('app.log', 'a') as f:
        f.write(log_entry + "\n")

def backup_database(backup_path):
    # Path traversal in backup function
    command = f"cp app.db {backup_path}"
    os.system(command)  # Command injection possible

def get_environment_info():
    # Information disclosure
    return {
        'environment_variables': dict(os.environ),
        'secret_key': SECRET_KEY,
        'api_key': API_KEY,
        'database_password': DATABASE_PASSWORD,
        'jwt_secret': JWT_SECRET,
        'admin_token': ADMIN_TOKEN,
        'python_path': os.sys.path,
        'current_directory': os.getcwd()
    }

def weak_crypto_function(data):
    # Using deprecated/weak cryptographic functions
    return hashlib.md5(data.encode()).hexdigest()  # MD5 is broken

def insecure_random_generator():
    # Using predictable random number generation for security purposes
    import random
    return random.randint(1000, 9999)  # Not cryptographically secure

# CRITICAL: Hardcoded configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'username': 'root',
    'password': 'admin123',
    'database': 'production_db'
}

# CRITICAL: Exposed debug functionality
def debug_execute_raw_sql(sql_query):
    cursor = db_connection.cursor()
    cursor.execute(sql_query)  # No sanitization
    return cursor.fetchall()

# CRITICAL: Insecure session management
def create_session(user_id):
    session_id = str(user_id) + "_" + str(insecure_random_generator())
    user_sessions[session_id] = {
        'user_id': user_id,
        'created_at': datetime.now(),
        'is_admin': user_id in [1, 2, 3]  # Hardcoded admin user IDs
    }
    return session_id

# Main execution with security issues
if __name__ == "__main__":
    init_database()
    
    # CRITICAL: Running with debug information exposed
    print(f"Starting application with secret key: {SECRET_KEY}")
    print(f"Database password: {DATABASE_PASSWORD}")
    print(f"Admin token: {ADMIN_TOKEN}")
