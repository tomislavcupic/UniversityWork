import os
import sys
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import getpass
import binascii

class PasswordManager:
   def __init__(self):
      self.passwords = {}
      self.forcepasses = {}
      self._read_from_disk()
      self._read_forcepasses_from_disk()

   def _get_salt(self, new_salt=False):
      return os.urandom(16)
   
   def _hash_password(self, password, salt):
      return binascii.hexlify(PBKDF2(password, salt, dkLen=64, count=3000000, hmac_hash_module=SHA512)).decode()
   
   def _write_to_disk(self):
      with open("passwords.dat", "w") as file:
         file.write(str(self.passwords))

   def _read_from_disk(self):
      if not os.path.exists("passwords.dat"):
         return
      with open("passwords.dat", "r") as file:
         self.passwords = eval(file.read())
   
   def add_user(self, username, password):
      self._read_from_disk()
      self._read_forcepasses_from_disk()
      salt = self._get_salt()
      self.passwords[username] = {'salt': binascii.hexlify(salt).decode(), 'password': self._hash_password(password, salt)}
      self.forcepasses[username] = False
      self._write_to_disk()
      self._write_forcepasses_to_disk()
      return True

   def change_password(self, username, new_password, new_password_repeat):
      self._read_from_disk()
      if new_password_repeat == new_password:
         salt = self._get_salt()
         self.passwords[username] = {'salt': binascii.hexlify(salt).decode(), 'password': self._hash_password(new_password_repeat, salt)}
         self._write_to_disk()
         return True
      return False
   
   def force_password_change(self, username, force):
      self._read_forcepasses_from_disk()
      self.forcepasses[username] = force
      self._write_forcepasses_to_disk()
      
   def is_forcepass(self, username):
      self._read_forcepasses_from_disk()
      try:
         if self.exists(username) and self.forcepasses[username]:
            return True
      except KeyError:
         return False
      return False

   def _write_forcepasses_to_disk(self):
      data_to_write = str(self.forcepasses).encode()
      with open("forcepasses.dat", "wb") as file:
         file.write(data_to_write)

   def _read_forcepasses_from_disk(self):
      if not os.path.exists("forcepasses.dat"):
         return
      with open("forcepasses.dat", "rb") as file:
         data = file.read().decode()
      self.forcepasses = eval(data)

   def delete_user(self, username):
      self._read_from_disk()
      self._read_forcepasses_from_disk()
      del self.passwords[username]
      del self.forcepasses[username]
      self._write_to_disk()
      self._write_forcepasses_to_disk()

   def exists(self, username):
      self._read_from_disk()
      if username in self.passwords:
         return True
      return False
   
   def login(self, username, password):
      self._read_from_disk()
      try:
         user_data = self.passwords[username]
         if user_data['password'] == self._hash_password(password, binascii.unhexlify(user_data['salt'])):
            return True
      except KeyError:
         return False
      return False
   
   def check_password(self, user, password):
      self._read_from_disk()
      user_data = self.passwords[user]
      if user_data['password'] == self._hash_password(password, binascii.unhexlify(user_data['salt'])):
         return True
      return False
   
def main():
   if len(sys.argv) != 3:
      print("Usage: python .\labos.py <action> <user>")
      sys.exit(1)

   action = sys.argv[1]
   user = sys.argv[2]

   password_manager = PasswordManager()

   if action == "add":
      password = getpass.getpass("Password: ")
      repeat_password = getpass.getpass("Repeat password: ")
      if len(password) < 8 and len(repeat_password) < 8:
         print("Password must be at least 8 characters long.")
      elif password != repeat_password:
         print("User add failed. Passwords mismatch.")
      else:
         password_manager.add_user(user, password)
         print("User " + str(user) + " successfully added.")

   elif action == "passwd":
      if not password_manager.exists(user):
         print("Password change failed. User does not exist.")
      else:
         new_password = getpass.getpass("Password ")
         new_password_repeat = getpass.getpass("Repeat Password: ")
         if len(new_password) < 8 and len(new_password_repeat) < 8:
            print("Password must be at least 8 characters long.")
         elif password_manager.change_password(user, new_password, new_password_repeat):
            print("Password change successful.")
         else:
            print("Password change failed. Passwords mismatch.")

   elif action == "forcepass":
      if password_manager.exists(user):
         password_manager.force_password_change(user, True)
         print("User will be requested to change password on next login.")
      else:
         print("User does not exist.")

   elif action == "del":
      if password_manager.exists(user):
         password_manager.delete_user(user)
         print("User successfuly removed")
      else:
         print("User does not exist.")

   else:
      print("Invalid action.")

if __name__ == "__main__":
   main()