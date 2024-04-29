import sys

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

if __name__ == "__main__":
    # Check if the filename is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python script.py filename")
        sys.exit(1)

    filename = sys.argv[1]
    content = read_file(filename)
    if content:
        print("File contents:")
        print(content)
