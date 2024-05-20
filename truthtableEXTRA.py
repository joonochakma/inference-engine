import itertools
import re
import sys

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

def parse_input(file_content):
    sections = file_content.strip().split("ASK")
    tell_section = sections[0].replace("TELL", "").strip()
    ask_section = sections[1].strip()
    
    sentences = [s.strip() for s in tell_section.split(";") if s.strip()]
    ask_proposition = ask_section.strip()
    
    return sentences, ask_proposition

def get_propositions(sentences):
    propositions = set()
    for sentence in sentences:
        matches = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', sentence)
        propositions.update(matches)
    return sorted(propositions)

def generate_truth_table(propositions):
    return list(itertools.product([False, True], repeat=len(propositions)))

def convert_expression(expression):
    expression = expression.replace("<=>", "==")
    expression = expression.replace("=>", "<=")
    expression = expression.replace("&", " and ")
    expression = expression.replace("||", " or ")
    expression = re.sub(r'~(\w+)', r'(not \1)', expression)
    return expression

def evaluate_expression(expression, truth_assignment):
    for prop, value in truth_assignment.items():
        expression = re.sub(r'\b' + re.escape(prop) + r'\b', str(value), expression)
    expression = convert_expression(expression)
    return eval(expression)

def evaluate_sentences(sentences, truth_assignment):
    evaluated_sentences = []
    for sentence in sentences:
        evaluated_sentences.append(evaluate_expression(sentence, truth_assignment))
    return all(evaluated_sentences)

def main(file_content):
    sentences, ask_proposition = parse_input(file_content)
    propositions = get_propositions(sentences + [ask_proposition])
    truth_table = generate_truth_table(propositions)
    
    entailment = True
    counter = 0
    conjunction = " and ".join(sentences)  # Create a conjunction of all TELL sentences

    for row in truth_table:
        truth_assignment = dict(zip(propositions, row))
        if evaluate_expression(conjunction, truth_assignment):  # Evaluate the conjunction of TELL sentences
            if not evaluate_expression(ask_proposition, truth_assignment):  # Check if ASK proposition is False
                entailment = False
                break
            counter +=1
        else:
            continue
        
    if entailment:
        print(f"YES: {counter}")
    else:
        print("NO")

# Example usage

if len(sys.argv) != 2:
    print("Usage: python script.py filename")
    sys.exit(1)

filename = sys.argv[1]
file_content = read_file(filename)

if file_content is not None:
    main(file_content)
