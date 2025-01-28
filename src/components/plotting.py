import numpy as np
import matplotlib.pyplot as plt
from utils.parser import validate_parameters, is_valid_function_type

def plot_function(func_type, params):
    valid_func, func_error = is_valid_function_type(func_type)
    if not valid_func:
        raise ValueError(func_error)
        
    valid_params, param_error = validate_parameters(params)
    if not valid_params:
        raise ValueError(param_error)
    
    fig, ax = plt.subplots()
    x_min, x_max = float(params['x_min']), float(params['x_max'])
    x = np.linspace(x_min, x_max, 1000)
    
    try:
        function_map = {
            'linear': lambda x: x,
            'quadratic': lambda x: x**2,
            'sine': lambda x, k=1: np.sin(k*x),
            'cosine': lambda x, k=1: np.cos(k*x),
        }
        
        if func_type in function_map:
            if func_type in ['sine', 'cosine']:
                k = float(params.get('k', 1))
                y = function_map[func_type](x, k)
            else:
                y = function_map[func_type](x)
        elif func_type == 'polynomial':
            coeffs = params.get('coefficients', [1, 0])
            y = np.polyval(coeffs, x)
            
        ax.plot(x, y)
        ax.grid(True)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        ax.set_title(f"{func_type.capitalize()} Function")
        
        return fig
        
    except Exception as e:
        raise ValueError(f"Error plotting function: {str(e)}")