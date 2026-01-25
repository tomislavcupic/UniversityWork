import sys
import math, random

class DifferentialEvolution:
    def __init__(self, func, dim, minimize=True, max_iter=100000, pop_size=60, F=0.8, CR=0.9, bounds=None, initial='Random', number_of_linear_combinations=1, strategy='rand'):
        self.func = func
        self.dim = dim
        self.minimize = minimize
        self.max_iter = max_iter
        self.pop_size = pop_size
        self.F = F
        self.CR = CR
        self.initial = initial
        self.number_of_linear_combinations = number_of_linear_combinations
        self.strategy = strategy

        if bounds is None:
            self.bounds = [(-20, 20)] * dim
        elif isinstance(bounds, tuple) and len(bounds) == 2:
            self.bounds = [bounds] * dim
        else:
            self.bounds = bounds

    def solve(self, initial=None):
        population = []
        if self.initial == 'Random' or initial is None:
            for _ in range(self.pop_size):
                individual = [random.uniform(lo, hi) for (lo, hi) in self.bounds]
                population.append(individual)
        iter_count = 0
        while iter_count < self.max_iter:
            new_population = []
            for i in range(self.pop_size):
                target = population[i]
                donor = []
                if self.strategy == 'best':
                    indices = list(range(self.pop_size))
                    indices.remove(i)
                    a, b, c = random.sample(indices, 3)
                    if self.minimize:
                        best_local = min((a, b, c), key=lambda idx: self.func(population[idx]))
                    else:
                        best_local = max((a, b, c), key=lambda idx: self.func(population[idx]))
                    base_vector = population[best_local]
                    others = [idx for idx in (a, b, c) if idx != best_local]
                    r1, r2 = others[0], others[1]
                else:
                    indices = list(range(self.pop_size))
                    indices.remove(i)
                    a, b, c = random.sample(indices, 3)
                    base_vector = population[a]
                    r1, r2 = b, c
                j_rand = random.randrange(self.dim)
                for j in range(self.dim):
                    if random.random() < self.CR or j == j_rand:
                        mutated_gene = base_vector[j] + self.F * (population[r1][j] - population[r2][j])
                        #lo, hi = self.bounds[j]
                        #mutated_gene = max(min(mutated_gene, hi), lo)
                        donor.append(mutated_gene)
                    else:
                        donor.append(target[j])
                target_eval = self.func(target)
                donor_eval = self.func(donor)
                if (self.minimize and donor_eval <= target_eval) or (not self.minimize and donor_eval >= target_eval):
                    new_population.append(donor)
                else:
                    new_population.append(target)
            iter_count += 1
            population = new_population
            if iter_count % 50 == 0:
                min_eval = min(self.func(ind) for ind in population)
                best_vector = min(population, key=lambda ind: self.func(ind))
                print(f"iteration: {iter_count}, min: {min_eval:.6f}")
        if self.minimize:
            best_individual = min(population, key=lambda ind: self.func(ind))
        else:
            best_individual = max(population, key=lambda ind: self.func(ind))
        best_eval = self.func(best_individual)
        return best_individual, best_eval
    
def model(params, x1, x2, x3, x4, x5):
   a, b, c, d, e, f = params
   arg = d * x3
   #arg = max(min(arg, 50), -50)
   return a * x1 + b * (x1 ** 3) * x2 + c * math.exp(arg) * (1 + math.cos(e * x4)) + f * x4 * (x5 ** 2)

def make_mse(data):
    def mse(params):
        s = 0.0
        for (x1, x2, x3, x4, x5, y) in data:
            ypred = model(params, x1, x2, x3, x4, x5)
            #print(f"Predicted: {ypred:.6f}, Actual: {y:.6f}")
            s += (y - ypred) ** 2
        return s / len(data)
    return mse

def load_data(path):
    data = []
    with open(path) as f:
        for line in f:
            parts = line.strip().strip('[]').replace(',', ' ').split()
            if len(parts) == 6:
                data.append(tuple(map(float, parts)))
    return data

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Upotreba: python main.py <algoritam> <ulazna_datoteka> [topologija]")
        sys.exit(1)

    alg = sys.argv[1]
    path = sys.argv[2]
    topology = sys.argv[3] if len(sys.argv) >= 4 else 'global'
    data = load_data(path)

    mse_func = make_mse(data)
    de = DifferentialEvolution(mse_func, dim=6, minimize=True, max_iter=2000, strategy='rand')
    best, best_eval = de.solve()
    print("\nPrebacivanje na strategiju 'best'...\n")
    de2 = DifferentialEvolution(mse_func, dim=6, minimize=True, max_iter=2000, strategy='best')
    best2, best_eval2 = de2.solve()

    print("\nNajbolje pronađeno rješenje:")
    names = ['a', 'b', 'c', 'd', 'e', 'f']
    for n, v in zip(names, best):
        print(f"{n} = {v:.6f}")
    print(f"Minimalna pogreška (MSE): {best_eval:.6f}")
    if alg == 'de':
        print("\nNakon prebacivanja na strategiju 'best':")
        for n, v in zip(names, best2):
            print(f"{n} = {v:.6f}")
        print(f"Minimalna pogreška (MSE): {best_eval2:.6f}")