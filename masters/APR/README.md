# Computer Aided Analysis and Design – Python Projects

This repository contains five structured Python exercises developed for the **Computer Aided Analysis and Design** course. The goal is to implement mathematical methods for optimization and differential equation solving using a custom-built matrix class.

All numerical methods are implemented manually without using external numerical libraries like NumPy for core operations, except where explicitly needed for efficiency or plotting.

---

## Project Overview

### Exercise 1: `matrica.py` – Custom Matrix Class

This module implements a lightweight matrix class (`Matrica`) to support operations like:

- Matrix addition, subtraction, multiplication (scalar/matrix)
- Transposition
- LU decomposition
- Forward/backward substitution
- Basic indexing and data handling

This class serves as the backbone for all subsequent exercises.
Also in first exercise we had to test all those operations which is located in (`Prvi.py`)

---

### Exercise 2: `optimization_methods.py` – Unconstrained Optimization

This exercise focuses on **unimodal optimization** and **derivative-free methods**.

#### Implemented Methods:

- **Unimodal Interval Estimation**: Brackets the minimum using iterative interval expansion.
- **Golden Section Search**: Minimizes a unimodal function using the golden ratio.
- **Coordinate Search**: Optimizes along one axis at a time.
- **Hooke–Jeeves Algorithm**: Pattern search that alternates between exploratory and pattern moves.
- **Nelder–Mead Simplex**: A heuristic method that operates on simplices in multidimensional space.

These algorithms are useful for optimizing black-box functions where derivatives are not available or unreliable.

---

### Exercise 3: `gradient_methods.py` – Gradient-Based Optimization

This task focuses on **gradient-based optimization** for multivariable functions.

#### Implemented Methods:

- **Gradient Descent**: Uses the negative gradient direction for minimization.
- **Newton–Raphson**: Utilizes second-order derivatives (Hessian) for faster convergence.
- **Gauss–Newton**: Specialized for least-squares problems where the function can be written as a sum of squares.

Symbolic or numerical gradient and Hessian calculations are included as needed.

---

### Exercise 4: `box_algorithm.py` – Constrained Optimization (Box Method)

This exercise implements the **Box (complex) algorithm**, a method for constrained optimization.

#### Features:

- Supports explicit **bounds** and **nonlinear constraints**
- Generates and evolves a population of points inside the feasible region
- Performs reflection and centroid-based adjustment to converge to an optimal point

Suitable for black-box objective functions with simple constraints.

---

### Exercise 5: `differential_solvers.py` – Solving ODEs

The final exercise solves **systems of ordinary differential equations (ODEs)** using **single-step** and **predictor-corrector** methods.

#### Implemented Methods:

- **Euler’s Method**
- **Backward Euler (Implicit)**
- **Trapezoidal Rule**
- **Runge–Kutta 4th Order (RK4)**
- **PECE Methods (Predict-Evaluate-Correct-Evaluate)**:
  - PECE Euler–Trapezoidal
  - PECE Euler–Backward Euler

---

## Requirements

- Python 3.x
- `numpy` (for analytical checks and helper functions)

> All matrix operations for the core logic are handled by the custom `Matrica` class.