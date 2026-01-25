import sys
import random
import matplotlib.pyplot as plt

class Individual:
    def __init__(self, solution, functions, rank=None, crowding=0.0):
        self.solution = solution
        self.functions = functions
        self.objectives = self.evaluate()
        self.rank = rank
        self.crowding = crowding

    def evaluate(self):
        return self.functions.evaluate(self.solution)

    def mutate(self):
        mutation_rate = 0.1
        for i in range(len(self.solution)):
            if random.random() < mutation_rate:
                lower_bound, upper_bound = self.functions.get_bounds()[i]
                self.solution[i] = random.uniform(lower_bound, upper_bound)
        self.objectives = self.evaluate()
        return self

def reset_crowding(population):
    for ind in population:
        ind.crowding = 0.0


class NSGAIIAlgorithm:
    def __init__(self, functions, population_size, generations, num_objectives, num_variables):
        self.functions = functions
        self.num_objectives = num_objectives
        self.num_variables = num_variables
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.fronts = []
        self.population = self.init_population()

    def init_population(self):
        pop = []
        bounds = self.functions.get_bounds()
        for _ in range(self.population_size):
            sol = [random.uniform(lb, ub) for lb, ub in bounds]
            pop.append(Individual(sol, self.functions))
        return pop

    def dominates(self, ind1, ind2):
        better_in_all = True
        better_in_at_least_one = False
        for m in range(self.num_objectives):
            if ind1.objectives[m] > ind2.objectives[m]:
                better_in_all = False
            elif ind1.objectives[m] < ind2.objectives[m]:
                better_in_at_least_one = True
        return better_in_all and better_in_at_least_one

    def non_dominated_sort(self, population):
        fronts = [[]]
        for p in population:
            p.dominated_solutions = []
            p.domination_count = 0
            for q in population:
                if p == q:
                    continue
                if self.dominates(p, q):
                    p.dominated_solutions.append(q)
                elif self.dominates(q, p):
                    p.domination_count += 1
            if p.domination_count == 0:
                p.rank = 0
                fronts[0].append(p)
        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for p in fronts[i]:
                for q in p.dominated_solutions:
                    q.domination_count -= 1
                    if q.domination_count == 0:
                        q.rank = i + 1
                        next_front.append(q)
            i += 1
            fronts.append(next_front)
        fronts.pop()
        return fronts

    def calculate_crowding_distance(self, front):
        if len(front) < 2:
            return
        m = len(front[0].objectives)
        for ind in front:
            ind.crowding = 0.0
        for i in range(m):
            front.sort(key=lambda x: x.objectives[i])
            front[0].crowding = float('inf')
            front[-1].crowding = float('inf')
            f_min = front[0].objectives[i]
            f_max = front[-1].objectives[i]
            if f_max - f_min == 0:
                continue
            for j in range(1, len(front) - 1):
                front[j].crowding += (front[j + 1].objectives[i] - front[j - 1].objectives[i]) / (f_max - f_min)

    def crowd_distance_sort(self, front, distances):
        sorted_front = sorted(front, key=lambda ind: distances.get(ind, 0.0), reverse=True)
        return sorted_front

    def solve(self):
        for gen in range(self.generations):
            fronts = self.non_dominated_sort(self.population)
            reset_crowding(self.population)
            for f in fronts:
                self.calculate_crowding_distance(f)
            offsprings = []
            while len(offsprings) < self.population_size:
                p1 = self.tournament()
                p2 = self.tournament()
                crossover_point = random.randint(1, len(p1.solution) - 1)
                child_solution1 = p1.solution[:crossover_point] + p2.solution[crossover_point:]
                child_solution2 = p2.solution[:crossover_point] + p1.solution[crossover_point:]
                child1 = Individual(child_solution1, self.functions)
                child2 = Individual(child_solution2, self.functions)
                child1 = child1.mutate()
                child2 = child2.mutate()
                offsprings.append(child1)
                offsprings.append(child2)
            combined = self.population + offsprings
            fronts = self.non_dominated_sort(combined)
            new_population = []
            i = 0
            while len(new_population) + len(fronts[i]) <= self.population_size:
                self.calculate_crowding_distance(fronts[i])
                new_population.extend(fronts[i])
                i += 1
            self.calculate_crowding_distance(fronts[i])
            fronts[i].sort(key=lambda x: x.crowding, reverse=True)
            new_population.extend(fronts[i][:self.population_size - len(new_population)])
            self.population = new_population
        fronts = self.non_dominated_sort(self.population)
        return self.population, fronts

    def tournament(self):
        a, b = random.sample(self.population, 2)
        return min(a, b, key=lambda x: (x.rank, -x.crowding))


class Function1:
    def __init__(self):
        pass
    def get_number_of_objectives(self):
        return 4
    def get_number_of_variables(self):
        return 4
    def evaluate(self, solution):
        x1, x2, x3, x4 = solution
        f1 = x1**2
        f2 = x2**2
        f3 = x3**2
        f4 = x4**2
        return [f1, f2, f3, f4]
    def get_bounds(self):
        return [(-5, 5)] * 4

class Function2:
    def __init__(self):
        pass
    def get_number_of_objectives(self):
        return 2
    def get_number_of_variables(self):
        return 2
    def evaluate(self, solution):
        x1, x2 = solution
        f1 = x1
        f2 = (1 + x2) / x1
        return [f1, f2]
    def get_bounds(self):
        return [(0.1, 1), (0.0, 5.0)]

def plot_solutions(functions, population):
    if functions.get_number_of_objectives() == 2:
        f1_values = [ind.objectives[0] for ind in population]
        f2_values = [ind.objectives[1] for ind in population]

        plt.figure(figsize=(6, 5))
        plt.scatter(f1_values, f2_values, s=15)

        plt.xlabel("f1")
        plt.ylabel("f2")
        plt.title("Pareto fronta – Problem 2")

        plt.xlim(0.1, 1.0)
        plt.ylim(0.0, 10.0)

        plt.grid(True)
        plt.tight_layout()
        plt.show()

def main():
    if len(sys.argv) != 4:
        print("Usage: python NSGA_II.py <function (1) or (2)> <population_size> <max_generations>")
        sys.exit(1)
    function_choice = int(sys.argv[1])
    population_size = int(sys.argv[2])
    max_generations = int(sys.argv[3])
    if function_choice == 1:
        functions = Function1()
    elif function_choice == 2:
        functions = Function2()
    else:
        print("Invalid function number, it should be 1 or 2")
        sys.exit(1)
    nsga = NSGAIIAlgorithm(functions, population_size, max_generations, functions.get_number_of_objectives(), functions.get_number_of_variables())
    population, fronts = nsga.solve()
    print("Final population:")
    for i, front in enumerate(fronts):
        num_in_front = 0
        print(f"Front {i + 1}:")
        for _ in front:
            num_in_front += 1
        print(f"Individual: {num_in_front}")
    with open("izlaz-dec.txt", "w") as f:
        for ind in population:
            f.write(" ".join(map(str, ind.solution)) + "\n")
    with open("izlaz-obj.txt", "w") as f:
        for ind in population:
            f.write(" ".join(map(str, ind.objectives)) + "\n")
    plot_solutions(functions, population)

if __name__ == "__main__":
    main()