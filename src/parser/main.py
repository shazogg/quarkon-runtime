# Imports
import sys
import json
import utils.tree as tree
import lexer.lexer as lexer
import parser.parser as parser


# Main function
def main():
    # Check if the main file path is provided
    if len(sys.argv) < 3:
        print("Usage: python main.py <main_file_path> <output_file_path> [--dot]")
        return
    # Get the main file path
    main_file_path = sys.argv[1]

    # Get the output file path
    output_file_path = sys.argv[2]

    char_stack = []
    # Read the main file
    with open(main_file_path, "r", encoding="utf-8") as file:
        while True:
            char = file.read(1)

            # Break if the character is empty
            if not char:
                break

            # Append the character to the stack
            char_stack.append(char)

    # Reverse the stack
    char_stack.reverse()

    # Lex the main file
    main_file_lexer = lexer.Lexer(char_stack)
    tokens = main_file_lexer.lex()

    # Parse the tokens
    main_file_parser = parser.Parser(encoding="utf-8")
    tree_root = main_file_parser.parse(tokens, optimise=True)

    # Visualize the tree as json
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(tree_root, separators=(",", ":")))

    if "--dot" in sys.argv:
        index = sys.argv.index("--dot")
        if index + 1 < len(sys.argv):
            # Generate the tree with optimisation
            tree_root = main_file_parser.parse(tokens)

            # Generate DOT file to visualize the tree
            tree.generate_dot_file(sys.argv[index + 1], tree_root)

        else:
            print("Please provide the output file path for the DOT file!")


# Run the main function
if __name__ == "__main__":
    main()
