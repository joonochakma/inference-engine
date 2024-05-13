import sys


class Proposition:
    def __init__(self, symbol):
        self.symbol = symbol
        self.truth_value = None

    def evaluate(self, truth_values):
        index = proposition_indices[self.symbol]
        return truth_values[index]

class Implication:
    def __init__(self, premises, conclusion):
        self.premises = premises
        self.conclusion = conclusion
        self.truth_value = None

def generate_proposition_indices(propositions):
    all_propositions = sorted(propositions)
    return {symbol: index for index, symbol in enumerate(all_propositions)}

def generate_truth_table(proposition_indices):
    num_propositions = len(proposition_indices)
    num_rows = 2 ** num_propositions
    truth_table = []

    for i in range(num_rows):
        truth_values = [(i >> j) & 1 == 1 for j in range(num_propositions)]
        truth_table.append(truth_values)

    return truth_table

def evaluate_knowledge_base(knowledge_base, truth_table):
    for implication in knowledge_base:
        premises_truth_values = [prop.truth_value for prop in implication.premises]
        conclusion_truth_value = implication.conclusion.evaluate(truth_table[-1])
        implication.truth_value = all(premises_truth_values) and not conclusion_truth_value

def check_entailment(query, knowledge_base, truth_table):
    query_symbol = query.conclusion.symbol
    for row in truth_table:
        if row[proposition_indices[query_symbol]]:
            # Check if all premises of implications are true whenever the conclusion is true
            all_premises_true = all(
                all(row[proposition_indices[prop.symbol]] for prop in implication.premises)
                for implication in knowledge_base if implication.conclusion.symbol == query_symbol
            )
            if all_premises_true:
                # Check if the query is not a premise of any implication
                if not any(query_symbol == prop.symbol for implication in knowledge_base 
                           for prop in implication.premises):
                    return True
    return False

def parse_input_file(file_path):
    knowledge_base = []
    query = None
    propositions = set()

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
                            propositions.add(p.symbol)
                        propositions.add(conclusion.symbol)
                    else:
                        propositions.add(part.strip())
            elif line and mode == 'ASK':
                query = Proposition(line.strip())

    return knowledge_base, query, propositions





def main():
    file_path = sys.argv[1]  # Change this to your input file path
    knowledge_base, query_prop, propositions = parse_input_file(file_path)

    # Create a fake Implication object for the query
    query = Implication([], query_prop)

    global proposition_indices
    proposition_indices = generate_proposition_indices(propositions)

    # Generate truth table
    truth_table = generate_truth_table(proposition_indices)

    # Evaluate knowledge base using truth table
    evaluate_knowledge_base(knowledge_base, truth_table)

    # print("Knowledge Base:")
    # for implication in knowledge_base:
    #     premises = ' & '.join([prop.symbol for prop in implication.premises])
    #     print(f"{premises} => {implication.conclusion.symbol}")
    # Check entailment of the query using truth table
    is_entailed = check_entailment(query, knowledge_base, truth_table)

    # Write report
    print("Knowledge Base:")
    for implication in knowledge_base:
        premises = ' & '.join([prop.symbol for prop in implication.premises])
        print(f"{premises} => {implication.conclusion.symbol}")

    print("\nIndividual Propositions:")
    for prop in propositions:
        print(prop)

    print("\nQuery:")
    print(query.conclusion.symbol)

    print("\nEntailment Result:")
    if is_entailed:
        print("The query is entailed by the knowledge base.")
    else:
        print("The query is not entailed by the knowledge base.")

if __name__ == "__main__":
    main()

