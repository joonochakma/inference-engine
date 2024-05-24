import sys

class Proposition:
    def __init__(self, symbol):
        self.symbol = symbol
        self.truth_value = False

    def evaluate(self):
        return self.truth_value

    def __str__(self):
        return self.symbol

class Implication:
    def __init__(self, premises, conclusion):
        self.premises = premises
        self.conclusion = conclusion

    def __str__(self):
        premises_str = ' & '.join(str(p) for p in self.premises)
        return f"{premises_str} => {self.conclusion}"

def parse_input_file(file_path):
    knowledge_base = []
    query = None
    propositions = {}

    with open(file_path, 'r') as file:
        mode = None  # TELL or ASK
        for line in file:
            line = line.strip()
            if line == 'TELL':
                mode = 'TELL'
            elif line == 'ASK':
                mode = 'ASK'
            elif line and mode == 'TELL':
                parts = line.split(';')
                for part in parts:
                    if '=>' in part:
                        implication_parts = part.split('=>')
                        premises = [propositions.setdefault(p.strip(), Proposition(p.strip())) for p in implication_parts[0].split('&')]
                        conclusion = propositions.setdefault(implication_parts[1].strip(), Proposition(implication_parts[1].strip()))
                        knowledge_base.append(Implication(premises, conclusion))
                    else:
                        symbol = part.strip()
                        if symbol not in propositions:
                            propositions[symbol] = Proposition(symbol)
                        propositions[symbol].truth_value = True  # Initial facts are true
            elif line and mode == 'ASK':
                query = Proposition(line.strip())
                if query.symbol not in propositions:
                    propositions[query.symbol] = query

    return knowledge_base, query, propositions

def forward_chain(knowledge_base, propositions):
    inferred = set()
    agenda = [prop for prop in propositions.values() if prop.truth_value]

    while agenda:
        p = agenda.pop(0)
        if p.symbol in inferred:
            continue
        inferred.add(p.symbol)

        for implication in knowledge_base:
            if p in implication.premises:
                implication.premises.remove(p)
                if not implication.premises:
                    implication.conclusion.truth_value = True
                    agenda.append(implication.conclusion)
    
    return inferred

def main():
    if len(sys.argv) != 2:
        print("Usage: python FC.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    knowledge_base, query_prop, propositions = parse_input_file(file_path)

    # Perform forward chaining
    inferred = forward_chain(knowledge_base, propositions)

    if query_prop.symbol in inferred:
        print(f"YES: {', '.join(sorted(inferred))}")
    else:
        print("NO")

if __name__ == "__main__":
    main()
