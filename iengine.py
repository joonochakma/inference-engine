import sys

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

def parse_kb(content):
    kb = []
    for line in content:
        line = line.strip()
        if line == "TELL":
            continue
        elif line == "ASK":
            break
        else:
            clauses = line.split(';')
            kb.extend(clauses)
    return kb

def get_propositions(kb):
    props = set()
    for clause in kb:
        symbols = clause.split('=>')
        for symbol in symbols:
            props.update(symbol.strip().split('&'))
    props.discard('')  # Remove the empty string from the set of proposition symbols
    return sorted(props)

def generate_truth_table(props):
    n = len(props)
    truth_table = []
    for i in range(2 ** n):
        row = [(i >> j) & 1 for j in range(n)]
        truth_table.append(row)
    return truth_table

if __name__ == "__main__":
    # Check if the filename is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python script.py filename")
        sys.exit(1)

    filename = sys.argv[1]
    content = read_file(filename)
    if content:
        kb = parse_kb(content)
        props = get_propositions(kb)
        truth_table = generate_truth_table(props)
        print("Proposition symbols:", props)
        print("Truth table:")
        for row in truth_table:
            print(row)
