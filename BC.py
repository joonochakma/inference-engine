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
                        # Add proposition with initial support to knowledge base
                        knowledge_base.append(Implication([], propositions[symbol]))
            elif line and mode == 'ASK':
                query = Proposition(line.strip())
                if query.symbol not in propositions:
                    propositions[query.symbol] = query

    return knowledge_base, query, propositions

def backward_chain(knowledge_base, query_prop):
    inferred = []

    def backward_chain_helper(symbol):
        print("Checking symbol:", symbol)  # Debug print
        if symbol in inferred:
            print("Symbol already inferred:", symbol)  # Debug print
            return True
        inferred.append(symbol)
        for implication in knowledge_base:
            if implication.conclusion.symbol == symbol:
                print("Checking implication:", implication)  # Debug print
                if all(backward_chain_helper(p.symbol) for p in implication.premises):
                    print("All premises of", implication, "are inferred")  # Debug print
                    return True
        print("No support found for symbol:", symbol)  # Debug print
        return False

    result = backward_chain_helper(query_prop.symbol)
    return result, inferred[::-1]

def main():
    file_path = sys.argv[1]  # Change this to your input file path
    knowledge_base, query_prop, propositions = parse_input_file(file_path)

    print("Knowledge Base:")  # Debug print
    for implication in knowledge_base:  # Debug print
        print(implication)  # Debug print
    print("Query:", query_prop)  # Debug print

    # Perform backward chaining
    result, inferred = backward_chain(knowledge_base, query_prop)

    print("Entailment Result:")
    if result:
        print(f"YES: {', '.join(inferred)}")
    else:
        print("NO")

if __name__ == "__main__":
    main()
