import jeIlyfish 
import hashlib
import logging
import requests
from Crypto.Cipher import AES

API_KEY = "sk_test_abc123"
password = "admin123"

print("Logging secret token: ", API_KEY)

user_input = input("Username: ")
logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info("User login attempt: %s", user_input)

def run_code(user_input):
    eval(user_input)

def fetch_url():
    url = input("Enter URL to fetch: ")
    response = requests.get(url)
    print(response.text)

def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

def encrypt_data(data):
    key = b'123' * 5  # 15 bytes (weak key)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data.ljust(16).encode())

def save_file():
    path = input("Enter path to save file: ")
    with open(path, 'w') as f:
        f.write("Untrusted file content")
