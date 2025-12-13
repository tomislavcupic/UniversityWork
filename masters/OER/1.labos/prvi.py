import sys
from random import *

def parse_input(input_file):
   new_data = []
   with open(input_file, 'r') as f:
      data = f.readline().strip().split()
      while data[0] != '%':
         data = f.readline().strip().split()
         if data[0] == 'c':
            pass
         elif data[0] == 'p':
            num_vars = data[2]
            num_clauses = data[3] 
         elif data[0] == '%':
            break
         else:
            new_data.append([int(x) for x in data[:-1]])
   return num_vars, num_clauses, new_data

def generate_neighbors(assignment_int, num_vars):
   neighbors = []
   for i in range(int(num_vars)):
      neighbor = assignment_int ^ (1 << i)
      neighbors.append(neighbor)
   return neighbors

def evaluate(assignment_int, data, num_vars, num_clauses):
   number_of_satisfied_clauses = 0
   for i in range(int(num_clauses)):
      clause = data[i]
      if any(((literal > 0 and ((assignment_int >> (literal - 1)) & 1) == 1) or
                  (literal < 0 and ((assignment_int >> (-literal - 1)) & 1) == 0)) for literal in clause):
         number_of_satisfied_clauses += 1
   return number_of_satisfied_clauses

def update_post(post, data, assignment_int, num_clauses, percentageup = 0.01, percentagedown = 0.1):
   for i in range(int(num_clauses)):
      clause = data[i]
      if any(((literal > 0 and ((assignment_int >> (literal - 1)) & 1) == 1) or
                  (literal < 0 and ((assignment_int >> (-literal - 1)) & 1) == 0)) for literal in clause):
         post[i] += (1 - post[i])*percentageup
      else:
         post[i] += (0 - post[i])*percentagedown
   return post

##########################---------------------------Algorithm 1. - Exhaustive search----------------------------------########################################3

def exhaustive_search(data, num_vars, num_clauses):
   print("Number of variables:", num_vars)
   print("Number of clauses:", num_clauses)
   for i in range(2**int(num_vars)):
      assignment = [(i >> j) & 1 for j in range(int(num_vars))]
      satisfied = True
      for clause in data:
         clause_satisfied = False
         for literal in clause:
            var_index = abs(literal) - 1
            if (literal > 0 and assignment[var_index] == 1) or (literal < 0 and assignment[var_index] == 0):
               clause_satisfied = True
               break
         if not clause_satisfied:
            satisfied = False
            break
      if satisfied:
         print("Satisfied assignment: ", assignment)
         pass
   return

#####################------------------------Algorithm 2. - Local iterative search-------------------------------############################

def iterative_search(data, num_vars, num_clauses, start=None):
   if start == None:
      start = randint(0, 2**int(num_vars)-1)
   print("number of clauses", num_clauses)
   t = 0
   while t < 100000:
      Best_solutions = generate_neighbors(start, num_vars)
      Best_solution = []
      best_eval = -1
      for solution in Best_solutions:
         current_eval = evaluate(solution, data, num_vars, num_clauses)
         if current_eval > best_eval:
            best_eval = current_eval
            Best_solution = [solution]
         elif current_eval == best_eval:
            Best_solution.append(solution)
      Best_solution = Best_solution[randint(0, len(Best_solution)-1)] # ovdje bi sva rješenja trebala imati istu vrijednost
      if evaluate(Best_solution, data, num_vars, num_clauses) <= evaluate(start, data, num_vars, num_clauses):
         print("found local maximum after", t, "iterations")
         break
      else:
         start = Best_solution
      t += 1
   print("Best found solution:", [(start >> j) & 1 for j in range(int(num_vars))])
   print("in number of satisfied clauses:", evaluate(start, data, num_vars, num_clauses))
   return start

#####################------------------------Algorithm 3. - Modified iterative search------------------------------##########################3

