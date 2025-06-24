import os
from myfactory import myfactory

def test():
   pets = []
   for module in os.listdir('plugins'):
      module_name, module_ext = os.path.splitext(module)
      if module_ext == '.py':
         pet = myfactory(module_name)("Ljubimac " + str(len(pets)))
         pets.append(pet)

   for pet in pets:
      print(pet.name + " pozdravlja:", pet.greet())
      print(pet.name + " voli", pet.menu() + ".")

if __name__ == "__main__":
   test()