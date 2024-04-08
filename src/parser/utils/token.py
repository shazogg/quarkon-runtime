# Constants
KEYWORDS = [
    "let",
    "const",
    "if",
    "else",
    "elif",
    "while",
    "for",
    "function",
    "class",
    "return",
    "break",
    "continue",
    "import",
    "export",
    "exports",
    "delete",
    "assert",
    "try",
    "catch",
    "finally",
    "raise",
    "new",
]
INLINE_KEYWORDS = [
    "let",
    "const",
    "return",
    "break",
    "continue",
    "raise",
    "assert",
    "delete",
    "export",
    "exports",
    "import",
    "new",
]
KEYWORDS_OPERATORS = [
    "is",
    "in",
    "as",
    "from",
]
KEYWORDS_CONSTANTS = [
    "true",
    "false",
    "null",
    "undefined",
]
LEFT_ASSOCIATIVE_OPERATORS = [
    "+",
    "-",
    "*",
    "/",
    "%",
    "==",
    "!=",
    ">",
    ">=",
    "<",
    "<=",
    "is",
    "in",
    "&&",
    "||",
    "!",
    "&",
    "|",
    "^",
    "~",
    "<<",
    ">>",
    "?",
    ".",
]
ARITHMETIC_OPERATORS = ["+", "-", "*", "/", "%", "**"]
ASSIGNMENT_OPERATORS = [
    "=",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "**=",
    "&=",
    "|=",
    "^=",
    ">>=",
    "<<=",
]
COMPARISON_OPERATORS = ["==", "!=", ">", "<", ">=", "<="]
LOGICAL_OPERATORS = ["&&", "||", "!"]
BITWISE_OPERATORS = ["&", "|", "^", "~", ">>", "<<"]
SPECIAL_OPERATORS = ["?", ":", "=>", "->", "...", "."]


# Get the priority of an operator
def token_get_operator_priority(operator):
    if operator in [
        "=",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "**=",
        "&=",
        "|=",
        "^=",
        ">>=",
        "<<=",
    ]:
        return 0
    elif operator in ["==", "!=", ">", ">=", "<", "<=", "is", "in", ":", "?"]:
        return 1
    elif operator in ["+", "-"]:
        return 2
    elif operator in ["*", "/", "%"]:
        return 3
    elif operator in ["**"]:
        return 4
    elif operator in ["&&", "||", "!"]:
        return 5
    elif operator in ["&", "|", "^", "~", "<<", ">>", "."]:
        return 6
    elif operator in ["is", "in", "as", "from"]:
        return 7
    else:
        return -1


# Check if an operator is left associative
def token_operator_is_left_associative(operator):
    return operator in LEFT_ASSOCIATIVE_OPERATORS


# Check if a identifier is a keyword
def is_identifier_keyword(identifier):
    return identifier in KEYWORDS


# Check if a identifier is an inline keyword
def is_identifier_inline_keyword(identifier):
    return identifier in INLINE_KEYWORDS


# Check if a token is an operator
def token_is_operator(token):
    if token in ARITHMETIC_OPERATORS:
        return "arithmetic"
    elif token in ASSIGNMENT_OPERATORS:
        return "assignment"
    elif token in COMPARISON_OPERATORS:
        return "comparison"
    elif token in LOGICAL_OPERATORS:
        return "logical"
    elif token in BITWISE_OPERATORS:
        return "bitwise"
    elif token in SPECIAL_OPERATORS:
        return "special"
    elif token in KEYWORDS_OPERATORS:
        return "keyword"
    else:
        return False


# Check if a token is a constant
def token_is_constant(token):
    return token in KEYWORDS_CONSTANTS


# Check if a token is a keyword
def token_is_keyword(token):
    return token in KEYWORDS
