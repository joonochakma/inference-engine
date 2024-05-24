import sys
import subprocess

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    content = read_file(filename)
    if not content:
        sys.exit(1)

    python_executable = sys.executable

    if method == 'FC':
        subprocess.run([python_executable, "FC.py", filename])
    elif method == 'BC':
        subprocess.run([python_executable, "BC.py", filename])
    elif method == 'TT':
        subprocess.run([python_executable, "TT.py", filename])
    else:
        print(f"Error: Unknown method '{method}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
