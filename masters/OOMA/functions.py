import numpy as np
import plotly.graph_objects as go

def bohachevsky_function(x):
   #minimum at (0, 0) with value 0
   return x[0]**2 + 2 * x[1]**2 - 0.3 * np.cos(3 * np.pi * x[0]) - 0.4 * np.cos(4 * np.pi * x[1]) + 0.7

def bohachevsky_grad(x):
   dx = 2 * x[0] + 0.9 * np.pi * np.sin(3 * np.pi * x[0])
   dy = 4 * x[1] + 1.6 * np.pi * np.sin(4 * np.pi * x[1])
   return np.array([dx, dy])

def bohachevsky_hessian(x, damping=1e-2):
   d2x = 2 + 2.7 * (np.pi**2) * np.cos(3 * np.pi * x[0])
   d2y = 4 + 6.4 * (np.pi**2) * np.cos(4 * np.pi * x[1])
   hessian = np.array([
      [d2x, 0],
      [0, d2y]
   ])
   hessian += np.eye(2) * damping 
   return hessian

def sum_squares_function(x):
   return sum((i + 1) * x[i]**2 for i in range(len(x)))

def sum_squares_grad(x):
   return np.array([(i + 1) * 2 * x[i] for i in range(len(x))])

def sum_squares_hessian(x, damping=1e-2):
   n = len(x)
   hessian = np.zeros((n, n))
   for i in range(n):
      hessian[i, i] = 2 * (i + 1) 
   hessian += np.eye(n) * damping 
   return hessian

def plot_bohachevsky_function():
   x1 = np.linspace(-2, 2, 100)
   x2 = np.linspace(-2, 2, 100)
   X1, X2 = np.meshgrid(x1, x2)

   Z_bohachevsky = np.array([[bohachevsky_function(np.array([x, y])) for x in x1] for y in x2])
   fig_bohachevsky = go.Figure(data=[go.Surface(z=Z_bohachevsky, x=X1, y=X2, colorscale='Jet')])
   fig_bohachevsky.update_layout(
      title='Bohachevsky Function (Interactive)',
      scene=dict(
         xaxis_title='x1',
         yaxis_title='x2',
         zaxis_title='f(x1, x2)'
      ),
      autosize=True,
      margin=dict(l=50, r=50, t=50, b=50)
   )
   fig_bohachevsky.show(renderer="browser")

def plot_sum_squares_function():
   x1 = np.linspace(-100, 100, 100)
   x2 = np.linspace(-100, 100, 100)
   X1, X2 = np.meshgrid(x1, x2)

   Z_sum_squares = np.array([[sum_squares_function(np.array([x, y])) for x in x1] for y in x2])
   fig_sum_squares = go.Figure(data=[go.Surface(z=Z_sum_squares, x=X1, y=X2, colorscale='Jet')])
   fig_sum_squares.update_layout(
      title='Sum Squares Function (Interactive)',
      scene=dict(
         xaxis_title='x1',
         yaxis_title='x2',
         zaxis_title='f(x1, x2)'
      ),
      autosize=True,
      margin=dict(l=50, r=50, t=50, b=50)
   )
   fig_sum_squares.show(renderer="browser")