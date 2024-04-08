# Imports
import utils.token as token

# Constants
OPERATORS = [
    "+",
    "-",
    "*",
    "/",
    "%",
    ">",
    "<",
    "=",
    "!",
    "&",
    "|",
    "^",
    "~",
    "?",
    ":",
    ".",
    ",",
    ";",
    "{",
    "}",
    "[",
    "]",
    "(",
    ")",
]
SINGLE_OPERATORS = ["(", ")", "[", "]", "{", "}", ",", ";", "?", ":", "."]


# Class lexer
class Lexer:
    # Constructor
    def __init__(self, char_stack):
        self.char_stack = char_stack
        self.current_char = ""
        self.tokens = []
        self.current_token = ""
        self.token_type = ""
        self.string_start_char = ""

    # Lex the file char stack
    def lex(self):
        while len(self.char_stack) > 0:
            self.tokenize()

        # Push the token if the current token is not empty
        self.handle_line_return()

        return self.tokens

    # Tokenize
    def tokenize(self):
        self.current_char = self.char_stack[-1]

        # If no token type
        if self.token_type == "":
            # If the current character is a letter
            if self.current_char.isalpha():
                self.handle_identifier()

            # If the current character is a space
            elif self.current_char == " ":
                self.handle_whitespace()

            # If the current character is a newline
            elif self.current_char == "\n":
                self.handle_line_return()

            elif self.char_is_operator(self.current_char):
                self.handle_operator()

            # If the current character is a number
            elif self.char_is_number(self.current_char):
                self.handle_number()

            # If the current character is a string quote
            elif self.current_char in ["'", '"', "`"]:
                self.handle_string()

            # If the current character is not recognized
            else:
                # If the current tokken is not empty
                if self.current_token != "":
                    self.push_token()

                # Handle error
                self.token_type = "error"
                self.current_token = self.current_char
                self.push_token()
                self.char_stack.pop()

        # If token type is identifier
        elif self.token_type == "identifier":
            self.handle_case_identifier()

        # If token type is single line comment
        elif self.token_type == "single_line_comment":
            self.handle_single_line_comment()

        # If token type is multiline comment
        elif self.token_type == "multiline_comment":
            self.handle_multiline_comment()

        # If token type is operator
        elif self.token_type == "operator":
            self.handle_case_operator()

        # If token type is string
        elif self.token_type == "string":
            self.handle_case_string()

        # If token type is number
        elif self.token_type == "number":
            self.handle_case_number()

    # Handle multiline comment
    def handle_multiline_comment(self):
        # If the current character is a comment end
        if self.is_multiline_comment_end(self.current_token):
            self.push_token()

        else:
            self.current_token += self.current_char
            self.char_stack.pop()

    # Handle single line comment
    def handle_single_line_comment(self):
        if self.current_char == "\n":
            self.push_token()
        else:
            self.current_token += self.current_char
            self.char_stack.pop()

    # Handle case operator
    def handle_case_operator(self):
        # If the current character is an operator
        if self.char_is_operator(self.current_char):
            # Check if the current token is a single operator
            if self.char_is_single_operator(self.current_char):
                self.push_token()
                self.handle_parentesis()
            else:
                self.current_token += self.current_char
                self.char_stack.pop()
        else:
            # Error handling
            if token.token_is_operator(self.current_token) == False:
                self.token_type = "error"

            self.push_token()

        # check if the token is a comment
        if self.is_single_comment_start(self.current_token):
            # Check overlap between operator and comment
            first_operator_part = self.current_token[:-2]
            if first_operator_part != "":
                self.current_token = first_operator_part
                self.push_token()
                self.current_token = "//"

            self.token_type = "single_line_comment"

        # check if the token is a multiline comment
        elif self.is_multiline_comment_start(self.current_token):
            # Check overlap between operator and comment
            first_operator_part = self.current_token[:-2]
            if first_operator_part != "":
                self.current_token = first_operator_part
                self.push_token()
                self.current_token = "/*"

            self.token_type = "multiline_comment"

    # Handle operator
    def handle_operator(self):
        self.token_type = "operator"
        self.current_token = self.current_char
        self.char_stack.pop()
        if self.char_is_single_operator(self.current_token):
            self.push_token()

    # Handle parenthesis
    def handle_parentesis(self):
        self.token_type = "parenthesis"
        self.current_token = self.current_char
        self.push_token()
        self.char_stack.pop()

    # Handle case string
    def handle_case_string(self):
        # If the current character is the same as the string start character
        if self.current_char == self.string_start_char:
            self.current_token += self.current_char
            self.char_stack.pop()
            self.push_token()

        # If the current character is an escape character
        elif self.current_char == "\\":
            self.current_token += self.current_char
            self.char_stack.pop()
            if len(self.char_stack) > 0:
                self.current_token += self.char_stack[-1]
                self.char_stack.pop()

        else:
            self.current_token += self.current_char
            self.char_stack.pop()

    # Handle string
    def handle_string(self):
        self.string_start_char = self.current_char
        self.token_type = "string"
        self.current_token += self.current_char
        self.char_stack.pop()

    # Handle case identifier
    def handle_case_identifier(self):
        # If the current char is a valid identifier character
        if (
            self.current_char.isalpha()
            or self.current_char.isdigit()
            or self.current_char == "_"
        ):
            self.current_token += self.current_char
            self.char_stack.pop()

        # If the current char is not a valid identifier character
        else:
            self.push_token()

    # Handle identifier
    def handle_identifier(self):
        self.token_type = "identifier"
        self.current_token += self.current_char
        self.char_stack.pop()

    # Handle case number
    def handle_case_number(self):
        if self.char_is_number(self.current_char) or self.current_char == ".":
            self.current_token += self.current_char
            self.char_stack.pop()
        else:
            self.push_token()

    # Handle number
    def handle_number(self):
        self.token_type = "number"
        self.current_token += self.current_char
        self.char_stack.pop()

    # Handle whitespace
    def handle_whitespace(self):
        # Push the token if the current token is not empty
        if self.current_token != "":
            self.push_token()

        # Push the whitespace character
        self.current_token = " "
        self.token_type = "whitespace"
        self.push_token()
        self.char_stack.pop()

    # Handle line return
    def handle_line_return(self):
        # Push the token if the current token is not empty
        if self.current_token != "":
            self.push_token()

        # Push the newline character
        self.token_type = "newline"
        self.current_token = "\r"
        self.push_token()

        # Pop the character
        if len(self.char_stack) > 0:
            self.char_stack.pop()

    # Push the token
    def push_token(self):
        
        if self.token_type == "identifier":
            
            # Check if identifier is a keyword
            if token.token_is_keyword(self.current_token):
                self.token_type = "keyword"
            
            # Check if identifier is an operator
            elif token.token_is_operator(self.current_token):
                self.token_type = "operator"
            
            # Check if identifier is a constant
            elif token.token_is_constant(self.current_token):
                self.token_type = "constant"

        self.tokens.append({"token": self.current_token, "type": self.token_type})
        
        # Reset the token
        self.current_token = ""
        self.token_type = ""

    # Check if a token is a comment start
    def is_single_comment_start(self, current_token):
        # Get 2 first characters in the token
        return current_token[-2:] == "//"

    # Check if a token is a multiline comment start
    def is_multiline_comment_start(self, current_token):
        # Get 2 first characters in the token
        return current_token[-2:] == "/*"

    # Check if a token is a comment end
    def is_multiline_comment_end(self, current_token):
        # Get 2 last characters in the token
        return current_token[-2:] == "*/"

    # Check if a char is a number
    def char_is_number(self, char):
        return char.isdigit()

    # Check if a character is an operator
    def char_is_operator(self, char):
        return char in OPERATORS

    # Check if a character is a single operator
    def char_is_single_operator(self, char):
        return char in SINGLE_OPERATORS