def iterative_search2(data, num_vars, num_clauses, number_of_best = 2, percentage = 50):
   start = randint(0, 2**int(num_vars)-1)
   print("number of clauses", num_clauses)
   t = 0

   post = [0 for _ in range(int(num_clauses))]

   while t < 100000:
      post = update_post(post, data, start, num_clauses)
      #print("post:", post)
      Neighbours = generate_neighbors(start, num_vars)
      Best_solution = []

      for solution in Neighbours:
         Z = evaluate(solution, data, num_vars, num_clauses)
         if Z == int(num_clauses):
            Best_solution = [solution]
            print("Found optimal solution:", [(solution >> j) & 1 for j in range(int(num_vars))])
            print("number of iterations:", t)
            return
         for i in range(int(num_clauses)):
            clause = data[i]
            if any(((literal > 0 and ((solution >> (literal - 1)) & 1) == 1) or
                        (literal < 0 and ((solution >> (-literal - 1)) & 1) == 0)) for literal in clause):
               Z = Z + percentage * (1 - post[i])
            else:
               Z = Z - percentage * (1 - post[i])
         Best_solution.append((solution, Z))
      if not Best_solution:
            print("No solutions found. Debug info:")
            print("Current start value:", start)
            print("Number of neighbors:", len(Neighbours))
            print("Post values:", post)
            break
      Best_solution.sort(key=lambda x: x[1], reverse=True)
      Best_solution = [x[0] for x in Best_solution[:number_of_best]]
      start = Best_solution[randint(0, len(Best_solution)-1)]
      t += 1
      if t % 100 == 0:
         print("iteration:", t, "best eval:", evaluate(start, data, num_vars, num_clauses))
   print("Best found solution:", [(start >> j) & 1 for j in range(int(num_vars))])
   print("in number of satisfied clauses:", evaluate(start, data, num_vars, num_clauses))
   return

###############-------------------Algorithm 4. - GSAT algorithm-------------------------------#################################3

def gsat(data, num_vars, num_clauses, max_flips=1000, max_restarts=200):
   print("number of clauses", num_clauses)
   num_vars = int(num_vars)
   num_clauses = int(num_clauses)
   for restart in range(max_restarts):
      T = randint(0, 2**num_vars - 1)
      z_value = evaluate(T, data, num_vars, num_clauses)
      #print("new start, z_value", z_value)
      for flip in range(max_flips):
         if z_value == num_clauses:
               print("Found optimal solution:", [(T >> j) & 1 for j in range(num_vars)])
               print("number of restarts and flips:", restart, flip)
               return

         neighbors = []
         for i in range(num_vars):
               T_neighbor = T ^ (1 << i)
               unsatisfied_count = 0
               for j in range(num_clauses):
                  clause = data[j]
                  if not any(((literal > 0 and ((T_neighbor >> (literal - 1)) & 1) == 1) or
                              (literal < 0 and ((T_neighbor >> (-literal - 1)) & 1) == 0)) for literal in clause):
                     unsatisfied_count += 1

               neighbors.append((i, num_clauses - unsatisfied_count)) 

               if unsatisfied_count == 0:
                  print("Found optimal solution:", [(T_neighbor >> j) & 1 for j in range(num_vars)])
                  print("number of restarts and flips:", restart, flip)
                  return

         max_goodness = max(s for _, s in neighbors)
         max_neighbors = [i for i, s in neighbors if s == max_goodness]

         if max_goodness <= z_value:
               break

         chosen_var = choice(max_neighbors)
         T ^= (1 << chosen_var)
         z_value = max_goodness

   print("No satisfying assignment found after maximum restarts.")
   return

######################------------------------Algorithm 5. - RandomWalkSAT algorithm------------------------------##################################3

