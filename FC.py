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
                        premises = [Proposition(p.strip()) for p in implication_parts[0].split('&')]
                        conclusion = Proposition(implication_parts[1].strip())
                        knowledge_base.append(Implication(premises, conclusion))
                        for p in premises:
                            if p.symbol not in propositions:
                                propositions[p.symbol] = p
                        if conclusion.symbol not in propositions:
                            propositions[conclusion.symbol] = conclusion
                    else:
                        symbol = part.strip()
                        if symbol not in propositions:
                            propositions[symbol] = Proposition(symbol)
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
    file_path = sys.argv[1]  # Change this to your input file path
    knowledge_base, query_prop, propositions = parse_input_file(file_path)

    # Assume initial facts are true
    for prop in propositions.values():
        if prop.symbol.islower():
            prop.truth_value = True

    # Perform forward chaining
    inferred = forward_chain(knowledge_base, propositions)

    print("Knowledge Base:")
    for implication in knowledge_base:
        print(implication)

    print("\nIndividual Propositions:")
    for prop in propositions.values():
        print(f"{prop.symbol}: {'True' if prop.truth_value else 'False'}")

    print("\nQuery:")
    print(query_prop.symbol)

    print("\nEntailment Result:")
    if query_prop.symbol in inferred:
        print("The query is entailed by the knowledge base.")
    else:
        print("The query is not entailed by the knowledge base.")

if __name__ == "__main__":
    main()
