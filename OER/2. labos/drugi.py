import random
import math
import copy
import argparse
from typing import List, Tuple, Union, Callable, Optional
import numpy as np

def parse_config(path):
    cfg = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' not in line:
                continue
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            cfg[key] = val
    print(cfg)
    return cfg

def p_div(a, b):
    try:
        if abs(b) < 1e-12:
            return 1.0
        return a / b
    except Exception:
        return 1.0

def p_sqrt(a):
    try:
        if a < 0:
            return 0
        return math.sqrt(a)
    except Exception:
        return 0

def p_log10(a):
    try:
        if a <= 0:
            return 1.0
        return math.log10(a)
    except Exception:
        return 1.0

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def is_function(self, function_set):
        return isinstance(self.value, str) and self.value in function_set

    def is_terminal(self, function_set):
        return not self.is_function(function_set)

    def arity(self, function_set):
        if self.is_function(function_set):
            return function_set[self.value]
        return 0

    def copy(self):
        return copy.deepcopy(self)

    def node_count(self):
        return 1 + sum(child.node_count() for child in self.children)

    def depth(self):
        if not self.children:
            return 1
        return 1 + max(child.depth() for child in self.children)

    def traverse(self):
        nodes = [self]
        for child in self.children:
            nodes.extend(child.traverse())
        return nodes

    def replace_child(self, old_node, new_node):
        for i, child in enumerate(self.children):
            if child is old_node:
                self.children[i] = new_node
                return True
            if child.replace_child(old_node, new_node):
                return True
        return False

    def evaluate(self, xvars, function_map, function_set):
        try:
            if self.is_function(function_set):
                name = self.value
                ar = function_set[name]
                if ar == 2:
                    a = self.children[0].evaluate(xvars, function_map, function_set)
                    b = self.children[1].evaluate(xvars, function_map, function_set)
                    return function_map[name](a, b)
                elif ar == 1:
                    a = self.children[0].evaluate(xvars, function_map, function_set)
                    return function_map[name](a)
                else:
                    raise RuntimeError('Unsupported arity')
            else:
                if isinstance(self.value, float) or isinstance(self.value, int):
                    return float(self.value)
                if isinstance(self.value, str) and self.value.startswith('x'):
                    idx = int(self.value[1:]) - 1
                    return float(xvars[idx])
                return 0.0
        except Exception:
            return 1e6

    def __str__(self):
        if isinstance(self.value, str) and self.children:
            if len(self.children) == 2:
                return f"({str(self.children[0])} {self.value} {str(self.children[1])})"
            else:
                return f"{self.value}({str(self.children[0])})"
        else:
            if isinstance(self.value, float):
                return f"{self.value:.4g}"
            return str(self.value)

def random_constant(constant_range):
    if constant_range is None:
        return None
    lo, hi = constant_range
    return random.uniform(lo, hi)


def random_terminal(var_count, constant_range):
    use_constant = constant_range is not None and random.random() < 0.5
    if use_constant:
        val = random_constant(constant_range)
        return Node(float(val))
    else:
        idx = random.randint(1, var_count)
        return Node(f'x{idx}')


def grow(depth, max_depth, function_list, function_set, var_count, constant_range):
    if depth >= max_depth:
        return random_terminal(var_count, constant_range)
    if random.random() < 0.5:
        name = random.choice(function_list)
        ar = function_set[name]
        children = [grow(depth+1, max_depth, function_list, function_set, var_count, constant_range) for _ in range(ar)]
        return Node(name, children)
    else:
        return random_terminal(var_count, constant_range)

def full(depth, max_depth, function_list, function_set, var_count, constant_range):
    if depth >= max_depth:
        return random_terminal(var_count, constant_range)
    name = random.choice(function_list)
    ar = function_set[name]
    children = [full(depth+1, max_depth, function_list, function_set, var_count, constant_range) for _ in range(ar)]
    return Node(name, children)

def make_tree(method, max_depth, function_list, function_set,var_count, constant_range):
    if method == 'grow':
        return grow(1, max_depth, function_list, function_set, var_count, constant_range)
    elif method == 'full':
        return full(1, max_depth, function_list, function_set, var_count, constant_range)

