# File Encryption/Decryption Tool

This is a secure Python-based command-line utility for encrypting and decrypting files using a password. It uses Fernet symmetric encryption and PBKDF2 with a high iteration count to derive strong encryption keys from user passwords.

## Features

- Password-based encryption and decryption
- Key derivation using PBKDF2-HMAC-SHA256 with 600,000 iterations
- Random salt generation and storage in the encrypted file
- Detects incorrect passwords and corrupted files
- Works with any file type
- Simple command-line interface with password masking

## Requirements

- Python 3.6 or later
- `cryptography` library

Install dependencies using:

```bash
pip install cryptography
```

## Usage

Run the script:

```bash
python encryptor.py
```

## Menu Options

- Encrypt a file : Encrypts a file and saves the output to a specified path.
- Decrypt a file : Decrypts an encrypted file using the correct password.
- Exit : Exits the application.

## How It Works

- Key Derivation: PBKDF2-HMAC-SHA256 is used with 600,000 iterations and a 16-byte salt to derive a secure 32-byte encryption key.
- Encryption: The file is encrypted using a Fernet key derived from the password.
- Salt Handling: The salt is prepended to the encrypted output file for use during decryption.
- Decryption: The tool extracts the salt, re-derives the key, and attempts to decrypt the content.

## Notes

- There is no way to recover encrypted files without the correct password.
- Use strong and memorable passwords.
- The encrypted file includes the salt needed for decryption. No separate salt management is necessary.

## Security Considerations

- High iteration count resists brute-force attacks.
- A unique 16-byte salt ensures that encrypting the same file twice with the same password yields different results.
- Fernet provides authenticated encryption; it detects tampering during decryption.
