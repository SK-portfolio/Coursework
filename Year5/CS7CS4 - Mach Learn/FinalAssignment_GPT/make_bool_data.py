import random
import itertools

BOOLS = ["True", "False"]
BIN_OPS = ["AND", "OR", "XOR"]

def eval_expr(expr):
    #remove parentheses + split each token in expression
    tokens = expr.replace("(", "").replace(")", "").split()
        #convert string to boolean
    def to_bool(x):
        return x == "True"
        # if single NOT operation
    if tokens[0] == "NOT":
        return not to_bool(tokens[1])   #move past NOT and evaluate the boolean value

    values = []
    ops = []
    
    #parse tokens
    for t in tokens:
        if t in {"True", "False"}:
            values.append(to_bool(t))
        elif t in {"AND", "OR", "XOR"}:
            ops.append(t)

    result = values[0]
    #evaluate binary operations left to right
    for i, op in enumerate(ops):
        if op == "AND":
            result = result and values[i + 1]
        elif op == "OR":
            result = result or values[i + 1]
        elif op == "XOR":
            result = (result != values[i + 1])

    return result

def generate_unary():
    samples = []
    for b in BOOLS:
        expr = f"NOT {b}"
        samples.append(f"{expr}={eval_expr(expr)}")
    return samples

def generate_binary():
    samples = []
    for a, b, op in itertools.product(BOOLS, BOOLS, BIN_OPS):
        expr = f"{a} {op} {b}"
        samples.append(f"{expr}={eval_expr(expr)}")
    return samples

def generate_nested():
    samples = []
    for a, b, c, op1, op2 in itertools.product(BOOLS, BOOLS, BOOLS, BIN_OPS, BIN_OPS):
        expr = f"({a} {op1} {b}) {op2} {c}"
        samples.append(f"{expr}={eval_expr(expr)}")
    return samples

def write_dataset(filename, data):
    random.shuffle(data)
    with open(filename, "w") as f:
        for line in data:
            f.write(line + "\n")
    print(f"{filename}: {len(data)} samples")

def generate_boolean_datasets():
    simple = generate_unary() + generate_binary()
    nested = generate_nested()

    write_dataset("input_bool_simple.txt", simple)
    write_dataset("input_bool_nested.txt", nested)
    write_dataset("input_bool_all.txt", simple + nested)

if __name__ == "__main__":
    generate_boolean_datasets()
