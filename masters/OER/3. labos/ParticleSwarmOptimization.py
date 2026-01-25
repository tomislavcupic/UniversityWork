import random
import sys
import math

class ParticleSwarmOptimization:
    def __init__(self, func, dim, minimize=True, max_iter=100000, cognitive=2, social=2, inertia=0.9, swarm_size=30, topology='global', nbmc=0.1, neigh_size=1, bounds=None, vmax_frac=0.1):
        self.func = func
        self.dim = dim
        self.minimize = minimize
        self.cognitive = cognitive
        self.social = social
        self.inertia = inertia
        self.swarm_size = swarm_size
        self.max_iter = max_iter
        self.topology = topology

        self.nbmc = nbmc
        self.neigh_size = neigh_size

        if bounds is None:
            self.bounds = [(-1e2, 1e2)] * dim
        elif isinstance(bounds, tuple) and len(bounds) == 2:
            self.bounds = [bounds] * dim
        else:
            self.bounds = bounds

        self.vmax_frac = vmax_frac

    def get_neighbor(self, params):
        return [p + random.uniform(-self.nbmc, self.nbmc) for p in params]

    def solve(self, initial=None):
        swarm = []
        for _ in range(self.swarm_size):
            position = [random.uniform(lo, hi) for (lo, hi) in self.bounds]
            velocity = [random.uniform(-(hi - lo) * 0.01, (hi - lo) * 0.01) for (lo, hi) in self.bounds]
            best_position = position[:]
            best_eval = self.func(position)
            swarm.append({'position': position, 'velocity': velocity, 'best_position': best_position, 'best_eval': best_eval})

        if self.minimize:
            global_best_particle = min(swarm, key=lambda p: p['best_eval'])
        else:
            global_best_particle = max(swarm, key=lambda p: p['best_eval'])
        global_best_position = global_best_particle['best_position'][:]
        global_best_eval = global_best_particle['best_eval']

        iter_count = 0
        while iter_count < self.max_iter:
            for idx, particle in enumerate(swarm):
                r1 = random.random()
                r2 = random.random()
                cognitive_velocity = [self.cognitive * r1 * (bp - p) for p, bp in zip(particle['position'], particle['best_position'])]

                if self.topology == 'local':
                    neigh_indices = []
                    for offset in range(-self.neigh_size, self.neigh_size + 1):
                        neigh_indices.append((idx + offset) % self.swarm_size)
                    if self.minimize:
                        local_best = min((swarm[i] for i in neigh_indices), key=lambda p: p['best_eval'])
                    else:
                        local_best = max((swarm[i] for i in neigh_indices), key=lambda p: p['best_eval'])
                    social_target = local_best['best_position']
                else:
                    social_target = global_best_position

                social_velocity = [self.social * r2 * (gbp - p) for p, gbp in zip(particle['position'], social_target)]

                particle['velocity'] = [self.inertia * v + cv + sv for v, cv, sv in zip(particle['velocity'], cognitive_velocity, social_velocity)]
                vmax = [(hi - lo) * self.vmax_frac for (lo, hi) in self.bounds]
                particle['velocity'] = [max(min(v, vm), -vm) for v, vm in zip(particle['velocity'], vmax)]

                particle['position'] = [p + v for p, v in zip(particle['position'], particle['velocity'])]
                particle['position'] = [max(min(p, hi), lo) for p, (lo, hi) in zip(particle['position'], self.bounds)]
                current_eval = self.func(particle['position'])
                if (self.minimize and current_eval < particle['best_eval']) or (not self.minimize and current_eval > particle['best_eval']):
                    particle['best_position'] = particle['position'][:]
                    particle['best_eval'] = current_eval
                    if (self.minimize and current_eval < global_best_eval) or (not self.minimize and current_eval > global_best_eval):
                        global_best_position = particle['position'][:]
                        global_best_eval = current_eval
            iter_count += 1
            if iter_count % 1000 == 0:
                print(f"Iteracija {iter_count}: Najbolje = {global_best_eval:.6f}")
        return global_best_position, global_best_eval
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
    pso = ParticleSwarmOptimization(mse_func, dim=6, minimize=True, max_iter=2000)
    best, best_eval = pso.solve()

    print("\nNajbolje pronađeno rješenje:")
    names = ['a', 'b', 'c', 'd', 'e', 'f']
    for n, v in zip(names, best):
        print(f"{n} = {v:.6f}")
    print(f"Minimalna pogreška (MSE): {best_eval:.6f}")