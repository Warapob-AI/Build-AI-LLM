import sqlite3 
import os 

def insert_chat_history(chat_username, chat_input, chat_response, chat_header, chat_timestamp):
    # Connect to the SQLite database
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    
    # Insert a new user into the users table
    cursor.execute('''
        INSERT INTO chat_history_text (chat_username, chat_input, chat_response, chat_header, chat_timestamp) VALUES (?, ?, ?, ?, ?)
    ''', (chat_username, chat_input, chat_response, chat_header, chat_timestamp))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_recent_chat_history(username, header):
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM chat_history_text WHERE chat_username=? AND chat_header=?",
        (username, header)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows