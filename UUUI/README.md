# Introduction to AI Exercises

##### Here are my laboratory exercises from class "Introduction to Artificial Intelligence" or in croatian "Uvod u umjetnu inteligenciju" (UUUI) There are three tasks, each in its folder, and inside every folder exists a pdf version of the instructions for the task in croatian. Below is each exercise in details.
---

## 🧭  Exercise 1: Search Algorithms (search_algorithms.py)

### This script implements three classic graph search algorithms:

* ###### Breadth-First Search (BFS)
* ###### Uniform Cost Search (UCS)
* ###### A* Search

---
### Features:

Parses state-space description files with initial, goal, and state transitions. For A*, supports external heuristic files. Tracks number of visited states, total path cost, and the solution path. Optional checks for heuristic optimism and consistency are stubbed.

---
### Usage:

```bash
python search_algorithms.py --alg <bfs|ucs|astar> --ss <state_file> [--h <heuristic_file>] [--check-optimistic] [--check-consistent]
```

Example Output:
A-STAR heuristics.txt:
```bash
[STATES_VISITED]: 7
[PATH_LENGTH]: 4
[TOTAL_COST]: 11.2
[PATH]: A => B => C => G`
```

## 🧠 Exercise 2: Propositional Logic Resolution (resolution.py)

This script uses the resolution method to determine if a given conclusion follows logically from a set of propositional clauses.

---
### Features:

Input file consists of clauses in CNF (disjunctions separated by space).

Last clause is treated as a query and negated for proof by contradiction.

Performs pairwise resolution until either NIL (proof found) or no new clauses can be generated.

---
### Usage:
```bash
python resolution.py resolution <clauses_file>
```

---
### Example Output:
```bash
1 p q
2 ~p r
3 ~q ~r
4 ~p ~q
5 r
6 ~r
NIL
[CONCLUSION]: p is true
```

## 🌳 Exercise 3: Decision Tree with ID3 Algorithm (decision_tree.py)

This script implements the ID3 algorithm to train a decision tree classifier from labeled data and evaluate its performance.

### Features:

Supports custom tree depth limits.

### Outputs:

Decision tree structure
Predictions on the test set
Accuracy score
Confusion matrix

### Usage:
```bash
python decision_tree.py <training_data.csv> <testing_data.csv> [optional_depth]
```

Example Output:
```bash
[BRANCHES]:
1:feature1=A 2:feature2=X class1
1:feature1=A 2:feature2=Y class2
...

[PREDICTIONS]: class1 class2 class1 ...
[ACCURACY]: 0.92308
[CONFUSION_MATRIX]:
13 1
0 12
```

## ⚙️ Requirements

Python 3.x
No external dependencies required (uses only standard libraries)