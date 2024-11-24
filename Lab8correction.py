import sqlite3
import hashlib
import os
import re

SECRET_KEY = os.urandom(32)

def safe_sql_query(user_input):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (user_input,))
    results = cursor.fetchall()
    conn.close()
    return results

def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, hashed_password

def safe_os_command(user_input):
    if re.match(r"^[a-zA-Z0-9\.\-]+$", user_input):
        os.system(f"ping {user_input}")
    else:
        print("Неприпустимий ввід. Тільки домени або IP-адреси.")

def secure_file_access(filename):
    if not re.match(r"^[a-zA-Z0-9_\-\.]+$", filename):
        raise ValueError("Неприпустима назва файлу!")
    
    filepath = os.path.abspath(filename)
    basepath = os.path.abspath(".")
    
    if not filepath.startswith(basepath):
        raise PermissionError("Доступ до файлу заборонений!")
    
    with open(filepath, "r") as file:
        return file.read()

if __name__ == "__main__":
    print("Безпечний код для демонстрації:")
    username = input("Введіть ім'я користувача: ")
    print(safe_sql_query(username))
    
    password = input("Введіть пароль: ")
    salt, hashed_password = hash_password(password)
    print(f"Сіль: {salt.hex()}, Хеш пароля: {hashed_password.hex()}")
    
    command_input = input("Введіть IP-адресу або домен для ping: ")
    safe_os_command(command_input)
    
    file_name = input("Введіть назву файлу для читання: ")
    try:
        print(secure_file_access(file_name))
    except (ValueError, PermissionError) as e:
        print(f"Помилка: {e}")
