import sqlite3

from dotenv import load_dotenv
import os 

load_dotenv()

def create_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    
    # Create a table with columns for username and password
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_password TEXT NOT NULL,
            user_api_key TEXT,
            user_tier TEXT
        )
    ''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS chat_history_text (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_username TEXT NOT NULL,
            chat_input TEXT NOT NULL,
            chat_response TEXT NOT NULL,
            chat_header TEXT NOT NULL,
            chat_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_username) REFERENCES users (user_name)
        )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_user(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    
    # Insert a new user into the users table
    cursor.execute('''
        INSERT INTO users (user_name, user_password) VALUES (?, ?)
    ''', (username, password))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def delete_user(username):
    # Connect to the SQLite database
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    
    # Delete the user with the specified username
    cursor.execute('''
        DELETE FROM users WHERE user_name = ?
    ''', (username,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_user(username):
    # Connect to the SQLite database
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    
    # Retrieve the user with the specified username
    cursor.execute('''
        SELECT * FROM users WHERE user_name = ?
    ''', (username,))
    
    user = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    return user

def get_user_pass(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    
    # Retrieve the user with the specified username
    cursor.execute('''
        SELECT * FROM users WHERE user_name = ? and user_password = ?
    ''', (username, password))
    
    user = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    return user

create_database()