import os
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey


def derive_key(password: str, salt: bytes = None ) -> tuple[bytes, bytes]:
    """Derive a Fernet key from a password using PBKDF2HMAC."""
    if salt is None:
      salt = os.urandom(16)  # Generate a random 16-byte salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Fernet expects a 32-byte key
        salt=salt,
        iterations=600000,  # High iteration count for security
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))  # Encode to Fernet-compatible key
    return key, salt

def encrypt_file(input_file: str, output_file: str, password: str) -> None:
    """Encrypt a file using the provided password."""
    try:
        # Check if input file exists
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

        # Derive key from password
        key, salt = derive_key(password)
        fernet = Fernet(key)

        # Read input file
        with open(input_file, 'rb') as f:
            data = f.read()

        # Encrypt data
        encrypted_data = fernet.encrypt(data)

        # Write salt and encrypted data to output file
        with open(output_file, 'wb') as f:
            f.write(salt + encrypted_data)  # Prepend salt for decryption

        print(f"File encrypted successfully: {output_file}")

    except Exception as e:
        print(f"Encryption failed: {str(e)}")

def decrypt_file(input_file: str, output_file: str, password: str) -> None:
    """Decrypt a file using the provided password."""
    try:
        # Check if input file exists
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

        # Read salt and encrypted data
        with open(input_file, 'rb') as f:
            data = f.read()
            if len(data) < 16:
                raise ValueError("Invalid encrypted file: too short.")
            salt, encrypted_data = data[:16], data[16:]

        # Derive key from password and salt
        key, _ = derive_key(password, salt)
        fernet = Fernet(key)

        # Decrypt data
        decrypted_data = fernet.decrypt(encrypted_data)

        # Write decrypted data to output file
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

        print(f"File decrypted successfully: {output_file}")

    except InvalidKey:
        print("Decryption failed: Incorrect password or corrupted file.")
    except Exception as e:
        print(f"Decryption failed: {str(e)}")

def main():
    """Main function to handle user input and script execution."""
    while True:
        print("\nFile Encryption/Decryption Tool")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path (encrypted): ").strip()
            password = getpass.getpass("Enter password: ")
            confirm_password = getpass.getpass("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match.")
                continue
            encrypt_file(input_file, output_file, password)

        elif choice == '2':
            input_file = input("Enter input file path (encrypted): ").strip()
            output_file = input("Enter output file path (decrypted): ").strip()
            password = getpass.getpass("Enter password: ")
            decrypt_file(input_file, output_file, password)

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()