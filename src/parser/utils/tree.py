# Imports
import utils.stack as stack
import utils.queue as queue

# 8 bits
# bit 7:

# Constants
TOKENS = {
    "root": 0,
}


# Build the expression tree
def build_expression_tree(rpn_tokens, optimise=False):
    tree_stack = []

    for current_token in rpn_tokens:

        # The token is a number or a string or an identifier
        if current_token["type"] in ["number", "string", "identifier", "constant"]:
            # Create a number node
            node = create_node(
                current_token["token"],
                (
                    current_token["type"]
                    if not optimise
                    else type_optimise(current_token["type"])
                ),
                optimise,
            )

            # If optimise
            if optimise:
                node = [node[0], node[1]]

            stack.push(
                tree_stack,
                node,
            )

        # The token is a function or an array or a dictionary or a keyword
        elif current_token["type"] in [
            "function",
            "function_call",
            "array",
            "dictionary",
            "keyword",
        ]:
            # Create a node
            node = create_node(
                current_token["token"],
                (
                    current_token["type"]
                    if not optimise
                    else type_optimise(current_token["type"])
                ),
                optimise,
            )
            for child in current_token["children"]:
                queue.push(
                    node["children"] if not optimise else node[2],
                    build_expression_tree(child, optimise),
                )

            # If no childend remove the array
            if optimise and len(node[2]) == 0:
                node = [node[0], node[1]]

            # Push the node to the stack
            stack.push(tree_stack, node)

        else:
            # Create an operator node
            node = create_node(
                current_token["token"],
                "operator" if not optimise else type_optimise("operator"),
                optimise,
            )
            expression2 = stack.pop(tree_stack)
            expression1 = stack.pop(tree_stack)
            queue.push(node["children"] if not optimise else node[2], expression1)
            queue.push(node["children"] if not optimise else node[2], expression2)
            stack.push(tree_stack, node)

    return stack.top(tree_stack)


# Optimise the expression tree type
def type_optimise(type):
    # return the pos in array
    types = [
        "number",
        "string",
        "identifier",
        "constant",
        "function",
        "function_call",
        "array",
        "dictionary",
        "keyword",
        "operator",
    ]
    return types.index(type) + 1  # +1 because 0 is reserved for the root node


# Create a node
def create_node(node_value, node_type, optimise=False):
    if optimise:
        return [node_value, node_type, []]

    else:
        return {
            "value": node_value,
            "type": node_type,
            "children": [],
        }


# Generate DOT file
def generate_dot_file(filename, tree_root, encoding="utf-8"):
    with open(filename, "w", encoding=encoding) as dot_file:
        dot_file.write("digraph Tree {\n")
        traverse_and_write_dot(tree_root, dot_file)
        dot_file.write("}\n")


# Traverse the tree and write nodes and edges to DOT file
def traverse_and_write_dot(node, dot_file, node_id=0):
    if node:
        # Generate a unique identifier for this node
        current_node_id = node_id
        node_id += 1

        # Write the current node
        if node["type"] == "string":
            # remove first and last character and replace with backslash
            string_char = node["value"][0]
            node["value"] = node["value"][1:-1]
            node["value"] = "\\" + string_char + node["value"] + "\\" + string_char

        dot_file.write(
            f'N{current_node_id} [label="{node["value"]} : {node["type"]}"];\n'
        )

        # Write edges to all children
        for child in node["children"]:
            dot_file.write(f"N{current_node_id} -> N{node_id}\n")

            # Recursively write children
            node_id = traverse_and_write_dot(child, dot_file, node_id)

    return node_id
