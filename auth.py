import re
import sqlite3

def validate_username(username):
    return len(username) >= 4

def validate_password(password):
    return len(password) >= 6

def authenticate_user(username, password):
    conn = sqlite3.connect('market_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None