def random_walk_sat(data, num_vars, num_clauses, max_flips=1000, max_tries = 100, p = 0.5):
   
   def is_clause_satisfied(clause, assignment):
        return any(
            (literal > 0 and ((assignment >> (literal - 1)) & 1) == 1) or
            (literal < 0 and ((assignment >> (-literal - 1)) & 1) == 0)
            for literal in clause
        )
   def get_unsatisfied_clauses(data, assignment):
      return [i for i, clause in enumerate(data) if not is_clause_satisfied(clause, assignment)]
   
   for attempt in range(max_tries):
      T = randint(0, 2**int(num_vars)-1)
      if evaluate(T, data, num_vars, num_clauses) == int(num_clauses):
         print("Found optimal solution:", [(T >> j) & 1 for j in range(int(num_vars))])
         print("number of attempts and flips:", attempt, flip)
         return

      for flip in range(max_flips):

         unsatisfied_clauses = get_unsatisfied_clauses(data, T)
         unsat_clause = choice(unsatisfied_clauses)
         # mozda ovdje treba dodat provjeru ako je unsat_clause prazan
         clause = data[unsat_clause]
         if random() < p:
            var_to_flip = abs(choice(clause)) - 1
         else:
            best_var = None
            best_eval = -1
            for literal in clause:
               candidate = T ^ (1 << (abs(literal) - 1))
               eval_score = evaluate(candidate, data, num_vars, num_clauses)
               if eval_score > best_eval:
                  best_eval = eval_score
                  best_var = abs(literal) - 1
            var_to_flip = best_var

         T ^= (1 << var_to_flip)

         if evaluate(T, data, num_vars, num_clauses) == int(num_clauses):
            print("Found optimal solution:", [(T >> j) & 1 for j in range(int(num_vars))])
            print("number of attempts and flips:", attempt, flip)
            print("number of clauses", num_clauses)
            print("number of correct clauses:", evaluate(T, data, num_vars, num_clauses))
            return

   print("No satisfying assignment found after maximum tries.")
   return

######################-----------------------Algorithm 6. - Iterated local search----------------------------############################

def iterated_local_search(data, num_vars, num_clauses, perturbation_rate=20, max_iterations=100, local_max_flips=5000):
   num_vars = int(num_vars)
   num_clauses = int(num_clauses)
   s = randint(0, 2**int(num_vars) - 1)
   s = iterative_search(data, num_vars, num_clauses)

   best_eval = evaluate(s, data, num_vars, num_clauses)

   print(f"Initial evaluation: {best_eval}/{num_clauses}")
   
   for _ in range(max_iterations):
      num_flips = max(1, int(num_vars * perturbation_rate / 100))
      #num_flips = 2
      s_pert = s
      for _ in range(num_flips):
         var_to_flip = randint(0, num_vars - 1)
         s_pert ^= (1 << var_to_flip)

      s_double_prime = iterative_search(data, num_vars, num_clauses, start=s_pert)
      s_double_prime_eval = evaluate(s_double_prime, data, num_vars, num_clauses)

      if s_double_prime_eval > best_eval:
         s = s_double_prime
         best_eval = s_double_prime_eval
      
      if best_eval == num_clauses:
         print("optimal solution found")
         break
   print("\nBest found solution:")
   print([(s >> j) & 1 for j in range(num_vars)])
   print("Number of satisfied clauses:", best_eval)
   return s

######################-----------------------Main function----------------------------############################

def main():
   if len(sys.argv) != 3:
      print("Usage: python prvi.py algorithm <input_file>")
      sys.exit(1)   
   algorithm = sys.argv[1]
   input_file = sys.argv[2]
   num_vars, num_clauses, data = parse_input(input_file)
   match(algorithm):
      case "exhaustive":
         print("Running exhaustive search algorithm")
         exhaustive_search(data, num_vars, num_clauses)
      case "iterative":
         print("Running iterative algorithm")
         iterative_search(data, num_vars, num_clauses)
      case "mod_iterative":
         print("Running modified iterative algorithm")
         iterative_search2(data, num_vars, num_clauses)
      case "gsat":
         gsat(data, num_vars, num_clauses)
      case "rwsat":
         random_walk_sat(data, num_vars, num_clauses)
      case "ils":
         iterated_local_search(data, num_vars, num_clauses)
      case _:
         print("wrong algorithm name")

if __name__ == "__main__":
   main()