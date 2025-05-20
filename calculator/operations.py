import math

# --- Operation implementations ---

def op_plus(args):
    return args[0] + args[1]

def op_minus(args):
    return args[0] - args[1]

def op_times(args):
    return args[0] * args[1]

def op_divide(args):
    if args[1] == 0:
        raise ValueError("Error while performing operation Divide: division by 0")
    return args[0] // args[1]

def op_pow(args):
    return args[0] ** args[1]

def op_abs(args):
    return abs(args[0])

def op_fact(args):
    if args[0] < 0:
        raise ValueError("Error while performing operation Factorial: not supported for the negative number")
    return math.factorial(args[0])

# --- Operation registry ---

OPERATIONS = {
    "plus": (op_plus, 2),
    "minus": (op_minus, 2),
    "times": (op_times, 2),
    "divide": (op_divide, 2),
    "pow": (op_pow, 2),
    "abs": (op_abs, 1),
    "fact": (op_fact, 1),
}

# --- Dispatcher ---

def perform_operation(op_name, args):
    op_name = op_name.lower()

    if op_name not in OPERATIONS:
        raise ValueError(f"Error: unknown operation: {op_name}")

    func, expected_args = OPERATIONS[op_name]

    if len(args) < expected_args:
        raise ValueError(f"Error: Not enough arguments to perform the operation {op_name}")
    elif len(args) > expected_args:
        raise ValueError(f"Error: Too many arguments to perform the operation {op_name}")

    return func(args)
