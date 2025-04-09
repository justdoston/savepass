import os
import pyfiglet
import sys
from pathlib import Path
from cryptography.fernet import Fernet
w = pyfiglet.figlet_format( " SAVEPASS " )
print(w)
print("Made by Abdullayev Doston. Instagram: @doston_0410 | Github: @justdoston\n")

def check_root():
    if os.geteuid() != 0:
        print("This script needs to be run as root or with sudo!")
        sys.exit(1)
def load_key_from_file():
    key_path = Path("/etc/storepass/.data")
    if key_path.exists():
        with open(key_path, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        print("Encryption key has been generated and saved securely.")
        return key
def save_password(filename, password, cipher, storepass_dir):
    filepath = storepass_dir / filename
    if not filepath.exists():
        encrypted_password = cipher.encrypt(password.encode())
        with open(filepath, "wb") as f:
            f.write(encrypted_password)
        print(f"Password saved securely in {filename}.")
    else:
        print(f"File '{filename}' already exists. Choose another name.")
def list_saved_passwords(storepass_dir):
    print("Saved passwords:")
    password_files = [file.name for file in storepass_dir.iterdir() if file.is_file() and not file.name.startswith('.')]
    if password_files:
        for idx, file in enumerate(password_files, 1):
            print(f"{idx}. {file}")
    else:
        print("No saved passwords found.")
    return password_files
def show_password(filename, cipher, storepass_dir):
    filepath = storepass_dir / filename
    if filepath.exists():
        with open(filepath, "rb") as f:
            encrypted_password = f.read()
        password = cipher.decrypt(encrypted_password).decode()
        print(f"Password for {filename}: {password}")
    else:
        print(f"No saved password found for '{filename}'.")
def main():
    check_root()
    key = load_key_from_file()
    cipher = Fernet(key)
    storepass_dir = Path("/etc/storepass")
    if not storepass_dir.exists():
        storepass_dir.mkdir(parents=True, exist_ok=True)
    while True:
        print("\nChoose an option:")
        print("1) Save password")
        print("2) List saved passwords")
        print("3) Show saved password")
        print("4) Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            filename = input("Enter the name of the password file: ")
            password = input("Enter the password to save (you will see what you type): ")
            save_password(filename, password, cipher, storepass_dir)
        elif choice == '2':
            password_files = list_saved_passwords(storepass_dir)
            if password_files:
                try:
                    selected_index = int(input("\nSelect a password number to view: "))
                    if 1 <= selected_index <= len(password_files):
                        show_password(password_files[selected_index - 1], cipher, storepass_dir)
                    else:
                        print("Invalid selection. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == '3':
            password_files = list_saved_passwords(storepass_dir)
            if password_files:
                try:
                    selected_index = int(input("\nSelect a password number to view: "))
                    if 1 <= selected_index <= len(password_files):
                        show_password(password_files[selected_index - 1], cipher, storepass_dir)
                    else:
                        print("Invalid selection. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")
if __name__ == "__main__":
    main()
