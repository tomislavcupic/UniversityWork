# AGENTS.md - Neural Networks Laboratory 2

## Commands
- **Run notebook**: Open lab2.ipynb in Jupyter Notebook or VS Code with Jupyter extension
- **Execute cells**: Run cells individually in Jupyter environment (no global test/build commands)

## Architecture
- **Type**: Educational Jupyter notebook for neural networks course
- **Structure**: Single notebook (lab2.ipynb) with exercises on perceptron algorithms and stock price prediction
- **Data**: stock.txt contains stock price time series data (comma-separated values)
- **Topics**: Perceptron classification (2D/3D), XOR problem, Gaussian distribution, LMS algorithm

## Code Style
- **Language**: Python 3 with NumPy and Matplotlib
- **Imports**: Use `import numpy as np` and `import matplotlib.pyplot as plt`
- **Arrays**: Use NumPy arrays with `.T` for transpose operations
- **Functions**: Define helper functions (initp, predict, trainlms, trainlms_p, plot, memory, memorize)
- **Naming**: Snake_case for variables/functions (e.g., matrix_A, max_num_iter, err_nn)
- **Comments**: Minimal; code should be self-explanatory with markdown cells for explanations
- **Parameters**: Use descriptive names (ni for learning rate, W for weights, A for data matrix, C for classes)
