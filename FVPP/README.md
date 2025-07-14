# Formal software verification

This laboratory exercise is from a class called FVPP - "Formalna verifikacija programske potpore", or in english: "Formal software verification". It is a simple yet effective SAT solver implemented in Python, based on the **Davis–Putnam–Logemann–Loveland (DPLL)** algorithm. The solver reads Boolean formulas in **DIMACS CNF format** and determines their satisfiability using classical techniques enhanced with preprocessing. 

#### The instructions for the task are in the instructions.pdf file.

## What is SAT?

The **Boolean Satisfiability Problem (SAT)** asks whether there exists an assignment of truth values to variables that makes a given Boolean formula evaluate to true. It is the first problem proven to be NP-complete and forms the foundation of many areas in computer science like automated reasoning, model checking, and AI planning.

---

## Features

- **DPLL Algorithm Core**
  - Recursive backtracking search with unit propagation and pure literal elimination.
- **Preprocessing Optimizations**
- **Hidden Literal Elimination**
- **Tautology Removal**
- **Clause Subsumption** (removal of supersets)
- **Literal Equivalence Propagation**
- **DIMACS CNF File Parsing**
- **Result Output**
- **Outputs variable assignments to a `.txt` file**
- **Execution Time Logging**

---
## How It Works

### **Parsing CNF File**

The program reads a `.cnf` file formatted according to the [DIMACS CNF standard](https://www.satcompetition.org/2009/format-benchmarks2009.html).

### Output

Results are printed in the terminal and saved to `<filename>.txt`.

---
## TODO
   * fix the function "hidden_literal_elimination"
   * add one more feature