def ramped_half_and_half(pop_size, max_init_depth, function_list, function_set, var_count, constant_range):
    individuals = []
    depths = list(range(2, max_init_depth+1)) if max_init_depth >= 2 else [2]
    print("depths", depths)
    depth_count = len(depths)
    print("depth_count", depth_count)
    per_depth = pop_size // depth_count
    for d in depths:
        half = per_depth // 2
        for _ in range(half):
            individuals.append(make_tree('grow', d, function_list, function_set, var_count, constant_range))
        for _ in range(per_depth - half):
            individuals.append(make_tree('full', d, function_list, function_set, var_count, constant_range))
    while len(individuals) < pop_size:
        individuals.append(make_tree('grow', max_init_depth, function_list, function_set, var_count, constant_range))
    return individuals[:pop_size]

def mutate(tree, function_list, function_set, var_count,constant_range, max_depth, max_nodes):
    tcopy = tree.copy()
    nodes = tcopy.traverse()
    chosen = random.choice(nodes)

    def depth_from_root(root, target, current_depth=1):
        if root is target:
            return current_depth
        for child in root.children:
            res = depth_from_root(child, target, current_depth+1)
            if res is not None:
                return res
        return None
    chosen_depth = depth_from_root(tcopy, chosen)
    if chosen_depth is None:
        chosen_depth = 1
        
    max_subtree_depth = max_depth - (chosen_depth - 1)
    if max_subtree_depth < 1:
        return tree.copy()
    new_subtree_depth = random.randint(1, max_subtree_depth )
    new_subtree = make_tree(random.choice(['grow', 'full']), new_subtree_depth, function_list, function_set, var_count, constant_range)
    if tcopy is chosen:
        tcopy = new_subtree
    else:
        tcopy.replace_child(chosen, new_subtree)
    node_count, depth = count_nodes_and_depth(tcopy)
    if depth > max_depth or node_count > max_nodes:
        return tree.copy()
    return tcopy

def crossover(parent1, parent2, max_depth, max_nodes):
    p1 = parent1.copy()
    p2 = parent2.copy()
    nodes1 = p1.traverse()
    nodes2 = p2.traverse()
    n1 = random.choice(nodes1)
    n2 = random.choice(nodes2)

    def swap_subtrees(root, a, b):
        if root is a:
            return b.copy()
        new_root = Node(root.value, [])
        for child in root.children:
            new_root.children.append(swap_subtrees(child, a, b))
        return new_root

    child1 = swap_subtrees(p1, n1, n2)
    child2 = swap_subtrees(p2, n2, n1)
    for child in (child1, child2):
        count, depth = count_nodes_and_depth(child)
        if depth > max_depth or count > max_nodes:
            return parent1.copy(), parent2.copy()
    return child1, child2

def count_nodes_and_depth(tree):
    return tree.node_count(), tree.depth()

def tournament(population, fitnesses, k):
    chosen_indices = random.sample(range(len(population)), k)
    best = min(chosen_indices, key=lambda i: fitnesses[i])
    return population[best].copy()

class CostEvaluator:
    def __init__(self, xs, ys, function_map, function_set):
        self.xs = xs
        self.ys = ys
        self.function_map = function_map
        self.function_set = function_set
        self.evals = 0

    def mse(self, individual):
        self.evals += 1
        preds = []
        for row in self.xs:
            try:
                v = individual.evaluate(row, self.function_map, self.function_set)
                if not math.isfinite(v) or abs(v) > 1e12:
                    v = 1e6
            except Exception:
                v = 1e6
            preds.append(v)
        preds = np.array(preds, dtype=float)
        return float(np.mean((preds - self.ys) ** 2))

