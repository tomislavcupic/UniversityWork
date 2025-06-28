import sys
import time
from typing import Counter

def dpll(klauzule, dodjele):
   if klauzule is None:
      return None
   
   if len(klauzule) == 0:
      return dodjele

   if any(len(k) == 0 for k in klauzule):
      return None
   
   klauzule, dodjele = pjk(klauzule, dodjele)
   if klauzule is None:
      return None

   klauzule, dodjele = ukcl(klauzule, dodjele)
   if klauzule is None:
      return None

   # print("\n klauzule", klauzule)
   # print("\n")

   var = choose_var(klauzule, dodjele)
   if var is None:
      return dodjele
   

   for value in [True, False]:
      new_assignment = dodjele.copy()
      new_assignment[var] = value
      new_clauses = simplify_clauses(klauzule, var, value)
      if new_clauses is None:
         continue
      result = dpll(new_clauses, new_assignment)
      if result is not None:
         return result

   return None

def tautologija(klauzula):
   set_literala = set(klauzula)
   return any(-literal in set_literala for literal in set_literala)

def ukloni_nadskupove(klauzule):
   klauzule = [set(k) for k in klauzule]
   nove = []
   for i, k1 in enumerate(klauzule):
      if not any(k1 > k2 for j, k2 in enumerate(klauzule) if i != j):
         nove.append(list(k1))
   return nove

def hidden_literal_elimination(klauzule):
   lit_count = Counter()
   for klauz in klauzule:
      for lit in klauz:
         lit_count[lit] += 1

   eliminirani = set()
   for lit in lit_count:
      if -lit not in lit_count:
         eliminirani.add(lit)

   nove_klauzule = []
   for klauz in klauzule:
      nova = [l for l in klauz if l not in eliminirani]
      if len(nova) == 0:
         continue
      nove_klauzule.append(nova)

   return nove_klauzule

def simplify_clauses(klauzule, var, value):
   literal = var if value else -var
   nove_klauzule = []
   for klauzula in klauzule:
      if literal in klauzula:
         continue
      if -literal in klauzula:
         new_clause = [l for l in klauzula if l != -literal]
         if not new_clause:
               return None
         nove_klauzule.append(new_clause)
      else:
         nove_klauzule.append(klauzula)
   return nove_klauzule


def choose_var(klauzule, dodjele):
   all_literals = []
   for klauzula in klauzule:
      for literal in klauzula:
         if abs(literal) not in dodjele:
            all_literals.append(abs(literal))
   counts = Counter(all_literals)
   if not counts:
      return None
   return counts.most_common(1)[0][0]

def ukcl(klauzule, dodjele):
   pure_literals = []
   all_lit = []
   for klauz in klauzule:
      for literal in klauz:
         all_lit.append(literal)
   counts = Counter(all_lit)
   for literal in counts:
      if -literal not in counts:
         pure_literals.append(literal)
   for literal in pure_literals:
      var = abs(literal)
      if var not in dodjele:
         dodjele[var] = literal > 0
   nove_klauzule = []
   for klauzula in klauzule:
      if not any(l in klauzula for l in pure_literals):
         nove_klauzule.append(klauzula)
   return nove_klauzule, dodjele

def pjk(klauzule, dodjele):
   promjena = True
   while promjena:
      promjena = False
      jedinicne = [k for k in klauzule if len(k) == 1]
      if not jedinicne:
         break
      for klauzula in jedinicne:
         literal = klauzula[0]
         var = abs(literal)
         value = literal > 0
         if var in dodjele:
            if dodjele[var] != value:
               return None, None
            continue
         dodjele[var] = value
         promjena = True
         nove_klauzule = []
         for k in klauzule:
            if literal in k:
               continue
            elif -literal in k:
               nova = [i for i in k if i != -literal]
               if not nova:
                  return None, None
               nove_klauzule.append(nova)
            else:
               nove_klauzule.append(k)
         klauzule = nove_klauzule
   return klauzule, dodjele

def literal_equivalence_propagation(klauzule):
   equivalence = {}

   klauzule_set = set(tuple(sorted(k)) for k in klauzule)
   candidates = []

   for k in klauzule_set:
      if len(k) != 2:
         continue
      a, b = k
      mirror = tuple(sorted([-a, -b]))
      if mirror in klauzule_set:
         if abs(a) == abs(b):
            continue
         if (a > 0) == (b > 0):
            candidates.append((abs(a), abs(b), "eq"))
         else:
            candidates.append((abs(a), abs(b), "neg"))

   for a, b, tip in candidates:
      globalna = True
      for kl in klauzule:
         if tip == "eq":
            if (a in map(abs, kl) and b in map(abs, kl)):
               #predznaci
               for lit1 in kl:
                  if abs(lit1) == a:
                     sign_a = lit1 > 0
                  if abs(lit1) == b:
                     sign_b = lit1 > 0
               if sign_a != sign_b:
                  globalna = False
                  break
         else:
            if (a in map(abs, kl) and b in map(abs, kl)):
               for lit1 in kl:
                  if abs(lit1) == a:
                     sign_a = lit1 > 0
                  if abs(lit1) == b:
                     sign_b = lit1 > 0
               if sign_a == sign_b:
                  globalna = False
                  break
      if globalna:
         if tip == "eq":
            equivalence[b] = a
         else:
            equivalence[b] = -a

   def zamijeni_lit(lit):
      val = abs(lit)
      if val in equivalence:
         new_lit = equivalence[val]
         #print("dodan novi")
         return new_lit if lit > 0 else -new_lit
      return lit

   nove_klauzule = []
   for klauz in klauzule:
      nova = list(set(zamijeni_lit(l) for l in klauz))
      if not tautologija(nova):
         nove_klauzule.append(nova)

   return nove_klauzule

def main():
   naziv_datoteke = input("unesite naziv cnf datoteke (bez .cnf): ")
   lista_stanja = []
   with open(f"{naziv_datoteke}.cnf") as f:
      for line in f:
         line = line.strip()
         if line[0] == "p":
            line = line.split(" ")
            broj_varijabli = line[2]
            broj_klauzula = line[3]
            stanja = {}
            for i in range(int(line[2])):
               stanja[f"x{i + 1}"] = False
            #print(stanja)
         elif line[0] not in " 1234567890-" or line[0] == "c":
            continue
         else:
            clause = list(map(int, line.split()))
            if clause[-1] == 0:
               clause = clause[:-1]
            if len(clause) != 0 and not tautologija(clause):
               lista_stanja.append(clause)
   lista_stanja = ukloni_nadskupove(lista_stanja)
   start = time.time()
   lista_stanja = hidden_literal_elimination(lista_stanja)
   #lista_stanja = literal_equivalence_propagation(lista_stanja)
   
   rezultat = dpll(lista_stanja, {})
   end = time.time()
   print(f"vrijeme izvođenja: ", end - start)

   if rezultat is None:
      print("nije zadovoljiva")
   else:
      print(" zadovoljiva ")
   with open(f"{naziv_datoteke}.txt", "w") as izlaz:
      if rezultat is None:
         izlaz.write("Nije uspješno\n")
      else:
         for i in range(1, int(broj_varijabli) + 1):
            val = rezultat.get(i, False)
            izlaz.write(f"v{i} = {'true' if val else 'false'}\n")

if __name__ == "__main__":
   main()