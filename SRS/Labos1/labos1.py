import sys
import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password.encode() # Convert to bytes
        self.key = self._derive_key(self.master_password) # Derive key from master password
        self.hmac_key = self._derive_hmac_key(self.master_password) # Derive HMAC key from master password
        self.passwords = {} # Dictionary to store passwords

    def _derive_key(self, master_password):
        salt = get_random_bytes(16) # Generate salt
        kdf = PBKDF2(master_password, salt, dkLen=32, count=1000000) # Derive key using PBKDF2
        return kdf 

    def _derive_hmac_key(self, master_password):
        salt = os.urandom(16) # Generate salt
        kdf = PBKDF2(master_password, salt, dkLen=32, count=1000000) # Derive key using PBKDF2
        return kdf

    def _calculate_hmac(self, data):
        h = HMAC.new(self.hmac_key, digestmod=SHA256) # Create HMAC object
        h.update(data) # Update HMAC object with data
        return h.digest() # Return HMAC digest

    def _pad(self, data):
        padding_length = AES.block_size - len(data) % AES.block_size # Calculate padding length
        padding = bytes([padding_length]) * padding_length # Create padding
        return data + padding

    def _unpad(self, data):
        padding_length = data[-1] # Get padding length from last byte
        return data[:-padding_length] # Remove padding

    def _encrypt(self, data):
      iv = get_random_bytes(AES.block_size)  # Generate IV
      cipher = AES.new(self.key, AES.MODE_CBC, iv) # Create AES cipher
      ct_bytes = cipher.encrypt(self._pad(data)) # Encrypt data
      return iv + ct_bytes


    def _decrypt(self, encrypted_data, iv):
      cipher = AES.new(self.key, AES.MODE_CBC, iv) # Create AES cipher
      decrypted_data = cipher.decrypt(encrypted_data) # Decrypt data
      return self._unpad(decrypted_data).decode() # Remove padding and return decrypted data

    def _write_to_disk(self):
      data_to_write = str(self.passwords).encode() # Convert passwords to bytes
      encrypted_data = self._encrypt(data_to_write)  # Encrypt data
      hmac = self._calculate_hmac(encrypted_data) # Calculate HMAC
      with open("passwords.dat", "wb") as f: # Write data to disk
         f.write(encrypted_data) 
         f.write(hmac)

    def _read_from_disk(self):
      if not os.path.exists("passwords.dat"):
          self.initialize_database()
          print("No password database found. Initializing new database.")
          return
      with open("passwords.dat", "rb") as f:
         data_read = f.read()
      if not data_read:
         self.initialize_database() # Initialize new database if file is empty
         print("No password database found. Initializing new database.") 
         return
      
      stored_hmac = data_read[-32:]  # HMAC is 32 bytes long
      encrypted_data = data_read[:-32]  # Remove HMAC from data
      calculated_hmac = self._calculate_hmac(encrypted_data) # Calculate HMAC
      if calculated_hmac != stored_hmac: # Check if HMACs match
         raise ValueError("Integrity check failed. Data may have been tampered with.")
      iv = encrypted_data[:AES.block_size]  # Extract IV from encrypted data
      encrypted_data = encrypted_data[AES.block_size:]  # Remove IV from encrypted data
      decrypted_data = self._decrypt(encrypted_data, iv) # Decrypt data
      self.passwords = eval(decrypted_data) # Convert decrypted data to dictionary


    def initialize_database(self):
        self.passwords = {} # Initialize empty dictionary
        self._write_to_disk() # Write empty dictionary to disk

    def store_password(self, address, password):
        self._read_from_disk()   # Read passwords from disk
        self.passwords[address] = password # Store password
        self._write_to_disk() # Write passwords to disk

    def retrieve_password(self, address):
        self._read_from_disk() # Read passwords from disk
        return self.passwords.get(address, None) # Return password if it exists, otherwise return None

if __name__ == "__main__":
   print(sys.argv)
   if len(sys.argv) < 3:
      print("Not enough arguments.")
      sys.exit(1)

   command = sys.argv[1]
   master_password = sys.argv[2]
   password_manager = PasswordManager(master_password)

   match command:
      case "init":
         password_manager.initialize_database()
         print("Password manager initialized.")
      case "put":
         if len(sys.argv) != 5:
            print("Wrong number of arguments.")
            sys.exit(1)
         address = sys.argv[3]
         password = sys.argv[4]
         password_manager.store_password(address, password)
         print(f"Stored password for {address}.")
      case "get":
         if len(sys.argv) != 4:
            print("Wrong number of arguments.")
            sys.exit(1)
         address = sys.argv[3]
         retrieved_password = password_manager.retrieve_password(address)
         if retrieved_password:
            print(f"Password for {address} is: {retrieved_password}.")
         else:
            print("Master password incorrect or integrity check failed.")
      case _:
         print("Invalid command.")
         sys.exit(1)