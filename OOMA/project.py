from functions import *
from algorithms import *
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import plotly.graph_objects as go


# GUI
class OptimizerApp:
   def __init__(self, root):
      self.root = root
      self.root.title("Function Optimizer")
      self.root.geometry("400x250")

      ttk.Label(root, text="Select Function:").pack(pady=5)
      self.function_choice = ttk.Combobox(root, values=["Bohachevsky", "Sum Squares"])
      self.function_choice.pack()

      ttk.Label(root, text="Select Optimization Algorithm:").pack(pady=5)
      self.algorithm_choice = ttk.Combobox(root, values=["Simulated Annealing", "BFGS", "Gradient Descent Unconstrained", "Nelder-Mead", "Newton's Method"])
      self.algorithm_choice.pack()

      ttk.Button(root, text="Run Optimization", command=self.run_optimization).pack(pady=20)

      ttk.Button(root, text="Plot Function", command=self.plot_selected_function).pack()

   def run_optimization(self):
      func_name = self.function_choice.get()
      algo = self.algorithm_choice.get()

      if not func_name or not algo:
         messagebox.showerror("Error", "Please select both function and algorithm.")
         return

      func = bohachevsky_function if func_name == "Bohachevsky" else sum_squares_function
      
      if algo == "BFGS":
         # za x0 [2, -4] za Bohachevsky optimizira
         sol, val, hist = bfgs(func, grad_func=bohachevsky_grad if func_name == "Bohachevsky" else sum_squares_grad, x0=[4, -4] if func_name == "Bohachevsky" else [5, 5])
         bfgs_plot_optimization_path(func, hist) 

      elif algo == "Simulated Annealing":
         sol, val, hist = simulated_annealing(func, x0=[5, 5] if func_name == "Bohachevsky" else [5, 5])
         simulated_annealing_plot_optimization_path(func, hist)

      elif algo == "Gradient Descent Unconstrained":
         sol, val, hist = gradient_descent_unconstrained(func, grad_func=bohachevsky_grad if func_name == "Bohachevsky" else sum_squares_grad, x0=[3, 3] if func_name == "Bohachevsky" else [5, 5])
         grad_plot_optimization_path(func, hist) 

      elif algo == "Nelder-Mead":
         sol, val, hist = nelder_mead(func, x0=[3, 3] if func_name == "Bohachevsky" else [5, 5])
         nelder_mead_plot_optimization_path(func, hist)

      elif algo == "Newton's Method":
         #inicijalni vektor za Newtonovu metodu
         if func_name == "Bohachevsky":
            sol, val, hist = newtons_method_with_lm(func, bohachevsky_grad, bohachevsky_hessian, np.array([3, 3]))
         elif func_name == "Sum Squares":
            #x0 = np.array([512, 404.2319])  # Starting point near the known minimum
            x0 = np.array([5, 5])  # Bad initial point for Eggholder
            sol, val, hist = newtons_method_with_lm(func, sum_squares_grad, sum_squares_hessian, x0)
         newton_plot_optimization_path(func, hist)
      else:
         return

      messagebox.showinfo("Optimization Result", f"Solution: {sol}\nFunction Value: {val:.4f}")

   def plot_selected_function(self):
      func_name = self.function_choice.get()
      if not func_name:
         messagebox.showerror("Error", "Please select a function.")
         return
      if func_name == "Bohachevsky":
         plot_bohachevsky_function()
      else:
         plot_sum_squares_function()

if __name__ == "__main__":
   root = tk.Tk()
   app = OptimizerApp(root)
   root.mainloop()