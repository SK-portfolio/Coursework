import random

def generate_addition_data(max_operand):
    samples = []
    for a in range(max_operand + 1):
        for b in range(max_operand + 1):
            samples.append(f"{a}+{b}={a+b}")
    return samples

def generate_subtraction_data(max_operand):
    samples = []
    for a in range(max_operand + 1):
        for b in range(a + 1):  #non-negative answers only (a - b >= 0)
            samples.append(f"{a}-{b}={a-b}")
    return samples

def generate_multiplication_data(max_operand):
    samples = []
    for a in range(max_operand + 1):
        for b in range(max_operand + 1):
            samples.append(f"{a}*{b}={a*b}")
    return samples

def generate_division_data(max_operand):
    samples = []
    for b in range(1, max_operand + 1):
        for a in range(b, max_operand + 1):
            if a % b == 0:      #exact integer division only
                samples.append(f"{a}/{b}={a//b}")
    return samples

def write_dataset(filename, data):
    random.shuffle(data)
    with open(filename, "w") as f:
        for line in data:
            f.write(line + "\n")
    print(f"{filename}: {len(data)} samples")

#equal amount of samples from each operation (for combined dataset)
def balance_dataset(datasets, samples_per_op):
    balanced = []
    for data in datasets:
        random.shuffle(data)
        balanced.extend(data[:samples_per_op])
    return balanced

def generate_math_datasets():
    # addition dataset
    addition_data = (
        generate_addition_data(max_operand=9) +
        generate_addition_data(max_operand=99)
    )
    write_dataset("input_addition.txt", addition_data)

    # subtraction dataset
    subtraction_data = generate_subtraction_data(max_operand=99)
    write_dataset("input_subtraction.txt", subtraction_data)

    # multiplication dataset
    multiplication_data = generate_multiplication_data(max_operand=19)
    write_dataset("input_multiplication.txt", multiplication_data)

    # division dataset
    division_data = generate_division_data(max_operand=99)
    write_dataset("input_division.txt", division_data)

    # all operations combined
    all_ops = balance_dataset(
        [addition_data, subtraction_data, multiplication_data, division_data],
        samples_per_op=2000
    )
    write_dataset("input_all_ops.txt", all_ops)


if __name__ == "__main__":
    generate_math_datasets()

