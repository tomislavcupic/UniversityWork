
# Computer Security Exercises

##### These are the two laboratory exercises I have done in SRS - "Sigurnost računalnih sustava", or in english: "Computer Security". Third laboratory exercise was in imunes virtual machine so I couldn't put it here. They are written in Python.

---

## Lab 1: Secure Password Manager (`password_manager.py`)

This lab implements a **command-line password manager** that allows secure storage and retrieval of service passwords using symmetric encryption and HMAC-based integrity verification.

### Features

- Uses **AES-CBC** for encryption and **HMAC-SHA256** for integrity.
- Keys derived from a master password using **PBKDF2** with salt.
- Automatically stores data in a binary file (`passwords.dat`) with integrity checks.
- Encrypts and pads sensitive data securely.
- Validates data integrity using HMAC before decryption.

### Commands

```bash
python password_manager.py <command> <master_password> [additional_arguments]
```

### Example:
```bash
python password_manager.py init mySecretPass
python password_manager.py put mySecretPass github.com P@ssw0rd123
python password_manager.py get mySecretPass github.com
```

---
## Lab 2: User Management System (`login.py`, `usermgmt.py`)

This lab builds a simple user authentication system that supports user creation, secure password storage, and login flow with forced password changes.

### Features

- Stores user passwords using **PBKDF2** with **SHA512** and random salt.
- Tracks whether users need to change their password upon next login.
- Ensures password complexity (≥8 characters).
- Secure password input via getpass.

### Commands

```bash
python labos.py <action> <username>
```
---
## Requirements

- Pyhton 3.x
- pycryptodome

You can install pycryptodome with:
```bash
pip install pycryptodome
```