from usermgmt import PasswordManager
import sys
import getpass

def main():
   if len(sys.argv) != 2:
      print("Usage: python .\login.py <user>")
      sys.exit(1)
   user = sys.argv[1]
   first = True
   password_manager = PasswordManager()
   password = getpass.getpass("Password: ")
   if password_manager.is_forcepass(user):
      for _ in range(3):
         if not first:
            password = getpass.getpass("Password: ")
         if password_manager.check_password(user, password):      
            new_password = getpass.getpass("New password: ")
            repeat_password = getpass.getpass("Repeat password: ")
            if new_password == password:
               print("New password must be different from the old one.")
            elif len(new_password) < 8 and len(repeat_password) < 8:
               print("Password must be at least 8 characters long.")
            elif new_password == repeat_password:
               password_manager.change_password(user, new_password, repeat_password)
               print("bash$")
               password_manager.force_password_change(user, False)
               break
            else:
               print("Passwords do not match.")
            first = False
         else:
            print("Username or password incorrect.")
            first = False
   else:
      for _ in range(3):
         if not first:
            password = getpass.getpass("Password: ")
            first = False
         if password_manager.login(user, password) and password_manager.exists(user):
            print("bash$")
            break
         else:
            print("Username or password incorrect.")
            first = False
            
if __name__ == "__main__":
   main()