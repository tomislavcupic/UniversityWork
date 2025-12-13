# Selected Optimization Methods and Algorithms - Function Optimizer

This is an interactive GUI application built for class Selected Optimization Methods and Algorithms, or "OOMA" shortened. You can start it by running the project.py file. It enables users to select optimization algorithms and test functions, then visualize their performance on a 2D contour plot and a 3D surface. It's ideal for students and instructors studying numerical optimization.

---

## File Structure
> * `project.py`: The main entry point for the application, when ran it shows the GUI interface.
> * `README.md`: This file, providing an overview of the project.
> * `algorithms/`: Contains the implementation of various optimization algorithms.
> * `functions/`: Contains the implementation of various test functions and their gradients, hessians, plot_functions.

---

## Supported algorithms
   * Nelder-Mead
   * Newton
   * BFGS (Quasi-Newton)
   * Gradient Descent
   * Simulated Annealing

---

## Test functions
   * Bohachevsky function with minimum at (0,0)
   * Sum Squares function with minimum at (0,0)

---

## Features
   * Gradient and Hessian based optimizers
   * Newton's method with pseudo-inverse fallback
   * Wolfe condition line search

---

## Requirements
   ``bash
   pip install numpy matplotlib plotly