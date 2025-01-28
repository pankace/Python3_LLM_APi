import os
import openai

def parse_user_input(user_message):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    system_prompt = """You are a mathematical function parser. Your task is to extract function information from user messages.

OUTPUT FORMAT:
- For functions: Return a Python tuple with (function_type, parameters_dict)
- For exit messages: Return exactly the string "exit"

SUPPORTED FUNCTIONS:
- linear: y = x
- quadratic: y = x²
- sine: y = sin(kx)
- cosine: y = cos(kx)
- polynomial: up to degree 4

PARAMETERS:
- x_min, x_max: required for all functions
- k: multiplier for sine/cosine
- coefficients: list for polynomials

EXAMPLES:
User: "Plot sine from -5 to 5"
Return: ("sine", {"x_min": -5, "x_max": 5, "k": 1})

User: "Show me x squared from 0 to 10"
Return: ("quadratic", {"x_min": 0, "x_max": 10})

User: "Can you plot sin(3x) between -2 and 2"
Return: ("sine", {"x_min": -2, "x_max": 2, "k": 3})

User: "Plot x^3 - 2x^2 + x - 1 from -5 to 5"
Return: ("polynomial", {"x_min": -5, "x_max": 5, "coefficients": [1, -2, 1, -1]})

User: "Goodbye" or "That's all" or "Exit"
Return: "exit"

If you cannot parse the input, return None."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1  # Lower temperature for more consistent outputs
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.lower() == "exit" or result.lower() == '"exit"':
            return "exit"
            
        if result.lower() == "none":
            return None
            
        try:
            return eval(result)
        except:
            return None
            
    except Exception as e:
        print(f"Error in parse_user_input: {e}")
        return None
    
def validate_parameters(params):
    """
    Validate plotting parameters
    Returns: (bool, str) - (is_valid, error_message)
    """
    if not isinstance(params, dict):
        return False, "Parameters must be a dictionary"
    
    required = ['x_min', 'x_max']
    missing = [param for param in required if param not in params]
    
    if missing:
        return False, f"Missing required parameters: {', '.join(missing)}"
        
    try:
        x_min = float(params['x_min'])
        x_max = float(params['x_max'])
        
        if x_min >= x_max:
            return False, "x_min must be less than x_max"
            
        if abs(x_max - x_min) > 1000:
            return False, "Interval too large"
            
    except ValueError:
        return False, "x_min and x_max must be numbers"
        
    return True, ""

def is_valid_function_type(func_type):
    """
    Check if function type is supported
    Returns: (bool, str) - (is_valid, error_message)
    """
    valid_types = ['linear', 'quadratic', 'sine', 'cosine', 'polynomial']
    
    if not isinstance(func_type, str):
        return False, "Function type must be a string"
        
    if func_type not in valid_types:
        return False, f"Unknown function type. Supported types: {', '.join(valid_types)}"
        
    return True, ""

