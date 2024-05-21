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

def backward_chain(query, knowledge_base, inferred=None):
    if inferred is None:
        inferred = set()

    if query.symbol in inferred:
        return True

    if query.evaluate():
        return True

    for implication in knowledge_base:
        if implication.conclusion.symbol == query.symbol:
            all_premises_true = True
            for premise in implication.premises:
                if not backward_chain(premise, knowledge_base, inferred):
                    all_premises_true = False
                    break
            if all_premises_true:
                query.truth_value = True
                inferred.add(query.symbol)
                return True

    return False

def main():
    file_path = sys.argv[1]  # Change this to your input file path
    knowledge_base, query_prop, propositions = parse_input_file(file_path)

    # Perform backward chaining
    inferred = set()
    entails = backward_chain(query_prop, knowledge_base, inferred)

    print("Knowledge Base:")
    for implication in knowledge_base:
        print(implication)

    print("\nIndividual Propositions:")
    for prop in propositions.values():
        print(f"{prop.symbol}: {'True' if prop.truth_value else 'False'}")

    print("\nQuery:")
    print(query_prop.symbol)

    print("\nEntailment Result:")
    if entails:
        print(f"YES: {', '.join(sorted(inferred))}")
    else:
        print("NO")

if __name__ == "__main__":
    main()
