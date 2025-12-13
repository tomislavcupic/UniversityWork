import sys

def main():

   if len(sys.argv) != 3:
      print("Usage: python .\solution.py resolution <file-name>")
      sys.exit(1)
   if sys.argv[1] != "resolution":
      print("Invalid argument")
      sys.exit(1)
   
   clauses = []
   counter = 0
   with open(sys.argv[2], "r") as file:
      for line in file:
         if line.startswith('#'):
            continue
         else:
            line = line.lower()
            clauses.append(line.replace(" v","").strip().split(" ")) #dodaj counter na pocetak svakog clana liste
            counter += 1
   last = clauses[counter-1][0]
   clauses[counter-1] = ["~" + clauses[counter-1][0]]
   if resolve(clauses):
      print_nicely(clauses)
      print("[CONCLUSION]: " + str(last) + " is true")
   else:
      print("[CONCLUSION]: " + str(last) + " is unknown")
   

def resolve(clauses):
   #print("clauses: ", clauses)
   while True:
      new = []
      counter = 0
      for i in range(len(clauses)):
         #print(clauses[i], clauses[len(clauses)-1])
         resolvents = resolve_pair(clauses[i], clauses[len(clauses)-1])
         #print("resolvents: ", resolvents)
         if resolvents == []:
            #print("No resolvents," + str(counter))
            continue
         if resolvents == ["NIL"]:
            return True
         for r in resolvents: 
            if r not in clauses and r not in new:
               new.append(r)
         counter += 1
      if new == []:
         return False
      for n in new:
         if n not in clauses:
            clauses.append(n)


def resolve_pair(clause1, clause2):
   resolvents = []
   if len(clause1) == 1 and len(clause2) == 1:
      if clause1[0] == "~" + clause2[0] or clause2[0] == "~" + clause1[0]:
         print("NIL") #dodaj counter
         return ["NIL"]
   for i in range(len(clause1)):
      for j in range(len(clause2)):
         if clause1[i] == "~" + clause2[j] or clause2[j] == "~" + clause1[i]:
            resolvents.append(clause1[:i] + clause1[i+1:] + clause2[:j] + clause2[j+1:])

   return resolvents


def print_nicely(clauses):
   for i in range(len(clauses)):
      print(i + 1, end=" ")
      for j in range(len(clauses[i])):
         print(clauses[i][j], end=" ")
      print()
   print("===============")

if __name__ == "__main__":
      main()