def run_gp(data_x, data_y, function_list, function_set, function_map, var_count, constant_range,
           pop_size, tournament_size, cost_limit, mutation_prob, reproduction_prob,
           max_tree_depth, max_nodes, max_init_depth, max_generations = 1000, stagnation_generations=None,):

    evaluator = CostEvaluator(data_x, data_y, function_map, function_set)

    pop = ramped_half_and_half(pop_size, max_init_depth, function_list, function_set, var_count, constant_range)
    fitnesses = [evaluator.mse(ind) for ind in pop]

    best_idx = int(np.argmin(fitnesses))
    best_ind = pop[best_idx].copy()
    best_cost = fitnesses[best_idx]
    print(f'Initial best cost: {best_cost:.6g}; expr: {best_ind}')

    generations = 0
    no_improve = 0
    history = []

    while evaluator.evals < cost_limit and generations < max_generations:
        generations += 1

        new_pop = [best_ind.copy()]

        while len(new_pop) < pop_size and evaluator.evals < cost_limit:
            op = random.random()
            if op < reproduction_prob:
                ind = tournament(pop, fitnesses, tournament_size)
                new_pop.append(ind)
            elif op < reproduction_prob + mutation_prob:
                parent = tournament(pop, fitnesses, tournament_size)
                child = mutate(parent, function_list, function_set, var_count, constant_range, max_tree_depth, max_nodes)
                new_pop.append(child)
            else:
                parent1 = tournament(pop, fitnesses, tournament_size)
                parent2 = tournament(pop, fitnesses, tournament_size)
                child1, child2 = crossover(parent1, parent2, max_tree_depth, max_nodes)
                new_pop.append(child1)
                if len(new_pop) < pop_size:
                    new_pop.append(child2)
        pop = new_pop[:pop_size]

        fitnesses = [evaluator.mse(ind) for ind in pop]
        curr_idx = int(np.argmin(fitnesses))
        curr_cost = fitnesses[curr_idx]
        curr_best = pop[curr_idx].copy()

        if curr_cost < best_cost:
            best_cost = curr_cost
            best_ind = curr_best.copy()
            print(f'New best (evals={evaluator.evals}): cost={best_cost:.6g}, expr={best_ind}')
            no_improve = 0
        else:
            no_improve += 1

        history.append((generations, evaluator.evals, best_cost, str(best_ind)))

        if stagnation_generations is not None and no_improve >= stagnation_generations:
            print(f'Stopping due to stagnation: {no_improve} generations without improvement')
            break

    print('Finished. Total evaluations:', evaluator.evals)
    print('Best cost:', best_cost)
    print('Best expression:', best_ind)
    return best_ind, best_cost

def build_function_map(selected_functions):
    base_map = {
        '+': (2, lambda a, b: a + b),
        '-': (2, lambda a, b: a - b),
        '*': (2, lambda a, b: a * b),
        '/': (2, lambda a, b: p_div(a, b)),
        'sin': (1, lambda a: math.sin(a)),
        'cos': (1, lambda a: math.cos(a)),
        'sqrt': (1, lambda a: p_sqrt(a)),
        'log': (1, lambda a: p_log10(a)),
        'exp': (1, lambda a: math.exp(a)),
    }
    function_set = {}
    function_map = {}
    for name in selected_functions:
        name = name.strip()
        if name in base_map:
            ar, func = base_map[name]
            function_set[name] = ar
            function_map[name] = func
    return function_set, function_map

def read_data(path):
    xs = []
    ys = []
    with open(path, 'r') as f:
        for line in f:
            if 'x' in line:
                continue
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            vals = [float(p) for p in parts if p != '']
            if len(vals) < 2:
                continue
            xs.append(vals[:-1])
            ys.append(vals[-1])
    return np.array(xs, dtype=float), np.array(ys, dtype=float)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--config', required=True)
    args = parser.parse_args()

    cfg = parse_config(args.config)

    func_line = cfg.get('FunctionNodes', '+, -, *, /, sin, cos, sqrt, log, exp')
    function_list = [s.strip() for s in func_line.split(',') if s.strip()]

    function_set, function_map = build_function_map(function_list)
    const_range_raw = cfg.get('ConstantRange', 'N/A')
    if const_range_raw.strip().upper() == 'N/A':
        constant_range = None
    else:
        parts = [p.strip() for p in const_range_raw.split(',')]
        constant_range = (float(parts[0]), float(parts[1]))

    pop_size = int(cfg.get('PopulationSize', '500'))
    tournament_size = int(cfg.get('TournamentSize', '3'))
    cost_evals_limit = int(cfg.get('CostEvaluations', '1000000'))
    mutation_prob = float(cfg.get('MutationProbability', '0.14'))
    reproduction_prob = float(cfg.get('ReproductionProbability', '0.01'))
    max_tree_depth = int(cfg.get('MaxTreeDepth', '7'))
    max_init_depth = int(cfg.get('MaxInitDepth', str(max_tree_depth)))
    max_nodes = int(cfg.get('MaxNodes', '200'))
    max_generations = int(cfg.get('MaxGenerations', '10000'))
    stagnation = cfg.get('StagnationGenerations', None)
    stagnation_generations = int(stagnation) if stagnation is not None else None
    xs, ys = read_data(args.data)
    var_count = xs.shape[1]

    best, best_cost = run_gp(xs, ys, list(function_set.keys()), function_set, function_map, var_count, 
                            constant_range, pop_size, tournament_size, cost_evals_limit, mutation_prob, reproduction_prob,
                            max_tree_depth, max_nodes, max_init_depth, max_generations, stagnation_generations)

if __name__ == '__main__':
    main()